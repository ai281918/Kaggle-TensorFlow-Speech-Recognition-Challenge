import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import random
import math
from PIL import Image
from scipy.io import wavfile
import cv2
import pickle

input_dir = 'audio/'
output_dir = 'QQ/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def wav_to_pickle():
    files = os.listdir(input_dir)
    class_list = []
    wav_list = []
    for f in files:
        if f == '_background_noise_':
            continue
        print(f)
        class_list.append(f)
        wav_list.append([])
        path = input_dir + f + '/'
        wav_files = os.listdir(path)
        for wav_file in wav_files:
            [samprate, wav] = wavfile.read(path + wav_file)
            wav_list[-1].append(wav)
    
    file = open('class_list.pickle', 'wb')
    pickle.dump(class_list, file)
    file.close()
    file = open('wav_list.pickle', 'wb')
    pickle.dump(wav_list, file)
    file.close()

def wav_to_2D(wav_lsit, class_list, width, height, size):
    img_list = []
    for i,wavs in enumerate(wav_list):
        for k,wav in enumerate(wavs):
            img = np.zeros([height, width], dtype=np.float32)
            for j,v in enumerate(wav):
                img[min(max(int(v/(4000.)*height/2. + height/2.), 0), height-1)][min(max(int(j/22050.*width), 0), width-1)] = 1
            
            if not os.path.exists(output_dir + class_list[i] + '/'):
                os.makedirs(output_dir + class_list[i] + '/')
            
            plt.imsave(output_dir + class_list[i] + '/' + '_' + str(k).zfill(4) + '.jpg', img,  cmap='Greys_r')
            if k >= size:
                break
        


with open('wav_list.pickle', 'rb') as file:
    wav_list =pickle.load(file)
with open('class_list.pickle', 'rb') as file:
    class_list =pickle.load(file)
wav_to_2D(wav_list, class_list, 128, 64, 100)