"""
This example script gives an example of a continuous-time dynamical system interacting with a digital controller.
"""

# Import packages
import numpy as np
import control as ct
import setupScript
from setupScript import tableau_color_palette_10 as col_vals
from functions import utils, plots, sims
import matplotlib.pyplot as plt

# ------------ PARAMETERS ------------

# Set the random seed
seed_value = 45538370

# Set the sampling time
h = 0.05

# Import dynamics
sys_ol_ct, sys_c_dt = setupScript.get_plant_state_space('chaos_gleizer_2022'), setupScript.get_controller_state_space('chaos_gleizer_2022', h=h)
# sys_ol_ct, sys_c_dt = setupScript.get_plant_state_space('event_tallapragada_2012'), setupScript.get_controller_state_space('event_tallapragada_2012', h=h)

# Convert the dynamics to full-state feedback
if sys_ol_ct.noutputs != sys_ol_ct.nstates:
    sys_ol_ct = utils.set_input_output_matrix(sys_ol_ct, None, np.eye(sys_ol_ct.nstates))

# Set the noise characteristics
B_w, D_v = np.eye(2), np.eye(2)
mu_w, mu_v = np.zeros(sys_ol_ct.nstates), np.zeros(sys_ol_ct.noutputs)
Sigma_w, Sigma_v = 0.001 * np.eye(sys_ol_ct.nstates), 0. * np.eye(sys_ol_ct.noutputs)

# Set the initial condition
x_0 = np.array([-1, 5])

# Set the system parameters
B_w = np.eye(sys_ol_ct.nstates)
delta_ubar = 0.1

# Set the STC parameters
alpha = 0.5  # α ∈ (0,1), interpolation constant
Delta = 0.05
tau_lbar = 0.05
kappa_ubar = 20
sigma = 0.2
sigma_mazo = 0.9
L_lemmon = np.eye(sys_ol_ct.nstates)
sigma_lemmon = 0.000001

# Set parameters which determine runtime
T_end = 200  # Number of sample-times
inter_sample_res_ct = 50
n_iter = 10  # Number of steps in the bisection algorithm
n_points = 1000  # Number of points in the line search
tau_range = (0, 3)  # Range over which to perform the line search for tau_min

# ------------ SCRIPT ------------

def get_bounded_perturbation_func():

    def bounded_perturbation_func(sgnl: dict):
        #: Extract the time
        t = sgnl['T'][-1]
        # #: Do a pairwise check
        # if t < 2:
        #     w = 0 * np.ones(2)
        # elif t < 7:
        #     w = 0.2 * np.ones(2)
        # else:
        #     w = 0.1  * np.ones(2)
        w = 0.5  * np.ones(2)
        #: Return the process noise
        return w

    return bounded_perturbation_func

# Extract the static controller gain
if sys_c_dt.nstates != 0:
    raise ValueError(f"The feedback controller sys_c_ct must be static gain controller")
K = sys_c_dt.D

# Create a 'event'-triggered controller
sys_c_et = ct.ss(sys_c_dt.A, sys_c_dt.B, sys_c_dt.C, sys_c_dt.D, dt=True)

# Find the minimal inter-sample time
try:
    tau_min = utils.get_lowest_inter_sample_time_mazo(sys_ol_ct, -K, alpha, tau_range, n_points)
except ValueError:
    tau_min = 0

# Retrieve the triggering function
stc_trigger_func = sims.get_stc_mazo_iss(sys_ol_ct, -K, alpha, tau_lbar, Delta, kappa_ubar)

# Compute the discretized system
h = sys_c_dt.dt
sys_ol_dt = sys_ol_ct.sample(Ts=h, method='zoh')

# ------------ SIMULATION ------------

# Retrieve variables
A_ct, B_ct, K = sys_ol_ct.A, sys_ol_ct.B, sys_c_dt.D

Q, xi_elems = utils.get_quadratic_triggering_matrix(sys_ol_ct.nstates, 'rel_state_error', (sigma,))

M = A_ct - B_ct @ K

P = utils.get_lyapunov_solution_ct(M)

#: Find the largest eigenvalue
lambda_0 = 1 / (2 * np.max(np.linalg.eigvals(P)))
#: Select the desired decay rate
lambda_e = sigma * lambda_0

bounded_perturbation_func = get_bounded_perturbation_func()

stc_trigger_func_trigger_rel_state_error = sims.get_stc_static_quadratic(sys_ol_ct, sys_c_dt.dt, Q, xi_elems, kappa_ubar)

stc_trigger_func_mazo_iss = sims.get_stc_mazo_iss(sys_ol_ct, -K, sigma_mazo, sys_c_dt.dt, sys_c_dt.dt, kappa_ubar)

stc_trigger_func_lemmon_iss = sims.get_stc_lemmon_iss(sys_ol_ct, L_lemmon, sigma_lemmon)

#: Calculate lower and upper bound
tau_lbar_lemmon, tau_ubar_lemmon = utils.get_bounds_inter_sample_time_lemmon(sys_ol_ct, L_lemmon, sigma_lemmon) 

stc_trigger_func_mazo_iss_as_quadratic = sims.get_stc_dynamic_quadratic(sys_ol_ct, sys_c_dt.dt, 'mazo_iss', (sigma_mazo, -K, kappa_ubar))

petc_trigger_func_static_quadratic = sims.get_petc_static_quadratic(sys_ol_ct, sys_c_dt.dt, Q, xi_elems, kappa_ubar)

T_ct, T_i_ct, X_ct, Y_ct, Y_k = sims.sim(sys_ol_ct, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'T_i', 'X', 'Y', 'Y_k'), inter_sample_res_ct=inter_sample_res_ct)

T_dt, T_i_dt, X_dt, Y_dt, Y_k_2 = sims.sim(sys_ol_dt, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'T_i', 'X', 'Y', 'Y_k'))

T_stc, T_i_stc, X_stc, Y_stc, Y_k_stc, Kappa_stc, Tau_stc, T_k = sims.sim(sys_ol_ct, sys_c_dt, T_end, x_0, sampling_mode='STC', sampling_params=(stc_trigger_func_trigger_rel_state_error,), values_to_return=('T', 'T_i', 'X', 'Y', 'Y_k', 'Kappa_i', 'Tau_i', 'T_k'), inter_sample_res_ct=inter_sample_res_ct)

T_stc_dt, T_i_stc_dt, X_stc_dt, Y_stc_dt, Y_k_stc_dt = sims.sim(sys_ol_dt, sys_c_dt, T_end, x_0, sampling_mode='STC', sampling_params=(stc_trigger_func_trigger_rel_state_error,), values_to_return=('T', 'T_i', 'X', 'Y', 'Y_k'))

T_mazo, T_i_mazo, X_mazo, Y_mazo, Y_k_mazo, T_i_mazo = sims.sim(sys_ol_ct, sys_c_et, T_end, x_0, sampling_mode='STC', sampling_params=(stc_trigger_func_mazo_iss,), values_to_return=('T', 'T_i', 'X', 'Y', 'Y_k', 'T_i'), inter_sample_res_ct=inter_sample_res_ct)

# FIXME: For some reason this is reaaaallly slow, so we need to optimize it, possibly with caching? But this is actually difficult with nested Numpy arrays?
# T_mazo_2, X_mazo_2, Y_mazo_2, Y_k_mazo_2, Kappa_mazo = sims.sim(sys_ol_ct, sys_c_dt, T_end, x_0, sampling_mode='STC', sampling_params=(stc_trigger_func_mazo_iss_as_quadratic,), values_to_return=('T', 'X', 'Y', 'Y_k', 'Kappa_i'), inter_sample_res_ct=inter_sample_res_ct)

T_petc, T_k_petc, T_i_petc, X_petc, Y_petc, Y_k_petc, Y_i_petc = sims.sim(sys_ol_ct, sys_c_dt, T_end, x_0, sampling_mode='PETC', sampling_params=(petc_trigger_func_static_quadratic,), values_to_return=('T', 'T_k', 'T_i', 'X', 'Y', 'Y_k', 'Y_i'), inter_sample_res_ct=50)

T_w, T_k_w, T_i_w, X_w, Y_w, Y_i_w, Y_k_w, Kappa_w = sims.sim(sys_ol_ct, sys_c_dt, T_end, x_0, sampling_mode='PETC', sampling_params=(petc_trigger_func_static_quadratic,), values_to_return=('T', 'T_k', 'T_i', 'X', 'Y', 'Y_i','Y_k', 'Kappa_i'), random_seed=seed_value, noise_matrices=(B_w, D_v), noise_params=('custom', bounded_perturbation_func,), inter_sample_res_ct=inter_sample_res_ct)

T_gauss, T_k_gauss, T_i_gauss, X_gauss, Y_gauss, Y_k_gauss, Y_i_gauss, Kappa_gauss = sims.sim(sys_ol_dt, sys_c_dt, T_end, x_0, sampling_mode='PETC', sampling_params=(petc_trigger_func_static_quadratic,), values_to_return=('T', 'T_k', 'T_i', 'X', 'Y', 'Y_k', 'Y_i', 'Kappa_i'), noise_matrices=(B_w, D_v), noise_params=('normal', (mu_w, Sigma_w), (mu_v, Sigma_v)), inter_sample_res_ct=inter_sample_res_ct)

T_lemmon, T_i_lemmon, X_lemmon, X_hat_lemmon, Y_lemmon, Y_k_lemmon, Tau_lemmon = sims.sim(sys_ol_ct, sys_c_et, T_end, x_0, sampling_mode='STC', sampling_params=(stc_trigger_func_lemmon_iss,), values_to_return=('T', 'T_i', 'X', 'X_hat', 'Y', 'Y_k', 'Tau_i'))

# Compute the Lyapunov function
V_lyap = np.zeros(X_mazo.shape[1])
decay_function = np.zeros(X_mazo.shape[1])
for idx, t in np.ndenumerate(T_mazo):
    V_lyap[idx] = (X_mazo[:, idx].T @ P @ X_mazo[:, idx]).item()
    if t in T_i_mazo:
        # Retrieve the last sample
        x = X_mazo[:, idx]
        # Compute the stationary part
        V_x = (x.T @ P @ x).item()
        # Reset the elapsed time 
        s = 0
    # Compute the other decay function
    decay_function[idx] = V_x * np.exp(-lambda_e * s)
    # Increase s
    try:
        s += np.abs(T_mazo[idx] - T_mazo[idx[0] + 1])
    except IndexError:
        s += T_mazo[idx[0] - 1] - T_mazo[idx]

V_lyap_k = np.zeros(Y_k_mazo.shape[1])
for idx in range(V_lyap_k.size):
    V_lyap_k[idx] = Y_k_mazo[:, idx].T @ P @ Y_k_mazo[:, idx]

#: Compute the bound on the disturbance
max_norm_petb = utils.get_upper_bound_perturbation(sys_ol_ct, B_w, delta_ubar, tau_lbar)

# ------------ PRINTING ------------ 

# Print the found minimal range
print(f"tau_min: {tau_min}")

# Print the found norm on the disturbance
print(f"max_norm_petb: {max_norm_petb}")

# Print the statistics for Lemmon
print(f"------ LEMMON ------\n"f"tau_min: {tau_lbar_lemmon:.2f} ({np.min(Tau_lemmon[1:]):.2f}), tau_max: {tau_ubar_lemmon:.2f} ({np.max(Tau_lemmon):.2f})")

# ------------ PLOTTING ------------

fig_traj, ax_traj = plots.get_plot_trajectory_phase_space(X_ct, T=T_ct, T_i=T_i_ct, label=r"TTC", color=col_vals[1])

ax_traj = plots.get_plot_trajectory_phase_space(X_dt, T=T_dt, T_i=T_i_dt, label=r"TTC, DT", color=col_vals[2], ax_exist=ax_traj)

ax_traj = plots.get_plot_trajectory_phase_space(X_stc, T=T_stc, T_i=T_i_stc, label=r"STC quadratic", color=col_vals[3], ax_exist=ax_traj)

ax_traj = plots.get_plot_trajectory_phase_space(X_mazo, T=T_mazo, T_i=T_i_mazo, label=r"STC Mazo", color=col_vals[4], ax_exist=ax_traj)

# ax_traj = plots.get_plot_trajectory_phase_space(X_mazo_2, label=r"STC Mazo 2", color=col_vals[5], ax_exist=ax_traj)
# ax_traj.plot(Y_k_mazo_2[0, :], Y_k_mazo_2[1, :], 'd', color=col_vals[5])

ax_traj = plots.get_plot_trajectory_phase_space(X_petc, T=T_petc, T_k=T_k_petc, T_i=T_i_petc, label=r"PETC", color=col_vals[6], ax_exist=ax_traj)

ax_traj = plots.get_plot_trajectory_phase_space(X_stc_dt, T=T_stc_dt, T_i=T_i_stc_dt, label=r"STC, DT", color=col_vals[7], ax_exist=ax_traj)

ax_traj = plots.get_plot_trajectory_phase_space(X_w, T=T_w, T_k=T_k_w, T_i=T_i_w, label=r"PETC, $\boldsymbol{\delta}(t)$", color=col_vals[8], ax_exist=ax_traj)

ax_traj = plots.get_plot_trajectory_phase_space(X_gauss, T=T_gauss, T_k=T_k_gauss, T_i=T_i_gauss, label=r"PETC, DT, Gaussian", color=col_vals[9], ax_exist=ax_traj)

ax_traj = plots.get_plot_trajectory_phase_space(X_lemmon, T=T_lemmon, T_i=T_i_lemmon, label=r"STC, CT, Lemmon", color=col_vals[10 % len(col_vals)], ax_exist=ax_traj)

ax_traj.legend(loc="upper right")  # Add legend

fig_lyap, ax_lyap = plt.subplots()
ax_lyap.plot(range(V_lyap.size), V_lyap, label='Continuous-time')
ax_lyap.plot(range(decay_function.size), decay_function, '--', label='Bound')
ax_lyap.legend(loc="upper right")  # Add legend

# Show the figures
# plt.close(fig_traj)
plt.close(fig_lyap)
plt.show()

