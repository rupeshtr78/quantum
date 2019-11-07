from projectq import MainEngine
from projectq.ops import All, CNOT, H, Measure, X, Z

quantum_engine = MainEngine()


def create_bell_pair(quantum_engine):
    # Newly created Qubits are in the base state of 0,
    qubit_one = quantum_engine.allocate_qubit()
    qubit_two = quantum_engine.allocate_qubit()
    H | qubit_one
    # Measure | qubit_one
    # qubit_one_val = int(qubit_one)

    CNOT | (qubit_one, qubit_two)
    # Measure | qubit_two
    # cnot_val = int(qubit_two)

    return qubit_one, qubit_two


def create_message(quantum_engine='', qubit_one='', message_value=0):
    qubit_to_send = quantum_engine.allocate_qubit()
    if message_value == 1:
        '''
        setting the qubit to positive if message_value is 1
        by flipping the base state with a Pauli-X gate.
        '''
        X | qubit_to_send

    # entangle the original qubit with the message qubit
    CNOT | (qubit_to_send, qubit_one)

    '''
    1 - Put the message qubit in superposition
    2 - Measure out the two values to get the classical bit value
        by collapsing the state.
    '''
    H | qubit_to_send
    Measure | qubit_to_send
    Measure | qubit_one

    # The qubits are now turned into normal bits we can send through classical channels
    classical_encoded_message = [int(qubit_to_send), int(qubit_one)]

    return classical_encoded_message


def message_reciever(quantum_engine, message, qubit_two):
    '''
    Pauli-X and/or Pauli-Z gates are applied to the Qubit,
    conditionally on the values in the message.
    '''
    if message[1] == 1:
        X | qubit_two
    if message[0] == 1:
        Z | qubit_two

    '''
    Measuring the Qubit and collapsing the state down to either 1 or 0
    '''
    Measure | qubit_two

    quantum_engine.flush()

    received_bit = int(qubit_two)
    return received_bit


qubit_one, qubit_two = create_bell_pair(quantum_engine)
classical_encoded_message = create_message(
    quantum_engine=quantum_engine, qubit_one=qubit_one, message_value=0)

print('classical_encoded_message = ', classical_encoded_message)

received_bit = message_reciever(
    quantum_engine=quantum_engine, message=classical_encoded_message, qubit_two=qubit_two)

print('received_bit = ', str(received_bit))


def send_receive(bit=0, quantum_engine=''):
    # Create bell pair
    qubit_one, qubit_two = create_bell_pair(quantum_engine)
    # entangle the bit with the first qubit
    classical_encoded_message = create_message(
        quantum_engine=quantum_engine, qubit_one=qubit_one, message_value=bit)
    # print('send_bit = ', classical_encoded_message)
    # Teleport the bit and return it back
    received_bit = message_reciever(
        quantum_engine, classical_encoded_message, qubit_two)
    # print('received_bit = ', received_bit)
    return received_bit


message = 'HelloWorld'
binary_encoded_message = [bin(ord(x))[2:].zfill(8) for x in message]
print('Message to send: ', message)
print('Binary message to send: ', binary_encoded_message)

received_bytes_list = []
for letter in binary_encoded_message:
    received_bits = ''
    for bit in letter:
        received_bits = received_bits + \
            str(send_receive(int(bit), quantum_engine))
    received_bytes_list.append(received_bits)

binary_to_string = ''.join([chr(int(x, 2)) for x in received_bytes_list])
print('Received Binary message: ', received_bytes_list)
print('Received message: ', binary_to_string)

quantum_engine.flush()


# bin_mess = 'a'
# print(ord(bin_mess))
# print(bin(ord(bin_mess)))
# print(bin(ord(bin_mess))[2:])
# print(bin(ord(bin_mess))[2:].zfill(8))

# bin_result = bin(ord(bin_mess))[2:].zfill(8)
# print(chr(int(bin_result, 2)))
