import glob
import os
import re
import getopt
import numpy as np
import png
import subprocess
import msvcrt
import sys


class Decoder():
    def exit(self):
        helpMsg = "\nUsage:\npython imagesDecodeScript.py <command> <path> <destinationPath>\n" \
                  "Commands:\n\t-mtx\tgenerates mtx files\n\t-midi\tgenerates midi files\n" \
                  "Path:\t path to image file, or folder with image files\n" \
                  "Destination Path:\t path to destination Folder, if not existing, will create."
        print(helpMsg)
        sys.exit(2)
    def __init__(self, argv):
        self.path = ''
        self.destPath = ''
        self.command = ''
        #test mode
        if len(argv) == 1:
            argv = ['imagesDecodeScript.py', '--midi', 'F:/EiTI Infa/Semestr 7/Inżynierka/Diploma/files/images/img4.png',
             'F:/EiTI Infa/Semestr 7/Inżynierka/Diploma/files/midiGenerated']
        try:
            opts, args = getopt.getopt(argv[1:], "hmt", ["midi","mtx"])
        except getopt.GetoptError:
            self.exit()
        for opt, arg in opts:
            if opt == '-h':
                self.exit()
            elif opt in ("-m", "--midi"):
                self.command = 'midi'
            elif opt in ("-t", "--mtx"):
                self.command = 'mtx'
        if(len(argv)!=4):
            print("Not enough arguments!\n")
            self.exit()
        self.path = args[0]
        self.destPath = args[1]
        self.isFolder = os.path.isdir(self.path)
        if not os.path.isdir(self.destPath):
            print("Destination Path: must be a directory!\n")
            self.exit()
        self.decode()

    def decode(self):
        # This script will decompress images 128x128 into mtx files, that will be lately transformed into midi files
        my_path = os.path.abspath(os.path.dirname(__file__))
        if self.isFolder:
            self.path = self.path + "\\*.png"
            fileNames = glob.glob(self.path)
        else:
            fileNames = [self.path]
        print("Images To Mtx Decompressing: " + str(len(fileNames)) + " files")

        fileCounter = 0
        quantization = 30
        length = 128
        width = 128

        for fn in fileNames:

            mtxFile = []
            mtxFile.append("MFile 1 1 120\n")
            mtxFile.append("MTrk\n")
            # print(os.path.basename(fn))
            fileCounter += 1
            progress = 100 * fileCounter / len(fileNames)
            sys.stdout.write("\r" + str(round(progress, 1)) + '%')

            reader = png.Reader(filename=fn)
            _, _, _, meta = reader.read_flat()
            if meta['alpha']:
                continue
            w, h, pixels, _ = png.Reader(filename=fn).asRGB()

            array = np.asarray(list(pixels))
            activeNotes = array[:, 0]*0

            for i in range(len(array[0,:])):
                newActiveNotes = array[:,i] #kolejny wiersz z nutami wdanym ticku
                for j in range(len(newActiveNotes)):
                    if newActiveNotes[j]>0 and activeNotes[j]==0:
                        # note just pressed
                        mtxFile.append(str(i*quantization) + " On ch=1 n=" + str(length-j-1) + " v=127\n")
                        activeNotes[j] = newActiveNotes[j]
                    elif newActiveNotes[j]==0 and activeNotes[j]>0:
                        mtxFile.append(str(i * quantization) + " On ch=1 n=" + str(length-j-1) + " v=0\n")
                        activeNotes[j] = newActiveNotes[j]
            mtxFile.append("TrkEnd\n")
            self.imageNumber = re.search('img(.*).png', os.path.basename(fn)).group(1)
            self.mtxName = os.path.join(self.destPath+"/file"+str(self.imageNumber)+".mtx")
            try:
                to_save = open(self.mtxName , "w")
            except FileNotFoundError:
                os.mkdir(self.destPath)
                to_save = open(self.mtxName , "w")
            to_save.writelines(mtxFile)
            if self.command == 'midi':
                self.convertToMidi()
    def convertToMidi(self):
        theproc = subprocess.Popen(["echo",  '' ,"|" ,"Mtx2Midi", os.path.basename(self.mtxName)], shell=True, cwd=self.destPath)
        print()
        print(theproc.communicate())


if __name__ == '__main__':
    import sys
    # python imagesDecodeScript.py --midi "F:/EiTI Infa/Semestr 7/Inżynierka/Diploma/files/images/img0.png" "F:/EiTI Infa/Semestr 7/Inżynierka/Diploma/files/midiGenerated"
    app = Decoder(sys.argv)
    sys.exit()


