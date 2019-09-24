
from abc import ABC, abstractmethod
from search import Problem


class Action(ABC):

    @abstractmethod
    def execute(self, state):
        pass

    @abstractmethod
    def is_enabled(self, state):
        pass


class MissionariesLeftToRight(Action):

    def __init__(self, cant):
        self.cant = cant

    def execute(self, state):
        return state[0]-self.cant, state[1], state[2]+self.cant, state[3], 1

    def is_enabled(self, state):
        return state[0] >= self.cant and state[0]-self.cant >= state[1] and state[4] == 0


class MissionariesAndCannibals(Problem):

    def __init__(self, initial, goal):
        Problem.__init__(self, initial, goal)
        self.all_actions = [MissionariesLeftToRight(1), MissionariesLeftToRight(2)]

    def actions(self, state):
        return filter(lambda act: act.is_enabled(), self.all_actions)

    def result(self, state, action):
        return action.execute(state)
