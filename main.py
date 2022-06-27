import pygame
import os
from tetriscouleur_xens2019 import *

run = True
clear = True

os.environ['SDL_VIDEO_CENTERED']='1'

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
pygame.display.set_caption("TETRIS COULEUR")
clock = pygame.time.Clock()

#colors

BLACK = (10, 10, 10)
GRAY = (127, 127, 127)
WHITE = (240, 240, 240)

RED = (240, 10, 10)
GREEN = (5, 240, 5)
BLUE = (5, 5, 240)

YELLOW = (240, 240, 10)
CYAN = (10, 240, 240)
MAGENTA = (240, 10, 240)

C1_GREEN = (204, 255, 204)
C1_BLUE = (153, 204, 255)
TITLE = (255,153,51)

BACKGROUND = (153, 204, 255)

#afficher du texte
def set_text(string, coordx, coordy, fontSize, color=BLACK):
    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    text = font.render(string, True, color) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)
#totalText = set_text("Text in Pygame!", 250, 250, 60)
#screen.blit(totalText[0], totalText[1])

#paramètres

x0, y0, x1, y1 = 200,1040,700,40
largeur, hauteur = 6, 12
p1 = (x1-x0)//largeur
p2 = (y0-y1)//hauteur

#focntions d'affichage

def fond_blanc():
    pygame.draw.rect(screen, WHITE, (x0,y1,x1-x0,y0-y1) )
    
def draw_tab():
    for i in range(1,largeur):
        pygame.draw.line(screen,BLACK, (x0+p1*i, y0), (x0+i*p1,y1), 4 )
    for j in range(1,hauteur):
        pygame.draw.line(screen,BLACK, (x0,y1+j*p2), (x1,y1+j*p2), 4 )
    pygame.draw.line(screen,BLACK, (x0-2,y0), (x1+2,y0), 8 )    
    pygame.draw.line(screen,BLACK, (x0-2,y1), (x1+2,y1), 8 )
    pygame.draw.line(screen,BLACK, (x0,y0+2), (x0,y1-2), 8 )
    pygame.draw.line(screen,BLACK, (x1+2,y0+2), (x1,y1-2), 8 )
    
def coloriercase(i,j,c):
    pygame.draw.rect(screen, c, (x0+i*p1, y1+(hauteur-j-1)*p2, p1, p2) )

def afficher(grille):
    fond_blanc()
    for x in range(largeur):
        for y in range(hauteur):
            if grille[x][y]!=VIDE:
                coloriercase(x,y,grille[x][y])
                
def afficher_score(score):
    screen.blit(*set_text('SCORE : '+str(score), 1300, 400, 60))

def afficher_temps(t):
    screen.blit(*set_text('TIME : '+str(t), 1300, 700, 60))
    
def afficher_titre():
    screen.blit(*set_text('TETRIS COULEUR', 1295, 105, 120))
    screen.blit(*set_text('TETRIS COULEUR', 1300, 100, 120,TITLE))

def refresh(score=0,t=0):
    afficher(grille)
    draw_tab()
    afficher_score(score)
    afficher_temps(t)
    afficher_titre()
    pygame.display.update()
 
#pygame

fps = 10
run = True
i, clear = 0, True
x,y = 0,0
score = 0
grille = creergrille()

while run:
    i+=1
    clock.tick(fps)
    screen.fill(BACKGROUND)

    if (y>0 and grille[x][y-1]==VIDE):
        plt.pause(0.5)
        i += 5
        descente(grille,x,y,3)
        y = y-1
        clear = False
    else:
        clear = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_UP:
                permuterbarreau(grille,x,y,3)
            if event.key == pygame.K_RIGHT:
                deplacerbarreau(grille,x,y,3,1)
                x, clear = x+1, False
            if event.key == pygame.K_LEFT:
                deplacerbarreau(grille,x,y,3,-1)
                x, clear = x-1, False
                
    refresh(score,i//10)
    if clear:
        plt.pause(0.2)
        new_score = -1
        while new_score != 0:
            if new_score==-1:
                new_score = 0
            plt.pause(0.2)
            score += new_score
            tassementgrille(grille)
            refresh(score,i//10)
            plt.pause(0.2)
            grille, new_score = effacealignement(grille)
        x = genbarreau(grille,3)
        if x==-1:
            run = False
        y = hauteur-3
        clear = False
    refresh(score,i//10)
    
pygame.quit()
        
        
    
            