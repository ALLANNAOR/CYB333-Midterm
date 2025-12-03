"""
Simple TCP client for CYB333 Midterm Exam.
Connects to the server and sends messages for testing.

Run this file after starting the server:
    python client.py
"""

import socket


HOST = "127.0.0.1"   # Server address (localhost)
PORT = 5000          # Must match the server port


def run_client():
    """Connect to the server, send messages, receive responses, and handle errors."""

    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.settimeout(5)  # Prevents freezing

        try:
            print(f"[CLIENT] Connecting to {HOST}:{PORT} ...")
            client_socket.connect((HOST, PORT))
            print("[CLIENT] Connected to server.")
            print("[CLIENT] Type a message and press Enter. Type 'quit' to exit.\n")

            while True:
                message = input("Enter message: ")

                # Quit command for clean shutdown
                if message.lower().strip() == "quit":
                    print("[CLIENT] Closing connection.")
                    break

                # Prevent sending empty messages
                if not message.strip():
                    print("[CLIENT] Empty message detected. Try again.")
                    continue

                # Send message to server
                client_socket.sendall(message.encode("utf-8"))

                # Receive response
                data = client_socket.recv(1024)

                if not data:
                    print("[CLIENT] Server closed the connection.")
                    break

                response = data.decode("utf-8").strip()
                print(f"[CLIENT] Received: {response}")

        except ConnectionRefusedError:
            print("[CLIENT] Connection failed. Is the server running?")

        except socket.timeout:
            print("[CLIENT] Connection attempt timed out.")

        except KeyboardInterrupt:
            print("\n[CLIENT] Program interrupted by user.")

        except Exception as e:
            print(f"[CLIENT] Unexpected error: {e}")

        print("[CLIENT] Client stopped cleanly.")


if __name__ == "__main__":
    run_client()
