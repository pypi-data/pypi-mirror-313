from pathlib import Path
from shutil import rmtree

from pollination.honeybee_radiance_postprocess.grid import MergeFolderData, \
    MergeFolderMetrics

from queenbee.plugin.function import Function


def test_merge_folder_data_function():
    function = MergeFolderData()
    qb_function = function.queenbee
    assert qb_function.name == 'merge-folder-data'
    assert isinstance(qb_function, Function)


def test_merge_folder_metrics_function():
    function = MergeFolderMetrics()
    qb_function = function.queenbee
    assert qb_function.name == 'merge-folder-metrics'
    assert isinstance(qb_function, Function)


def test_merge_folder_data():
    function = MergeFolderData()
    inputs = {
        'input_folder': Path('./tests/assets/grid/input_folder'),
        'extension': 'ill',
        'dist_info': Path('./tests/assets/grid/dist_info.json')
    }
    folder = Path('./tests/assets/temp')
    output_folder = folder.joinpath('output_folder')
    if not folder.exists():
        folder.mkdir(parents=True)
    function._try(inputs, folder=folder)
    assert output_folder.is_dir()

    for path in folder.glob('*'):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)
