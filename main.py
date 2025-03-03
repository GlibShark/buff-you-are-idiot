import sys
import random
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer
from pygame import mixer 
from concurrent.futures import ThreadPoolExecutor
import threading

class IdiotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_randomly)
        self.move_timer.start(30)  

    def initUI(self):
        self.setWindowTitle("YOU ARE AN IDIOT")
        label = QLabel(self)
        pixmap = QPixmap("idiot_image.png")  
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        screen_width = QApplication.primaryScreen().size().width()
        screen_height = QApplication.primaryScreen().size().height()
        self.move(random.randint(0, screen_width - self.width()),
                  random.randint(0, screen_height - self.height()))

    def move_randomly(self):
        screen_width = QApplication.primaryScreen().size().width()
        screen_height = QApplication.primaryScreen().size().height()
        x = self.x() + random.randint(-500, 500)
        y = self.y() + random.randint(-500, 500)
        x = max(0, min(x, screen_width - self.width()))
        y = max(0, min(y, screen_height - self.height()))
        self.move(x, y)

def play_music():
    mixer.init()
    mixer.music.load("music.mp3")
    mixer.music.play(-1)

def create_window():
    return IdiotWindow()

def main():
    app = QApplication(sys.argv)
    
    play_music()
    
    windows = []
    
    for _ in range(5):
        window = IdiotWindow()
        window.show()
        windows.append(window)
    
    executor = ThreadPoolExecutor(max_workers=10) 
    
    pending_windows = []

    def spawn_new_window():
        if pending_windows:
            window = pending_windows.pop(0)
            window.show()
            windows.append(window)
            if len(windows) > 1000:  
                old_window = windows.pop(0)
                old_window.close()
        
        future = executor.submit(create_window)
        pending_windows.append(future.result()) 
    
    spawn_timer = QTimer()
    spawn_timer.timeout.connect(spawn_new_window)
    spawn_timer.start(1)  
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()