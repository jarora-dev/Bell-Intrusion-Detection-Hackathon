import socketio
from scapy.all import *
from scapy.layers.http import HTTP, HTTPRequest, HTTPResponse
from scapy.layers.inet import IP, TCP
import pandas as pd


df = pd.read_csv('test.csv')

dst_ip = '3.95.237.206'  
dst_port = 8080  

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print("Connected!")

@sio.on('disconnect')
def on_disconnect():
    print("Disconnected!")

sio.connect('http://localhost:5000')

for index, row in df.iterrows():
    srcip = row['srcip']
    dstip = row['dstip']
    sport = row['sport']
    dport = row['dport']
    proto = row['proto']
    service = row['service']
    sbytes = row['sbytes']
    sttl = row['sttl']
    dttl = row['dttl']

    # SYN
    syn = IP(src=src_ip, dst=dst_ip, ttl=sttl) / TCP(sport=src_port, dport=dst_port, flags='S')
    # syn_ack = sr1(syn)

    # ACK
    ack = IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags='A', seq=syn_ack.ack, ack=syn_ack.seq + 1)
    send(ack)

    print("Packet Sent")

    # HTTP Request with parameters
    path_with_params = f"/?proto={proto}&service={service}&sbytes={sbytes}&sttl={sttl}&dttl={dttl}"
    http_req = HTTP() / HTTPRequest(Method="GET", Path=path_with_params, Host=dst_ip)
    response = sr1(IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags='A', seq=syn_ack.ack, ack=syn_ack.seq + 1) / http_req)

    # Handle the response
    if response and HTTPResponse in response:
        http_response = response[HTTPResponse]
        content = http_response.load.decode('utf-8')
        if "539b77d2a929c972a243bf7bc5aa7483" in content:  # Secret Content
            print("Server responded with the secret content")
            payload = {
                "requestData": {
                    "sNo": 2,
                    "originatingIP": "192.168.1.2",
                    "protocol": "UDP",
                    "serviceState": "Inactive",
                    "sourcePackets": 3,
                    "sourceBytes": 700,
                },
                "requestBlocked": False,
                "requestMalicious": False
            }
            sio.emit('send-data', payload)
            print(payload)
            print("Event emitted!")

        elif "17bce0c664922472c00fc5843b312780" in content:  # Dummy Content
            print("Server responded with the dummy content")
            payload = {
                "requestData": {
                    "sNo": 2,
                    "originatingIP": "192.168.1.2",
                    "protocol": "UDP",
                    "serviceState": "Inactive",
                    "sourcePackets": 3,
                    "sourceBytes": 700,
                },
                "requestBlocked": True,
                "requestMalicious": False
            }
            sio.emit('send-data', payload)
            print(payload)
            print("Event emitted!")
        else:
            print("Unexpected response content from server:", content)

    # Finishing the connection
    fin = ip_layer / TCP(sport=src_port, dport=dst_port, flags='FA', seq=response.ack, ack=response.seq + len(response.payload))
    fin_ack = sr1(fin, verbose=False)

    sio.disconnect()


