import os
import pygame
import MidiScripts.imagesDecodeScript as Img2Midi

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
        self.play_music()
    def setMidiPath(self,midiFilePath):
        self.midiFilePath = midiFilePath

    def play_music(self):
        try:
            pygame.mixer.music.load(os.path.abspath(self.midiFilePath))
        except pygame.error:
            return
        pygame.mixer.music.play()

class Player(QWidget):
    def animation(self):
        qp = QPainter()
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, 0, 30, 30)
        self.anim = QPropertyAnimation(self.frame, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setStartValue(qp.drawLine(0,0,30,30))
        self.anim.setEndValue( qp.drawLine(0,0,40,40))
        self.anim.start()

    def playMidiFile(self):
        self.worker = Worker()
        self.worker.setMidiPath(self.midiFilePath)
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
    def openFileDialog(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        imgFilePath = os.path.join(my_path, "..\\files\\images")
        fileName = QFileDialog.getOpenFileName(self, 'Open File', imgFilePath)
        if fileName[0]:
            self.stopMusic()
            self.textLine.setText(os.path.basename(fileName[0]))
            pixmap = QPixmap(fileName[0])
            self.label.setPixmap(pixmap.scaled(3 * pixmap.height(), 3 * pixmap.width()))
            self.convertImageToMidi(fileName[0])
            self.midiFilePath = (str(fileName[0])[:-3]+"mid").replace("images","midiGenerated").replace("img","file")
            self.playButton.setDisabled(False)

    def convertImageToMidi(self, fileName):
        destinationDir = "F:\\EiTI Infa\\Semestr 7\\Inżynierka\\Diploma\\files\\midiGenerated"
        argvec = ['imageDecodeScript.py','--midi', fileName, destinationDir]
        Img2Midi.Decoder(argvec)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mute = Mute()
        self.threadpool = QThreadPool()
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "..\\files\\images\\img0.png")
        self.interface()

    def interface(self):

        self.muteButton = QPushButton("Mute/Unmute")
        self.playButton = QPushButton("Play")
        self.stopButton = QPushButton("Stop")
        self.fileButton = QPushButton("Choose File")
        self.textLine = QLineEdit(self)

        self.volumeLabel = QLabel("       Volume:     ")
        self.volumeLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.volumeLabel.setAlignment(Qt.AlignCenter)

        self.playButton.pressed.connect(lambda: self.playMidiFile())
        self.muteButton.pressed.connect(lambda: self.muteMusicToggle())
        self.stopButton.pressed.connect(lambda: self.stopMusic())
        self.stopButton.setDisabled(True)
        self.playButton.setDisabled(True)
        self.fileButton.pressed.connect(lambda: self.openFileDialog())

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(5)
        self.slider.setSingleStep(1)
        self.slider.setValue(70)
        self.slider.valueChanged.connect(lambda: self.volumeChanged())

        self.label = QLabel()
        self.label.setPixmap(QPixmap(128*3,128*3))

        vBox = QVBoxLayout()

        vButtonBox = QHBoxLayout()
        vButtonBox.addWidget(self.playButton)
        vButtonBox.addWidget(self.muteButton)
        vButtonBox.addWidget(self.stopButton)
        vBox.addLayout(vButtonBox)


        hBox = QHBoxLayout()
        hBox.addWidget(self.volumeLabel)
        hBox.addWidget(self.slider)
        vBox.addLayout(hBox)

        vButtonBox = QHBoxLayout()
        vButtonBox.addWidget(self.textLine)
        vButtonBox.addWidget(self.fileButton)
        vBox.addLayout(vButtonBox)

        hBox = QHBoxLayout()
        hBox.addWidget(self.label)
        hBox.addLayout(vBox)

        self.setWindowTitle('MIDI Player')
        self.resize(800,400)
        self.setLayout(hBox)

        self.show()
    def clearMidiFolder(self):
        folder = "F:\EiTI Infa\Semestr 7\Inżynierka\Diploma\\files\midiGenerated"
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
    def closeEvent(self, event):
        odp = QMessageBox.question( self,'Komunikat',"Czy chcesz usunąć wygenerowane pliki midi?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if odp == QMessageBox.Yes:
            self.clearMidiFolder()
        event.accept()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Player()
    sys.exit(app.exec_())
