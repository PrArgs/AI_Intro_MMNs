# MMN15 MCP - Missionaries and Cannibals Problem

This assignment focuses on problem representation and search algorithm implementation for the Missionaries and Cannibals Problem (MCP) in the field of Artificial Intelligence.

## Disclaimer
This README file was written with the assistance of ChatGPT in order to meet industry conventions, avoid typos, and ensure clarity. However, each and every word was reviewed by me, and additions were made to meet the assignment's demands.

## Problem Representation

To represent the MCP, the following classes and data structures have been implemented:

1. `MissionariesCannibalsProblem` class: This class represents the state, actions, and constraints of the MCP. Each state is represented as a list with the following elements:
   - Number of Missionaries on the left bank
   - Number of Cannibals on the left bank
   - Number of Missionaries on the right bank
   - Number of Cannibals on the right bank
   - Boat position (0 for left bank, 1 for right bank)

   - The goal as I set it, is to move all people from the Right bank to the Left bank

## Legal Successors (how i developed the states)
In the Missionaries and Cannibals Problem (MCP), the legal successors refer to the valid states that can be reached from the current state by applying a valid action. The successors are generated based on the constraints of the problem, which are as follows:

The number of cannibals on either side of the river should not exceed the number of missionaries. Otherwise, the cannibals would overpower the missionaries, resulting in an invalid state.

 To create the legal successors, the following approach was used:

    Iterate through all possible combinations of moving the missionaries and cannibals across the river.
    Check if the combination is valid based on the constraints mentioned above.
    If the combination is valid, create a new state by updating the number of missionaries, cannibals, and boat position accordingly.
    Add the new state to the list of legal successors.
    By systematically exploring all possible combinations and filtering out the invalid ones, the legal successors for each state can be generated.

    This approach ensures that only valid states are considered during the search process, leading to a solution that satisfies the problem constraints.


2. Search Algorithms: 4 search algorithms have been implemented to find a solution to the MCP:
I used the Util file from MMN11 in order to use Data structures like the Queue in BFS and the Sstack in IDDFS 
and the PriorityQueue in GBFS and A*. Although, I did changed PriorityQueue a little bit in order to get the priority as well when pop 

## Breadth-First Search (BFS)
BFS is an uninformed search algorithm that explores all the neighbors of a node before moving to the next level, ensuring the shortest path is found in terms of the number of states 'till destenation.


## Iterative Deepening Depth-First Search (IDDFS)
IDDFS is an uninformed search algorithm that combines the benefits of BFS and DFS by repeatedly performing a depth-limited search with increasing depth limits, ensuring the optimal solution is found while maintaining memory efficiency. usnig a Stack.

## Greedy Best-First Search (GBFS)
GBFS is an informed search algorithm that selects the most promising node based on a heuristic function, prioritizing nodes that are estimated to be closer to the goal state. It does not guarantee an optimal solution since it is also a greedy algorithm

## A* Search
A* is an informed search algorithm that combines the advantages of both BFS and GBFS. It uses a heuristic function to estimate the cost of reaching the goal state from a specific node and considers both the actual cost and the heuristic cost to make informed decisions. A* guarantees an optimal solution.

## Heuristic for the Missionaries and Cannibals Problem
The heuristic function used in this implementation calculates the number of trips required to reach the goal state. It considers the number of missionaries and cannibals on both banks and the current boat position. The heuristic decreases as more people are moved from the right bank to the left bank, and it increases if moving two people from the left bank to the right bank is required. 

## Running the Search Algorithms

To run the search algorithms and find a solution to the MCP, follow these steps:

1. Ensure you have Python installed on your system.
2. Open the `MCPProblem.py` file in a Python IDE or text editor.
3. Run the `main` function.

The program will execute the implemented search algorithms and display the solution path if found.

## File Structure

The project directory contains the following files:

- `MCPProblem.py`: The main script to run the search algorithms.
- `util.py`: Utility module providing data structures and functions for the search algorithms (FROM MMN11).
- `README.md`: This file, providing an overview of the project.

## Acknowledgements

This MCP project is part of the MMN15 assignment for practicing problem representation and search algorithm implementation. It is developed by [Roi Argaman].
so please don't copy it.

## Contact

For any questions or suggestions regarding this project, please contact [argamanroi@gmail.com].

Feel free to update and customize this README file to match the specific details and requirements of your MCP project.