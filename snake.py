import pygame
import pygame.locals
from sys import exit
import copy
from random import randint

pygame.init()
altura = 480
largura = 640
tela = pygame.display.set_mode((largura, altura ))
relogio = pygame.time.Clock()
pygame.display.set_caption("Snake Game")
x_cobra = largura/2
y_cobra = altura/2
velocidade = 10
x_controle = velocidade
y_controle = 0
x_maca = randint(40, 600)
y_maca = randint(50, 430)
fontepontos = pygame.font.SysFont("arial", 15, True, True)
fontefases = pygame.font.SysFont("arial", 40, True, True)
pontos = 0
lista_cobra = []
comprimento_inicial = 5
morte = False
imagem_maca = pygame.image.load("apple.png")
imagem_maca = pygame.transform.scale(imagem_maca, (25, 25))
fase = 1


# Função de desenho do corpo da cobra
def aumentaCobra(lista_cobra):
    for XeY in lista_cobra:
        # XeY = [x, y]
        # XeY[0] = x
        # XeY[1] = y
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 20, 20))


#Função de reinicio do jogo
def restart():
    global fase,pontos, comprimento_inicial, x_cobra, y_cobra, velocidade, x_controle, y_controle, lista_cobra, lista_cabeca, x_maca, y_maca, morte
    pontos = 0
    fase = 1
    comprimento_inicial = 5
    x_cobra = largura/2
    y_cobra = altura/2
    velocidade = 10
    x_controle = velocidade
    y_controle = 0
    lista_cobra = []
    lista_cabeca= []
    x_maca = randint(40, 600)
    y_maca = randint(50, 430)
    morte = False


#Função verificadora de eventos
def verify_events():
    global fase,pontos, comprimento_inicial, x_cobra, y_cobra, velocidade, x_controle, y_controle, lista_cobra, lista_cabeca, x_maca, y_maca, morte
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if morte:
                restart()
                morte = False
            else: 
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if x_controle == velocidade:
                        pass
                    else:
                        x_controle = -velocidade
                        y_controle = 0
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if x_controle == -velocidade:
                        pass
                    else:
                        x_controle = velocidade
                        y_controle = 0
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if y_controle == velocidade:
                        pass
                    else:
                        x_controle = 0
                        y_controle = -velocidade
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if y_controle == -velocidade:
                        pass
                    else:
                        x_controle = 0
                        y_controle = velocidade


# Função para renderizar o jogo
def render_game():
    global fase,pontos, comprimento_inicial, x_cobra, y_cobra, velocidade, x_controle, y_controle, lista_cobra, lista_cabeca, x_maca, y_maca, morte
    pontuacao = f"Pontos: {pontos}"
    fases = f"FASE {fase}"
    texto_fases = fontefases.render(fases, True, (0, 0, 0))
    texto_formatado = fontepontos.render(pontuacao, True, (0, 0, 0))
    x_cobra = x_cobra + x_controle
    y_cobra = y_cobra + y_controle
    cobra = pygame.draw.rect(tela, (65, 105, 225), (x_cobra, y_cobra, 20, 20))
    maca = pygame.draw.rect(tela, (255, 255, 255), (x_maca, y_maca, 20, 20))
    if cobra.colliderect(maca):
        x_maca = randint(40, 600)
        y_maca = randint(50, 430)
        pontos += 1
        comprimento_inicial += 1
    # Fases de dificuldade
    if 10 <= pontos < 20 and morte == False:
        fase = 2
        tela.fill((0, 0, 0))
        texto_formatado = fontepontos.render(pontuacao, True, (255, 255, 255))
        texto_fases = fontefases.render(fases, True, (255, 255, 255))
        cobra = pygame.draw.rect(tela, (255, 255, 225), (x_cobra, y_cobra, 20, 20))
        velocidade = 12
    if pontos >= 20 and morte == False:
        fase = 3
        tela.fill((255, 0, 0))
        velocidade = 15
    if pontos >= 40 and morte == False:
        fase = 4
        tela.fill((255, 0, 0))
        velocidade = 20
    # Lista que armazena a cada frame a posição da cabeça da cobra, ou seja, os valores de posicionamento mais recentes que a cobra assume
    lista_cabeca = [x_cobra, y_cobra]
    # Lista que armazena o corpo da cobra, utilizando da posição que a cabeça passou, fazendo com que ela cresça por onde passou
    lista_cobra.append(copy.deepcopy(lista_cabeca))
    # Colisão com a parede
    if x_cobra > largura:
        morte = True
    if x_cobra < 0:
        morte = True
    if y_cobra < 0:
        morte = True
    if y_cobra > altura:
        morte = True
    # Corrigindo a colisão com o proprio corpo da cobra
    if lista_cobra.count(lista_cabeca) > 1:
        morte = True
    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]
    aumentaCobra(lista_cobra)
    tela.blit(texto_formatado, (540, 20))
    tela.blit(texto_fases, (260, 40))
    tela.blit(imagem_maca, (x_maca, y_maca))


# Função de morte
def render_morte():
    fontemorte = pygame.font.SysFont("arial", 20, True, True)
    mensagem_morte = f"Voce morreu, caso deseje reiniciar o jogo aperte qualquer tecla"
    mensagem_morte_formatado = fontemorte.render(mensagem_morte, True, (0, 0, 0))
    ret_mensagem_morte = mensagem_morte_formatado.get_rect()
    ret_mensagem_morte.center = (largura // 2, altura // 2)
    tela.blit(mensagem_morte_formatado, ret_mensagem_morte)

while True:
    relogio.tick(30)
    tela.fill((255, 255, 255))
    if not(morte):
        render_game()
    else:
        render_morte()
    pygame.display.update()
    verify_events();
