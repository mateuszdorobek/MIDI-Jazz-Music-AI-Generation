import glob
import os
import sys

# This script will clear mtx files from unnecessary data in way
# that they can still be transformed back to mid files without
# any distortion to musical content.
# I'm only extruding only piano tracks, and merging it onto one channel

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "..\\files\\mtx\\*.mtx")
fileNames = glob.glob(path)
print("Mtx Files Clearing: " + str(len(fileNames)) + " files")
fileCounter = 1

# Looking for the biggest block MTrk - TrkEnd,
# which should be music block with piano track ( bass and drums are typically shorter)
for fn in fileNames:
    progress = 100 * fileCounter / len(fileNames)
    sys.stdout.write("\r" + str(round(progress, 1)) + '%')

    f = open(fn, "r")
    start = 0
    max_start = 0
    max_end = 0
    max = 0
    started = False
    pianoChannels = ("ch=1", "ch=2", "ch=4", "ch=8", "ch=9")
    lines = f.readlines()

    # deleting all PitchBend ev ents, that might enlarge bass parts to much
    j = 0
    while j < len(lines):
        if len(lines[j].split()) >= 4:
            lineType = lines[j].split()[1]
            if lineType.startswith("Pb"):
                del lines[j]
        j +=1
    # searching for the longest track
    isPianoTrack = 0
    for i in range(len(lines)):
        if lines[i].startswith("MTrk"):
            isPianoTrack = 0
            started = True
            start = i
        elif lines[i].startswith("TrkEnd"):
            if not started:
                raise AssertionError("Error")
            diff = i - start
            if diff > max and isPianoTrack >= 0:
                max = diff
                max_start = start
                max_end = i
                isPianoTrack = 0
        if len(lines[i].split()) >= 4:
            if lines[i].split()[2].startswith(pianoChannels):
                isPianoTrack += 1
            else:
                isPianoTrack -= 1
    # Opening output folder, creating if folder doesn't exist

    path = os.path.join(my_path, "..\\files\\mtxSimplified")
    name = os.path.join(path, os.path.basename(fn))
    try:
        to_save = open(name, "w")
    except FileNotFoundError:
        os.mkdir(path)
        to_save = open(name, "w")
    # Changing first line so we will use only one channel for piano
    cut_file = ["MFile 1 1 120\n"]
    division = int(lines[0].split()[3])
    normTempoDivider = division/120
    # Rewriting lines of the biggest block
    for i in range(max_start, max_end + 1):
        lineType = ""
        lineChannel = "ch=1"
        lineParC = "c=64"
        if lines[i].startswith(("MTrk", "TrkEnd")):
            cut_file.append(lines[i])
            continue
        # Here im dividing tick by the normalization parameter that will allow me to
        # make all mtx files to have division parameter equals 120
        lineTickNormalized = str(int(int(lines[i].split()[0]) / normTempoDivider))
        lines[i] = lineTickNormalized + ' ' + ' '.join(lines[i].split()[1:len(lines[i].split())]) + '\n'

        if len(lines[i].split()) >= 4:
            lineType = lines[i].split()[1]
            lineChannel = lines[i].split()[2]
            lineParC = lines[i].split()[3]
        if not lineChannel == "ch=1":
            continue
        if not lineParC.startswith("c=64") and lineType.startswith("Par"):
            continue
        if not lineType.startswith(("On", "Par")):
            continue
        else:
            cut_file.append(lines[i])
    to_save.writelines(cut_file)
    fileCounter += 1


