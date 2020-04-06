#!/bin/usr/env/ python3

import argparse, cv2, string
import numpy as np
from pathlib import Path

class imageToText():
    def __init__(self, image, width=120):
        self.file = str(image)
        self.width = int(width)
        self.prepare_file()
        self.convert()
        self.show()

    def show(self):
        res = ''
        for i in self.ch:
            row = ''
            for c in i:
                row += str(c)
            res += "\n" + row
        print(res)

    def lookup_val(self, prcnt):
        return self.char_db.get(prcnt) or self.char_db[min(self.char_db.keys(), key = lambda key: abs(key-prcnt))]

    def prepare_file(self):
        def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
            # initialize the dimensions of the image to be resized and
            # grab the image size
            dim = None
            (h, w) = image.shape[:2]
            # adjusting proportions
            h *= 0.465
            # if both the width and height are None, then return the
            # original image
            if width is None and height is None:
                return image
            # check to see if the width is None
            if width is None:
                # calculate the ratio of the height and construct the
                # dimensions
                r = height / float(h)
                dim = (int(w * r), height)
                # otherwise, the height is None
            else:
                # calculate the ratio of the width and construct the
                # dimensions
                r = width / float(w)
                dim = (width, int(h * r))
            # resize the image
            resized = cv2.resize(image, dim, interpolation = inter)

            # return the resized image
            return resized

        im_gray = image_resize(cv2.imread(self.file, cv2.IMREAD_GRAYSCALE),self.width)
        px_v = np.vectorize(self.percentage)
        self.prcn_data = px_v(im_gray)
        chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`\". "
        self.char_db = dict()
        for i in range(len(chars)):
            self.char_db[self.percentage(i,len(chars))] = chars[i]

    def convert(self):
        ch_v = np.vectorize(self.lookup_val)
        self.ch = ch_v(self.prcn_data)

    def percentage(self, part, whole=255):
        return int(100 * float(part)/float(whole))

if __name__ == '__main__':
    text = """
  _                       ___    _                   _
 (_)                     |__ \  | |                 | |
  _   _ __ ___     __ _     ) | | |_    ___  __  __ | |_
 | | | '_ ` _ \   / _` |   / /  | __|  / _ \ \ \/ / | __|
 | | | | | | | | | (_| |  / /_  | |_  |  __/  >  <  | |_
 |_| |_| |_| |_|  \__, | |____|  \__|  \___| /_/\_\  \__|
                   __/ |
                  |___/

        //     Convert your images to text.     \\\\
    """

    parser = argparse.ArgumentParser(description=text)
    parser.add_argument("-i", "--image", help="set input image file. example: '/path/to/image.jpg'",required=True)
    parser.add_argument("-w", "--width", help="set out image width (characters in row)")
    args = parser.parse_args()
    if args.image:
        print(text)
        print("-----> Proccessing image: %s" % args.image)
        f = Path(args.image)

        if args.width:
            print("-----> Setting output width (characters in row): %s" % args.width)
            img2text = imageToText(f,args.width)
        else:
            print("-----> Setting output width to default 120 characters in a row.\n-----> {!} Please, experement width '[-w], [--width]' arguments for best results")
            img2text = imageToText(f)
    else:
         parser.print_help()
