import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
X_COLOR = (84, 84, 84)

# Pygame Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe with AI')
screen.fill(BG_COLOR)


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Row check
        row_ind = square // 3
        row = self.board[row_ind * 3: (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        # Column check
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Diagonal checks
        if square % 2 == 0:
            diagonal1 = [self.board[0], self.board[4], self.board[8]]
            if all([spot == letter for spot in diagonal1]):
                return True

            diagonal2 = [self.board[2], self.board[4], self.board[6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False

    def minimax(self, state, depth, maximizing_player, alpha=-math.inf, beta=math.inf):
        case = self.check_winner(state)

        if case == 'X':
            return 1, None
        elif case == 'O':
            return -1, None
        elif case == 'Tie':
            return 0, None

        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for possible_move in self.available_moves():
                state[possible_move] = 'X'
                eval, _ = self.minimax(state, depth + 1, False, alpha, beta)
                state[possible_move] = ' '

                if eval > max_eval:
                    max_eval = eval
                    best_move = possible_move

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            min_eval = math.inf
            best_move = None
            for possible_move in self.available_moves():
                state[possible_move] = 'O'
                eval, _ = self.minimax(state, depth + 1, True, alpha, beta)
                state[possible_move] = ' '

                if eval < min_eval:
                    min_eval = eval
                    best_move = possible_move

                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move

    def check_winner(self, board):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]

        for combo in winning_combinations:
            if (board[combo[0]] == board[combo[1]] == board[combo[2]]) and board[combo[0]] != ' ':
                return board[combo[0]]

        if ' ' not in board:
            return 'Tie'

        return None


def draw_lines():
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)


def draw_figures(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            index = row * 3 + col
            if board[index] == 'O':
                # Draw circle
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                    int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   SQUARE_SIZE // 3, 10)
            elif board[index] == 'X':
                # Draw X
                pygame.draw.line(screen, X_COLOR,
                                 (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + 50),
                                 ((col + 1) * SQUARE_SIZE - 50, (row + 1) * SQUARE_SIZE - 50), 15)
                pygame.draw.line(screen, X_COLOR,
                                 (col * SQUARE_SIZE + 50, (row + 1) * SQUARE_SIZE - 50),
                                 ((col + 1) * SQUARE_SIZE - 50, row * SQUARE_SIZE + 50), 15)


def get_square_from_mouse():
    mouseX, mouseY = pygame.mouse.get_pos()
    col = mouseX // SQUARE_SIZE
    row = mouseY // SQUARE_SIZE
    return row * 3 + col


def display_message(message):
    font = pygame.font.Font(None, 75)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)


def main():
    game = TicTacToe()

    # Drawing initial board
    draw_lines()
    pygame.display.update()

    current_player = 'X'  # Human starts
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == 'X':
                mouseX, mouseY = event.pos
                clicked_square = get_square_from_mouse()

                if game.board[clicked_square] == ' ':
                    game.make_move(clicked_square, 'X')
                    draw_figures(game.board)
                    pygame.display.update()

                    # Check for human win/tie
                    result = game.check_winner(game.board)
                    if result:
                        if result == 'X':
                            display_message('You Win!')
                        elif result == 'Tie':
                            display_message('Tie Game!')
                        game_over = True
                        break

                    # AI's turn
                    current_player = 'O'

            # AI Move
            if current_player == 'O':
                _, best_move = game.minimax(game.board, 0, False)
                game.make_move(best_move, 'O')
                draw_figures(game.board)
                pygame.display.update()

                # Check for AI win/tie
                result = game.check_winner(game.board)
                if result:
                    if result == 'O':
                        display_message('AI Wins!')
                    elif result == 'Tie':
                        display_message('Tie Game!')
                    game_over = True
                    break

                current_player = 'X'


main()
pygame.quit()