from flask import Flask, send_from_directory, request, jsonify
import requests
from scapy.all import sniff
import threading


app = Flask(__name__)

def process_packet(packet):
    if packet.haslayer('IP') and (packet.haslayer('TCP') or packet.haslayer('UDP')):
        srcip = packet['IP'].src
        dstip = packet['IP'].dst
        proto = packet['IP'].proto
        sbytes = len(packet)
        sttl = packet['IP'].ttl
        dttl = packet['IP'].ttl  # Using the TTL of the incoming packet

        # Default values
        sport = 0
        dport = 0
        service = "UNKNOWN"

        if packet.haslayer('TCP'):
            sport = packet['TCP'].sport
            dport = packet['TCP'].dport
            if dport == 80 or sport == 80:
                service = 'HTTP'
            elif dport == 443 or sport == 443:
                service = 'HTTPS'
        elif packet.haslayer('UDP'):
            sport = packet['UDP'].sport
            dport = packet['UDP'].dport
            if dport == 53 or sport == 53:
                service = 'DNS'

        if malicious_request_detected(srcip, dstip, sport, dport, proto, service, sbytes, sttl, dttl):
            print("Malicious packet detected!")
        else:
            print("Safe packet detected!")

# This function will run the sniffing in the background.
def run_sniff():
    sniff_thread = threading.Thread(target=lambda: sniff(filter="ip", prn=process_packet))
    sniff_thread.start()


def malicious_request_detected(srcip, dstip, sport, dport, proto, service, sbytes, sttl, dttl):
    ml_endpoint = "https://ec2-3-95-189-216.compute-1.amazonaws.com/predict/"
    
    req_data = {
        'srcip': srcip,
        'dstip': dstip,
        'sport': sport,
        'dport': dport,
        'proto': proto,
        'service': service,
        'sbytes': sbytes,
        'sttl': sttl,
        'dttl': dttl,
    }

    response = requests.post(ml_endpoint, json=req_data)
    return response.json().get('malicious', False)

@app.route('/')
def serve_file():
    if malicious_request_detected("some_srcip", "some_dstip", 80, 80, "TCP", "HTTP", 100, 64, 64):
        return send_from_directory(directory="path_to_directory", filename="file2.txt")
    else:
        return send_from_directory(directory="path_to_directory", filename="file1.txt")

if __name__ == '__main__':
    run_sniff()  
    app.run("Server Running and sniffing packets",host='0.0.0.0', port=8080)
