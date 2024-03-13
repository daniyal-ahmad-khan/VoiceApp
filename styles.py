dark_theme_style_sidebar = {
                            "label": """
                            QLabel {
                                    color: #715FCF;        /* Set the text color to purple */
                                    font-size: 20px;    /* Optional: Adjust font size as needed */
                                    padding-bottom: 2px;
                            }
                            """,
                            "cost_label": """
                            QLabel {
                                font-size: 10px;  /* Large font size */
                                font-weight: bold; /* Bold font weight */
                                color: #00FFA0; /* Custom text color */
                                padding-top: 10px;
                            }
                        """,
                        "button": """
                                            QPushButton {
                                                background-color: #715FCF; /* Purple background */
                                                color: #0f0f0f;
                                                border-radius: 20px;
                                                padding: 15px 15px;
                                                margin-top: 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: #8a7ac3; /* Lighter purple for hover */
                                            }
                                            QPushButton:pressed {
                                                background-color: #5e4b99; /* Darker purple for pressed */
                                            }

                                        """,
                        "toggle_switch": """
                                            QCheckBox {
                                                background-color: rgb(113, 95, 207); /* Purple background */
                                                border-radius: 13px;
                                                border: 2px solid #8a7ac3; /* Lighter purple border */
                                                width: 26px; height: 26px;
                                            }
                                            QCheckBox::indicator {
                                                background: transparent;
                                                width: 26px;
                                                height: 26px;
                                                background: #5e4b99; /* Darker purple when unchecked */
                                                border-radius: 13px;
                                                margin: 2;
                                            }
                                            QCheckBox::indicator:checked {
                                                left: 30px;
                                                background: rgb(113, 95, 207); /* Purple when checked */
                                            }
                                        """,
                        "char_card": """
                                        QWidget {
                                            background-color: #333333;  /* Dark gray background */
                                            border-radius: 15px;        /* Rounded corners */
                                            padding: 0px;               /* No padding inside the card */
                                        }
                                    """,
                        "char_count": """
                                        QLabel {
                                            color: #715FCF;        /* Set the text color to purple */
                                            font-size: 64px;  /* Large font size */
                                            font-weight: bold; /* Bold font weight */
                                            margin: 0;         /* No margin */
                                            padding: 0;        /* No padding */
                                        }
                                     """,
                        "api_button": """
                                            QPushButton {
                                                background-color: #715FCF; /* Purple background */
                                                color: #0f0f0f;
                                                border-radius: 10px;
                                                padding: 5px 5px;
                                                margin-top: 2px;
                                            }
                                            QPushButton:hover {
                                                background-color: #8a7ac3; /* Lighter purple for hover */
                                            }
                                            QPushButton:pressed {
                                                background-color: #5e4b99; /* Darker purple for pressed */
                                            }

                                        """,
                        "edit_text": """
                                QTextEdit {
                                    color: #ffffff; 
                                    background-color: #333333; 
                                    border: 1px solid #333333;
                                    margin-bottom: 10px;
                                }
                            """
                        
                            
                            }
light_theme_style_sidebar = {
                            "label": """
                            QLabel {
                                    color: #715FCF;        /* Set the text color to purple */
                                    font-size: 20px;    /* Optional: Adjust font size as needed */
                                    padding-bottom: 2px;
                            }
                            """,
                            "cost_label": """
                            QLabel {
                                font-size: 10px;  /* Large font size */
                                font-weight: bold; /* Bold font weight */
                                color: #00FFA0; /* Custom text color */
                                padding-top: 10px;
                            }
                        """,
                        "button": """
                                            QPushButton {
                                                background-color: #715FCF; /* Purple background */
                                                color: #ffffff;
                                                border-radius: 20px;
                                                padding: 15px 15px;
                                                margin-top: 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: #8a7ac3; /* Lighter purple for hover */
                                            }
                                            QPushButton:pressed {
                                                background-color: #5e4b99; /* Darker purple for pressed */
                                            }

                                        """,
                        "toggle_switch": """
                                        """,
                        "char_card": """
                                        QWidget {
                                            background-color: #ededed;  /* Dark gray background */
                                            border-radius: 15px;        /* Rounded corners */
                                            padding: 0px;               /* No padding inside the card */
                                        }
                                     """,
                        "char_count": """
                                        QLabel {
                                            color: #715FCF;        /* Set the text color to purple */
                                            font-size: 64px;  /* Large font size */
                                            font-weight: bold; /* Bold font weight */
                                            margin: 0;         /* No margin */
                                            padding: 0;        /* No padding */
                                        }
                                     """,
                        "api_button": """
                                            QPushButton {
                                                background-color: #715FCF; /* Purple background */
                                                color: #ffffff;
                                                border-radius: 10px;
                                                padding: 5px 5px;
                                                margin-top: 2px;
                                            }
                                            QPushButton:hover {
                                                background-color: #8a7ac3; /* Lighter purple for hover */
                                            }
                                            QPushButton:pressed {
                                                background-color: #5e4b99; /* Darker purple for pressed */
                                            }

                                        """,
                        "edit_text": """
                                QTextEdit {
                                    color: #4a4948; 
                                    background-color: #ededed; 
                                    border: 1px solid #ededed;
                                    margin-bottom: 10px;
                                }
                            """
                        

                        }
                    

api_key_button_style = """
            QPushButton {
                background-color: #0077b6;
                color: #ffffff;
                border-radius: 10px;
                padding: 5px 5px;
                margin-top: 3px;
            }
            QPushButton:hover {
                background-color: #0096c7;
            }
            QPushButton:pressed {
                background-color: #023e8a;
            }
        """