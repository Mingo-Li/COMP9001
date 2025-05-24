import numpy as np
from collections import deque
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform ANSI colors
init(autoreset=True)

class LightsOut:
    def __init__(self, size=5):
        self.size = size
        self.board = np.random.choice([True, False], (size, size))  # Random initial state

    def toggle(self, row, col):
        """Toggle the selected cell and its neighbors"""
        for r, c in [(row, col), (row+1, col), (row-1, col), (row, col+1), (row, col-1)]:
            if 0 <= r < self.size and 0 <= c < self.size:
                self.board[r][c] = not self.board[r][c]

    def is_solved(self):
        """Check if all lights are off"""
        return np.all(self.board == False)

    def board_to_tuple(self):
        return tuple(map(tuple, self.board))

    def print_board(self):
        print("\n" + "  " + " ".join(str(i).center(3) for i in range(self.size)) + "  ← COL")
        for i, row in enumerate(self.board):
            print(f"{i} ", end="")
            for cell in row:
                print(Fore.YELLOW + Style.BRIGHT + "(💡)" if cell else Style.DIM + "(⚫)", end=" ")
            print()
        print("↑\nROW")

    def solve_bfs(self):
        """BFS solver returning optimal moves or None if unsolvable"""
        target = np.full((self.size, self.size), False)
        queue = deque()
        visited = set()
        
        # Save initial state
        initial_state = self.board_to_tuple()
        queue.append((self.board.copy(), []))
        visited.add(initial_state)
        
        while queue:
            current_board, path = queue.popleft()
            
            if np.all(current_board == target):
                return path
            
            for row in range(self.size):
                for col in range(self.size):
                    # Create new board state
                    new_board = np.copy(current_board)
                    for r, c in [(row, col), (row+1, col), (row-1, col), (row, col+1), (row, col-1)]:
                        if 0 <= r < self.size and 0 <= c < self.size:
                            new_board[r][c] = not new_board[r][c]
                    
                    # Convert to hashable tuple
                    new_state = tuple(map(tuple, new_board))
                    
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_board, path + [(row, col)]))
        return None

def main():
    print(f"\n{Fore.CYAN}=== LIGHTS OUT ===")
    print(f"Toggle bulbs until all are off!{Style.RESET_ALL}")
    print("💡 = ON | ⚫ = OFF | 's' = Solve | 'q' = Quit\n")

    size = int(input("Enter board size (3 recommended): ") or 3)
    game = LightsOut(size)

    while not game.is_solved():
        game.print_board()
        cmd = input("Enter ROW COL (or 's'/'q'): ").lower()
        
        if cmd == 'q':
            print("Game aborted!")
            return
        elif cmd == 's':
            solution = game.solve_bfs()
            if solution:
                print(f"\n{Fore.GREEN}Optimal solution ({len(solution)} moves):{Style.RESET_ALL}")
                for i, (row, col) in enumerate(solution, 1):
                    print(f"Move {i}: toggle ({row}, {col})")
                    game.toggle(row, col)
                    game.print_board()
                break
            else:
                print(f"{Fore.RED}No solution found!{Style.RESET_ALL}")
        else:
            try:
                row, col = map(int, cmd.split())
                game.toggle(row, col)
            except:
                print(f"{Fore.RED}Invalid input! Examples: '2 3' or 's'{Style.RESET_ALL}")

    if game.is_solved():
        game.print_board()
        print(f"\n{Fore.GREEN}CONGRATULATIONS!{Style.RESET_ALL}")
        print("All lights have been turned off! 🎉\n")

if __name__ == "__main__":
    main()

