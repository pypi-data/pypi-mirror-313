"""
Script which handles all plotting methods.

# NOTE: This script adheres to the control package convention on time series
# FROM: https://python-ct.readthedocs.io/en/latest/conventions.html#time-series-convention
"""

# Import packages
import numpy as np
import utils
from utils import NPArray
import matplotlib.pyplot as plt
from matplotlib import colors as mplcolors
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.patches import FancyArrowPatch  # For plotting 
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # For plotting polygons in 3d
from mpl_toolkits.mplot3d import proj3d  # For fancy arrows
from typing import Literal
import warnings

# Tableau colors
# FROM: https://jrnold.github.io/ggthemes/reference/tableau_color_pal.html
color_palette = ["#4E79A7",  # 0: Blue
                            "#F28E2B",  # 1: Orange
                            "#E15759",  # 2: Red
                            "#76B7B2",  # 3: Teal
                            "#59A14F",  # 4: Green
                            "#EDC948",  # 5: Yellow
                            "#B07AA1",  # 6: Purple
                            "#FF9DA7",  # 7: Pink
                            "#9C755F",  # 8: Brown
                            "#BAB0AC"]  # 9: Gray


# ------------ CLASSES ------------


class Arrow3D(FancyArrowPatch):
    # FROM: https://stackoverflow.com/questions/22867620/putting-arrowheads-on-vectors-in-a-3d-plot
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))

        return np.min(zs)
    

# ------------ PLOTTING ------------


def get_plot_trajectory_phase_space(X: NPArray[float], T: NPArray | None = None, T_k: NPArray | None = None, T_i: NPArray | None = None, x_bounds: tuple[tuple[float, float], ...] | None = None, clip_trajectory: Literal['clip_to_box', 'clip_to_nan'] | None = None, label: str | None = None, color: str = color_palette[0], ax_exist: Axes | None = None) -> tuple[Figure, Axes]:

    def get_clipped_trajectories(X: NPArray[float], x_bounds: tuple[tuple[float, float], ...] | None = None) -> NPArray[float]:
        #: Extract the bounds
        if x_bounds is None:
            #: Extract bounds from axis
            x_bounds = ((ax.get_xlim()), (ax.get_ylim()), (ax.get_zlim()))
        #: Initialize the clipped state
        X_clipped = np.copy(X)
        #: Loop over all states
        for idx in range(X.shape[1]):
            #: Extract the state
            x = X[:, idx]
            #: Loop over all entries
            for elem, x_i in np.ndenumerate(x):
                #: Match the clipping mode
                match clip_trajectory:
                    case 'clip_to_box':
                        X_clipped[elem, idx] = np.clip(X[elem, idx], x_bounds[elem[0]][0], x_bounds[elem[0]][1])
                    case 'clip_to_nan':
                        if not x_bounds[elem[0]][0] <= x_i <= x_bounds[elem[0]][1]:
                            X_clipped[:, idx] = np.full(X_clipped[:, idx].size, np.nan)
                            break
        #: Return the result
        return X_clipped
    
    #: Retrieve the dimensionality
    n_x = X.shape[0]
    #: Add to existing axes (if they exist)
    if ax_exist is not None:
        #: Set equal
        fig, ax = None, ax_exist
    else:
        if n_x == 3:
            #: Set the projection to 3d
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
        else:
            #: Create a figure
            fig, ax = plt.subplots()
    #: Clip the trajectories
    if clip_trajectory is not None:
        X_clipped = get_clipped_trajectories(X, x_bounds)
    else:
        X_clipped = X
    #: Create concatenation arrays
    X_clipped_tuple = tuple([x_idx for x_idx in X_clipped])
    #: Create plots
    ax.plot(*X_clipped_tuple, color=color, label=label)
    if T is not None and T_k is not None:
        #: Find the indices where a sample was taken
        indices_k = np.where(np.in1d(T, T_k))[0]
        #: Confine the state vector
        X_k_clipped = X_clipped[:, indices_k]
        #: Convert to a tuple
        X_k_clipped_tuple = tuple([x_idx for x_idx in X_k_clipped])
        #: Plot the samples
        ax.plot(*X_k_clipped_tuple, '.', color=color, markersize=4)
    if T is not None and T_i is not None:
        #: Find the indices where a measurement was transmitted
        indices_i = np.where(np.in1d(T, T_i))[0]
        #: Confine the state vector
        X_i_clipped = X_clipped[:, indices_i]
        #: Convert to a tuple
        X_i_clipped_tuple = tuple([x_idx for x_idx in X_i_clipped])
        #: Plot the samples
        ax.plot(*X_i_clipped_tuple, 'd', color=color, markersize=3)
    #: Set the axis labels
    ax.set_xlabel(r'$x_{1}$')
    ax.set_ylabel(r'$x_{2}$', rotation='horizontal')
    if n_x == 3:
        ax.set_zlabel(r'$x_{3}$')
    #: Create the bounds
    if x_bounds is not None:
        ax.set_xlim(x_bounds[0][0], x_bounds[0][1])
        ax.set_ylim(x_bounds[1][0], x_bounds[1][1])
        if n_x == 3:
            ax.set_zlim(x_bounds[2][0], x_bounds[2][1])
    #: Return the axis
    if ax_exist is not None:
        return ax
    else:
        return fig, ax
    

def get_plot_subspace(V: NPArray[float], x_bounds: tuple[tuple[float, float], ...] | None = None, label: str | None = None, color: str = color_palette[0], alpha: float = 1.,
                      ax_exist: Axes | None = None) -> tuple[Figure, Axes]:
    """
    V ∈ ℝ^{n_x × dim_v} is a basis for the subspace
    # FIXME: I think not specifying x_bounds leads to trouble.
    # TODO: Currently, we are assuming the vectors in V are linearly independent: we need to rigorously check this when the argument are first passed.
    """

    #: Retrieve the dimensionality
    if V.size != 0:
        n_x, dim_v = V.shape[0], V.shape[1]
    else:  # Empty basis
        #: Retrieve the projection
        if ax_exist is not None:
            #: Retrieve the projection
            if ax_exist.name == '3d':
                n_x, dim_v = 3, 0
            else:
                n_x, dim_v = 2, 0
        else:  # NOTE: This assumes as standard that the plotting is in 3d
            n_x, dim_v = 3, 0
    #: Add to existing axes (if they exist)
    if ax_exist is not None:
        #: Set equal
        fig, ax = None, ax_exist
    else:
        if n_x == 3:
            #: Set the projection to 3d
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
        else:
            #: Create a figure
            fig, ax = plt.subplots()
    #: Get the bounds
    if x_bounds is None:
        if n_x == 2:
            x_bounds = ((ax.get_xlim()), (ax.get_ylim()))
        else:
            x_bounds = ((ax.get_xlim()), (ax.get_ylim()), (ax.get_zlim()))
    #: Check the dimensionality of the subspace V
    match dim_v:
        case 0:  # Origin
            if n_x == 2:  # Planar
                raise NotImplementedError(f"Planar plotting is not yet implemented")
            else:  # 3-dimensional
                ax.plot(0, 0, 0, '.', color=color)
        case 1:  # Line
            if n_x == 2:  # Planar
                raise NotImplementedError(f"Planar plotting is not yet implemented")
            else:  # 3-dimensional
                ax = get_plot_line_3d(ax, V[:, 0], np.array([0, 0, 0]), x_bounds, color, alpha)
        case 2:  # Plane
            if n_x == 2:  # Planar
                raise NotImplementedError(f"Planar plotting is not yet implemented")
            else:  # 3-dimensional
                ax = get_plot_plane_3d(ax, V[:, 0], V[:, 1], np.array([0, 0, 0]), x_bounds, color, alpha)
        case 3:  # Box
            if n_x == 2:  # Planar
                raise NotImplementedError(f"Planar plotting is not yet implemented")
            else:  # 3-dimensional
                ax = get_plot_box_3d(ax, x_bounds, color, alpha)
    #: Set the axis labels
    ax.set_xlabel(r'$x_{1}$')
    ax.set_ylabel(r'$x_{2}$', rotation='horizontal')
    if n_x == 3:
        ax.set_zlabel(r'$x_{3}$')
    # TODO: Make it such that the <label> parameter shows up with the correct icon
    #: Create the bounds
    if x_bounds is not None:
        ax.set_xlim(x_bounds[0][0], x_bounds[0][1])
        ax.set_ylim(x_bounds[1][0], x_bounds[1][1])
        if n_x == 3:
            ax.set_zlim(x_bounds[2][0], x_bounds[2][1])
    #: Return the axis
    if ax_exist is not None:
        return ax
    else:
        return fig, ax


def get_plot_plane_3d(ax: Axes, v_1: NPArray[float], v_2: NPArray[float], v_offset: NPArray[float], x_bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]], color: str = color_palette[0], alpha: float = 1.) -> Axes:
    # TODO: Merge this with the line plot
    #: Get the list of intersection points
    intersection_list = get_intersection_bounding_box_3d(v_1, v_2, v_offset, x_bounds)
    #: Compute the normal vector to the plane
    normal = np.cross(v_1, v_2)
    #: Sort the points
    intersection_list = get_sorted_list_of_vertices(intersection_list, normal)
    #: Compute the hexadecimal value to rgb
    color_rgba = [*mplcolors.to_rgb(color), alpha]
    #: Add the polygon
    ax.add_collection3d(Poly3DCollection([intersection_list], color=[color_rgba for _ in range(len(intersection_list))]))
    #: Return the results
    return ax


def get_plot_arrow_3d(arrow: NPArray[float], color: str = color_palette[0], label: str | None = None, start: NPArray[float] = np.array([0, 0, 0]), ax_exist: Axes | None = None) -> tuple[Figure, Axes]:
    #: Add to existing axes (if they exist)
    if ax_exist is not None:
        #: Set equal
        fig, ax = None, ax_exist
    else:
        #: Create a figure
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
    #: Create the arrow
    arrow = Arrow3D([start[0], arrow[0]], [start[1], arrow[1]], [start[2], arrow[2]],
                    **dict(mutation_scale=10, arrowstyle="-|>", color=color, shrinkA=0, shrinkB=0))
    #: Add the arrow to the plot
    ax.add_artist(arrow)
    #: Add a label
    if label is not None:
        ax.plot(np.nan, np.nan, np.nan, marker=">", color=color, label=label)
        ax.legend(loc="upper left")
    #: Return the axis
    if ax_exist is not None:
        return ax
    else:
        return fig, ax


def get_plot_line_3d(ax: Axes, v: NPArray[float], v_offset: NPArray[float], x_bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]], color: str = color_palette[0], alpha: float = 1.) -> Axes:
    # TODO: Merge this with the plane plot
    #: Get the list of intersection points
    intersection_list = get_intersection_bounding_box_3d(v, None, v_offset, x_bounds)
    ##: Compute the hexadecimal value to rgb
    color_rgba = [*mplcolors.to_rgb(color), alpha]
    #: Add the polygon
    ax.add_collection3d(Poly3DCollection([intersection_list], color=[color_rgba for _ in range(len(intersection_list))]))
    #: Return the results
    return ax


def get_plot_box_3d(ax: Axes, bounds_box: tuple[tuple[float, float], tuple[float, float], tuple[float, float]], color: str = color_palette[0], alpha: float = 1.) -> Axes:
    #: Set the dimension of the state-space
    n_x = 3
    #: Create a list
    list_planes = ['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax']
    #: Create a dictionary
    dict_planes = get_dict_planes(bounds_box)
    #: Loop over all the planes
    for name_plane in list_planes:
        #: Extract the planes data
        v_1_plane, v_2_plane, offset_plane = dict_planes[name_plane]
        #: Plot the plane
        ax = get_plot_plane_3d(ax, v_1_plane, v_2_plane, offset_plane, bounds_box, color, alpha)
    #: Return the results
    return ax

        
def get_axes_inputs_outputs_state_norm(T: NPArray[float], T_i: NPArray[float], X: NPArray[float], U: NPArray[float], Y: NPArray[float], X_hat: NPArray[float] | None = None, Kappa: NPArray[float] | None = None, vertical_bounds: tuple[tuple[float, float], ...] | None = None, ax_exist: Axes | None = None) -> tuple[Figure, tuple[Axes, Axes, Axes]]:
    
    # FROM: https://stackoverflow.com/questions/67236425/matplotlib-twiny-axis-does-not-have-the-padding-the-original-axis-has  # nopep8
    def lim(x, pad=5):
        xmin, xmax = min(x), max(x)
        margin = (xmax - xmin) * pad/100
        return xmin - margin, xmax + margin

    #: Add to existing axes (if they exist)
    if ax_exist is not None:
        #: Set equal
        fig, ax = None, ax_exist
    else:
        #: Check the number of plots
        if Kappa is not None:
            num_subplots = 4
        else:
            num_subplots = 3
        #: Create a figure
        fig, ax = plt.subplots(num_subplots, 1)
    #: Create plots
    # TODO: How do we distinguish between a CT system and a DT system?
    ax[0].plot(T, np.linalg.norm(X, axis=0), "--", color=color_palette[0], label=r"$\Vert \boldsymbol{\chi}(t) \Vert$")  # Plot the norm of the state
    #: Extend the sampling instant to the last simulation time
    if T[-1] != T_i[-1]:
        #: Add the last sampled state
        T_i = np.append(T_i, T[-1])
        U = np.hstack((U, U[:, -1][:, np.newaxis]))
        Y = np.hstack((Y, Y[:, -1][:, np.newaxis]))
    if X_hat is not None:
        ax[0].plot(T_i, np.linalg.norm(X_hat, axis=0), color=color_palette[0], drawstyle="steps-post", label=r"$\Vert \hat{\boldsymbol{x}}[k] \Vert$")  # Plot the norm of the estimated state (at transmission/event instants)
    for elem in range(U.shape[0]):
        if U.shape[0] == 1:  # Scalar input
            ax[1].plot(T_i, np.squeeze(U[elem, :]), color=color_palette[1], drawstyle="steps-post", label=r"$u_{i}$")  # Plot the input
        else:  # Vector-values input
            ax[1].plot(T_i, np.squeeze(U[elem, :]), color=color_palette[1], drawstyle="steps-post", label=fr"$u_{{{elem + 1},i}}$")  # Plot the input
    #: Retrieve the dimensionality of the output
    n_y = Y.shape[0]
    for elem in range(n_y):
        if n_y == 1:  # Scalar output
            ax[2].plot(T_i, np.squeeze(Y[elem, :]), color=color_palette[2], drawstyle="steps-post", label=r"$y_{i}$")  # Plot the output
        else:  # Vector-values output
            #: Construct the color
            rgb, a = get_rgb_from_hex(color_palette[2], mode='float'), (1 - elem * (1 / n_y))
            rgba_elem = (*rgb, a)
            ax[2].plot(T_i, np.squeeze(Y[elem, :]), color=rgba_elem, drawstyle="steps-post", label=fr"$y_{{{elem + 1},i}}$")  # Plot the output
    #: Add inter-sample times
    if Kappa is not None:
        ax[3].stem(T_i, Kappa, linefmt=color_palette[3], markerfmt=color_palette[3], basefmt=color_palette[3], label=r"$\kappa_{i}$" )
    #: Add labels
    if Kappa is not None:
        idx_last = 3
    else:
        idx_last = 2
    ax[idx_last].set_xlabel(r"$t$")
    #: Remove tick labels
    for idx in range(idx_last):
        ax[idx].tick_params(labelbottom=False)
    #: Add secondary axis
    for idx in range(idx_last + 1):
        ax_top = ax[idx].twiny()
        ax[idx].callbacks.connect('xlim_changed', lambda l: ax_top.set_xlim(*lim(T_i)))
        ax[idx].set_xlim(*lim(T)) # trigger the xlim_changed callback
        ax_top.set_xticks(T_i)
        if idx == 0:
            ax_top.set_xticklabels(range(T_i.size))
            ax_top.set_xlabel(r"$i$")
        else:
            ax_top.tick_params(labeltop=False)
    #: Add legends
    ax[0].legend(loc='upper left')
    ax[1].legend(loc='upper left')
    ax[2].legend(loc='upper left')
    if Kappa is not None:
        ax[3].legend(loc='upper left')
    #: Add the bounds
    if vertical_bounds is not None:
        for idx, bound in enumerate(vertical_bounds):
            ax[idx].set_ylim(bound)
    #: Return the axis
    if ax_exist is not None:
        return ax
    else:
        return fig, ax
    

# ------------ SUPPORT FUNCTIONS ------------


def get_intersection_three_planes(v_1_plane_1: NPArray[float], v_2_plane_1: NPArray[float], offset_plane_1: NPArray[float], v_1_plane_2: NPArray[float], v_2_plane_2: NPArray[float], offset_plane_2: NPArray[float], v_1_plane_3: NPArray[float], v_2_plane_3: NPArray[float], offset_plane_3: NPArray[float]) -> NPArray | None:
    # FROM: ChatGPT3.5
    # TODO: Make an actual plane class for an equivalent representation
    #: Calculating normal vectors of the planes
    normal_plane_1 = np.cross(v_1_plane_1, v_2_plane_1)
    normal_plane_2 = np.cross(v_1_plane_2, v_2_plane_2)
    normal_plane_3 = np.cross(v_1_plane_3, v_2_plane_3)
    #: Adjusting D constants for the planes based on offsets
    D_plane_1 = -np.dot(normal_plane_1, offset_plane_1)
    D_plane_2 = -np.dot(normal_plane_2, offset_plane_2)
    D_plane_3 = -np.dot(normal_plane_3, offset_plane_3)
    #: Constructing coefficient matrix
    coeff_matrix = np.array([normal_plane_1, normal_plane_2, normal_plane_3])
    #: Constructing constant vector
    const_vector = np.array([D_plane_1, D_plane_2, D_plane_3])
    #: Solving the system of equations
    try:
        intersection_point = np.linalg.solve(coeff_matrix, const_vector)
    except np.linalg.LinAlgError:  # There is no intersection point
        intersection_point = None 
    #: Return the result
    return intersection_point


def get_intersection_line_plane(v_1_plane: NPArray[float], v_2_plane: NPArray[float], offset_plane: NPArray[float], line: NPArray[float], offset_line: NPArray[float]) -> NPArray | None:
    # FROM: ChatGPT3.5
    #: Define the plane by three points
    p_1_plane = offset_plane
    #: Calculate the normal vector of the plane
    normal_plane = np.cross(v_1_plane, v_2_plane)
    #: Define the line by a point and its direction
    point_line = offset_line
    direction_line = line
    #: Calculate the inner product
    dot_product = np.dot(normal_plane, direction_line)
    #: Check if there is an intersection point
    if dot_product == 0.:
        return None
    else:
        #: Calculate the parameter t for the intersection point
        t = np.dot(normal_plane, p_1_plane - point_line) / dot_product
    #: Calculate the intersection point
    intersection_point = point_line + t * direction_line
    #: Return the results
    return intersection_point


def get_intersection_bounding_box_3d(v_1: NPArray[float], v_2: NPArray[float] | None, v_offset: NPArray[float], x_bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]) -> list:    
    #: Set the dimension of the state-space
    n_x = 3
    #: Create a list
    list_planes = ['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax']
    #: Create the inequality plot
    F_ineq, b_ineq = np.vstack((np.eye(n_x), -np.eye(n_x))), np.array([x_bounds[0][1], x_bounds[1][1], x_bounds[2][1], -x_bounds[0][0], -x_bounds[1][0], -x_bounds[2][0]])
    #: Create a dictionary
    dict_planes = get_dict_planes(x_bounds)
    #: Calculate the intersection points
    if v_2 is not None:  # Intersection with a plane
        #: List all the pairs
        list_pairs = [(list_planes[p1], list_planes[p2]) for p1 in range(len(list_planes)) for p2 in range(p1+1, len(list_planes))]
        #: Create a list of intersection points
        intersection_list = []
        #: Loop over all elements in the list
        for pair in list_pairs:
            #: Extract the planes data
            v_1_plane_1, v_2_plane_1, offset_plane_1 = dict_planes[pair[0]]
            v_1_plane_2, v_2_plane_2, offset_plane_2 = dict_planes[pair[1]]
            #: Find the intersection
            points_intersection = get_intersection_three_planes(v_1_plane_1, v_2_plane_1, offset_plane_1, v_1_plane_2, v_2_plane_2, offset_plane_2, v_1, v_2, v_offset)
            #: FIXME: For some reason there is an imaginary part?
            points_intersection = points_intersection.real if points_intersection is not None else None
            #: Check if the element is within the plotting area
            if points_intersection is not None and np.all(F_ineq @ points_intersection <= 1.1 * b_ineq):
                #: Add the vertex to the collection
                intersection_list.append(points_intersection)
    else:  # Intersection with a line
        #: Create a list of intersection points
        intersection_list = []
        #: Loop over all elements in the list
        for plane in list_planes:
            #: Extract the plane data
            v_1_plane, v_2_plane, offset_plane = dict_planes[plane]
            #: Find the intersection
            points_intersection = get_intersection_line_plane(v_1_plane, v_2_plane, offset_plane, v_1, np.zeros(n_x))
            #: Check if the element is within the plotting area
            if points_intersection is not None and np.all(F_ineq @ points_intersection <= b_ineq):
                #: Add the vertex to the collection
                intersection_list.append(points_intersection)
    #: Return the result
    return intersection_list


def get_sorted_list_of_vertices(intersection_list: list, normal: NPArray[float]) -> list:
    #: Loop over all indices
    for idx in range(len(intersection_list) - 1):
        #: Compute the angle between the current vertex
        angle_to_current = np.array([utils.get_signed_angle(intersection_list[idx], vert, look=normal).real for vert in intersection_list])
        #: Create the mask
        mask = np.zeros(len(intersection_list))
        mask[idx] = 1
        mask[angle_to_current < 0] = 1
        #: Compute the smallest index
        smallest_index = np.argmin(np.ma.array(angle_to_current, mask=mask))
        #: Reorder the list
        intersection_list[idx + 1], intersection_list[smallest_index] = intersection_list[smallest_index], intersection_list[idx + 1]
    #: Return the results
    return intersection_list


def get_dict_planes(box_bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]) -> dict:
    #: Create the direction vectors
    xmin_1, xmin_2 = np.array([0, 1, 0]), np.array([0, 0, 1]) 
    xmax_1, xmax_2 = np.array([0, 1, 0]), np.array([0, 0, 1]) 
    ymin_1, ymin_2 = np.array([1, 0, 0]), np.array([0, 0, 1]) 
    ymax_1, ymax_2 = np.array([1, 0, 0]), np.array([0, 0, 1]) 
    zmin_1, zmin_2 = np.array([1, 0, 0]), np.array([0, 1, 0]) 
    zmax_1, zmax_2 = np.array([1, 0, 0]), np.array([0, 1, 0]) 
    #: Create the offset vectors
    xmin_offset = np.array([box_bounds[0][0], 0, 0])
    xmax_offset = np.array([box_bounds[0][1], 0, 0])
    ymin_offset = np.array([0, box_bounds[1][0], 0])
    ymax_offset = np.array([0, box_bounds[1][1], 0])
    zmin_offset = np.array([0, 0, box_bounds[2][0]])
    zmax_offset = np.array([0, 0, box_bounds[2][1]])
    #: Create the dictionary
    dict_planes = {'xmin': (xmin_1, xmin_2, xmin_offset), 'xmax': (xmax_1, xmax_2, xmax_offset), 'ymin': (ymin_1, ymin_2, ymin_offset), 'ymax': (ymax_1, ymax_2, ymax_offset), 'zmin': (zmin_1, zmin_2, zmin_offset), 'zmax': (zmax_1, zmax_2, zmax_offset)}
    #: return the results
    return dict_planes


def get_rgb_from_hex(hex: str, mode: str = 'int') -> tuple[float, float, float]:
    # FROM: "https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python"  # nopep8
    #: Strip the '#' symbols
    hex = hex.lstrip('#')
    #: Convert to RGB
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    if mode == 'float':
        rgb = (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
    #: Return the result
    return rgb
