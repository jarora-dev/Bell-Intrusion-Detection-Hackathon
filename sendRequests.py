import socketio

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print("Connected!")
    payload = {
        "requestData":
            {
                "sNo": 2,
                "originatingIP": "192.168.1.2",
                "protocol": "UDP",
                "serviceState": "Inactive",
                "sourcePackets": 3,
                "sourceBytes": 500,
            },
        "requestBlocked" : "true"

    }
    sio.emit('send-data', payload)
    print(payload)
    print("Event emitted!")

@sio.on('disconnect')
def on_disconnect():
    print("Disconnected!")

sio.connect('http://localhost:5000')
# sio.wait()