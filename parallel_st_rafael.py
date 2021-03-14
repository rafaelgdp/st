# This program creates the sierpinski triangle programmatically.
# Made by Rafael Pontes :)

from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont
from random import randint
import sys, itertools, psutil, datetime

config = {
    "image_dimension": 20000,
    "total_points": 1_000_000,
    "processor_cores": 4,
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
    estimated_size_MB = ((4 * (dimension ** 2)) // 1024 // 1024) * config["processor_cores"]
    print("Estimated: {:d}MB".format(estimated_size_MB))
    
    available_memory = psutil.virtual_memory().available
    available_memory_MB = available_memory // (1024**2)
    
    if (estimated_size_MB <= available_memory_MB):
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
        font = ImageFont.truetype("./font/Courier Prime.ttf", size=font_size)
        draw.text((20, 20), "Feito por Rafael Pontes. :)", fill=(255, 255, 255, 255), font=font)
        date_str = datetime.datetime.now().strftime("%Y_%m_%d_%Hh%Mmin%S")
        filename = f"st_{config['image_dimension']}x{config['image_dimension']}_at_{date_str}.png"
        img.save(filename)
        print("Created file %s, which has transparent background." % filename)
        print("Next is the creation of a black-coloured background image...")
        for row in range(img.width):
            for col in range(img.height):
                point = (row, col)
                if img.getpixel(point)[3] == 0:
                    img.putpixel(point, config["bg_color"])
        draw.text((20, 20), "Feito por Rafael Pontes. :)", fill=(255, 255, 255, 255), font=font)
        filename = f"st_{config['image_dimension']}x{config['image_dimension']}_at_{date_str}_black.png"
        print("About to save image named %s." % filename)
        img.save(filename)
        print("Done!")
    else:
        print("Dangerous amount of memory allocation! Estimated %d MB of concurrent RAM usage but only %d MB available." % (estimated_size_MB, available_memory_MB))