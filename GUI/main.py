import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer


import librosa
from keras.utils import to_categorical
import numpy as np
from preprocess import *
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint


root = tk.ThemedTk()
root.get_themes()                 # Returns a list of all themes that can be set
root.set_theme("clam")         # Sets an available theme

# Fonts - Arial (corresponds to Helvetica), Courier New (Courier), Comic Sans MS, Fixedsys,
# MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), and Verdana
#
# Styles - normal, bold, roman, italic, underline, and overstrike.

statusbar = ttk.Label(root, text="Audio Recognizer", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu

subMenu = Menu(menubar, tearoff=0)

playlist = []


# playlist - contains the full path + filename
# playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside play load function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)
    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About', 'This is a GUI build for the final project of CSCE 636. It can be used to label audio clips.')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer

root.title("Audio Recognizer")

# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame - The listbox (playlist)
# RightFrame - TopFrame,MiddleFrame and the BottomFrame

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    audio = playlistbox.curselection()
    audio = int(audio[0])
    playlistbox.delete(audio)
    playlist.pop(audio)


delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
delBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack(pady=5)


def show_details(audio):
    file_data = os.path.splitext(audio)

    if file_data[1] == '.mp3':
        audio = MP3(audio)
        total_length = audio.info.length
    else:
        a = mixer.Sound(audio)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop()
            time.sleep(1)
            audio = playlistbox.curselection()
            audio = int(audio[0])
            play_it = playlist[audio]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Could not find the file. Please check again.')


def stop():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Paused"



def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause)
pauseBtn.grid(row=0, column=2, padx=10)

# Bottom Frame for volume, rewind, mute etc.

bottomframe = Frame(rightframe)
bottomframe.pack()

mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)

feature_dim_1 = 20
feature_dim_2 = 40
channel = 1
num_classes = 45
labels = ['down', 'learn', 'right', 'nine', 'eight', 'dog', 'bird', 'house',
 'marvin', 'zero', 'sheila', 'bed', 'follow', 'off', 'happy', 'backward', 'on',
  'cat', 'left', 'five', 'visual', 'one', 'no', 'two', 'yes', 'forward', 'tree',
   'three', 'go', 'seven', 'six', 'wow', 'stop', 'four', 'up','air_conditioner',
   'dog_bark', 'street_music', 'car_horn', 'drilling', 'children_playing',
    'siren', 'engine_idling', 'jackhammer', 'gun_shot']

weights_path =  'model.hdf5'

def wav2mfcc(file_path, max_len=11,samprate = 8000):
    wave, sr = librosa.load(file_path, mono=True, sr=None)
    wave = wave[::3]
    ##mfcc = librosa.feature.mfcc(wave, sr=16000)
    mfcc = librosa.feature.mfcc(wave, sr=samprate)
    # If maximum length exceeds mfcc lengths then pad the remaining ones
    if (max_len > mfcc.shape[1]):
        pad_width = max_len - mfcc.shape[1]
        mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')

    # Else cutoff the remaining parts
    else:
        mfcc = mfcc[:, :max_len]

    return mfcc

def create_model():
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(2, 2), activation='relu', input_shape=(feature_dim_1, feature_dim_2, channel)))
    model.add(Conv2D(48, kernel_size=(2, 2), activation='relu'))
    model.add(Conv2D(120, kernel_size=(2, 2), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(120, kernel_size=(2, 2), activation='relu'))
    model.add(Conv2D(120, kernel_size=(2, 2), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(num_classes, activation='softmax'))
    return model


model = create_model()
model.load_weights(weights_path)

# Predicts one sample
def predict(filepath, model,labels):
    mfcc = wav2mfcc(filepath, max_len=40)
    mfcc_reshaped = mfcc.reshape(1,feature_dim_1,feature_dim_2,channel)
    odds= model.predict(mfcc_reshaped)
    odds_max = np.argmax(odds)
    label = labels[odds_max]
    return label

def findLabel():
    print(playlist)
    audio = playlistbox.curselection()
    audio = int(audio[0])
    file = playlist[audio]
    print(file)
    label = predict(file,model,labels)
    audioLabel['text'] = label


predictBtn = ttk.Button(bottomframe, text='Predict Label', command=findLabel)
predictBtn.grid(row=1, column=1 , pady=10, padx =10)

audioLabel = ttk.Label(bottomframe, text='Label')
audioLabel.grid(row = 1, column = 2, pady=10, padx =10)


def on_closing():
    stop()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
