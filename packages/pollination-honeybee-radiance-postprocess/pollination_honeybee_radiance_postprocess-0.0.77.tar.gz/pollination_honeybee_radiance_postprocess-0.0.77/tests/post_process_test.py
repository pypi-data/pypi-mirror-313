from pathlib import Path
from shutil import rmtree

from pollination.honeybee_radiance_postprocess.post_process import \
    AnnualDaylightMetrics, AnnualDaylightEn17037Metrics, \
    AnnualDaylightMetricsFile, AnnualIrradianceMetrics

from queenbee.plugin.function import Function


def test_annual_daylight_metrics():
    function = AnnualDaylightMetrics()
    qb_function = function.queenbee
    assert qb_function.name == 'annual-daylight-metrics'
    assert isinstance(qb_function, Function)


def test_annual_daylight_en17037_metrics():
    function = AnnualDaylightEn17037Metrics()
    qb_function = function.queenbee
    assert qb_function.name == 'annual-daylight-en17037-metrics'
    assert isinstance(qb_function, Function)


def test_annual_daylight_metrics_file():
    function = AnnualDaylightMetricsFile()
    qb_function = function.queenbee
    assert qb_function.name == 'annual-daylight-metrics-file'
    assert isinstance(qb_function, Function)


def test_annual_daylight_metrics_file_calculate():
    function = AnnualDaylightMetricsFile()
    inputs = {
        'file': Path('./tests/assets/post_process/annual_daylight_metrics_file/total.npy'),
        'sun_up_hours': Path('./tests/assets/post_process/annual_daylight_metrics_file/sun-up-hours.txt'),
        'schedule': Path('./tests/assets/post_process/annual_daylight_metrics_file/schedule.csv'),
        'study_info': Path('./tests/assets/post_process/annual_daylight_metrics_file/study_info.json')
    }
    folder = Path('./tests/assets/temp')
    output_folder = folder.joinpath('metrics')
    output_file = output_folder.joinpath('da', 'grid.da')
    if not folder.exists():
        folder.mkdir(parents=True)
    function._try(inputs, folder=folder)
    assert output_folder.is_dir()
    assert output_file.is_file()

    for path in folder.glob('*'):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)


def test_annual_irradiance_metrics():
    function = AnnualIrradianceMetrics()
    inputs = {
        'folder': Path('./tests/assets/results/results_irradiance')
    }
    folder = Path('./tests/assets/temp')
    output_folder = folder.joinpath('metrics')
    output_file = output_folder.joinpath(
        'average_irradiance', 'TestRoom_1.res')
    if not folder.exists():
        folder.mkdir(parents=True)
    function._try(inputs, folder=folder)
    assert output_folder.is_dir()
    assert output_file.is_file()

    for path in folder.glob('*'):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)
