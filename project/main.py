import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Photo Browser")
        self.resize(600, 500)
        
        # 1. Provide a list of image file paths located on your Mac
        # ⚠️ Replace these strings with real image paths from your computer!
        self.image_list = [
            "images/Space_logo.png",
            "images/hand.png",
            "images/drag.png"
        ]
        self.current_index = 0

        # 2. Create a QLabel to act as the visual display canvas
        self.image_display = QLabel("No images loaded yet.")
        self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Give the canvas a subtle background color via QSS to trace its boundaries
        self.image_display.setStyleSheet("background-color: #333333; border-radius: 8px;")

        # 3. Setup control buttons
        self.prev_btn = QPushButton("◀ Previous")
        self.next_btn = QPushButton("Next ▶")
        
        # Wire up click signals to navigation methods
        self.prev_btn.clicked.connect(self.show_previous_image)
        self.next_btn.clicked.connect(self.show_next_image)

        # 4. Assemble the layout trays
        button_tray = QHBoxLayout()
        button_tray.addWidget(self.prev_btn)
        button_tray.addWidget(self.next_btn)

        main_tray = QVBoxLayout()
        main_tray.addWidget(self.image_display, stretch=1) # The display consumes remaining space
        main_tray.addLayout(button_tray)
        main_tray.addStretch() # Ground the buttons tightly at the baseline
        
        self.setLayout(main_tray)
        self.setStyleSheet("QWidget { background-color: #468E86; }")

        # Load the initial image in the list
        self.update_displayed_image()

    def update_displayed_image(self):
        """Loads a file path into memory and updates the screen canvas."""
        if not self.image_list:
            return
            
        current_path = self.image_list[self.current_index]
        
        # Load the raw image file from storage into a pixel map container
        pixmap = QPixmap(current_path)
        
        if pixmap.isNull():
            self.image_display.setText(f"Failed to load image:\n{current_path}")
        else:
            # 🛠️ Scale down large assets dynamically so they match the canvas size constraints
            scaled_pixmap = pixmap.scaled(
                self.image_display.width() - 20, 
                self.image_display.height() - 20,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            # Render the picture directly into the text label container
            self.image_display.setPixmap(scaled_pixmap)

    def show_next_image(self):
        """Increments index loops smoothly back to zero."""
        if self.image_list:
            self.current_index = (self.current_index + 1) % len(self.image_list)
            self.update_displayed_image()

    def show_previous_image(self):
        """Decrements index securely loops backwards to end of list."""
        if self.image_list:
            self.current_index = (self.current_index - 1) % len(self.image_list)
            self.update_displayed_image()

    def resizeEvent(self, event):
        """Triggered automatically by macOS whenever window frames dynamically resize."""
        super().resizeEvent(event)
        self.update_displayed_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = ImageBrowser()
    browser.show()
    sys.exit(app.exec())
