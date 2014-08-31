import argparse
import ColorCheat

parser = argparse.ArgumentParser(description='Make an image map of RGB space.')

parser.add_argument('--step', type=int, default=3,
                   help='Color steps in output image map, default 3.')

parser.add_argument('filename', metavar='filename',
                   help='Output file name.')

if __name__ == '__main__':
    args = parser.parse_args()
    ColorCheat.make_image(args.step).save(args.filename)