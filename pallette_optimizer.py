from blueprint_builder import *
import math
#Introduce pallette
pallette  = []
item_name = []
item_type = []
with open("pallettes/alien_biomes.txt","r") as f:
    for line in f:
        entry = line.split(":")
        pallette.append(eval(entry[0].strip()))
        item_name.append(entry[1].strip())
        item_type.append(entry[2].strip())

row_length = round(len(pallette)**0.5)
bp = Blueprint("Pallette Test")
for p_index in range(len(pallette)):
    bp.addEntity(item_name[p_index],(math.floor(p_index/row_length),p_index%row_length),item_type[p_index])

pallette_itera = pallette.copy()
pallette_iterb = pallette.copy()

for a in reversed(pallette_itera):
    pallette_iterb.remove(a)
    for b in pallette_iterb:
        difference = (a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2
        if difference < 225:
            try:
                del item_name[pallette.index(b)]
                del item_type[pallette.index(b)]
                pallette.remove(b)
            except:
                pass

bp_string = open("pallettes/alien_biomes_optimized.txt","w+")
bp_string.write("".join([str(pallette[i])+":"+item_name[i]+":"+item_type[i]+"\n" for i in range(len(pallette))])[0:-1])
bp_string.close()

#Write blueprint to string to txt file
bp_string = open("pallettes/alien_biomes_pallette_blueprint.txt","w+")
bp_string.write(bp.getBlueprintString())
bp_string.close()
