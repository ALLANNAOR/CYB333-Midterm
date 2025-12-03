"""
Simple TCP server for CYB333 Midterm Exam.
Listens for client connections and echoes messages back.

Run this file first:
    python server.py
"""

import socket


HOST = "127.0.0.1"   # Localhost
PORT = 5000          # Port the server listens on


def start_server():
    """Start a basic TCP server that handles one client at a time."""

    # Create a TCP socket (IPv4, TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # Allow quick reuse of address after shutdown
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind((HOST, PORT))
        except OSError as e:
            print(f"[SERVER] Could not bind to {HOST}:{PORT} → {e}")
            return

        server_socket.listen(1)
        print(f"[SERVER] Listening on {HOST}:{PORT} ...")
        print("[SERVER] Waiting for a client connection ...")

        try:
            while True:
                conn, addr = server_socket.accept()
                print(f"[SERVER] Connected to {addr}")

                # Context manager ensures clean connection close
                with conn:
                    while True:
                        data = conn.recv(1024)

                        # Client closed connection
                        if not data:
                            print("[SERVER] Client disconnected.")
                            break

                        message = data.decode("utf-8").strip()
                        print(f"[SERVER] Received: {message}")

                        response = f"Server received: {message}"
                        conn.sendall(response.encode("utf-8"))
                        print(f"[SERVER] Sent: {response}")

        except KeyboardInterrupt:
            print("\n[SERVER] Server shutdown requested (CTRL+C).")

        except Exception as e:
            print(f"[SERVER] Unexpected error: {e}")

        print("[SERVER] Server stopped cleanly.")


if __name__ == "__main__":
    start_server()
