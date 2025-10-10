import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QGridLayout
 

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ilo calculator")
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.inputf = QLineEdit()
        self.buttonL = QGridLayout()
        self.createButtons()
        self.initUI()
    
    def initUI(self):
        self.setGeometry(100, 100, 300, 400)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

        # Set background color for the main window
        self.setStyleSheet("background-color: #f0f0f0;")

        self.inputf.setReadOnly(True)
        self.inputf.setStyleSheet("""
            QLineEdit {
                font-size: 24px;
                height: 60px;
                
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.layout.addWidget(self.inputf)
        self.layout.addLayout(self.buttonL)
        
    def createButtons(self):
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0), ('⌫', 4, 1), # Added backspace button
        ]
        
        for btn_text, row, col in buttons:
            button = QPushButton(btn_text)
            if btn_text in ['+', '-', '*', '/', '=']:
                # Operator buttons style
                button.setStyleSheet("""
                    QPushButton {
                        font-size: 18px;
                        height: 40px;
                        background-color: #ff9500;
                        color: white;
                        border-radius: 5px;
                    }
                    QPushButton:pressed {
                        background-color: #cc7700;
                    }
                """)
            elif btn_text in ['C', '⌫']:
                # Clear and backspace buttons style
                button.setStyleSheet("""
                    QPushButton {
                        font-size: 18px;
                        height: 40px;
                        background-color: #ff3b30;
                        color: white;
                        border-radius: 5px;
                    }
                    QPushButton:pressed {
                        background-color: #cc2f26;
                    }
                """)
            else:
                # Number buttons style
                button.setStyleSheet("""
                    QPushButton {
                        font-size: 18px;
                        height: 40px;
                        background-color: #e8e8e8;
                        border-radius: 5px;
                    }
                    QPushButton:pressed {
                        background-color: #d4d4d4;
                    }
                """)
            button.clicked.connect(lambda checked, text=btn_text: self.on_button_click(text))
            self.buttonL.addWidget(button, row, col)

    def on_button_click(self, text):
        if text == "C":
            self.inputf.setText("")
        elif text == "⌫":  # Handling backspace
            current_text = self.inputf.text()
            self.inputf.setText(current_text[:-1])
        elif text == "=":
            try:
                expression = self.inputf.text()
                result = str(eval(expression))
                self.inputf.setText(result)
            except Exception as e:
                self.inputf.setText("Error")
        else:
            self.inputf.setText(self.inputf.text() + text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())