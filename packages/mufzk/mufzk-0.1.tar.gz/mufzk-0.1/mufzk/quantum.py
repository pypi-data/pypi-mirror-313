import numpy as np
from scipy.linalg import qr


# randomly create a NxN-dimensional unitary operator
def random_unitary(num_qubits=1, dtype="float"):
    assert num_qubits >= 1, f"num_qubits should be greater than or equal to 1."
    if dtype == "float":
        N = int(2 ** num_qubits)
        H = np.random.randn(N, N)
        Q, R = qr(H)
    elif dtype == "complex":
        N = int(2 ** num_qubits)
        H_real = np.random.randn(N, N)
        H_imag = np.random.randn(N, N)
        Q, R = qr(H_real + 1j*H_imag)
    else:
        raise AttributeError(f"dtype should be either 'float' or 'complex', not {dtype}")
    return Q


# randomly create a N-dimensional quantum state
def random_state(num_qubits=1, dtype="float"):
    assert num_qubits >= 1, f"num_qubits should be greater than or equal to 1."
    if dtype == "float":
        angle = 2 * np.pi * np.random.random()
        state = np.array([np.cos(angle), np.sin(angle)])
        if num_qubits == 1:
            return state
        else:
            for _ in range(num_qubits - 1):
                angle = 2 * np.pi * np.random.random()
                state = np.kron(state, np.array([np.cos(angle), np.sin(angle)]))
            return state
    elif dtype == "complex":
        return random_state(num_qubits) + 1j * random_state(num_qubits)
    else:
        raise AttributeError(f"dtype should be either 'float' or 'complex', not {dtype}")


# finding the angle of a 2-dimensional quantum state
def find_angle(state):
    assert len(state) == 2, "Angle value can be calculated only for a single qubit state."
    x, y = state[0], state[1]
    angle_radian = np.acos(x)  # radian of the angle with state |0>
    angle_degree = 360 * angle_radian / (2 * np.pi)  # degree of the angle with state |0>
    # if the second amplitude is negative,
    #     then angle is (-angle_degree)
    #     or equivalently 360 + (-angle_degree)
    if y < 0:
        angle_degree = 360 - angle_degree  # degree of the angle
    # else degree of the angle is the same as degree of the angle with state |0>
    return angle_degree
