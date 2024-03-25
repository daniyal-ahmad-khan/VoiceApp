from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap
import os
import sys
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Use these paths in your application
config_path = resource_path('config.yaml')
imgs_path = resource_path('imgs/')

class TutorialSlideshow(QDialog):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.setWindowTitle("Tutorial")
        self.main_window = main_window
        self.current_step = 0  # Start with the first step
        self.initUI()
        self.steps = [
            self.highlightSettingsButton, 
            self.highlightLicenseKeyField, 
            self.highlightSaveLicenseKeyButton,
            self.highlightAPIKeyField, 
            self.highlightSaveAPIKeyButton
        ]
        self.nextStep()  # Automatically start with the first step

    def initUI(self):
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.layout.addWidget(self.label)

        buttonsLayout = QHBoxLayout()  # Layout to hold both buttons
        
        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(self.nextStep)
        self.nextButton.setFixedSize(100, 40)
        buttonsLayout.addWidget(self.nextButton)
        
        self.skipButton = QPushButton("Skip")
        self.skipButton.clicked.connect(self.closeTutorial)
        self.skipButton.setFixedSize(100, 40)
        buttonsLayout.addWidget(self.skipButton)
        
        self.layout.addLayout(buttonsLayout)
        self.setLayout(self.layout)
        self.setMinimumSize(400, 100)

    def nextStep(self):
        if self.current_step < len(self.steps):
            self.steps[self.current_step]()
            self.current_step += 1
        else:
            self.closeTutorial()

    def greetUser(self):
        self.label.setText("Thank you for choosing our app.")
    def closeTutorial(self):
        self.highlightNone()  # Ensure all highlights are removed
        self.close()
    def highlightSettingsButton(self):
        # Define the size you want for your icon
        icon_width = 32
        icon_height = 32
        
        # Path to your settings icon
        settings_icon_path = resource_path(imgs_path + 'gear_icon.png')
        
        # Set the QLabel to display text and icon with specified icon size
        # Using HTML to format text and include the icon with specified dimensions
        self.label.setText('Press the "Settings" <img src="{}" width="{}" height="{}"> button to open settings.'.format(settings_icon_path, icon_width, icon_height))
        
        self.label.setTextFormat(Qt.RichText)
        
        # Apply highlighting effect to the settings button if needed
        self.applyHighlight(self.main_window.sidebar.settings_button)

    def highlightLicenseKeyField(self):
        self.main_window.toggle_api_sidebar(True)
        self.label.setText("Enter your license key here.")
        self.highlightNone()
        self.applyHighlight(self.main_window.api_sidebar.license_key_input)

    def highlightAPIKeyField(self):
        self.label.setText("Now, enter your API key here.")
        self.highlightNone()
        self.applyHighlight(self.main_window.api_sidebar.api_key_input)

    def highlightSaveLicenseKeyButton(self):
        self.label.setText("After entering your license key, press this button to save it.")
        self.highlightNone()
        self.applyHighlight(self.main_window.api_sidebar.save_license_key_button)

    def highlightSaveAPIKeyButton(self):
        self.label.setText("After entering your API key, press this button to save it.")
        self.highlightNone()
        self.applyHighlight(self.main_window.api_sidebar.save_api_key_button)
    def applyHighlight(self, widget):
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(20)
        effect.setColor(QColor('red'))
        effect.setOffset(0)
        widget.setGraphicsEffect(effect)
    

    def highlightNone(self):
        # Reset any highlights if needed
        self.main_window.sidebar.settings_button.setGraphicsEffect(None)
        self.main_window.api_sidebar.license_key_input.setGraphicsEffect(None)
        self.main_window.api_sidebar.api_key_input.setGraphicsEffect(None)
        self.main_window.api_sidebar.save_license_key_button.setGraphicsEffect(None)
        self.main_window.api_sidebar.save_api_key_button.setGraphicsEffect(None)
