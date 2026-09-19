import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
# imports

app = QApplication(sys.argv) # creating an application 
window = QWidget() # creating an window for the prgramm
window.setWindowTitle("Image") # setting the title 
pix_map = QPixmap("../images/Space_logo.png") # loading the image in 

# modifyed the picture
scaled_pixmap = pix_map.scaled(
    256, 256, # resized image creation
    Qt.AspectRatioMode.KeepAspectRatio # sets the image resize command to not resiable
)
image_label = QLabel()# area for the picture position
image_label.setPixmap(scaled_pixmap) # creating a pixmap area of the image


image_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # the positioning in the label so label_center == picure_center

tray = QVBoxLayout()# creates a trya for all the data
tray.addWidget(image_label)# passting the labbel into the tray
window.setLayout(tray)# locks in the image into possition and removes the tray

# 🎨 Match your custom teal window style!
window.setStyleSheet("background-color: #468E86;")

# 5. Bring it to the screen and loop!
window.show()
sys.exit(app.exec())