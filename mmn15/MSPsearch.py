from typing import Any
import numpy as np
import util



LEFTBANCK = 0
RIVER = 1
RIGHTBANCK = 2

MLB = 0 #Missionaries Left Bank 
KLB = 1 #Kannibals Left Bank
MRB = 2 #Missionaries Right Bank
KRB = 3 #Kannibals Right Bank
BP = 4 #Boat Position
LBP = 5 #Last Boat Position




#######################################################
# K = kannibals 
# M = Missionaries
#                
#######################################################




class MissionariesCannibalsProblem():    

    def __init__(self, state =[0,0,3,3,RIGHTBANCK,RIGHTBANCK], action = ""):
        #list of 6 elements M in left bank, K in left bank, M in right bank, K in right bank, 5 boat position, 6 last boat position.
        self.state = state
        Action = action

    def __getitem__(self, index):
        return self.state[index]

    def __setitem__(self, index, value):
        self.state[index] = value

    def getAction(self):
        print(self.Action)
        return str(self.Action)
    
    def __hash__(self):
        value = 0
        for i in range(0,5):
            value +=np.power(2,self.state[i]*i)
        return (int(value))
    
    def __str__(self):
        return str(self.state)
    
    def copy(self):
        return MissionariesCannibalsProblem(self.state.copy())
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
    def isGoalState(self ,goal = None):
        if goal is None:
            goal = MissionariesCannibalsProblem([3,3,0,0,LEFTBANCK,RIVER])
        return self.__eq__(goal)
    
    def getStartState(self):
        return self.copy()
    
    
        
    # check if the state is legal
    def isLegal(self):
        if (self.state[MLB] < self.state[KLB] or self.state[MRB] < self.state[KRB]):
            return False
        #on line check if one of the inedexes is negative or bigger than 3
        for i in self.state:
            if i < 0 or i > 3:
                return False
        #sum the number banks
        sumBanks = sum([self.state[i] for i in range(0, 4)])
        if sumBanks > 6 or sumBanks < 4:
            return False
        return True
    
    
    def __isinstance__(obj, MissionariesCannibalsProblem):
        return isinstance(obj, MissionariesCannibalsProblem)

    
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
            return result
        #boat came from right bank drop passengers on right bank base on type of passengers
        elif result[BP] == RIGHTBANCK:
            result[MRB] += MissionariesOnBoat
            result[KRB] += KanibalsOnBoat
            return result
        else:
            raise Exception("Error in dropPasnngares you can't drop passengers in the river")
           
    def crossRiver(self):
        successors = []
        # Boat came from left bank
        if self.state[LBP] == LEFTBANCK:
            temp = self.state.copy()
            temp[BP] = RIGHTBANCK
            temp[LBP] = RIVER
            successors.append(MissionariesCannibalsProblem(temp))
            return successors
        # Boat came from right bank
        else:
            temp = self.state.copy()
            temp[BP] = LEFTBANCK
            temp[LBP] = RIVER
            successors.append(MissionariesCannibalsProblem(temp))
            return successors
        
    def LeavLeftBank(self):
        successors = []
        droped = MissionariesCannibalsProblem(self.dropPasnngares())
        if droped.isGoalState():
            successors.append(droped)
           
        #put people on boat
        for i in range(0, 2):
            for j in range(0, 2):
                if i+j <3:
                    temp = droped.copy()
                    temp[MLB] -= i
                    temp[KLB] -= j
                    temp[BP] = RIVER
                    temp[LBP] = LEFTBANCK
                    action = "Take " + str(i) + " Missionaries and " + str(j) + " Kannibals from left bank to right bank"                    
                    successors.append(MissionariesCannibalsProblem(temp , action))
        return successors                 
    
    def LeavRightBank(self):
        successors = []
        droped = MissionariesCannibalsProblem(self.dropPasnngares())
        #put people on boat
        for i in range(0, 2):
            for j in range(0, 2):
                if i+j <3:
                    temp = droped.copy()
                    temp[MRB] -= i
                    temp[KRB] -= j
                    temp[BP] = RIVER
                    temp[LBP] = RIGHTBANCK
                    action = "Take " + str(i) + " Missionaries and " + str(j) + " Kannibals from right bank to left bank"
                    successors.append(MissionariesCannibalsProblem(temp, action))
        return successors
    

    def getSuccessors(self):
        successors = []
        #check if the boat is in the river
        if self.state[BP] == RIVER:            
            successors= self.crossRiver()


            #check if successors is a has a list member
            for i in successors:
                if isinstance(i, list):
                    print("Error in the type of the successors RIVER",i) 
                    exit(1)
            

        #check if the boat is in the left bank
        elif self.state[BP] == LEFTBANCK:
            successors= (self.LeavLeftBank())
            #check if successors has a list member
            for i in successors:
                if isinstance(i, list):
                    print("Error in the type of the successors LEFTBANCK",i) 
                    exit(1)
            

        #check if the boat is in the right bank
        elif self.state[BP] == RIGHTBANCK:
            successors= (self.LeavRightBank())
             #check if successors is a has a list member
            for i in successors:
                if isinstance(i, list):
                    print("Error in the type of the successors RIGHTBANCK",i) 
                    exit(1)      
        

        #filter the legal successors
        successors = filter(MissionariesCannibalsProblem.isLegal, successors)
        #Make sure each successor appears only once in the list using set
        successors = list(set(successors))

        for node in successors:
            if not isinstance(node, MissionariesCannibalsProblem):
                print("Error in the type of the node") 
                exit(1)
        
        return successors

def backtrcking(node,startState, fatherSunDict , howmayNodes):
    """
    This function is used to backtrack from the goal state to the start state
    and return the list of actions that lead to the goal state from the start state
    by using the fatherSunDict dictionary that contains the parent of each node
    """
    result = []  
    while not startState.__eq__(node):        
        result.append(node)
        node = fatherSunDict[node]
    result = result[::-1] #reverse the list
    for node in result:
        print(node)
    print("Over all we have generated ", howmayNodes, " nodes")
    return result

# BFS
def breadthFirstSearch(problem):
    howManyNodes = 1
    fornteire = util.Stack()    
    fornteire.push(problem)
    explored = []
    fatherSunDict = {}
    #keep searching while there are still nodes to explore
    while not fornteire.isEmpty():
        node = fornteire.pop()    

        #start backtracking if we have reached the goal   
        if node.isGoalState():
            return backtrcking(node, problem.getStartState(), fatherSunDict , howManyNodes)
        
        #add the current node cordinates to the explored list
        explored.append(node)

        

        #add the successors of the current node to the frontier
        for successor in node.getSuccessors():
            if successor not in explored:
                howManyNodes += 1
                fornteire.push(successor)
                fatherSunDict[successor] = node
    return []

#IDDFS
def iterativeDeepeningSearch(prblem):
    raise NotImplementedError 

#GBFS
def greedyBestFirstSearch(prblem):
    raise NotImplementedError

#A*
def aStarSearch(prblem):
    raise NotImplementedError


def main():

    problem = MissionariesCannibalsProblem()
    # ask the user to enter the algorithm he wants to use as a list of numbers
    # 1 for BFS, 2 for IDDFS, 3 for GBFS, 4 for A* 5 for all
    #scanner = input("Enter the algorithm you want to use as a list of numbers 1 for BFS, 2 for IDDFS, 3 for GBFS, 4 for A* 5 for all: ")
    # print("You entered: ", scanner)
    # if scanner == 1:
    #     print("BFS")
    #     breadthFirstSearch(problem)
    # elif scanner == 2:
    #     iterativeDeepeningSearch(problem)
    # elif scanner == 3:
    #     greedyBestFirstSearch(problem)
    # elif scanner == 4:
    #     aStarSearch(problem)
    # elif scanner == 5:
    #     
    breadthFirstSearch(problem)
    # iterativeDeepeningSearch(problem)
    # greedyBestFirstSearch(problem)
    # aStarSearch(problem)
    
    print("All done!")


main()

        
            


    
