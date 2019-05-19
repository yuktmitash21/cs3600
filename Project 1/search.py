# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):

    """
    Search the deepest nodes in the search tree firs

    """
    "*** YOUR CODE HERE ***"

    #initialize start
    startingVertex = problem.getStartState()
    curr = startingVertex

    #make hash set and map for list
    myHashSet = set()
    map = {startingVertex: []}
    action = []

    #stack
    myStack = util.Stack()
    listOfVisits = []
    myStack.push(startingVertex)

    #while current is not the goal state continue
    while not problem.isGoalState(curr):

        #iterate through successors and add to stack if not already checked
        for list in problem.getSuccessors(curr):
            if not list[0] in myHashSet:
                myStack.push(list[0])
                temp = action
                temp = temp + [list[1]]
                map[list[0]] = temp


        #update current and action
        curr = myStack.pop()
        myHashSet.add(curr)
        listOfVisits.append(curr)
        action = map[curr]
    return action


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    #initialize start and current
    startingVertex = problem.getStartState()
    curr = startingVertex

    #intialize hashSet and map
    myHashSet = set()
    map = {startingVertex: []}

    #initialize a queue (it may be called myStack but it's a queue!)
    myStack = util.Queue()
    otherList = []
    action = []

    #push to the stack
    myStack.push(startingVertex)
    otherList.append(startingVertex)
    myHashSet.add(startingVertex)

    #pop
    curr = myStack.pop()
    myHashSet.add(curr)
    otherList.append(curr)
    action = map[curr]

    #continue until you reach the goal state
    while True:
        if (problem.isGoalState(curr)):
            return action

        #iterate through curr's successors and add to queue if not already looked at
        for list in problem.getSuccessors(curr):

            if not list[0] in myHashSet:
                myStack.push(list[0])
                temp = action
                #probably bad news
                myHashSet.add(list[0])
                otherList.append(list[0])
                temp = temp + [list[1]]
                map[list[0]] = temp

        #update curr, myHashSet, and action
        curr = myStack.pop()
        myHashSet.add(curr)
        otherList.append(curr)
        action = map[curr]


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"

    #initialize startingPoint, set, PQ, alternative Queue
    startingVertex = problem.getStartState()
    curr = startingVertex
    mySet = set()
    # print "successors", problem.getSuccessors(startingVertex)[0]
    myStack = util.PriorityQueue()
    otherQueue = util.Queue()

    #push on to queue
    myStack.push(startingVertex, 0)
    otherQueue.push(startingVertex)
    map = {startingVertex: []}
    mapOfWeights = {startingVertex: 0}

    #pop and set variables
    current = myStack.pop()
    otherQueue.pop()
    action = map[current]
    weight = mapOfWeights[current]
    mySet.add(current)



    #loop until goal is reached
    while not problem.isGoalState(current):

        #check succeessors and add to queue if need be
        for list in problem.getSuccessors(current):
            if not list[0] in mySet and not list[0] in otherQueue.list:
                myStack.push(list[0], (list[2] + weight))
                mapOfWeights[list[0]] = list[2] + weight
                #mySet.add(list[0])
                otherQueue.push(list[0])
                temp = action
                temp = temp + [list[1]]
                map[list[0]] = temp


        #pop and update list
        current = myStack.pop()
        otherQueue.pop()
        action = map[current]
        weight = mapOfWeights[current]
        mySet.add(current)

    return action






def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
\
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    #initialize PQ, empty list, weight of 0
    myPriorityQueue = util.PriorityQueue()
    ActionList = []
    weight = 0
    otherQueue = util.Queue()
    startingVertex = problem.getStartState()
    otherQueue.push(startingVertex)

    #create initial list of attributes, push on to queue with weight of -
    listOfValues = [startingVertex, weight, ActionList]
    myPriorityQueue.push(listOfValues, weight)
    otherQueue.pop()
    mySet = set()


    #loop until goal is reached
    while True:

        #get all values by popping queue
        listOfValues = myPriorityQueue.pop()
        currentVertex = listOfValues[0]
        currentWeight = listOfValues[1]
        currentList = listOfValues[2]
        if problem.isGoalState(currentVertex):
            return currentList

        #push new list onto queue for all suceessors
        if not currentVertex in mySet:
            mySet.add(currentVertex)
            for list in problem.getSuccessors(currentVertex):
                if not list[0] in mySet:
                    otherQueue.push(list[0])
                    newVertex = list[0]
                    newWeight = list[2]
                    newList = list[1]

                    updatedList = [newVertex, newWeight + currentWeight, currentList + [newList]]
                    myPriorityQueue.push(updatedList, newWeight + currentWeight + heuristic(newVertex, problem))





# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
