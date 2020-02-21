import numpy as np
from numba import njit, vectorize
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from IPython.display import HTML


@vectorize(['float64(float64, float64, float64)'])
def time_step(ele, dt, temp_lim):
    if ele >= temp_lim:
        return dt
    else:
        return 0


@vectorize(['float64(float64, float64, float64)'])
def keep_burning(time, temp, temp_lim):
    if 0 < time < 10800:
        return temp_lim # return max(temp, temp_lim)
    else:
        return temp


@njit(parallel=True)
def main_loop(total, step, T, W, K, N, dt, h, temp_lim):
    partials = []
    partials.append(T)

    T_new = T.copy()
    Times = np.zeros_like(T)
    Times = time_step(T, dt, temp_lim)

    for i in range(total):
        T_new[1:-1, 1:-1] = T[1:-1, 1:-1]*(1 - 16*N[1:-1, 1:-1]*K[1:-1, 1:-1]) \
            + T[1:-1, 2:]*(N[1:-1, 1:-1]*(K[1:-1, 2:] - K[1:-1, :-2] + 4*K[1:-1, 1:-1]) + W[0]*dt/(2*h)) \
            + T[2:, 1:-1]*(N[1:-1, 1:-1]*(K[2:, 1:-1] - K[:-2, 1:-1] + 4*K[1:-1, 1:-1]) + W[1]*dt/(2*h)) \
            + T[1:-1, :-2]*(N[1:-1, 1:-1]*(-K[1:-1, 2:] + K[1:-1, :-2] + 4*K[1:-1, 1:-1]) + W[0]*dt/(2*h)) \
            + T[:-2, 1:-1]*(N[1:-1, 1:-1]*(-K[2:, 1:-1] + K[:-2, 1:-1] + 4*K[1:-1, 1:-1]) + W[1]*dt/(2*h))

        #
        Times = Times + time_step(T_new, dt, temp_lim)
        T_new = keep_burning(Times, T_new, temp_lim)

        # Boundary conditions
        T, T_new = update_bounries(T, T_new, K, N)

        if i % step == 0:
            partials.append(T.copy())
            print(i*100/total)

    partials.append(T.copy())
    return partials, T


@njit
def update_bounries(T, T_new, K, n):
    # Neumann oundary conditions
    # Left
    T_new[1:-1, 0] = T[1:-1, 0]*(1 - 16*n[1:-1, 0]*K[1:-1, 0]) \
        + 2*n[1:-1, 0]*T[1:-1, 1]* (4*K[1:-1, 0]) \
        + n[1:-1, 0]*T[2:, 0]* (4*K[1:-1, 0]) \
        + n[1:-1, 0]*T[:-2, 0]*(4*K[1:-1, 0])

    # Top
    T_new[0, 1:-1] = T[0, 1:-1]*(1 - 16*n[0, 1:-1]*K[0, 1:-1]) \
        + n[0, 1:-1]*T[0, 2:]* (4*K[0, 1:-1]) \
        + 2*n[0, 1:-1]*T[1, 1:-1]* (4*K[0, 1:-1]) \
        + n[0, 1:-1]*T[0, :-2]*(4*K[0, 1:-1])

    # Right
    T_new[1:-1, -1] = T[1:-1, -1]*(1 - 16*n[1:-1, -1]*K[1:-1, -1]) \
        + n[1:-1, -1]*T[2:, -1]* (4*K[1:-1, -1]) \
        + 2*n[1:-1, -1]*T[1:-1, -2]*(4*K[1:-1, -2]) \
        + n[1:-1, -1]*T[:-2, -1]*(4*K[1:-1, -1])

    # Bottom
    T_new[-1, 1:-1] = T[-1, 1:-1]*(1 - 16*n[-1, 1:-1]*K[-1, 1:-1]) \
        + n[-1, 1:-1]*T[-1, 2:]* (4*K[-1, 1:-1]) \
        + n[-1, 1:-1]*T[-1, :-2]*(4*K[-1, 1:-1]) \
        + 2*n[-1, 1:-1]*T[-2, 1:-1]*(4*K[-2, 1:-1])

    T = T_new.copy()

    return T, T_new


class Solver:
    def __init__(self, T, Rho, Cp, K, W, h, total_time, img_at):
        # Model input
        self.T = T
        self.Rho = Rho
        self.Cp = Cp
        self.K = K
        self.W = W

        # General config
        self.h = h
        self.img_at = img_at
        self.total_time = total_time

        # Delta de tiempo [s]
        k_max = self.K.max()
        r_min = self.Rho.min()
        cp_min = self.Cp.min()
        self.dt = min(1, (r_min*cp_min*self.h**2)/(4*k_max))

        # Grid points
        self.nx = self.T.shape[0]
        self.ny = self.T.shape[1]

        self.partials = []

    def solve(self):
        N = self.dt/(4*self.Rho*self.Cp*self.h**2)

        total = int(self.total_time/self.dt)
        step = int(self.img_at*total/100)

        temp_lim = 1873.15 # 1600°C

        self.partials, self.T = main_loop(total, step, self.T, self.W, self.K,
                                          N, self.dt, self.h, temp_lim)


    def plot(self, colors=['#00008f', '#009fff', '#8fff6f', '#ff6f00', '#7f0000'], n_bins=100):
        fig_index = 0
        temp_min = min([p.min() for p in self.partials])
        temp_max = max([p.max() for p in self.partials])

        # Create the colormap
        cm = LinearSegmentedColormap.from_list('custom_bar', colors, N=n_bins)

        fig, ax = plt.subplots(figsize=(8, 6))
        im = plt.imshow(self.partials[0], vmin=temp_min, vmax=temp_max, interpolation='nearest', cmap=cm)

        # Set axis and ref
        x_labels = [f'{i:.3f}' for i in np.linspace(0, self.T.shape[0]*self.h, num=10)]
        y_labels = [f'{i:.3f}' for i in np.linspace(0, self.T.shape[1]*self.h, num=10)]
        plt.xticks(np.linspace(0, self.nx, num=10), x_labels, rotation=45)
        plt.yticks(np.linspace(0, self.ny, num=10), y_labels)
        plt.colorbar()

        def updatefig(frame):
            total = int(self.total_time/self.dt)
            step = int(self.img_at*total/100)

            im.set_array(self.partials[frame + 1])
            ax.set_title(f'Time: {self.dt * step * frame:.2g} seg')
            return im,

        anim = animation.FuncAnimation(fig, updatefig, frames=len(self.partials) - 1, blit=True)
        return HTML(anim.to_jshtml())
