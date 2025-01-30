import numpy as np

def initialize_state(initial_states):
   
    state = np.array([1, 0], dtype=complex) if initial_states[0] == 0 else np.array([0, 1], dtype=complex)
    for i in range(1, len(initial_states)):
        next_qubit = np.array([1, 0], dtype=complex) if initial_states[i] == 0 else np.array([0, 1], dtype=complex)
        state = np.kron(state, next_qubit)
    
    return state

def measure_state(state):
    
    num_qubits = int(np.log2(len(state))) 
    probabilities = np.abs(state) ** 2  

    measurement_result = [format(i, f'0{num_qubits}b') for i in range(2 ** num_qubits)]
    
    return measurement_result, probabilities
