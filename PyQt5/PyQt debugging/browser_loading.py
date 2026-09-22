import sys
# Core UI components and web engines pulled entirely from PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtCore import QUrl, QSize

class SpaceCommandStation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hacker Space Command Station 🌌")
        self.resize(1100, 800) # Crisp wide aspect resolution frame

        # 1. CREATE BUTTON 1: Link to your live Carrd Portfolio site
        self.btn_carrd = QPushButton("Mission Blueprint 🛸")
        self.btn_carrd.setObjectName("NavButton")
        self.btn_carrd.clicked.connect(self.load_carrd_site)

        # 2. CREATE BUTTON 2: Link to an integrated live weather radar/display
        self.btn_weather = QPushButton("Weather Grid 📡")
        self.btn_weather.setObjectName("NavButton")
        self.btn_weather.clicked.connect(self.load_weather_site)

        # 3. THE EMBEDDED VIEWPORT: The Google Chromium web engine frame
        self.browser_viewport = QWebEngineView()

        # 4. ASSEMBLE THE TOP CONTROL BUTTON ROW (Horizontal Alignment Tray)
        button_row = QHBoxLayout()
        button_row.setSpacing(15) # Perfect gaps between the navigation triggers
        button_row.addWidget(self.btn_carrd)
        button_row.addWidget(self.btn_weather)
        button_row.addStretch() # Pushes both buttons nicely to the top left side

        # 5. ASSEMBLE THE MASTER COLUMN CONTAINER (Vertical Alignment Tray)
        master_tray = QVBoxLayout()
        master_tray.addLayout(button_row) # Control buttons sit on the top row
        
        # Adding stretch factor '1' forces the browser window to fill the rest of the canvas
        master_tray.addWidget(self.browser_viewport, 1) 
        
        self.setLayout(master_tray)

        # Fire up your personal Carrd landing site automatically on application boot
        self.load_carrd_site()

        # 🎨 MASTER APP STYLING SHEET (QSS Configuration)
        self.setStyleSheet("""
            QWidget {
                background-color: #468E86;       /* Your custom Teal background */
            }
            
            /* 1. NORMAL BUTTON CONFIGURATION */
            QPushButton#NavButton {
                background-color: #FF3333;       /* Your custom Vibrant Red background */
                color: #ffffff;                  /* Crisp white text font */
                font-family: 'Courier New', monospace;
                font-size: 14px;                 
                font-weight: bold;               
                border-radius: 6px;              /* Clean rounded corners */
                padding: 10px 20px;              /* Internal button breathing room */
                border: none;                    /* Strips default OS frames */
            }
            
            /* 2. HOVER EFFECT (Mouse resting over the target button) */
            QPushButton#NavButton:hover {
                background-color: #cc2929;       /* Smooth medium red color shift */
            }
            
            /* 3. CLICKED PRESSED EFFECT (Active click mouse animation) */
            QPushButton#NavButton:pressed {
                background-color: #990000;       /* Deep wine red flash */
            }
        """)

    # 💥 SLOT FUNCTION 1: Overwrites view destination to your live Carrd site
    def load_carrd_site(self):
        print("Routing to Mission Blueprint... 🛰️")
        self.browser_viewport.setUrl(QUrl("https://spaceclock.carrd.co/"))

    # 💥 SLOT FUNCTION 2: Overwrites view destination to your live weather tracker
    def load_weather_site(self):
        print("Routing to Atmospheric Weather Grid... ⛈️")
        # We can link this to open an interactive live open-source weather canvas view!
        self.browser_viewport.setUrl(QUrl("https://wttr.in"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpaceCommandStation()
    window.show()
    sys.exit(app.exec_()) # Secure PyQt5 environment loop closure
