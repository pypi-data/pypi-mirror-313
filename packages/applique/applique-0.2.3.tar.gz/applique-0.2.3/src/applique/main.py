import argparse
from emoji import emojize
from applique.convert import convert

call_me_hand = emojize(":call_me_hand:")
wind_face = emojize(":wind_face:")

parser = argparse.ArgumentParser(
    prog="applique",
    description="applique is a small program to convert .mol to .xyz files",
    epilog="Thank you for using my software. It means a lot. Have amazing times ahead. Image from (https://www.asciiart.eu/vehicles/boats)\n\nMay the wind be with you "
    + wind_face
    + "\n\n   Truly yours, \nJulian"
    + call_me_hand,
)
parser.add_argument("--i", help="location of input file", type=str)
parser.add_argument("--o", help="location to output file", type=str)
args = parser.parse_args()

convert(args.i, args.o)


def cli():
    args = parser.parse_args()

    convert(args.i, args.o)
