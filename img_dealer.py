import sys

import easyocr
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import matlab
import matlab.engine
import scipy.io as sio

sys.path.append("F:\python3proj\myutils")
import Online_breakpoint_debug

# md = Online_breakpoint_debug.Online_breakpoint_debug()
# md.start()

class MyMatlab_engine:

    def __init__(self, addpaths):
        self.eng = matlab.engine.start_matlab()
        self.eng.addpath(addpaths)


    def quit(self):
        self.eng.quit()


def save_img_data(path, root, eng):
    args = {
        'min_x':360.,
        'max_x':760.,
        'min_y':0.,
        'max_y':100.,
        'step_x' : 20,
        'step_y' : 10,
        'thresh_binary' : 0.5,
        'find_corner' : 0,
        'mark_points' : matlab.double([[0,155],[305,0]]),
        'filter_level': 'medium'
    }
    [x, y, viz] = eng.imgPlot2digital(path, matlab.double(list(range(380, 721))), '', args, nargout=3)
    eng.saveas(viz, f'{root}/xy.jpg', nargout=0)
    eng.close('all', 'hidden')
    x = x[0]
    y = y[0]
    # print(x)
    # print(y)
    # plt.plot(x, y)
    # plt.savefig(f'{root}/xy.jpg')
    sio.savemat(f'{root}/xy.mat', {'x': list(x), 'y': list(y)})



def save_img_plot(path):
    im = cv2.imread(path)
    im = im[150:307, 35:339, :]
    imbg = cv2.imread("I:\python3proj\spider_filters\perfect_jpg_bg\perfect_colorBG.jpg")
    imdiff = np.abs(im - imbg)
    imdiff[imdiff<50] = 255

    # md.goin(locals())

    os.remove(path)
    cv2.imwrite(path, imdiff)




if __name__ == '__main__':
    # get_img_data(r"I:\python3proj\spider_filters\output\4860\cinegel_4860_jpg\cinegel_4860.jpg")

    mymatlab = MyMatlab_engine('I:\matlabproj\image_graph_line_to_digital_convert')
    save_img_data(r"I:\python3proj\spider_filters\output\375\cinelux_375_jpg\cinelux_375.jpg",
                  r"I:\python3proj\spider_filters\output\375\cinelux_375_jpg",mymatlab.eng)
    mymatlab.quit()
