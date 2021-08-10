from PIL import Image


def black_and_white_image_copy(input_image_path,
                                     output_image_path):
    color_image = Image.open(input_image_path)
    bw = color_image.convert('L')
    bw.save(output_image_path)


def rotated_mage_copy(input_image_path, output_image_path, angle):
    image = Image.open(input_image_path)
    image = image.rotate(angle, expand=True)
    image.save(output_image_path)


if __name__ == '__main__':
    black_and_white_image_copy('test', 'test')

