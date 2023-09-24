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


def malicious_request_detected(srcip=None, dstip=None, sport=None, dport=None, proto=None, service=None, sbytes=None, sttl=None, dttl=None):
    
    srcip = srcip or request.args.get('srcip')
    dstip = dstip or request.args.get('dstip')
    sport = sport or int(request.args.get('sport', 0))
    dport = dport or int(request.args.get('dport', 0))
    proto = proto or request.args.get('proto')
    service = service or request.args.get('service')
    sbytes = sbytes or int(request.args.get('sbytes', 0))
    sttl = sttl or int(request.args.get('sttl', 0))
    dttl = dttl or int(request.args.get('dttl', 0))
    
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
    if malicious_request_detected():
        return send_from_directory(directory="dummy", filename="secret.txt")
    else:
        return send_from_directory(directory="real", filename="secret.txt")

if __name__ == '__main__':
    run_sniff()  
    app.run(host='0.0.0.0', port=8080)
