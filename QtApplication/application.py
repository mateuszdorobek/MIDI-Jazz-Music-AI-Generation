import os
import pygame

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Pause(object):

    def __init__(self):
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.set_volume(1.0)
        self.paused = pygame.mixer.music.get_busy()

    def toggle(self):
        if self.paused:
            pygame.mixer.music.set_volume(1.0)
            # pygame.mixer.music.unpause()
        if not self.paused:
            print("pause test")
            pygame.mixer.music.set_volume(0)
            # pygame.mixer.music.pause()
        self.paused = not self.paused

class Worker(QRunnable):

    @pyqtSlot()
    def run(self):
        print("run")
        my_path = os.path.abspath(os.path.dirname(__file__))
        #midiFilePath = self.getMidFromImg()
        midiFilePath = os.path.join(my_path, "..\\files\\midi\\afine-1.mid")
        self.play_music(midiFilePath)

    def play_music(self, music_file):
        print("play")
        try:
            pygame.mixer.music.load(os.path.abspath("..\\files\midi\A Remark You Made.mid"))
        except pygame.error:
            return
        pygame.mixer.music.play()

class Player(QWidget):
    def animation(self):


        # self.anim = QPropertyAnimation(self.frame, b"geometry")
        # self.anim.setDuration(10000)
        # self.anim.setStartValue(QRect(150, 30, 100, 100))
        # self.anim.setEndValue(QRect(150, 30, 200, 200))
        # self.anim.start()
        qp = QPainter()
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, 0, 30, 30)
        self.anim = QPropertyAnimation(self.frame, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setStartValue(qp.drawLine(0,0,30,30))
        self.anim.setEndValue( qp.drawLine(0,0,40,40))
        self.anim.start()

    def getMidFromImg(self,path):
        return " "

    def playMidiFile(self):
        self.worker = Worker()
        self.threadpool.start(self.worker)
        self.animation()

    def muteMusicToggle(self):
        print("paused: " + self.pause.paused)
        if self.pause.paused():
            self.slider.setValue(0)
        else:
            self.slider.setValue(100)
        self.pause.toggle()

    def stopMusic(self):
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()

    def volumeChanged(self):
        value = self.slider.value()/100.0
        pygame.mixer.music.set_volume(value)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "..\\files\\images\\img0.png")
        self.interface(path)

    def interface(self,path):
        self.pause = Pause()

        playButton = QPushButton("Play")
        muteButton = QPushButton("Mute/Unmute")
        stopButton = QPushButton("Stop")
        playButton.pressed.connect(lambda: self.playMidiFile())
        muteButton.pressed.connect(lambda: self.muteMusicToggle())
        stopButton.pressed.connect(lambda: self.stopMusic())

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(5)
        self.slider.setSingleStep(1)
        self.slider.setValue(70)
        self.slider.valueChanged.connect(lambda: self.volumeChanged())

        pixmap = QPixmap(path)
        self.label = QLabel()
        self.label.setPixmap(pixmap.scaled(3 * pixmap.height(), 3 * pixmap.width()))

        vButtonBox = QHBoxLayout()
        vButtonBox.addWidget(playButton)
        vButtonBox.addWidget(muteButton)
        vButtonBox.addWidget(stopButton)

        vBox = QVBoxLayout()
        vBox.addLayout(vButtonBox)
        vBox.addWidget(self.slider)

        hBox = QHBoxLayout()
        hBox.addWidget(self.label)
        hBox.addLayout(vBox)

        self.frame = QFrame(self)
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.frame.setGeometry(150, 30, 100, 100)

        self.setGeometry(130, 130, 800, 800)
        self.setWindowTitle('Animation')
        self.show()


        self.resize(800,400)
        self.setLayout(hBox)

        self.show()
    def koniec(self):
        self.close()

    def closeEvent(self, event):
        event.accept()
        # odp = QMessageBox.question( self,'Komunikat',"Czy na pewno koniec?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # if odp == QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Player()
    sys.exit(app.exec_())