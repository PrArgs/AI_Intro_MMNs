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




#######################################################
# K = kannibals 
# M = Missionaries
#                
#######################################################




class MissionariesCannibalsProblem():    

    def __init__(self, state =[0,0,3,3,RIGHTBANCK,RIGHTBANCK]):
        #list of 5 elements M in left bank, K in left bank, M in right bank, K in right bank, 5 boat position, 6 last boat position, 7 Missionaries on Boat, 8 Kannibals on Boat
        self.state = state

    def getVal(self):

        value = 0
        for i in range(0,5):
            value +=np.power(2,self.state[i]*i)
        return value
    
    def __eq__(self, other):
        return self.getVal == other.getVal    
    
    def isGoalState(self, state):
        return state == [3,3,0,0,LEFTBANCK,RIVER]
        
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
        KanibalsOnBoat =  3- (state[KLB] + state[KRB])
        MissionariesOnBoat = 3 - (state[MLB] + state[MRB])
        if KanibalsOnBoat < 0 or MissionariesOnBoat < 0:
            raise Exception("Error in dropPasnngares you are missing some passengers")
        #boat came from left bank drop passengers on left bank base on type of passengers
        if state[BP] == LEFTBANCK:
            result[MLB] += MissionariesOnBoat
            result[KLB] += KanibalsOnBoat
            return result
        #boat came from right bank drop passengers on right bank base on type of passengers
        elif state[BP] == RIGHTBANCK:
            result[MRB] += MissionariesOnBoat
            result[KRB] += KanibalsOnBoat
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
        successors = []
        droped = MissionariesCannibalsProblem(self.dropPasnngares(state))
        if droped.isGoalState(droped.state):
            successors.append(droped)
           
        #put people on boat
        for i in range[0,2]:
            for j in range[0,2]:
                if i+j <3:
                    temp = droped.copy()
                    temp[MLB] -= i
                    temp[KLB] -= j
                    temp[BP] = RIVER
                    temp[LBP] = LEFTBANCK
                    successors.append(MissionariesCannibalsProblem(temp))
        return successors                 
    
    def LeavRightBank(self, state):
        successors = []
        droped = MissionariesCannibalsProblem(self.dropPasnngares(state))
        #put people on boat
        for i in range[0,2]:
            for j in range[0,2]:
                if i+j <3:
                    temp = droped.copy()
                    temp[MRB] -= i
                    temp[KRB] -= j
                    temp[BP] = RIVER
                    temp[LBP] = RIGHTBANCK
                    successors.append(MissionariesCannibalsProblem(temp))
    

    def getSuccessors(self, state):
        successors = []

        #check if the boat is in the river
        if state[BP] == RIVER:            
            successors.append(self.crossRiver(state))

        #check if the boat is in the left bank
        elif state[BP] == LEFTBANCK:
            successors.append(self.LeavLeftBank(state))

        #check if the boat is in the right bank
        elif state[BP] == RIGHTBANCK:
            successors.append(self.LeavRightBank(state))
        
        #filter the legal successors
        successors = filter(self.isLegal, successors)
        #Make sure each successor appears only once in the list using set
        successors = list(set(successors))
        return successors
        
            


    
