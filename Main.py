import pygame
import sys
import math

class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Chess")
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()

        self.current: str = "w"
        self.opposite: str = "b"
        self.clicked: tuple[int, int, str] = (0, 0, "")
        self.legal: list[tuple[int, int]] = []

        self.pieces = (
            (pygame.transform.scale(pygame.image.load("white_pawn.png").convert_alpha(), (100, 100)),
             pygame.transform.scale(pygame.image.load("white_knight.png").convert_alpha(), (100, 100)),
             pygame.transform.scale(pygame.image.load("white_bishop.png").convert_alpha(), (100, 100)),
             pygame.transform.scale(pygame.image.load("white_rook.png").convert_alpha(), (100, 100)),
             pygame.transform.scale(pygame.image.load("white_queen.png").convert_alpha(), (100, 100)),
             pygame.transform.scale(pygame.image.load("white_king.png").convert_alpha(), (100, 100))
             ),
            (pygame.transform.scale(pygame.image.load("black_pawn.png").convert_alpha(), (100, 100)),
             pygame.transform.scale(pygame.image.load("black_knight.png").convert_alpha(), (100, 100)),
             pygame.transform.scale(pygame.image.load("black_bishop.png").convert_alpha(), (100, 100)),
             pygame.transform.scale(pygame.image.load("black_rook.png").convert_alpha(), (100, 100)),
             pygame.transform.scale(pygame.image.load("black_queen.png").convert_alpha(), (100, 100)),
             pygame.transform.scale(pygame.image.load("black_king.png").convert_alpha(), (100, 100))
             )
        )

        self.moves = (pygame.transform.scale(pygame.image.load("moves_dot.png").convert_alpha(), (100, 100)),
                      pygame.transform.scale(pygame.image.load("moves_ring.png").convert_alpha(), (100, 100)))

        self.board: list[list[str]] = [
            ["br ", "bn ", "bb ", "bq ", "bk ", "bb ", "bn ", "br "],
            ["bp ", "bp ", "bp ", "bp ", "bp ", "bp ", "bp ", "bp "],
            ["   ", "   ", "   ", "   ", "   ", "   ", "   ", "   "],
            ["   ", "   ", "   ", "   ", "   ", "   ", "   ", "   "],
            ["   ", "   ", "   ", "   ", "   ", "   ", "   ", "   "],
            ["   ", "   ", "   ", "   ", "   ", "   ", "   ", "   "],
            ["wp ", "wp ", "wp ", "wp ", "wp ", "wp ", "wp ", "wp "],
            ["wr ", "wn ", "wb ", "wq ", "wk ", "wb ", "wn ", "wr "]
        ]

    def draw_chessboard(self) -> None:
        """Draws the chessboard"""
        self.screen.fill((235, 236, 208))
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 1:
                    pygame.draw.rect(self.screen, (129, 159, 95), (100 * x, 100 * y, 100, 100))

    def draw_pieces(self) -> None:
        """Draws the pieces on the chessboard based on self.board"""
        for x in range(8):
            for y in range(8):
                piece: str = self.board[y][x]
                if piece[:2] == "  ": continue

                color: int = 0 if piece[0] == "w" else 1
                piece_type: int = ["p", "n", "b", "r", "q", "k"].index(piece[1])
                self.screen.blit(self.pieces[color][piece_type], (100 * x, 100 * y))

    def draw_legal_moves(self) -> None:
        """Draws legal spots to move to based on self.board"""
        for x, y in self.legal:
            if self.board[y][x][:2] == "  ":
                self.screen.blit(self.moves[0], (100 * x, 100 * y))
            else:
                self.screen.blit(self.moves[1], (100 * x, 100 * y))

    def update_board(self) -> None:
        """Re-draws the chessboard"""
        self.draw_chessboard()
        self.draw_pieces()
        self.draw_legal_moves()

    def legal_pawn_moves(self, x: int, y: int) -> None:
        """Adds legal pawn moves to self.legal"""
        if self.board[y - 1][x] == "   ":
            self.legal.append((x, y - 1))
            if self.board[y - 2][x] == "   " and y == 6:
                self.legal.append((x, y - 2))
        if x != 7 and self.board[y - 1][x + 1][0] == self.opposite:
            self.legal.append((x + 1, y - 1))
        if x != 0 and self.board[y - 1][x - 1][0] == self.opposite:
            self.legal.append((x - 1, y - 1))

    def legal_knight_moves(self, x: int, y: int) -> None:
        """Adds legal knight moves to self.legal"""
        for a in range(-1, 2, 2):
            for b in range(-2, 3, 4):
                if 0 <= x + a < 8 and 0 <= y + b < 8 and self.board[y + b][x + a][0] != self.current:
                    self.legal.append((x + a, y + b))
        for a in range(-2, 3, 4):
            for b in range(-1, 2, 2):
                if 0 <= x + a < 8 and 0 <= y + b < 8 and self.board[y + b][x + a][0] != self.current:
                    self.legal.append((x + a, y + b))

    def legal_bishop_moves(self, x: int, y: int) -> None:
        """Adds legal bishop moves to self.legal"""
        for sign_x in range(-1, 2, 2):
            for sign_y in range(-1, 2, 2):
                distance_x: int = sign_x
                distance_y: int = sign_y
                while 0 <= x - distance_x < 8 and 0 <= y - distance_y < 8:
                    if self.board[y - distance_y][x - distance_x][:2] == "  ":
                        self.legal.append((x - distance_x, y - distance_y))
                    elif self.board[y - distance_y][x - distance_x][0] == self.opposite:
                        self.legal.append((x - distance_x, y - distance_y))
                        break
                    else: break
                    distance_x += sign_x
                    distance_y += sign_y

    def legal_rook_moves(self, x: int, y: int) -> None:
        """Adds legal rook moves to self.legal"""
        for sign in range(-1, 2, 2):
            distance: int = sign
            while 0 <= x + distance < 8:
                if self.board[y][x + distance][:2] == "  ":
                    self.legal.append((x + distance, y))
                elif self.board[y][x + distance][0] == self.opposite:
                    self.legal.append((x + distance, y))
                    break
                else: break
                distance += sign
        for sign in range(-1, 2, 2):
            distance: int = sign
            while 0 <= y + distance < 8:
                if self.board[y + distance][x][:2] == "  ":
                    self.legal.append((x, y + distance))
                elif self.board[y + distance][x][0] == self.opposite:
                    self.legal.append((x, y + distance))
                    break
                else: break
                distance += sign

    def legal_queen_moves(self, x: int, y: int) -> None:
        """Adds legal queen moves to self.legal"""
        self.legal_bishop_moves(x, y)
        self.legal_rook_moves(x, y)

    def legal_king_moves(self, x: int, y: int) -> None:
        """Adds legal king moves to self.legal"""
        for a in range(-1, 2):
            for b in range(-1, 2):
                if 0 <= x + a < 8 and 0 <= y + b < 8 and self.board[y + b][x + a][0] != self.current:
                    self.legal.append((x + a, y + b))

    def add_legal_moves(self, x: int, y: int) -> None:
        """Adds the legal moves to self.legal"""
        piece: str = self.board[y][x]
        self.legal.clear()
        match piece[1]:
            case "p":
                self.legal_pawn_moves(x, y)
            case "n":
                self.legal_knight_moves(x, y)
            case "b":
                self.legal_bishop_moves(x, y)
            case "r":
                self.legal_rook_moves(x, y)
            case "q":
                self.legal_queen_moves(x, y)
            case "k":
                self.legal_king_moves(x, y)
        for x, y in self.legal:
            self.board[y][x] = self.board[y][x][:2] + "*"

    def move_piece(self, x: int, y: int) -> None:
        """Moves a piece to a legal spot"""
        self.board[self.clicked[1]][self.clicked[0]] = "   "
        self.board[y][x] = self.clicked[2]
        for x in range(8):
            for y in range(8):
                if self.board[y][x][2] == "*":
                    self.board[y][x] = self.board[y][x][:2] + " "

    def switch_turns(self) -> None:
        """Flips the board and switches turns"""
        self.board = [row[::-1] for row in self.board[::-1]]
        self.current, self.opposite = self.opposite, self.current

    def on_mouse_click(self, position: tuple[int, int]) -> None:
        """Run when the board is clicked"""
        x: int = math.floor(position[0] / 100)
        y: int = math.floor(position[1] / 100)

        if self.board[y][x] == "   ": return
        if self.board[y][x][2] == " " and self.board[y][x][0] == self.opposite: return

        if self.board[y][x][2] == "*":
            self.move_piece(x, y)
            self.clicked = (0, 0, "")
            self.legal.clear()
            self.switch_turns()
        else:
            self.add_legal_moves(x, y)
            self.clicked = (x, y, self.board[y][x])

    def update_game(self) -> None:
        """Main game loop"""
        game.update_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.on_mouse_click(event.pos)

        pygame.display.flip()
        self.clock.tick()


game = GameEngine()
while True:
    game.update_game()
