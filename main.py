import re
import webvtt
import torch
import argparse
from pydub import AudioSegment
from TTS.api import TTS
import os
import io

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(model).to(device)

def text_to_speech(text, speaker_wav):
    # Usa un buffer di memoria invece di un file temporaneo
    buffer = io.BytesIO()
    tts.tts_to_file(text=text, speaker_wav=speaker_wav, language="en", file_path=buffer)
    buffer.seek(0)
    return AudioSegment.from_wav(buffer)

def silence(duration):
    return AudioSegment.silent(duration=duration)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converti un file VTT in un file WAV.')
    parser.add_argument('vtt_file', type=str, help='Il file VTT da convertire.')
    parser.add_argument('speaker_wav', type=str, help='Il file WAV dello speaker.')
    args = parser.parse_args()
    captions = webvtt.read(args.vtt_file)
    final_audio = AudioSegment.empty()

    for i in range(len(captions)):
        # Rimuovi i ritorni a capo dal testo
        text = captions[i].text.replace('\n', ' ')
        # divide le frasi se c'è un punto 
        sentences = re.split(r'(?<=[.!?]) +', text)
        for sentence in sentences:
            speech = text_to_speech(sentence, args.speaker_wav)
            final_audio += speech

        if i > 0 and captions[i].start_in_seconds != captions[i-1].end_in_seconds:
            silence_duration = (captions[i].start_in_seconds - captions[i-1].end_in_seconds) * 1000
            final_audio += silence(silence_duration)

    final_audio.export('output.wav', format='wav')
