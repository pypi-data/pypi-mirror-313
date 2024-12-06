from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class AnnualDaylightMetrics(Function):
    """Calculate annual daylight metrics for annual daylight simulation."""

    folder = Inputs.folder(
        description='This folder is an output folder of annual daylight recipe. Folder '
        'should include grids_info.json and sun-up-hours.txt. The command uses the list '
        'in grids_info.json to find the result files for each sensor grid.',
        path='raw_results'
    )

    schedule = Inputs.file(
        description='Path to an annual schedule file. Values should be 0-1 separated '
        'by new line. If not provided an 8-5 annual schedule will be created.',
        path='schedule.txt', optional=True
    )

    thresholds = Inputs.str(
        description='A string to change the threshold for daylight autonomy and useful '
        'daylight illuminance. Valid keys are -t for daylight autonomy threshold, -lt '
        'for the lower threshold for useful daylight illuminance and -ut for the upper '
        'threshold. The default is -t 300 -lt 100 -ut 3000. The order of the keys is not'
        ' important and you can include one or all of them. For instance if you only '
        'want to change the upper threshold to 2000 lux you should use -ut 2000 as '
        'the input.', default='-t 300 -lt 100 -ut 3000'
    )

    @command
    def calculate_annual_metrics(self):
        return 'honeybee-radiance-postprocess post-process annual-daylight ' \
            'raw_results --schedule schedule.txt {{self.thresholds}} ' \
            '--sub-folder metrics'

    # outputs
    annual_metrics = Outputs.folder(
        description='Annual metrics folder. This folder includes all the other '
        'sub-folders which are also exposed as separate outputs.', path='metrics'
    )

    daylight_autonomy = Outputs.folder(
        description='Daylight autonomy results.', path='metrics/da'
    )

    continuous_daylight_autonomy = Outputs.folder(
        description='Continuous daylight autonomy results.', path='metrics/cda'
    )

    useful_daylight_illuminance_lower = Outputs.folder(
        description='Lower useful daylight illuminance results.',
        path='metrics/udi_lower'
    )

    useful_daylight_illuminance = Outputs.folder(
        description='Useful daylight illuminance results.', path='metrics/udi'
    )

    useful_daylight_illuminance_upper = Outputs.folder(
        description='Upper useful daylight illuminance results.',
        path='metrics/udi_upper'
    )


@dataclass
class AnnualDaylightEn17037Metrics(Function):
    """Calculate annual daylight EN 173037 metrics for annual daylight simulation."""

    folder = Inputs.folder(
        description='This folder is an output folder of annual daylight recipe. Folder '
        'should include grids_info.json and sun-up-hours.txt. The command uses the list '
        'in grids_info.json to find the result files for each sensor grid.',
        path='raw_results'
    )

    schedule = Inputs.file(
        description='Path to an annual schedule file. Values should be 0-1 separated '
        'by new line. This should be a daylight hours schedule according to EN 17037.',
        path='schedule.txt'
    )

    @command
    def calculate_annual_metrics_en17037(self):
        return 'honeybee-radiance-postprocess post-process annual-daylight-en17037 ' \
            'raw_results schedule.txt --sub_folder metrics'

    # outputs
    annual_en17037_metrics = Outputs.folder(
        description='Annual EN 17037 metrics folder. This folder includes all the other '
        'subfolders which are also exposed as separate outputs.', path='metrics'
    )

    daylight_autonomy = Outputs.folder(
        description='Daylight autonomy results.', path='metrics/da'
    )

    spatial_daylight_autonomy = Outputs.folder(
        description='Spatial daylight autonomy results.', path='metrics/sda'
    )


@dataclass
class AnnualDaylightMetricsFile(Function):
    """Calculate annual daylight metrics for a single file."""

    file = Inputs.file(
        description='Annual illuminance file. This can be either a NumPy file '
        'or a binary Radiance file.',
        path='illuminance.ill'
    )

    sun_up_hours = Inputs.file(
        description='A text file that includes all the sun up hours. Each '
        'hour is separated by a new line.', path='sun-up-hours.txt'
    )

    schedule = Inputs.file(
        description='Path to an annual schedule file. Values should be 0-1 separated '
        'by new line. If not provided an 8-5 annual schedule will be created.',
        path='schedule.txt', optional=True
    )

    thresholds = Inputs.str(
        description='A string to change the threshold for daylight autonomy and useful '
        'daylight illuminance. Valid keys are -t for daylight autonomy threshold, -lt '
        'for the lower threshold for useful daylight illuminance and -ut for the upper '
        'threshold. The default is -t 300 -lt 100 -ut 3000. The order of the keys is not'
        ' important and you can include one or all of them. For instance if you only '
        'want to change the upper threshold to 2000 lux you should use -ut 2000 as '
        'the input.', default='-t 300 -lt 100 -ut 3000'
    )

    grid_name = Inputs.str(
        description='Optional name of each metric file.', default='grid'
    )

    study_info = Inputs.file(
        description='Optional study info file. This option is needed if the '
        'time step is larger than 1.', path='study_info.json', optional=True
    )

    @command
    def calculate_annual_metrics_file(self):
        return 'honeybee-radiance-postprocess post-process annual-daylight-file ' \
            'illuminance.ill sun-up-hours.txt --schedule schedule.txt ' \
            '{{self.thresholds}} --grid-name "{{self.grid_name}}" ' \
            '--study-info study_info.json --sub-folder metrics'

    # outputs
    annual_metrics = Outputs.folder(
        description='Annual metrics folder. This folder includes all the other '
        'sub-folders which are also exposed as separate outputs.', path='metrics'
    )

    daylight_autonomy = Outputs.folder(
        description='Daylight autonomy results.', path='metrics/da'
    )

    continuous_daylight_autonomy = Outputs.folder(
        description='Continuous daylight autonomy results.', path='metrics/cda'
    )

    useful_daylight_illuminance_lower = Outputs.folder(
        description='Lower useful daylight illuminance results.',
        path='metrics/udi_lower'
    )

    useful_daylight_illuminance = Outputs.folder(
        description='Useful daylight illuminance results.', path='metrics/udi'
    )

    useful_daylight_illuminance_upper = Outputs.folder(
        description='Upper useful daylight illuminance results.',
        path='metrics/udi_upper'
    )


@dataclass
class GridSummaryMetrics(Function):
    """Calculate grid summary for metrics."""

    folder = Inputs.folder(
        description='A folder with metrics.',
        path='metrics'
    )

    model = Inputs.file(
        description='Path to HBJSON file. The purpose of the model in this function is '
        'to use the mesh area of the sensor grids to calculate area-weighted metrics. '
        'In case no model is provided or the sensor grids in the model do not have any '
        'mesh area, it will be assumed that all sensor points cover the same area.',
        path='model.hbjson', optional=True
    )

    grids_info = Inputs.file(
        description='A JSON file with grid information.',
        path='grids_info.json', extensions=['json'], optional=True
    )

    grid_metrics = Inputs.file(
        description='A JSON file with additional custom metrics to calculate.',
        path='grid_metrics.json', extensions=['json'], optional=True
    )

    folder_level = Inputs.str(
        description='Use sub-folder to loop over all sub folders. Use '
        'main-folder if the metrics are in the main directory.',
        spec={'type': 'string', 'enum': ['sub-folder', 'main-folder']},
        default='sub-folder'
    )

    @command
    def grid_summary_metrics(self):
        return 'honeybee-radiance-postprocess post-process grid-summary ' \
            'metrics --model model.hbjson --grids-info grids_info.json ' \
            '--grid-metrics grid_metrics.json --{{self.folder_level}}'

    # outputs
    grid_summary = Outputs.file(
        description='Grid summary as csv file.', path='metrics/grid_summary.csv'
    )


@dataclass
class AnnualIrradianceMetrics(Function):
    """Calculate annual irradiance metrics for annual irradiance simulation."""

    folder = Inputs.folder(
        description='This folder is an output folder of annual daylight recipe. Folder '
        'should include grids_info.json and sun-up-hours.txt. The command uses the list '
        'in grids_info.json to find the result files for each sensor grid.',
        path='raw_results'
    )

    @command
    def calculate_annual_irradiance_metrics(self):
        return 'honeybee-radiance-postprocess post-process annual-irradiance ' \
            'raw_results --sub-folder metrics'

    # outputs
    annual_metrics = Outputs.folder(
        description='Annual metrics folder. This folder includes all the other '
        'sub-folders which are also exposed as separate outputs.', path='metrics'
    )

    average_irradiance = Outputs.folder(
        description='Average irradiance in W/m2 for each sensor over the wea '
        'period.', path='metrics/average_irradiance'
    )

    peak_irradiance = Outputs.folder(
        description='The cumulative radiation in kWh/m2 for each sensor over '
        'the wea period.', path='metrics/peak_irradiance'
    )

    cumulative_radiation = Outputs.folder(
        description='The cumulative radiation in kWh/m2 for each sensor over '
        'the wea period.', path='metrics/cumulative_radiation'
    )


@dataclass
class DirectSunHours(Function):
    """Calculate direct sun hours and cumulative direct sun hours.."""

    input_mtx = Inputs.file(
        description='Annual direct sun hours file. This can be either a NumPy '
        'file or a binary Radiance file.',
        path='direct_matrix.mtx'
    )

    divisor = Inputs.int(
        description='An optional number, that the summed row will be divided '
        'by. For example, this can be a timestep, which can be used to ensure '
        'that a summed row of irradiance yields cumulative radiation over the '
        'entire time period of the matrix.',
        default=1
    )

    @command
    def calculate_direct_sun_hours(self):
        return 'honeybee-radiance-postprocess post-process direct-sun-hours ' \
            'direct_matrix.mtx --divisor {{self.divisor}}'

    # outputs
    direct_sun_hours = Outputs.file(
        description='Direct sun hours as a NumPy file.',
        path='direct_sun_hours.npy'
    )

    cumulative_direct_sun_hours = Outputs.file(
        description='Cumulative direct sun hours as a text file.',
        path='cumulative.res'
    )
