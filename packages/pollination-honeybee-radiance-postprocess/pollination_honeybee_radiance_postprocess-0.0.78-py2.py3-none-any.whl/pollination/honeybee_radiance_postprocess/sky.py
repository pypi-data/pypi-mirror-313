from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class AddRemoveSkyMatrix(Function):
    """Multiply a matrix with conversation numbers."""
    total_sky_matrix = Inputs.file(
        description='Path to matrix for total sky contribution.',
        path='sky.ill', extensions=['ill', 'dc']
    )

    direct_sky_matrix = Inputs.file(
        description='Path to matrix for direct sky contribution.',
        path='sky_dir.ill', extensions=['ill', 'dc']
    )

    sunlight_matrix = Inputs.file(
        description='Path to matrix for direct sunlight contribution.',
        path='sun.ill', extensions=['ill', 'dc']
    )

    conversion = Inputs.str(
        description='Conversion as a string which will be passed to rmtxop -c option.',
        default=''
    )

    @command
    def create_matrix(self):
        return 'honeybee-radiance-postprocess mtxop operate-three ' \
            '"{{self.total_sky_matrix}}" "{{self.direct_sky_matrix}}" ' \
            '"{{self.sunlight_matrix}}" --operator-one - --operator-two + ' \
            '--conversion "{{self.conversion}}" --name output'

    results_file = Outputs.file(
        description='Results as a npy file.', path='output.npy'
    )
