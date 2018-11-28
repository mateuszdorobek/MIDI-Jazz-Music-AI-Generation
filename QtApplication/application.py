import os
import pygame

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Mute(object):

    def __init__(self):
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.set_volume(1.0)
        self.muted = pygame.mixer.music.get_busy()

    def toggle(self):
        if self.muted:
            pygame.mixer.music.set_volume(1.0)
            # pygame.mixer.music.unpause()
        if not self.muted:
            print("pause test")
            pygame.mixer.music.set_volume(0)
            # pygame.mixer.music.pause()
        self.muted = not self.muted
        return self.muted

class Worker(QRunnable):

    @pyqtSlot()
    def run(self):
        print("run")
        my_path = os.path.abspath(os.path.dirname(__file__))
        #midiFilePath = self.getMidFromImg()
        midiFilePath = os.path.join(my_path, "..\\files\\midi\\afine-1.mid")
        self.play_music(midiFilePath)

    def play_music(self, music_file):
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
        self.stopButton.setDisabled(False)
        self.playButton.setDisabled(True)
        # self.animation()

    def muteMusicToggle(self):

        if self.mute.toggle():
            self.lastVolume = self.slider.value()
            self.slider.setValue(0)
        else:
            self.slider.setValue(self.lastVolume)

    def stopMusic(self):
        self.stopButton.setDisabled(True)
        self.playButton.setDisabled(False)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()

    def volumeChanged(self):
        value = self.slider.value()/100.0
        pygame.mixer.music.set_volume(value)
        if value > 0:
            self.mute.muted = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mute = Mute()
        self.threadpool = QThreadPool()

        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "..\\files\\images\\img0.png")
        self.interface(path)

    def interface(self,path):

        self.muteButton = QPushButton("Mute/Unmute")
        self.playButton = QPushButton("Play")
        self.stopButton = QPushButton("Stop")

        self.playButton.pressed.connect(lambda: self.playMidiFile())
        self.muteButton.pressed.connect(lambda: self.muteMusicToggle())
        self.stopButton.pressed.connect(lambda: self.stopMusic())
        self.stopButton.setDisabled(True)

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
        vButtonBox.addWidget(self.playButton)
        vButtonBox.addWidget(self.muteButton)
        vButtonBox.addWidget(self.stopButton)

        vBox = QVBoxLayout()
        vBox.addLayout(vButtonBox)
        vBox.addWidget(self.slider)

        hBox = QHBoxLayout()
        hBox.addWidget(self.label)
        hBox.addLayout(vBox)



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