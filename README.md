# Exploring  Basic Concepts of Quantum Computing using Python projectq

- Classical computers are just dealing with simple states of 0 and 1. 
- **Quantum computers** on the other hand are working on **qubits** in quantum states and not simple 0s and 1s. 
-  In quantum computing, a qubit or quantum bit is the basic unit of quantum information.
- The quantum state might be an electron in **superposition** between 1 and 0 .This makes it too fragile to be sent anywhere.A crude example of is the state when a coin is tossed up.While up in air it has equal probability of being heads or tails.
- Usually denoted as  ![{\displaystyle |0\rangle ={\bigl [}{\begin{smallmatrix}1\\0\end{smallmatrix}}{\bigr ]}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/279f5336e8dcc639125e7dda2410319b81c9bf94) and ![{\displaystyle |1\rangle ={\bigl [}{\begin{smallmatrix}0\\1\end{smallmatrix}}{\bigr ]}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/e788c1d112bf1312c0a7d6416782b66eecb0788b)   pronounced "ket 0" and "ket 1" .
- Additionally, the[ no-cloning-theorem](https://en.wikipedia.org/wiki/No-cloning_theorem) states that it is impossible to create an identical copy of an unknown quantum state because the **quantum state is collapsed when measured**, and thus the quantum state is destroyed.
-  There are two possible outcomes for the measurement of a qubit— value "0" and "1", like a bit or binary digit.  
- Quantum computations on a Qubit, where quantum computations refers to applying quantum logic gates such as   ,Pauli-X, CNOT etc to Qubits.



##### Generating Quantum Random number using python package pythonq

1. Create a new Qubit
2. Applying a Hadamard gate to the Qubit to put it into a **superposition** of equal probability of being 0 and 1.
3. Measuring the Qubit

```python
pip3 install projectq

from projectq.ops import H, Measure
from projectq import MainEngine

# initialises a new quantum backend
quantum_engine = MainEngine()

# Create Quibit
qubit = quantum_engine.allocate_qubit()

# Using Hadamard gate put it in superposition
H | qubit

#  Measure Quibit
Measure | qubit

# print(int(qubit))
random_number = int(qubit)
print(random_number)

# Flushes the quantum engine from memory
quantum_engine.flush()
```



**CNOT** **Gate**

- The CNOT gate is two-qubit operation, where the first qubit is usually referred to as the **control** qubit and the second qubit as the **target** qubit. 
- Leaves the control qubit **unchanged** 
- Performs a **Pauli-X** gate on the **target** qubit when the control qubit is in state **∣1⟩**
- Leaves the **target** **unchanged** when the control qubit is in state **∣0⟩**

**The Bloch Sphere and Pauli-gates**

- In quantum computing, we can imagine the qubit as a sphere- what's referred to as the[ Bloch sphere](https://en.wikipedia.org/wiki/Bloch_sphere). 
- The Bloch sphere is a geometrical representation of a qubit and represents the different states the Qubit can take on, in a 3D space.
- The Pauli family of gates indicates which way the system is spinning around the x, y, or z-axes. Where the Pauli-X gate will equate on the X-axis and, the Pauli-Z will alter the Z axis on the sphere
- **Pauli-X gate** is the direct quantum equivalent of the classical NOT gate . The Pauli-X gate takes one input and **inverts the output**, and is also referred to as a bit flip gate. A bit flip gate means that it will invert the value of the bit in such a way that |1⟩ becomes |0⟩, and |0⟩ becomes |1⟩.
- **The Pauli-Z gate** alters the spin of the Bloch sphere on the Z axis by the defined π radians. Pauli-Z gate leaves state |0⟩ unchanged, but flips |1⟩ to |-1⟩.

```python
from projectq import MainEngine
from projectq.ops import All, CNOT, H, Measure, X, Z
from collections import OrderedDict

quantum_engine = MainEngine()
od = OrderedDict()

control = quantum_engine.allocate_qubit()
target = quantum_engine.allocate_qubit()

H | control
Measure | control
od['Control'] = int(control)

H | target
Measure | target
od['Target'] = int(target)

CNOT | (control, target)
Measure | target
od['CNOT'] = int(target)

quantum_engine.flush()


for key, value in od.items():
    print(key, value)
```

| Control    | 0     | 0     | 1     | **1** |
| ---------- | ----- | ----- | ----- | ----- |
| **Target** | **0** | **1** | **0** | **1** |
| **CNOT**   | **0** | **1** | **1** | **0** |



**Entanglement**

- In physics, the no-cloning theorem states that it is impossible to create an identical copy of an arbitrary unknown quantum state
- The state of one system can be **entangled** with the state of another system.
- For instance, one can use the controlled NOT gate (**CNOT)** and the **Hadamard** gate to **entangle** two qubits.
- Entanglement is not cloning. No well-defined state can be attributed to a subsystem of an entangled state.
- It is impossible to create an identical copy of an unknown quantum state because the quantum state is collapsed when measured, and thus the quantum state is destroyed.
- These two particles are forced to hold mutual information and be **entangled**  in a way that if the information of one particle is known, the information of the other particle is also automatically known. 

**Create Bell Pair**

1. To **entangle** the qubits in a Bell pair, start by applying the Hadamard gate to the first Qubit to put it in a superposition where there is an equal probability of measuring 1 or 0.
2. With the Qubit in superposition, apply a CNOT gate to flip the second Qubit conditionally on the first qubit being in the state |1⟩. 



```python
from projectq import MainEngine
from projectq.ops import All, CNOT, H, Measure, X, Z

quantum_engine = MainEngine()

def entangle(quantum_engine):

    control = quantum_engine.allocate_qubit()
    target = quantum_engine.allocate_qubit()
    H | control
    Measure | control
    control_val = int(control)

    CNOT | (control, target)
    Measure | target
    target_cnot_val = int(target)

    return control_val, target_cnot_val


bell_pair_list = []
for i in range(10):
    bell_pair_list.append(entangle(quantum_engine))
quantum_engine.flush()
print(bell_pair_list)

bell_pair_list = [(1, 1), (1, 1), (1, 1), (1, 1), (1, 1)]
```



**Teleportation** 

- **Teleportation** here means transferring the **state of the particle** through two classical bits, where the state is destroyed by the **sender** when it is measured and recreated by the **receiver** when the classical bits are computed. Quantum teleportation makes use of four different gates, the Hadamard gate, the CNOT gate, the Pauli-X gate and Pauli-Z gate.



The process is executed in three steps.

1. Function to create a Bell pair initially of sender qubit as control and Receiver qubit as Target
2. Creation function to entangle a message into Senders share of the Bell pair, and return the message back as classical bits.
3. Receiver function that takes a classical encoded message, and uses the second pair of the Bell pair to re-create the state of the message qubit.

- Refer teleportation.py
