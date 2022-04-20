import glob

import easyocr
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from main import *

def _p_n(num):
    a = np.column_stack((np.arange(0, len(num)), np.array(num)))

    return a


class Filter_num:
    def __init__(self, out):
        fs = list(map(
            lambda x: x.split('_')[-1],
            glob.glob(f'{out}/n*')
        ))

        if not os.path.exists(f'{out}/no_res.txt'):
            fs_cannotFind = []
        else:
            with open(f'{out}/no_res.txt', "r") as f:
                fs_cannotFind = f.read().split(',')[:-1]
                print('cannot find are: ', fs_cannotFind)

        self.fs = fs + fs_cannotFind


    def has_it(self, num):
        return num in self.fs


def get_img_id(args):
    my_Filter_num = Filter_num(args.output_dir)

    reader = easyocr.Reader(['en'])
    file = cv2.imread(args.imgPath,cv2.CV_8UC1)

    result = reader.readtext(file)

    numbers = []
    cnt = 0
    for r in result:
        if r[1].startswith('#') and len(r[1]) > 1 and r[2] >= 0.0:
            no = r[1][1:]
            if my_Filter_num.has_it(no) and args.filter_exsits == 1:
                continue
            else:
                cnt += 1
                numbers.append(no)
                print(r[1], r[2])

    print(f'=======found {cnt} results.')
    print(_p_n(numbers))


    while True:
        pair = input('index u want to change(idx,number):')
        if pair == 'q':
            break
        idx, num = pair.split(',')
        idx = int(idx)
        if num == 'del':
            numbers.pop(idx)
        else:
            numbers[idx] = num
        print(_p_n(numbers))

    return '.'.join(numbers)




if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('imgPath', type=str)
    parser.add_argument('--output_dir', type=str, default='output')
    parser.add_argument('--filter_exsits', type=int, default=1)
    args = parser.parse_args()

    ids_str = get_img_id(args)
    start(ids_str, args.output_dir, 5)

