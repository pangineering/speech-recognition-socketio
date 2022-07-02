import socketio

sio = socketio.Client()



@sio.on('connect')
def on_connect():
    sio.emit('message', {'response': 'my response'})
    print('connection established')

@sio.on('message')
def on_message(data):
    print('message received with ', data)
    #sio.emit('message', {'response': 'my response'})

@sio.on('asr')
def on_asr(data):
    print('asr received with ', data)
    #sio.emit('message', {'response': 'my response'})

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

sio.connect('http://localhost:8000')
sio.emit('file',"test.wav")