from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class AbntNbr15575Daylight(Function):
    """Post-processing for ABNT NBR 15575."""

    folder = Inputs.folder(
        description='Simulation folder for a ABNT NBR 15575 simulation. It '
        'should contain four sub-folder of complete point-in-time illuminance '
        'simulations labeled "4_930AM", "4_330PM", "10_930AM", and "10_330PM". '
        'These sub-folder should each have results folder that include a '
        'grids_info.json and .res files with illuminance values for each sensor.',
        path='results'
    )

    model = Inputs.file(
        description='Path to HBJSON file. This file is used to extract the '
        'center points of the sensor grids. It is a requirement that the sensor '
        'grids have Meshes.',
        path='model.hbjson'
    )

    ground_level = Inputs.float(
        description='A value to define the height of the ground level. This '
        'will make sure that rooms below this height will not be counted as '
        'ground level rooms',
        default=0
    )

    room_center = Inputs.str(
        default='room',
        description='An input to indicate if the evaluation of the center is at '
        'the center of the room or the center of the grid.',
        spec={'type': 'string', 'enum': ['room', 'grid']}
    )

    @command
    def abnt_nbr_15575_daylight(self):
        return 'honeybee-radiance-postprocess post-process abnt abnt-nbr-15575 ' \
            'results model.hbjson --ground-level {{self.ground_level}} ' \
            '--{{self.room_center}}-center --sub-folder abnt_nbr_15575'

    # outputs
    abnt_nbr_15575 = Outputs.folder(
        description='Folder with the ABNT NBR 15575 post-processing.',
        path='abnt_nbr_15575'
    )

    abnt_nbr_15575_summary = Outputs.file(
        description='CSV file containing the illuminance level and the '
        'illuminance at the center of the sensor grid.',
        path='abnt_nbr_15575/abnt_nbr_15575_rooms.csv'
    )

    center_points = Outputs.file(
        description='JSON file containing the center points used in the '
        'evaluation of illuminance.',
        path='abnt_nbr_15575/center_points.json'
    )

    illuminance_levels = Outputs.folder(
        description='A folder where illuminance results are mapped to an integer '
        'value noting the illuminance level. There are four different levels.',
        path='abnt_nbr_15575/illuminance_levels'
    )
