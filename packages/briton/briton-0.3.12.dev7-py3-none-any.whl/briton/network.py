import socket


def is_port_available(port, host="localhost"):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Try to connect to the specified host and port
            s.bind((host, port))
            return True
    except OSError:
        # Port is not available
        return False
