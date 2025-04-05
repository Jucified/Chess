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

        self.board = [
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

    def add_legal_moves(self, x: int, y: int) -> None:
        """Adds the legal moves to self.legal"""
        piece: str = self.board[y][x]
        self.legal.clear()
        match piece[1]:
            case "p":
                if self.board[y - 1][x] == "   ":
                    self.legal.append((x, y - 1))
                    if self.board[y - 2][x] == "   ":
                        self.legal.append((x, y - 2))
                if x != 7 and self.board[y - 1][x + 1][0] == self.opposite:
                    self.legal.append((x + 1, y - 1))
                if x != 0 and self.board[y - 1][x - 1][0] == self.opposite:
                    self.legal.append((x - 1, y - 1))

            case "n":
                pass

            case "b":
                pass

            case "r":
                pass

            case "q":
                pass

            case "k":
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        m, n = x + a, y + b
                        if 0 <= m < 8 and 0 <= n < 8 and self.board[n][m][0] != self.current:
                            self.legal.append((m, n))

    def move_piece(self) -> None:
        pass

    def switch_turns(self) -> None:
        self.board = [row[::-1] for row in self.board[::-1]]
        self.current, self.opposite = self.opposite, self.current

    def on_mouse_click(self, event) -> None:
        x, y = event.pos
        x: int = math.floor(x / 100)
        y: int = math.floor(y / 100)

        if self.board[y][x] == "   ": return
        if self.board[y][x][0] != self.current and self.board[y][x][2] != "*": return

        if self.board[y][x] == "  *":
            self.move_piece()
        else:
            self.add_legal_moves(x, y)

    def update_game(self) -> None:
        game.update_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.on_mouse_click(event)

        pygame.display.flip()
        self.clock.tick()


game = GameEngine()
while True:
    game.update_game()
