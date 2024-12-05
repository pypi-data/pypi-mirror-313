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
import os
os.system('cls||clear')  # Clears the terminal, FROM: https://stackoverflow.com/questions/62742102/how-do-i-automatically-clear-the-terminal-in-vscode-before-execution-of-script  # nopep8

# ------------ PARAMETERS ------------

# Set the random seed
seed_value = 45538370

# Import dynamics
# FIXME: Actually, something is not working correctly.. the input seems to follow the (unknonw state) rather than the observed measurement
sys_ol_dt, sys_c_dt = setupScript.get_plant_state_space('detection_ferrari_2017'), setupScript.get_controller_state_space('detection_ferrari_2017', feedback=1)
# sys_ol_dt, sys_c_dt = setupScript.get_plant_state_space('murguia_cusum_2016'), setupScript.get_controller_state_space('murguia_cusum_2016')

# Convert the dynamics to full-state feedback
if sys_ol_dt.noutputs != sys_ol_dt.nstates or (sys_ol_dt.C != np.eye(sys_ol_dt.nstates)).any():
    sys_ol_dt = utils.set_input_output_matrix(sys_ol_dt, None, np.eye(sys_ol_dt.nstates))

# Set the noise characteristics
B_w, D_v = np.eye(sys_ol_dt.nstates), np.eye(sys_ol_dt.noutputs)
mu_w, mu_v = np.zeros(sys_ol_dt.nstates), np.zeros(sys_ol_dt.noutputs)
Sigma_w, Sigma_v = 0.001 * np.eye(sys_ol_dt.nstates), 0. * np.eye(sys_ol_dt.noutputs)

# Set the initial condition
x_0 = np.array([0., 0.])  # [-1, 5]

# Set the reference params
ref_period = 60
ref_radius = 2

# Set the attack parameters
k_a = 600
Delta_k = 480

# Set parameters which determine runtime
T_end = 1000  # Number of sample-times
inter_sample_res_ct = 50
n_iter = 10  # Number of steps in the bisection algorithm
n_points = 1000  # Number of points in the line search
tau_range = (0, 3)  # Range over which to perform the line search for tau_min

# ------------ SIMULATION ------------

# Add nominal trajectory
T_ttc, T_i_ttc, X_ttc, Y_ttc, Y_k_ttc = sims.sim(sys_ol_dt, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'T_i', 'X', 'Y', 'Y_k'))

# Add attack-free trajectory with Gaussian noise
T_w, T_i_w, X_w, Y_w, Y_k_w = sims.sim(sys_ol_dt, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'T_i', 'X', 'Y', 'Y_k'), random_seed=seed_value, noise_matrices=(B_w, D_v), noise_params=('normal', (mu_w, Sigma_w), (mu_v, Sigma_v)))

# Add replay attack trajectory with Gaussian noise
T_replay, T_i_replay, X_replay, Y_replay, Y_i_replay, U_replay = sims.sim(sys_ol_dt, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'T_i', 'X', 'Y', 'Y_i_prime', 'U_i'), random_seed=seed_value, noise_matrices=(B_w, D_v), noise_params=('normal', (mu_w, Sigma_w), (mu_v, Sigma_v)), attack_params=('delay_attack', k_a, Delta_k))

# Add replay attack trajectory with reference and Gaussian noise
T_ref, T_i_ref, X_ref, Y_ref, Y_i_ref, U_ref = sims.sim(sys_ol_dt, sys_c_dt, T_end, x_0, sampling_mode='TTC', values_to_return=('T', 'T_i', 'X', 'Y', 'Y_i_prime', 'U_i_prime'), random_seed=seed_value, noise_matrices=(B_w, D_v), noise_params=('normal', (mu_w, Sigma_w), (mu_v, Sigma_v)), reference_params=('circular', ref_period, ref_radius), attack_params=('delay_attack', k_a, Delta_k))

# ------------ PLOTTING ------------

# Add trajectory in phase space
fig_traj, ax_traj = plots.get_plot_trajectory_phase_space(X_ttc, T=T_ttc, T_i=T_i_ttc, label=r"TTC", color=col_vals[1])
ax_traj = plots.get_plot_trajectory_phase_space(X_w, T=T_w, T_i=T_i_w, label=r"TTC, $\boldsymbol{w}[k]$", color=col_vals[2], ax_exist=ax_traj)  # Add attack-free trajectory with Gaussian noise
ax_traj = plots.get_plot_trajectory_phase_space(X_replay, T=T_replay, T_i=T_i_replay, label=fr"TTC + replay ($k_{{\text{{a}}}}$: {k_a}, $\Delta k$: {Delta_k}), $\boldsymbol{{w}}[k]$", color=col_vals[3], ax_exist=ax_traj)  # Add replay attack trajectory with Gaussian noise
ax_traj = plots.get_plot_trajectory_phase_space(X_ref, T=T_ref, T_i=T_i_ref, label=fr"TTC + replay ($k_{{\text{{a}}}}$: {k_a}, $\Delta k$: {Delta_k}), $\boldsymbol{{w}}[k]$", color=col_vals[4], ax_exist=ax_traj)  # Add replay attack trajectory with Gaussian noise and reference

fig_traj.suptitle('Trajectory in phase space')  # Add title
ax_traj.legend(loc="upper right")  # Add legend

# Add output vector and norm
fig_norm, _ = plots.get_axes_inputs_outputs_state_norm(T_replay, T_i_replay, X_replay, U_replay, Y_i_replay, vertical_bounds=((0, 0.5), (-0.5, 0.5), (-0.5, 0.5)))
fig_norm.suptitle('Regulation with replay')  # Add title

# Add output vector and norm
fig_norm, _ = plots.get_axes_inputs_outputs_state_norm(T_ref, T_i_ref, X_ref, U_ref, Y_i_ref, vertical_bounds=((0, 6), (-1, 1), (-3, 3)))
fig_norm.suptitle('Reference tracking with replay')  # Add title

# Show the figures
# plt.close(fig_traj)
plt.show()

