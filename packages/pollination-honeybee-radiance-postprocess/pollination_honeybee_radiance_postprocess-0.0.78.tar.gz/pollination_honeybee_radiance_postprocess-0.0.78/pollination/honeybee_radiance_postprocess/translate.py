from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class BinaryToNpy(Function):
    """Convert binary Radiance matrix file to NumPy file."""
    matrix_file = Inputs.file(
        description='Path to binary Radiance matrix file.',
        path='input.ill', extensions=['ill', 'dc']
    )

    conversion = Inputs.str(
        description='Conversion as a string which will be passed to rmtxop -c option.',
        default=''
    )

    @command
    def binary_to_npy(self):
        return 'honeybee-radiance-postprocess translate binary-to-npy ' \
            'input.ill --conversion "{{self.conversion}}" --name output'

    output_file = Outputs.file(
        description='Output as a npy file.', path='output.npy'
    )


@dataclass
class TxtToNpy(Function):
    """Convert a space or tab separated text file to npy file."""
    txt_file = Inputs.file(
        description='Path to txt file.', path='input.txt'
    )

    @command
    def txt_to_npy(self):
        return 'honeybee-radiance-postprocess translate txt-to-npy input.txt ' \
            '--name output'

    output_file = Outputs.file(
        description='Output as npy file.', path='output.npy'
    )


@dataclass
class NpyToTxt(Function):
    """Convert a npy file to text file."""
    npy_file = Inputs.file(
        description='Path to npy file.', path='input.npy'
    )

    @command
    def npy_to_txt(self):
        return 'honeybee-radiance-postprocess translate npy-to-txt input.npy ' \
            '--name output'

    output_file = Outputs.file(
        description='Output as a text file.', path='output.txt'
    )
