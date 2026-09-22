import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class SliderTerminal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matrix Brightness Control 📡")
        self.resize(400, 200)

        # 1. Create a display label to show the current slider value
        self.value_label = QLabel("Brightness Level: 128")
        self.value_label.setAlignment(Qt.AlignCenter)

        # 2. 🎯 CREATE THE SLIDER BAR
        self.slider = QSlider(Qt.Horizontal) # Forces a horizontal layout slide line
        self.slider.setRange(0, 255)         # Perfect range for standard RGB color scales!
        self.slider.setValue(128)            # Start the handle dead-center at 128 on startup

        # WIRE IT UP: Every single time the handle moves, fire our update function!
        self.slider.valueChanged.connect(self.handle_slider_movement)

        # 3. Assemble the vertical layout tray stack
        tray = QVBoxLayout()
        tray.setSpacing(20)
        tray.addWidget(self.value_label)
        tray.addWidget(self.slider)         # Drops the slider bar directly below the text
        tray.addStretch()
        self.setLayout(tray)

        # 🎨 Master Theme Styling Sheet (QSS)
        self.setStyleSheet("""
            QWidget {
                background-color: #468E86;   /* Your custom Teal background */
                color: #ffffff;
                font-family: 'Courier New', monospace;
                font-size: 16px;
                font-weight: bold;
            }
            /* Style the sliding handle and groove line dynamically! */
            QSlider::groove:horizontal {
                border: 1px solid #2d5c57;
                height: 10px;
                background: #ffffff;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #FF3333;         /* Your custom Vibrant Red handle! */
                border: none;
                width: 20px;
                height: 20px;
                margin: -5px 0;              /* Centers the handle over the groove line */
                border-radius: 10px;         /* Makes the handle perfectly round */
            }
            QSlider::handle:horizontal:hover {
                background: #cc2929;         /* Darkens the red slightly when hovering */
            }
        """)

    def handle_slider_movement(self):
        """Triggers instantly when dragged. Grabs the new position and updates screen."""
        # 🎯 READ THE SLIDER FACTOR POSITION HERE!
        current_position = self.slider.value()
        
        # Rewrite the display text on the fly
        self.value_label.setText(f"Brightness Level: {current_position}")
        print(f"Matrix voltage signal dialed to: {current_position}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SliderTerminal()
    window.show()
    sys.exit(app.exec_())
