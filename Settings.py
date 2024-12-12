class Settings:
    
    def button_style(Dark_mode: bool) -> str:
        Dark_mode = False
        if Dark_mode == False:
            return """
            QPushButton {
                background-color: #ea560a;
                color: #0b0907;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff6b1c;
            }
        """
        else:
            return """
            QPushButton {
                background-color: #ea560a;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #fc6a20;
            }
            QPushButton:pressed {
                background-color: #d64c05;
            }
        """
        