import numpy as np

def get_gate_matrix(gate_name):
    """
    Retorna a matriz correspondente à porta quântica especificada.
    """
    if gate_name == "H": 
        return (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
    elif gate_name == "X":  
        return np.array([[0, 1], [1, 0]], dtype=complex)
    elif gate_name == "Y":  
        return np.array([[0, -1j], [1j, 0]], dtype=complex)
    elif gate_name == "Z": 
        return np.array([[1, 0], [0, -1]], dtype=complex)
    elif gate_name == "CNOT": 
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 1],
                         [0, 0, 1, 0]], dtype=complex)
    else:
        raise ValueError(f"Porta quântica '{gate_name}' não reconhecida.")

def apply_gate(state, gate_name, target_qubit, control_qubit=None):
    
    num_qubits = int(np.log2(len(state))) 
    gate_matrix = get_gate_matrix(gate_name)

    if gate_name == "CNOT":
        if control_qubit is None:
            raise ValueError("A porta CNOT requer um qubit de controle.")

        identity = np.eye(2 ** num_qubits, dtype=complex)
        cnot_matrix = identity.copy()
        
    
        for i in range(2 ** num_qubits):
            binary = format(i, f'0{num_qubits}b')  
            if binary[control_qubit] == '1': 
                flipped = list(binary)
                flipped[target_qubit] = '1' if flipped[target_qubit] == '0' else '0'
                flipped_index = int("".join(flipped), 2)
                cnot_matrix[i, i], cnot_matrix[i, flipped_index] = 0, 1
                cnot_matrix[flipped_index, flipped_index], cnot_matrix[flipped_index, i] = 0, 1
        
        return cnot_matrix @ state

    else:

        full_gate = 1
        for i in range(num_qubits):
            if i == target_qubit:
                full_gate = np.kron(full_gate, gate_matrix) 
            else:
                full_gate = np.kron(full_gate, np.eye(2)) 
        
        return full_gate @ state
