import pygame
from pygame.constants import K_BACKSPACE, K_RETURN
import requests
from solver import solve, find, is_valid

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((600, 670))
screen.fill((0,0,0))
pygame.display.set_caption('Sudoku')
font = pygame.font.SysFont('Times New Roman', 45)
small_font = pygame.font.SysFont('Times New Roman', 15)
spacing = 600 / 9
buffer = 5

#randomized board
response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
board = response.json()['board']
#store copy of original board
original_board = [[board[i][j] for j in range(len(board[0]))] for i in range(len(board))]

def user_input(screen, position):
    i = position[1]
    j = position[0]
    font = pygame.font.SysFont('Times New Roman', 45)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                # check if it selects an original value of the board
                if (original_board[i][j] != 0):
                    return
                # check if the key is backspace to delete the value in the box
                if event.key == K_BACKSPACE:
                    board[i][j] = event.key - 48
                    pygame.draw.rect(screen, (0, 0, 0), (j*spacing+buffer, i*spacing+buffer, spacing-buffer, spacing-buffer))
                    pygame.display.update()
                    return
                #checks if it's a valid number
                if (0 < event.key - 48 < 10):
                    pygame.draw.rect(screen, (0, 0, 0), (j*spacing+buffer, i*spacing+buffer, spacing-buffer, spacing-buffer))
                    value = font.render(str(event.key - 48), True, (255, 255, 255))
                    screen.blit(value, (j*spacing+20, i*spacing+10)) 
                    board[i][j] = event.key - 48
                    pygame.display.update()
                    return
                return
            

def initialize_board(bo):
    # adding the grid
    for i in range(0, 10):
        # delineates between each square in the grid
        if i % 3 == 0:
            thickness = 3
        else:
            thickness = 1
        pygame.draw.line(screen, (255, 255, 255), (0, i*spacing), (600, i*spacing), thickness)
        pygame.draw.line(screen, (255, 255, 255), (i*spacing, 0), (i*spacing, 600), thickness)

    pygame.display.update()

    #puts original numbers into correct squares
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] != 0:
                original_value = font.render(str(bo[i][j]), True, (117, 200, 255))
                screen.blit(original_value, (j*spacing+20, i*spacing+10))
    pygame.display.update()
    



def checker(bo):
    solve(original_board)
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if original_board[i][j] != bo[i][j]:
                return False
    return True

def solve_board(bo):
    solve(bo)
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if original_board[i][j] != 0:
                color = (117, 200, 255)
            else:
                color = (0,255,127)
            pygame.draw.rect(screen, (0, 0, 0), (j*spacing+buffer, i*spacing+buffer, spacing-buffer, spacing-buffer))
            value = font.render(str(bo[i][j]), True, color)
            screen.blit(value, (j*spacing+20, i*spacing+10)) 
            pygame.display.update()
    return

def main():
    spacing = 600 / 9
    initialize_board(board)

    while True:
        for event in pygame.event.get():
            #creates checker button
            check_button = small_font.render("Check Board", True, (0, 0, 0))
            mouse_pos = pygame.mouse.get_pos()
            if 25 <= mouse_pos[0] <= 200 and 620 <= mouse_pos[1] <= 655:
                #light color
                pygame.draw.rect(screen, (117, 200, 255), (25, 620, 175, 35))
            else:
                pygame.draw.rect(screen, (18, 156, 247), (25, 620, 175, 35))
            screen.blit(check_button, (75, 627))
            pygame.display.update()

            #creates solver button
            solve_button = small_font.render("Solve Board", True, (0,0,0))
            solve_pos = pygame.mouse.get_pos()
            if 300 <= solve_pos[0] <= 475 and 620 <= solve_pos[1] <= 655:
                #light color
                pygame.draw.rect(screen, (117, 200, 255), (300, 620, 175, 35))
            else:
                pygame.draw.rect(screen, (18, 156, 247), (300, 620, 175, 35))
            screen.blit(solve_button, (350, 627))
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                i = pos[0]//spacing
                j = pos[1]//spacing
                if pos[1] < 600:
                 #   print(pos)
                    #pygame.draw.rect(screen, (114,206,226), (i*spacing, j*spacing, spacing, spacing), 3)
                    user_input(screen, (int(i), int(j)))
                if (25 <= pos[0] <= 200 and 620 <= pos[1] <= 655):
                    #print(pos)
                    #print(checker(board))
                    if (checker(board)):
                        correct = small_font.render("O", True, (0,255,127))
                        pygame.draw.rect(screen, (0, 0, 0), (210, 620, 35, 35))
                        screen.blit(correct, (220, 630))
                        pygame.display.update()
                    else:
                        wrong = small_font.render("X", True, (220,20,60))
                        pygame.draw.rect(screen, (0, 0, 0), (210, 620, 35, 35))
                        screen.blit(wrong, (220, 630))
                        pygame.display.update()
                    break
                if (300 <= pos[0] <= 475 and 620 <= pos[1] <= 655):
                    new_board = [[original_board[i][j] for j in range(len(original_board[0]))] for i in range(len(original_board))]
                    solve_board(new_board)
            if event.type == pygame.QUIT:
                pygame.quit()
                return

main()