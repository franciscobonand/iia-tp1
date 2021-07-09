# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    Start: (5, 5)
    Is the start a goal? False
    Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    """
    from game import Directions

    start = problem.getStartState()

    if problem.isGoalState(start):
        return Directions.STOP

    visited = []  # list containing visited tiles
    steps = []  # list of steps taken to get to the objective
    expanded = util.Stack()  # stack of expanded tiles (the ones viable to be visited)
    expanded.push((start, []))

    while not expanded.isEmpty():
        # (current tile, steps taken to reach it)
        (curr, steps) = expanded.pop()

        if curr not in visited:
            visited.append(curr)

            if problem.isGoalState(curr):
                return steps
            else:
                next_tiles = problem.getSuccessors(curr)

                for (coord, dir, _) in next_tiles:
                    # next step = all the steps to reach current tile + next step
                    next_step = steps + [dir]
                    expanded.push((coord, next_step))

    return steps


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    from game import Directions

    # This algorithim implementation is pretty similar to DFS
    # The main difference is that it uses a Queue instead of a Stack
    start = problem.getStartState()

    if problem.isGoalState(start):
        return Directions.STOP

    visited = []  # list containing visited tiles
    steps = []  # list of steps taken to get to the objective
    expanded = util.Queue()  # queue of expanded tiles (the ones viable to be visited)
    expanded.push((start, []))

    while not expanded.isEmpty():
        # (current tile, steps taken to reach it)
        (curr, steps) = expanded.pop()

        if curr not in visited:
            visited.append(curr)

            if problem.isGoalState(curr):
                return steps
            else:
                next_tiles = problem.getSuccessors(curr)

                for (coord, dir, _) in next_tiles:
                    # next step = all the steps to reach current tile + next step
                    next_step = steps + [dir]
                    expanded.push((coord, next_step))

    return steps


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from game import Directions

    # This algorithim implementation is pretty similar to DFS and BFS
    # The main difference is that it uses a PriorityQueue, which orders
    # it's elements by the cost to reach them
    start = problem.getStartState()

    if problem.isGoalState(start):
        return Directions.STOP

    visited = []  # list containing visited tiles
    steps = []  # list of steps taken to get to the objective
    # priority queue of expanded tiles (the ones viable to be visited)
    expanded = util.PriorityQueue()
    expanded.push((start, [], 0), 0)

    while not expanded.isEmpty():
        # (current tile, steps taken to reach it, cost to reach it)
        (curr, steps, cost) = expanded.pop()

        if curr not in visited:
            visited.append(curr)

            if problem.isGoalState(curr):
                return steps
            else:
                next_tiles = problem.getSuccessors(curr)

                for (coord, dir, tile_cost) in next_tiles:
                    # next step = all the steps to reach current tile + next step
                    next_step = steps + [dir]
                    # next cost = cost to reach the current tile + next step cost
                    next_cost = cost + tile_cost
                    queue_item = (coord, next_step, next_cost)
                    expanded.update(queue_item, next_cost)

    return steps


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def greedySearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest heuristic first."""
    from game import Directions

    start = problem.getStartState()

    if problem.isGoalState(start):
        return Directions.STOP

    visited = []  # list containing visited tiles
    steps = []  # list of steps taken to get to the objective
    # priority queue of expanded tiles (the ones viable to be visited)
    start_value = heuristic(start, problem)
    expanded = util.PriorityQueue()
    expanded.push((start, []), 0)

    while not expanded.isEmpty():
        # (current tile, steps taken to reach it, cost of heuristic)
        (curr, steps) = expanded.pop()

        if curr not in visited:
            visited.append(curr)

            if problem.isGoalState(curr):
                return steps
            else:
                next_tiles = problem.getSuccessors(curr)

                for (coord, dir, _) in next_tiles:
                    # next step = all the steps to reach current tile + next step
                    next_step = steps + [dir]
                    # next h cost = heuristic cost of next step
                    next_h_cost = heuristic(coord, problem)
                    queue_item = (coord, next_step)
                    expanded.update(queue_item, next_h_cost)

    return steps


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from game import Directions

    start = problem.getStartState()

    if problem.isGoalState(start):
        return Directions.STOP

    visited = []  # list containing visited tiles
    steps = []  # list of steps taken to get to the objective
    # priority queue of expanded tiles (the ones viable to be visited)
    expanded = util.PriorityQueue()
    expanded.push((start, [], 0), 0)

    while not expanded.isEmpty():
        # (current tile, steps taken to reach it, cost of heuristic)
        (curr, steps, cost) = expanded.pop()

        if curr not in visited:
            visited.append(curr)

            if problem.isGoalState(curr):
                return steps
            else:
                next_tiles = problem.getSuccessors(curr)

                for (coord, dir, tile_cost) in next_tiles:
                    # next step = all the steps to reach current tile + next step
                    next_step = steps + [dir]
                    # next h cost = heuristic cost of next step
                    next_h_cost = heuristic(coord, problem)
                    # next cost = cost to reach the current tile + next step cost
                    next_cost = cost + tile_cost
                    total_cost = next_h_cost + next_cost
                    queue_item = (coord, next_step, next_cost)
                    expanded.update(queue_item, total_cost)

    return steps


def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    (pacmanPosition, foodGrid) = state
    goals = foodGrid.asList()
    (x, y) = pacmanPosition
    score = 0

    while len(goals) > 0:
        # dict with key = (pacman position, a goal position) and
        # value = distance between them
        table = {(goal): (abs(x - goal[0]) + abs(y - goal[1]))
                 for goal in goals}

        # gets goal which is closer to pacman
        min_dist = min(table.values())
        # cumulative manhattan distance to closer goal (score to get to it is bigger)
        score += min_dist
        # gets key of closer goal
        minKey = min(table, key=table.get)
        # remove analysed goal from goal list
        goals.remove(minKey)

    # returns the cost to get all the goals from current pacman position
    return score


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
gs = greedySearch
astar = aStarSearch
