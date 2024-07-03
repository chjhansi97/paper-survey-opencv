from PIL import Image
import sys
import os

def concat(id, im1, im2, save_folder):
    images = [im1, im2]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_folder = os.path.join('concat_images', save_folder)
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    new_im.save(f'{new_folder}/{id}.jpg')

if __name__ == '__main__':
    folder_path = sys.argv[1]
    save_folder = os.path.basename(folder_path)

    concat_images_path = 'concat_images'
    if not os.path.exists(concat_images_path):
        os.makedirs(concat_images_path)

    for dir in os.listdir(folder_path):
        
        if dir == 'log.txt':
            continue
        im1 = Image.open(f'{folder_path}/{dir}/14.jpg')
        im2 = Image.open(f'{folder_path}/{dir}/15.jpg')
        concat(dir, im1, im2, save_folder)
