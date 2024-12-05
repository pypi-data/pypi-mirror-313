"""
This is an example script showing the NCSim toolbox with a 3D state space 
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

# Set the choice for the dynamics
dynamics_name = 'wang_fault_2008'  # 'temp_1'

# Import dynamics
sys_ol_ct = setupScript.get_plant_state_space(dynamics_name)

# Set the input and output matrix
if dynamics_name == 'wang_fault_2008':
    B = np.array([[0], [0], [1]])  # If None, leave the matrices as is  | np.array([[0], [0], [1]])
    C = np.array([[1, -1, 0]])  # If None, leave the matrices as is  | np.array([[1, -1, 0]])
elif dynamics_name == 'temp_1':
    B = None  # If None, leave the matrices as is  | np.array([[0], [0], [1]])
    C = None  # If None, leave the matrices as is  | np.array([[1, -1, 0]])

# Set the initial condition
x_0 = np.array([0, 0, 0])  # np.array([0.1, 0.15, 0.5])
f_0 = None  # Initial attack vector, if None calculate automatically
eps_f_0 = 1E-3

# Set the bounds in state-space
x_bounds_unsafe = ((-1, 1), (-2, 2), (-3, 3))  # ((-1, 1), (-1, 1), (-1, 1)) | ((-5, 5), (-3, 3), (-10, 10))
input_bounds = ((-20, 20),)

# Set the noise characteristics
delta_vec = np.array([100, 100, 100])
delta_ubar = 1.2 * np.linalg.norm(delta_vec, ord=2)

# Set the detection and performance parameters
eps_output = 0.005
N_horizon = None  # If None, make it equal to the simulation time

# Set the system parameters
h = 0.2
kappa_ubar = 10
sigma = 0.2

# Set the parameters which determine runtime
T_end = 20
break_on_norm = 1E4
inter_sample_res_ct = 100

# ------------ SCRIPT ------------

# Reconfigure the system
if B is not None or C is not None:
    sys_ol_ct = utils.set_input_output_matrix(sys_ol_ct, B, C)

# Compute the discretization 
sys_ol_dt = sys_ol_ct.sample(Ts=h, method='zoh')

# Compute a zero-gain controller
sys_c_dt = ct.ss([], [], [], np.zeros(sys_ol_ct.noutputs), dt=h)

# Create a 'event'-triggered controller
sys_c_et = ct.ss([], [], [], np.zeros(sys_ol_ct.nstates), dt=True)

# Get the maximal controlled-invariant subspace contained in the kernel
V = utils.get_maximal_controlled_invariant_subspace_kernel(sys_ol_dt)

# Get the quadratic triggering matrix
Q, _ = utils.get_quadratic_triggering_matrix(sys_ol_ct.nstates, 'rel_state_error', (sigma,))

# Get the STC trigger parameter
stc_trigger_func_trigger_rel_state_error = sims.get_stc_static_quadratic(sys_ol_ct, h, Q, ('x_s', 'x_hat_i'), kappa_ubar)

# Calculate the initial attack state
if f_0 is None:
    #: Pick the first span
    f_0 = eps_f_0 * V[:, 0]

# Calculate the norm on the bound
bound_norm_x = utils.max_vector_norm_outside_box(x_bounds_unsafe)

# ------------ SIMULATION ------------

T, X_ct, Y_ct, Y_k = sims.sim(sys_ol_ct, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'X', 'Y', 'Y_k'), inter_sample_res_ct=inter_sample_res_ct)

T_dt, X_dt, Y_dt, Y_k_dt = sims.sim(sys_ol_dt, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'X', 'Y', 'Y_k'))

T_zda, T_k_zda, X_zda, Y_zda, Y_k_zda, U_zda = sims.sim(sys_ol_ct, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'T_k', 'X', 'Y', 'Y_k', 'U_i_hold'), attack_params=('zda_transmission_zero', sys_ol_dt, None), hold_params=('saturation', input_bounds), break_params=('2_norm', break_on_norm), inter_sample_res_ct=inter_sample_res_ct)

T_opt, T_k_opt, X_opt, Y_opt, Y_k_opt, U_opt = sims.sim(sys_ol_ct, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'T_k', 'X', 'Y', 'Y_k', 'U_i_hold'), attack_params=('zda_optimization', sys_ol_dt, T_end, x_0, x_bounds_unsafe, eps_output, input_bounds), hold_params=('saturation', input_bounds), break_params=('2_norm', break_on_norm), inter_sample_res_ct=inter_sample_res_ct)

# FIXME: This code is not working, the disturbance regulation is screwed up
# T_opt_w, T_k_opt_w, X_opt_w, Y_opt_w, Y_k_opt_w, U_opt_w = sims.sim(sys_ol_ct, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'T_k', 'X', 'Y', 'Y_k', 'U_i_hold'), noise_params=('constant', delta_vec), attack_params=('zda_optimization', sys_ol_dt, T_end, x_0, x_bounds_unsafe, eps_output, input_bounds), hold_params=('saturation', input_bounds), break_params=('2_norm', break_on_norm), inter_sample_res_ct=inter_sample_res_ct)

T_switch, T_k_switch, X_switch, X_hat_switch, Y_switch, Y_k_switch, U_switch, Kappa_switch = sims.sim(sys_ol_ct, sys_c_et, T_end, x_0, sampling_mode='STC', sampling_params=(stc_trigger_func_trigger_rel_state_error,), values_to_return=('T', 'T_k', 'X', 'X_hat', 'Y', 'Y_k', 'U_i_hold', 'Kappa_i'), observer_params=('almeida_observer', h, kappa_ubar), attack_params=('switched_zda', sys_ol_ct, h, f_0, kappa_ubar), hold_params=('saturation', input_bounds), break_params=('2_norm', break_on_norm), inter_sample_res_ct=inter_sample_res_ct)

T_dt_switch, T_dt_k_switch, X_dt_switch, X_dt_hat_switch, Y_dt_switch, Y_dt_k_switch, U_dt_switch, Kappa_dt_switch = sims.sim(sys_ol_dt, sys_c_et, T_end, x_0, sampling_mode='STC', sampling_params=(stc_trigger_func_trigger_rel_state_error,), values_to_return=('T', 'T_k', 'X', 'X_hat', 'Y', 'Y_k', 'U_i_hold', 'Kappa_i'), observer_params=('almeida_observer', h, kappa_ubar), attack_params=('switched_zda', sys_ol_dt, h, f_0, kappa_ubar), hold_params=('saturation', input_bounds), break_params=('2_norm', break_on_norm), inter_sample_res_ct=inter_sample_res_ct)

# ------------ PLOTTING ------------

fig_traj, ax_traj = plots.get_plot_trajectory_phase_space(X_ct, label=r"TTC", color=col_vals[1])
fig_traj.suptitle(f"Trajectory in phase space")

_ = plots.get_plot_trajectory_phase_space(X_dt, label=r"TTC, DT", color=col_vals[2], ax_exist=ax_traj)

_ = plots.get_plot_trajectory_phase_space(X_zda, label=r"TTC, ZDA", color=col_vals[4], clip_trajectory='clip_to_nan', x_bounds=x_bounds_unsafe, ax_exist=ax_traj)

_ = plots.get_plot_trajectory_phase_space(X_opt, label=r"TTC, ZDA opt", color=col_vals[5], clip_trajectory='clip_to_nan', x_bounds=x_bounds_unsafe, ax_exist=ax_traj)

# _ = plots.get_plot_subspace(V, color=col_vals[3], x_bounds=x_bounds_unsafe, alpha=0.5, ax_exist=ax_traj)

v_offset_1 = eps_output * (np.cross(V[:, 0], V[:, 1]) / np.linalg.norm(np.cross(V[:, 0], V[:, 1])))
v_offset_2 = eps_output * (np.cross(V[:, 1], V[:, 0]) / np.linalg.norm(np.cross(V[:, 0], V[:, 1])))
_ = plots.get_plot_plane_3d(ax_traj, V[:, 0], V[:, 1], v_offset_1, color=col_vals[3], x_bounds=x_bounds_unsafe, alpha=0.2)
_ = plots.get_plot_plane_3d(ax_traj, V[:, 0], V[:, 1], v_offset_2, color=col_vals[3], x_bounds=x_bounds_unsafe, alpha=0.2)

ax_traj.legend(loc="upper right")  # Add legend

fig_trans, ax_trans = plots.get_axes_inputs_outputs_state_norm(T_zda, T_k_zda, X_zda, U_zda, Y_k_zda, vertical_bounds=((0, bound_norm_x), *input_bounds, (-eps_output, eps_output)))
fig_trans.suptitle(f"Transmission zero outcome")

fig_norm, ax_norm = plots.get_axes_inputs_outputs_state_norm(T_opt, T_k_opt, X_opt, U_opt, Y_k_opt, vertical_bounds=((0, bound_norm_x), *input_bounds, (-eps_output, eps_output)))
fig_norm.suptitle(f"Optimization outcome")

# fig_noise, ax_noise = plots.get_axes_inputs_outputs_state_norm(T_opt_w, T_k_opt_w, X_opt_w, U_opt_w, Y_k_opt_w, vertical_bounds=((0, bound_norm_x), *input_bounds, (-eps_output, eps_output)))
# fig_noise.suptitle(f"Optimization outcome with noise")

fig_switch, ax_switch = plots.get_axes_inputs_outputs_state_norm(T_switch, T_k_switch, X_switch, U_switch, Y_k_switch, X_hat=X_hat_switch, Kappa=Kappa_switch, vertical_bounds=((0, 1), *input_bounds, (-eps_output, eps_output)))
fig_switch.suptitle(f"Switched ZDA")

fig_switch_dt, ax_switch_dt = plots.get_axes_inputs_outputs_state_norm(T_dt_switch, T_dt_k_switch, X_dt_switch, U_dt_switch, Y_dt_k_switch, X_hat=X_dt_hat_switch, Kappa=Kappa_dt_switch, vertical_bounds=((0, 1), *input_bounds, (-eps_output, eps_output)))
fig_switch_dt.suptitle(f"Switched ZDA (DT)")

# Show the figures
# plt.close(fig_traj)
# plt.close(fig_trans)
# plt.close(fig_norm)
# plt.close(fig_noise)
plt.close(fig_switch)
plt.close(fig_switch_dt)
plt.show()