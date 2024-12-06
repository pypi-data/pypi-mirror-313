from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class SphericalViewFactorContribution(Function):
    """Calculate spherical view factor contribution for a grid of sensors."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters. -I and -aa 0 are already included in '
        'the command.', default=''
    )

    fixed_radiance_parameters = Inputs.str(
        description='Radiance parameters. -I and -aa 0 are already included in '
        'the command.', default='-aa 0'
    )

    ray_count = Inputs.int(
        description='The number of rays to be equally distributed over a sphere '
        'to compute the view factor for each of the input sensors.', default=6,
        spec={'type': 'integer', 'minimum': 2}
    )

    modifiers = Inputs.file(
        description='Path to modifiers file. In most cases modifiers are sun modifiers.',
        path='scene.mod'
    )

    sensor_grid = Inputs.file(
        description='Path to sensor grid files.', path='grid.pts',
        extensions=['pts']
    )

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct',
        extensions=['oct']
    )

    @command
    def run_daylight_coeff(self):
        return 'honeybee-radiance-postprocess view-factor contrib scene.oct ' \
            'grid.pts scene.mod --ray-count {{self.ray_count}} ' \
            '--rad-params "{{self.radiance_parameters}}" ' \
            '--rad-params-locked "{{self.fixed_radiance_parameters}}" --name view_factor'

    view_factor_file = Outputs.file(
        description='Output file with a matrix of spherical view factors from the '
        'sensors to the modifiers.', path='view_factor.npy'
    )
