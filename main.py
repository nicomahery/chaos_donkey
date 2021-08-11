import os
from random import *
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance

MAX_RANDOM_WIDTH = 800
MAX_RANDOM_HEIGHT = 800
MIN_RANDOM_WIDTH = 350
MIN_RANDOM_HEIGHT = 350
transposition_dict = {Image.ROTATE_90: '90_', Image.ROTATE_180: '180_', Image.ROTATE_270: '270_',
                      Image.FLIP_LEFT_RIGHT: 'flip_ltr_', Image.FLIP_TOP_BOTTOM: 'flip_ttb_'}
filter_dict = {ImageFilter.BLUR: 'blur_', ImageFilter.DETAIL: 'detail_', ImageFilter.FIND_EDGES: 'find_edges_',
               ImageFilter.CONTOUR: 'contour_', ImageFilter.EDGE_ENHANCE: 'edge_enhance_',
               ImageFilter.EDGE_ENHANCE_MORE: 'edge_enhance_more_', ImageFilter.SHARPEN: 'sharpen_',
               ImageFilter.SMOOTH_MORE: 'smooth_more'}


def convert_black_and_white_image(input_image_path, output_image_path):
    color_image = Image.open(input_image_path)
    bw = color_image.convert('L')
    bw.save(output_image_path)


def resize_image(input_image_path, output_image_path, width, height):
    image = Image.open(input_image_path)
    resized = image.resize((width, height))
    resized.save(output_image_path)


def transpose_image(input_image_path, output_image_path, transposition):
    image = Image.open(input_image_path)
    transpose = image.transpose(transposition)
    transpose.save(output_image_path)


def generate_rotated_image(input_image_path, output_image_path, angle):
    image = Image.open(input_image_path)
    image = image.rotate(angle, expand=True)
    image.save(output_image_path)


def generate_box_blur_image(input_image_path, output_image_path, radius):
    image = Image.open(input_image_path)
    image = image.filter(ImageFilter.BoxBlur(radius))
    image.save(output_image_path)


def apply_filter_image(input_image_path, output_image_path, filter_to_apply):
    image = Image.open(input_image_path)
    image = image.filter(filter_to_apply)
    image.save(output_image_path)


def apply_chaotic_transformation_to_image(input_image_path, output_directory_path):
    filename = os.path.basename(input_image_path)
    created_image_path_list = []
    for transposition in transposition_dict.keys():
        transposed_filename = transposition_dict[transposition] + filename
        transposed_image_path = os.path.join(output_directory_path, transposed_filename)
        transpose_image(input_image_path, transposed_image_path, transposition)
        created_image_path_list.append(transposed_image_path)


def apply_chaotic_filter_to_image(input_image_path, output_directory_path):
    for filter_applied in filter_dict.keys():
        filtered_image_path = os.path.join(output_directory_path, filter_dict[filter_applied] + os.path.basename(input_image_path))
        apply_filter_image(input_image_path, filtered_image_path, filter_applied)


def resize_image_at_random_dimensions(input_image_path, output_directory_path):
    random_width = randint(MIN_RANDOM_WIDTH, MAX_RANDOM_WIDTH)
    random_height = randint(MIN_RANDOM_HEIGHT, MAX_RANDOM_HEIGHT)
    resized_image_path = os.path.join(output_directory_path, str(random_width) + '_' + str(random_height) + '_'
                                      + os.path.basename(input_image_path))
    resize_image(input_image_path, resized_image_path, random_width,  random_height)
    return resized_image_path


if __name__ == '__main__':
    convert_black_and_white_image('test', 'test')

