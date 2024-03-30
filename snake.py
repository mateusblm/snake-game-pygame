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
fonte = pygame.font.SysFont("arial", 20, True, True)
pontos = 0
lista_cobra = []
comprimento_inicial = 5
morte = False
imagem_maca = pygame.image.load("apple.png")
imagem_maca = pygame.transform.scale(imagem_maca, (25, 25))
# Função de desenho do corpo da cobra
def aumentaCobra(lista_cobra):
    for XeY in lista_cobra:
        # XeY = [x, y]
        # XeY[0] = x
        # XeY[1] = y
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 20, 20))
def restart():
    global pontos, comprimento_inicial, x_cobra, y_cobra, velocidade, x_controle, y_controle, lista_cobra, lista_cabeca, x_maca, y_maca, morte
    pontos = 0
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
while True:
    relogio.tick(30)
    tela.fill((255, 255, 255))
    pontuacao = f"Pontos: {pontos}"
    texto_formatado = fonte.render(pontuacao, True, (0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Dificultando um pouco após 25 pontos e 50 pontos
        if comprimento_inicial > 25:
            velocidade = 12
        elif comprimento_inicial > 50:
            velocidade = 14
        else:
            velocidade = 10
        if event.type == pygame.KEYDOWN:
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
    x_cobra = x_cobra + x_controle
    y_cobra = y_cobra + y_controle
    cobra = pygame.draw.rect(tela, (65, 105, 225), (x_cobra, y_cobra, 20, 20))
    maca = pygame.draw.rect(tela, (255, 255, 255), (x_maca, y_maca, 20, 20))
    if cobra.colliderect(maca):
        x_maca = randint(40, 600)
        y_maca = randint(50, 430)
        pontos += 1
        comprimento_inicial += 1
    # Lista que armazena a cada frame a posição da cabeça da cobra, ou seja, os valores de posicionamento mais recentes que a cobra assume
    lista_cabeca = [x_cobra, y_cobra]
    # Lista que armazena o corpo da cobra, utilizando da posição que a cabeça passou, fazendo com que ela cresça por onde passou
    lista_cobra.append(copy.deepcopy(lista_cabeca))
    # Cena de morte
    fontemorte = pygame.font.SysFont("arial", 20, True, True)
    mensagem_morte = f"Game Over, pressione a tecla R para reiniciar o jogo"
    mensagem_morte_formatado = fontemorte.render(mensagem_morte, True, (0, 0, 0))
    ret_mensagem_morte = mensagem_morte_formatado.get_rect()
    ret_mensagem_morte.center = (largura // 2, altura // 2)
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
 
    while morte:
        tela.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    morte = False
            tela.blit(mensagem_morte_formatado, ret_mensagem_morte)
            pygame.display.update() 
    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumentaCobra(lista_cobra)
    tela.blit(texto_formatado, (450, 40))
    tela.blit(imagem_maca, (x_maca, y_maca))
    pygame.display.update()
