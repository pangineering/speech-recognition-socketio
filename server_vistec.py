from unittest import result
import eventlet
import socketio

import torch
import torchaudio


from transformers import AutoProcessor, AutoModelForCTC
import soundfile as sf
# import librosa



processor = AutoProcessor.from_pretrained("airesearch/wav2vec2-large-xlsr-53-th")

model = AutoModelForCTC.from_pretrained("airesearch/wav2vec2-large-xlsr-53-th")

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

sio = socketio.Server()
app = socketio.WSGIApp(sio) #, static_files={'/': {'content_type': 'text/html', 'filename': 'index.html'}})

def get_transcription(audio_path):
    speech, sr = torchaudio.load(audio_path)
    speech = speech.squeeze()
    resampler = torchaudio.transforms.Resample(sr, 16000)
    speech = resampler(speech)
    input_values = processor(speech, return_tensors="pt", sampling_rate=16000)["input_values"][0]
    logits = model(input_values)["logits"]
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])
    #print(transcription)
    return transcription





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
    result = get_transcription(data)
    
    print(result)
    sio.emit('asr',result)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
    