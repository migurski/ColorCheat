import argparse
import ColorCheat
from PIL import Image

parser = argparse.ArgumentParser(description='Apply an image map of RGB space.')

parser.add_argument('input', metavar='input',
                   help='Input file name.')

parser.add_argument('map', metavar='map',
                   help='Map file name.')

parser.add_argument('output', metavar='output',
                   help='Output file name.')

if __name__ == '__main__':
    args = parser.parse_args()
    ColorCheat.apply_image(Image.open(args.map), Image.open(args.input)).save(args.output)