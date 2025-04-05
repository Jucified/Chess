import pygame
import sys
import math

class GameEngine:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Chess")
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()
        self.current = "w"
        self.legal = []

        self.screen.fill((235, 236, 208))
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 1:
                    pygame.draw.rect(self.screen, (129, 159, 95), (x * 100, y * 100, 100, 100))

        self.white = (pygame.transform.scale(pygame.image.load("white_pawn.png").convert_alpha(), (100, 100)),
                      pygame.transform.scale(pygame.image.load("white_knight.png").convert_alpha(), (100, 100)),
                      pygame.transform.scale(pygame.image.load("white_bishop.png").convert_alpha(), (100, 100)),
                      pygame.transform.scale(pygame.image.load("white_rook.png").convert_alpha(), (100, 100)),
                      pygame.transform.scale(pygame.image.load("white_queen.png").convert_alpha(), (100, 100)),
                      pygame.transform.scale(pygame.image.load("white_king.png").convert_alpha(), (100, 100)))

        self.black = (pygame.transform.scale(pygame.image.load("black_pawn.png").convert_alpha(), (100, 100)),
                      pygame.transform.scale(pygame.image.load("black_knight.png").convert_alpha(), (100, 100)),
                      pygame.transform.scale(pygame.image.load("black_bishop.png").convert_alpha(), (100, 100)),
                      pygame.transform.scale(pygame.image.load("black_rook.png").convert_alpha(), (100, 100)),
                      pygame.transform.scale(pygame.image.load("black_queen.png").convert_alpha(), (100, 100)),
                      pygame.transform.scale(pygame.image.load("black_king.png").convert_alpha(), (100, 100)))

        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
        ]

    def update_board(self):
        self.screen.fill((235, 236, 208))
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 1:
                    pygame.draw.rect(self.screen, (129, 159, 95), (x * 100, y * 100, 100, 100))
        for x in range(8):
            for y in range(8):
                if self.board[y][x] == "*":
                    self.board[y][x] = ""
                for i in range(len(self.legal)):
                    self.board[self.legal[i][1]][self.legal[i][0]] = "*"

                piece = self.board[y][x]
                if piece == "":
                    continue
                elif piece == "*":
                    pygame.draw.circle(self.screen, (0, 0, 0, 153), (100 * x + 50, 100 * y + 50), 20)
                elif piece[0] == "b":
                    if piece[1] == "p":
                        self.screen.blit(self.black[0], (100 * x, 100 * y))
                    elif piece[1] == "n":
                        self.screen.blit(self.black[1], (100 * x, 100 * y))
                    elif piece[1] == "b":
                        self.screen.blit(self.black[2], (100 * x, 100 * y))
                    elif piece[1] == "r":
                        self.screen.blit(self.black[3], (100 * x, 100 * y))
                    elif piece[1] == "q":
                        self.screen.blit(self.black[4], (100 * x, 100 * y))
                    elif piece[1] == "k":
                        self.screen.blit(self.black[5], (100 * x, 100 * y))
                elif piece[0] == "w":
                    if piece[1] == "p":
                        self.screen.blit(self.white[0], (100 * x, 100 * y))
                    elif piece[1] == "n":
                        self.screen.blit(self.white[1], (100 * x, 100 * y))
                    elif piece[1] == "b":
                        self.screen.blit(self.white[2], (100 * x, 100 * y))
                    elif piece[1] == "r":
                        self.screen.blit(self.white[3], (100 * x, 100 * y))
                    elif piece[1] == "q":
                        self.screen.blit(self.white[4], (100 * x, 100 * y))
                    elif piece[1] == "k":
                        self.screen.blit(self.white[5], (100 * x, 100 * y))

    def flip_board(self):
        self.board = [row[::-1] for row in self.board[::-1]]

    def update_game(self):
        game.update_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                x = math.floor(x / 100)
                y = math.floor(y / 100)
                piece_type = self.board[y][x]

                if piece_type == "":
                    break
                elif piece_type == "*":
                    pass
                else:
                    self.legal.clear()
                    if piece_type[1] == "p":
                        if self.board[y - 1][x] == "":
                            self.legal.append((x, y - 1))
                            if self.board[y - 2][x] == "":
                                self.legal.append((x, y - 2))
                        # if len(self.board[y - 1][x + 1]) == 2 and self.board[y - 1][x + 1][0] != self.current:
                        #     self.legal.append((x + 1, y - 1))
                        # if len(self.board[y - 1][x - 1]) == 2 and self.board[y - 1][x - 1][0] != self.current:
                        #     self.legal.append((x - 1, y - 1))
                    elif piece_type[1] == "n":
                        self.screen.blit(self.black[1], (100 * x, 100 * y))
                    elif piece_type[1] == "b":
                        self.screen.blit(self.black[2], (100 * x, 100 * y))
                    elif piece_type[1] == "r":
                        self.screen.blit(self.black[3], (100 * x, 100 * y))
                    elif piece_type[1] == "q":
                        self.screen.blit(self.black[4], (100 * x, 100 * y))
                    elif piece_type[1] == "k":
                        self.screen.blit(self.black[5], (100 * x, 100 * y))

        pygame.display.flip()
        self.clock.tick()


game = GameEngine()
while True:
    game.update_game()
