"""
Script which contains all the simulations functions from NCSim.

# NOTE: This script adheres to the control package convention on time series
# FROM: https://python-ct.readthedocs.io/en/latest/conventions.html#time-series-convention
"""

# Import packages
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)  # Filter future warning, to prevent CVXPY from complaining
import numpy as np
import scipy as sp
import control as ct
import cvxpy as cvx
import functools
from functions import utils
from typing import Any, Callable, Literal, TypeVar, TypeAlias
import numpy.typing as npt

# Create an abbreviation for the type hint "npt.NDArray[Any, np.dtype[dtype]]"
# FROM: https://stackoverflow.com/questions/49887430/can-i-make-type-aliases-for-type-constructors-in-python-using-the-typing-module  # nopep8
# FROM: https://stackoverflow.com/questions/41914522/mypy-is-it-possible-to-define-a-shortcut-for-complex-type  # nopep8
T = TypeVar('T', int, float, complex, bool)
NPArray: TypeAlias = npt.NDArray[np.dtype[T]]

# ----------- MAIN SIMULATION METHOD ------------


def sim(sys_ol: ct.StateSpace, sys_cont: ct.StateSpace | None, T_end: float | int, x_0: NPArray[float], values_to_return: tuple[str, ...] = ('X',), sampling_mode: Literal['TTC', 'CETC', 'PETC', 'STC'] = 'TTC', sampling_params: tuple[str, ...] | None = None, hold_params: tuple[str, ...] | None = None, noise_matrices: tuple[NPArray[float] | None, NPArray[float] | None] | None = None, noise_params: tuple[str, ...] | None = None, reference_params: tuple[str, ...] | None = None, observer_params: tuple[str, ...] | None = None, attack_params: tuple[str, ...] | None = None, break_params: tuple[str, ...] | None = None, random_seed: int | None = None, inter_sample_res_ct: float | int = 10) -> tuple[NPArray[float], ...]:
    """
    # NOTE: This function assumes negative feedback interconnection
    # NOTE: The controller must be a digital controller, i.e. discrete-time
    # FIXME: The above does not work: if we are dealing with a STC mechanism which computes irregular sampling times, i.e. not equidistant?
    # TODO: We must make a clear destination on what T_end represents based on the datatype. If it is an integer, then I suggest T_end is the amount of sampling instants, so not the amount of event/transmission instants
    # FIXME: When signals are missing, such as a state-less, static full-state feedback controller, do we want the signals of dimension 0 (which means we can run into indexing problems) or of dimension 1 (which means a index which should actually not be there)
    # TODO: Maybe store all the signals in a dictionary: that way, we can pass the dictionary directly to functions? 
    # FIXME: We have to make it do something smart if the STC implementation is equidistant, because the we can do something different
    # FIXME: Use True as a sampling time for event-triggered controllers, and if h > 0 then the sampling times generated must match exactly.
    # TODO: Make sure that all the systems have the correct names

    Version: 0.1.0
    """

    def check_arguments():
        # ------ ERRORS ------
        # E1 | Check if the feedforward matrix D is empty
        if (sys_ol.D != 0).any():
            raise NotImplementedError("The feedforward matrix D must contain only zero entries (algebraic loop solver not implemented)")
        # E2 | Check if the sampling mode is not CETC
        if sampling_mode == 'CETC':
            raise NotImplementedError(f"CETC is not implemented")
        # E3 | Check if the STC policy is compatible with the time base of the controller 
        pass
        # TODO: Check the mapping of the functions using 'from inspect import signature'
        # ------ WARNING ------
        # W1 | Warn if the closed-loop dynamics are unstable
        # FIXME: Add checks
        # ------ NAMING ------
        # N1 | Name the signals for the open-loop plant
        sys_ol.name = 'plant'
        sys_ol.set_states([f"x[{i}]" for i in range(sys_ol.nstates)])
        sys_ol.set_inputs([f"u[{i}]" for i in range(sys_ol.ninputs)])
        sys_ol.set_outputs([f"y[{i}]" for i in range(sys_ol.noutputs)])
        # N2 | Name the signals for the controller
        # FIXME: We need to change this naming convention
        sys_cont.name = 'controller'
        sys_cont.set_states([f"c[{i}]" for i in range(sys_cont.nstates)])
        sys_cont.set_inputs([f"e[{i}]" for i in range(sys_cont.ninputs)])
        sys_cont.set_outputs([f"u[{i}]" for i in range(sys_cont.noutputs)])
        

    def check_terminate_cond(sim_in_progress: bool) -> bool:
        # TODO: Do all these checks based on whether the system is sampled-data system or discrete-time
        #: Check if there are break conditions
        if break_params is not None:
            #: Extract the break condition
            break_condition, *_ = break_params
            #: Match the break condition
            match break_condition:
                case '2_norm':
                    #: Extract the tolerance
                    _, norm_tol = break_params
                    #: Check if the norm is exceeded
                    if np.linalg.norm(sgnl['X'][-1], ord=2) >= norm_tol:
                        warnings.warn(f"Simulation was ended prematurely due to norm constraints after {sgnl['T'][-1]:.2f} time units ({np.floor(100 / (T_end / sgnl['T'][-1])).astype(int):d}%)", RuntimeWarning, stacklevel=3)
                        sim_in_progress = False
                case _:
                    raise ValueError(f"Unknown break condition '{break_condition}'")
        #: Check if the runtime is exceeded
        match T_end:
            case int():
                #: Check if number of sampling instants are exceeded
                if len(sgnl['Y_k']) >= T_end:
                    sim_in_progress = False
            case float():
                #: Check if the simulation time is exceeded
                if sgnl['T'][-1] >= T_end:
                    sim_in_progress = False
            case _:
                raise ValueError(f"T_end must be of type float or int, received '{type(T_end)}'")
        #: Return the results
        return sim_in_progress
    
    def initialize_signals() -> dict:
        #: Create non-empty signals
        x, x_hat, x_cont, x_obsv_cont = [x_0], [np.zeros(n_x) if observer_params is not None else np.array([])], [np.zeros(sys_cont.nstates)], [np.zeros(sys_obsv.nstates + sys_cont.nstates)]
        #: Create a dictionary
        # TODO: Maybe rename Y_i_prime to Y_i_received?
        dict_signals = {'T': T, 'T_i': [], 'T_k': [], 'K': [0], 'Tau_i': [0], 'Kappa_i': [0], 'X': x, 'X_hat': x_hat, 'X_cont': x_cont, 'X_obsv_cont': x_obsv_cont, 'U_i': [], 'U_a': [], 'U_i_prime': [], 'U_i_hold': [], 'Y': [], 'Y_k': [], 'Y_i': [], 'Y_a': [], 'Y_i_prime': [], 'Ref': [], 'W': [], 'V': [], 'E': []}
        #: Return the results
        return dict_signals
    
    def transmit_output() -> bool:
        #: Match the sampling mode
        match sampling_mode:
            case 'TTC' | 'STC':
                #: Always sample 
                return True
            case 'CETC' | 'PETC':
                #: Check if this is the first sample time
                if sgnl['T'][-1] == 0:
                    return True
                #: Check if the triggering conditions holds
                to_sample = etc_trigger_func(sgnl)
                #: Return the result
                return to_sample
            
    def no_process_noise(sgnl: dict) -> NPArray[float]:
        #: Create a zero vector
        w = np.zeros(n_x)
        #: Return the result
        return w
    
    def construct_process_noise(T_inter: NPArray[float]) -> NPArray[float]:
        #: Initialize the empty array
        W_inter = np.zeros((n_x, T_inter.size))
        #: Loop over all elements in this set
        for idx in range(W_inter.shape[1]):
            #: Check if the process noise function is defined
            if procces_noise_func is not None:
                #: Retrieve the noise vector
                W_inter[:, idx] = procces_noise_func(sgnl)
            else:
                #: Empty noise vector
                W_inter[:, idx] = np.zeros(n_x)
        #: Return the result
        return W_inter
    
    def construct_reference(T_inter: NPArray[float]) -> NPArray[float]:
        #: Initialize the empty array
        Ref_inter = np.zeros((n_x_hat, T_inter.size))
        # FIXME: This does not take into account the future times
        for idx in range(Ref_inter.shape[1]):
            #: Retrieve the reference params
            Ref_inter[:, idx] = ref_func(sgnl)
        #: Return the result
        return Ref_inter


    #: Check the arguments
    check_arguments()
    # ------ INITIALIZE ------
    #: Set the random seed
    if random_seed is not None:
        np.random.seed(random_seed)
    #: Retrieve dimensions and simulation parameters
    # TODO: Actually, instead of looking at the controller, we should first deduce if the plant is discrete-time
    # FIXME: Actually the controller should not determine the sampling time: solely the sampling mechanism should
    n_x, n_u, n_y = sys_ol.nstates, sys_ol.ninputs, sys_ol.noutputs
    #: Check if the contr
    #: Get the simulation time
    T = get_simulation_time_array(sys_ol, sys_cont, T_end)
    #: Create a noise augmented system
    sys_ol_u_w_v = get_noise_augmented_system(sys_ol, noise_matrices)
    #: Initialize auxiliary systems
    sys_obsv = get_observer(sys_ol, sys_cont.dt, observer_params)
    #: Initialize auxiliary functions
    stc_pred_func = sampling_params[0] if sampling_mode == 'STC' else None
    etc_trigger_func = sampling_params[0] if sampling_mode in ('PETC','CETC') else None
    attack_gen_func = get_attack_signal(T_end, attack_params) if attack_params is not None else None
    # FIXME: This is not correct, because noise_params can be very different. It must either be a function, or some descriptive text, such as 'Gaussian'
    if noise_params is not None:
        if noise_params[0] == 'custom':
            # TEMP
            print(f"Custom")
            procces_noise_func = noise_params[1]
        else:
            procces_noise_func = functools.partial(get_noise_signal, 'process_noise', sys_ol, noise_params)
    else:
        procces_noise_func = no_process_noise
    #: Retrieve the hold function
    construct_hold_signal = get_hold_signal(hold_params)
    #: Retrieve other dimensions
    # TODO: Make this nice
    n_x_hat = sys_obsv.noutputs
    sum_block = ct.ss([], [], [], np.hstack((np.eye(n_x_hat), -np.eye(n_x_hat))))
    sum_block.name = 'sum_block'
    sum_block.set_inputs([f"r[{i}]" for i in range(n_x_hat)] + [f"x_hat_or_y[{i}]" for i in range(n_x_hat)])
    sum_block.set_outputs([f"e[{i}]" for i in range(n_x_hat)])
    sys_obsv_cont = ct.interconnect([sys_cont, sys_obsv, sum_block], inputs=[f"r[{i}]" for i in range(n_x_hat)] + [f"y_trans[{i}]" for i in range(sys_ol.noutputs)], outputs=[f"u[{i}]" for i in range(sys_ol.ninputs)] + [f"x_hat_or_y[{i}]" for i in range(sys_obsv.nstates)])
    sys_obsv_cont.name = 'observer_controller'
    #: Retrieve the reference function
    ref_func = get_reference_signal(n_x_hat, reference_params)
    #: Retrieve the time base for all systems
    h_plant, h_cont = sys_ol.dt, sys_cont.dt
    #: Check the case
    if stc_pred_func is not None:  # STC
        h_samp = stc_pred_func.dt
    elif etc_trigger_func is not None:  # ETC
        h_samp = etc_trigger_func.dt
    else:  # TTC
        h_samp = h_cont
    #: Initialize all signals
    sgnl = initialize_signals() 
    #: Start the simulation loop 
    sim_in_progress = True
    # ------ START SIM ------
    while sim_in_progress:
        # 0 | Generate measurement noise signal
        sgnl['V'] += [get_noise_signal('measurement_noise', sys_ol, noise_params, sgnl)]
        # 1 | Calculate current output
        u_0_v = np.concatenate((np.zeros(n_u), np.zeros(n_x), sgnl['V'][-1]))
        sgnl['Y'] += [sys_ol_u_w_v.output(0, sgnl['X'][-1], u_0_v)]
        sgnl['T_k'] += [sgnl['T'][-1]]
        # 2 | Append the sampled output
        sgnl['Y_k'] += [sgnl['Y'][-1]]
        # 3a | Check if the sampled output needs to be transmitted
        if transmit_output():
            sgnl['Y_i'] += [sgnl['Y_k'][-1]]
            sgnl['T_i'] += [sgnl['T'][-1]]
        # 3b | Check if the sampled output is attacked
        if attack_params is None:
            sgnl['Y_i_prime'] += [sgnl['Y_i'][-1]]
        else:
            sgnl['Y_a'] += [attack_gen_func('S2C', sgnl)]
            sgnl['Y_i_prime'] += [sgnl['Y_i'][-1] + sgnl['Y_a'][-1] if sgnl['Y_a'][-1].size > 0 else sgnl['Y_i'][-1]]
        # 4 | Calculate the current reference
        sgnl['Ref'] += [ref_func(sgnl)]
        # 5 + 6 | Calculate the current input and the current estimated state
        r_y = np.concatenate((sgnl['Ref'][-1], sgnl['Y_i_prime'][-1]))
        u_x_hat = sys_obsv_cont.output(0, sgnl['X_obsv_cont'][-1], r_y)
        sgnl['U_i'] += [u_x_hat[:n_u]]
        sgnl['X_hat'] += [u_x_hat[n_u:]]
        # 7 | Calculate the next sampling instance
        # TODO: Maybe also move this to a separate method?
        # NOTE: Now, Kappa_i and Tau_i always contains one more entry: it gives a prediction on when to sample next
        match sampling_mode:
            case 'TTC' | 'PETC' | 'CETC':
                sgnl['Kappa_i'] += [1]
                sgnl['Tau_i'] += [h_samp]
            case 'STC':
                #: Retrieve the predicted value
                pred_val = stc_pred_func(sgnl)
                #: Match the datatype
                match pred_val:
                    case int():
                        sgnl['Kappa_i'] += [pred_val]
                        sgnl['Tau_i'] += [h_samp * pred_val]
                    case float():
                        sgnl['Tau_i'] += [pred_val]
                    case _:
                        raise ValueError(f"The value returned by the STC predictor should be either an int or a float, received '{type(pred_val)}'") 
        # 8 | Calculate the transmitted output
        if attack_params is None:
            sgnl['U_i_prime'] += [sgnl['U_i'][-1]]
        else:
            sgnl['U_a'] += [attack_gen_func('C2A', sgnl)]
            sgnl['U_i_prime'] += [sgnl['U_i'][-1] + sgnl['U_a'][-1] if sgnl['U_a'][-1].size > 0 else sgnl['U_i'][-1]]
        # sgnl['W'] += [get_noise_signal('process_noise', sys_ol, noise_params, sgnl)]
        sgnl['W'] += [procces_noise_func(sgnl)]
        # # # TEMP
        # print(sgnl['W'][-1])
        # 8b | Calculate the hold output
        sgnl['U_i_hold'] += [construct_hold_signal(sgnl)]
        # 9b | Calculate the next state(s) (and outputs) of the plant
        # TODO: Maybe wrap this in a separate method
        u_w_0 = np.concatenate((sgnl['U_i_hold'][-1], sgnl['W'][-1], np.zeros(n_y)))
        if sys_ol.dt == 0:  # Continuous-time
            T_inter = np.linspace(sgnl['T'][-1], sgnl['T'][-1] + sgnl['Tau_i'][-1], inter_sample_res_ct + 1)
            # 9a | Generate the process noise signal
            # FIXME: Now we cannot make the disturbance state-dependent, as it is made in advance: maybe we want to change that? Or at least implement it in discrete-time?
            U_0_inter = np.tile(sgnl['U_i_hold'][-1][:, np.newaxis], (1, T_inter.size))
            W_inter = construct_process_noise(T_inter)
            # # TEMP
            # print(f"------ W_inter ------")
            # print(W_inter)
            # FIXME: This thing below is also incorrect, as here we also need to make V not constant
            V_inter = np.tile(np.zeros(n_y)[:, np.newaxis], (1, T_inter.size))
            U_inter = np.vstack((U_0_inter, W_inter, V_inter))
            _, Y_inter, X_inter = ct.forced_response(sys_ol_u_w_v, T=T_inter, U=U_inter, X0=sgnl['X'][-1], return_x=True)
            # # TEMP
            # print(f"------ X_inter ------")
            # print(X_inter)
        elif sys_ol.dt == True or sys_ol.dt > 0:  # Discrete-time
            T_inter = np.linspace(sgnl['T'][-1], sgnl['T'][-1] + h_cont * sgnl['Kappa_i'][-1], sgnl['Kappa_i'][-1] + 1)
            # FIXME: This is not correct, because the noise is constant now
            U_inter = np.tile(u_w_0[:, np.newaxis], (1, T_inter.size))
            _, Y_inter, X_inter = ct.forced_response(sys_ol_u_w_v, U=U_inter, X0=sgnl['X'][-1], return_x=True)
        else:
            raise ValueError(f"Unknown time base of the plant '{sys_ol.dt}'")
        # 10 + 11 | Calculate the next state(s) (and outputs) of the controller and auxiliary systems
        if sys_obsv_cont.dt == 0:  # Continuous-time
            raise NotImplementedError(f"Continuous-time controllers are not yet supported")
        elif sys_obsv_cont.dt == True:  # Discrete-time (event-triggered)
            #: Retrieve the intermediate values
            Ref_current = sgnl['Ref'][-1]
            Y_i_current = sgnl['Y_i'][-1]
            U_obsv_cont_current = np.concatenate((Ref_current, Y_i_current))
            #: Compute a single step update
            X_obsv_cont_next = sys_obsv_cont.dynamics(t=0, x=sgnl['X_obsv_cont'][-1], u=U_obsv_cont_current)
            X_obsv_cont_inter = np.hstack((sgnl['X_obsv_cont'][-1][:, np.newaxis], X_obsv_cont_next[:, np.newaxis])) 
        elif sys_obsv_cont.dt > 0:  # Discrete-time (time-triggered)
            T_obsv_cont_inter = np.linspace(sgnl['T'][-1], sgnl['T'][-1] + h_cont * sgnl['Kappa_i'][-1], sgnl['Kappa_i'][-1] + 1)
            Ref_inter = construct_reference(T_obsv_cont_inter)
            Y_i_inter = np.tile(sgnl['Y_i'][-1][:, np.newaxis], (1, T_obsv_cont_inter.size))
            U_obsv_cont_inter = np.vstack((Ref_inter, Y_i_inter))
            _, _, X_obsv_cont_inter = ct.forced_response(sys_obsv_cont, U=U_obsv_cont_inter, X0=sgnl['X_obsv_cont'][-1], return_x=True)
        else:
            raise ValueError(f"Unknown time base of the controller '{sys_obsv_cont.dt}'")
        # 12a | Append the discrete-time value
        if sampling_mode in ('TTC', 'PETC'):
            sgnl['K'] += [sgnl['K'][-1] + sgnl['Kappa_i'][-1]]
        # 12b | Append the next states
        # FIXME: Do we also not need to consider the input? Like to continuous-time input?
        sgnl['T'] += [int(t) if (isinstance(h_cont, int) and not isinstance(h_cont, bool)) else t for t in T_inter[1:]]
        sgnl['X'] += [x for x in X_inter[:, 1:].T]
        sgnl['Y'] += [y for y in Y_inter[:, 1:-1].T]
        # 12c | Append the next states
        # FIXME: What about the controller time?
        sgnl['X_obsv_cont'] += [x for x in X_obsv_cont_inter[:, 1:].T]
        #: Check the break condition
        sim_in_progress = check_terminate_cond(sim_in_progress)
    # ------ END SIM ------ 
    #: Convert the data to time series format
    dict_values = get_dictionary_values_to_time_series(sgnl)
    #: Create the outputs in the order they are requested
    outputs = get_output_based_on_names(values_to_return, dict_values)
    #: Return the results
    return outputs


def get_dictionary_values_to_time_series(dict_values: dict) -> dict:
    # TODO: If an array contains a single value (i.e. zero), then remove it and return an empty array
    #: Loop over all values
    for name, value in dict_values.items():
        value = np.array(value)
        dict_values[name] = value.T  # To comply with Python's control package
    #: Return the dictionary
    return dict_values


def get_output_based_on_names(return_values: tuple[str, ...], dict_values: dict) -> list:
    #: Convert the return values to a list
    return_values = list(return_values)
    #: Create an empty list
    outputs = []
    #: Loop over all return values
    for key in return_values:
        #: Add value from key
        outputs.append(dict_values.get(key))
        if dict_values.get(key) is None:
            warnings.warn(f"Variable name '{key}' not found, returning None", Warning, stacklevel=3)
    #: Check is output is a single entry
    if len(outputs) == 1:
        outputs = outputs[0]
    #: Return the list
    return outputs


# ------------ SYSTEMS AND SIGNALS ------------


def get_simulation_time_array(sys_ol: ct.StateSpace, sys_cont: ct.StateSpace, T_end: float | int) -> list:
    # TODO: Based on the type of system, i.e. continuous-time of discrete-time, create an appropriate time vector. Maybe also base this on TTC, PETC, STC and CETC implementation?
    #: Extract the discrete-time step
    h = sys_ol.dt
    #: Check if the system is discrete-time, and set sampling instants to 1
    if h:  # check if h is True
        h = 1
    #: Create the simulation time
    T = [0]  # Simulation time
    #: Return the simulation time
    return T


def get_noise_augmented_system(sys_ol: ct.StateSpace, noise_matrices: tuple[NPArray[float] | None, NPArray[float] | None] | None) -> ct.StateSpace:
    #: Check which augmented matrices need to be created
    if noise_matrices is not None:
        #: Retrieve the noise input array matrices
        B_w, D_v = noise_matrices[0], noise_matrices[1]
        #: Augment the original system (with the available matrices)
        if B_w is not None and D_v is not None:
            pass
        elif B_w is None:
            #: Create empty process noise input matrix
            B_w = np.zeros((sys_ol.nstates, sys_ol.nstates))
        elif D_v is None:
            #: Create empty measurement noise input matrix
            D_v = np.zeros((sys_ol.noutputs, sys_ol.noutputs))
    else:
        #: Create empty process and measurement noise input matrices
        B_w, D_v = np.zeros((sys_ol.nstates, sys_ol.nstates)), np.zeros((sys_ol.noutputs, sys_ol.noutputs))
    #: Retrieve the system parameters
    A, B, C, D, h, n_x, n_y = sys_ol.A, sys_ol.B, sys_ol.C, sys_ol.D, sys_ol.dt, sys_ol.nstates, sys_ol.noutputs
    #: Augment the system
    B_u_w_v = np.hstack((B, B_w, np.zeros((n_x, D_v.shape[1]))))
    D_u_w_v = np.hstack((D, np.zeros((n_y, B_w.shape[1])), D_v))
    sys_ol_u_w_v = ct.StateSpace(A, B_u_w_v, C, D_u_w_v, h)
    #: Return the noise-augmented system
    return sys_ol_u_w_v


def get_observer(sys_ol: ct.StateSpace, h: float, observer_params: tuple[str, ...]) -> ct.StateSpace:

    #: Extract the observer params
    if observer_params is not None:
        observer_type, *_ = observer_params
    else:
        observer_type = None
    #: Match the observer times
    match observer_type:
        case None:
            #: Extract the system parameters
            n_y = sys_ol.noutputs
            #: Construct a unity-gain observer
            # NOTE: The input to the observer is [u(k), y(k)]
            sys_obsv = ct.ss([], [], [], np.hstack((np.zeros(n_y)[:, np.newaxis], np.eye(n_y))), dt=h)
            #: Set the naming of observer
            # FIXME: Change this naming convention in something sensible
            sys_obsv.name = 'observer'
            sys_obsv.set_states([f"x_hat[{i}]" for i in range(sys_obsv.nstates)])
            sys_obsv.set_inputs([f"u[{i}]" for i in range(sys_ol.ninputs)] + [f"y_trans[{i}]" for i in range(sys_ol.noutputs)])
            sys_obsv.set_outputs([f"x_hat_or_y[{i}]" for i in range(sys_obsv.noutputs)])
        case 'almeida_observer':
            #: Extract the observer parameters
            _, h, kappa_ubar = observer_params
            #: Extract the system params 
            n_x, n_u, n_y = sys_ol.nstates, sys_ol.ninputs, sys_ol.noutputs
            #: Perform discretization
            if sys_ol.dt == 0:
                sys_ol_dt = sys_ol.sample(Ts=h, method='zoh')
            else:
                sys_ol_dt = sys_ol
            #: Retrieve the static observer gain
            L = get_static_observer_gain_almeida(sys_ol_dt, kappa_ubar)
            #: Construct a steady-state Kalman filter/Luenberger observer
            sys_obsv = ct.StateSpace((sys_ol_dt.A - L @ sys_ol_dt.C), np.hstack((sys_ol_dt.B - L @ sys_ol_dt.D, L)), np.eye(n_x), np.zeros((n_x, n_u + n_y)), dt=True)
            #: Set the naming of the observer
            # FIXME: Change this naming convention in something sensible
            sys_obsv.name = 'observer'
            sys_obsv.set_states([f"x_hat_or_y[{i}]" for i in range(sys_obsv.nstates)])
            sys_obsv.set_inputs([f"u[{i}]" for i in range(sys_ol.ninputs)] + [f"y_trans[{i}]" for i in range(sys_ol.noutputs)])
            sys_obsv.set_outputs([f"x_hat_or_y[{i}]" for i in range(sys_obsv.noutputs)])
        case _:
            raise ValueError(f"Unknown observer type '{observer_type}'")
    #: Return the result
    return sys_obsv


def get_noise_signal(process_or_measurement_noise: Literal['process_noise', 'measurement_noise'], sys_ol: ct.StateSpace, noise_params: Any | None, sgnl: dict) -> NPArray[float]:
    # FIXME: Actually this should all be separate methods which only take in process_or_measurement_noise, instead of one method for all. And the wrapper function does not need to take sgnl

    def compute_bounds_truncated_normal(mu: NPArray[float], var: NPArray[float], confidence_interval: tuple[float, float]) -> tuple[NPArray[float], NPArray[float]]:
        #: Initialize the arrays
        bounds = np.zeros((mu.size, 2))
        #: Compute bounds
        for idx in range(mu.size):
            bounds[idx, :] = sp.stats.norm.ppf(confidence_interval, loc=mu[idx], scale=np.sqrt(var[idx]))
        #: Convert these to number of standard deviations from the mean (which are used in truncnorm)
        bounds[:, 0], bounds[:, 1] = (bounds[:, 0] - mu) / np.sqrt(var), (bounds[:, 1] - mu) / np.sqrt(var)
        #: Return the bounds
        return bounds

    #: Extract the noise params
    if noise_params is None:
        noise_type = 'noise_free'
    else:
        noise_type, *_ = noise_params
    #: Check the noise type
    match noise_type:
        case 'normal':
            #: Unpack the noise parameters
            _, params_w, params_v = noise_params
            if params_w is not None and process_or_measurement_noise == 'process_noise':
                #: Unpack the noise parameters
                mu_w, Sigma_w = params_w
                #: Create multi-variate randomly distributed vectors
                W_or_V = np.random.multivariate_normal(mu_w, Sigma_w)
            elif params_v is not None and process_or_measurement_noise == 'measurement_noise':
                #: Unpack the noise parameters
                mu_v, Sigma_v = params_v
                #: Create multi-variate randomly distributed vectors
                W_or_V = np.random.multivariate_normal(mu_v, Sigma_v)
            else:
                # FIXME: When is this the case? It should never be the case right?
                W_or_V = np.array([0])
        case 'norm_trunc':
            raise NotImplementedError(f"This is not implemented yet")
        case 'uniform_ball':
            raise NotImplementedError(f"This is not implemented yet")
        case 'constant':
            #: Extract the dimension
            n_x, n_y = sys_ol.nstates, sys_ol.noutputs
            #: Extract the constant value
            _, delta_vec = noise_params
            #: Create the noise vector
            W_or_V = delta_vec if process_or_measurement_noise == 'process_noise' else np.zeros(n_y)
        case 'noise_free':
            #: Extract the dimension
            n_x, n_y = sys_ol.nstates, sys_ol.noutputs
            #: Return a zero vector
            W_or_V = np.zeros(n_x if process_or_measurement_noise == 'process_noise' else n_y)
        case 'custom':
            # FIXME: This should actually only be a function o V, as the process noise is different
            #: Extract the dimension
            n_x, n_y = sys_ol.nstates, sys_ol.noutputs
            #: Return a zero vector
            W_or_V = np.zeros(n_x if process_or_measurement_noise == 'process_noise' else n_y)
        case _:
            raise ValueError(f"Unknown noise type '{noise_type}'")
    #: Return the noise vector
    return W_or_V


def get_reference_signal(n_x_hat: int, reference_params: Any | None) -> NPArray[float]:

    def regulation_func(sgnl: dict) -> NPArray[float]:
        #: Create a zero vector
        Ref = np.zeros(n_x_hat)
        #: Return the results
        return Ref
    
    def circular_ref_func(sgnl: dict) -> NPArray[float]:
        # FIXME: This will only work with DT?
        #: Retrieve the time index
        k = sgnl['K'][-1]
        #: Retrieve the direction
        direction = np.sign(period)
        #: Create the rotation matrix
        rotation_matrix = radius * np.array([[np.cos(direction * (k / period + offset) * 2 * np.pi), -np.sin(direction * (k / period + offset) * 2 * np.pi)], [np.sin(direction * (k / period + offset) * 2 * np.pi), np.cos(direction * (k / period + offset) * 2 * np.pi)]])
        #: Create the reference signal
        Ref = rotation_matrix @ np.array([1, 0])
        #: Return the results
        return Ref
    
    #: Retrieve the first argument
    try:
        reference_type, *_ = reference_params
    except TypeError:
        #: Retrieve the zero-reference function
        func = regulation_func
        #: Return the result
        return func
    #: Match the corresponding condition
    match reference_type:
        case 'circular':
            #: Retrieve the reference parameters
            _, period, radius, offset = reference_params if len(reference_params) == 4 else (*reference_params, 0)
            #: Retrieve the zero-reference function
            func = circular_ref_func
            #: Return the result
            return func
        case _:
            raise ValueError(f"Unknown attack type '{reference_type}'")


def get_attack_signal(T_end: int | float, attack_params: Any | None) -> NPArray[float] | None:

    @utils.static_vars(f_i=None, sys_a_list=None)
    def switched_zda_dynamics(channel: Literal['C2A', 'S2C'], sgnl: dict) -> NPArray[float]:
        # TODO: Actually, we are now assuming a fixed sampling distance between them: however, we can also expand this dynamically if we read tau_i_p_1 online, and then dynamically create the array

        def initialize():
            #: Retrieve the attack parameters
            _, sys_ol, h, f_0, kappa_ubar = attack_params
            #: Initialize the initial condition
            switched_zda_dynamics.f_i = f_0
            #: Compute the discretization 
            if sys_ol.dt == 0:
                #: Extract the discretized dynamics
                sys_ol_dt = sys_ol.sample(Ts=h)
            else:
                #: Set equal to the dynamics
                sys_ol_dt = sys_ol
            #: Compute the maximal controlled-invariant subspace
            V = utils.get_maximal_controlled_invariant_subspace_kernel(sys_ol_dt)
            #: Initialize an empty list
            switched_zda_dynamics.sys_a_list = []
            #: Compute the full-state feedback gains
            for kappa in range(1, kappa_ubar + 1):
                #: Check if the system is continuous-time or discrete-time
                if sys_ol.dt == 0:
                    #: Extract the discretized dynamics
                    sys_ol_dt_kappa = sys_ol.sample(Ts=(h * kappa))
                else:
                    # FIXME: What about dt = True? How to deal with that?
                    #: Compute a longer hold
                    sys_ol_dt_kappa = utils.discrete_time_prolonged_zoh(sys_ol_dt, kappa)
                #: Extract the matrices
                A_kappa, B_kappa = sys_ol_dt_kappa.A, sys_ol_dt_kappa.B
                #: Compute a friend F of V
                F_kappa = utils.get_friend_controlled_invariant_subspace(V, A_kappa, B_kappa)
                #: Compute the autonomous dynamical system
                switched_zda_dynamics.sys_a_list += [ct.ss(A_kappa + B_kappa @ F_kappa, np.zeros((sys_ol.nstates, 1)), F_kappa, np.zeros((sys_ol.ninputs, 1)), dt=(h * kappa))]
                #: Check whether V is an invariant subspace of this system
                _, sol_res, *_ = np.linalg.lstsq(V, switched_zda_dynamics.sys_a_list[-1].A @ V, rcond=None)
                if np.max(np.abs(sol_res)) >= 1E-12:
                    warnings.warn(f"The residual ({np.max(np.abs(sol_res)):.2E}) appears to be too high, something might be wrong")
        
        #: Check if this is the initial call
        if switched_zda_dynamics.f_i is None and switched_zda_dynamics.sys_a_list is None:
            #: Initialize the system
            initialize()
        #: Check if this function is called on the C2A channel
        if channel == 'C2A':  # Actuator channel
            #: Retrieve the next sampling time
            kappa_i_p_1 = sgnl['Kappa_i'][-1]
            #: Retrieve the attack vector
            a_i = switched_zda_dynamics.sys_a_list[kappa_i_p_1 - 1].output(0, x=switched_zda_dynamics.f_i)
            #: Retrieve the next state vector
            switched_zda_dynamics.f_i = switched_zda_dynamics.sys_a_list[kappa_i_p_1 - 1].dynamics(0, x=switched_zda_dynamics.f_i)
            #: Return the result
            return a_i
        else:  # Sensor channel
            #: Return an empty array
            return np.array([])


    def transmission_zero_zda_dynamics(channel: Literal['C2A', 'S2C'], sgnl: dict) -> NPArray[float]:
        #: Check if this function is called on the C2A channel
        if channel == 'C2A':  # Actuator channel
            #: Retrieve the current time step
            k = sgnl['K'][-1]
            #: Retrieve the attack vector
            # FIXME: How to actually deal with real zeros
            a_i = u_0 * (largest_zero.real ** k)
            #: Return the result
            return a_i
        else:  # Sensor channel
            #: Return an empty array
            return np.array([])

    def single_shot_optimization_zda_dynamics(channel: Literal['C2A', 'S2C'], sgnl: dict) -> NPArray[float]:
        #: Check if this function is called on the C2A channel
        if channel == 'C2A':  # Actuator channel
            #: Retrieve the current time step
            k = sgnl['K'][-1]
            #: Retrieve the attack vector
            try:
                a_i = np.atleast_1d(U_zda[k])
            except IndexError:
                warnings.warn(f"The simulation length exceeds the precomputed attack vector length, returning a zero vector instead", Warning, stacklevel=3)
                a_i = np.zeros(sys_ol_dt.ninputs)
            #: Return the result
            return a_i
        else:  # Sensor channel
            #: Return an empty array
            return np.array([])

    def replay_delay_func(channel: Literal['C2A', 'S2C'], sgnl: dict) -> NPArray[float]:
        #: Check if this function is called on the S2C channel
        if channel == 'S2C':  # Sensor channel
            #: Retrieve the current time step
            k, n_y = sgnl['K'][-1], sgnl['Y_i'][-1].size
            #: Check if the replay attack has already started
            if k >= k_a:  # Replay attack in progress
                a_i = -sgnl['Y_i'][-1] + sgnl['Y_i'][-(Delta_k + 1)]
            else:
                a_i = np.zeros(n_y)
            #: Return the result
            return a_i
        else:  # Actuator channel
            #: Return an empty array
            return np.array([])

    # TODO: Implement all the necessary checks, to make sure that the right arguments are passed
    #: Retrieve the first argument
    attack_type, *_ = attack_params
    #: Match the corresponding condition
    match attack_type:
        # ============ ZDA ============
        case 'switched_zda':
            #: Return the switched ZDA generator function
            return switched_zda_dynamics
        # FROM: "A secure control framework for resource-limited adversaries", Teixeira et al. (2015)
        case 'zda_transmission_zero':
            #: Extract the parameters
            _, sys_ol_dt, norm_u_0 = attack_params
            #: Solve the transmission zero problem
            try:
                zeros = sys_ol_dt.zeros()
            except NotImplementedError:
                raise NotImplementedError("For MIMO-like systems with unequal number of inputs and outputs, transmission zero ZDAs are not supported")
            # TODO: Which on to select if there are multiple zeros?
            #: Select the (largest) unstable zero
            largest_zero = zeros[np.argmax(np.abs(zeros))]
            #: Check if this zero is unstable
            if np.abs(largest_zero) < 1:
                warnings.warn("The sampled-data system does not contain unstable sampling zeros, ZDA will not be disruptive", Warning, stacklevel=3)
            #: Construct the Rosenbrock system matrix
            R = np.block([[sys_ol_dt.A -  largest_zero * np.eye(sys_ol_dt.nstates), sys_ol_dt.B], [sys_ol_dt.C, sys_ol_dt.D]])
            #: Solve for the input direction
            Phi = np.squeeze(sp.linalg.null_space(R).real)
            #: Extract the directional components
            _, u_0 = Phi[:sys_ol_dt.nstates], Phi[sys_ol_dt.nstates:] 
            #: Scale the initial condition
            if norm_u_0 is not None:
                u_0 = (norm_u_0 / np.linalg.norm(u_0, ord=2)) * u_0
            # TODO: Maybe we want the construction to be done offline? Now, it seems like this function actually computes this online, which is not the case
            #: Return the transmission zero ZDA strategy
            return transmission_zero_zda_dynamics
        case 'zda_optimization':
            #: Extract the parameters
            _, sys_ol_dt, N_horizon, x_0, bounds_unsafe, eps_output, bounds_input = attack_params
            #: Check if horizon is supplied 
            if N_horizon is None:
                N_horizon = T_end
            #: Check if the initial condition is unknown
            if x_0 is None:  # FIXME: Instead of x_0 being None, it should be a convex set
                raise NotImplementedError(f"Currently, robust optimization associated with uncertainty in the initial condition is not supported, but will be added in the future")
            #: Construct the attack vector
            U_zda = get_zda_single_shot_optimization(sys_ol_dt, N_horizon, x_0, bounds_unsafe, eps_output, bounds_input)
            #: Check if the attack construction was successful
            if U_zda.size == 0:
                warnings.warn(f"No solution was found to the ZDA optimization problem, returning a zero attack vector instead", Warning, stacklevel=3)
            #: Return the single shot optimization problem ZDA strategy
            return single_shot_optimization_zda_dynamics
        # ============ Replay attack ============
        case 'delay_attack':
            #: Extract the parameters
            _, k_a, Delta_k = attack_params
            #: Retrieve the predictor function
            func = replay_delay_func
            #: Return the result
            return func
        case _:
            raise ValueError(f"Unknown attack type '{attack_type}'")


def get_hold_signal(hold_params: Any | None) -> Callable:
    
    def zero_order_hold(sgnl: dict) -> NPArray[float]:
        #: Retrieve the input
        u_hold = sgnl['U_i_prime'][-1]
        #: Return the result
        return u_hold
    
    def zero_order_hold_saturation(sgnl : dict) -> NPArray[float]:
        #: Retrieve the input
        u_prime = sgnl['U_i_prime'][-1]
        #: Create a copy
        u_hold = np.copy(u_prime)
        #: Apply saturation
        for elem in range(u_prime.size):
            u_hold[elem] = np.clip(u_prime[elem], input_bounds[elem][0], input_bounds[elem][1])
        #: Return the result
        return u_hold

    #: Check if arguments are provided
    if hold_params is None:
        #: Retrieve the predictor function
        func = zero_order_hold
        #: Return the result
        return func
    else:
        #: Retrieve the hold type
        hold_type, *_ = hold_params
        match hold_type:
            case 'saturation':
                #: Retrieve the bounds
                _, input_bounds = hold_params
                #: Retrieve the predictor function
                func = zero_order_hold_saturation
                #: Return the result
                return func
            case _: 
                raise ValueError(f"Unknown hold type '{hold_type}'")


# ---------- TRIGGERING FUNCTIONS ----------


def get_stc_mazo_iss(sys_ol_ct: ct.StateSpace, K: NPArray[float], sigma: float, tau_lbar: float, Delta: float, N_max: int, xi_elems: tuple[str, ...] = ('x_s', 'x_i')) -> Callable:
    """
    # FROM: "An ISS self-triggered implementation of linear controllers", Mazo et al. (2010)
    # FROM: "Observer based self-triggered control of linear plants with unknown disturbances", Almeida et al. (2012)
    # NOTE: This function assumes positive feedback, i.e. u = Kx
    # FIXME: This method still produces wildly weird results, its for sure broken. The state-evolution matrix does seem to be in order though, M is correct.
    # FIXME: The argument xi_elems is not properly defined
    """

    def predictor_func(sgnl: dict) -> int | float:

        def decay_func(x: NPArray[float], s: float) -> float:
            #: Calculate the evolution matrices
            M = utils.get_state_evolution_matrix(sys_ol_ct, K, s)
            #: Calculate the evolution of the state 
            x_s = M @ x
            #: Calculate the value of h
            h_disc = np.sqrt(x_s.T @ P @ x_s) - np.sqrt(x.T @ P @ x) * np.exp(-lambda_e * s)
            #: Return the result
            return h_disc
    
        #: Retrieve the signals
        if xi_elems == ('x_s', 'x_i'):
            x_i = sgnl['Y_i_prime'][-1]
        elif xi_elems == ('x_s', 'x_hat_i'):
            x_i = sgnl['X_hat'][-1]
        else:
            raise NotImplementedError(f"Here there needs to be a check on how to augment Q and construct the xi vector")
        #: Initiate the index
        n = 0
        #: Loop over all allowed values
        while n < N_max:
            #: Calculate the decay function
            h_disc = decay_func(x_i, tau_lbar + Delta * n)
            #: Check the condition
            if h_disc <= 0:
                #: Increase the counter
                n += 1
            else:
                #: Check if the value for kappa is valid
                if n == 0:
                    break
                #: Return the last best value for which h(x, tau) was positive
                n -= 1
                #: Break from the loop
                break
        #: Compute the next inter-sample time
        tau_i_plus_1 = tau_lbar + Delta * n
        #: Return the result
        return tau_i_plus_1
    
    #: Retrieve the matrices
    A, B = sys_ol_ct.A, sys_ol_ct.B
    #: Construct the closed-loop system matrix
    M = A + B @ K
    #: Get the Lyapunov solution
    P = utils.get_lyapunov_solution_ct(M)
    #: Check is a solution was found
    if P is None:
        raise ValueError(f"The closed-loop dynamics are not stable with the provided matrix K, implementation impossible")
    #: Find the largest eigenvalue
    lambda_0 = 1 / (2 * np.max(np.linalg.eigvals(P)))
    #: Select the desired decay rate
    lambda_e = sigma * lambda_0
    #: Retrieve the predictor function
    func = predictor_func
    #: Set the time base and return type
    func.dt = 0
    func.dtype = float
    #: Return the result
    return func


def get_stc_lemmon_iss(sys_ol_ct: ct.StateSpace, L: NPArray[float], sigma: float, xi_elems: tuple[str, ...] = ('x_s', 'x_i')) -> Callable:
    """
    # FROM: "Self-triggered observer based control of linear plants", Almeida et al. (2011)  # nopep8
    # TODO: Add the check that L is PD
    """

    def predictor_func(sgnl: dict) -> float:

        def mu_M(A: NPArray[float], M: NPArray[float]) -> float:
            # NOTE: This function calculates the log norm of a matrix
            #: Calculate the square root
            M_sqrt = np.linalg.cholesky(M)
            #: Calculate the intermediate matrix
            X = M_sqrt @ A @ np.linalg.inv(M_sqrt)
            #: Calculate the eigenvalues
            lambdas = np.linalg.eigvals(X + X.T)
            #: Calculate the evolution of the state 
            log_norm = (1 / 2) * np.max(lambdas.real)
            #: Return the result
            return log_norm
        
        def weighted_norm(x: NPArray[float], W: NPArray[float]) -> float:
            # TODO: Make sure that W is PD
            res = np.sqrt(x.T @ W @ x)
            #: Return the result
            return res
    
        #: Retrieve the signals
        if xi_elems == ('x_s', 'x_i'):
            x_i = sgnl['Y_i_prime'][-1]
        elif xi_elems == ('x_s', 'x_hat_i'):
            x_i = sgnl['X_hat'][-1]
        else:
            raise NotImplementedError(f"Here there needs to be a check on how to augment Q and construct the xi vector")
        #: Calculate the next sampling instant
        tau_i_plus_1 = (1 / mu_M(A, M)) * np.log(1 + ((mu_M(A, M) * weighted_norm(x_i, N)) / (weighted_norm(A_cl @ x_i, M))))
        #: Return the result
        return tau_i_plus_1
    
    #: Extract the matrices
    A, B = sys_ol_ct.A, sys_ol_ct.B
    #: Solve the CARE
    P, _, K = ct.care(A, B, L)
    #: Set the full-state feedback matrix to positive feedback
    K *= -1
    #: Compute the closed-loop matrix
    A_cl = A + B @ K
    #: Set the Q matrix
    Q = K.T @ K
    #: Set the slower decay matrix S
    S = sigma * L
    #: Set the matrix R
    R = L - S
    #: Set the matrices M and N
    M = 2 * Q + R
    N = Q + (1 / 4) * R 
    #: Retrieve the predictor function
    func = predictor_func
    #: Set the time base and return type
    func.dt = 0
    func.dtype = float
    #: Return the result
    return func


def get_stc_anderson_mss(sys_ol_ct: ct.StateSpace, Q: NPArray[float], sigma: float, mode: str = 'A_&_B', xi_elems: tuple[str, ...] = ('x_s', 'x_i')) -> Callable:

    def predictor_func(sgnl: dict) -> int | float:

        def A(norm_x: float, tau_i_plus_1: float) -> float:
            #: Compute the quantity
            A_res = ((2 * norm_x ** 2 + 1) / 3) * (np.exp(12 * K_e * tau_i_plus_1) - 1)
            #: Return the result
            return A_res
        
        def B(norm_x: float, tau_i_plus_1: float) -> float:
            #: Compute the quantity
            B_res = ((5 * norm_x ** 2 + 1) / 3) * (np.exp(-6 * K_e * tau_i_plus_1) - 1) - ((2 * norm_x ** 2 + 1) / 3)
            #: Return the result
            return B_res
        
        def C(norm_x: float, tau_i_plus_1: float) -> float:
            #: Compute the quantity
            C_res = ((2 * norm_x ** 2 * (1 + np.sqrt(L_m))) / (4 + 3 * np.sqrt(L_m))) * (np.exp((4 * np.sqrt(L_m) + 3 * L_m) * tau_i_plus_1) - 1)
            #: Return the result
            return C_res
        
        def D(norm_x: float, tau_i_plus_1: float) -> float:
            #: Compute the quantity
            D_res = ((norm_x ** 2) / (4 + 3 * np.sqrt(L_m))) * ((6 + 5 * np.sqrt(L_m)) * np.exp(-(4 * np.sqrt(L_m) + 3 * L_m) * tau_i_plus_1) - 2 * (1 + np.sqrt(L_m)))
            #: Return the result
            return D_res
        
        def inequality_func(tau: float, x_i: NPArray[float]) -> float:
            match mode:
                case 'A_&_B':
                    #: Compute the inequality
                    res = A(np.linalg.norm(x_i, ord=2), tau) - theta * B(np.linalg.norm(x_i, ord=2), tau) - d_alpha
                case 'C_&_D':
                    #: Compute the inequality
                    res = C(np.linalg.norm(x_i, ord=2), tau) - theta * D(np.linalg.norm(x_i, ord=2), tau) - d_alpha
                case _:
                    raise ValueError(f"Unknown mode '{mode}'")
            #: Return the result
            return res
    
        #: Retrieve the signals
        if xi_elems == ('x_s', 'x_i'):
            x_i = sgnl['Y_i_prime'][-1]
        elif xi_elems == ('x_s', 'x_hat_i'):
            x_i = sgnl['X_hat'][-1]
        else:
            raise NotImplementedError(f"Here there needs to be a check on how to augment Q and construct the xi vector")
        #: Find the root of the function
        tau_i_plus_1, = sp.optimize.root(inequality_func, 0.1, args=(x_i,)).x
        #: Return the result
        return tau_i_plus_1
    
    # NOTE: Here we assume that B_w = sigma * I 
    #: Extract the matrices
    A, B = sys_ol_ct.A, sys_ol_ct.B
    #: Solve the CARE
    P, _, K = ct.care(A, B, Q)
    # TEMP
    P = np.array([[1, 0.25], [0.25, 1]])
    K = np.array([[-1, 4]])
    #: Create a matrix with positive feedback
    K *= -1
    #: Calculate the value of a and b
    a = np.min(np.linalg.eigvals(Q))
    b = np.linalg.norm((B @ K).T @ P + P @ (B @ K), ord=2)
    #: Retrieve the monotone growth K_e and Lipchitz coefficient L_m
    K_e = np.max([(1 / 2) * np.linalg.norm(B @ K, ord=2) ** 2 - 1, (1 / 2) * np.linalg.norm(B @ K, ord=2), (1 / 2) * sigma ** 2])
    L_m = np.max([2 * np.linalg.norm(A + B @ K, ord=2) ** 2, 2 * np.linalg.norm(B @ K, ord=2) ** 2])
    #: Compute an upper bound to θ_d_ubar
    theta_ubar = a / b
    # FIXME: Why is everything below the case?
    # TEMP
    theta = 0.0028
    d_alpha = 1
    theta_d = (theta * sigma ** 2) / d_alpha
    #: Retrieve the predictor function
    func = predictor_func
    #: Set the time base and return type
    func.dt = 0
    func.dtype = float
    #: Return the result
    return func


def get_stc_dynamic_quadratic(sys_ol: ct.StateSpace, h: float, condition: Literal['mazo_iss'], trigger_params: Any | None = None) -> Callable:
    # TODO: How to deal with triggering function taking different inputs? Maybe by means of a dictionary?

    @utils.static_vars(s=0) 
    def predictor_func(sgnl: dict) -> int | float:
        #: Retrieve the signals
        x_i = sgnl['Y_i_prime'][-1]
        #: Start counting
        kappa = 1
        #: Calculate the evolution matrices
        M = utils.get_state_evolution_matrix(sys_ol_ct, K, h)
        #: Retrieve the next state
        x_s = M @ x_i
        #: Concatenate both vectors
        xi = np.concatenate((x_s, x_i))
        #: Retrieve the triggering matrix
        Q, _ = utils.get_quadratic_triggering_matrix(sys_ol.nstates, 'mazo_iss', (sys_ol, K, sigma, predictor_func.s))
        #: Check if the condition applies
        while xi.T @ Q @ xi <= 0 and kappa < kappa_ubar:
            #: Increase the counter
            kappa += 1
            predictor_func.s += h
            #: Calculate the evolution matrices
            M = utils.get_state_evolution_matrix(sys_ol_ct, K, predictor_func.s)
            #: Retrieve the next state
            x_s = M @ x_i
            #: Concatenate both vectors
            xi = np.concatenate((x_s, x_i))
            #: Retrieve the triggering matrix
            Q, _ = utils.get_quadratic_triggering_matrix(sys_ol.nstates, 'mazo_iss', (sys_ol, K, sigma, predictor_func.s))
        #: Reset the elapsed time
        predictor_func.s = 0
        #: Return the result
        # FIXME: For some reason adding 1 to this leads to the same implementation as Manuel? No, that's actually not the case
        return kappa

    #: Match the case
    match condition:
        case 'mazo_iss':
            # NOTE: This implementation is a PETC emulation based variation, where all inter-sample times are integer multiples of some h
            # FIXME: I don't think this actually follows Manuel's convention, as in it triggers one late?
            #: Retrieve the triggering parameter and the full-state feedback gain
            sigma, K, kappa_ubar = trigger_params
            #: Check if the system is continuous-time
            if sys_ol.dt != 0:
                raise ValueError(f"System must be continuous-time")
            else:
                sys_ol_ct = sys_ol
            #: Return the result
            return predictor_func 
        case _:
            raise ValueError(f"Unknown triggering condition '{condition}'")
        

def get_stc_static_quadratic(sys_ol: ct.StateSpace, h: bool | float, Q: NPArray[float], xi_elems: tuple[str, ...], kappa_ubar: int | None) -> Callable:

    def predictor_func(sgnl: dict) -> int | float:
        # NOTE: This predictor function assumes full-state feedback. It is a PETC emulation based design which provides stability in the noise-free case (it samples when the condition has already been violated).
        #: Retrieve the signals
        if xi_elems == ('x_s', 'x_i'):
            x_i, u_i = sgnl['Y_i_prime'][-1], sgnl['U_i'][-1]
        elif xi_elems == ('x_s', 'x_hat_i'):
            x_i, u_i = sgnl['X_hat'][-1], sgnl['U_i'][-1]
        else:
            raise NotImplementedError(f"Here there needs to be a check on how to augment Q and construct the xi vector")
        #: Start counting
        kappa = 1
        #: Retrieve the next state
        x_s = A_dt @ x_i + B_dt @ u_i
        #: Concatenate both vectors and convert to column vector
        xi = np.concatenate((x_s, x_i))[:, np.newaxis]
        #: Loop over the values
        while not xi.T @ Q @ xi > 0 and kappa < kappa_ubar:
            #: Increase the index
            kappa += 1
            #: Retrieve the next state
            x_s = A_dt @ x_s + B_dt @ u_i
            #: Concatenate both vectors and convert to column vector
            xi = np.concatenate((x_s, x_i))[:, np.newaxis]
        #: Return the result
        return kappa
    
    #: Check if the system is continuous-time or discrete-time
    if sys_ol.dt == 0:
        #: Create a discretize system
        sys_ol_dt = sys_ol.sample(Ts=h, method='zoh')
        #: Retrieve the state-space data
        A_dt, B_dt = sys_ol_dt.A, sys_ol_dt.B
    else:
        #: Retrieve the state-space data
        A_dt, B_dt = sys_ol.A, sys_ol.B
    #: Check if kappa_ubar is None
    if kappa_ubar is None:
        #: Print a warning
        warnings.warn("Setting kappa_ubar to None in a STC is not recommended,simulation might never halt", Warning, stacklevel=2)
        #: Set the upper bound to infinity
        kappa_ubar = np.inf
    #: Retrieve the predictor function
    func = predictor_func
    #: Set the time base and return type
    func.dt = h
    func.dtype = int
    #: Return the result
    return predictor_func


def get_petc_static_quadratic(sys_ol: ct.StateSpace, h: bool | float, Q: NPArray[float], xi_elems: tuple[str, ...], kappa_ubar: int | None) -> Callable:

    def trigger_func(sgnl: dict) -> int | float:
        #: Retrieve the signals
        if xi_elems == ('x_s', 'x_i'):
            x_k, x_i = sgnl['Y'][-1], sgnl['Y_i_prime'][-1]
        else:
            raise NotImplementedError(f"Here there needs to be a check on how to augment Q and construct the xi vector")
        #: Concatenate both vectors and convert to column vector
        xi = np.concatenate((x_k, x_i))[:, np.newaxis]
        #: Check the condition
        to_sample = xi.T @ Q @ xi > 0
        #: Return the result
        return to_sample
    
    #: Retrieve the predictor function
    func = trigger_func
    #: Set the time base and return type
    func.dt = h
    func.dtype = int
    #: Return the result
    return func


# ------------ ZDA CONSTRUCTION ------------


def get_zda_single_shot_optimization(sys_ol_dt: ct.StateSpace, N_horizon: int, x_0: NPArray[float], bounds_unsafe: tuple[tuple[float, float], ...], epsilon_output: float, bounds_input: tuple[tuple[float, float], ...] | None = None) -> NPArray[float] | None:
    """
    NOTE: Currently this method only takes box-constraints into account on the unsafe region
    """
    # TODO: Maybe replace everything with the 'polytope' package?
    # FROM: https://github.com/tulip-control/polytope/tree/main  # nopep8

    def check_arguments():
        #: Check if the initial condition is feasible
        if np.linalg.norm(C @ x_0, ord=2) > epsilon_output:
            raise ValueError("The initial condition is such that the output exceeds the threshold. Optimization is not feasible, choose a larger epsilon or different x_0.")

    def solve_optimization_problem(F_unsafe: NPArray[float], b_unsafe: NPArray[float]) -> NPArray[float]:
        #: Create optimization variables
        X, U = cvx.Variable((n_x, N_horizon + 1)), cvx.Variable((n_u, N_horizon))
        #: Initialize the cost function and list of constraints
        # TODO: Add the infinity-norm of the output to the cost-function
        cost_function, constraints_list = 0., []
        #: Add constraint for the initial state
        constraints_list += [X[:, 0] == x_0]
        #: Loop over all time steps
        for k in range(N_horizon):
            #: Add constraint for the dynamics
            constraints_list += [X[:, k + 1] == A @ X[:, k] + B @ U[:, k]]
            #: Add constraint for output
            # TODO: This now only works if n_y = 1, otherwise it will fails
            # TODO: See if we can replace this with a norm constraint, second order cone programming (SOCP) problem
            # FROM: https://math.stackexchange.com/questions/3636612/linear-program-with-quadratic-l2-norm-constraint  # nopep8
            constraints_list += [C @ X[:, k] <= epsilon_output, C @ X[:, k] >= -epsilon_output]
            #: Add constraint for the inputs
            if bounds_input is not None:
                #: Add constraints on every input
                for idx in range(U.shape[0]):
                    # TODO: What about norm constraints? This makes it a SOQC program?
                    #: Add both the lower and upper bound
                    constraints_list += [bounds_input[idx][0] <= U[idx, k], U[idx, k] <= bounds_input[idx][1]]
        #: Add constraint for the terminal state
        constraints_list += [F_unsafe @ X[:, N_horizon] <= b_unsafe]
        # FIXME: Why does this thing below not work?
        # FROM: https://www.cvxpy.org/examples/basic/socp.html  # nopep8
        # constraints_list += [cvx.SOC(-1.1, -X[:, N_horizon])]
        #: Add constraint for the terminal output
        # NOTE: We do need this, otherwise it will give all 0's and one big punch to infinity
        constraints_list += [C @ X[:, N_horizon] <= epsilon_output, C @ X[:, N_horizon] >= -epsilon_output]
        #: Construct the optimization problem
        prob = cvx.Problem(cvx.Maximize(cost_function), constraints=constraints_list)
        #: Solve problem for a feasible solution
        prob.solve()
        #: Print warning if no solution was found
        if prob.status != "optimal":
            #: Returning empty array
            return np.array([])
        #: Save the solution
        U = U.value
        #: Remove any dimensions of size one
        U = np.squeeze(U)
        #: Return the result
        return U

    #: Method which iterates over the 2 * n_x bounds
    def iterate_optimization_problem() -> NPArray[float] | None:
        #: Initialize input sequence
        U = None
        #: Convert list of tuple to array
        bounds_unsafe_array = np.array([element for set in bounds_unsafe for element in set])
        #: Loop over all half-spaces
        for idx in range(n_x * 2):
            #: Construct the constraints vectors
            ones_idx = np.zeros(n_x)
            ones_idx[np.floor_divide(idx, 2)] = 1 
            #: Construct the constraint
            F_unsafe = (-1) ** idx * ones_idx[np.newaxis, :]
            b_unsafe = (-1) ** idx * np.atleast_2d(bounds_unsafe_array[idx])
            #: Solve the optimization program
            U = solve_optimization_problem(F_unsafe, b_unsafe)
            #: Check if the solution is feasible
            if U.size != 0:
                break
        #: Return the input
        return U

    #: Retrieve the matrices
    A, B, C, n_x, n_u = sys_ol_dt.A, sys_ol_dt.B,  sys_ol_dt.C, sys_ol_dt.nstates, sys_ol_dt.ninputs
    #: Check the arguments
    check_arguments()
    #: Compute the optimization problem
    U = iterate_optimization_problem()
    #: Return the results
    return U


# ---------- OBSERVER DESIGNS ----------


def get_static_observer_gain_almeida(sys_ol_dt: ct.StateSpace, kappa_ubar: int, tolerance: float = 1E-4) -> NPArray[float]:
    #: Extract the dimensions
    n_x, n_y = sys_ol_dt.nstates, sys_ol_dt.noutputs
    #: Create the optimization variables
    W, Y, I = cvx.Variable((n_x, n_x), PSD=True), cvx.Variable((n_x, n_y)), np.eye(n_x)
    #: Create a constraints list
    cons_list = []
    #: Loop over all matrices
    for kappa in range(1, kappa_ubar + 1):
        #: Retrieve the prolonged ZOH system
        sys_ol_dt_kappa_i = utils.discrete_time_prolonged_zoh(sys_ol_dt, kappa)
        #: Extract the relevant matrices
        A_kappa_i, C_kappa_i = sys_ol_dt_kappa_i.A, sys_ol_dt_kappa_i.C
        #: Create the LMI constraint
        cons_list.append(cvx.bmat([[W - I, A_kappa_i.T @ (W - Y @ C_kappa_i).T], [(W.T - C_kappa_i.T @ Y.T) @ A_kappa_i, W]]) >> tolerance)
    #: Create the cost-function
    cost_function = cvx.trace(W)
    #: Create the optimization problem
    prob = cvx.Problem(cvx.Minimize(cost_function), constraints=cons_list)
    #: Solve the optimization problem
    prob.solve()
    #: Print warning if no solution was found
    if prob.status != "optimal":
        warnings.warn("No observer gain matrix L was found, returning empty array", Warning, stacklevel=2)
        return np.array([])
    #: Save the solutions
    W, Y = W.value, Y.value
    #: Retrieve the observer gain
    L = np.linalg.inv(W) @ Y
    #: Return the result
    return L


