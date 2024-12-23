"""Created by Leon Asanovski - 221007"""

import random
import pygame
import sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 1000
REVEALSPEED = 8
BOXSIZE = 120
BOARDIMENSIONS = 5
XMARGIN = 100
YMARGIN = 200

ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)
BLUE = (0, 0, 139)
TURQUOISE = (48, 213, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (240, 240, 240)

colors = {
    "orange": ORANGE,
    "purple": PURPLE,
    "turquoise": TURQUOISE,
    "blue": BLUE,
}


def getRandomFont():
    return pygame.font.SysFont("arial", size=30, bold=True)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def makeText(text, color1, color2, top, left):
    textSurf = BASICFONT.render(text, True, color1, color2)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return textSurf, textRect


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * BOXSIZE) + (tileX - 1)
    top = YMARGIN + (tileY * BOXSIZE) + (tileY - 1)
    return left, top


def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if tileRect.collidepoint(x, y):
                return tileX, tileY
    return None, None


def drawTile(tilex, tiley, color, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, color, (left + adjx, top + adjy, BOXSIZE, BOXSIZE))
    pygame.draw.rect(DISPLAYSURF, BLACK, (left + adjx, top + adjy, BOXSIZE, BOXSIZE), 2)


def drawPalette():
    pygame.draw.circle(DISPLAYSURF, ORANGE, (150, 100), 50, 0)
    pygame.draw.circle(DISPLAYSURF, PURPLE, (300, 100), 50, 0)
    pygame.draw.circle(DISPLAYSURF, TURQUOISE, (450, 100), 50, 0)
    pygame.draw.circle(DISPLAYSURF, BLUE, (600, 100), 50, 0)

    pygame.draw.circle(DISPLAYSURF, BLACK, (150, 100), 50, 3)
    pygame.draw.circle(DISPLAYSURF, BLACK, (300, 100), 50, 3)
    pygame.draw.circle(DISPLAYSURF, BLACK, (450, 100), 50, 3)
    pygame.draw.circle(DISPLAYSURF, BLACK, (600, 100), 50, 3)


def check_valid_move(board, tileX, tileY, selected_color):
    actions = ((0, -1), (0, +1), (1, 0), (-1, 0))
    for action in actions:
        x = tileX + action[0]
        y = tileY + action[1]
        if 0 <= x < len(board) and 0 <= y < len(board[0]):
            if board[x][y] == selected_color:
                return False
    return True


def drawBoard(board):
    DISPLAYSURF.fill(BOARD_COLOR)
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            color = board[tilex][tiley] if board[tilex][tiley] else WHITE
            drawTile(tilex, tiley, color)

    left, top = getLeftTopOfTile(0, 0)
    width = 600
    height = 600
    pygame.draw.rect(DISPLAYSURF, BLACK, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


def checkIfWin(board):
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley] == "":
                return False
    return True


def fadeOutBoard(board):
    fade_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    fade_surface.fill(BOARD_COLOR)
    fade_surface.set_alpha(0)

    alpha = 0
    while alpha <= 255:
        checkForQuit()

        drawBoard(board)
        displayMessage("Congratulations, you have won the game!")

        fade_surface.set_alpha(alpha)
        DISPLAYSURF.blit(fade_surface, (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        alpha += 5

    DISPLAYSURF.fill(BOARD_COLOR)
    pygame.display.update()

    pygame.time.wait(1000)


def displayMessage(message):
    textSurf = BASICFONT.render(message, True, BLUE, BOARD_COLOR)
    textRect = textSurf.get_rect()
    textRect.topleft = (175, 50)
    DISPLAYSURF.blit(textSurf, textRect)


def autoSolve(colors):
    board = [["" for _ in range(BOARDIMENSIONS)] for _ in range(BOARDIMENSIONS)]
    color_list = list(colors)
    random.shuffle(color_list)
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            if board[tileX][tileY] == "":
                for color in color_list:
                    if check_valid_move(board, tileX, tileY, color):
                        board[tileX][tileY] = color
                        break
    drawBoard(board)
    displayMessage("This is a representation of a solved board")
    pygame.display.update()
    pygame.time.wait(3000)
    return [["" for _ in range(BOARDIMENSIONS)] for _ in range(BOARDIMENSIONS)]


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Color Fill Puzzle')

    BASICFONT = getRandomFont()

    RESET_SURF, RESET_RECT = makeText('Reset', WHITE, ORANGE, WINDOWWIDTH - 180, WINDOWHEIGHT - 50)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve', WHITE, BLUE, WINDOWWIDTH - 180, WINDOWHEIGHT - 90)

    board = [["" for _ in range(BOARDIMENSIONS)] for _ in range(BOARDIMENSIONS)]
    selected_color = None

    while True:
        if checkIfWin(board):
            fadeOutBoard(board)
            board = [["" for _ in range(BOARDIMENSIONS)] for _ in range(BOARDIMENSIONS)]
            selected_color = None
            continue

        checkForQuit()
        drawBoard(board)
        drawPalette()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                if RESET_RECT.collidepoint(mouseX, mouseY):
                    print("Reset button clicked!")
                    board = [["" for _ in range(BOARDIMENSIONS)] for _ in range(BOARDIMENSIONS)]
                    selected_color = None
                    continue
                elif SOLVE_RECT.collidepoint(mouseX, mouseY):
                    print("Solving board automatically!")
                    board = autoSolve(colors.keys())
                    selected_color = None
                    continue
                else:
                    if pygame.Rect(100, 50, 100, 100).collidepoint(mouseX, mouseY):
                        selected_color = ORANGE
                    elif pygame.Rect(250, 50, 100, 100).collidepoint(mouseX, mouseY):
                        selected_color = PURPLE
                    elif pygame.Rect(400, 50, 100, 100).collidepoint(mouseX, mouseY):
                        selected_color = TURQUOISE
                    elif pygame.Rect(550, 50, 100, 100).collidepoint(mouseX, mouseY):
                        selected_color = BLUE
                    tileX, tileY = getSpotClicked(board, mouseX, mouseY)
                    if tileX is not None and tileY is not None and selected_color and check_valid_move(board, tileX,
                                                                                                       tileY,
                                                                                                       selected_color):
                        board[tileX][tileY] = selected_color

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
