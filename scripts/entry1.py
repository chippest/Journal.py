import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton
)
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QPropertyAnimation

class DarkenedFullScreenWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darkened Full Screen Window")
        # Remove window frame, set as tool to hide from taskbar, and enable transparency
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._closing = False

        # Start with 0 opacity for the fade-in effect
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
        self.close_button.clicked.connect(self.close)
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

        # Set full screen after widgets are created
        self.showFullScreen()

    def resizeEvent(self, event):
        # Center the text input
        self.text_input.move((self.width() - self.text_input.width()) // 2,
                               (self.height() - self.text_input.height()) // 2)
        # Position the close button at top right
        self.close_button.move(self.width() - self.close_button.width() - 20, 20)
        super().resizeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        # Fade in: transition opacity from 0 to 1 over 300ms
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(300)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.start()

    def closeEvent(self, event):
        if not self._closing:
            self._closing = True
            # Fade out: transition opacity from current value to 0 over 300ms
            self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
            self.fade_anim.setDuration(300)
            self.fade_anim.setStartValue(self.windowOpacity())
            self.fade_anim.setEndValue(0)
            self.fade_anim.finished.connect(self.finalClose)
            self.fade_anim.start()
            event.ignore()
        else:
            event.accept()

    def finalClose(self):
        self.hide()
        super().close()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Instead of a blurred background, we darken the background
        # Here we use a semi-transparent black overlay
        dark_color = QColor(0, 0, 0, 150)
        painter.fillRect(self.rect(), QBrush(dark_color))
        super().paintEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DarkenedFullScreenWindow()
    window.show()
    sys.exit(app.exec_())
