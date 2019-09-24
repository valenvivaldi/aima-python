from missionaries_cannibals import *
import pytest


# Simple unit tests example
def test_is_enabled_returns_false():
    act = MissionariesLeftToRight(1)
    state = (3, 3, 1, 1, 0)
    assert not act.is_enabled(state)


def test_is_enabled_returns_true():
    act = MissionariesLeftToRight(1)
    state = (3, 2, 1, 1, 0)
    assert act.is_enabled(state)
    assert (2, 2, 2, 1, 1) == act.execute(state)


# Parameterized tests example
def params_enabled_returns_true():
    return [((1, 0, 1, 0, 0), (0, 0, 2, 0, 1)),
            ((3, 2, 1, 1, 0), (2, 2, 2, 1, 1))]


@pytest.mark.parametrize("state, expected", params_enabled_returns_true())
def test_parameterized_enabled_returns_true(state, expected):
    act = MissionariesLeftToRight(1)
    assert act.is_enabled(state)
    assert expected == act.execute(state)


# Fixture example
@pytest.fixture
def mltor1_act():
    return MissionariesLeftToRight(1)


def test_is_enabled_returns_false_fixture(mltor1_act):
    state = (3, 3, 1, 1, 0)
    assert not mltor1_act.is_enabled(state)


def test_is_enabled_returns_true_fixture(mltor1_act):
    state = (3, 2, 1, 1, 0)
    assert mltor1_act.is_enabled(state)
    assert (2, 2, 2, 1, 1) == mltor1_act.execute(state)