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
    def help(self):
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
            self.help()
        for opt, arg in opts:
            if opt == '-h':
                self.help()
            elif opt in ("-m", "--midi"):
                self.command = 'midi'
            elif opt in ("-t", "--mtx"):
                self.command = 'mtx'
        if(len(argv)!=4):
            print("Not enough arguments!\n")
            self.help()
        self.path = args[0]
        self.destPath = args[1]
        self.isFolder = os.path.isdir(self.path)
        if not os.path.isdir(self.destPath):
            print("Destination Path: must be a directory!\n")
            sys.exit(2)
        self.decode()


    def decode(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        if self.isFolder:
            self.path = self.path + "\\*.png"
            self.fileNames = glob.glob(self.path)
        else:
            self.fileNames = [self.path]
        print("Dekompresja " + str(len(self.fileNames)) + " obrazów")

        fileCounter = 0
        quantization = 30
        length = 64
        width = 64
        down_offset = 36

        for fn in self.fileNames:

            mtxFile = []
            mtxFile.append("MFile 1 1 120\n")
            mtxFile.append("MTrk\n")
            
            progress = 100 * fileCounter / len(self.fileNames)
            sys.stdout.write("\r" + str(round(progress, 1)) + '%')

            reader = png.Reader(filename=fn)
            _, _, _, meta = reader.read_flat()
            if meta['alpha']:
                continue
            w, h, pixels, _ = png.Reader(filename=fn).asRGB()
            array = np.asarray(list(pixels))
            activeNotes = array[:, 0]*0

            for i in range(len(array[0,:])):
                newActiveNotes = array[:,i]
                for j in range(len(newActiveNotes)):
                    if newActiveNotes[j]>0 and activeNotes[j]==0:
                        mtxFile.append(str(i*quantization) + " On ch=1 n=" + str(length-j-1+down_offset) + " v=127\n")
                        activeNotes[j] = newActiveNotes[j]
                    elif newActiveNotes[j]==0 and activeNotes[j]>0:
                        mtxFile.append(str(i * quantization) + " On ch=1 n=" + str(length-j-1+down_offset) + " v=0\n")
                        activeNotes[j] = newActiveNotes[j]
            mtxFile.append("TrkEnd\n")
            self.imageNumber = re.search('(.*).png', os.path.basename(fn)).group(1)
            self.mtxName = os.path.join(self.destPath+"/"+str(fileCounter)+".mtx")
            try:
                to_save = open(self.mtxName , "w")
            except FileNotFoundError:
                os.mkdir(self.destPath)
                to_save = open(self.mtxName , "w")
            to_save.writelines(mtxFile)
            
            fileCounter += 1
        if self.command == 'midi':
            self.convertToMidi()
    def convertToMidi(self):
        for fileCounter in range(len(self.fileNames)):
            mtxName = os.path.join(self.destPath+"/"+str(fileCounter)+".mtx")
            theproc = subprocess.Popen(["echo",  '' ,"|" ,"Mtx2Midi", os.path.basename(mtxName)], shell=True, cwd=self.destPath)
            #print(self.mtxName + "       " + self.destPath + "\n")
            print(theproc.communicate())

if __name__ == '__main__':
    import sys
    Decoder(sys.argv)
    #theproc = subprocess.Popen(["echo",  '' ,"|" ,"Mtx2Midi", os.path.basename("wygenerowane_pliki_midi/23.mtx")], shell=True, cwd="wygenerowane_pliki_midi")
    sys.exit()


