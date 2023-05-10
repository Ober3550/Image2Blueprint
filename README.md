# Image2Blueprint

Converts png images into blueprints according to a limited color pallette

## How to use.

1. Have Python3 installed. Download online -default install
2. Install requirements: `pip install -r requirements.txt`
3. run `python image_to_blueprint.py <target_png_file_path> --palette <palette_name>`
4. output image and blueprint will be stored in `output/`
5. It's not necessary to change the pallette but it should be pretty self-explanatory how they work. "vanilla" is Vanilla "alien_biomes" is Alien Biomes etc. You can make your own pallette files.

## Extended features

* Now produces a pallette file of the image in the pallettes directory with tiles sorted by use frequency.
* I recommend running your image once through with alien biomes. Going to the pallettes file. Opening the pallette for the image.
* Trimming back to about 20-30 tiles to taste and then using the new pallette to reduce the number of different tiles you need to craft in  game.
