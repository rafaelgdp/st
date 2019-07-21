# This program creates the sierpinski triangle programmatically.
# Made by Rafael Pontes :)

from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont
from random import randint
import sys, itertools

config = {
    "image_dimension": 10000,
    "total_points": 1_000_000,
    "processor_cores": 2,
    "bg_color": (0, 0, 0, 255),
    "point_color": (255, 255, 255, 255),
    "parallel_figures": 20
}

def f(img) -> Image:
    print("Started one process...")

    vertices = [
        (img.width // 2, 0),
        (0, img.height - 1),
        (img.width - 1, img.height - 1),
    ]

    point = img.size
    i = 0
    total_points = config["total_points"]
    while (i < total_points):
        vertice = vertices[randint(0, 2)]
        point = (int((point[0] + vertice[0]) / 2), int((point[1] + vertice[1]) / 2))
        img.putpixel(point, config["point_color"])
        i += 1
    return img

if __name__ == '__main__':
    dimension = config["image_dimension"]
    estimated_size = ((4 * (dimension ** 2)) // 1024 // 1024) * config["processor_cores"]
    print("Estimated: {:d}MB".format(estimated_size))
    if (estimated_size <= 4096):
        img = Image.new('RGBA', (dimension, dimension), (0, 0, 0, 0))
        file_size = sys.getsizeof(img.tobytes()) / 1024 / 1024
        print("Actual size: %dMB" % (file_size))
        pool = Pool(processes=config["processor_cores"])
        imgs = pool.map(f, list(itertools.repeat(img, config["parallel_figures"])))
        index = 1
        for image in imgs:
            print("Merging original with image {:d}".format(index))
            index += 1
            img.paste(image, mask=image)
        draw = ImageDraw.Draw(img)
        font_size = img.width // 40
        font = ImageFont.truetype("/usr/share/fonts/TTF/DroidSansMono.ttf", size=font_size)
        draw.text((20, 20), "Feito por Rafael Pontes. :)", fill=(255, 255, 255, 255), font=font)
        img.save("st.png")
        
        for row in range(img.width):
            for col in range(img.height):
                point = (row, col)
                if img.getpixel(point)[3] == 0:
                    img.putpixel(point, config["bg_color"])
        draw.text((20, 20), "Feito por Rafael Pontes. :)", fill=(255, 255, 255, 255), font=font)
        img.save("st_blackbg.png")
    else:
        print("Dangerous amount of memory allocation!")