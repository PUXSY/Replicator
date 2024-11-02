class Settings:
    
    def button_style(Dark_mode: bool) -> str:
        Dark_mode = False
        if Dark_mode == False:
            return """
            QPushButton {
                background-color: #17242e;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #263d4f;
            }
            QPushButton:pressed {
                background-color: #12202a;
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
        