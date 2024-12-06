from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class CreateRadianceFolder(Function):
    """Create a Radiance folder from a HBJSON input file.

    This function creates the folder but doesn't expose information for sensor grids
    and views.
    """

    input_model = Inputs.file(
        description='Path to input HBJSON file.',
        path='model.hbjson'
    )

    grid_filter = Inputs.str(
        description='Text for a grid identifier or a pattern to filter the sensor grids '
        'of the model that are simulated. For instance, first_floor_* will simulate '
        'only the sensor grids that have an identifier that starts with '
        'first_floor_. By default, all grids in the model will be simulated.',
        default='*'
    )

    view_filter = Inputs.str(
        description='Text for a view identifier or a pattern to filter the views '
        'of the model that are simulated. For instance, first_floor_* will simulate '
        'only the views that have an identifier that starts with first_floor_. By '
        'default, all views in the model will be simulated.', default='*'
    )

    @command
    def hbjson_to_rad_folder(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson ' \
            '--grid " {{self.grid_filter}} " --view "{{self.view_filter}}"'

    model_folder = Outputs.folder(description='Radiance folder.', path='model')

    receivers = Outputs.list(
        description='Information for all the receivers.',
        path='model/receiver/_info.json', optional=True
    )


@dataclass
class CreateRadianceFolderGrid(Function):
    """Create a Radiance folder from a HBJSON input file."""

    input_model = Inputs.file(
        description='Path to input HBJSON file.',
        path='model.hbjson'
    )

    grid_filter = Inputs.str(
        description='Text for a grid identifier or a pattern to filter the sensor grids '
        'of the model that are simulated. For instance, first_floor_* will simulate '
        'only the sensor grids that have an identifier that starts with '
        'first_floor_. By default, all grids in the model will be simulated.',
        default='*'
    )

    @command
    def hbjson_to_rad_folder(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson ' \
            '--grid " {{self.grid_filter}} " --grid-check'

    model_folder = Outputs.folder(description='Radiance folder.', path='model')

    bsdf_folder = Outputs.folder(
        description='Folder containing any BSDF files needed for the simulation.',
        path='model/bsdf', optional=True
    )

    sensor_grids = Outputs.list(
        description='Information for exported sensor grids in grids subfolder.',
        path='model/grid/_info.json'
    )

    sensor_grids_file = Outputs.file(
        description='Information JSON file for exported sensor grids in grids '
        'subfolder.', path='model/grid/_info.json'
    )

    model_sensor_grids = Outputs.list(
        description='Sensor grids information from the HB model.',
        path='model/grid/_model_grids_info.json'
    )

    model_sensor_grids_file = Outputs.file(
        description='Sensor grids information from the HB model JSON file.',
        path='model/grid/_model_grids_info.json'
    )

    receivers = Outputs.list(
        description='Information for the states for all dynamic apertures.',
        path='model/receiver/_info.json', optional=True
    )


@dataclass
class CreateRadianceFolderView(Function):
    """Create a Radiance folder from a HBJSON input file."""

    input_model = Inputs.file(
        description='Path to input HBJSON file.',
        path='model.hbjson'
    )

    view_filter = Inputs.str(
        description='Text for a view identifier or a pattern to filter the views '
        'of the model that are simulated. For instance, first_floor_* will simulate '
        'only the views that have an identifier that starts with first_floor_. By '
        'default, all views in the model will be simulated.', default='*'
    )

    @command
    def hbjson_to_rad_folder(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson ' \
            '--view " {{self.view_filter}} " --view-check'

    model_folder = Outputs.folder(description='Radiance folder.', path='model')

    bsdf_folder = Outputs.folder(
        description='Folder containing any BSDF files needed for the simulation.',
        path='model/bsdf', optional=True
    )

    views = Outputs.list(
        description='Views information.', path='model/view/_info.json'
    )

    views_file = Outputs.file(
        description='Views information JSON file.', path='model/view/_info.json'
    )

    receivers = Outputs.list(
        description='Information for the states for all dynamic apertures.',
        path='model/receiver/_info.json', optional=True
    )


@dataclass
class CreateRadiantEnclosureInfo(Function):
    """Create JSONs with radiant enclosure information from a HBJSON input file.

    This enclosure info is intended to be consumed by thermal mapping functions.
    """

    model = Inputs.file(
        description='Path to input HBJSON file.',
        path='model.hbjson'
    )

    @command
    def hbjson_to_radiant_enclosure_info(self):
        return 'honeybee-radiance translate model-radiant-enclosure-info model.hbjson ' \
            '--folder output --log-file enclosure_list.json'

    enclosure_list = Outputs.dict(
        description='A list of dictionaries that include information about generated '
        'radiant enclosure files.', path='enclosure_list.json'
    )

    enclosure_list_file = Outputs.file(
        description='A JSON file that includes information about generated radiant '
        'enclosure files.', path='enclosure_list.json'
    )

    output_folder = Outputs.folder(
        description='Output folder with the enclosure info JSONs for each grid.',
        path='output'
    )
