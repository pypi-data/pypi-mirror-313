from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class MergeFolderData(Function):
    """Restructure files in a distributed folder."""

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

    output_extension = Inputs.str(
        description='Output file extension. This is only used if as_text is set '
        'to True. Otherwise the output extension will be npy.', default='ill'
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
        return 'honeybee-radiance-postprocess grid merge-folder ./input_folder ' \
            './output_folder {{self.extension}} --dist-info dist_info.json ' \
            '--output-extension {{self.output_extension}} --as-text {{self.as_text}} ' \
            '--fmt {{self.fmt}} --delimiter {{self.delimiter}}'


    output_folder = Outputs.folder(
        description='Output folder with newly generated files.', path='output_folder'
    )


@dataclass
class MergeFolderMetrics(Function):
    """Restructure annual daylight metrics in a distributed folder."""

    input_folder = Inputs.folder(
        description='Input sensor grids folder.',
        path='input_folder'
    )

    dist_info = Inputs.file(
        description='Distribution information file.',
        path='dist_info.json', optional=True
    )

    grids_info = Inputs.file(
        description='Grid information file.',
        path='grids_info.json', optional=True
    )

    @command
    def merge_metrics_in_folder(self):
        return 'honeybee-radiance-postprocess grid merge-folder-metrics ' \
            './input_folder ./output_folder --dist-info dist_info.json ' \
            '--grids-info grids_info.json'

    output_folder = Outputs.folder(
        description='Output folder with newly generated files.', path='output_folder'
    )
