import os
from random import *
from PIL import Image, ImageFilter, ImageDraw, ImageFont

IMAGE_INPUT_DIRECTORY = 'IMAGE_INPUT_DIRECTORY'
IMAGE_OUTPUT_DIRECTORY = 'IMAGE_OUTPUT_DIRECTORY'
POST_REMOVE_INPUT_FILE = 'POST_REMOVE_INPUT_FILE'
PNG_EXTENSION_ARRAY = ['.png', '.PNG']
MAX_RANDOM_WIDTH = 800
MAX_RANDOM_HEIGHT = 800
MIN_RANDOM_WIDTH = 350
MIN_RANDOM_HEIGHT = 350
WATERMARK_MARGIN = 10
MIN_RANDOM_FONT_SIZE = 30
MAX_RANDOM_FONT_SIZE = 250
MIN_BLUR_RADIUS = 1
MAX_BLUR_RADIUS = 7
FONT_ARRAY = ['fonts/GreatVibes-Regular.ttf', 'fonts/Trueno-75PE.otf', 'fonts/WarsawGothic-BnBV.otf',
              'fonts/NanotechLlc-ed2B.otf', 'fonts/arial.ttf', 'fonts/calibri.ttf', ]
TRANSPOSITION_DICT = {Image.ROTATE_90: '90_', Image.ROTATE_180: '180_', Image.ROTATE_270: '270_',
                      Image.FLIP_LEFT_RIGHT: 'flip_ltr_', Image.FLIP_TOP_BOTTOM: 'flip_ttb_'}
FILTER_DICT = {ImageFilter.BLUR: 'blur_', ImageFilter.DETAIL: 'detail_', ImageFilter.FIND_EDGES: 'find_edges_',
               ImageFilter.CONTOUR: 'contour_', ImageFilter.EDGE_ENHANCE: 'edge_enhance_',
               ImageFilter.EDGE_ENHANCE_MORE: 'edge_enhance_more_', ImageFilter.SHARPEN: 'sharpen_',
               ImageFilter.SMOOTH_MORE: 'smooth_more'}
WATERMARK_TEXT_ARRAY = ['Test Watermark', 'TEST WATERMARK', 'WATERMARK', 'Watermark', 'GIFFY', 'STOCK IMAGE',
                        'Shutterstock', 'Copyright']


def convert_black_and_white_image(input_image_path, output_directory_path):
    color_image = Image.open(input_image_path)
    bw = color_image.convert('L')
    output_path_location = os.path.join(output_directory_path, os.path.basename(input_image_path))
    bw.save(output_path_location)
    return output_path_location


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


def generate_box_blur_image(input_image_path, output_directory_path):
    image = Image.open(input_image_path)
    image = image.filter(ImageFilter.BoxBlur(randint(MIN_BLUR_RADIUS, MAX_BLUR_RADIUS)))
    image.save(os.path.join(output_directory_path, os.path.basename(input_image_path)))


def apply_filter_image(input_image_path, output_image_path, filter_to_apply):
    image = Image.open(input_image_path)
    image = image.filter(filter_to_apply)
    image.save(output_image_path)


def apply_chaotic_transformation_to_image(input_image_path, output_directory_path):
    created_image_path_list = []
    for transposition in TRANSPOSITION_DICT.keys():
        transposed_filename = TRANSPOSITION_DICT[transposition] + os.path.basename(input_image_path)
        transposed_image_path = os.path.join(output_directory_path, transposed_filename)
        transpose_image(input_image_path, transposed_image_path, transposition)
        created_image_path_list.append(transposed_image_path)
    return created_image_path_list


def apply_chaotic_filter_to_image(input_image_path, output_directory_path):
    for filter_applied in FILTER_DICT.keys():
        filtered_image_path = os.path.join(output_directory_path, FILTER_DICT[filter_applied]
                                           + os.path.basename(input_image_path))
        apply_filter_image(input_image_path, filtered_image_path, filter_applied)


def resize_image_at_random_dimensions(input_image_path, output_directory_path):
    random_width = randint(MIN_RANDOM_WIDTH, MAX_RANDOM_WIDTH)
    random_height = randint(MIN_RANDOM_HEIGHT, MAX_RANDOM_HEIGHT)
    resized_image_path = os.path.join(output_directory_path, str(random_width) + '_' + str(random_height) + '_'
                                      + os.path.basename(input_image_path))
    resize_image(input_image_path, resized_image_path, random_width, random_height)
    return resized_image_path


def convert_image_to_png(input_image_path):
    png_filename = os.path.splitext(input_image_path)[0] + '.png'
    Image.open(input_image_path).convert('RGB') \
        .save(os.path.join(os.path.dirname(os.path.realpath(input_image_path)), png_filename))
    os.remove(input_image_path)
    return png_filename


def watermark_image_using_text(input_image_path, output_directory_path):  # position is example (x,y)
    watermark_text = WATERMARK_TEXT_ARRAY[randint(0, len(WATERMARK_TEXT_ARRAY) - 1)]
    image = Image.open(input_image_path).convert("RGBA")
    width, height = image.size
    watermark_overlay = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    watermark_overlay_draw = ImageDraw.Draw(watermark_overlay)
    font = ImageFont.truetype(FONT_ARRAY[randint(0, len(FONT_ARRAY) - 1)],
                              randint(MIN_RANDOM_FONT_SIZE, MAX_RANDOM_FONT_SIZE))
    text_width, text_height = watermark_overlay_draw.textsize(watermark_text, font)
    watermark_position = (
        randint(WATERMARK_MARGIN,
                WATERMARK_MARGIN if (width - text_width - WATERMARK_MARGIN) < WATERMARK_MARGIN else (
                        width - text_width - WATERMARK_MARGIN)),
        randint(WATERMARK_MARGIN,
                WATERMARK_MARGIN if (height - text_height - WATERMARK_MARGIN) < WATERMARK_MARGIN else (
                            height - text_height - WATERMARK_MARGIN)))
    watermark_overlay_draw.text(watermark_position, watermark_text, font=font, fill=(255, 255, 255, randint(100, 255)))
    output_image = Image.alpha_composite(image, watermark_overlay)
    output_image.save(os.path.join(output_directory_path, 'watermarked_' + os.path.basename(input_image_path)))
    return os.path.join(output_directory_path, 'watermarked_' + os.path.basename(input_image_path))


if __name__ == '__main__':
    image_input_directory = os.environ[IMAGE_INPUT_DIRECTORY]
    image_output_directory = os.environ[IMAGE_OUTPUT_DIRECTORY]
    try:
        if os.environ[POST_REMOVE_INPUT_FILE] == 'TRUE':
            post_remove_input_file = True
        else:
            post_remove_input_file = False
    except KeyError:
        post_remove_input_file = False

    if image_input_directory is not None and image_output_directory is not None:
        for directory in os.walk(image_input_directory):
            if directory[0] is not image_input_directory:
                dirname = os.path.basename(directory[0])
                destination_path = os.path.join(image_output_directory, dirname)
                print(f'Starting conversion of {dirname} directory to {destination_path}')
                if not os.listdir(image_output_directory).__contains__(dirname):
                    os.mkdir(destination_path)
                for filename in directory[2]:
                    image_filename = filename
                    if not str.__contains__(image_filename, PNG_EXTENSION_ARRAY[0]) \
                            and not str.__contains__(image_filename, PNG_EXTENSION_ARRAY[1]):
                        image_filename = convert_image_to_png(os.path.join(directory[0], image_filename))

                    image_location = os.path.join(directory[0], image_filename)
                    Image.open(os.path.join(directory[0], image_filename))\
                        .save(os.path.join(destination_path, image_filename))
                    watermarked_image_location = watermark_image_using_text(image_location, destination_path)
                    watermarked_watermarked_image_location = \
                        watermark_image_using_text(watermarked_image_location, destination_path)
                    bw_image_location = convert_black_and_white_image(image_location, destination_path)
                    bw_watermarked_image_location = \
                        convert_black_and_white_image(watermarked_image_location, destination_path)
                    bw_watermarked_watermarked_image_location = \
                        convert_black_and_white_image(watermarked_watermarked_image_location, destination_path)
                    image_array = [image_location, watermarked_image_location, watermarked_watermarked_image_location,
                                   bw_watermarked_image_location, bw_watermarked_watermarked_image_location]

                    for image_to_change in image_array:
                        resized_image = resize_image_at_random_dimensions(image_to_change, destination_path)
                        apply_chaotic_transformation_to_image(image_to_change, destination_path)
                        apply_chaotic_transformation_to_image(resized_image, destination_path)
                        apply_chaotic_filter_to_image(image_to_change, destination_path)
                        apply_chaotic_filter_to_image(resized_image, destination_path)
                        generate_box_blur_image(image_to_change, destination_path)
                        generate_box_blur_image(resized_image, destination_path)

                    if post_remove_input_file:
                        os.remove(image_location)

                    print(f'{os.path.join(dirname, filename)} chaos copies generated')

                if post_remove_input_file:
                    os.rmdir(directory[0])

                print(f'Conversion of {dirname} directory to {destination_path} complete')

    else:
        print('Unable to start the chaos donkey due to:')
        if image_input_directory is None:
            print('    Error IMAGE_INPUT_DIRECTORY env is not defined')
        if image_output_directory is None:
            print('    Error IMAGE_OUTPUT_DIRECTORY env is not defined')