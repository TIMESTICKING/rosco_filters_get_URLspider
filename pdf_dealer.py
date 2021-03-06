import re
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import scipy.io as sio


def get_pdf_data(path):
    with open(path, 'rb') as f:
        pdf_file = PdfFileReader(f)

        page = pdf_file.getPage(0)
        text = page.extractText()
        text = text.replace(' ','').replace('\n','{{')
        trans = re.search(r'trans%(.*?)MATERIALSPECIFICATIONS:', text)
        # print(text)
        waves = list(range(360, 741, 20))
        trans = list(map(
            int,
            trans[0].split('{{')[1:-1]
        ))
        # print(waves)
        # print(trans)

    return waves, trans


def save_pdf_data(waves, trans, root):
    fig = plt.figure(1, (9,5))
    plt.plot(waves, trans)
    plt.ylim((0, 100))
    # plt.show()
    plt.savefig(f'{root}/xy.jpg')
    sio.savemat(f'{root}/xy.mat', {'x': waves, 'y': trans})


if __name__ == '__main__':
    save_pdf_data(*get_pdf_data(r'.\output\3203\Permacolor_3203_pdf\Permacolor_3203.pdf'), r'output\3203\Permacolor_3203_pdf')


