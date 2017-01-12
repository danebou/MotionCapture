import numpy as np
import cv2
import sys
from mcOrient import *

def error(err):
    print(err)
    raw_input("The program will now exit...")
    exit()
    return

def processArgs(argv):
    # Make sure there are enough arguments
    if len(argv) != 3:
        error("Wrong number of arguments")

    # Get number of cameras
    try:
        cameraCount = int(argv[1])
    except ValueError:
        error(argv[1] + " is not a number (arg 1)")

    # Get chess Size
    chessSize = argv[2].split("x", cameraCount)
    try:
        chessSize = tuple([int(dim) for dim in chessSize])
    except ValueError:
        error('Argument 2 needs to be formated as "NxN"');

    return cameraCount, chessSize


def main():
    print("""---- Motion Capture Head Tracking v0.1 ----

    - by Dane Bouchie               
            
-------------------------------------------
""")
    # Load arguments
    cameraCount, chessSize = processArgs(sys.argv);

    # Get orientation
    orientation = orientationFromSetup(cameraCount, chessSize) 

    # 

    return 

if __name__ == "__main__":
    main()