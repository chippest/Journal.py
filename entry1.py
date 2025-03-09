import sys
import keyboard  # Requires: pip install keyboard
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QPropertyAnimation

class DarkenedFullScreenWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darkened Full Screen Window")
        # Hide from the taskbar and remove the window frame
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        # Allow a transparent background so we can draw a custom dark overlay
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._closing = False

        # Start with zero opacity (invisible) for fade-in
        self.setWindowOpacity(0)

        # Create a centered text input
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Enter text...")
        self.text_input.setFixedWidth(300)
        self.text_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid gray;
                border-radius: 10px;
                padding: 5px;
                background: white;
            }
        """)

        # Create a close button ("X") at the top right
        self.close_button = QPushButton("X", self)
        self.close_button.setFixedSize(40, 40)
        self.close_button.clicked.connect(self.hideWithFade)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                border: none;
                border-radius: 20px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)

        # Set the window size to full screen (but do not show it yet)
        self.resize(QApplication.primaryScreen().size())

    def resizeEvent(self, event):
        # Center the text input
        self.text_input.move((self.width() - self.text_input.width()) // 2,
                               (self.height() - self.text_input.height()) // 2)
        # Position the close button in the top-right corner
        self.close_button.move(self.width() - self.close_button.width() - 20, 20)
        super().resizeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        # Fade in: animate window opacity from 0 to 1 over 300ms
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(300)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.start()

    def hideWithFade(self):
        if not self._closing:
            self._closing = True
            # Fade out: animate window opacity from current value to 0 over 300ms
            self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
            self.fade_anim.setDuration(300)
            self.fade_anim.setStartValue(self.windowOpacity())
            self.fade_anim.setEndValue(0)
            self.fade_anim.finished.connect(self.finalHide)
            self.fade_anim.start()

    def finalHide(self):
        self._closing = False
        self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        # Darken the background by painting a semi-transparent black overlay
        dark_color = QColor(0, 0, 0, 150)
        painter.fillRect(self.rect(), QBrush(dark_color))
        super().paintEvent(event)

def main():
    app = QApplication(sys.argv)
    window = DarkenedFullScreenWindow()

    # Register global hotkey: Ctrl+Alt+1. When pressed, show the window in full-screen mode.
    keyboard.add_hotkey('ctrl+alt+1', lambda: (window.showFullScreen(), window.show()))

    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
