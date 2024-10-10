import numpy as np
from collections import deque

class Node:
    def __init__(self, state, parent, action):
        self.state = state  # The puzzle configuration (as a 2D array)
        self.parent = parent  # Parent node (used to trace back the solution)
        self.action = action  # Action taken to reach this state (e.g., 'up', 'down')

class Puzzle:
    def __init__(self, start, start_index, goal, goal_index):
        self.start = [start, start_index]  # Starting puzzle state and blank tile index
        self.goal = [goal, goal_index]  # Goal puzzle state and blank tile index
        self.solution = None  # To store the final solution path

    def neighbors(self, state):
        mat, (row, col) = state  # Puzzle state and the position of the blank tile (0)
        results = []

        # Move the blank tile up
        if row > 0:
            mat1 = np.copy(mat)
            mat1[row][col] = mat1[row - 1][col]
            mat1[row - 1][col] = 0
            results.append(('up', [mat1, (row - 1, col)]))

        # Move the blank tile left
        if col > 0:
            mat1 = np.copy(mat)
            mat1[row][col] = mat1[row][col - 1]
            mat1[row][col - 1] = 0
            results.append(('left', [mat1, (row, col - 1)]))

        # Move the blank tile down
        if row < 2:
            mat1 = np.copy(mat)
            mat1[row][col] = mat1[row + 1][col]
            mat1[row + 1][col] = 0
            results.append(('down', [mat1, (row + 1, col)]))

        # Move the blank tile right
        if col < 2:
            mat1 = np.copy(mat)
            mat1[row][col] = mat1[row][col + 1]
            mat1[row][col + 1] = 0
            results.append(('right', [mat1, (row, col + 1)]))

        return results

    def solve_bfs(self):
        """Breadth-First Search (BFS) implementation for solving the 8-puzzle."""
        # Initialize the frontier with the starting node (queue)
        start = Node(state=self.start, parent=None, action=None)
        frontier = deque([start])  # Using deque for fast popping from the left (FIFO)

        explored = []  # List to keep track of explored states

        while frontier:
            # Dequeue the node (FIFO)
            node = frontier.popleft()

            # Check if the current state is the goal state
            if (node.state[0] == self.goal[0]).all():
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return self.solution

            # Add the current state to the explored set
            explored.append(node.state)

            # Expand the neighbors of the current state
            for action, neighbor in self.neighbors(node.state):
                # If the neighbor state has not been explored and is not in the frontier
                if not any((explored_state[0] == neighbor[0]).all() for explored_state in explored):
                    if not any((frontier_node.state[0] == neighbor[0]).all() for frontier_node in frontier):
                        # Add the neighbor to the frontier
                        child_node = Node(state=neighbor, parent=node, action=action)
                        frontier.append(child_node)

        # No solution found
        raise Exception("No solution found.")

    def print_solution(self):
        if self.solution is None:
            print("No solution available.")
            return

        # Print the solution path
        print("Initial State:")
        print(self.start[0], "\n")

        for action, state in zip(self.solution[0], self.solution[1]):
            print(f"Action: {action}")
            print(state[0], "\n")

        print("Goal Reached!")


# Function to take user input and convert it to a 3x3 matrix
def get_puzzle_input():
    print("Enter the 8-puzzle configuration (use 0 for the blank space):")
    puzzle = []
    for i in range(3):
        row = input(f"Enter row {i + 1} (space-separated numbers): ").split()
        puzzle.append([int(num) for num in row])
    return np.array(puzzle)

# Get user input for start and goal states
start = get_puzzle_input()
goal = get_puzzle_input()

# Find the index of the blank tile (0) in the initial and goal states
start_index = (np.where(start == 0)[0][0], np.where(start == 0)[1][0])
goal_index = (np.where(goal == 0)[0][0], np.where(goal == 0)[1][0])

# Create the puzzle object
puzzle = Puzzle(start, start_index, goal, goal_index)

# Solve the puzzle using BFS
puzzle.solve_bfs()

# Print the solution path
puzzle.print_solution()
