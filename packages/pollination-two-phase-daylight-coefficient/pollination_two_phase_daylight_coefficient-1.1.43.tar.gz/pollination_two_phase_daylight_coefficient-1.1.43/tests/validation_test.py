from pollination.two_phase_daylight_coefficient.entry import TwoPhaseDaylightCoefficientEntryPoint
from queenbee.recipe.dag import DAG


def test_two_phase_daylight_coefficient():
    recipe = TwoPhaseDaylightCoefficientEntryPoint().queenbee
    assert recipe.name == 'two-phase-daylight-coefficient-entry-point'
    assert isinstance(recipe, DAG)
