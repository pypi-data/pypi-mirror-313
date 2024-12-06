import socket, random, os, requests
global portA
global hostB
def send(MSG,host,port):
    host = str(host)
    port = int(port)
    MSG = str(MSG)
    print(f"Sending message '{MSG}' to {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            s.sendall(MSG)
        except:
            print("Timed out!")
def recive(host, port):
    host = str(host)
    port = int(port)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
    except:
        print("Cannot start listening, IP is not forwarded or/and is not connected to internet!")
def test():
    print("Contacting Google")
    try:
        request = requests.get("http://216.239.38.120",timeout=5)
        print("Internet is connected")
    except (requests.ConnectionError,requests.Timeout) as exception:
        print("Internet is disconnected")
def Matrix():
    text = ["1","0"]
    for i in range(20):
        line = ""
        for i in range(16):
            line = line + random.choice(text)
        print(line)
