import argparse
import ColorMapper

parser = argparse.ArgumentParser(description='Make an image map of RGB space.')

parser.add_argument('--step', type=int, default=4,
                   help='Color steps in output image map.')

parser.add_argument('filename', metavar='filename',
                   help='Output file name.')

if __name__ == '__main__':
    args = parser.parse_args()
    ColorMapper.make_image(args.step).save(args.filename)