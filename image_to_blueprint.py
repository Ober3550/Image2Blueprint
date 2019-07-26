from PIL import Image
from blueprint_builder import *

def find_closest_pallette_color(oldpixel,pallette):
    distance = [0] * len(pallette)
    for i in range(len(pallette)):
        distance[i] = (oldpixel[0] - pallette[i][0])**2 + (oldpixel[1] - pallette[i][1])**2 + (oldpixel[2] - pallette[i][2])**2
    return distance.index(min(distance))

def quantize(qua_pixel,old_pixel,new_pixel,ratio):
    red   = round(qua_pixel[0] + ratio*(old_pixel[0] - new_pixel[0]))
    green = round(qua_pixel[1] + ratio*(old_pixel[1] - new_pixel[1]))
    blue  = round(qua_pixel[2] + ratio*(old_pixel[2] - new_pixel[2]))
    return (red,green,blue)

#################
#Input File Name#
#################
filename = "stonks"

#Create Images
old_img = Image.open('in_n_out/'+filename+'.png')
new_img = Image.new('RGBA',[old_img.size[0],old_img.size[1]],'white')

#Load image into rgba array format
old_pixels = old_img.load()
new_pixels = new_img.load()

#Create blueprint builder object
bp = Blueprint(filename)

#Introduce pallette
pallette  = []
item_name = []
item_type = []
with open("pallettes/vanilla.txt","r") as f:
    for line in f:
        entry = line.split(":")
        pallette.append(eval(entry[0].strip()))
        try:
            item_name.append(entry[1].strip())
            item_type.append(entry[2].strip())
        except:
            pass

#Iterate through image and quantize it
progress = 0
for i in range(old_img.size[0]):
    
    #Progress Meter
    if progress < round(i*100/old_img.size[0]):
        progress = round(i*100/old_img.size[0])
        print("{}%".format(progress))
        
    for j in range(old_img.size[1]):
        #Find entity assosciated with closest pallette color
        p_index = find_closest_pallette_color(old_pixels[i,j],pallette);
        
        #Floyd Steinberg Diffusion
        new_pixels[i,j] = pallette[p_index]
        try:
            #Add entity
            bp.addEntity(item_name[p_index],(i,j),item_type[p_index])

            #Quantization
            old_pixels[i+1,j  ] = quantize(old_pixels[i+1,j  ],old_pixels[i,j],new_pixels[i,j],7/16)
            old_pixels[i-1,j+1] = quantize(old_pixels[i-1,j+1],old_pixels[i,j],new_pixels[i,j],3/16)
            old_pixels[i  ,j+1] = quantize(old_pixels[i  ,j+1],old_pixels[i,j],new_pixels[i,j],5/16)
            old_pixels[i+1,j+1] = quantize(old_pixels[i+1,j+1],old_pixels[i,j],new_pixels[i,j],1/16)
        except:
            pass

#Write blueprint to string to txt file
bp_string = open('in_n_out/'+filename+".txt","w+")
bp_string.write(bp.getBlueprintString())
bp_string.close()

#Show Final Image
new_img.show()
new_img.save('in_n_out/'+filename+'_output.png')

