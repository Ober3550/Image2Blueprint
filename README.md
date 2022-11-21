# Image2Blueprint
#Converts png images into blueprints according to a limited color pallette

# How to use. 
1. Have Python Installed (2 or 3). Download online -default install
2. Install requirements: `pip install -r requirements.txt`

3. Insert your desired png file into in_n_out
4. Open the 'image_to_blueprint' script with IDLE since it's both an editor and the interpreter.
5. There is a big red commented title saying "Input File Name" change the filename variable to whatever png you're working with.
6. It's not necessary to change the pallette but it should be pretty self-explanatory how they work. "vanilla" is Vanilla "alien_biomes" is Alien Biomes etc. You can make your own pallette files.
7. Press f5 to run the module. When the script is done it should display an image of the error-diffused image as well as output a txt file of the same name as the input containing the blueprint string within the in_n_out file

# Extended features
8. Now produces a pallette file of the image in the pallettes directory with tiles sorted by use frequency. 
9. I recommend running your image once through with alien biomes. Going to the pallettes file. Opening the pallette for the image. 
10. Trimming back to about 20-30 tiles to taste and then using the new pallette to reduce the number of different tiles you need to craft in  game.
