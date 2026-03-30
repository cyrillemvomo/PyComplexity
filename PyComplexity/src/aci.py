import numpy as np
import plotly.graph_objects as go


def lds_calc(state, ws, fs, period, min_val= 4, plotje=0):
    """
    MATLAB-faithful LDS calculation (Rosenstein 1993),
    with Plotly interactive plotting.
    """

    ws_samp = int(np.round(ws * fs))
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
        difference[i_t, :] = np.nan  # explicit self-exclusion

        dist_sum = np.sum(difference, axis=1)
        index = int(np.nanargmin(dist_sum))

        diff_vec = state_ext[i_t:i_t + ws_samp, :] - state_ext[index:index + ws_samp, :]
        divergence_mat[i_t, :] = np.sqrt(np.sum(diff_vec ** 2, axis=1))

    divergence = np.nanmean(np.log(divergence_mat), axis=0)

    # ---- linear fits (identical to MATLAB) ----

    if ws_samp > min_val * period * fs:
        L2 = int(np.round(min_val * period * fs))
        t_long = np.arange(L2 + 1, ws_samp + 1) / fs
        Pl = np.polyfit(t_long, divergence[L2:], 1)
    else:
        L2 = None
        Pl = np.array([np.nan, np.nan])

    aci = Pl[0]

    # ---- Plotly plot ----
    if plotje == 1:
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
            title="Divergence curve (Local Dynamic Stability)",
            xaxis_title="Stride Number",
            yaxis_title="Ln(divergence)",
            template="simple_white",
            hovermode="x unified"
        )

        fig.show()

    return aci
