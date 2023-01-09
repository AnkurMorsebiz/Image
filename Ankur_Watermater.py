import glob,os,requests,shutil
from PIL import Image
import numpy as np



def get_image():
    if not os.path.exists('logo.png'):
        logo_img = requests.get('https://github.com/AnkurMorsebiz/Image/raw/main/MB_Logo.png', stream=True)
        with open(f'logo.png','wb') as fa: shutil.copyfileobj(logo_img.raw, fa)
    if not os.path.exists('watermark.png'):
        watermark_img = requests.get('https://github.com/AnkurMorsebiz/Image/raw/main/watermark2.png', stream=True)
        with open(f'watermark.png','wb') as fa: shutil.copyfileobj(watermark_img.raw, fa)
get_image()





def has_transparency(img):
    if img.info.get("transparency", None) is not None: return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent: return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255: return True
    return False




def transparent_to_WhiteBackground(image_path):
    image = Image.open(image_path)
    new_image = Image.new("RGBA", image.size, "WHITE")
    new_image.paste(image, (0, 0), image)
    new_image.convert('RGB')
    return new_image




def Image_Add_LogoWatermark(image_path):
    fol_check = str(image_path).rsplit('\\', 1)[0]
    os.makedirs(f"Output/{str(fol_check)}", exist_ok=True)


    main_image = Image.open(image_path)
    Transparent_check = has_transparency(main_image)


    if Transparent_check==True: main_image = transparent_to_WhiteBackground(image_path)


    logo = Image.open('logo.png')
    watermark = Image.open('watermark.png')

    main_width = main_image.size[0]
    main_height = main_image.size[1]

    #Puuting Logo
    logo_width = int(main_width/6)
    logo_height = int(logo_width/4)
    logo = logo.resize((logo_width,logo_height))
    main_image.paste(logo, (int(main_width/50), int(main_height/50)), logo)



    #Puuting Watermark
    watermark.putalpha(18)

    if int(main_width)>int(main_height):
        watermark_width = int(main_width / 2.2)
        watermark_height = int(watermark_width / 4.1)


        main_width2 = int((main_width / 2) / 1.8)
        main_height2 = int((main_height / 2) / 1.2)

        watermark = watermark.resize((watermark_width, watermark_height))
        main_image.paste(watermark, (int(main_width2), int(main_height2)), watermark)


    else:
        watermark_width = int(main_width / 1.8)
        watermark_height = int(watermark_width / 4.5)

        main_width2 = int((main_width/2)/2)
        main_height2 = int((main_height/2)/1.2)

        watermark = watermark.resize((watermark_width,watermark_height))
        main_image.paste(watermark,(int(main_width2),int(main_height2)),watermark)


    main_image.save(os.path.join('Output', str(image_path)))
    print('Source Image: ',image_path)
    print('Output Image: ',f'Output\{str(image_path)}')
    print('\n\n')


    # main_image.show()






images = glob.glob("fixed\\fixed\\*.png")

# Just Give the list of Path of Images to show the magic
# images = ['ACCENT FRONT OTR-1804.png']


for i in images:
    Image_Add_LogoWatermark(i)