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
        if r[1].startswith('#') and len(r[1]) > 1:
            cnt += 1
            numbers.append(r[1][1:])
            print(r)

    print(f'=======found {cnt} results.')
    print(numbers)

    return '.'.join(numbers)




if __name__ == '__main__':
    ids_str = get_img_id(r"rec_number\IMG_3104.jpeg")
    start(ids_str, 'output')

