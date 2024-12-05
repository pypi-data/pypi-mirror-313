"""
Script which contains various utility functions.

NOTE: As a convention, all vectors of length n are 1D vectors of shape (n,) which means no distinction is made between column and row vectors
FROM: https://python-control.readthedocs.io/en/0.9.4/conventions.html  # nopep8

NOTE: To remove all comments marked "#:" use the following steps: 1) Find the maximum number of indentations n, i.e. tabs (equivelant to four spaces), 2) Using "find and replace" (CTRL + R), search for "<n x 4 spaces>#:.*$\n" and replace with nothing, 3) Repeat step 2 for n - 1 indentations until n = 1
FROM: https://stackoverflow.com/questions/69060850/intellij-how-to-delete-all-line-containing-annotation  # nopep8
FROM: https://intellij-support.jetbrains.com/hc/en-us/community/posts/115000142590-How-can-you-find-delete-lines-not-just-replace-with-nothing-  # nopep8
"""

# Import packages
import numpy as np
import scipy as sp
import cvxpy as cvx
import control as ct
from functools import cache, wraps
import numpy.typing as npt
from typing import TypeVar, TypeAlias, Callable, Any, Literal
import warnings

# Create an abbreviation for the type hint "npt.NDArray[Any, np.dtype[dtype]]"
# FROM: https://stackoverflow.com/questions/49887430/can-i-make-type-aliases-for-type-constructors-in-python-using-the-typing-module # nopep8
# FROM: https://stackoverflow.com/questions/41914522/mypy-is-it-possible-to-define-a-shortcut-for-complex-type  # nopep8
T = TypeVar('T', int, float, complex, bool)
NPArray: TypeAlias = npt.NDArray[np.dtype[T]]


def np_cache(function):
    # FROM: https://stackoverflow.com/questions/52331944/cache-decorator-for-numpy-arrays  # nopep8

    @cache
    def cached_wrapper(*args, **kwargs):
        args = [np.array(a) if isinstance(a, tuple) else a for a in args]
        kwargs = {
            k: np.array(v) if isinstance(v, tuple) else v for k, v in kwargs.items()
        }
        return function(*args, **kwargs)

    @wraps(function)
    def wrapper(*args, **kwargs):
        args = [tuple(map(tuple, a)) if (isinstance(a, np.ndarray) and len(a.shape) == 2) else
                tuple(a) if (isinstance(a, np.ndarray) and len(a.shape) == 1) else a for a in args]
        kwargs = {
            k: tuple(map(tuple, v)) if (isinstance(v, np.ndarray) and len(v.shape) == 2) else
            tuple(v) if (isinstance(v, np.ndarray) and len(v.shape) == 1) else v for k, v in kwargs.items()
        }
        return cached_wrapper(*args, **kwargs)

    # Copy cache information
    wrapper.cache_info = cached_wrapper.cache_info
    wrapper.cache_clear = cached_wrapper.cache_clear
    return wrapper


# TODO: Can we actually make this simpler? FROM: https://stackoverflow.com/questions/338101/python-function-attributes-uses-and-abuses  # nopep8
def static_vars(**kwargs):
    # FROM: https://stackoverflow.com/questions/279561/what-is-the-python-equivalent-of-static-variables-inside-a-function  # nopep8

    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


def arange_step_number(start: float, step: float, number: int):
    #: Create a linearly spaced vector with the specific number of points and step size
    return start + np.arange(number) * step


def get_signed_angle(v_1: NPArray[float], v_2: NPArray[float], look: NPArray[float]) -> float:
    """
    FROM: https://github.com/lace/vg/blob/main/vg/core.py  #nopep8 
    """

    #: Compute the dot product (normalized)
    dot_products_normalized = np.dot(v_1, v_2) / np.linalg.norm(v_1, ord=2) / np.linalg.norm(v_2, ord=2)
    #: Compute the unsigned angle
    angle = np.arccos(np.clip(dot_products_normalized, -1.0, 1.0))  # Clipping is needed due to numerical issues
    #: The sign of (A x B) dot look gives the sign of the angle. Here, angle > 0 means clockwise, angle < 0 is counterclockwise.
    sign = np.array(np.sign(np.cross(v_1, v_2).dot(look)))
    #: An angle of 0 means collinear: 0 or 180. Let's call that clockwise.
    sign[sign == 0] = 1
    #: Compute the signed angle
    signed_angle = sign * angle
    #: Return the result
    return signed_angle


def max_vector_norm_outside_box(bounds: tuple[tuple[float, float], ...]):
    # FROM: ChatGPT3.5
    max_norm_sq = 0
    for b in bounds:
        max_norm_sq += max(abs(b[0]) ** 2, abs(b[1]) ** 2)
    return np.sqrt(max_norm_sq)


def max_vector_norm_inside_box(bounds: tuple[tuple[float, float], ...]):
    # FROM: ChatGPT3.5
    min_dist_sq = float('inf')
    for b in bounds:
        min_dist_sq = min(min_dist_sq, min(b[0] ** 2, b[1] ** 2))
    return np.sqrt(min_dist_sq)


def get_bisection_method(func: Callable, range: tuple[float, float], args: tuple | None = None, n_iter: int = 10):
    # TODO: Make an implementation where we can also have a tolerance as a criterion
    # FIXME: This function now only except continuous functions
    # FROM: https://stackoverflow.com/questions/52996211/bisection-method-in-python  # nopep8
    #: Set the iteration number
    iter, lb, ub = 0, range[0], range[1]
    #: Retrieve the type of the argument
    return_type = func(lb, *args)
    #: Match the return type
    match return_type:
        case bool():
            #: Check if both are either true or false
            if (func(lb, *args) and func(ub, *args)) or (not func(lb, *args) and not func(ub, *args)):
                raise ValueError(f"The lower and upper bound are both (in)feasible")
            else:
                while iter < n_iter:
                    #: Set the midpoint
                    midpoint = (lb + ub) / 2.
                    if func(lb, *args) != func(midpoint, *args):
                        ub = midpoint
                    else:
                        lb = midpoint
                    iter += 1
                #: Return the result
                return lb
        case float() | int():
            #: Check if the sign is the same
            if func(lb, *args) * func(ub, *args) > 0:
                raise ValueError(f"The lower and upper bound both have the same sign")
            else:
                while iter < n_iter:
                    #: Set the midpoint
                    midpoint = (lb + ub) / 2.
                    if func(lb, *args) * func(midpoint, *args) < 0:
                        lb = midpoint
                    else:
                        ub = midpoint
                    iter += 1
                #: Return the result
                return lb
        case _:
            raise ValueError(f"Unsupported return type by the function func, '{return_type}'")
    

def get_line_search(func: Callable, args: tuple, range: tuple[float, float], n_points: int = 10) -> tuple[NPArray[float], NPArray[float]]:
    #: Construct the line over which the search needs to be done
    x_line = np.linspace(range[0], range[1], n_points)
    #: Initialize the output
    f_line = np.zeros(x_line.size)
    #: Loop over all values
    for idx, x in np.ndenumerate(x_line):
        #: Compute the output of the function
        y = func(x, *args)
        #: Save the output
        f_line[idx] = y
    #: Return the result
    return x_line, f_line


def solve_underdetermined_system(A: NPArray[float], b: NPArray[float]) -> NPArray[float]:
    #: Retrieve the relevant dimensions
    n_x, n_u = A.shape[1], b.shape[1]
    #: Create the optimization variable
    x_sol = cvx.Variable((n_x, n_u))
    #: Create the equality constraint
    constraint = [A @ x_sol == b]
    #: Add as a cost function the L2-norm
    cost_function = cvx.norm(x_sol)
    #: Construct the optimization problem
    prob = cvx.Problem(cvx.Minimize(cost_function), constraints=constraint)
    #: Solve problem for a feasible solution
    prob.solve()
    #: Print warning if no solution was found
    if prob.status != "optimal":
        warnings.warn("No feasible input sequence was found, returning empty array", Warning, stacklevel=3)
        return np.array([])
    #: Save the solution
    x_sol = x_sol.value
    #: Remove any dimensions of size one
    x_sol = np.squeeze(x_sol)
    #: Return the result
    return x_sol


def set_input_output_matrix(sys: ct.StateSpace, B: NPArray[float] | None, C: NPArray[float] | None, D: NPArray[float] | None = None) -> ct.StateSpace:
    #: Check if the system needs to become autonomous
    if B is None and C is None:
        sys = ct.ss(sys.A, np.zeros((sys.nstates, 1)), np.eye(sys.nstates), np.zeros((sys.nstates, 1)))
    #: Check the feedforward matrix D
    if D is None:
        D = np.zeros((C.shape[0] if C is not None else sys.noutputs, B.shape[1] if B is not None else sys.ninputs))
    #: Set the new matrices
    sys = ct.StateSpace(sys.A, B if B is not None else sys.B, C if C is not None else sys.C, D, dt=sys.dt)
    #: Check if the system is controllable
    if np.linalg.matrix_rank(ct.ctrb(sys.A, sys.B)) != sys.nstates:
        warnings.warn(f"System is no longer controllable with input matrix B = \n{sys.B.round(2)}", Warning, stacklevel=2)
    #: Check if the system is observable
    if np.linalg.matrix_rank(ct.obsv(sys.A, sys.C)) != sys.nstates:
        warnings.warn(f"System is no longer observable with measurement matrix C = {sys.C.round(2)}", Warning, stacklevel=2)
    #: Return the results
    return sys
    

def get_discretization_with_rounding(sys_ct: ct.StateSpace, h: float, method: str = 'zoh', decimals: int = 4) -> ct.StateSpace:
    #: Perform the discretization
    sys_dt = sys_ct.sample(Ts=h, method=method)
    #: Retrieve the discretized matrices
    A_dt, B_dt, C_dt, D_dt = sys_dt.A, sys_dt.B, sys_dt.C, sys_dt.D
    #: Perform rounding
    A_dt, B_dt, C_dt, D_dt = (A_dt.round(decimals) + np.zeros(A_dt.shape), B_dt.round(decimals) + np.zeros(B_dt.shape), C_dt.round(decimals) + np.zeros(C_dt.shape), D_dt.round(decimals) + np.zeros(D_dt.shape))
    #: Construct the discretized system
    sys_dt = ct.StateSpace(A_dt, B_dt, C_dt, D_dt, dt=h)
    #: Return the discretized system
    return sys_dt


def discrete_time_prolonged_zoh(sys_dt: ct.StateSpace, n_sampling_periods: int) -> ct.StateSpace:
    #: Retrieve the discrete-time matrices
    A_dt, B_dt = sys_dt.A, sys_dt.B
    #: Compute the state dynamics matrix
    A_dt_i = np.linalg.matrix_power(A_dt, n_sampling_periods)
    #: Compute the input matrix
    B_dt_i = np.eye(sys_dt.nstates)
    for power in range(1, n_sampling_periods):
        #: Add the matrix exponent of A to the running total
        B_dt_i += np.linalg.matrix_power(A_dt, power)
    #: Combine the running total with the input matrix
    B_dt_i = B_dt_i @ B_dt
    #: Combine the discretized system
    sys_dt_i = ct.StateSpace(A_dt_i, B_dt_i, sys_dt.C, sys_dt.D, dt=(n_sampling_periods * sys_dt.dt))
    #: Return the system
    return sys_dt_i


def get_lyapunov_solution_ct(A: NPArray[float], Q: NPArray[float] | None = None, tolerance: float = 1E-3):
    # FIXME: We can just replace this with ct.lyap
    #: Retrieve the dimension
    n_x = A.shape[0]
    #: Set the rate matrix
    if Q is None:
        Q = np.eye(n_x)
    #: Create optimization variables
    P = cvx.Variable((n_x, n_x), PSD=True)
    #: Create constraints
    cons_1 = A @ P + P @ A.T + Q == np.zeros((n_x, n_x))
    cons_2 = P >> tolerance * np.eye(n_x)
    #: Construct the optimization problem
    prob = cvx.Problem(cvx.Maximize(0), constraints=[cons_1, cons_2])
    #: Solve LMIs
    prob.solve()
    #: Print warning if no solution was found
    if prob.status != "optimal":
        warnings.warn("No Lyapunov solution was found, is the system stable?", Warning, stacklevel=3)
    #: Save the solution
    P = P.value
    #: Return the result
    return P


def get_lyapunov_solution_decay_rate_from_gain(A_ct: NPArray[float], B_ct: NPArray[float], K: NPArray[float], tolerance: float = 1E-3) -> tuple[NPArray[float], NPArray[float]]:
    # NOTE: This function assume negative unity feedback
    # FIXME: This is not working, maybe we can do this symbolically?
    #: Extract the dimensions
    n_x = A_ct.shape[0]
    #: Construct the optimization variables
    P = cvx.Variable((n_x, n_x), PSD=True)
    Q = cvx.Variable((n_x, n_x), PSD=True)
    #: Construct the closed-loop system
    A_cl = A_ct + B_ct @ K
    #: Create constraints
    cons_1 = A_cl.T @ P + P @ A_cl + Q == np.zeros((n_x, n_x))
    cons_2 = P >> tolerance * np.eye(n_x)
    cons_3 = Q >> tolerance * np.eye(n_x)
    #: Construct the optimization problem
    prob = cvx.Problem(cvx.Maximize(0), constraints=[cons_1, cons_2, cons_3])
    #: Solve LMIs
    prob.solve()
    #: Print warning if no solution was found
    if prob.status != "optimal":
        warnings.warn("No solution was found, returning empty matrix", Warning, stacklevel=3)
        return np.array([]), np.array([])
    #: Save the solution
    P = P.value
    Q = Q.value
    #: Return the result
    return P, Q


def get_lowest_inter_sample_time_mazo(sys_ol_ct: ct.StateSpace, K: NPArray[float], alpha: float, tau_range: tuple[float, float], n_iter: int = 10) -> float:
    """
    # FROM: "An ISS self-triggered implementation of linear controllers", Mazo et al. (2010)  # nopep8
    # NOTE: This function assumes positive unity feedback, meaning u = Kx
    # FIXME: This function does not appear to be correct, it is returning weird results
    # FIXME: Maybe we are doing this wrong, as we are looking for the value for which the sign changes: this might not happen, so instead we need to look at the value for which it is approximately zero.
    """

    def get_determinant_matrix(tau: float, lambda_e: float, P: NPArray[float], C: NPArray[float], F: NPArray[float]) -> float:
        #: Construct the matrix
        M = C @ (sp.linalg.expm(F.T * tau) @ C.T @ P @ C @ sp.linalg.expm(F * tau) - C.T @ P @ C * np.exp(-lambda_e * tau)) @ C.T
        #: Compute the determinant
        det_M = np.linalg.det(M)
        #: Return the results
        return det_M 

    #: Retrieve the matrices
    A, B, n_x = sys_ol_ct.A, sys_ol_ct.B, sys_ol_ct.nstates
    #: Construct the closed-loop system matrix
    M = A + B @ K
    #: Retrieve the Lyapunov solution
    P = get_lyapunov_solution_ct(M)
    #: Find the largest eigenvalue
    lambda_0 = 1 / (2 * np.max(np.linalg.eigvals(P)))
    #: Set the decay rate
    lambda_e = alpha * lambda_0
    #: Create the augmented C matrix
    C = np.hstack((np.eye(n_x), np.zeros((n_x, n_x))))
    F = np.block([[A + B @ K, B @ K], [-A - B @ K, -B @ K]])
    #: Run a line search 
    x_line, f_line = get_line_search(get_determinant_matrix, (lambda_e, P, C, F), tau_range, n_iter)
    #: Check if the first index is zero
    if tau_range[0] == 0:  # Skip the first index
        x_line, f_line = np.delete(x_line, 0), np.delete(f_line, 0)
    # FIXME: Below is the sign change code, but this does not appear to work 
    # #: Calculate the the sign changes
    # sign_change = np.diff(np.sign(f_line)).astype(bool)
    # #: Check if there is at least a single sign change
    # if np.count_nonzero(sign_change) == 0:
    #     raise ValueError(f"The specified range tau_range is too small, no sign change detected. Increase the range.") 
    # #: Find the index before the first sign change
    # index_first_change = np.argmax(sign_change)
    # #: Find the corresponding inter-sample time
    # tau_min = x_line[index_first_change]
    # FIXME: Below is the tolerance code
    #: Set the tolerance
    tol_eps = 1E-3
    #: Find the tolerance withing zero
    tol_list = np.where(np.abs(f_line) < tol_eps)
    #: Check if there is at least a single sign change
    if np.count_nonzero(tol_list) == 0:
        raise ValueError(f"The specified range tau_range is too small, no value within the tolerance detected. Increase the resolution or increase the tolerance.") 
    #: Find the index first within the tolerance
    index_first_tol = np.argmax(tol_list)
    #: Find the corresponding inter-sample time
    tau_min = x_line[index_first_tol]
    #: Return the result
    return tau_min


def get_bounds_inter_sample_time_lemmon(sys_ol_ct: ct.StateSpace, L: NPArray[float], sigma: float) -> tuple[float, float]:

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
    #: Create the closed-loop matrix
    A_cl = A + B @ K
    #: Create the matrix M_bar
    M_ubar = np.linalg.cholesky(A_cl.T @ M @ A_cl)
    #: Calculate the lower and upper bound
    tau_lbar = (1 / mu_M(A, M)) * np.log(1 + mu_M(A, M) * np.sqrt(np.min(M_ubar @ N @ M_ubar)))
    tau_ubar = (1 / mu_M(A, M)) * np.log(1 + mu_M(A, M) * np.sqrt(np.max(M_ubar @ N @ M_ubar)))
    #: Return the result
    return tau_lbar, tau_ubar


def get_upper_bound_perturbation(sys_ol_ct: ct.StateSpace, B_w: NPArray[float], delta_ubar: float, tau: float) -> float:
    """
    FROM: "Efficient wireless networked control: Towards practical event-triggered implementations", Fu (2018)
    """

    def forced_response_element(s: float) -> float:
        #: Calculate the entry
        entry = np.exp(lambda_max * s)
        #: Return the result
        return entry

    #: Extract the matrices
    A, B = sys_ol_ct.A, sys_ol_ct.B
    #: Compute the largest eigenvalue
    lambda_max = np.max(np.linalg.eigvals((A.T + A) / 2))
    #: Compute the integral
    int_petb = sp.integrate.quad(forced_response_element, 0, tau)[0]
    #: Compute the spectral norm of the matrix
    B_w_norm = np.linalg.norm(B_w, ord=2)
    #: Compute the magnitude
    mag_delta_ubar = int_petb * B_w_norm * delta_ubar
    #: Return the results
    return mag_delta_ubar


@np_cache
def get_state_evolution_matrix(sys_ol_ct: ct.StateSpace, K: NPArray[float], s: float) -> NPArray[float]:
    """
    # NOTE: This function assumes positive feedback, i.e. u = Kx
    """

    def forced_response_matrix_element(s: float, row: int, column: int) -> float:
        #: Calculate the entry
        entry = sp.linalg.expm(A * s)[row, column].item()
        #: Return the result
        return entry

    #: Extract the matrices
    A, B = sys_ol_ct.A, sys_ol_ct.B
    #: Compute integral over each forced response matrix element
    F_s = np.zeros(A.shape)
    #: Loop the integration over each element
    for row, column in np.ndindex(A.shape):
        F_s[row, column] = sp.integrate.quad(forced_response_matrix_element, 0, s, args=(row, column))[0]
    #: Calculate the trajectory due to the state
    A_s = sp.linalg.expm(A * s)
    #: Calculate the forced response matrix
    M = A_s + F_s @ B @ K
    #: Return the forced response matrix
    return M


def get_maximal_controlled_invariant_subspace_kernel(sys_ol: ct.StateSpace, epsilon_eigvals: float = 1E-12) -> NPArray[float]:
    # FROM: "Controlled and conditioned invariant subspaces in linear system theory", Basile et al. (1969)| Algorithm 4.1.2  # nopep8
    #: Extract the matrices 
    A, B, C = sys_ol.A, sys_ol.B, sys_ol.C
    #: Compute the inverse mapping
    try:
        A_inv = np.linalg.inv(A)
    except np.linalg.LinAlgError:
        raise NotImplementedError("The dynamic matrix A appears to be singular, this algorithm cannot handle such systems")
    #: Initialize the first subspace as the kernel of C
    V_i = sp.linalg.null_space(C)
    while True:
        #: Create the inverse mapped subspace
        E_i = sp.linalg.orth(A_inv @ np.concatenate((V_i, B), axis=1))
        #: Remove linearly dependent rows
        # FIXME: This must be done to allow invertibility. However, due to numerical precision, orth() usually returns imaginary eigenvectors
        #: Create the projection matrices
        # FROM: https://math.stackexchange.com/questions/767882/linear-algebra-vector-space-how-to-find-intersection-of-two-subspaces/2179047#2179047  # nopep8
        P_V_i = V_i @ np.linalg.inv(V_i.T @ V_i) @ V_i.T
        P_E_i = E_i @ np.linalg.inv(E_i.T @ E_i) @ E_i.T
        #: Create the matrix M
        P_EV_i = P_V_i @ P_E_i
        #: Solve the eigenvalue equation
        eigvals, eigvecs = np.linalg.eig(P_EV_i)
        #: Select the eigenvalues with eigenvalue 1
        V_i_plus_1 = eigvecs[:, np.argwhere((np.abs(eigvals - 1)) < epsilon_eigvals).ravel()]
        #: Check if the basis is empty
        if V_i_plus_1.size == 0:
            #: Print a warning
            warnings.warn(f"Maximal controlled invariant subspace is empty, returning an empty array", RuntimeWarning, stacklevel=2)
            return np.array([])
        elif V_i_plus_1.shape[1] == V_i.shape[1]:
            #: Return the basis
            return V_i_plus_1
        else:
            #: Perform another iteration
            V_i = V_i_plus_1


def get_friend_controlled_invariant_subspace(V: NPArray[float], A: NPArray[float], B: NPArray[float]) -> NPArray[float]:
    # FROM: "Invariant and controlled invariant subspaces", Xiaoming Hu (2002)| Algorithm for finding F, p. 11  # nopep8
    # FIXME: Do the matrices A and B need to be discrete-time?
    #: Extract the number of inputs
    n_u = B.shape[1]
    #: Compute the mapping under A for the invariant subspace V
    AV = A @ V
    #: Compute the mapping parameter array Φ = [[x_1, ..., u_1, u_2, ...], [x_1, ..., u_1, u_2, ...], ...]
    Phi = np.linalg.solve(np.concatenate((V, B), axis=1), AV)
    #: Extract the inputs
    U = Phi[-n_u:, :]
    #: Solve the underdetermined system
    F = solve_underdetermined_system(V.T, -U.T)
    #: Add 1st dimension is absent
    if len(F.shape) == 1:
        F = F[np.newaxis, :]
    #: Return the result
    return F


def get_quadratic_triggering_matrix(n_x: int, condition: Literal['rel_state_error', 'mazo_iss'], trigger_params: Any | None = None) -> tuple[NPArray[float], tuple[str, ...]]:
    #: Match the condition
    match condition:
        # FROM: "An ISS self-triggered implementation of linear controllers", Mazo et al. (2010)
        case 'mazo_iss':
            # NOTE: This function assumes positive state feedback
            #: Retrieve the triggering params
            sys_ol_ct, K, sigma, s = trigger_params
            #: Retrieve the matrices
            A, B = sys_ol_ct.A, sys_ol_ct.B
            #: Construct the closed-loop system matrix
            M_ct = A + B @ K
            #: Get the Lyapunov solution
            P = get_lyapunov_solution_ct(M_ct)
            #: Find the largest eigenvalue
            lambda_0 = 1 / (2 * np.max(np.linalg.eigvals(P)))
            #: Select the desired decay rate
            lambda_e = sigma * lambda_0
            #: Compute the decay rate
            alpha = np.exp(-2 * lambda_e * s)
            #: Construct the triggering matrix
            Q = np.block([[P, np.zeros((n_x, n_x))], [np.zeros((n_x, n_x)), -alpha * P]])
            #: Set the state elements
            xi_elems = ('x_s', 'x_i')
        # FROM: "Periodic Event-Triggered Control for Linear Systems", Heemels et al. (2013)
        case 'rel_state_error':
            #: Extract the triggering parameter
            sigma, = trigger_params
            #: Construct the triggering matrix
            Q = np.block([[(1 - sigma ** 2) * np.eye(n_x), -np.eye(n_x)], [-np.eye(n_x), np.eye(n_x)]])
            #: Set the state elements
            xi_elems = ('x_s', 'x_i')
    #: Return the results
    return Q, xi_elems