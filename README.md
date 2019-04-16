# Music Generator
This project implements Deep Learning solution in generating music with it's image form - piano roll.
It was part of my diploma thesis defended in January 2019.

**LAST UPDATE** - New article ["Use of artificial intelligence for generating musical contents"](https://github.com/SaxMan96/Music-Generator/blob/master/Article.pdf) PL

Listen **AI Music** at my [SoundCloud](https://soundcloud.com/mateuszdorobek/sets/ai-music)

<a href="https://soundcloud.com/mateuszdorobek/sets/ai-music">
<img border="0" alt="W3Schools" src="https://www.magneticmag.com/.image/t_share/MTU5MDMzNzc3NjQ4MDUxOTky/soundcloud.png" width="200">
</a>


# Input Data
I've decided to use piano roll forma, becouse it has the less data redundation compared with audio wave form and spectrogram:
<img src="https://raw.githubusercontent.com/SaxMan96/Music-Generator/master/images/music_formats_%20comparition.png" width="500" align="middle" title="Music Formats Comparition">

Images in piano roll format was created from two midi databases:
| Nazwa 	| Opis 	| Typ danych 	| Liczba danych 	|
|----------------	|------------------------------------------------------	|-------------	|---------------------	|
| [Dough McKeznie](https://bushgrafts.com/midi/) 	| Pianino jazzowe solo 	| MIDI 	| ~300 utworów, 20h 	|
| MidKar 	| Różne gatunki, pełne składy 	| MIDI 	| ~1000 utworów, 60h 	|
| [MAESTRO](https://magenta.tensorflow.org/datasets/maestro#dataset) 	| Nagrania z pianistycznego konkursu muzyki klasycznej 	| Wave & MIDI 	| ~2500 utworów, 170h 	|

Using scripts in [MidiScripts](https://github.com/SaxMan96/Music-Generator/tree/master/MidiScripts) I've transformed raw midi files into piano roll image format. 
#### Preprocessing steps:

- Removing unnecessary markers from MIDI file using [mtxClearScript.py](https://github.com/SaxMan96/Music-Generator/blob/master/MidiScripts/mtxClearScript.py)
- Quantizing midi events to 30ms using [mtxQuantizeScript.py](https://github.com/SaxMan96/Music-Generator/blob/master/MidiScripts/mtxQuantizeScript.py)
- Merging all midi files with [mtxMergeScript.py](https://github.com/SaxMan96/Music-Generator/blob/master/MidiScripts/mtxMergeScript.py) into one big pixel matrix 
- Dividing and converting with [mtxCompressScript.py](https://github.com/SaxMan96/Music-Generator/blob/master/MidiScripts/mtxCompressScript.py) into training image set.

#### Sample MIDI in text format (MIDI is basicly binary file)
```
MFile 1 2 384
MTrk
0 Tempo 500000
0 TimeSig 4/4 24 8
1 Meta TrkEnd
TrkEnd
MTrk
0 PrCh ch=1 p=0
806 On ch=1 n=42 v=71
909 Par ch=1 c=64 v=37
924 Par ch=1 c=64 v=50
939 Par ch=1 c=64 v=58
955 Par ch=1 c=64 v=62
970 Par ch=1 c=64 v=65
986 Par ch=1 c=64 v=68
...
```
### Piano Roll example:
<img src="https://raw.githubusercontent.com/SaxMan96/Music-Generator/master/images/img.png?token=AQ9tTYisSGQLtBd-wC1vXO8bEgenRsebks5cgXUcwA%3D%3D" width="400" align="middle" title="Input Image">

# Neural Network
I've decided to use DCGAN architecture described and implemented [here](https://pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html) 
#### Structure of DCGAN:
<img src="https://camo.qiitausercontent.com/d20575271ed262c2d75d8deed30f1f84809be141/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f36343333342f64336566623363342d386130632d653438642d373239382d3538303834393461326266342e706e67"  width="500" title="DCGAN Structure">

# Training
To train I've used [Google Collaboratory](colab.research.google.com) with their amazing **Tesla K80**, and my private device with **NVidia 1050Ti** which performed really well.
As a result of training I've recived bunch of indistinguishable images which I've to transform back to midi form with [imagesDecodeScript.py](https://github.com/SaxMan96/Music-Generator/blob/master/MidiScripts/imagesDecodeScript.py)

![Fake vs Real](https://raw.githubusercontent.com/SaxMan96/Music-Generator/master/images/Fake%20vs%20Real.png?token=AQ9tTS3Gwu_EG1oyGgVLGJGHY8E0xcTHks5cgXvbwA%3D%3D)

Overal cost function in first experiments semms to prove some overfitting, but in this kind of images it's nothing suprising.

![Cost Function](https://raw.githubusercontent.com/SaxMan96/Music-Generator/master/images/G%26D%20Loss.png?token=AQ9tTWjsbX7O7GxkGVsMZuVQeG2GQYMWks5cgXxcwA%3D%3D)

And here we have one of the most beautiful things in using GAN networks, learning progres animation


![GIF](https://github.com/SaxMan96/Music-Generator/blob/master/images/gif_short.gif?raw=true)

# Results

As always not the theory, but results are the most interesting thigs in this type of projects. 

Look at [examples](https://github.com/SaxMan96/Music-Generator/tree/master/music) where you can find music generated using DCGAN. 

# Tech Stack

<img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  height="60" title="Github"><img src="https://s3-ap-south-1.amazonaws.com/av-blog-media/wp-content/uploads/2018/12/PyTorch-logo.jpg"  height="60"  title="Github"><img src="https://www.fullstackpython.com/img/logos/pycharm.jpg"  height="60" title="Pycharm Logo"><img src="https://upload.wikimedia.org/wikipedia/en/c/cd/Anaconda_Logo.png"  height="60" title="Anaconda Logo">
