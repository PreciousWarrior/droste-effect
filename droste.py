#!/usr/bin/env python3
from PIL import Image
import argparse

def coordinate_in_image(width, height, coord):
    return 0 < coord[0] <= width and 0 < coord[1] <= height

def image_too_small(width, height, tl, br):
    if not (coordinate_in_image(width, height, tl) and coordinate_in_image(width, height, br)): return True 
    if (br[0]-tl[0] <= 0 or  br[1]-tl[1] <= 0): return True
    return False

def generate_image(image, recursion_call):
    if recursion_call >= limit:
        return image 
    width, height = image.size
    tl = (int(tl_ratio[0]*width), int(tl_ratio[1]*height))
    br = (int(br_ratio[0]*width), int(br_ratio[1]*height))
    if args.verbose:
        print(tl, br, image.size)
    if image_too_small(width, height, tl, br): return image
    resized = image.resize((br[0]-tl[0], br[1]-tl[1]))
    updated = generate_image(resized, recursion_call + 1)
    image.paste(updated, tl)
    return image

parser = argparse.ArgumentParser(description="Create the droste effect")
parser.add_argument("-i", required=True, dest="input_filename", help="Path to input file (image)", type=str)
parser.add_argument("-o", required=True, dest="output_filename", help="Path to output file (image)", type=str)
parser.add_argument("-tl", "--top-left", required=True, dest="tl", help="Coordinates of the top left pixel to start the Droste effect in", type=int, nargs=2)
parser.add_argument("-br", "--bottom-right", required=True, dest="br", help="Coordinates of the bottom right pixel to start the Droste effect in", type=int, nargs=2)
parser.add_argument('-L', '--limit', type=int, default=5, help='Recursion limit for the effect')
parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
args = parser.parse_args()
image = Image.open(args.input_filename)
width, height = image.size
limit = args.limit 
tl_ratio = (args.tl[0]/width, args.tl[1]/height)
br_ratio = (args.br[0]/width, args.br[1]/height)
generate_image(image, 0).save(args.output_filename)
print(f"File saved to {args.output_filename}")
