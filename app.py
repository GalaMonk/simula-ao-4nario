import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.subplots as sp  
import numpy as np
from quantum_gates import apply_gate
from quantum_state import initialize_state, measure_state
from utils import calculate_bloch_vectors

initial_states = [0, 0, 0, 0]
quantum_state = initialize_state(initial_states)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Simulador de 4nario", style={"textAlign": "center"}),
    

    html.Div([
        html.Label("Estados Iniciais:"),
        dcc.Input(id="qubit-1", type="number", value=0, min=0, max=1),
        dcc.Input(id="qubit-2", type="number", value=0, min=0, max=1),
        dcc.Input(id="qubit-3", type="number", value=0, min=0, max=1),
        dcc.Input(id="qubit-4", type="number", value=0, min=0, max=1),
    ], style={"textAlign": "center", "marginBottom": 20}),
    
    html.Div([
        html.Label("Portas Quânticas:"),
        dcc.Dropdown(
            id="gate-dropdown",
            options=[
                {"label": "Hadamard (H)", "value": "H"},
                {"label": "Pauli-X (X)", "value": "X"},
                {"label": "Pauli-Y (Y)", "value": "Y"},
                {"label": "Pauli-Z (Z)", "value": "Z"},
                {"label": "CNOT", "value": "CNOT"}
            ],
            value="H"
        ),
        dcc.Input(id="target-qubit", type="number", placeholder="Qubit Alvo (1-4)", min=1, max=4),
        dcc.Input(id="control-qubit", type="number", placeholder="Qubit Controle", min=1, max=4),
        html.Button("Aplicar Porta", id="apply-gate-button", n_clicks=0),
    ], style={"textAlign": "center", "marginBottom": 20}),
    

    html.Div([
        dcc.Graph(id="bloch-spheres", style={"width": "50%", "display": "inline-block"}),
        dcc.Graph(id="probability-graph", style={"width": "50%", "display": "inline-block"})
    ])
])

@app.callback(
    [Output("bloch-spheres", "figure"), Output("probability-graph", "figure")],
    [Input("apply-gate-button", "n_clicks")],
    [
        State("qubit-1", "value"),
        State("qubit-2", "value"),
        State("qubit-3", "value"),
        State("qubit-4", "value"),
        State("gate-dropdown", "value"),
        State("target-qubit", "value"),
        State("control-qubit", "value")
    ]
)
def update_quantum_state(n_clicks, q1, q2, q3, q4, gate, target_qubit, control_qubit):
    global quantum_state
    
    initial_states = [int(q1), int(q2), int(q3), int(q4)]
    quantum_state = initialize_state(initial_states)
    
    if n_clicks > 0:
        target_qubit = int(target_qubit) - 1
        if gate == "CNOT":
            control_qubit = int(control_qubit) - 1
            quantum_state = apply_gate(quantum_state, "CNOT", target_qubit, control_qubit=control_qubit)
        else:
            quantum_state = apply_gate(quantum_state, gate, target_qubit)
    

    bloch_vectors = calculate_bloch_vectors(quantum_state)
    measurement_result, probabilities = measure_state(quantum_state)
    
    fig_bloch = sp.make_subplots(rows=2, cols=2, specs=[[{'type': 'scene'}, {'type': 'scene'}],
                                                     [{'type': 'scene'}, {'type': 'scene'}]])
    for i, (x, y, z) in enumerate(bloch_vectors):
        row, col = divmod(i, 2)
        fig_bloch.add_trace(go.Scatter3d(
            x=[0, x], y=[0, y], z=[0, z],
            mode="lines+markers",
            name=f"Qubit {i+1}"
        ), row=row+1, col=col+1)
    fig_bloch.update_layout(title="Esferas de Bloch", scene_aspectmode="cube")

    states = [format(i, "04b") for i in range(len(probabilities))]
    fig_prob = go.Figure(data=[go.Bar(x=states, y=probabilities)])
    fig_prob.update_layout(title="Probabilidades de Medição", xaxis_title="Estados", yaxis_title="Probabilidade")
    
    return fig_bloch, fig_prob

if __name__ == "__main__":
    app.run_server(debug=True)
