"""
File containing several dynamics from the literature.
"""

# Import packages
import numpy as np
import control as ct
from typing import Literal, Any
import copy

# ------------ METHODS ------------


# TODO: Change str as rgument to Literal
def get_plant_state_space(selection: str, sys_params: Any | None = None) -> ct.StateSpace:
    #: Create selection
    match selection:
        # ------------ 2 states ------------
        # FROM: "CUSUM and chi-squared attack detection of compromised sensors", Murguia et al. (2016)  # nopep8
        case 'murguia_cusum_2016':
            # states: 2, inputs: 1, outputs: 2, discrete-time, controllable, observable, poles (2, stable, real): [0.63, 0.33], zeros (0): N.A.
            A, B = np.array([[0.84, 0.23], [-0.47, 0.12]]), np.array([[0.07], [0.23]])
            C = np.array([[1, 0], [1, 1]])
            sys_ol = ct.ss(A, B, C, np.zeros((2, 1)), dt=True)
        # FROM: "Detection and Isolation of Replay Attacks through Sensor Watermarking", Ferrari et al. (2017)  # nopep8
        case 'detection_ferrari_2017':
            # states: 2, inputs: 1, outputs: 2, discrete-time, controllable, observable, poles (2, unstable, real): [1.05, 0.94], zeros (0): N.A.
            A, B = np.array([[1, 0.1], [0.035, 0.99]]), np.array([[0], [1]])
            C = np.eye(2)
            h = 0.1
            sys_ol = ct.ss(A, B, C, np.zeros((2, 1)), dt=h)
        # FROM: "Event-triggered dynamic output feedback control for LTI systems", Tallapragada et al. (2012)  # nopep8
        case 'event_tallapragada_2012':
            # states: 2, inputs: 1, outputs: 1, continuous-time, controllable, observable, poles (2, unstable, real): [0.82, -1.82], zeros (0): N.A.
            A, B = np.array([[2, 3], [1, 3]]), np.array([[0], [1]])
            C = np.array([[1, 0]])
            L = np.array([[-10], [-14]])  # Observer gain F, not used
            sys_ol = ct.ss(A, B, C, np.zeros((1, 1)))
        # FROM: "On event-triggered control of linear systems under periodic denial-of-service jamming attacks", Shisheh Foroush et al. (2012)  # nopep8
        case 'event_shisheh_2012':
            # states: 2, inputs: 1, outputs: 2, continuous-time, controllable, observable, poles (2, unstable, real): [0.82, -1.82], zeros (0): N.A.
            A, B = np.array([[0, 1], [1.5, -1]]), np.array([[0], [1]])
            C = np.eye(2)
            sys_ol = ct.ss(A, B, C, np.zeros((2, 1)))
        # FROM: "Chaos and Order in Event-Triggered Control", Gleizer et al. (2022)  # nopep8
        # FROM: "Periodic event-triggered control for linear systems", Heemels et al. (2013)  # nopep8
        # FROM: "Output-Based Event-Triggered Control With Guaranteed L-Gain and Improved and Decentralized Event-Triggering", Donkers et al (2012)  # nopep8
        case 'chaos_gleizer_2022' | 'periodic_heemels_2013' | 'output_donkers_2012':
            # states: 2, inputs: 1, outputs: 2, continuous-time, controllable, observable, poles (2, unstable, real): [2, 1], zeros (0): N.A.
            if sys_params is None:
                sign = 1
            elif sys_params[0] == 'stable':
                sign = -1
            A, B = np.array([[0, 1], [-2, sign * 3]]), np.array([[0], [1]])
            C = np.eye(2)
            C_2 = np.array([[-1, 4]])  # Donkers et al. (2012)
            B_w = np.array([[1], [0]])  # Heemels et al. (2013)
            B_w = np.array([[0], [1]])  # Donkers et al. (2012)
            h = 0.05  # Heemels et al. (2013)
            sys_ol = ct.ss(A, B, C, np.zeros((2, 1)))
        # FROM: "Sink or Swim: A Tutorial on the Control of Floating Wind Turbines", Stockhouse et al. (2023)  # nopep8
        case 'stockhouse_sink_2023':
            raise NotImplementedError(f"These dynamics are not yet available")
        # ------------ 3 states ------------
        case "temp_1":
            # 3 x 3, continuous-time, stable, real eigenvalues
            A_ct, B_ct, C_ct, D_ct = (np.array([[-5, 1, 0], [-8, 0, 1], [-4, 0, 0]]), np.array([[0], [0], [1]]), np.array([[1, 0, 0]]), 0)
            sys_ol = ct.StateSpace(A_ct, B_ct, C_ct, D_ct)
        # FROM: "Stabilization of linear systems over networks with bounded packet loss", Xiong et al (2007)  # nopep8
        case 'stabilization_xiong_2007':
            # states: 3, inputs: 1, outputs: 1, continuous-time, controllable, observable, poles (3, unstable, real): [0.5, -0.5, -1], zeros (1, stable, real): [-0.5].
            # FIXME: This is actually not a minimal realization as we have pole-zero cancellation
            # FIXME: If its not minreal, how can it be controllable and observable?
            A = np.array([[-1, 0, -0.5], [1, -0.5, 0], [0, 0, 0.5]])
            B = np.array([[0], [0], [1]])
            C = np.array([[1, 0, 0]])  # NOTE: In this paper no measurement matrix C is actually given
            sys_ol = ct.ss(A, B, C, np.zeros((1, 1)))
        # FROM: "Computing the average inter-sample time of event-triggered control using quantitative automata", Gleizer et al (2023)  # nopep8
        case 'gleizer_computing_2023':
            # states: 3, inputs: 1, outputs: 3, continuous-time, controllable, observable, poles (3, unstable, complex): [0.54, -0.77 ± 1.12j], zeros (0): N.A.
            A = np.array([[0, 1, 0], [0, 0, 1], [1, -1, -1]])
            B = np.array([[0], [0], [1]])
            C = np.eye(3)  # NOTE: With C = [1, 0, 0] the system still has no zeros
            sys_ol = ct.ss(A, B, C, np.zeros((3, 1)))
        # FROM: "Fault Detection of Networked Control Systems with Packet Dropout", Wang et al. (2008)  # nopep8
        case 'wang_fault_2008':
            # states: 3, inputs: 3, outputs: 3, continuous-time, controllable, observable, poles (3, stable, real): [-2, -3, -4], zeros (0): N.A.
            A, B = np.array([[-3, 0, 1], [0, -4, 1], [0, 0, -2]]), np.array([[1, 0, 0], [2, 0, 1], [0, 2, 1]])
            C = np.eye(3)
            B_d, B_f = np.array([[1, 0.7, 1], [0.3, 1, 0.3], [1, 1, 0]]), np.array([[1], [0], [1]])
            D_d = np.array([[1, 0, 0], [0, 0.5, 1], [0, 1, 0]])
            h = 1
            sys_ol = ct.ss(A, B, C, np.zeros((3, 3)))
        # ------------ 4 states ------------
        # FROM: "Dual rate control for security in cyber-physical systems", Naghnaeian et al (2015)  # nopep8
        case 'dual_naghnaeian_2015':
            # states: 4, inputs: 1, outputs: 1, discrete-time, controllable, observable, poles (4, stable, complex): [-0.96 ± 1.23j, -0.04 ± 0.64j], zeros (1, stable, real): [-1].
            A = np.array([[0.0105, 0.3949, 3.86, 2.869], [-0.0057, -0.1817, -1.369, -0.587], [0.00117, 0.03359, 0.1793, -0.4597], [0.00092, 0.03197, 0.3163, 0.8918]])
            B = np.array([[-0.005738], [0.001174], [0.0009193], [0.0002165]])
            C = np.array([[0, 0, 0, 5000]])
            h = 0.5
            sys_ol = ct.ss(A, B, C, np.zeros((1, 1)), dt=h)
        # FROM: "Quantized Zero Dynamics Attacks against Sampled-data Control Systems", Kimura et al (2022)  # nopep8
        # FROM: "Neutralizing zero dynamics attack on sampled-data systems via generalized holds", Kim et al (2020)  # nopep8
        case 'quantized_kimura_2022' | 'neutralizing_kim_2020':
            # states: 4, inputs: 1, outputs: 1, continuous-time, controllable, observable, poles (4, stable, complex): [-0.96 ± 1.23j, -0.04 ± 0.64j], zeros (1, stable, real): [-1].
            A = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [-2, 1, -1, 1], [1, -1, 1, -1]])
            B = np.array([[0], [0], [0], [1]])
            C = np.array([[1, 0, 0, 0]])
            sys_ol = ct.ss(A, B, C, np.zeros((1, 1)))
            # ------ UNUSED ------
            # # states: 4, inputs: 1, outputs: 1, continuous-time, controllable, observable, poles (4, stable, complex): [-0.96 ± 1.23j, -0.04 ± 0.64j], zeros (1, stable, real): [-1].
            # s = ct.tf('s')
            # G = (s + 1) / ((s ** 2 + 1) * (s ** 2 + s + 1) + (s + 1) * s ** 2)
            # sys_ol = ct.tf2ss(G)
        # FROM: "Dynamic Event-triggered Control and Estimation: A Survey", Ge et al (2021)  # nopep8
        case 'dynamic_ge_2021':
            # NOTE: This is an in-vehicle networked active suspension system
            # FIXME: Currently, the zeros are gigantic with the default parameters
            # states: 4, inputs: 1, outputs: 1, continuous-time, controllable, observable, poles (4, stable, complex): [-1.31 ± 0.95j, -0.19 ± 0.59j], zeros (3, unstable, real): [7.52E+7, -7.52E+7, -1].
            if sys_params is not None:
                m_s, m_u, k_s, k_t, c_s, c_t = sys_params
            else:
                m_s, m_u, k_s, k_t, c_s, c_t = 1, 1, 1, 1, 1, 1  # NOTE: These are not parameters from the paper
            A = np.array([[0, 0, 1, -1], [0, 0, 0, 1], [-k_s / m_s, 0, -c_s / m_s, c_s / m_s], [k_s / m_s, -k_t / m_u, c_s / m_u, -(c_s + c_t) / m_u]])
            B = np.array([[0], [0], [1 / m_s], [-1 / m_u]])
            C = np.array([[1, 2, 0, 0]])  # FIXME: Where is this from?
            B_w = np.array([[0], [-1], [0], [c_t / m_u]])
            sys_ol = ct.ss(A, B, C, np.zeros((1, 1)))
        # FROM: "Observer based self-triggered control of linear plants with unknown disturbances", Almeida et al (2012)  # nopep8
        # FROM: "Self-triggered output-feedback control of LTI systems subject to disturbances and noise", Gleizer et al (2020)  # nopep8
        case 'observer_almeida_2012' | 'self_gleizer_2020':
            # NOTE: This is the linearized model of an unstable batch reactor process
            # states: 4, inputs: 2, outputs: 1, continuous-time, controllable, observable, poles (4, unstable, real): [1.99, 0.064, -5.06, -8.67], zeros (0): N.A.
            A = np.array([[1.38, -0.2077, 6.715, -5.676], [-0.5814, -4.29, 0, 0.675], [1.067, 4.273, -6.654, 5.893], [0.048, 4.273, 1.343, -2.104]])
            B = np.array([[0, 0], [5.679, 0], [1.136, -3.146], [1.136, 0]])
            C = np.array([[1, 0, 1, -1]])
            C_2 = np.array(np.concatenate((np.eye(2), np.array([[1, -1], [0, 0]])), axis=1))  # Gleizer et al. (2020)
            if sys_params is not None and 'C_2' in sys_params:
                C = C_2
            B_w = np.eye(4)  # Almeida et al. (2012)
            B_w = np.array([[1], [0], [0], [0]])  # E | Gleizer et al. (2020)
            D_v = 1
            h = 0.01  # Gleizer et al. (2020)
            sys_ol = ct.ss(A, B, C, np.zeros((C.shape[0], 2)))
        # FROM: "Revealing stealthy attacks in control systems", Teixeira et al (2021)  # nopep8
        case 'revealing_teixeira_2012':
            # NOTE: These are the linearized dynamics of a continuous-time nonlinear quadruple Quadruple-Tank Process (QTP)
            # states: 4, inputs: 2, outputs: 2, discrete-time, controllable, observable, poles (4, stable, real): [0.975, 0.977, 0.958, 0.956], zeros (2, unstable, real): [1.03, 0.89].
            h = 0.5
            A = np.array([[0.975, 0, 0.042, 0], [0, 0.977, 0, 0.044], [0, 0, 0.958, 0], [0, 0, 0, 0.956]])
            B = np.array([[0.0515, 0.0016], [0.0019, 0.0447], [0, 0.0737], [0.0850, 0]])
            C = np.array([[0.2, 0, 0, 0], [0, 0.2, 0, 0]])
            sys_ol = ct.ss(A, B, C, np.zeros((2, 2)), dt=h)
        case _: 
            raise ValueError(f"Unknown plant dynamics '{selection}'")
    #: Return the dynamics
    return sys_ol


def get_controller_state_space(selection: Literal['chaos_gleizer_2022'], feedback: Literal[-1, 1] = -1, h: float | None = None) -> ct.StateSpace:
    #: Create selection
    match selection:
        # ------------ Full-state feedback (FSF) ------------
        # FROM: "CUSUM and chi-squared attack detection of compromised sensors", Murguia et al. (2016)  # nopep8
        case 'murguia_cusum_2016':
            # states: 0, inputs: 2, outputs: 1, full-state feedback, static
            K = np.array([[1.85, 0.96]])
            if h is None:
                h = True  # Discrete-time dynamics
            # FIXME: in the paper they state u = Kx, but this appears not to be the case? The simulation is unstable
            sys_c = ct.ss([], [], [], feedback * K, dt=h)
        # FROM: "Periodic event-triggered control for linear systems", Heemels et al. (2013)  # nopep8
        case 'periodic_heemels_2013':
            # states: 0, inputs: 2, outputs: 1, full-state feedback, static
            K = np.array([[1, -4]])
            if h is None:
                h = 0  # Continuous-time dynamics
            sys_c = ct.ss([], [], [], feedback * K, dt=h)
        # FROM: "Chaos and Order in Event-Triggered Control", Gleizer et al.  (2022)  # nopep8
        case 'chaos_gleizer_2022':
            # states: 0, inputs: 2, outputs: 1, full-state feedback, static
            K = np.array([[0, -6]])
            if h is None:
                h = 0  # Continuous-time dynamics
            sys_c = ct.ss([], [], [], feedback * K, dt=h)
        # FROM: "Event-triggered dynamic output feedback control for LTI systems", Tallapragada et al. (2012)  # nopep8
        case 'event_tallapragada_2012':
            # states: 0, inputs: 2, outputs: 1, full-state feedback, static
            K = np.array([[-15, -10]])
            if h is None:
                h = 0  # Continuous-time dynamics
            sys_c = ct.ss([], [], [], feedback * K, dt=h)
        # FROM: "Observer based self-triggered control of linear plants with unknown disturbances" Almeida et al (2012)  # nopep8
        case 'observer_almeida_2012':
            # states: 0, inputs: 4, outputs: 2, continuous-time, full-state feedback, static, MIMO
            K_f = np.array([[0.1006, -0.2469, -0.0952, -0.2447], 
                            [1.4099, -0.1966, 0.0139, 0.0823]])
            if h is None:
                h = 0  # Continuous-time dynamics
            sys_c = ct.ss([], [], [], feedback * K_f)
        # ------------ Output feedback (OF) ------------
        # FROM: "Self-triggered output-feedback control of LTI systems subject to disturbances and noise", Gleizer et al (2020)  # nopep8
        # FROM: " Self-Triggered Output Feedback Control for Perturbed Linear Systems", Gleizer et al (2018)  # nopep8
        case 'self_gleizer_2020' | 'self_gleizer_2018':
            # states: 2, inputs: 2, outputs: 2, discrete-time, output feedback, dynamic, MIMO
            # NOTE: This is a PI controller taken from Walsh and Ye (2001)
            if h is None or h is True:
                h = 0.01  # Discrete-time dynamics
            A_c, B_c = np.eye(2), np.array([[0, h], [h, 0]])
            C_c, D_c = np.array([[-2, 0], [0, 8]]), np.array([[0, -2], [5, 0]])
            sys_c = ct.ss(A_c, B_c, C_c, D_c, dt=h)
        # ------------ Reference tracking controller ------------
        # FROM: "Detection and Isolation of Replay Attacks through Sensor Watermarking", Ferrari et al. (2017)  # nopep8
        case 'detection_ferrari_2017':
            # states: 2, inputs: 1, outputs: 2, discrete-time, full-state feedback, dynamic, MISO, error term fed
            A_c, B_c = np.eye(2), 0.1 * np.eye(2)
            C_c, D_c = np.array([[0.01, 0.022]]), np.array([[0.0875, 0.1980]])
            if h is None:
                h = 0.1  # Discrete-time dynamics
            sys_c = ct.ss(A_c, B_c, C_c, D_c, dt=h)
        case _: 
            raise ValueError(f"Unknown controller dynamics '{selection}'")
    #: Return the dynamics
    return sys_c


def get_list_suitable_dynamics(must_have: dict | None = None, must_not_have: dict | None = None) -> dict:
    # FROM: ChatGPT3.5

    def initialize_dictionary() -> dict:
        #: Set the list of names
        name_list = ['murguia_cusum_2016', ('chaos_gleizer_2022', 'periodic_heemels_2013', 'output_donkers_2012'), 'detection_ferrari_2017', 'event_shisheh_2012', 'event_tallapragada_2012', 'stabilization_xiong_2007', 'gleizer_computing_2023', 'wang_fault_2008', 'quantized_kimura_2022', 'dynamic_ge_2021', 'observer_almeida_2012', 'revealing_teixeira_2012']
        #: Create an empty dictionary
        dict_dynamics = {}
        #: Loop over all names
        for name in name_list:
            #: Initialize the relevant dictionary
            dict_name = {}
            properties_name = []
            #: Extract the open-loop system
            if isinstance(name, str):
                sys_ol = get_plant_state_space(name)
            else:
                sys_ol = get_plant_state_space(name[0])
            #: Extract the relevant dynamics
            A, B, C, D, h, n_x, n_u, n_y, poles = sys_ol.A, sys_ol.B, sys_ol.C, sys_ol.D, sys_ol.dt, sys_ol.nstates, sys_ol.ninputs, sys_ol.noutputs, sys_ol.poles()
            if n_u == n_y:
                zeros = sys_ol.zeros()
            else:
                # FIXME: This is actually not correct
                zeros = []
            #: Set the values
            dict_name['h'], dict_name['n_x'], dict_name['n_u'], dict_name['n_y'] = h, n_x, n_u, n_y
            dict_name['rel_deg'] = len(poles) - len(zeros) if (n_y == 1 and n_u == 1) else None 
            dict_name['poles'], dict_name['zeros'] = poles, zeros
            #: Check whether the system is stable
            if h == 0:  # Continuous-time
                if np.max(poles.real) >= 0:
                    properties_name.append('unstable')
                else:
                    properties_name.append('stable')
            else:  # Discrete-time
                if np.max(np.abs(poles)) >= 1:
                    properties_name.append('unstable')
                else:
                    properties_name.append('stable')
            #: Check whether the poles are real or imaginary
            if np.max(poles.imag) >= 1E-12:
                properties_name.append('complex')
            else:
                properties_name.append('real')
            #: Check whether the system is SISO or MIMO
            if n_u == 1:
                if n_y == 1:
                    properties_name.append('SISO')
                else:
                    properties_name.append('SIMO')
            else:
                if n_y == 1:
                    properties_name.append('MISO')
                else:
                    properties_name.append('MIMO')
            #: Check whether the system is observable and controllable
            if np.linalg.matrix_rank(ct.ctrb(A, B)) == n_x:
                properties_name.append('controllable')
            elif np.linalg.matrix_rank(ct.obsv(A, C)) == n_x:
                properties_name.append('observable')
            #: Check whether the system is (non)-minimum phase
            if h == 0:  # Continuous-time
                if np.argmax(poles.real) < 0 and np.argmax(zeros.real) < 0:
                    properties_name.append('minimum phase')
                else:
                    properties_name.append('non-minimum phase')
            else:  # Discrete-time
                if np.argmax(np.abs(poles)) >= 1:
                    properties_name.append('unstable')
                else:
                    properties_name.append('stable')
            #: Add the list of values
            dict_name['properties'] = properties_name
            #: Add all the properties
            dict_dynamics[name] = dict_name
        #: Return the result
        return dict_dynamics
    
    #: Initialize the dictionary
    dict_dynamics = initialize_dictionary()
    dict_selection = copy.deepcopy(dict_dynamics) if must_have is None else {}
    if must_have is None and must_not_have is None:
        return dict_selection
    dict_matched = {}
    # TODO: We must augment this function such that it takes multiple values for each key
    if must_have is not None:
        for key in must_have:
            dict_matched[key] = [name for name in dict_dynamics if key == 'properties' and any(val in dict_dynamics[name][key] for val in must_have[key]) or dict_dynamics[name][key] == must_have[key]]
    for name in (set.intersection(*(set(dict_matched[key]) for key in dict_matched)) if must_have is not None else dict_matched.get(list(dict_matched)[0], [])):
        if all(name in dict_matched[key] for key in dict_matched):
            dict_selection[name] = dict_dynamics[name]
    if must_not_have is not None:
        for key in must_not_have:
            for name in dict_selection.copy():
                if key == 'properties' and any(val in dict_selection[name][key] for val in must_not_have[key]) or dict_selection[name][key] == must_not_have[key]:
                    dict_selection.pop(name)
    #: Return the result
    return dict_selection


# ------------ DATA ------------

# Tableau colors
# FROM: https://jrnold.github.io/ggthemes/reference/tableau_color_pal.html
tableau_color_palette_10 = ["#4E79A7",  # 0: Blue
                            "#F28E2B",  # 1: Orange
                            "#E15759",  # 2: Red
                            "#76B7B2",  # 3: Teal
                            "#59A14F",  # 4: Green
                            "#EDC948",  # 5: Yellow
                            "#B07AA1",  # 6: Purple
                            "#FF9DA7",  # 7: Pink
                            "#9C755F",  # 8: Brown
                            "#BAB0AC"]  # 9: Gray