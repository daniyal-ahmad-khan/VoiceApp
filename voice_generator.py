from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import soundfile as sf
import sounddevice as sd
import io
import numpy as np
import openai
import yaml
import sys
import os
import threading

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

imgs_path = resource_path('imgs/')

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_initial_config_if_missing(file_path):
    if not os.path.isfile(file_path):
        initial_config = {
            'api_key': 'sk-dasda',
            'char_count': 0,
            'first_startup': True,
            'license_key': 'A-B-C-D'
        }
        with open(file_path, 'w') as file:
            yaml.dump(initial_config, file, default_flow_style=False)

def persistent_path(relative_path):
    app_dir = os.path.join(os.path.expanduser("~"), ".VoiceApp")
    ensure_directory_exists(app_dir)
    config_file_path = os.path.join(app_dir, relative_path)
    create_initial_config_if_missing(config_file_path)
    return config_file_path

config_path = persistent_path('config.yaml')

class VoiceGenerator(QObject):
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, text, settings):
        super().__init__()
        self.text = text
        self._is_running = True
        self.config = self.load_config()
        self.update_config(settings)
        self.client = openai.OpenAI(api_key=self.config.get('api_key'))
        self.audio_data_list = []
        self.playback_thread = None
        self.stop_playback = threading.Event()

    def update_config(self, settings):
        self.config.update(settings)

    def load_config(self):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def stop(self):
        print("Stopping VoiceGenerator...")
        self._is_running = False
        self.stop_playback.set()
        if self.playback_thread and self.playback_thread.is_alive():
            self.playback_thread.join()
        print("VoiceGenerator stopped.")

    def split_text(self, text, max_length):
        for i in range(0, len(text), max_length):
            yield text[i:i + max_length]

    @pyqtSlot()
    def run(self):
        try:
            self.audio_data_list = []
            max_chunk_size = 4000
            chunks = list(self.split_text(self.text, max_chunk_size))

            for idx, sentence in enumerate(chunks):
                if not self._is_running:
                    self.finished.emit()
                    return

                if not sentence.endswith('.'):
                    sentence += '.'

                try:
                    response = self.client.audio.speech.create(
                        model="tts-1-hd" if self.config.get("quality") == "HD" else "tts-1",
                        voice=self.config.get('voice'),
                        input=sentence,
                        response_format=self.config.get('format')
                    )
                    buffer = io.BytesIO()
                    for chunk in response.iter_bytes(chunk_size=4096):
                        if not self._is_running:
                            self.finished.emit()
                            return
                        buffer.write(chunk)
                    buffer.seek(0)

                    with sf.SoundFile(buffer, 'r') as sound_file:
                        data = sound_file.read(dtype='float32')
                        self.samplerate = sound_file.samplerate

                    if len(data.shape) == 1:
                        data = np.stack([data, data], axis=-1)

                    self.audio_data_list.append(data)

                except Exception as e:
                    error_message = f"Error in processing sentence: {e}"
                    self.error_occurred.emit(error_message)
                    return

            if self._is_running:
                self.save_combined_audio()
                self.play_combined_audio()

            self.finished.emit()
        except Exception as e:
            error_message = f"Error in processing: {str(e)}"
            self.error_occurred.emit(error_message)
        finally:
            self.finished.emit()

    def save_combined_audio(self):
        combined_data = np.concatenate(self.audio_data_list, axis=0)
        output_file_path = self.config.get('output_path', 'default_output.mp3')
        file_format = output_file_path.split('.')[-1]
        sf.write(output_file_path, combined_data, self.samplerate, format=file_format)

    def play_combined_audio(self):
        self.stop_playback.clear()
        combined_data = np.concatenate(self.audio_data_list, axis=0)

        stream = sd.OutputStream(samplerate=self.samplerate, channels=2)
        stream.start()
        chunk_size = 1024
        for start in range(0, len(combined_data), chunk_size):
            if self.stop_playback.is_set():
                break
            end = min(start + chunk_size, len(combined_data))
            stream.write(combined_data[start:end])
        stream.stop()
        self.finished.emit()

