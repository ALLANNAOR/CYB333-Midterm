"""
Simple Python Port Scanner for CYB333 Midterm Exam
You are ONLY authorized to scan:
 - 127.0.0.1
 - localhost
 - scanme.nmap.org
"""

import socket
import time
from datetime import datetime


def parse_ports(port_input):
    """Convert strings like '22,80,443' or '20-25' into a list of ports."""
    ports = set()
    pieces = port_input.split(",")

    for piece in pieces:
        piece = piece.strip()
        if not piece:
            continue

        if "-" in piece:
            # Handle ranges like 20-25
            start_str, end_str = piece.split("-", 1)
            start = int(start_str)
            end = int(end_str)

            if start < 1 or end > 65535 or start > end:
                raise ValueError("Port range must be between 1 and 65535.")

            for p in range(start, end + 1):
                ports.add(p)

        else:
            # Single port
            port = int(piece)
            if port < 1 or port > 65535:
                raise ValueError("Ports must be 1–65535.")
            ports.add(port)

    if not ports:
        raise ValueError("No valid ports provided.")

    return sorted(ports)


def scan_port(host, port):
    """Return True if port is open, False if closed."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        return result == 0  # 0 means OPEN


def main():
    print("=== CYB333 SIMPLE PYTHON PORT SCANNER ===")
    print("ALLOWED TARGETS: 127.0.0.1, localhost, scanme.nmap.org\n")

    target = input("Enter target (e.g., 127.0.0.1): ").strip()

    # Prevent scanning unauthorized systems
    allowed = ["127.0.0.1", "localhost", "scanme.nmap.org"]
    if target not in allowed:
        print("[ERROR] This host is NOT authorized for scanning.")
        return

    port_string = input("Enter ports (e.g., 22,80,443 or 20-25): ").strip()

    try:
        ports = parse_ports(port_string)
    except ValueError as e:
        print(f"[ERROR] Invalid port list: {e}")
        return

    # Try to resolve the target to an IP address
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("[ERROR] Host could not be resolved.")
        return

    print(f"\nScanning {target} ({ip})...")
    print("Ports to scan:", ports)

    start = datetime.now()
    print(f"Scan started: {start.strftime('%Y-%m-%d %H:%M:%S')}\n")

    open_ports = []

    for port in ports:
        try:
            is_open = scan_port(ip, port)
            status = "OPEN" if is_open else "closed"
            print(f"Port {port}: {status}")

            if is_open:
                open_ports.append(port)

            time.sleep(0.05)  # polite delay

        except Exception as e:
            print(f"[ERROR] Problem scanning port {port}: {e}")

    end = datetime.now()
    print("\nScan finished:", end.strftime('%Y-%m-%d %H:%M:%S'))
    print("Total time:", end - start)

    if open_ports:
        print("\nOpen ports found:")
        for p in open_ports:
            print(f" - {p}")
    else:
        print("\nNo open ports detected.")


if __name__ == "__main__":
    main()
