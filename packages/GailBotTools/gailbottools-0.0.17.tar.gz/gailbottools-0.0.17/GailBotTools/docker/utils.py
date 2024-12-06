import socket
import sys

# CONSTANTS
SLEEP_TIME = 1
ID_BYTES = 4
SIZE_BYTES = 16
MD_BYTES = 20
def send_data(client_socket, id: str, data: str):
    
    id = int(id)
    id_bytes = id.to_bytes(length=ID_BYTES, byteorder='big', signed=False)

    # Encode the data and calculate its length
    data_bytes = data.encode('utf-8')
    data_length = len(data_bytes)
    
    # Convert length to bytes
    size_bytes = data_length.to_bytes(length=SIZE_BYTES, byteorder='big', signed=False)

    # Construct the payload
    payload = id_bytes + size_bytes + data_bytes

    sys.stdout.flush()
    if len(data) > 1_000_000:
        raise ValueError("Payload size exceeds the maximum allowed limit.")
    else: 
        client_socket.sendall(payload)

def recv_all(client_socket):
    # Receive the metadata: ID (4 bytes) + Size (16 bytes)
    meta_data = recv_all_helper(client_socket, MD_BYTES)

    sys.stdout.flush()

    if len(meta_data) != MD_BYTES:
        raise ValueError(f"Metadata length is incorrect. Expected 20 bytes, got {len(meta_data)} bytes")

    # Split the metadata into ID and size_of_payload
    id = int.from_bytes(meta_data[:4], byteorder='big')
    size_of_payload = int.from_bytes(meta_data[4:], byteorder='big')
    

    # Receive the payload itself
    payload = recv_all_helper(client_socket, size_of_payload)

    return id, payload.decode('utf-8')

def recv_all_helper(sock, n):
    """ Helper function to receive exactly n bytes from the socket """
    data = b''
    while len(data) < n:
        try:
            packet = sock.recv(n - len(data))
            if not packet:
                raise ConnectionError("Socket connection lost")
            data += packet
        except Exception as e:
            print(f"[DEBUG] Error while receiving data: {e}")
            sys.stdout.flush()
            raise
    return data


if __name__ == "__main__":
    sys.stderr.write("This is a utils package and not meant to be run on its own\n")
    exit(1)
