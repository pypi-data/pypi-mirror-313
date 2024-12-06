from dataclasses import dataclass
from pollination_dsl.dag import Inputs, GroupedDAG, task, Outputs
from pollination.honeybee_radiance.sun import CreateSunMtx, ParseSunUpHours
from pollination.honeybee_radiance.translate import CreateRadianceFolderGrid
from pollination.honeybee_radiance.sky import CreateSkyDome, CreateSkyMatrix
from pollination.honeybee_radiance.multiphase import PrepareMultiphase
from pollination.honeybee_radiance.study import StudyInfo

# input/output alias
from pollination.alias.inputs.model import hbjson_model_grid_input
from pollination.alias.inputs.wea import wea_input
from pollination.alias.inputs.north import north_input
from pollination.alias.inputs.grid import grid_filter_input, \
    min_sensor_count_input, cpu_count


@dataclass
class TwoPhasePrepareFolder(GroupedDAG):
    """Prepare folder for two phase daylight coefficient."""

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
        description='The number of processors to be used as a result of the '
        'grid-splitting operation. This value is equivalent to the number of '
        'sensor grids that will be generated when the cpus-per-grid is left as 1.',
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

    @task(template=CreateSunMtx)
    def generate_sunpath(self, north=north, wea=wea):
        """Create sunpath for sun-up-hours."""
        return [
            {
                'from': CreateSunMtx()._outputs.sunpath,
                'to': 'resources/sunpath.mtx'
            },
            {
                'from': CreateSunMtx()._outputs.sun_modifiers,
                'to': 'resources/suns.mod'
            }
        ]

    @task(template=CreateRadianceFolderGrid, annotations={'main_task': True})
    def create_rad_folder(self, input_model=model, grid_filter=grid_filter):
        """Translate the input model to a radiance folder."""
        return [
            {
                'from': CreateRadianceFolderGrid()._outputs.model_folder,
                'to': 'model'
            },
            {
                'from': CreateRadianceFolderGrid()._outputs.sensor_grids_file,
                'to': 'results/grids_info.json'
            }
        ]

    @task(template=CreateSkyDome)
    def create_sky_dome(self):
        """Create sky dome for daylight coefficient studies."""
        return [
            {
                'from': CreateSkyDome()._outputs.sky_dome,
                'to': 'resources/sky.dome'
            }
        ]

    @task(template=CreateSkyMatrix)
    def create_total_sky(self, north=north, wea=wea, sun_up_hours='sun-up-hours'):
        return [
            {
                'from': CreateSkyMatrix()._outputs.sky_matrix,
                'to': 'resources/sky.mtx'
            }
        ]

    @task(template=CreateSkyMatrix)
    def create_direct_sky(
        self, north=north, wea=wea, sky_type='sun-only', sun_up_hours='sun-up-hours'
    ):
        return [
            {
                'from': CreateSkyMatrix()._outputs.sky_matrix,
                'to': 'resources/sky_direct.mtx'
            }
        ]

    @task(template=ParseSunUpHours, needs=[generate_sunpath])
    def parse_sun_up_hours(self, sun_modifiers=generate_sunpath._outputs.sun_modifiers):
        return [
            {
                'from': ParseSunUpHours()._outputs.sun_up_hours,
                'to': 'results/sun-up-hours.txt'
            }
        ]

    @task(template=StudyInfo)
    def create_study_info(self, wea=wea, timestep=timestep):
        return [
            {
                'from': StudyInfo()._outputs.study_info,
                'to': 'results/study_info.json'
            }
        ]

    @task(
        template=PrepareMultiphase,
        needs=[create_rad_folder, generate_sunpath]
    )
    def prepare_multiphase(
        self, model=create_rad_folder._outputs.model_folder,
        sunpath=generate_sunpath._outputs.sunpath, phase=2,
        cpu_count=cpu_count, cpus_per_grid=3,
        min_sensor_count=min_sensor_count, static='include'
    ):
        return [
            {
                'from': PrepareMultiphase()._outputs.scene_folder,
                'to': 'resources/dynamic/octree'
            },
            {
                'from': PrepareMultiphase()._outputs.grid_folder,
                'to': 'resources/dynamic/grid'
            },
            {
                'from': PrepareMultiphase()._outputs.two_phase_info,
                'to': 'resources/two_phase.json'
            },
            {   'from': PrepareMultiphase()._outputs.grid_states_file,
                'to': 'results/grid_states.json'
            }
        ]

    two_phase_info = Outputs.list(source='resources/two_phase.json')

    model_folder = Outputs.folder(
        source='model', description='input model folder folder.'
    )

    resources = Outputs.folder(
        source='resources', description='resources folder.'
    )

    results = Outputs.folder(
        source='results', description='results folder.'
    )
