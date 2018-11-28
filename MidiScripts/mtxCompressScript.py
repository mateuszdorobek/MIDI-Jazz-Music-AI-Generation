import os
import sys
import numpy as np
import png
import math

quantization = 30
# This script will compress big data file with merged midi files into pictures and split it into 128x128 batches
def loadLine(lines):
    currentTick = int(int(lines[i].split()[0]))  # 0,1,2,3 etc.
    type = 0 if lines[i].split()[1].startswith("Par") else 1  # Par 0,    On 1
    value = int((lines[i].split()[3])[2:])  # c=64 64,  n=25 25   ...
    volume = False if int(lines[i].split()[4][2:]) == 0 else True  # v=0 0,    v=127 1
    return currentTick,type,value,volume

def tickNormalize(tick):
    return int(tick/quantization)

def tickNormToPixel(tick):
    return (int(tick/3),tick%3)
def lenInTicks(lines):
   return int(int(lines[len(lines)-3].split()[0]))

my_path = os.path.abspath(os.path.dirname(__file__))
fileName = os.path.join(my_path, "..\\files\\mtxMerged\\data.mtx")
print("Mtx Files Compressing: ")
lineCounter = 3

file = open(fileName, "r")
lines = file.readlines()

cut_file = []
savedFiles = 0

length = 128
width = tickNormToPixel(tickNormalize(lenInTicks(lines)))[0]+100

isSustained = False

activeNotes = [False] * length
holdNotes = [False] * width
img = np.zeros((length, width, 3), np.uint8)

prevTick = 0
for i in range(2, len(lines) - 1):
    if not lines[i].split()[1].startswith("Par"):
        prevTick = tickNormalize(int(lines[i].split()[0]))
        break
currentTick = 0
for i in range(2, len(lines) - 1):

    progress = 100 * lineCounter / len(lines)
    sys.stdout.write("\r" + str(round(progress, 1)) + '%')
    if lines[i].startswith(("MTrk", "MFile", "TrkEnd")) or len(lines[i].split()) < 4:
        lineCounter += 1
        continue
    tempTick = currentTick
    (currentTick, type, value, volume) = loadLine(lines)

    currentTick = tickNormalize(currentTick)
    # Adding note to active notes - played at this moment
    if type == 1:  # On
        activeNotes[value] = volume
        prevTick = tempTick

    if type == 0:  # Par
        isSustained = volume
    # If sustain pedal is pressed, I add activeNotes to holdNotes
    if isSustained:
        for j in range(len(activeNotes)):
            if activeNotes[j]:
                holdNotes[j] = True
    else:
        holdNotes = [False] * 128

    # setting values of midi notes to pixels. Coded on BGR values of pixels.
    # So first line will be on Blue value of first pixel, second on Green value of first and so on.

    prevColumn = img[:, tickNormToPixel(prevTick)[0], tickNormToPixel(prevTick)[1]]
    for tick in range(prevTick, currentTick):
        img[:, tickNormToPixel(tick)[0], tickNormToPixel(tick)[1]] = prevColumn
    for noteIndex in range(length):
        if activeNotes[noteIndex]:
            img.itemset(length - noteIndex - 1, tickNormToPixel(currentTick)[0],tickNormToPixel(currentTick)[1], 255)
        else:
            img.itemset(length - noteIndex - 1, tickNormToPixel(currentTick)[0],tickNormToPixel(currentTick)[1], 0)
        if isSustained and holdNotes[noteIndex]:
            img.itemset(length - noteIndex - 1, tickNormToPixel(currentTick)[0], tickNormToPixel(currentTick)[1], 255)

    lineCounter += 1

# saving last file, that might be uncompleted
name = os.path.join(my_path, "..\\files\\images\\img")
for index in range(math.ceil(width/128)):
    progress = 100 * index / math.ceil(width/128)
    sys.stdout.write("\r" + str(round(progress, 1)) + '%')
    part = img[:,index*128:(index+1)*128,:]
    if part.shape[1]<128:
        break
    pngFile = open(name + str(index) + ".png", "wb")
    pngWriter = png.Writer(128,128)
    pngWriter.write(pngFile, np.reshape(part, (-1, 128 * 3)))
    pngFile.close()