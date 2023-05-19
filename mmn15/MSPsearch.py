import numpy as np



LEFTBANCK = 0
RIVER = 1
RIGHTBANCK = 2

MLB = 0 #Missionaries Left Bank 
KLB = 1 #Kannibals Left Bank
MRB = 2 #Missionaries Right Bank
KRB = 3 #Kannibals Right Bank
BP = 4 #Boat Position
LBP = 5 #Last Boat Position
MB = 6 # Missionaries on Boat
KB = 7 # Kannibals on Boat





#######################################################
# K = kannibals 
# M = Missionaries
#                
#######################################################




class MissionariesCannibalsProblem():    

    def __init__(self, state =[0,0,3,3,RIGHTBANCK,RIGHTBANCK,0,0]):
        #kist of 5 elements M in left bank, K in left bank, M in right bank, K in right bank, 5 boat position
        self.state = state

    def getVal(self):
        return (lambda x: sum(np.power(2,x* self.state[x])))(self.state)
    
    def __eq__(self, other):
        return self.getVal == other.getVal    
    
    def isGoalState(self, state):
        return state == [3,3,0,0,LEFTBANCK,RIVER,0,0]
    
    # return one of 4 states
    def getCase(self, state):
        # 1. == both banks has same number of kannibals and missionaries
        if state[MLB] == state[KLB] and state[MRB] == state[KRB]:
            return 1
        # 2. = > left bank has same number of kannibals and missionaries and right bank has more missionaries than kannibals
        elif state[MLB] == state[KLB] and state[MRB] > state[KRB]:
            return 2
        # 3. > = right bank has same number of kannibals and missionaries and left bank has more missionaries than kannibals
        elif state[MLB] > state[KLB] and state[MRB] == state[KRB]:
            return 3
        # 4. > > both banks has more missionaries than kannibals
        elif state[MLB] > state[KLB] and state[MRB] > state[KRB]:
            return 4
        
    # check if the state is legal
    def isLegal(self, state):
        if (state[MLB] < state[KLB] or state[MRB] < state[KRB]):
            return False
        #on line check if one of the inedexes is negative or bigger than 3
        for i in state:
            if i < 0 or i > 3:
                return False            
        return True
    
    def dropPasnngares(self, state):
        result = state.copy()
        #boat came from left bank drop passengers on left bank base on type of passengers
        if state[BP] == LEFTBANCK:
            result[MLB] += state[MB]
            result[MB] = 0
            result[KLB] += state[KB]
            result[KB] = 0
            return result
        #boat came from right bank drop passengers on right bank base on type of passengers
        elif state[BP] == RIGHTBANCK:
            result[MRB] += state[MB]
            result[MB] = 0
            result[KRB] += state[KB]
            result[KB] = 0
            return result
        else:
            raise Exception("Error in dropPasnngares you can't drop passengers in the river")

           
    def crossRiver(self, state):
        successors = []
        # Boat came from left bank
        if state[LBP] == LEFTBANCK:
            temp = state.copy()
            temp[BP] = RIGHTBANCK
            temp[LBP] = RIVER
            successors.append(MissionariesCannibalsProblem(temp))
            return successors
        # Boat came from right bank
        else:
            temp = state.copy()
            temp[BP] = LEFTBANCK
            temp[LBP] = RIVER
            successors.append(MissionariesCannibalsProblem(temp))
            return successors
        
    def LeavLeftBank(self, state):
        droped = self.dropPasnngares(state)
        successors = []
        #put people on boat
        for i in range[0,2]:
            for j in range[0,2]:
                if i+j <3:
                    temp = droped.copy()
                    temp[MB] = i
                    temp[KB] = j
                    temp[MLB] -= i
                    temp[KLB] -= j
                    temp[BP] = RIVER
                    temp[LBP] = LEFTBANCK
                    successors.append(MissionariesCannibalsProblem(temp))
        return successors                 
    
    def LeavRightBank(self, state):
        droped = self.dropPasnngares(state)
        successors = []
        #put people on boat
        for i in range[0,2]:
            for j in range[0,2]:
                if i+j <3:
                    temp = droped.copy()
                    temp[MB] = i
                    temp[KB] = j
                    temp[MRB] -= i
                    temp[KRB] -= j
                    temp[BP] = RIVER
                    temp[LBP] = RIGHTBANCK
                    successors.append(MissionariesCannibalsProblem(temp))
    

    def getSuccessors(self, state):
        successors = []
        peopleOnBoat = abs((sum(state[0:4]) - 6))
        case = self.getCase(state)

        if state[BP] == RIVER:            
            successors.append(self.crossRiver(state))
        
        elif state[BP] == LEFTBANCK:
            successors.append(self.LeavLeftBank(state))
        
        elif state[BP] == RIGHTBANCK:
            successors.append(self.LeavRightBank(state))
        
        #filter the legal successors
        successors = filter(self.isLegal, successors)
        return successors
        
            


    
