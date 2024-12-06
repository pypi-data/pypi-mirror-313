import os
import sqlite3
import socket
import random
import psutil
import getpass
from ffquant.utils.Logger import stdout_log

__ALL__ = ['get_available_port']

DB_PATH = os.path.expanduser("~/.db/pid_ports.db")

# Ensure the .db directory exists
def ensure_db_directory_exists():
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

# Check if a port is available
def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

# Get an available port
def get_random_available_port():
    while True:
        port = random.randint(7000, 8000)
        if is_port_available(port):
            return port

def initialize_db():
    ensure_db_directory_exists()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pid_ports (
            pid INTEGER PRIMARY KEY,
            port INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Main function to get the available port
def get_available_port(debug=False):
    pid = os.getpid()

    initialize_db()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Fetch all records
        cursor.execute("SELECT pid, port FROM pid_ports")
        records = cursor.fetchall()

        # Remove records with invalid PIDs
        for record in records:
            record_pid, record_port = record
            if not is_pid_running(record_pid):
                if debug:
                    stdout_log(f"Removing idle record, pid: {record_pid}, port: {record_port}")
                cursor.execute("DELETE FROM pid_ports WHERE pid = ?", (record_pid,))

        # Check if current process already has a port
        cursor.execute("SELECT port FROM pid_ports WHERE pid = ?", (pid,))
        result = cursor.fetchone()
        if result:
            # Port already assigned to this process
            port = result[0]
        else:
            # Assign a new port
            port = get_random_available_port()
            if debug:
                stdout_log(f"Assigned new record, pid: {pid}, port: {port}")
            cursor.execute("INSERT INTO pid_ports (pid, port) VALUES (?, ?)", (pid, port))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

    return port

def is_pid_running(pid):
    current_user = getpass.getuser()
    try:
        proc = psutil.Process(pid)
        return proc.username() == current_user
    except psutil.NoSuchProcess:
        return False
    
if __name__ == "__main__":
    stdout_log(get_available_port())