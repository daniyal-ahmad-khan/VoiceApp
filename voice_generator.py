from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import soundfile as sf
import sounddevice as sd
import io
import numpy as np
import openai
import yaml
import sys
import os


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Use these paths in your application

imgs_path = resource_path('imgs/')

def ensure_directory_exists(path):
    """Ensure that a directory exists."""
    if not os.path.exists(path):
        os.makedirs(path)

def create_initial_config_if_missing(file_path):
    """Create the initial config.yaml if it does not exist."""
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
    """Resolve path for writable files ensuring persistence across sessions."""
    app_dir = os.path.join(os.path.expanduser("~"), ".VoiceApp")
    ensure_directory_exists(app_dir)
    
    config_file_path = os.path.join(app_dir, relative_path)
    create_initial_config_if_missing(config_file_path)
    
    return config_file_path

# Use this to get the path to your config.yaml
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

    def update_config(self, settings):
        self.config.update(settings)

    def load_config(self):
        # Read configuration from YAML file
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def stop(self):
        self._is_running = False

    def split_text(self,text, max_length):
        for i in range(0, len(text), max_length):
            yield text[i:i + max_length]


    def split_text(self,text, max_length):
        for i in range(0, len(text), max_length):
            yield text[i:i + max_length]

    @pyqtSlot()
    def run(self):
        # Split the text into sentences
        try:
            self.audio_data_list = []
            print(self.config)
            max_chunk_size = 4000
            print("Starting to chunk the text.")

            # Split the text into chunks
            chunks = list(self.split_text(self.text, max_chunk_size))
            print(f"Total chunks to process: {len(chunks)}")

            # Process each sentence
            for idx, sentence in enumerate(chunks):
                if not self._is_running:
                    print("Operation stopped.")
                    self.finished.emit()
                    return

                # Ensure that the sentence ends with a period
                if not sentence.endswith('.'):
                    sentence += '.'

                print(f"Processing sentence {idx + 1} of {len(chunks)}")

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
                            print("Operation stopped.")
                            self.finished.emit()
                            return
                        buffer.write(chunk)
                    buffer.seek(0)

                    # Load the audio data
                    with sf.SoundFile(buffer, 'r') as sound_file:
                        data = sound_file.read(dtype='float32')
                        self.samplerate = sound_file.samplerate

                    # Determine if the audio is mono or stereo
                    if len(data.shape) == 1:
                        # If mono, convert to stereo by duplicating the channel
                        data = np.stack([data, data], axis=-1)

                    # Create a stream for stereo playback
                    stream = sd.OutputStream(samplerate=self.samplerate, channels=2)
                    stream.start()

                    # Play the audio in chunks, checking the _is_running flag
                    chunk_size = 1024
                    for start in range(0, len(data), chunk_size):
                        if not self._is_running:
                            break
                        end = min(start + chunk_size, len(data))
                        stream.write(data[start:end])

                    stream.stop()
                    self.audio_data_list.append(data)

                except Exception as e:
                    print(f"Error in processing sentence: {e}")

            if self._is_running:
                print("All sentences processed and converted to speech.")
                self.save_combined_audio()
            else:
                print("Operation stopped by the user.")

            self.finished.emit()
        except Exception as e:
            error_message = f"Error in processing sentence: {str(e)}"
            print(error_message)
            self.error_occurred.emit(error_message)  # Emit the error signal
            return
        finally:
            self.finished.emit()


    def save_combined_audio(self):
        combined_data = np.concatenate(self.audio_data_list, axis=0)
        output_file_path = self.config.get('output_path', 'default_output.mp3')  # Default name if not provided

        # Determine the file format from the file extension
        file_format = output_file_path.split('.')[-1]
        sf.write(output_file_path, combined_data, self.samplerate, format=file_format)