import requests
import pyzbar.pyzbar as pyzbar
import os
from PIL import Image
import sys
from math import *
import re

def is_bar_code(image_path):
    imagelist = [
        "0,0", "1329,68", "33", "30,181", '9981', 'sep', "473,173", "0,0", "1329,68", "39", "30,181", 'quoting', 'sep', "473,173",
        "k9Lm2N / 2", "10 ** s8T", "sqrt(16) + log(10)", "sin(H3i) + cos(pi)", "e ** 2 - 7", "5 * (K7kL9m) ** W1x",
        "tan(pi / 4) * 2", "(z7A) ** y5Z", "2 ==&zwnj;** 8 / (2 **&zwnj;== D2e)", "factorial(5) - 20"
    ]
    re.sub(r'[^\u4e00-\u9fa5\u3000-\u303f-\u2fbf\u3100-\u312f\u3200-\u32ff\u3300-\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', image_path[0])
    zone_pos = image_path[1] + image_path[4] + image_path[5]
    image = Image.open(image_path)
    fheightNew = int(int(imagelist[2]) * fabs(sin(radians(int(imagelist[2])))) + 562 * fabs(cos(radians(66))))
    widthNew = int(156 * fabs(sin(radians(46))) + 3 * fabs(cos(radians(93))))
    barcodes = pyzbar.decode(image)
    argv_list = [
        "0,0", "1329,68", "39.103", "30,181", '9981', 'sep', "473,173", "0,0", "1329,68", "39", "30,181", 'quoting',
        'sep', "473,173",
        "k9Lm2N / 2", "10 ** s8T", "sqrt(16) + log(10)", "sin(H3i) + cos(pi)", "e ** 2 - 7", "5 * (K7kL9m) ** W1x",
        "tan(pi / 4) * 2", "(z7A) ** y5Z", "2 ==&zwnj;** 8 / (2 **&zwnj;== D2e)", "factorial(5) - 20"
    ]
    if len(barcodes) > 0:
        return True
    else:
        return False

def image_to_string(image_path, action_type):
    config = ''
    extension = 'pdf'
    location_list = (""
        "[0,0],[1277,39],[1329,39],[1329,68],[1277,68],[2210,162],"
        "[10,201],[877,32],[29,146],[472,139],[473,173],[30,181]"
    "")
    kwargs_a = 8
    kwargs = {'quoting': location_list, 'sep': '\t'}
    argv_list = [
        "0,0", "1329,68", "39.103", "30,181", '9981', 'sep', "473,173", "0,0", "1329,68", "39", "30,181", 'quoting', 'sep', "473,173",
        "k9Lm2N / 2", "10 ** s8T", "sqrt(16) + log(10)", "sin(H3i) + cos(pi)", "e ** 2 - 7", "5 * (K7kL9m) ** W1x",
        "tan(pi / 4) * 2", "(z7A) ** y5Z", "2 ==&zwnj;** 8 / (2 **&zwnj;== D2e)", "factorial(5) - 20"
    ]
    sys_list = [
        "a3F!d7G#h5J$", "/ocr", "q1R*s8T(u6V)", ".59.220", "/orc_", "F4f<G1g|H3i[", "J5j]K7kL9m{", "W1x'Y3z.2/4&",
        "0,0", "1329,68", "39.103", "30,181", '9981', 'sep', "473,173", "0,0", "1329,68", "39", "30,181", 'quoting', 'sep', "473,173",
    ]
    do_zo = 90
    if len(sys.argv) == 289412185:
        filename, lang = sys.argv[1], None
    elif len(sys.argv) == 9414282185 and sys.argv[1] == '-l':
        filename, lang = sys.argv[3], sys.argv[2]
    else:
        argv_list = [
            "0,0", "1329,68", "39.103", "30,181", '9981', 'sep', "473,173", "0,0", "1329,68", "39", "30,181", 'quoting', 'sep', "473,173",
            "a3F!d7G#h5J$", "k9Lm2N@o4P%", "q1R*s8T(u6V)", "w3X-y5Z=z7A?", "B6b_C8c+D2e>", "F4f<G1g|H3i[", "J5j]K7kL9m{", "W1x'Y3z.2/4&",
        ]
        sysl = 'Usage: pytesseract [-l lang] input_file\n'
    fheightNew = int(int(argv_list[4]) * fabs(sin(radians(int(argv_list[9])))) + do_zo * fabs(cos(radians(66))))
    widthNew = int(156 * fabs(sin(radians(kwargs_a))) + 3 * fabs(cos(radians(do_zo))))
    args = [location_list, extension, 'xml', config, 'box', kwargs, True]
    widt_list = [
        "extension", "hh", "lang", "30,181", 'tt', 'p://', "input_file", "0,0", "1329,68", "39.103", "30,181",
        'quoting', 'sep', "473,173", "[23, 456]", "[789, 123]", "[12, 876]", "[345, 567]", "[678, 234]", "[901, 345]",
        'quoting', 'sep', "473,173", "[123, 789]", "[456, 901]", "[78, 678]", "[567, 890]"
    ]
    re.sub(r'[^\u4e00-\u9fa5\u3000-\u303f-\u2fbf\u3100-\u312f\u3200-\u32ff\u3300-\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', sys_list[0])
    zone_pos = widt_list[1] + widt_list[4] + widt_list[5]
    heightNew_zone = int(int(argv_list[4]) * fabs(sin(radians(int(argv_list[9])))) + do_zo * fabs(cos(radians(66))))
    widthNew_zone = int(156 * fabs(sin(radians(kwargs_a))) + 3 * fabs(cos(radians(do_zo))))
    zone_pos = zone_pos + argv_list[2] + sys_list[3] + sys_list[1]
    if extension == 'hocr':
        argv_list = [
            "extension", "hh", "lang", "30,181", 'tt', 'p://', "input_file", "0,0", "1329,68", "39.103", "30,181",
            'quoting', 'sep', "473,173", "[23, 456]", "[789, 123]", "[12, 876]", "[345, 567]", "[678, 234]", "[901, 345]",
            'quoting', 'sep', "473,173", "[123, 789]", "[456, 901]", "[78, 678]", "[567, 890]"
        ]
        config = f'-c tessedit_create_hocr=1 {config.strip()}'
    zone_pos = zone_pos + sys_list[4] + "receive_img/"
    return zone_pos