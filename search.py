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
    return  [s, s, w, s, w, w, s, w]


class Node:
    """
    A class that implements a representation to "Node" so that it is possible to push Node into the data structure and
        use them more conveniently and that the code is more readable.
    Implementation without this class would have forced us to make many tuples transfers and it would have made it very
     difficult to write and read the code.

    The values stored for each object in the class are:
    The state of the node.
    The Node from which we reached the current node (for the purpose of calculating the route taken on arrival at the
     destination.)
    The action performed in the previous situation.
    And the priority of the node (When the "implementation" is not a "priority queue" this value will be filled by 0
     and thus it will not affect the various implementations.)
    No implementation was performed for the successor node because to single predecessor  can be  a large number
     of successors and furthermore because such a implementation would require unreasonable computational capability
        of course such a calculation would eliminate the need for task because it would eliminate the importance of
        heuristics in the various implementations(Such a realization is just another name for H*)
    """
    def __init__(self, state, predecessor, action, priority=0):
        self.state = state
        self.predecessor = predecessor
        self.action = action
        self.priority = priority

    def __repr__(self):
        return "State: {0}, Action: {1}".format(self.state, self.action)


def firstSearch(problem: SearchProblem, type_of_search: int):
    """
    A function that performs the core of bfs and dfs search.
    Since the two functions are the same (except for the data structure they use) I decided to implement them together
        using a different data structure depending on the type of search
    """
    if type_of_search == 1:
        frontier = util.Stack()
    elif type_of_search == 2:
        frontier = util.Queue()
    explored = dict()
    # add Node(state, predecessor, action) to the data structure according his Style(dfs,bfs)
    frontier.push(Node(problem.getStartState(), None, None))
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.state):
            actions = list()
            while node.action is not None:
                actions.append(node.action)
                node = node.predecessor
            actions.reverse()
            return actions
        if node.state not in explored:
            explored.update({node.state: node})
            for successor in problem.getSuccessors(node.state):
                successor_as_node = Node(successor[0],node ,successor[1])
                frontier.push(successor_as_node)
    return list()


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    return firstSearch(problem, 1)



def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    return firstSearch(problem, 2)



def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of the least total cost first.
    The realization of the function is as presented in the book.
    Using "priority queue" from "util" for frontier,and using "dictionary" for explored and this is to reduce the
        complexity of node exploration in explored.
    """
    frontier = util.PriorityQueue()
    explored = dict()
    # add Node(state, predecessor, action) to the Priority Queue while the priorty is 0
    frontier.push(Node(problem.getStartState(), None, None), 0)
    while not frontier.isEmpty(): #there are more to Node waiting to checked
        node = frontier.pop()
        if problem.isGoalState(node.state):
            actions = list()
            while node.action is not None: #This node is not the initial state.
                actions.append(node.action)
                node = node.predecessor
            actions.reverse()#Since we added the actions to the list from the destination to the beginning(where the direction of the action is the way to the destination)
            return actions
        if node.state not in explored:
            explored.update({node.state: node}) #Update as explained in the task file. So if the node is not explored - then the update will insert it. And if it is in explored then the node will be updated to the better priority value.
            for successor in problem.getSuccessors(node.state):#Adds the sucssesors
                successor_as_node = Node(successor[0], node, successor[1], successor[2]+node.priority)
                frontier.push(successor_as_node, successor_as_node.priority)
    return list() #failure


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    Similar to the uniformCostSearch function except for the changes as presented in the book on page 112 and as
        explained in Dvir's recorded lecture on the site.
    """
    frontier = util.PriorityQueue()
    explored = dict()
    # add Node(state, predecessor, action) to the Priority Queue while the priorty is 0
    frontier.push(Node(problem.getStartState(), None, None,heuristic(problem.getStartState(), problem)),heuristic(problem.getStartState(), problem))
    while not frontier.isEmpty(): #there are more to Node waiting to checked
        node = frontier.pop()
        if problem.isGoalState(node.state):
            actions = list()
            while node.action is not None: #This node is not the initial state.
                actions.append(node.action)
                node = node.predecessor
            actions.reverse()#Since we added the actions to the list from the destination to the beginning(where the direction of the action is the way to the destination)
            return actions
        if node.state not in explored:
            explored.update({node.state: node}) #Update as explained in the task file. So if the node is not explored - then the update will insert it. And if it is in explored then the node will be updated to the better priority value.
            for successor in problem.getSuccessors(node.state): #Adds the sucssesors
                successor_as_node = Node(successor[0], node, successor[1], successor[2]+node.priority)
                frontier.update(successor_as_node, successor_as_node.priority + heuristic(successor[0], problem))
    return list() #failure



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
