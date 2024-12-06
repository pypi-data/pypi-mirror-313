from dataclasses import dataclass
from pollination_dsl.dag import Inputs, DAG, task, Outputs

# input/output alias
from pollination.alias.inputs.model import hbjson_model_grid_input
from pollination.alias.inputs.wea import wea_input
from pollination.alias.inputs.north import north_input
from pollination.alias.inputs.radiancepar import rad_par_annual_input
from pollination.alias.inputs.grid import grid_filter_input, \
    min_sensor_count_input, cpu_count

from ._prepare_folder import TwoPhasePrepareFolder
from .two_phase.entry import TwoPhaseSimulation


@dataclass
class TwoPhaseDaylightCoefficientEntryPoint(DAG):
    """Annual daylight entry point."""

    # inputs
    north = Inputs.float(
        default=0,
        description='A number between -360 and 360 for the counterclockwise '
        'difference between the North and the positive Y-axis in degrees. This '
        'can also be a Vector for the direction to North. (Default: 0).',
        spec={'type': 'number', 'minimum': -360, 'maximum': 360},
        alias=north_input
    )

    cpu_count = Inputs.int(
        default=50,
        description='The maximum number of CPUs for parallel execution. This will be '
        'used to determine the number of sensors run by each worker.',
        spec={'type': 'integer', 'minimum': 1},
        alias=cpu_count
    )

    min_sensor_count = Inputs.int(
        description='The minimum number of sensors in each sensor grid after '
        'redistributing the sensors based on cpu_count. This value takes '
        'precedence over the cpu_count and can be used to ensure that '
        'the parallelization does not result in generating unnecessarily small '
        'sensor grids. The default value is set to 1, which means that the '
        'cpu_count is always respected.', default=500,
        spec={'type': 'integer', 'minimum': 1},
        alias=min_sensor_count_input
    )

    radiance_parameters = Inputs.str(
        description='The radiance parameters for ray tracing.',
        default='-ab 2 -ad 5000 -lw 2e-05 -dr 0',
        alias=rad_par_annual_input
    )

    grid_filter = Inputs.str(
        description='Text for a grid identifier or a pattern to filter the sensor grids '
        'of the model that are simulated. For instance, first_floor_* will simulate '
        'only the sensor grids that have an identifier that starts with '
        'first_floor_. By default, all grids in the model will be simulated.',
        default='*',
        alias=grid_filter_input
    )

    model = Inputs.file(
        description='A Honeybee Model JSON file (HBJSON) or a Model pkl (HBpkl) file. '
        'This can also be a zipped version of a Radiance folder, in which case this '
        'recipe will simply unzip the file and simulate it as-is.',
        extensions=['json', 'hbjson', 'pkl', 'hbpkl', 'zip'],
        alias=hbjson_model_grid_input
    )

    wea = Inputs.file(
        description='Wea file.',
        extensions=['wea', 'epw'],
        alias=wea_input
    )

    timestep = Inputs.int(
        description='Input wea timestep.', default=1,
        spec={'type': 'integer', 'minimum': 1, 'maximum': 60}
    )

    @task(template=TwoPhasePrepareFolder)
    def prepare_folder_annual_daylight(
        self, north=north, cpu_count=cpu_count, min_sensor_count=min_sensor_count,
        grid_filter=grid_filter, model=model, wea=wea, timestep=timestep
        ):
        return [
            {
                'from': TwoPhasePrepareFolder()._outputs.model_folder,
                'to': 'model'
            },
            {
                'from': TwoPhasePrepareFolder()._outputs.resources,
                'to': 'resources'
            },
            {
                'from': TwoPhasePrepareFolder()._outputs.results,
                'to': 'results'
            },
            {
                'from': TwoPhasePrepareFolder()._outputs.two_phase_info
            }
        ]

    @task(
        template=TwoPhaseSimulation,
        loop=prepare_folder_annual_daylight._outputs.two_phase_info,
        needs=[prepare_folder_annual_daylight],
        sub_folder='calcs/2_phase/{{item.identifier}}',
        sub_paths={
            'octree_file': 'dynamic/octree/{{item.octree}}',
            'octree_file_direct': 'dynamic/octree/{{item.octree_direct}}',
            'octree_file_with_suns': 'dynamic/octree/{{item.octree_direct_sun}}',
            'sensor_grids_folder': 'dynamic/grid/{{item.sensor_grids_folder}}',
            'sky_dome': 'sky.dome',
            'total_sky': 'sky.mtx',
            'direct_sky': 'sky_direct.mtx',
            'sun_modifiers': 'suns.mod',
            'bsdf_folder': 'bsdf'
        }
    )
    def calculate_two_phase_matrix(
        self,
        identifier='{{item.identifier}}',
        light_path='{{item.light_path}}',
        radiance_parameters=radiance_parameters,
        sensor_grids_info='{{item.sensor_grids_info}}',
        sensor_grids_folder=prepare_folder_annual_daylight._outputs.resources,
        octree_file=prepare_folder_annual_daylight._outputs.resources,
        octree_file_direct=prepare_folder_annual_daylight._outputs.resources,
        octree_file_with_suns=prepare_folder_annual_daylight._outputs.resources,
        sky_dome=prepare_folder_annual_daylight._outputs.resources,
        total_sky=prepare_folder_annual_daylight._outputs.resources,
        direct_sky=prepare_folder_annual_daylight._outputs.resources,
        sun_modifiers=prepare_folder_annual_daylight._outputs.resources,
        bsdf_folder=prepare_folder_annual_daylight._outputs.model_folder,
        results_folder='../../../results'
    ):
        pass

    results = Outputs.folder(
        source='results', description='Folder with raw result files (.ill) that '
        'contain illuminance matrices for each sensor at each timestep of the analysis.'
    )
