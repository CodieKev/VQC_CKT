from qiskit.aqua.components.feature_maps import FeatureMap
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import BlueprintCircuit
import numpy as np
import matplotlib.pyplot as plt
import functools

from qiskit import BasicAer
from qiskit.circuit.library import ZFeatureMap,ZZFeatureMap, PauliFeatureMap
from qiskit.aqua import QuantumInstance
from qiskit.aqua.components.feature_maps import self_product
from qiskit.aqua.algorithms import QSVM
from qiskit.ml.datasets import ad_hoc_data
from numpy import pi
class CustomFeatureMap(FeatureMap):
    """Mapping data with a custom feature map."""
    
    def __init__(self, feature_dimension, depth=2, entangler_map=None):
        """
        Args:
            feature_dimension (int): number of features
            depth (int): the number of repeated circuits
            entangler_map (list[list]): describe the connectivity of qubits, each list describes
                                        [source, target], or None for full entanglement.
                                        Note that the order is the list is the order of
                                        applying the two-qubit gate.        
        """
        self._support_parameterized_circuit = False
        self._feature_dimension = feature_dimension
        self._num_qubits = self._feature_dimension = feature_dimension+2
        self._depth = depth
        self._entangler_map = None
        if self._entangler_map is None:
            self._entangler_map = [[i, j] for i in range(self._feature_dimension) for j in range(i + 1, self._feature_dimension)]
            
    def construct_circuit(self, x, qr, inverse=False):
        """Construct the feature map circuit.
        
        Args:
            x (numpy.ndarray): 1-D to-be-transformed data.
            qr (QauntumRegister): the QuantumRegister object for the circuit.
            inverse (bool): whether or not to invert the circuit.
            
        Returns:
            QuantumCircuit: a quantum circuit transforming data x.
        """
        qc = QuantumCircuit(5)

        
        for _ in range(self._depth):
            y = -1.3*x[0]+x[1]
            z = (0.130554 + 0.087421 *(x[0]**2) + 0.193981* (x[1]**2) + x[0] *(0.14809 - 0.248248 *x[1] - 0.0651 *x[2]) +x[1]*(-0.140875 - 0.0429*x[2]) - 0.319747*x[2] + 0.270152 *(x[2]**2))*13
            qc.h(0)
            qc.h(1)
            qc.h(2)
            qc.h(3)
            qc.u1(x[0],0)
            qc.u1(x[1],1)
            qc.u1(x[2],2)
            qc.u1(y,3)
            qc.u1(z,3)
            qc.cx(0,1)
            qc.u1((2*(pi-x[0])*(pi-x[1])),1)
            qc.cx(0,1)
            qc.cx(0,2)
            qc.u1((2*(pi-x[0])*(pi-x[2])),2)
            qc.cx(0,2)
            qc.cx(0,3)
            qc.u1((2*(pi-x[0])*(pi-y)),3)
            qc.cx(0,3)
            qc.cx(1,2)
            qc.u1((2*(pi-x[1])*(pi-x[2])),2)
            qc.cx(1,2)
            qc.cx(1,3)
            qc.u1((2*(pi-x[1])*(pi-y)),3)
            qc.cx(1,3)
            qc.cx(2,3)
            qc.u1((2*(pi-x[2])*(pi-y)),3)
            qc.cx(2,3)
            qc.cx(0,4)
            qc.u1((2*(pi-x[0])*(pi-z)),4)
            qc.cx(0,4)
            qc.cx(1,4)
            qc.u1((2*(pi-x[1])*(pi-z)),4)
            qc.cx(1,4)
            qc.cx(2,4)
            qc.u1((2*(pi-x[2])*(pi-z)),4)
            qc.cx(2,4)
            qc.cx(3,4)
            qc.u1((2*(pi-y)*(pi-z)),4)
            qc.cx(3,4)
            
            
            
            
        if inverse:
            qc.inverse()
        return qc
def feature_map():
    return CustomFeatureMap(feature_dimension=3, depth=2)
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
    var_circuit = EfficientSU2(num_qubits=5, su2_gates= ['rx', 'ry'], entanglement='circular', reps=3)
    
    # BUILD VARIATIONAL CIRCUIT HERE - END
    """
    # return the variational circuit which is either a VaritionalForm or QuantumCircuit object
    from qiskit.circuit import QuantumCircuit, ParameterVector

    num_qubits = 4            
    reps = 2              # number of times you'd want to repeat the circuit
    reps_2 = 2

    x = ParameterVector('x', length=reps*(5*num_qubits-1))  # creating a list of Parameters
    qc = QuantumCircuit(num_qubits)

    # defining our parametric form
    for k in range(reps):
            for i in range(num_qubits):
                qc.rx(x[2*i+k*(5*num_qubits-1)],i)
                qc.ry(x[2*i+1+k*(5*num_qubits-1)],i)
            for i in range(num_qubits-1):
                qc.cx(i,i+1)
            for i in range(num_qubits-1):
                qc.rz(2.356194490192345, i)
                qc.rx(1.5707963267948966, i)
                qc.rz(-2.356194490192345, i+1)
                qc.rx(1.5707963267948966, i+1)
                qc.cz(i, i+1)
                qc.rz(-1.5707963267948966, i)
                qc.rx(1.5707963267948966, i)
                qc.rz(x[i+2*(num_qubits)+k*(5*num_qubits-1)], i)
                qc.rx(-1.5707963267948966, i)
                qc.rz(1.5707963267948966, i+1)
                qc.rx(1.5707963267948966, i+1)
                qc.rz(x[i+2*(num_qubits)+k*(5*num_qubits-1)], i+1)
                qc.rx(-1.5707963267948966, i+1)
                qc.cz(i, i+1)
                qc.rz(-1.5707963267948966, i)
                qc.rx(1.5707963267948966, i)
                qc.rz(0.7853981633974483, i)
                qc.rz(-1.5707963267948966, i+1)
                qc.rx(-1.5707963267948966, i+1)
                qc.rz(2.356194490192345, i+1)
            for i in range(num_qubits):
                qc.rx(x[2*i+3*num_qubits-1+k*(5*num_qubits-1)],i)
                qc.ry(x[2*i+1+3*num_qubits-1+k*(5*num_qubits-1)],i)
        
            
    """
                
            
    #custom_circ.draw()
    return var_circuit
# # the write_and_run function writes the content in this cell into the file "optimal_params.py"

### WRITE YOUR CODE BETWEEN THESE LINES - START
    
# import libraries that are used in the function below.
import numpy as np
    
### WRITE YOUR CODE BETWEEN THESE LINES - END

def return_optimal_params():
    # STORE THE OPTIMAL PARAMETERS AS AN ARRAY IN THE VARIABLE optimal_parameters 
    
    optimal_parameters =[ 0.91854302, -1.08798177, -0.21009535, -0.58232799,  1.06935428,
       -0.04641256,  0.59552509,  3.54519991, -1.28918848,  2.28766243,
       -1.84491546,  0.90895254,  2.2535594 , -0.41148327,  1.6737878 ,
        0.34052944,  0.92970678,  0.20448063, -2.72046037, -1.60088967,
       -1.50488751, -1.68597962,  1.55208916,  0.9146031 , -1.05649925,
        0.75403961,  0.33066391,  0.09772049,  0.5280793 ,  0.62611578,
        0.1055327 , -0.0188807 ,  0.36066003,  0.96266194,  0.79398824,
        2.0723008 ,  0.10734654,  0.00983166,  0.38139291, -0.22015975]
    
    # STORE THE OPTIMAL PARAMETERS AS AN ARRAY IN THE VARIABLE optimal_parameters 
    return np.array(optimal_parameters)
