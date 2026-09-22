import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout # 🎯 Added QPushButton here

app = QApplication(sys.argv)
window = QWidget()

button = QPushButton("Click me")
def say_hi():
    print("Hello I am verity")
button.clicked.connect(say_hi)


tray = QVBoxLayout()
tray.addWidget(button)
window.setLayout(tray)

window.show()
sys.exit(app.exec())