from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class MergeFiles(Function):
    """Merge files in a distributed folder."""

    input_folder = Inputs.folder(
        description='Input sensor grids folder.',
        path='input_folder'
    )

    extension = Inputs.str(
        description='Extension of the files to collect data from. It will be ``pts`` '
        'for sensor files. Another common extension is ``ill`` for the results of '
        'daylight studies.'
    )

    dist_info = Inputs.file(
        description='Distribution information file.',
        path='dist_info.json', optional=True
    )

    merge_axis = Inputs.int(
        description='Merge files along axis.',
        spec={"enum": [0, 1, 2]}, default=0
    )

    as_text = Inputs.bool(
        description='Set to True if the output files should be saved as text '
        'instead of NumPy files.', default=False
    )

    fmt = Inputs.str(
        description='Format for the output files when saved as text.',
        default='%.2f'
    )

    delimiter = Inputs.str(
        description='Delimiter for the output files when saved as text.',
        spec={"enum": ["space", "tab"]}, default='tab'

    )

    @command
    def merge_files_in_folder(self):
        return 'honeybee-radiance-postprocess merge merge-files ./input_folder ' \
            '{{self.extension}} --output-file output --dist-info dist_info.json ' \
            '--merge-axis "{{self.merge_axis}}" --as-text {{self.as_text}} ' \
            '--fmt {{self.fmt}} --delimiter {{self.delimiter}}'


    output_file = Outputs.file(
        description='Output folder with newly generated files.',
        path='output.npy'
    )
