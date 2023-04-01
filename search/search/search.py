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

def backtrcking(node,startState, fatherSunDict):
    """
    This function is used to backtrack from the goal state to the start state
    and return the list of actions that lead to the goal state from the start state
    by using the fatherSunDict dictionary that contains the parent of each node
    """
    result = []
    while node[0] != startState:
        result.append(node[1])
        node = fatherSunDict[node]
    result = result[::-1] #reverse the list
    return result

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
    """
    fornteire = util.Stack()
    fornteire.push((problem.getStartState(),None,0))
    explored = []
    fatherSunDict = {}
    #keep searching while there are still nodes to explore
    while not fornteire.isEmpty():
        node = fornteire.pop()
        state, action, cost = node
        #start backtracking if we have reached the goal
        if problem.isGoalState(state):
            return backtrcking(node, problem.getStartState(), fatherSunDict)
        
        #add the current node cordinates to the explored list
        explored.append(state)

        #add the successors of the current node to the frontier
        for successor in problem.getSuccessors(state):
            if successor[0] not in explored:
                fornteire.push(successor)
                fatherSunDict[successor] = node

    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    fornteire = util.Queue()
    fornteire.push((problem.getStartState(),None,0))
    explored = []
    explored.append(problem.getStartState())
    fatherSunDict = {}
    #keep searching while there are still nodes to explore
    while not fornteire.isEmpty():
        #initialize explored node with the first node in the frontier
        node = fornteire.pop()
        state, action, cost = node

        #start backtracking if we have reached the goal
        if problem.isGoalState(state):
            return backtrcking(node, problem.getStartState(), fatherSunDict)      

        #add the successors of the current node to the frontier
        #only if the successor is not in the explored list or sucssoor of any node in the frontier
        for successor in problem.getSuccessors(state):
            if successor[0] not in explored:
                fornteire.push(successor)
                fatherSunDict[successor] = node
                explored.append(successor[0])

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    fornteire = util.PriorityQueue()
    fornteire.push((problem.getStartState(),None,0,0),0)
    explored = []
    fatherSunDict = {}

    #keep searching while there are still nodes to explore
    while not fornteire.isEmpty():
        node, totalcost = fornteire.pop()
        state, action, cost = node

        #start backtracking if we have reached the goal
        #Since we use praority queue, we acan be sure that 
        #the first goal node we pop is the node with the least cost
        if problem.isGoalState(state):
            return backtrcking(node, problem.getStartState(), fatherSunDict) 
        
        #add the current node cordinates to the explored list
        explored.append(state)
        
        """add the successors of the current node to the frontier 
        if the successor is not in the frontier 
        or the successor path cost is less than the path cost of the node in the frontier 
        update the total cost of the successor if needed"""
        for successor in problem.getSuccessors(state):
            if (successor in explored):
                dist = totalcost+successor[3]
                fornteire.update(successor, dist)
                fatherSunDict[successor] = node
                
        

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
