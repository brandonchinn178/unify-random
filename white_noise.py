from utils import Program
from struct import pack
import wave

DURATION = 3
FRAME_RATE = 22050
SAMPLE_SIZE = 1
SAMPLE_MAX = 2 ** (8 * SAMPLE_SIZE) - 1

class WhiteNoiseGenerator(Program):
    """
    A program that generates a random 3 second WAV file.
    """
    DESCRIPTION = 'Generate a random 3 second WAV file'

    def _get_parser(self):
        parser = super(WhiteNoiseGenerator, self)._get_parser()
        parser.add_argument('-o', '--output', help='Filename of output file, e.g. foo.wav', default='tmp.wav')
        return parser

    def generate(self):
        wav = wave.open('output/%s' % self.args.output, 'w')
        wav.setparams((1, SAMPLE_SIZE, FRAME_RATE, 0, 'NONE', 'not compressed'))

        data = self.get_random_int(0, SAMPLE_MAX, FRAME_RATE * DURATION)
        for v in data:
            wav.writeframes(pack('B', v))

        wav.close()

if __name__ == '__main__':
    WhiteNoiseGenerator().generate()
