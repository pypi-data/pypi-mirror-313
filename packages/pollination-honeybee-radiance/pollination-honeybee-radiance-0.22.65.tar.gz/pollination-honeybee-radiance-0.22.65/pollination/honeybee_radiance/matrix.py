from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class MatrixMultiplication(Function):
    """Multiply a matrix with conversation numbers."""
    conversion = Inputs.str(
        description='conversion as a string which will be passed to -c',
        default='47.4 119.9 11.6'
    )

    input_matrix = Inputs.file(
        description='Path to input matrix.', path='input.ill'
    )

    output_format = Inputs.str(default='-fa')

    @command
    def create_matrix(self):
        return 'rmtxop {{self.output_format}} input.ill -c {{self.conversion}} | ' \
            'getinfo - > output.ill'

    output_matrix = Outputs.file(description='New matrix file.', path='output.ill')


@dataclass
class MatrixMultiplicationThreePhase(Function):
    """Three phase matrix multiplication between view, daylight, transmission and sky
    matrices."""

    sky_vector = Inputs.file(
        description='Path to sky vector.', path='sky.smx'
    )

    view_matrix = Inputs.file(
        description='Path to view matrix.', path='view.vmx'
    )

    t_matrix = Inputs.file(
        description='Path to input matrix.', path='t.xml'
    )

    daylight_matrix = Inputs.file(
        description='Path to daylight matrix.', path='day.dmx'
    )

    output_format = Inputs.str(
        description='Output format for output matrix. Valid inputs are a, f, d '
        'and c for ASCII, float, double or RGBE colors.', default='a'
    )

    conversion = Inputs.str(
        description='A flag to convert the result to illuminance. Default is '
        'illuminance to convert from RGB to illuminance. Use raw to keep the '
        'results in RGB triplets.',
        spec={'type': 'string', 'enum': ['illuminance', 'raw']},
        default='illuminance'
    )

    header = Inputs.str(
        default='remove',
        description='An input to indicate if header should be kept or removed from the'
        'output matrix.', spec={'type': 'string', 'enum': ['keep', 'remove']}
    )

    @command
    def matrix_multiply(self):
        return 'honeybee-radiance multi-phase three-phase rmtxop view.vmx t.xml ' \
            'day.dmx sky.smx output.res --output-format {{self.output_format}} ' \
            '--{{self.conversion}} --{{self.header}}-header'

    output_matrix = Outputs.file(description='Three phase result.', path='output.res')
