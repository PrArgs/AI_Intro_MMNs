q.1 - reflex agent
since we can only see one step ahead the Reflex Agent evaluation Function will determine which states are
to be penalized and which to be reworded:
penalized:
-too close to a monster
- not eating or getting farther from the closest food 
reward (not penalized):
- eating


q2- MinimaxAgent ExpectimaxAgent
Implementation of the algorithm based on pseudocode in the textbook.
since there is more than one Monster we need to make sure the first ghost will take the minimal action of 
the second ghost which in turn takes the minimal action of the next Max agent (Pacman).
in other words, we have a tree with 2 Min Node and one Max node.
the course of action will be chosen by the max agent from the minimal option available from the first 
Min agent that had chosen (like mentioned) the minimal action from the minimal action of it Min 
Agents (plural)
Hence we will always choose the curse with minimal damage and maximal gain for Pacman (up to the depth searched for)


q3- AlphaBetaAgent
Implementation of the algorithm based on pseudocode in the textbook.
Like the MiniMax agent, we have triplets of agents in each depth (Max, Min, Min)
only now each agent will be able to cut off any node that will lead to a path known to be possible to be chosen.
we can see that even the First Min agent wouldn't calculate all of it's other Min Agents


q4- ExpectimaxAgent
Implementation of the algorithm based on pseudocode in the textbook.
Like the MiniMax agent, we have triplets of agents in each depth (Max, Min, Min)
unlike AlphaBetaAgent since the actions of the Min agents are random and equally possible
meaning the best action for the Min agent wouldn't necessarily be chosen by its Min Agent.
since the actions of the ghost are random we will return the average of the cost of each step since this is the 
probability of the sum of the actions for this agent.


q.5 - BetterEvaluationFunction
After trial and error, we discovered an acceptable weight for each of the following:
	1. Current game score
	2. Food Amount left on board
	3. posible ghoest eating
	4. Distance to the nearest food
	5. Capsule remained

once we sum each of the above after multiplying each with its proper weight we can make sure that 
Pacman will choose the best move (in most cases and for the next 2 moves only) 

