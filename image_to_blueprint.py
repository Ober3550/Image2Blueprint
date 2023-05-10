from PIL import Image
from blueprint_builder import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("target", help="target png file to convert to blueprint", type=str)
parser.add_argument("--palette", help="palette to use. defaults to vanilla", type=str, default="vanilla")

def find_closest_palette_color(old_pixel,error,palette):
    distance = [0] * len(palette)
    for i in range(len(palette)):
        distance[i] = (old_pixel[0] + error[0] - palette[i][0])**2 + (old_pixel[1] + error[1] - palette[i][1])**2 + (old_pixel[2] + error[2] - palette[i][2])**2
    return distance.index(min(distance))

def floyd_steinberg(old_pixels,new_pixels,i,j, error_mask):
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
    palette_name = args.palette

    #Create Images
    old_img = Image.open(f'in_n_out/{filename}.png').convert('RGB')
    new_img = Image.new('RGB',[old_img.size[0],old_img.size[1]],'white')

    #Load image into rgba array format
    old_pixels = old_img.load()
    new_pixels = new_img.load()

    #Create blueprint builder object
    bp = Blueprint(filename)

    #Introduce palette
    palette  = []
    item_name = []
    item_type = []
    item_size = []
    used_palette = {}
    used_palette_colour = {}
    with open(f"palettes/{palette_name}.txt","r") as f:
        for line in f:
            if line[0:2] != "//":
                entry = line.split(":")
                color = tuple([int(c) for c in entry[0].strip()[1:-1].split(",")])
                palette.append(color)
                try:
                    used_palette_colour[entry[1].strip()] = color
                    item_name.append(entry[1].strip())
                    item_type.append(entry[2].strip())
                except:
                    item_name.append(None)
                    item_type.append(None)
                try:
                    item_size.append(int(entry[3].strip()))
                except:
                    item_size.append(1)

    #Add mask to be able to dither irregularly sized objects
    collision_mask = [[0 for _ in range(old_img.size[1])] for _ in range(old_img.size[0])]
    error_mask = [[[0 for _ in range(3)] for _ in range(old_img.size[1])] for _ in range(old_img.size[0])]

    #Iterate through image and quantize it
    progress = 0
    for i in range(old_img.size[0]):
        #Progress Meter
        if progress < round(i*100/old_img.size[0]):
            progress = round(i*100/old_img.size[0])
            print(f"{progress}%")

        for j in range(old_img.size[1]):
            #Find entity assosciated with closest palette color
            p_index = find_closest_palette_color(old_pixels[i,j],error_mask[i][j],palette);
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
                            new_pixels[i+k,j+l] = palette[p_index]
                            collision_mask[i+k][j+l] = 1
                            if i+k < old_img.size[0]-1:
                                if j+l < old_img.size[1]-1:
                                    floyd_steinberg(old_pixels,new_pixels,i+k,j+l, error_mask)
            if collision == False:
                #Add entity
                if item_name[p_index] != None:
                    if item_name[p_index] not in used_palette.keys():
                        used_palette[item_name[p_index]] = 0
                    used_palette[item_name[p_index]] = used_palette[item_name[p_index]] + 1
                    bp.addEntity(item_name[p_index],(i,j),item_type[p_index])


    #Write blueprint to string to txt file
    bp_string = open(f"in_n_out/{filename}.txt","w+")
    bp_string.write(bp.getBlueprintString())
    bp_string.close()

    with open(f"palettes/{filename}_palette.txt","w") as f:
        f.write("")
        used_palette_keys = used_palette.keys()
        used_palette_sorted = sorted(used_palette_keys, key=lambda x: -used_palette[x])
        for colour in used_palette_sorted:
            f.write("{0}:{1}:tile:1:{2}\n".format(used_palette_colour[colour],colour,used_palette[colour]))

    #Show Final Image
    new_img.show()
    new_img.save(f'in_n_out/{filename}_output.png')

if __name__ == "__main__":
    main(parser.parse_args())
