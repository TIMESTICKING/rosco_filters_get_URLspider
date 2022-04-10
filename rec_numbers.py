import easyocr
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from main import *

def get_img_id(path):
    reader = easyocr.Reader(['en'])
    file = cv2.imread(path,cv2.CV_8UC1)

    result = reader.readtext(file)

    numbers = []
    cnt = 0
    for r in result:
        if r[1].startswith('#') and len(r[1]) > 1 and r[2] >= 0.35:
            cnt += 1
            numbers.append(r[1][1:])
            print(r)

    print(f'=======found {cnt} results.')
    print(numbers)

    return '.'.join(numbers)




if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('imgPath', type=str)
    parser.add_argument('--output_dir', type=str, default='output')
    args = parser.parse_args()

    ids_str = get_img_id(args.imgPath)
    start(ids_str, args.output_dir, 8)

