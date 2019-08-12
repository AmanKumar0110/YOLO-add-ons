#!/usr/bin/env python
# coding: utf-8

# In[4]:

import shutil
import json as js
import os
import numpy as np
import argparse
import cv2
from PIL import Image





# In[6]:


def convert(size,box):
    dw = 1./size[0] #;print(dw)
    dh = 1./size[1] #;print(dh)
    x = (box[0]+box[1])/2.0 #;print(x)
    y = (box[2]+box[3])/2.0 #;print(y)
    w = box[1]-box[0] #;print(w)
    h = box[3]-box[2] #;print(h)
    x = x*dw #;print(x)
    w = w*dw #;print(w)
    y = y*dh #;print(y)
    h = h*dh #;print(h)
    #print(x/dw,w/dw,y/dh,h/dh)
    return(x,y,w,h)


# In[7]:


def transform(image,json_file,data_directory,directory):
#image = args.image
#json_file = args.json
#file = open("img1.txt","w")
    temp = json_file.split(('.')[0])
    file = open(os.path.join(directory,temp[0]+".txt"),"w+")
    image = os.path.join(data_directory,image)
    #cv2.imwrite(os.path.join(directory,temp[0]+".jpg"),cv2.imread(image))
    shutil.copy(image,directory)
    json_file = os.path.join(data_directory,json_file)
    print(json_file)
    print(os.path.join(directory,temp[0]+".txt"))
    
    with open(json_file,'rb') as read_file:
        data = js.load(read_file)
    
    im = Image.open(image)
    w = int(im.size[0])
    h = int(im.size[1])
#print(data["shapes"][0]["points"])
    label_encodings = {'knife 1':0,'knife 2':0,'stick':2,'men':9,'men and knife':9,'men and gun':9,'person1':9,'person2':9}
    for i in range(len(data["shapes"])):
        encoded_label = label_encodings[data['shapes'][i]['label']]
        if(len(data["shapes"][i]["points"])==4) and (encoded_label<9):
        #print(i)
        #print(data["shapes"][i]["points"])
            least_x = 0
            least_y = 0
            most_x = 0
            most_y = 0
            #print('points: ');print(data['shapes'][i]['points'])
            #print(data['shapes'][i]['points'][0][0])
            #print(data['shapes'][i]['points'][1][0])
            #print(data['shapes'][i]['points'][2][0])
            #print(data['shapes'][i]['points'][3][0])
            #print(data['shapes'][i]['points'][4][0])
            for j in range(4):
                #print(j)
                if(j==0):
                    least_x = data["shapes"][i]["points"][0][0]
                elif(least_x > data["shapes"][i]["points"][j][0]):
                    least_x = data["shapes"][i]["points"][j][0]
            for j in range(4):
                if(j==0):
                    least_y = data["shapes"][i]["points"][0][1]
                elif(least_y > data["shapes"][i]["points"][j][1]):
                    least_y = data["shapes"][i]["points"][j][1]
            for j in range(4):
                if(j==0):
                    most_x = data["shapes"][i]["points"][0][0]
                elif(most_x < data["shapes"][i]["points"][j][0]):
                    most_x = data["shapes"][i]["points"][j][0]
            for j in range(4):
                if(j==0):
                    most_y = data["shapes"][i]["points"][0][1]
                elif(most_y < data["shapes"][i]["points"][j][1]):
                    most_y = data["shapes"][i]["points"][j][1]
            b = (float(least_x),float(most_x),float(least_y),float(most_y))
            print('Mosts and Leasts');print(b)
            b = convert((w,h),b)
            print('Converted');print(b)
        #print(b[0]-b[2]//2, b[0]+b[2]//2, b[1]-b[3]//2,b[1]+b[3]//2)
            file.write(str(encoded_label)+" "+str(b[0])+" "+str(b[1])+" "+str(b[2])+" "+str(b[3])+" ")
            file.write("\n")
    file.close()


# In[8]:


#parser = argparse.ArgumentParser()
#parser.add_argument("--image",type = str, help = "Name of the image")
#parser.add_argument("--json", type = str, help = "Name of the json file")
#args = parser.parse_args()

if __name__ == '__main__':
    data_directory = os.path.join(os.getcwd(),'drone_images')
    directory = os.path.join(os.getcwd(),'converted_drone_images')
    print(data_directory)
    files = [f for f in os.listdir(data_directory) if os.path.isfile(os.path.join(data_directory,f))]
    files.sort()
    print(files)
    print(len(files))
    print("Starting conversion .... ")
    for i in range(len(files)//2):
 #   i=0
  #  if(True):
        image = files[2*i]
        json_file = files[2*i+1]
        print(image)
        print(json_file)
        
        transform(image,json_file,data_directory,directory)
        #break
