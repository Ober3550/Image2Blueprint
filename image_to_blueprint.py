from PIL import Image
from blueprint_builder import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("target", help="target png file to convert to blueprint", type=str)
parser.add_argument("--palette", help="palette to use", type=str)

def find_closest_pallette_color(old_pixel,error,pallette):
    distance = [0] * len(pallette)
    for i in range(len(pallette)):
        distance[i] = (old_pixel[0] + error[0] - pallette[i][0])**2 + (old_pixel[1] + error[1] - pallette[i][1])**2 + (old_pixel[2] + error[2] - pallette[i][2])**2
    return distance.index(min(distance))

def floyd_steinberg(old_pixels,new_pixels,i,j):
    try:
        for c in range(3):
            error = (old_pixels[i,j][c]-new_pixels[i,j][c])>>4
            #Quantization
            error_mask[i+1][j  ][c] += error*7
            error_mask[i-1][j+1][c] += error*5
            error_mask[i  ][j+1][c] += error*3
            error_mask[i+1][j+1][c] += error
    except:
        print(i,j)

def main(args):
    #################
    #Input File Name#
    #################
    filename = args.target
    pallettename = args.palette

    #Create Images
    old_img = Image.open(f'in_n_out/{filename}.png').convert('RGB')
    new_img = Image.new('RGB',[old_img.size[0],old_img.size[1]],'white')

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
    used_pallette = {}
    used_pallette_colour = {}
    with open(f"pallettes/{pallettename}.txt","r") as f:
        for line in f:
            if line[0:2] != "//":
                entry = line.split(":")
                pallette.append(eval(entry[0].strip()))
                try:
                    used_pallette_colour[entry[1].strip()] = eval(entry[0].strip())
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
    error_mask = [[[0 for c in range(3)] for x in range(old_img.size[1])] for y in range(old_img.size[0])] 

    #Iterate through image and quantize it
    progress = 0
    for i in range(old_img.size[0]):
        #Progress Meter
        if progress < round(i*100/old_img.size[0]):
            progress = round(i*100/old_img.size[0])
            print("{}%".format(progress))

        for j in range(old_img.size[1]):
            #Find entity assosciated with closest pallette color
            p_index = find_closest_pallette_color(old_pixels[i,j],error_mask[i][j],pallette);
            collision = False
            #Apply dithering to region around irregularly sized entity and set collision boundary
            #For elements with size 1 this will do the same as before            
            for k in range(item_size[p_index]):
                if collision==True:
                    break
                for l in range(item_size[p_index]):
                    if i+k < old_img.size[0]:
                        if j+l < old_img.size[1]:
                            if collision_mask[i+k][j+l] == 1:
                                collision=True
                                break
                            #Set pixel to closest color
                            new_pixels[i+k,j+l] = pallette[p_index]
                            collision_mask[i+k][j+l] = 1
                            if i+k < old_img.size[0]-1:
                                if j+l < old_img.size[1]-1:
                                    floyd_steinberg(old_pixels,new_pixels,i+k,j+l)
            if collision == False:
                #Add entity
                if item_name[p_index] != None:
                    if item_name[p_index] not in used_pallette.keys():
                        used_pallette[item_name[p_index]] = 0
                    used_pallette[item_name[p_index]] = used_pallette[item_name[p_index]] + 1
                    bp.addEntity(item_name[p_index],(i,j),item_type[p_index])


    #Write blueprint to string to txt file
    bp_string = open(f'in_n_out/{filename}.txt","w+")
    bp_string.write(bp.getBlueprintString())
    bp_string.close()

    with open(f"pallettes/{filename}_pallette.txt","w") as f:
        f.write("")
        used_pallette_keys = used_pallette.keys()
        used_pallette_sorted = sorted(used_pallette_keys, key=lambda x: -used_pallette[x])
        for colour in used_pallette_sorted:
            f.write("{0}:{1}:tile:1:{2}\n".format(used_pallette_colour[colour],colour,used_pallette[colour]))

    #Show Final Image
    new_img.show()
    new_img.save(f'in_n_out/{filename}_output.png')

if __name__ == "__main__":
    main(parser.parse_args())
