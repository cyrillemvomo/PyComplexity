# Version
__author__ = 'Cyrille E. Mvomo, https://github.com/cyrillemvomo/PyComplexity'
__version__ = "0.1.0"
__license__ = "MIT"

# Importations 
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import make_interp_spline

# Required function
def makestatelocal(signal, hc, n_dim=5, delay=10):
    """Get Delay-embedded state space.

    Parameters
    ----------
    signal : array_like, shape (T,) (acceleration magnitude recommended, see references at https://github.com/cyrillemvomo/PyComplexity)
        1D signal.
    hc : array_like, shape (n_strides,)
        Heel strike indices (samples).
    n_dim : int, default=5 (use GFNN to determine based on your data, see https://github.com/cyrillemvomo/PyComplexity)
        Embedding dimension.
    delay : int, default=10 (use AMI to determine based on your data, see https://github.com/cyrillemvomo/PyComplexity)
        Delay in samples.

    Returns
    -------
    state : ndarray, shape ( (n_strides-1)*100 - delay*(n_dim-1), n_dim )
        Delay-embedded state space.
    """

    signal = np.asarray(signal, dtype=np.float64).reshape(-1)
    hc = np.asarray(hc, dtype=np.int64).reshape(-1)

    # bounds check
    if hc.min() < 0 or hc.max() >= signal.size:
        raise ValueError(
            f"hc indices out of bounds after conversion. "
            f"min={hc.min()}, max={hc.max()}, len(signal)={signal.size}. "
        )

    n_strides = int(hc.size)
    n_samples = int((n_strides - 1) * 100)

    start = int(hc[0])
    stop_inclusive = int(hc[-1])
    signal_new = signal[start:stop_inclusive + 1]

    t_new = np.arange(1, signal_new.size + 1, dtype=np.float64)

    t_interp = (np.arange(1, n_samples + 1, dtype=np.float64) / n_samples) * t_new[-1]

    spline = make_interp_spline(t_new, signal_new, k=3) 
    signal_interp = spline(t_interp).astype(np.float64)

    # state space
    out_len = n_samples - delay * (n_dim - 1)
    if out_len <= 0:
        raise ValueError(
            f"Requested embedding is too long: out_len={out_len}. "
            f"Reduce n_dim and/or delay."
        )

    state = np.empty((out_len, n_dim), dtype=np.float64)

    for i_dim in range(n_dim):
        start_idx = i_dim * delay
        end_cut = (n_dim - 1 - i_dim) * delay
        col = signal_interp[start_idx:] if end_cut == 0 else signal_interp[start_idx:-end_cut]
        state[:, i_dim] = col

    return state



# Main function
def compute_aci(signal, hc, n_dim=5, delay=10, ws=12, fs=100, period=1, min_val= 5, plot=False):
    """Get ACI (plot divergence curves optional).

    Parameters
    ----------
    signal : array_like, shape (T,) (acceleration magnitude recommended, see references at https://github.com/cyrillemvomo/PyComplexity)
        1D signal used to get delay-embedded state space.
    hc : array_like, shape (n_strides,)
        Heel strike indices (samples) used to get delay-embedded state space. (recommended ~70 steady state consecutive strides minimum, see references at https://github.com/cyrillemvomo/PyComplexity)
    n_dim : int, default=5 (use GFNN to determine based on your data, see https://github.com/cyrillemvomo/PyComplexity)
        Embedding dimension used to get delay-embedded state space.
    delay : int, default=10 (use AMI to determine based on your data, see https://github.com/cyrillemvomo/PyComplexity)
        Delay in samples used to get delay-embedded state space.
    ws : int, default=12
        Upper bound of the window size to track the divergence (gait cycles) (recommended ~5-12 see references at https://github.com/cyrillemvomo/PyComplexity)
    fs : int, default=10 
        Sample frequency of the resampled data (100 frames per stride to control for differences in gait speed in case of comparisons)
    period : int, default=1 
        Period of the resampled signal is 1 (i.e. 1 stride every 100 samples)
    min_val : int, default=5 
        Lower bound of the window size to track the divergence (gait cycles) (recommended ~5-12 see references at https://github.com/cyrillemvomo/PyComplexity)
    plot : bool, default=False
        Divergence curve with ACI fit.

    Returns
    -------
    aci : float
        ACI value found.

    Example
    --------
    >>> # ACI computation and plot divergence curve fit: 
    >>> from PyComplexity import compute_aci
    >>> compute_aci(acc_magnitude, hc_frames, n_dim=5, delay=10, ws=12, fs=100, period=1, min_val= 5, plot=True)
    """


    # avoid common errors
    if hc.size < 2:
        raise ValueError("hc must contain at least 2 heel strikes.")
    if n_dim < 1:
        raise ValueError("n_dim must be >= 1")
    if delay < 0:
        raise ValueError("delay must be >= 0")
    if (ws > min_val) and (ws < len(hc)+5):
        raise ValueError("Make sure that (ws > min_val) and (ws < ~len(hc)+10)")
    

    # get divergence
    ws_samp = int(np.round(ws * fs))

    state = makestatelocal(signal, hc, n_dim, delay)
    m, n = state.shape

    state_ext = np.vstack([state, np.full((ws_samp, n), np.nan)])
    divergence_mat = np.full((m, ws_samp), np.nan)
    difference = np.full((m + ws_samp, n), np.nan)

    for i_t in range(m):
        for i_d in range(n):
            difference[:, i_d] = (state_ext[:, i_d] - state_ext[i_t, i_d]) ** 2

        start_index = int(np.round(max(0, i_t - np.round(0.5 * period * fs))))
        stop_index = int(np.round(min(m - 1, i_t + np.round(0.5 * period * fs))))
        difference[start_index:stop_index + 1, :] = np.nan
        difference[i_t, :] = np.nan  

        dist_sum = np.sum(difference, axis=1)
        index = int(np.nanargmin(dist_sum))

        diff_vec = state_ext[i_t:i_t + ws_samp, :] - state_ext[index:index + ws_samp, :]
        divergence_mat[i_t, :] = np.sqrt(np.sum(diff_vec ** 2, axis=1))

    divergence = np.nanmean(np.log(divergence_mat), axis=0)

    # linear fits 

    if ws_samp > min_val * period * fs:
        L2 = int(np.round(min_val * period * fs))
        t_long = np.arange(L2 + 1, ws_samp + 1) / fs
        Pl = np.polyfit(t_long, divergence[L2:], 1)
    else:
        L2 = None
        Pl = np.array([np.nan, np.nan])

    aci = Pl[0]

    # Plotly plot
    if plot:
        t_all = np.arange(1, ws_samp + 1) / fs

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=t_all,
            y=divergence,
            mode="lines",
            name="Divergence curve"
        ))

        if not np.isnan(Pl[0]):
            fig.add_trace(go.Scatter(
                x=t_long,
                y=np.polyval(Pl, t_long),
                mode="lines",
                name=f"Lambda L = {Pl[0]:.4f}"
            ))

        fig.update_layout(
            title="Divergence curve",
            xaxis_title="Stride Number",
            yaxis_title="Ln(divergence)",
            template="simple_white",
            hovermode="x unified"
        )

        fig.show()

    return aci
