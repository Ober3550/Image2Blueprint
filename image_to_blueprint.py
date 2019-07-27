from PIL import Image
from blueprint_builder import *

def find_closest_pallette_color(oldpixel,pallette):
    distance = [0] * len(pallette)
    for i in range(len(pallette)):
        distance[i] = (oldpixel[0] - pallette[i][0])**2 + (oldpixel[1] - pallette[i][1])**2 + (oldpixel[2] - pallette[i][2])**2
    return distance.index(min(distance))

def stucki(old_pixels,new_pixels,i,j):
    try:
        error = (old_pixels[i,j],new_pixels[i,j])/42
        #Quantization
        old_pixels[i+1,j  ] = quantize(old_pixels[i+1,j  ],error<<3)
        old_pixels[i+2,j  ] = quantize(old_pixels[i+2,j  ],error<<2)
        old_pixels[i-2,j+1] = quantize(old_pixels[i-2,j+1],error<<1)
        old_pixels[i-1,j+1] = quantize(old_pixels[i-1,j+1],error<<2)
        old_pixels[i  ,j+1] = quantize(old_pixels[i  ,j+1],error<<3)
        old_pixels[i+1,j+1] = quantize(old_pixels[i+1,j+1],error<<2)
        old_pixels[i+2,j+1] = quantize(old_pixels[i+2,j+1],error<<1)
        old_pixels[i-2,j+2] = quantize(old_pixels[i-2,j+2],error<<0)
        old_pixels[i-1,j+2] = quantize(old_pixels[i-1,j+2],error<<1)
        old_pixels[i  ,j+2] = quantize(old_pixels[i  ,j+2],error<<2)
        old_pixels[i+1,j+2] = quantize(old_pixels[i+1,j+2],error<<1)
        old_pixels[i+2,j+2] = quantize(old_pixels[i+2,j+2],error<<0)
    except:
        pass

def floyd_steinberg(old_pixels,new_pixels,i,j):
    try:
        error = (old_pixels[i,j],new_pixels[i,j])>>4
        #Quantization
        old_pixels[i+1,j  ] = quantize(old_pixels[i+1,j  ],error*7)
        old_pixels[i-1,j+1] = quantize(old_pixels[i-1,j+1],error*3)
        old_pixels[i  ,j+1] = quantize(old_pixels[i  ,j+1],error*5)
        old_pixels[i+1,j+1] = quantize(old_pixels[i+1,j+1],error*1)
    except:
        pass
        
def quantize(qua_pixel,error):
    red   = qua_pixel[0] + error
    green = qua_pixel[1] + error
    blue  = qua_pixel[2] + error
    return (red,green,blue)

#################
#Input File Name#
#################
filename = "Factorio-title"

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
item_size = []
with open("pallettes/vanilla.txt","r") as f:
    for line in f:
        entry = line.split(":")
        pallette.append(eval(entry[0].strip()))
        try:
            item_name.append(entry[1].strip())
            item_type.append(entry[2].strip())     
        except:
            item_name.append(None)
            item_type.append(None)
        try:
            item_size.append(eval(entry[3].strip()))
        except:
            item_size.append(1)

#Add mask to be able to dither irregularly sized objects
collision_mask = [[0 for x in range(old_img.size[1])] for y in range(old_img.size[0])] 

#Iterate through image and quantize it
progress = 0
for i in range(old_img.size[0]):
    #Progress Meter
    if progress < round(i*100/old_img.size[0]):
        progress = round(i*100/old_img.size[0])
        print("{}%".format(progress))
        
    for j in range(old_img.size[1]):
        if collision_mask[i][j] == 0:
            #Find entity assosciated with closest pallette color
            p_index = find_closest_pallette_color(old_pixels[i,j],pallette);

            #Add entity
            if item_name[p_index] != None:
                if item_size[p_index] != 1:
                    bp.addEntity(item_name[p_index],(i+(item_size[p_index])/2,j+(item_size[p_index])/2),item_type[p_index])
                else:
                    bp.addEntity(item_name[p_index],(i,j),item_type[p_index])

            #Apply dithering to region around irregularly sized entity and set collision boundary
            #For elements with size 1 this will do the same as before            
            for k in range(item_size[p_index]):
                for l in range(item_size[p_index]):
                    #Set pixel to closest color
                    new_pixels[i+k,j+l] = pallette[p_index]
                    
                    #Dither
                    floyd_steinberg(old_pixels,new_pixels,i+k,j+l)
                    #stucki(old_pixels,new_pixels,i,j)
                    
                    collision_mask[i+k][j+l] = 1

#Write blueprint to string to txt file
bp_string = open('in_n_out/'+filename+".txt","w+")
bp_string.write(bp.getBlueprintString())
bp_string.close()

#Show Final Image
new_img.show()
new_img.save('in_n_out/'+filename+'_output.png')

