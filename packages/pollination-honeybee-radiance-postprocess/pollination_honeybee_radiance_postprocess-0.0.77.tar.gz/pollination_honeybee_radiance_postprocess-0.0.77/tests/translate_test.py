from pathlib import Path
from shutil import rmtree

from pollination.honeybee_radiance_postprocess.translate import BinaryToNpy, \
    TxtToNpy, NpyToTxt

from queenbee.plugin.function import Function


def test_binary_to_npy():
    function = BinaryToNpy()
    qb_function = function.queenbee
    assert qb_function.name == 'binary-to-npy'
    assert isinstance(qb_function, Function)


def test_txt_to_npy():
    function = TxtToNpy()
    qb_function = function.queenbee
    assert qb_function.name == 'txt-to-npy'
    assert isinstance(qb_function, Function)


def test_npy_to_txt():
    function = NpyToTxt()
    qb_function = function.queenbee
    assert qb_function.name == 'npy-to-txt'
    assert isinstance(qb_function, Function)


def test_binary_to_npy_convert():
    function = BinaryToNpy()
    inputs = {
        'matrix_file': Path('./tests/assets/translate/results.ill')
    }
    folder = Path('./tests/assets/temp')
    output_file = folder.joinpath('output.npy')
    if not folder.exists():
        folder.mkdir(parents=True)
    function._try(inputs, folder=folder)
    assert output_file.is_file()

    for path in folder.glob('*'):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)


def test_txt_to_npy_convert():
    function = TxtToNpy()
    inputs = {
        'txt_file': Path('./tests/assets/translate/results.txt')
    }
    folder = Path('./tests/assets/temp')
    output_file = folder.joinpath('output.npy')
    if not folder.exists():
        folder.mkdir(parents=True)
    function._try(inputs, folder=folder)
    assert output_file.is_file()

    for path in folder.glob('*'):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)


def test_npy_to_txt_convert():
    function = NpyToTxt()
    inputs = {
        'npy_file': Path('./tests/assets/translate/illuminance.npy')
    }
    folder = Path('./tests/assets/temp')
    output_file = folder.joinpath('output.txt')
    if not folder.exists():
        folder.mkdir(parents=True)
    function._try(inputs, folder=folder)
    assert output_file.is_file()

    for path in folder.glob('*'):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)
