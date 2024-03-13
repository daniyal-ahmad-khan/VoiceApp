import base64
from PyQt5.QtWidgets import QWidget,QPushButton, QVBoxLayout, QHBoxLayout,\
    QCheckBox, QComboBox, QLabel, QToolTip, QFrame, QSpacerItem, QSizePolicy,\
        QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
from qtwidgets import AnimatedToggle
from PyQt5.QtGui import QFont
from styles import api_key_button_style,dark_theme_style_sidebar
import pyqtgraph as pg
import qdarktheme
import yaml
from styles import dark_theme_style_sidebar, light_theme_style_sidebar
from toggle_switch import PyQtSwitch
import sys
import os

api_sidebar_ui = base64.b64encode(b"""from PyQt5.QtWidgets import QWidget,QPushButton, QVBoxLayout, QHBoxLayout,\
    QCheckBox, QComboBox, QLabel, QToolTip, QFrame, QSpacerItem, QSizePolicy,\
        QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
from qtwidgets import AnimatedToggle
from PyQt5.QtGui import QFont
from styles import api_key_button_style,dark_theme_style_sidebar
import pyqtgraph as pg
import qdarktheme
import yaml
from styles import dark_theme_style_sidebar, light_theme_style_sidebar
from toggle_switch import PyQtSwitch
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
config_path = resource_path('config.yaml')



class APISidebar(QWidget):
    apiKeyChanged = pyqtSignal(bool)
    def __init__(self, parent=None,theme="dark"):
        super().__init__(parent)
        self.initUI()
        self.theme = theme
        self.load_keys()
        self.apply_initial_theme()
        

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        self.setFixedWidth(210)
        def centered_widget(widget, width=None):
            hbox = QHBoxLayout()
            hbox.addWidget(widget)
            hbox.setAlignment(Qt.AlignCenter)
            if width:
                widget.setFixedWidth(width)
            return hbox
        self.theme_label = QLabel("Toggle Theme:", self)
        self.theme_label.setAlignment(Qt.AlignLeft)
        self.theme_label.setStyleSheet("QLabel {color: #808080;        /* Set the text color to purple */font-size: 20px;    /* Optional: Adjust font size as needed */}")
        layout.addWidget(self.theme_label)
        toggle_container = QFrame(self)
        toggle_container_layout = QHBoxLayout(toggle_container)
        toggle_container_layout.setAlignment(Qt.AlignCenter)
        toggle_container.setFixedWidth(190)
        sd_label = QLabel("Light", toggle_container)
        sd_label.setStyleSheet("font-weight: bold;")
        toggle_container_layout.addWidget(sd_label)

        self.dark_mode_toggle = PyQtSwitch()
        self.dark_mode_toggle.setAnimation(True)
        self.dark_mode_toggle.setToolTip("Toggle Dark Mode")
        # self.dark_mode_toggle.setChecked(True)
        # self.dark_mode_toggle.setFixedWidth(60)
        
        
        toggle_container_layout.addWidget(self.dark_mode_toggle)
        hd_label = QLabel("Dark", toggle_container)
        hd_label.setStyleSheet("font-weight: bold;")
        toggle_container_layout.addWidget(hd_label)
        layout.addWidget(toggle_container)
        spacerx = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        

        layout.addSpacerItem(spacerx)
        self.license_key_input = QLineEdit(self)
        self.license_key_input.setPlaceholderText("Enter License Key")
        self.license_key_input.setFixedWidth(190)
        self.license_key_input.setToolTip("Edit License Key")
        layout.addLayout(centered_widget(self.license_key_input, 190))
        self.save_license_key_button = QPushButton("Save License Key", self)
        self.save_license_key_button.setFixedWidth(190)
        self.save_license_key_button.setStyleSheet(api_key_button_style)
        self.save_license_key_button.clicked.connect(self.save_license_key)
        self.save_license_key_button.setToolTip("Save License Key")
        layout.addLayout(centered_widget(self.save_license_key_button,190))

        # spacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        

        # layout.addSpacerItem(spacer)
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setPlaceholderText("Enter API Key")
        self.api_key_input.setFixedWidth(190)
        self.api_key_input.setToolTip("Edit API Key")
        layout.addLayout(centered_widget(self.api_key_input, 190))

        self.save_api_key_button = QPushButton("Save API Key", self)
        self.save_api_key_button.setFixedWidth(190)
        self.save_api_key_button.setStyleSheet(api_key_button_style)
        self.save_api_key_button.clicked.connect(self.save_api_key)
        self.save_api_key_button.setToolTip("Save API Key")
        layout.addLayout(centered_widget(self.save_api_key_button,190))
        self.setLayout(layout)
    


    def update_character_count(self, count):
        self.char_count_label.setText(str(count))
        # Update cost calculation here if needed

    def collect_settings(self):
        settings = {
            'quality': 'HD' if self.toggle_switch.isChecked() else 'SD',
            'voice': self.voice_selection.currentText(),
            'format': self.other_options.currentText(),
            'char_count': self.char_count_label.text(),
            'cost': self.cost_label.text()
            # Add other settings if needed
        }
        return settings
    
    def load_config(self):
        # Load configuration from YAML file
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return {}
        
    def load_keys(self):
        # Read the API key from the config file
        config = self.load_config()
        api_key = config.get('api_key', '')  # Default to empty string if not found
        self.api_key_input.setText(api_key)
        license_key = config.get('license_key', '')
        self.license_key_input.setText(license_key)
    
    def update_config_api(self, api_key):
        # Load existing config
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        # Update the API key
        config['api_key'] = api_key

        # Save the updated config
        with open(config_path, 'w') as file:
            yaml.safe_dump(config, file)
    def update_config_license(self, api_key):
        # Load existing config
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        # Update the API key
        config['license_key'] = api_key

        # Save the updated config
        with open(config_path, 'w') as file:
            yaml.safe_dump(config, file)
    
    def save_api_key(self):
        api_key = self.api_key_input.text()
        self.update_config_api(api_key)
        self.apiKeyChanged.emit(True)
    def save_license_key(self):
        license_key = self.license_key_input.text()
        self.update_config_license(license_key)
    def apply_initial_theme(self):
        if self.theme == "dark":
            self.apply_theme_styles(dark_theme_style_sidebar)
        else:
            self.apply_theme_styles(light_theme_style_sidebar)
    def on_theme_changed(self, theme):
        if theme == "dark":
            self.apply_theme_styles(dark_theme_style_sidebar)
        else:
            self.apply_theme_styles(light_theme_style_sidebar)

    def apply_theme_styles(self, theme_styles):
        # Apply styles to each component based on the theme
        # self.dark_mode_toggle.setStyleSheet(theme_styles["toggle_switch"])
        self.theme_label.setStyleSheet(theme_styles["label"])
        self.save_api_key_button.setStyleSheet(theme_styles["api_button"])
        self.save_license_key_button.setStyleSheet(theme_styles["api_button"])""")
run_api_sidebar_ui = exec(base64.b64decode(api_sidebar_ui))