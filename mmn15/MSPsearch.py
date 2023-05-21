from time import sleep
from typing import Any
import numpy as np
import util



LEFTBANCK = 0
RIGHTBANCK = 1

MLB = 0 #Missionaries Left Bank 
KLB = 1 #Kannibals Left Bank
MRB = 2 #Missionaries Right Bank
KRB = 3 #Kannibals Right Bank
BP = 4 #Boat Position





#######################################################
# K = kannibals 
# M = Missionaries
#                
#######################################################




class MissionariesCannibalsProblem():
 
    MAX_CAPACITY = 2
    GOAL_STATE = [3,3,0,0,LEFTBANCK]
    START_STATE = [0,0,3,3,RIGHTBANCK]

    """Constructor of MissionariesCannibalsProblem class"""
    def __init__(self, state =START_STATE, action = "", goal = GOAL_STATE):
        #list of 5 elements M in left bank, K in left bank, M in right bank, K in right bank, 5 boat position
        self.state = state
        self.Action = action
        self.goal = goal

    """Make MissionariesCannibalsProblem object get indexable""" 
    def __getitem__(self, index):
        return self.state[index]

    """Make MissionariesCannibalsProblem object set indexable"""
    def __setitem__(self, index, value):
        self.state[index] = value

    """Get the action that led to this state"""
    def getAction(self):  
        return (self.Action)
    
    """Make MissionariesCannibalsProblem object hashable"""
    def __hash__(self):
        value = 0
        for i in range(0,5):
            value +=np.power(2,self.state[i]*i)
        return (int(value))
    
    """Make MissionariesCannibalsProblem object printable"""
    def __str__(self):
        return str(self.state)
    
    """Make MissionariesCannibalsProblem object copyable"""
    def copy(self):
        return MissionariesCannibalsProblem(self.state.copy(), self.Action)
    
    """Make MissionariesCannibalsProblem object comparable"""
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
    """Check if the state is the goal state"""
    def isGoalState(self):
        goal = MissionariesCannibalsProblem(self.goal)
        return self.__eq__(goal)
    
    """Get the start state"""
    def getStartState(self):
        return self.copy()    
            
    """Check that the state is legal"""
    def isLegal(self):
        
        #chec that there are'nt any missionaries outnumbered by kannibals on any bank
        if (self.state[MLB] < self.state[KLB] and self.state[MLB] > 0) or (self.state[MRB] < self.state[KRB] and self.state[MRB] > 0):
            return False
        
        #check if one of the inedexes is negative or bigger than 3
        for tmp in self.state:
            if tmp < 0 or tmp > 3:
                return False 
        
        return True
    
    """Check if object is instance of MissionariesCannibalsProblem for debugging reasons."""
    def __isinstance__(obj, MissionariesCannibalsProblem):
        return isinstance(obj, MissionariesCannibalsProblem)
    
    """drop passengers on the other bank upone arrival"""
    
    def dropPasnngares(self):
        result = self.state.copy()
        KanibalsOnBoat =  3- (result[KLB] + result[KRB])
        MissionariesOnBoat = 3 - (result[MLB] + result[MRB])
        
        if KanibalsOnBoat < 0 or MissionariesOnBoat < 0:
            raise Exception("Error in dropPasnngares you are missing some passengers")
        #boat came from left bank drop passengers on left bank base on type of passengers
        if result[BP] == LEFTBANCK:
            result[MLB] += MissionariesOnBoat
            result[KLB] += KanibalsOnBoat
            return MissionariesCannibalsProblem(result)
        #boat came from right bank drop passengers on right bank base on type of passengers
        elif result[BP] == RIGHTBANCK:
            result[MRB] += MissionariesOnBoat
            result[KRB] += KanibalsOnBoat
            return MissionariesCannibalsProblem(result) 
        else:
            raise Exception("Error in dropPasnngares you can't drop passengers in the river")
        
        
                
    """Get the successors of the state"""
    def getSuccessors(self):
        successors = []
        #drop passengers on the bank upone arrival
        droped = self.dropPasnngares()
        if droped.isGoalState():
                successors.append(droped)
        
        

        #check if the boat is in the left bank
        if self.state[BP] == LEFTBANCK:
            misionTake = MLB
            kanibalTake = KLB
            newBank = RIGHTBANCK
            fromBank = "left"
            tooBank = "right"            

        # else the boat is in the right bank
        else:
            misionTake = MRB
            kanibalTake = KRB
            newBank = LEFTBANCK
            fromBank = "right"
            tooBank = "left"
            

        #Board people on boat
        for mission in range(0,3):
            for kanibal in range(0,3):
                if mission+kanibal <3 and mission+kanibal > 0:
                    temp = droped.copy()
                    temp[misionTake] -= mission
                    temp[kanibalTake] -= kanibal
                    temp[BP] = newBank                    
                    action = "Takes " + str(mission) + " Missionaries and " + str(kanibal) + " Kannibals from " + fromBank + " bank to " + tooBank + " bank"
                    temp.Action = action                    
                    successors.append(temp)


        #Debugging in case of error
        for node in successors:
            if not isinstance(node, MissionariesCannibalsProblem):
                print("Error in the type of the node") 
                exit(1)                    
        
        #filter the legal successors
        successors = filter(MissionariesCannibalsProblem.isLegal, successors)

        #Make sure each successor appears only once in the list using set
        successors = list(set(successors))       
        
        return successors
    

    """Get heuristic value of the state
    The heuristic is the number of trips that we need to make to get to the goal state as it
    hance as we move more people from the right side to the left side the heuristic will decrease
    and if we have to move 2 people from the left side to the right side it will increase the heuristic by 2
    since we take from the goal side that wil need to come back to the left side 
    """
    def heuristic(self):

        result = 0
        sumLeft = self.state[MLB] + self.state[KLB]
        sumRight = self.state[MRB] + self.state[KRB]

        # goal state
        if sumLeft == 6:
            return 0
        
        dropped = self.dropPasnngares().copy()
        
        # if we have 2 move 2 people from the left side to the right side it will increase the number of trips by at list 1
        if (self.state[BP]== LEFTBANCK):            
            if dropped.state[KLB] > dropped.state[MLB] and dropped.state[MLB] > 0:
                result += 2+sumRight
                
        #either we may take 1 person from the right side to the left side or 2 people from the left side to the right side
        result -= (1 +sumRight)

        #if we can can take 2 people from the left side to the right side it will decrease the number of trips by 1
        for mission in range(0,3):
            for kanibal in range(0,3):
                if mission+kanibal == 2:
                    temp = dropped.copy()
                    temp[MLB] -= mission
                    temp[KLB] -= kanibal
                    temp[BP] = RIGHTBANCK
                    if temp.isLegal():
                        result -= 1 
                        break   

        return result




"""
    This function is used to backtrack from the goal state to the start state
    and return the list of actions that lead to the goal state from the start state
    by using the fatherSunDict dictionary that contains the parent of each node
    """
def backtrcking(node,startState, fatherSunDict , howmayNodes, algorithm = ""):
    
    result = []  
    while not startState.__eq__(node):        
        result.append(node.getAction())
        node = fatherSunDict[node]
    result = result[::-1] #reverse the list
    for node in result:
        print(node)
    print("Over all " ,algorithm, " have explored ",howmayNodes, " nodes and the route is of length:", len(result) )

    #Not in use for now but it can be used to save the result if needed
    return result


# BFS
def breadthFirstSearch(problem):
    howManyNodes = 0
    fornteire = util.Queue()
    fornteire.push(problem)
    explored = []
    fatherSunDict = {}
    #keep searching while there are still nodes to explore
    while not fornteire.isEmpty():
        node = fornteire.pop()
        howManyNodes += 1    

        #add the current node cordinates to the explored list
        explored.append(node)     

        #add the successors of the current node to the frontier
        for successor in node.getSuccessors():                        
            if successor not in explored:
                # howManyNodes += 1
                #start backtracking if we have reached the goal   
                if successor.isGoalState():
                    fatherSunDict[successor] = node
                    return backtrcking(node, problem.getStartState(), fatherSunDict , howManyNodes , "BFS")
                fornteire.push(successor)
                fatherSunDict[successor] = node

    print("No solution found")
    return []

#IDDFS
def iterativeDeepeningSearch(problem):
    FINAL_LIMIT = 100
    limit = 1
    homeManyNodes = 0
    start_node = problem.getStartState()


    while limit < FINAL_LIMIT:
        #set a new frontier and explored list for each iteration
        frontier = util.Stack()
        explored = []
        fatherSunDict = {}
        depth = 0
        homeManyNodes = 0

        frontier.push([problem, depth])
        explored.append(problem)

        while not frontier.isEmpty() and depth < limit:
            #pop the node from the frontier and add it to the explored list
            node, depth = frontier.pop()
            homeManyNodes += 1
            #start backtracking if we have reached the goal
            if node.isGoalState():
                return backtrcking(node, start_node, fatherSunDict , homeManyNodes , "IDDFS")
            
            for successor in node.getSuccessors():
                if successor not in explored:
                    explored.append(successor) 
                    frontier.push([successor, depth + 1])
                    fatherSunDict[successor] = node
        limit += 1

    print("IDDFS failed to find a solution in depth limit of ", FINAL_LIMIT)  

     

#GBFS
def greedyBestFirstSearch(problem):
    #set a new frontier and explored list
    frontier = util.PriorityQueue()    
    explored = []
    fatherSunDict = {}
    howManyNodes = 0

    frontier.push(problem, problem.heuristic())
    explored.append(problem)

    while not frontier.isEmpty():
        node, _ = frontier.pop()        
        howManyNodes += 1

        #start backtracking if we have reached the goal
        if node.isGoalState():
            return backtrcking(node, problem.getStartState(), fatherSunDict , howManyNodes , "GBFS")
        
        for successor in node.getSuccessors():
            if successor not in explored:
                explored.append(successor) 
                frontier.push(successor, successor.heuristic())
                fatherSunDict[successor] = node



#A*
def aStarSearch(problem):
    #set a new frontier and explored list
    frontier = util.PriorityQueue()
    explored = []
    fatherSunDict = {}
    howManyNodes = 0
    gValue = 0


    frontier.push(problem, problem.heuristic() + gValue)
    explored.append(problem)

    while not frontier.isEmpty():

        node, gValue = frontier.pop()      
        howManyNodes += 1



        #start backtracking if we have reached the goal
        if node.isGoalState():
            return backtrcking(node, problem.getStartState(), fatherSunDict , howManyNodes , "A*")
        
        #adding the cost of the current node to the gValue
        gValue += 1
        for successor in node.getSuccessors():
            if successor not in explored:
                explored.append(successor) 
                frontier.push(successor, successor.heuristic() + gValue)
                fatherSunDict[successor] = node

    raise Exception("A* failed to find a solution")

def main():
    

    problem = MissionariesCannibalsProblem()            
    breadthFirstSearch(problem)
    print("BFS done!")
    print("##################################################################################################")
    print("##################################################################################################") 
    sleep(1.5)
    iterativeDeepeningSearch(problem)
    print("IDDFS done!")
    print("##################################################################################################")
    print("##################################################################################################")
    sleep(1.5)
    greedyBestFirstSearch(problem)
    print("GBFS done!")
    print("##################################################################################################")
    print("##################################################################################################")
    sleep(1.5)
    aStarSearch(problem)
    print("A* done!")


main()

        
            


    
