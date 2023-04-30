# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
ZERO = 0
ONE = 1

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves] # Get the score for each action
        bestScore = max(scores) # Get the best score value
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore] # Get the indices with the best score
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex] 

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore() # Get the score of the successor state
        # avvoid ghosts by penalizing the score
        for ghost in newGhostStates:
            gPose = ghost.getPosition()
            # if the ghost is close to pacman, penalize the score
            if manhattanDistance(newPos, gPose) < 2:
                score -= 1000
        # check if the the new state contained food if not find the closest food and panalize the score by its distance
        if not successorGameState.getNumFood() < currentGameState.getNumFood() :
            foodList = newFood.asList()
            # set min to infinity
            min = float("inf")
            for food in foodList:
                if manhattanDistance(newPos, food) < min:
                    min = manhattanDistance(newPos, food)
            score -= min           
        
        return score 

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = ZERO # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        _, action = self.__Max_Value(gameState, self.depth)
        return action
        

    def __Max_Value(self, gameState, depth ,agentIndex = ZERO):
        # check if the state is a terminal state
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState) , None
        # get the legal actions of the state
        legalActions = gameState.getLegalActions(agentIndex)
        #set first gohst index
        ghostIndex = self.index + ONE
        # set the max value to negative infinity
        value = float("-inf")
        a = Directions.STOP
        for action in legalActions:
            # get the successor state
            successor = gameState.generateSuccessor(agentIndex, action)
            # get the max value
            v, _ = self.__Min_Value(successor, depth, ghostIndex)           
            if v > value:
                value = v
                a = action
        return value, a
    
    def __Min_Value(self, gameState, depth , agentIndex):
       # check if the state is a terminal state
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState) , None
        # get the legal actions of the state
        legalActions = gameState.getLegalActions(agentIndex)
        # set the min value to infinity
        value = float("inf")
        a = Directions.STOP
        for action in legalActions:
             # get the successor state
            successor = gameState.generateSuccessor(agentIndex, action)

            # check if the agent is the last ghost
            if agentIndex < gameState.getNumAgents() - ONE:
                # get the min value
                v, _ = self.__Min_Value(successor, depth, agentIndex+ONE)
                if v < value:
                    value = v
                    a = action  
            else:               
                # get the min value
                v, _ = self.__Max_Value(successor, depth - ONE,)
                if v < value:
                    value = v
                    a = action  
        return value, a

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # set alpha to negative infinity and beta to positive infinity
        alpha = float("-inf")
        beta = float("inf")
        _, action = self.__Max_Value(gameState, self.depth, alpha, beta)
        return action

    def __Max_Value(self, gameState, depth ,alpha, beta, agentIndex = ZERO):
        # check if the state is a terminal state
        if gameState.isWin() or gameState.isLose() or depth == ZERO:
            return self.evaluationFunction(gameState) , None
        # get the legal actions of the state
        legalActions = gameState.getLegalActions(agentIndex)
        #set first gohst index
        ghostIndex = self.index + ONE
        # set the max value to negative infinity
        value = float("-inf")
        a = Directions.STOP
        for action in legalActions:
            # get the successor state
            successor = gameState.generateSuccessor(agentIndex, action)
            # get the max value
            v, _ = self.__Min_Value(successor, depth, ghostIndex, alpha, beta)           
            if v > value:
                value = v
                a = action
                alpha = max(alpha, value)
            # unlike regular alpha beta pruning, we've been asked not to check equality
            if value > beta:
                return value, a
        return value, a
    
    def __Min_Value(self, gameState, depth , agentIndex, alpha, beta):
        # check if the state is a terminal state
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState) , None
        # get the legal actions of the state
        legalActions = gameState.getLegalActions(agentIndex)
        # set the min value to infinity
        value = float("inf")
        a = Directions.STOP
        for action in legalActions:
             # get the successor state
            successor = gameState.generateSuccessor(agentIndex, action)

            # check if the agent is the last ghost
            if agentIndex < gameState.getNumAgents() - ONE:
                # get the min value
                v, _ = self.__Min_Value(successor, depth, agentIndex+ONE, alpha, beta)
                if v < value:
                    value = v
                    a = action
                    beta = min(beta, value)
                if value < alpha:
                    return value, a

            else:               
                # get the min value
                v, _ = self.__Max_Value(successor, depth - ONE, alpha, beta)
                if v < value:
                    value = v
                    a = action
                    beta = min(beta, value)
                if value < alpha:
                    return value, a
        return value, a

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        _, action = self.__Max_Value(gameState, self.depth)
        return action
        

    def __Max_Value(self, gameState, depth ,agentIndex = ZERO):
        # check if the state is a terminal state
        if gameState.isWin() or gameState.isLose() or depth == ZERO:
            return self.evaluationFunction(gameState) , None
        # get the legal actions of the state
        legalActions = gameState.getLegalActions(agentIndex)
        #set first gohst index
        ghostIndex = self.index + ONE
        # set the max value to negative infinity
        value = float("-inf")
        a = Directions.STOP
        for action in legalActions:
            # get the successor state
            successor = gameState.generateSuccessor(agentIndex, action)
            # get the max value of the average of the min values
            v, _ = self.__Min_Value(successor, depth, ghostIndex)           
            if v > value:
                value = v
                a = action
        return value, a
    
    def __Min_Value(self, gameState, depth , agentIndex):
       # check if the state is a terminal state
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState) , None
        # get the legal actions of the state
        legalActions = gameState.getLegalActions(agentIndex)
        # set the min value to infinity
        value = ZERO
        
        a = Directions.STOP
        for action in legalActions:
            sumMonsterOne  = ZERO
             # get the successor state
            successor = gameState.generateSuccessor(agentIndex, action)

            # check if the agent is the last ghost
            if agentIndex < gameState.getNumAgents() - ONE:
                # get the min value
                v, _ = self.__Min_Value(successor, depth, agentIndex+ONE)
                
                # sumMonsterOne += v
            else:               
                # get the min value
                v, _ = self.__Max_Value(successor, depth - ONE,)
                # counterMonsterTow += 1
                # sumMonsterTwo += v
            
            value += v
        # sinnce we know that the ghosts are choosing uniformly at random from their legal moves
        # The Expected value is the avrage of each possible move
        if len(legalActions) != ZERO:
            value = value / len(legalActions)
        else:
            raise Exception("legalActions is empty")
        return value, None

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """

    # final Reward values
    CHASE_REWARD = 199 # one less than the score of eating a scared ghost    

    # final whight
    SCORE_WEIGHT = 1
    FOOD_AMOUNT_WEIGHT = 0.8
    NEAREST_FOOD_WEIGHT = -0.5
    CAPSULE_WEIGHT = -0.5


    # Useful information you can extract from a GameState (pacman.py)
    
    pacmanPos = currentGameState.getPacmanPosition()
    MonsterPos = currentGameState.getGhostPositions()
    GhostStates = currentGameState.getGhostStates()
    #maps the scared times of the ghosts when the key is the ghost position and the value is the scared time   
    #ScaredTimes = {GhostStates[i].getPosition(): GhostStates[i].scaredTimer for i in range(len(GhostStates))}
    foodList = currentGameState.getFood().asList()


    # Find nearest food and multiply it by a weight
    if len(foodList) > ZERO:
        nearstFood = min([manhattanDistance(pacmanPos, food_position) for food_position in foodList]) 
    else:
        nearstFood = ONE


    # Find the number of capsules left and multiply it by a weight
    CapsuleLeft = len(currentGameState.getCapsules())
    
    # Find the score of the current state and multiply it by a weight
    game_score = currentGameState.getScore()

    # Since we see 2 steps ahead, we do not need the check if the ghost will eat pacman but we want to reward pacman for chasing the ghost if it can be eaten 
    ChaseGhost = ZERO

    # If ghost is scared, pacman should chase it can reach it in time
    # if true set ChaseGhost to the reward of eating a scared ghost 
    #ChaseGhost = sum([ONE for ghost in MonsterPos if ScaredTimes[ghost] > ZERO and manhattanDistance(pacmanPos, ghost) <= ScaredTimes[ghost]])
        
    scoreList = [game_score, nearstFood, ChaseGhost, CapsuleLeft]
    whightList = [SCORE_WEIGHT, NEAREST_FOOD_WEIGHT, FOOD_AMOUNT_WEIGHT, CAPSULE_WEIGHT]

    return sum([score * weight for score, weight in zip(scoreList, whightList)])

# Abbreviation
better = betterEvaluationFunction
