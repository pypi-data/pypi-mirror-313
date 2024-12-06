from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class DaylightOptionOne(Function):
    """Calculate credits for LEED v4.1 Daylight Option 1.

    Use the shade-transmittance option to set a shade transmittance values for
    aperture groups. The shade-transmittance-file option takes precedence over
    the shade-transmittance, however, if any aperture groups are missing in the
    JSON file given to the shade-transmittance-file option, the value from
    shade-transmittance will be used for those aperture groups.
    """

    folder = Inputs.folder(
        description='This folder is an output folder of annual daylight recipe. Folder '
        'should include grids_info.json and sun-up-hours.txt. The command uses the list '
        'in grids_info.json to find the result files for each sensor grid.',
        path='results'
    )

    grid_filter = Inputs.str(
        description='Text for a grid identifier or a pattern to filter the sensor grids '
        'of the model.',
        default='*'
    )

    shade_transmittance = Inputs.float(
        description='A value to use as a multiplier in place of solar shading. Value '
        'for shade transmittance must be 1 > value > 0.', default=0.02
    )

    shd_transmittance_file = Inputs.file(
        description='A JSON file with a dictionary where aperture groups are keys, and '
        'the value for each key is the shade transmittance. Values for shade '
        'transmittance must be 1 > value > 0.',
        path='shade_transmittance.json', extensions=['json'], optional=True
    )

    blind_postprocess = Inputs.str(
        description='A flag to select if the post-processing should use a '
        'shade transmittance or the simulated states of aperture groups. Using '
        'states should only be selected if the annual daylight simulation '
        'included ray tracing of a second (blind) state for each aperture group.',
        default='shade-transmittance',
        spec={'type': 'string', 'enum': ['shade-transmittance', 'states']}
    )

    model = Inputs.file(
        description='Path to HBJSON file. The purpose of the model in this function is '
        'to use the mesh area of the sensor grids to calculate area-weighted metrics. '
        'In case no model is provided or the sensor grids in the model do not have any '
        'mesh area, it will be assumed that all sensor points cover the same area.',
        path='model.hbjson', optional=True
    )

    @command
    def leed_daylight_option_one(self):
        return 'honeybee-radiance-postprocess post-process leed daylight-option-one ' \
            'results --shade-transmittance {{self.shade_transmittance}} ' \
            '--shade-transmittance-file shade_transmittance.json ' \
            '--use-{{self.blind_postprocess}} --sub-folder leed_summary'

    # outputs
    leed_summary = Outputs.folder(
        description='Annual metrics folder. This folder includes all the other '
        'sub-folders which are also exposed as separate outputs.',
        path='leed_summary'
    )
