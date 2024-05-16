from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QTextEdit, QVBoxLayout, 
                             QWidget, QHBoxLayout, QDockWidget, QMessageBox, QFileDialog)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QIcon
import fitz
import qdarktheme
import requests
import yaml
from docx import Document
import openai
import os
import sys
from tutorial import TutorialSlideshow
from styles import dark_theme_style_sidebar, light_theme_style_sidebar
from sidebar import Sidebar
from apisidebar import APISidebar
from voice_generator import VoiceGenerator

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

class MainWindow(QMainWindow):
    themeChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.theme = "dark"
        self.initUI()
        self.thread = None
        self.voice_generator = None
        self.apply_initial_theme()
        self.config = self.load_config()
        if self.config.get('first_startup', True):
            self.promptTutorial()

    def open_save_file_dialog(self):
        options = QFileDialog.Options()
        file_filter = "Audio Files (*.mp3 *.opus *.aac *.flac)"
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", file_filter, options=options)
        return fileName

    def stop_thread(self):
        if self.voice_generator:
            self.voice_generator.stop()

    def on_thread_finished(self):
        print("Thread finished")  # Debug print
        self.submit_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.thread = None

    def start_thread(self):
        if self.thread is not None and self.thread.isRunning():
            return
        self.config = self.load_config()
        api_key = self.config.get("api_key", "")
        is_valid, message = self.validate_api_key(api_key)
        if not is_valid:
            QMessageBox.warning(self, "API Key Validation Failed", message)
            return
        if self.config.get("api_key") != "" and is_valid:
            text = self.text_edit.toPlainText()
            file_path = self.open_save_file_dialog()
            if file_path:
                self.settings = self.sidebar.collect_settings()
                self.settings['output_path'] = file_path

                self.thread = QThread()
                self.voice_generator = VoiceGenerator(text, self.settings)
                self.voice_generator.moveToThread(self.thread)

                self.thread.started.connect(self.voice_generator.run)
                self.voice_generator.finished.connect(self.thread.quit)
                self.voice_generator.finished.connect(self.voice_generator.deleteLater)
                self.thread.finished.connect(self.on_thread_finished)
                self.voice_generator.error_occurred.connect(self.handle_voice_generator_error)
                self.submit_button.setEnabled(False)
                self.stop_button.setEnabled(True)

                self.thread.start()
            else:
                QMessageBox.warning(self, "No File Selected", "Please select a file to save the output.")
        else:
            QMessageBox.warning(self, "No API Key Found", "Please set your OpenAI API key.")

    def initUI(self):
        self.config = self.load_config()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(0)

        left_layout = QHBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Insert Text Here")
        left_layout.addWidget(self.text_edit)

        buttons_layout = QHBoxLayout()

        self.submit_button = QPushButton("Generate Speech")
        self.submit_button.setToolTip("Press to generate speech")
        self.submit_button.setFixedHeight(55)
        self.submit_button.clicked.connect(self.start_thread)
        buttons_layout.addWidget(self.submit_button)

        self.init_stop_button()
        self.init_upload_button()

        self.sidebar_dock_widget = QDockWidget(self)
        self.sidebar = Sidebar(self.sidebar_dock_widget, theme=self.theme, stop_button=self.stop_button, upload_button=self.upload_button)
        self.themeChanged.connect(self.sidebar.on_theme_changed)
        self.sidebar.settings_button.clicked.connect(self.toggle_api_sidebar)
        self.text_edit.textChanged.connect(self.on_text_changed)
        self.sidebar_dock_widget.setWidget(self.sidebar)
        self.sidebar_dock_widget.setAllowedAreas(Qt.RightDockWidgetArea)
        self.sidebar_dock_widget.setTitleBarWidget(QWidget(None))
        self.addDockWidget(Qt.RightDockWidgetArea, self.sidebar_dock_widget)
        left_layout.addWidget(self.sidebar_dock_widget)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(buttons_layout)

        self.api_dock_widget = QDockWidget(self)
        self.api_dock_widget.setVisible(False)
        self.api_sidebar = APISidebar(self.api_dock_widget)
        self.api_sidebar.apiKeyChanged.connect(self.onApiKeyChanged)
        self.api_dock_widget.setWidget(self.api_sidebar)
        self.api_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.api_dock_widget.setTitleBarWidget(QWidget(None))
        self.addDockWidget(Qt.LeftDockWidgetArea, self.api_dock_widget)
        self.themeChanged.connect(self.api_sidebar.on_theme_changed)
        self.api_sidebar.dark_mode_toggle.toggled.connect(self.toggle_theme)

        self.show()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Voice Generation App")
        if not self.config.get('first_startup', False):
            self.implement_verification_initial()
        self.api_sidebar.save_license_key_button.clicked.connect(self.implement_verification)
        self.api_sidebar.save_api_key_button.clicked.connect(self.save_api_dialouge)

    def init_stop_button(self):
        self.stop_button = QPushButton('')
        self.stop_button.setIcon(QIcon(imgs_path + '/stop_icon.png'))
        self.stop_button.setIconSize(QSize(20, 20))
        self.stop_button.setFixedSize(40, 40)
        self.stop_button.clicked.connect(self.stop_thread)
        self.stop_button.setToolTip("Enabled while generating speech")
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet(
            "QPushButton {background-color: #F63D54; border-radius: 20px; border: none; icon-size: 20px;} "
            "QPushButton:hover {background-color: #FA6A64;} "
            "QPushButton:pressed {background-color: #E0343A;}"
        )

    def init_upload_button(self):
        self.upload_button = QPushButton('')
        self.upload_button.setIcon(QIcon(imgs_path + '/upload_icon.png'))
        self.upload_button.setIconSize(QSize(20, 20))
        self.upload_button.setFixedSize(40, 40)
        self.upload_button.setToolTip("Upload a text or PDF file")
        self.upload_button.clicked.connect(self.open_file_dialog)
        self.upload_button.setStyleSheet(
            "QPushButton {background-color: #027FFF; border-radius: 20px; border: none; icon-size: 20px;} "
            "QPushButton:hover {background-color: #3399FF;} "
            "QPushButton:pressed {background-color: #027FFF;}"
        )

    def onApiKeyChanged(self, hasApiKey):
        self.submit_button.setEnabled(hasApiKey)

    def handle_voice_generator_error(self, error_message):
        QMessageBox.critical(self, "Voice Generation Error", error_message)
        self.on_thread_finished()

    def validate_api_key(self, api_key):
        if not api_key.startswith("sk-") or " " in api_key:
            return False, "API key format is incorrect."
        try:
            client = openai.OpenAI(api_key=api_key)
            client.models.list()
            return True, "API key is valid."
        except Exception as e:
            return False, f"API key validation failed: {str(e)}"

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_filter = "Text Files (*.txt);;PDF Files (*.pdf);;Word Files (*.docx)"
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", file_filter, options=options)
        if fileName:
            if fileName.lower().endswith('.pdf'):
                self.process_pdf_file(fileName)
            elif fileName.lower().endswith('.docx'):
                self.process_docx_file(fileName)
            else:
                self.process_and_display_file(fileName)

    def process_and_display_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            self.text_edit.setText(text)
        except Exception as e:
            self.show_error_message(f"Error reading file: {e}")

    def process_pdf_file(self, file_path):
        try:
            doc = fitz.open(file_path)
            text = ''
            for page in doc:
                text += page.get_text()
            self.text_edit.setText(text)
            doc.close()
        except Exception as e:
            self.show_error_message(f"Error processing PDF file: {e}")

    def process_docx_file(self, file_path):
        try:
            doc = Document(file_path)
            text = ''
            for para in doc.paragraphs:
                text += para.text + ' '
            self.text_edit.setText(text)
        except Exception as e:
            self.show_error_message(f"Error processing Word file: {e}")

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def toggle_sidebar(self, state):
        if self.sidebar_dock_widget.isVisible():
            self.sidebar_dock_widget.close()
        else:
            self.sidebar_dock_widget.show()

    def toggle_api_sidebar(self, state):
        if self.api_dock_widget.isVisible():
            self.api_dock_widget.close()
        else:
            self.api_dock_widget.show()

    def toggle_api_sidebar_action(self, visible):
        self.api_sidebar.dark_mode_toggle.setChecked(visible)

    def on_text_changed(self):
        text = self.text_edit.toPlainText()
        self.sidebar.update_character_count(len(text))
        self.sidebar.calculate_cost(len(text))

    def toggle_theme(self, state):
        if state:
            self.theme = "dark"
            qdarktheme.setup_theme(theme="dark", additional_qss="QWidget {border-radius: 10px;}")
            self.themeChanged.emit(self.theme)
            self.apply_theme_styles(dark_theme_style_sidebar)
        else:
            self.theme = "light"
            qdarktheme.setup_theme(theme="light", additional_qss="QWidget {border-radius: 10px;}")
            self.themeChanged.emit(self.theme)
            self.apply_theme_styles(light_theme_style_sidebar)

    def apply_initial_theme(self):
        if self.theme == "dark":
            qdarktheme.setup_theme(theme="dark", additional_qss="QWidget {border-radius: 10px;}")
            self.themeChanged.emit(self.theme)
            self.apply_theme_styles(dark_theme_style_sidebar)
        else:
            qdarktheme.setup_theme(theme="light", additional_qss="QWidget {border-radius: 10px;}")
            self.themeChanged.emit(self.theme)
            self.apply_theme_styles(light_theme_style_sidebar)

    def apply_theme_styles(self, theme_styles):
        self.submit_button.setStyleSheet(theme_styles["button"])
        self.text_edit.setStyleSheet(theme_styles["edit_text"])

    def verify_license(self, license_key):
        url = "https://api.gumroad.com/v2/licenses/verify"
        data = {
            "product_id": "bXY9aPoQUJgqcwuCkCdaVw==",
            "license_key": license_key
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def enable_app(self):
        self.text_edit.setEnabled(True)
        self.submit_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.upload_button.setEnabled(True)

    def disable_app(self):
        self.text_edit.setDisabled(True)
        self.submit_button.setDisabled(True)
        self.stop_button.setDisabled(True)
        self.upload_button.setDisabled(True)

    def show_authentication_failed_alert(self):
        QMessageBox.critical(self, "Authentication Failed", "The license verification has failed. Please check your license key.")

    def show_verification_success_alert(self):
        QMessageBox.information(self, "Verification Successful", "The license key has been successfully verified.")

    def implement_verification_initial(self):
        license_key = self.api_sidebar.license_key_input.text()
        license_data = self.verify_license(license_key)
        if license_data and license_data.get("success"):
            self.enable_app()
        else:
            self.disable_app()
            self.show_authentication_failed_alert()

    def implement_verification(self):
        license_key = self.api_sidebar.license_key_input.text()
        license_data = self.verify_license(license_key)
        if license_data and license_data.get("success"):
            self.enable_app()
            self.show_verification_success_alert()
        else:
            self.disable_app()
            self.show_authentication_failed_alert()

    def load_config(self):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def save_config(self, config):
        with open(config_path, 'w') as file:
            yaml.safe_dump(config, file)

    def save_api_dialouge(self):
        api_key = self.api_sidebar.api_key_input.text()
        is_valid, message = self.validate_api_key(api_key)
        if api_key and is_valid:
            self.api_alert_success()
        else:
            self.api_alert_fail(message)

    def api_alert_fail(self, message):
        if message:
            QMessageBox.critical(self, "Failed!", message)
        else:
            QMessageBox.critical(self, "Failed!", "API key not saved.")

    def api_alert_success(self):
        QMessageBox.information(self, "Saved!", "API key saved successfully.")

    def promptTutorial(self):
        reply = QMessageBox.question(self, 'Tutorial', 'Do you want to see the tutorial?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.showTutorial()
        else:
            config = self.load_config()
            config['first_startup'] = False
            self.save_config(config)

    def showTutorial(self):
        self.tutorialDialog = TutorialSlideshow(self, self)
        self.tutorialDialog.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    sys.exit(app.exec_())
