# the write_and_run function writes the content in this cell into the file "variational_circuit.py"

### WRITE YOUR CODE BETWEEN THESE LINES - START
    
# import libraries that are used in the function below.
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.circuit.library import  RealAmplitudes, EfficientSU2
    
### WRITE YOUR CODE BETWEEN THESE LINES - END
import math

def nCr(n,r):
    f = math.factorial
    return int(f(n) / f(r) / f(n-r))

def variational_circuit():
    # BUILD VARIATIONAL CIRCUIT HERE - START
    
    # import required qiskit libraries if additional libraries are required
    
    # build the variational circuit
    #var_circuit = EfficientSU2(num_qubits=3, su2_gates= ['rx', 'ry'], entanglement='circular', reps=3)
    #var_circuit = EfficientSU2(num_qubits=4, su2_gates= ['rx', 'ry'], entanglement='circular', reps=3)
    
    # BUILD VARIATIONAL CIRCUIT HERE - END
    
    # return the variational circuit which is either a VaritionalForm or QuantumCircuit object
    from qiskit.circuit import QuantumCircuit, ParameterVector

    num_qubits = 3            
    reps = 1              # number of times you'd want to repeat the circuit

    x = ParameterVector('x', length=num_qubits)  # creating a list of Parameters
    custom_circ = QuantumCircuit(num_qubits)

    # defining our parametric form
    for _ in range(reps):
        for i in range(num_qubits):
            custom_circ.rx(x[i], i)
        for i in range(num_qubits):
            for j in range(i + 1, num_qubits):
                custom_circ.cx(i, j)
                custom_circ.u1(x[i] * x[j], j)
                custom_circ.cx(i, j)
            
            
    
                
            
    #custom_circ.draw()
    return custom_circ
