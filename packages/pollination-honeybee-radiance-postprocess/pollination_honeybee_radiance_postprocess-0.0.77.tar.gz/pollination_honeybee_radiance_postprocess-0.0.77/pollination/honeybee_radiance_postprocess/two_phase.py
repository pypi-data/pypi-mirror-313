from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class ProcessTwoPhase(Function):
    """Multiply a matrix with conversation numbers. Output both total and
    direct results. The direct output is the direct sunlight contribution
    (not the direct sky contribution)."""
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

    @command
    def process_two_phase(self):
        return 'honeybee-radiance-postprocess post-process two-phase ' \
            'rgb-to-illuminance "{{self.total_sky_matrix}}" ' \
            '"{{self.direct_sky_matrix}}" "{{self.sunlight_matrix}}"' \

    total = Outputs.file(
        description='Total results as a npy file.', path='total.npy'
    )

    direct = Outputs.file(
        description='Direct results as a npy file.', path='direct.npy'
    )


@dataclass
class TwoPhaseAddRemoveSkyMatrix(Function):
    """Remove direct sky from total sky and add direct sun. Output both total and
    direct results. The direct output is the direct sunlight contribution
    (not the direct sky contribution)."""
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

    @command
    def add_remove_sky_matrix(self):
        return 'honeybee-radiance-postprocess post-process two-phase ' \
            'add-remove-sky-matrix "{{self.total_sky_matrix}}" ' \
            '"{{self.direct_sky_matrix}}" "{{self.sunlight_matrix}}"' \

    total = Outputs.file(
        description='Total results as a npy file.', path='total.npy'
    )

    direct = Outputs.file(
        description='Direct results as a npy file.', path='direct.npy'
    )
