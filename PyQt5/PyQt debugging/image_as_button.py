import sys
# 🎯 Swapped all 'PyQt6' calls to 'PyQt5' for macOS 12 protection
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("../images/Space_logo.png"))
window = QWidget()
window.resize(400, 400)

window.setStyleSheet("""
    QWidget {
        background-color: #468E86;   
    }
    QPushButton {
        background-color: #FF3333;  
        border-radius: 8px;         
        padding: 12px;         
        border: none;               
    }
    QPushButton:hover {
        background-color: #cc2929;  
    }
    QPushButton:pressed {
        background-color: #990000;  
    }
""")

button = QPushButton()
button.setIcon(QIcon("../images/Space_logo.png"))
button.setIconSize(QSize(256, 256))

tray = QVBoxLayout() 
tray.addWidget(button)
window.setLayout(tray)

window.show()
sys.exit(app.exec_()) # ⚠️ Note: PyQt5 uses exec_() with a trailing underscore!
