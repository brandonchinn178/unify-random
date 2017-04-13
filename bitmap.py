from PIL import Image
from utils import Program
from struct import pack

WIDTH = 128
HEIGHT = 128

class BitmapGenerator(Program):
    """
    A program that generates a random 128x128 RGB bitmap picture
    """
    DESCRIPTION = 'Generate a random 128x128 RGB bitmap picture'

    def _get_parser(self):
        parser = super(BitmapGenerator, self)._get_parser()
        parser.add_argument('-o', '--output', help='Filename of output image, e.g. foo.png', default='tmp.png')
        return parser

    def generate(self):
        data = self.get_random_int(1, 255, WIDTH * HEIGHT * 3)
        image = Image.frombytes(
            'RGB',
            size=(WIDTH, HEIGHT),
            data=''.join([pack('B', x) for x in data]),
        )
        image.save(self.args.output)

if __name__ == '__main__':
    BitmapGenerator().generate()
