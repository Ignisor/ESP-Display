import os

from PIL import Image

INPUT_DIR = 'raw_images'
OUTPUT_DIR = 'esp/images'
IMG_SIZE = (128, 64)


def img_to_bin(img):
    if img.width > IMG_SIZE[0] or img.height > IMG_SIZE[1]:
        img = img.resize(IMG_SIZE)

    img = img.convert('L')

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            val = int(img.getpixel((x, y)) > 127)

            yield val


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for img_name in os.listdir(INPUT_DIR):
        img_path = os.path.join(INPUT_DIR, img_name)
        img = Image.open(img_path)

        with open(os.path.join(OUTPUT_DIR, os.path.splitext(img_name)[0] + '.bin'), 'wb') as out_file:
            for b in img_to_bin(img):
                out_file.write(bytes([b]))
