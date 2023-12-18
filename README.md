# WebVTT to WAV Converter by NiSpa

This project contains a Python script that converts VTT (WebVTT) files into WAV audio files using a speech synthesis model.

In this script, TTS and the `xtts_v2` model will be used.

## Requirements

- Python 3.6 or higher
- Python Libraries: `webvtt`, `torch`, `argparse`, `pydub`, `TTS`

## Usage

After cloning the project...
1. Install the necessary dependencies with `pip install -r requirements.txt`.
2. From within the directory, activate the venv environment using `python -m venv venv`
3. Activate the virtual environment, for example, on windows it's `.\venv\Scripts\activate`
4. Run the script with `python main.py yourfile.vtt speaker.wav`, replacing "yourfile.vtt" with the path of your VTT file and `speaker.wav` with the path of the wav file of the speaker's voice to clone. A wav file of at least 7 seconds of clear voice is needed to clone.

## License

This project is distributed under the MIT license.
