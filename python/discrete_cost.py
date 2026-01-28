import control
import scipy.linalg as la
import numpy as np

def DiscreteCost(A, B, Q, R, x0, T, N):
    """
    Discrete-time optimal LQR cost with ZOH-consistent cost.
    """

    tau = T / N

    # Discretize dynamics
    sysd = control.c2d(control.ss(A, B, np.eye(A.shape[0]), 0), tau)
    Phi = np.asarray(sysd.A)
    Gamma = np.asarray(sysd.B)

    n, m = B.shape

    # Compute cost matrices
    Qbar = np.zeros((n, n))
    Pbar = np.zeros((n, m))
    Rbar = np.zeros((m, m))

    t_int = np.linspace(0, tau, 200)
    dt = t_int[1] - t_int[0]

    for ti in t_int:
        expAt = la.expm(A * ti)
        Qbar += expAt.T @ Q @ expAt * dt
        Pbar += expAt.T @ Q @ Gamma * dt
        Rbar += Gamma.T @ Q @ Gamma * dt

    Rbar += tau * R

    # Discrete LQR
    Kd, Sd, _ = control.dlqr(Phi, Gamma, Qbar, Rbar)
    Kd = np.asarray(Kd)

    # Simulate
    x = np.zeros((n, N+1))
    u = np.zeros((m, N))
    x[:, 0:1] = x0

    for k in range(N):
        u[:, k:k+1] = -Kd @ x[:, k:k+1]
        x[:, k+1:k+2] = Phi @ x[:, k:k+1] + Gamma @ u[:, k:k+1]

    # Discrete cost
    J = 0.0
    for k in range(N):
        xk = x[:, k:k+1]
        uk = u[:, k:k+1]
        J += (
            xk.T @ Qbar @ xk
            + uk.T @ Rbar @ uk
            + 2 * xk.T @ Pbar @ uk
        ).item()

    xT = x[:, -1:]
    J += (xT.T @ Sd @ xT).item()

    return J