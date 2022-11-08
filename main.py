"""
This example will run on Python3.8 and OpenCV4.

****** IMPORTANT *******
There are some assumptions:
  1. The input is the result of yolo sign detection (ex. data/images/panel.jpg)
  2. It only detect single square
  3. The resolution is high enough
  4. All panels are the same size
  5. There is no rotation in image
  6. There is no prespective in image


Usage:
    python3 main.py --source path/to/image
    
    Example:
        python3 main.py --source data/images/panel.jpg

    or use default path:
        python3 main.py

"""

import argparse
import os
import sys
from pathlib import Path

from utils.detection import color_detection
from utils.homography import homography


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default=ROOT / 'data/images/test.jpg', help='file/dir/URL/glob')
    opt = parser.parse_args()
    return opt


def main(opt):
    color_detection(**vars(opt))

    # To crop the image, uncomment this part.
    # You need to find the four corners of the the panel manually.
    # The corners are top-left, top-right, bottom-left, and bottom-right of panel respectively.
    # corners = [[15,17], [755,21], [21,136], [746,145]]
    # homography('data/raw/panel.jpg', corners, save=True, output='data/images/test.jpg')

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)

