from unittest import result
import eventlet
import socketio
import speech_recognition as sr
import tqdm
import os


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

sio = socketio.Server()
app = socketio.WSGIApp(sio) #, static_files={'/': {'content_type': 'text/html', 'filename': 'index.html'}})

def use_asr(data):
    recog = sr.Recognizer()
    audio_file_ = sr.AudioFile(data)
    with audio_file_ as source:
        audio_file = recog.record(source, duration = 7.0)
        result = recog.recognize_google(audio_data=audio_file, language='th')
    return result

@sio.on('connect')
def connect(sid, environ):
    sio.emit('message',"Hi")
    print('connect ', sid)

@sio.on('message')
def message(sid, data):
    print('message ', data)

@sio.on('file')
def get_file(sid, data):
    print('file ', data, ' from ',sid)
    
    result = use_asr(data)
    print(result)
    sio.emit('asr',result)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
    