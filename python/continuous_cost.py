import control
import scipy.linalg as la
import numpy as np


def ContinuousCost(A, B, Q, R, x0, T):
    """
    Continuous-time optimal LQR cost via simulation.
    """
    N = 10000
    dt = T / N
    t = np.linspace(0, T, N+1)

    # Continuous LQR
    K, P, _ = control.lqr(A, B, Q, R)
    K = np.asarray(K)

    # Closed-loop system
    sys_cl = control.ss(A - B @ K, B*0, np.eye(A.shape[0]), 0)

    # Simulate
    _, x = control.initial_response(sys_cl, T=t, X0=x0.flatten())
    x = np.asarray(x)

    # Continuous cost
    J = 0.0
    for k in range(N):
        xk = x[:, k:k+1]
        uk = -K @ xk
        J += (xk.T @ Q @ xk + uk.T @ R @ uk).item() * dt

    # Terminal cost (continuous Riccati solution)
    xT = x[:, -1:]
    J += (xT.T @ P @ xT).item()

    return J