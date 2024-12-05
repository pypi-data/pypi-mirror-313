"""
This is an example script showing the NCSim toolbox with a 3D state space with unstable dynamics
"""

# Import packages
import numpy as np
import scipy as sp
import control as ct
import setupScript
from setupScript import tableau_color_palette_10 as col_vals
from functions import utils, plots, sims
import matplotlib.pyplot as plt
import os
os.system('cls||clear')  # Clears the terminal, FROM: https://stackoverflow.com/questions/62742102/how-do-i-automatically-clear-the-terminal-in-vscode-before-execution-of-script  # nopep8

# ------------ PARAMETERS ------------

# Set the seed value
seed_value = 4553837

# Set the choice for the dynamics
dynamics_name = 'gleizer_computing_2023'

# Import dynamics
sys_ol_ct = setupScript.get_plant_state_space(dynamics_name)

# Set the input and output matrix
if dynamics_name == 'gleizer_computing_2023':
    B = None  # If None, leave the matrices as is  | np.array([[0], [0], [1]])
    C = np.array([[1, 0, 0]])  # If None, leave the matrices as is  | np.array([[1, -1, 0]])

# Set the initial condition
x_0 = np.array([0.1, 0.2, -0.1])  # [0.2, 0.4, 0.4] | [0.1, 0.2, -0.1]
f_0 = None  # Initial attack vector, if None calculate automatically
eps_f_0 = 1E-7
norm_u_0 = 1E-20

# Set the noise characteristics
B_w = np.eye(sys_ol_ct.nstates)
mu_w = np.zeros(sys_ol_ct.nstates)
Sigma_w = 0.001 * np.eye(sys_ol_ct.nstates)
delta_vec = np.array([0.1, 0.1, 0.1])
delta_ubar = 1.2 * np.linalg.norm(delta_vec, ord=2)

# Set the bounds in state-space
x_bounds_unsafe = ((-1.5, 1.5), (-2, 2), (-3, 3))  # ((-1, 1), (-1, 1), (-1, 1)) | ((-5, 5), (-3, 3), (-10, 10))
input_bounds = ((-20, 20),)

# Set the detection and performance parameters
eps_output = 2.
N_horizon = None  # If None, make it equal to the simulation time

# Set the system parameters
h = 0.2
kappa_ubar = 10
sigma = 0.2
h_mazo = 0.01
N_max_mazo = 30
sigma_mazo = 0.9

# Set the parameters which determine runtime
T_end = 49 * h
break_on_norm = 1E10
inter_sample_res_ct = 1000

# ------------ SCRIPT ------------

# Reconfigure the system
if B is not None or C is not None:
    sys_ol_ct = utils.set_input_output_matrix(sys_ol_ct, B, C)

# Compute the discretization 
sys_ol_dt = sys_ol_ct.sample(Ts=h, method='zoh')

# Compute a output-feedback controller
sys_c_dt = ct.ss([], [], [], 1.5, dt=h)

# Create a full-state feedback controller
sys_c_fsf_dt = ct.ss([], [], [], [1.5, 0, 0], dt=h)

# Create a full-state feedback controller, event-triggered
sys_c_fsf_et = ct.ss([], [], [], [1.5, 0, 0], dt=True)

# Extract the full-state feedback matrix
K = sys_c_fsf_dt.D

# Get the maximal controlled-invariant subspace contained in the kernel
V = utils.get_maximal_controlled_invariant_subspace_kernel(sys_ol_dt)

# Extract the eigenvalues and eigenspace
Lambda, E = np.linalg.eig(sys_ol_ct.A)
unstable_direction = E[:, 0].real

# Get the quadratic triggering matrix
Q, _ = utils.get_quadratic_triggering_matrix(sys_ol_ct.nstates, 'rel_state_error', (sigma,))

# Get the STC trigger parameter
stc_trigger_func_trigger_rel_state_error = sims.get_stc_static_quadratic(sys_ol_ct, h, Q, ('x_s', 'x_hat_i'), kappa_ubar)

stc_trigger_func_mazo_iss = sims.get_stc_mazo_iss(sys_ol_ct, -K, sigma_mazo, h_mazo, h_mazo, N_max_mazo, xi_elems=('x_s', 'x_hat_i'))

# Calculate the initial attack state
if f_0 is None:
    #: Pick the first span
    f_0 = eps_f_0 * V[:, 0]

# Calculate the norm on the bound
bound_norm_x = utils.max_vector_norm_outside_box(x_bounds_unsafe)

# ------------ SIMULATION ------------

# Nominal TTC dynamics
T_ct, T_i_ct, X_ct, Y_ct, Y_k_ct, U_ct = sims.sim(sys_ol_ct, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'T_i', 'X', 'Y', 'Y_k', 'U_i_prime'), inter_sample_res_ct=inter_sample_res_ct)

# TTC with transmission zero attack
T_trans, T_i_trans, X_trans, Y_trans, Y_k_trans, U_trans = sims.sim(sys_ol_ct, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'T_i', 'X', 'Y', 'Y_k', 'U_i_prime'), attack_params=('zda_transmission_zero', sys_ol_dt, norm_u_0), break_params=('2_norm', break_on_norm), inter_sample_res_ct=inter_sample_res_ct)

# STC with switched zero attack
T_switch, T_i_switch, X_switch, X_hat_switch, Y_switch, Y_k_switch, U_switch, Kappa_switch = sims.sim(sys_ol_ct, sys_c_fsf_dt, T_end, x_0, sampling_mode='STC', sampling_params=(stc_trigger_func_trigger_rel_state_error,), values_to_return=('T', 'T_i', 'X', 'X_hat', 'Y', 'Y_k', 'U_i_prime', 'Kappa_i'), observer_params=('almeida_observer', h, kappa_ubar), attack_params=('switched_zda', sys_ol_dt, h, f_0, kappa_ubar), break_params=('2_norm', break_on_norm), inter_sample_res_ct=inter_sample_res_ct)

# STC with switched zero attack, DT + noise
T_switch_dt, T_i_switch_dt, X_switch_dt, X_hat_switch_dt, Y_switch_dt, Y_k_switch_dt, U_switch_dt, Kappa_switch_dt = sims.sim(sys_ol_dt, sys_c_fsf_dt, T_end, x_0, sampling_mode='STC', sampling_params=(stc_trigger_func_trigger_rel_state_error,), values_to_return=('T', 'T_i', 'X', 'X_hat', 'Y', 'Y_k', 'U_i_prime', 'Kappa_i'), noise_matrices=(B_w, None), noise_params=('normal', (mu_w, Sigma_w), None), random_seed=seed_value, observer_params=('almeida_observer', h, kappa_ubar), attack_params=('switched_zda', sys_ol_dt, h, f_0, kappa_ubar), break_params=('2_norm', break_on_norm))

# STC with switched zero attack, CT + Mazo + bounded perturb
# FIXME: Not working..
T_switch_mazo, T_i_switch_mazo, X_switch_mazo, X_hat_switch_mazo, Y_switch_mazo, Y_k_switch_mazo, U_switch_mazo, Tau_switch_mazo = sims.sim(sys_ol_ct, sys_c_fsf_et, T_end, x_0, sampling_mode='STC', sampling_params=(stc_trigger_func_mazo_iss,), values_to_return=('T', 'T_i', 'X', 'X_hat', 'Y', 'Y_k', 'U_i_prime', 'Tau_i'), noise_matrices=(B_w, None), noise_params=('constant', delta_vec), random_seed=seed_value, observer_params=('almeida_observer', h, kappa_ubar), attack_params=('switched_zda', sys_ol_dt, h, f_0, kappa_ubar), break_params=('2_norm', break_on_norm))

# ------------ PLOTTING ------------

# Add the trajectory without attack
fig_traj, ax_traj = plots.get_plot_trajectory_phase_space(X_ct, T=T_ct, T_i=T_i_ct, label=r"TTC", color=col_vals[0], x_bounds=x_bounds_unsafe, clip_trajectory='clip_to_nan')

# Add the trajectory with transmission zeros attack
ax_traj = plots.get_plot_trajectory_phase_space(X_trans, label=r"TTC (ZDA trans)", color=col_vals[1], x_bounds=x_bounds_unsafe, clip_trajectory='clip_to_nan', ax_exist=ax_traj)

# Add the trajectory with switched ZDA
ax_traj = plots.get_plot_trajectory_phase_space(X_switch, T=T_switch, T_i=T_i_switch, label=r"STC (ZDA switch)", color=col_vals[5], x_bounds=x_bounds_unsafe, clip_trajectory='clip_to_nan', ax_exist=ax_traj)

# Add the trajectory with switched ZDA DT, with noise
ax_traj = plots.get_plot_trajectory_phase_space(X_switch_dt, label=r"STC, DT (ZDA switch)", color=col_vals[6], x_bounds=x_bounds_unsafe, clip_trajectory='clip_to_nan', ax_exist=ax_traj)

# Add the trajectory with switched ZDA CT Mazo, with noise
ax_traj = plots.get_plot_trajectory_phase_space(X_switch_mazo, label=r"STC | Mazo, CT (ZDA switch)", color=col_vals[7], x_bounds=x_bounds_unsafe, clip_trajectory='clip_to_nan', ax_exist=ax_traj)

# Add the unobservable subspace
_ = plots.get_plot_subspace(V, color=col_vals[3], x_bounds=x_bounds_unsafe, alpha=0.5, ax_exist=ax_traj)

# Add the unstable direction
_ = plots.get_plot_arrow_3d(unstable_direction, color=col_vals[2], label=r"$\boldsymbol{e}_{\text{unstable}}$", ax_exist=ax_traj)

fig_traj.suptitle(f"Trajectory in phase space")
ax_traj.legend(loc="upper right")  # Add legend

# TTC without attack
fig_nom, ax_nom = plots.get_axes_inputs_outputs_state_norm(T_ct, T_i_ct, X_ct, U_ct, Y_k_ct, vertical_bounds=((0, bound_norm_x), *input_bounds, (-eps_output, eps_output)))
fig_nom.suptitle(f"TTC without attack")

# TTC with transmission zero attack attack
fig_trans, ax_trans = plots.get_axes_inputs_outputs_state_norm(T_trans, T_i_trans, X_trans, U_trans, Y_k_trans, vertical_bounds=((0, bound_norm_x), *input_bounds, (-eps_output, eps_output)))
fig_trans.suptitle(f"TTC with transmission ZDA")

# STC with switched zero attack
fig_switch, ax_switch = plots.get_axes_inputs_outputs_state_norm(T_switch, T_i_switch, X_switch, U_switch, Y_k_switch, X_hat=X_hat_switch, Kappa=Kappa_switch, vertical_bounds=((0, bound_norm_x), *input_bounds, (-eps_output, eps_output)))
fig_switch.suptitle(f"STC with switched ZDA")

# STC with switched zero attack, DT + noise
fig_switch_dt, ax_switch_dt = plots.get_axes_inputs_outputs_state_norm(T_switch_dt, T_i_switch_dt, X_switch_dt, U_switch_dt, Y_k_switch_dt, X_hat=X_hat_switch_dt, Kappa=Kappa_switch_dt, vertical_bounds=((0, bound_norm_x), *input_bounds, (-eps_output, eps_output)))
fig_switch_dt.suptitle(f"STC with switched ZDA, DT + noise")

# STC from Mazo, CT
fig_switch_mazo, ax_switch_mazo = plots.get_axes_inputs_outputs_state_norm(T_switch_mazo, T_i_switch_mazo, X_switch_mazo, U_switch_mazo, Y_k_switch_mazo, X_hat=X_hat_switch_mazo, Kappa=Tau_switch_mazo, vertical_bounds=((0, bound_norm_x), *input_bounds, (-eps_output, eps_output)))
fig_switch_mazo.suptitle(f"STC with switched ZDA, CT | Mazo")

# Show the figures
# plt.close(fig_traj)
plt.close(fig_nom)
# plt.close(fig_trans)
# plt.close(fig_switch)
# plt.close(fig_switch_dt)
plt.show()