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
    volume = int(lines[i].split()[4][2:])
    return currentTick,type,value,volume

def tickNormalize(tick):
    return int(tick/quantization)

def tickNormToPixel(tick):
    return (int(tick/3),tick%3)
def lenInTicks(lines):
   return int(int(lines[len(lines)-3].split()[0]))
def limit_notes_range(value):
    if value < 36:
        value += math.ceil((36-value)/12)*12
    elif 99 < value:
        value -= math.ceil((value - 99)/12)*12
    return  value - 36;

my_path = os.path.abspath(os.path.dirname(__file__))
fileName = os.path.join(my_path, "zlaczone_pliki_mtx\\zlaczone_pliki_mtx.mtx")
print("Tworzenie obrazów ze złączonych plików MTX: ")
lineCounter = 3

file = open(fileName, "r")
lines = file.readlines()

cut_file = []
savedFiles = 0

length = 64
width = tickNormToPixel(tickNormalize(lenInTicks(lines)))[0]+100
linesLen = len(lines) - 1

isSustained = False

activeNotes = [0] * length
holdNotes = [0] * width
img = np.zeros((length, width, 3), np.uint8)

prevTick = 0
for i in range(2, linesLen):
    if not lines[i].split()[1].startswith("Par"):
        prevTick = tickNormalize(int(lines[i].split()[0]))
        break
currentTick = 0
sustainCounter = 0
for i in range(2, linesLen):

    progress = 100 * lineCounter / linesLen
    sys.stdout.write("\r" + str(round(progress, 1)) + '%')
    if lines[i].startswith(("MTrk", "MFile", "TrkEnd")) or len(lines[i].split()) < 4:
        lineCounter += 1
        continue
    tempTick = currentTick
    (currentTick, type, value, volume) = loadLine(lines)
    value = limit_notes_range(value)
    currentTick = tickNormalize(currentTick)
    # Adding note to active notes - played at this moment
    if type == 1:  # On
        activeNotes[value] = volume
        prevTick = tempTick

    if type == 0:  # Par
        isSustained = volume > 0

    if sustainCounter > 300:
        sustainCounter = 0
        isSustained = 0

    # If sustain pedal is pressed, I add activeNotes to holdNotes
    if isSustained:
        sustainCounter += 1
        for j in range(len(activeNotes)):
            if activeNotes[j] > 0:
                holdNotes[j] = activeNotes[j]

    else:
        holdNotes = [0] * 128

    # setting values of midi notes to pixels. Coded on BGR values of pixels.
    # So first line will be on Blue value of first pixel, second on Green value of first and so on.

    prevColumn = img[:, tickNormToPixel(prevTick)[0], tickNormToPixel(prevTick)[1]]
    for tick in range(prevTick, currentTick):
        img[:, tickNormToPixel(tick)[0], tickNormToPixel(tick)[1]] = prevColumn
    for noteIndex in range(length):
        if activeNotes[noteIndex] > 0:
            img.itemset(length - noteIndex - 1, tickNormToPixel(currentTick)[0], tickNormToPixel(currentTick)[1], int(round(255 * activeNotes[noteIndex]/127)))
        else:
            img.itemset(length - noteIndex - 1, tickNormToPixel(currentTick)[0], tickNormToPixel(currentTick)[1], 0)
        if isSustained and holdNotes[noteIndex] > 0:
            img.itemset(length - noteIndex - 1, tickNormToPixel(currentTick)[0], tickNormToPixel(currentTick)[1], int(round(255 * holdNotes[noteIndex]/127)))

    lineCounter += 1

# saving last file, that might be uncompleted
name = os.path.join(my_path, "obrazy\\obraz")
path = os.path.join(my_path, "obrazy")
print("Zapisywanie obrazów:\n")
output_files_count = math.ceil(width/length)-1
os.mkdir(path)
for index in range(output_files_count):
    progress = 100 * index / output_files_count
    sys.stdout.write("\r" + str(round(progress, 1)) + '%')
    part = img[:,index*length:(index+1)*length,:]
    pngFile = open(name + str(index) + ".png", "wb")
    pngWriter = png.Writer(length,length)
    pngWriter.write(pngFile, np.reshape(part, (-1, length * 3)))
    pngFile.close()