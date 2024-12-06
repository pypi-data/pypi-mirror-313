from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class OperateTwo(Function):
    """Operations between two Radiance matrices."""
    first_mtx = Inputs.file(
        description='Path to Radiance matrix.',
        path='mtx_1.mtx'
    )

    second_mtx = Inputs.file(
        description='Path to Radiance matrix.',
        path='mtx_2.mtx'
    )

    operator = Inputs.str(
        description='Operation between the two matrices.',
        spec={'type': 'string', 'enum': ['+', '-', '/', '*']},
        default='+'
    )

    conversion = Inputs.str(
        description='Conversion as a string which will be passed to rmtxop -c '
        'option.',
        default=''
    )

    binary = Inputs.str(
        description='Switch between binary and ascii input matrices. Default '
        'is binary.',
        spec={'type': 'string', 'enum': ['binary', 'ascii']},
        default='binary'
    )

    @command
    def operate_two(self):
        return 'honeybee-radiance-postprocess mtxop operate-two ' \
            'mtx_1.mtx mtx_2.mtx --operator {{self.operator}} ' \
            '--conversion "{{self.conversion}}" --{{self.binary}} ' \
            '--name output' \

    output_matrix = Outputs.file(
        description='Output matrix file.', path='output.npy'
    )


@dataclass
class OperateThree(Function):
    """Operations between three Radiance matrices."""
    first_mtx = Inputs.file(
        description='Path to Radiance matrix.',
        path='mtx_1.mtx'
    )

    second_mtx = Inputs.file(
        description='Path to Radiance matrix.',
        path='mtx_2.mtx'
    )

    third_mtx = Inputs.file(
        description='Path to Radiance matrix.',
        path='mtx_3.mtx'
    )

    operator_one = Inputs.str(
        description='Operation between matrix one and two.',
        spec={'type': 'string', 'enum': ['+', '-', '/', '*']},
        default='+'
    )

    operator_two = Inputs.str(
        description='Operation between matrix two and three.',
        spec={'type': 'string', 'enum': ['+', '-', '/', '*']},
        default='+'
    )

    conversion = Inputs.str(
        description='Conversion as a string which will be passed to rmtxop -c '
        'option.',
        default=''
    )

    binary = Inputs.str(
        description='Switch between binary and ascii input matrices. Default '
        'is binary.',
        spec={'type': 'string', 'enum': ['binary', 'ascii']},
        default='binary'
    )

    @command
    def operate_two(self):
        return 'honeybee-radiance-postprocess mtxop operate-three ' \
            'mtx_1.mtx mtx_2.mtx mtx_3.mtx --operator-one ' \
            '{{self.operator_one}} --operator-two {{self.operator_two}} ' \
            '--conversion "{{self.conversion}}" --{{self.binary}} ' \
            '--name output' \

    output_matrix = Outputs.file(
        description='Output matrix file.', path='output.npy'
    )
