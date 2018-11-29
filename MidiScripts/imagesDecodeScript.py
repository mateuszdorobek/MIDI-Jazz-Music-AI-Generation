import glob
import os
import re
import getopt
import numpy as np
import png

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
        self.isFolder = os.path.isdir(path)
        if not os.path.isdir(self.destPath):
            print("Destination Path: must be a directory!\n")
            self.exit()

    def decode(self):
        # This script will decompress images 128x128 into mtx files, that will be lately transformed into midi files
        my_path = os.path.abspath(os.path.dirname(__file__))
        if self.isFolder:
            self.path = os.path.join(self.path, "\\*.png")
            fileNames = glob.glob(self.path)
        else:
            fileNames = [self.path]
        print("Images To Mtx Decompressing: " + str(len(fileNames)) + " files")
        # TODO: zrobić wczytywanie dla wielu plików
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

            w, h, pixels, meta = png.Reader(filename=fn).asRGB()

            array = np.asarray(list(pixels))
            # array = pixels
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
            path = os.path.join(my_path, "..\\files\\mtxOutput\\mtx")
            imageNumber = re.search('img(.*).png', os.path.basename(fn)).group(1)
            name = os.path.join(path+str(imageNumber)+".mtx")
            try:
                to_save = open(name, "w")
            except FileNotFoundError:
                os.mkdir(    os.path.join(my_path, "..\\files\\mtxOutput\\"))
                to_save = open(name, "w")
            to_save.writelines(mtxFile)

if __name__ == '__main__':
    import sys
    app = Decoder(sys.argv)
    sys.exit()
    # python imagesDecodeScript.py --midi "F:/EiTI Infa/Semestr 7/Inżynierka/Diploma/filec/images/img0.png" "F:/EiTI Infa/Semestr 7/Inżynierka/Diploma/files/midiGenerated"