from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout,\
    QComboBox, QLabel,  QFrame, QSpacerItem, QSizePolicy, QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from styles import dark_theme_style_sidebar, light_theme_style_sidebar
from toggle_switch import PyQtSwitch
import sys
import os
import yaml

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

class Sidebar(QWidget):
    def __init__(self, parent=None,theme="dark",stop_button=None,upload_button=None):
        super().__init__(parent)
        self.theme=theme
        self.stop_button=stop_button
        self.upload_button=upload_button
        self.initUI()
        self.apply_initial_theme()


    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        self.setFixedWidth(200)
        def centered_widget(widget, width=None):
            hbox = QHBoxLayout()
            hbox.addWidget(widget)
            hbox.setAlignment(Qt.AlignCenter)
            if width:
                widget.setFixedWidth(width)
            return hbox
        self.quality_label = QLabel("Quality:", self)
        self.quality_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.quality_label)
        # Fixed width container for the SD/HD toggle and labels
        toggle_container = QFrame(self)
        toggle_container_layout = QHBoxLayout(toggle_container)
        toggle_container_layout.setAlignment(Qt.AlignCenter)
        toggle_container.setFixedWidth(200)  # Adjust this width as needed

        # SD label
        sd_label = QLabel("SD", toggle_container)
        sd_label.setStyleSheet("font-weight: bold;")
        toggle_container_layout.addWidget(sd_label)

        # Toggle switch
        self.toggle_switch = PyQtSwitch()
        self.toggle_switch.setAnimation(True)
        self.toggle_switch.setToolTip("Toggle between SD and HD")
        toggle_container_layout.addWidget(self.toggle_switch)

        # HD label
        hd_label = QLabel("HD", toggle_container)
        hd_label.setStyleSheet("font-weight: bold;")
        toggle_container_layout.addWidget(hd_label)
        

        # Add the toggle container to the main sidebar layout
        layout.addWidget(toggle_container)

        
        # layout.addWidget(self.settings_button)

        self.voice_label = QLabel("Voice:", self)

        self.voice_label.setAlignment(Qt.AlignLeft)
        # quality_label.setStyleSheet(quality_label_style)
        layout.addWidget(self.voice_label)
        # Voice Selection Dropdown
        self.voice_selection = QComboBox(self)
        self.voice_selection.addItems(["alloy", "fable", "echo", "nova", "shimmer", "onyx"])
        self.voice_selection.setToolTip("Select a different voice")
        self.voice_selection.setFixedWidth(180)
        # self.voice_selection.setStyleSheet(dropdown_style)
        layout.addWidget(self.voice_selection)


        self.format_label = QLabel("Format:", self)
        self.format_label.setAlignment(Qt.AlignLeft)
        # quality_label.setStyleSheet(quality_label_style)
        layout.addWidget(self.format_label)
        # Additional Dropdown for Other Options
        self.other_options = QComboBox(self)
        self.other_options.addItems(["mp3", "opus", "aac", "flac"])
        self.other_options.setToolTip("Select a different format")
        self.other_options.setFixedWidth(180)
        # self.other_options.setStyleSheet(self.voice_selection.styleSheet())  # Same style as voice_selection
        layout.addWidget(self.other_options)

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        layout.addSpacerItem(spacer)

        # Character Count Card
        self.char_count_card = QWidget(self)
        # char_count_card.setStyleSheet(char_count_card_style)

        card_layout = QVBoxLayout(self.char_count_card)
        card_layout.setSpacing(0)
    
        card_layout.setContentsMargins(0, 0, 0, 0)
        self.char_count_card.setFixedSize(180, 140)
        self.char_count_card.setContentsMargins(0, 0, 0, 10)

        # Character count label
        self.char_count_label = QLabel("0", self.char_count_card)
        # self.char_count_label.setStyleSheet(char_count_label_style)
        image_label = QLabel(self)
        pixmap = QPixmap(imgs_path + '/speech-to-text_ls.png')  # Replace with your image path
        scaled_pixmap = pixmap.scaled(160, 160, Qt.KeepAspectRatio,Qt.SmoothTransformation)  # Adjust 100, 100 to your desired dimensions

        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)  # Center align the image

        layout.addWidget(image_label)
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(20)
        self.buttons_layout.setAlignment(Qt.AlignCenter)
        if self.stop_button:
            self.buttons_layout.addWidget(self.stop_button)
        if self.upload_button:
            self.buttons_layout.addWidget(self.upload_button)

        # self.settings_button = QPushButton("", self)
        
        self.settings_button = QPushButton('',self)  # Empty string because we're setting an icon, not text
        self.settings_button.setIcon(QIcon(imgs_path + '/gear_icon.png'))
        self.settings_button.setStyleSheet("QPushButton {background-color: #715FCF; /* Purple background */border-radius: 20px; /* Half of the width/height */border: none;}QPushButton:hover {background-color: #5e4bad; /* Slightly lighter purple for the hover state */}QPushButton:pressed {background-color: #4e3b8e; /* Slightly darker purple for the pressed state */}")
        self.settings_button.setIconSize(QSize(20, 20))  # Assuming the button size is 40x40
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.setToolTip("Settings")
        self.buttons_layout.addWidget(self.settings_button)
        self.buttons_layout.setContentsMargins(15, 15, 15, 15)
        layout.addLayout(self.buttons_layout)
        self.char_count_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.char_count_label)
        # spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # layout.addSpacerItem(spacer)

        # "Characters" label
        characters_label = QLabel("Characters", self.char_count_card)
        # characters_label.setStyleSheet(characters_label_style)
        characters_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(characters_label)

        # Cost label
        self.cost_label = QLabel("$0.0", self.char_count_card)

        self.cost_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.cost_label)
        card_layout.setContentsMargins(0, 0, 0, 0)  # Set all margins to zero
        card_layout.setSpacing(0)

        # Add character count card to layout
        layout.addLayout(centered_widget(self.char_count_card))

        # Add a spacer for layout management
        # spacer = QSpacerItem(10, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # layout.addSpacerItem(spacer)


        self.toggle_switch.toggled.connect(lambda: self.calculate_cost_internal())

        # Set the layout to the widget
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
    def calculate_cost(self,char_count):
        quality = 'HD' if self.toggle_switch.isChecked() else 'SD'
        model="tts-1-hd" if quality == "HD" else "tts-1"
        # Replace this with your actual cost calculation logic
        if model == "tts-1":
            cost_per_char = 0.000015  # Cost per character for SD
        elif model == "tts-1-hd":  # Assuming the only other option is HD
            cost_per_char = 0.000030  # Cost per character for HD
        total_cost = char_count * cost_per_char
        self.cost_label.setText(f"${total_cost:.4f}")
    def calculate_cost_internal(self):
        char_count = int(self.char_count_label.text())
        quality = 'HD' if self.toggle_switch.isChecked() else 'SD'
        model="tts-1-hd" if quality == "HD" else "tts-1"
        # Replace this with your actual cost calculation logic
        if model == "tts-1":
            cost_per_char = 0.000015  # Cost per character for SD
        elif model == "tts-1-hd":  # Assuming the only other option is HD
            cost_per_char = 0.000030  # Cost per character for HD
        total_cost = char_count * cost_per_char
        self.cost_label.setText(f"${total_cost:.4f}")
        


    def toggle_hd_sd(self, state):
        if state == Qt.Checked:
            print("Switched to HD")
        else:
            print("Switched to SD")
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
        self.voice_label.setStyleSheet(theme_styles["label"])
        self.quality_label.setStyleSheet(theme_styles["label"])
        self.format_label.setStyleSheet(theme_styles["label"])
        self.cost_label.setStyleSheet(theme_styles["cost_label"])
        # self.toggle_switch.setStyleSheet(theme_styles["toggle_switch"])
        self.char_count_card.setStyleSheet(theme_styles["char_card"])
        self.char_count_label.setStyleSheet(theme_styles["char_count"])