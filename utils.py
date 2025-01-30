import numpy as np

def calculate_bloch_vectors(state):
    
    num_qubits = int(np.log2(len(state)))
    bloch_vectors = []
    
    for i in range(num_qubits):
        reduced_state = np.zeros((2, 2), dtype=complex)
        for j in range(2 ** num_qubits):
            binary = format(j, f'0{num_qubits}b')
            idx = int(binary[i])
            reduced_state[idx, idx] += np.abs(state[j]) ** 2
        x = np.real(reduced_state[0, 1] + reduced_state[1, 0])
        y = np.imag(reduced_state[0, 1] - reduced_state[1, 0])
        z = np.real(reduced_state[0, 0] - reduced_state[1, 1])
        bloch_vectors.append((x, y, z))
    
    return bloch_vectors

def calculate_probabilities(state):
    return np.abs(state) ** 2
