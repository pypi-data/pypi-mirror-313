from pathlib import Path
from shutil import rmtree

from pollination.honeybee_radiance_postprocess.leed import DaylightOptionOne

from queenbee.plugin.function import Function


def test_daylight_option_one():
    function = DaylightOptionOne()
    qb_function = function.queenbee
    assert qb_function.name == 'daylight-option-one'
    assert isinstance(qb_function, Function)


def test_daylight_option_one_with_shade_transmittance_file():
    function = DaylightOptionOne()
    inputs = {
        'folder': Path('./tests/assets/leed/results'),
        'model': Path('./tests/assets/leed/hb_sample_model_leed.hbjson'),
        'shd_transmittance_file': Path('./tests/assets/leed/shd.json')
    }
    folder = Path('./tests/assets/temp')
    output_folder = folder.joinpath('leed_summary')
    if not folder.exists():
        folder.mkdir(parents=True)
    function._try(inputs, folder=folder)
    assert output_folder.is_dir()

    for path in folder.glob('*'):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)
