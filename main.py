import re
import webvtt
import torch
import argparse
from pydub import AudioSegment
from TTS.api import TTS
import os
import io

def text_to_speech(tts, text, speaker_wav, lang):
    buffer = io.BytesIO()
    tts.tts_to_file(text=text, speaker_wav=speaker_wav, language=lang, file_path=buffer, temperature=0.8)
    buffer.seek(0)
    return AudioSegment.from_wav(buffer)

def silence(duration):
    return AudioSegment.silent(duration=duration)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converti un file WebVTT in un file WAV.')
    parser.add_argument('vtt_file', type=str, help='Il file VTT da convertire.')
    parser.add_argument('speaker_wav', type=str, help='Il file WAV dello speaker.')
    parser.add_argument('lang', type=str, help='Lingua da usare per la voce. Es. en per inglese, it per italiano, ecc...')
    args = parser.parse_args()
    captions = webvtt.read(args.vtt_file)
    final_audio = AudioSegment.empty()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = "tts_models/multilingual/multi-dataset/your_tts"
   # model = "tts_models/multilingual/multi-dataset/xtts_v2"
    tts = TTS(model).to(device)
    
    total_duration = 0

    for i in range(len(captions)):
        text = captions[i].text.replace('\n', ' ')
        sentences = re.split(r'(?<=[.!?]) +', text)
        for sentence in sentences:
            speech = text_to_speech(tts, sentence, args.speaker_wav, args.lang)
            speech_duration = len(speech)
            silence_duration = (captions[i].start_in_seconds * 1000) - total_duration
            if silence_duration > 0:
                final_audio += silence(silence_duration)
                total_duration += silence_duration
            final_audio += speech
            total_duration += speech_duration

        output_filename = os.path.splitext(os.path.basename(args.vtt_file))[0] + os.path.splitext(os.path.basename(args.speaker_wav))[0] + "_" + args.lang + '.wav'
        final_audio.export(output_filename, format='wav')