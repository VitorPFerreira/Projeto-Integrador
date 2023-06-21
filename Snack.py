import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

m_inicial = pygame.mixer.music.load("musica_inicio.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)

def musica_de_fundo():
    musica_fundo = pygame.mixer.music.load("musica_fundo.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

largura = 700
altura = 600

x_cobra = int(largura / 2)
y_cobra = int(altura / 2)

velocidade = 10
x_controle = velocidade
y_controle = 0

x_maca = randint(40, 660)
y_maca = randint(50, 530)

pontos = 0
fonte = pygame.font.SysFont('comicsans', 30)
tela = pygame.display.set_mode((largura, altura))

relogio = pygame.time.Clock()
lista_cobra = []
comprimento_inicial = 5
morte_cobra = False

def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:

        pygame.draw.rect(tela, (27, 67, 128), (XeY[0], XeY[1], 26, 26))

def reiniciar_jogo():
    global pontos, comprimento_inicial, lista_cobra, lista_cabeca, x_maca, y_maca, morte_cobra
    pontos = 0
    comprimento_inicial = 5

    lista_cobra = []
    lista_cabeca = []
    x_maca = randint(40, 660)
    y_maca = randint(50, 530)
    morte_cobra = False

tela_inicial = True
fonte_botao = pygame.font.SysFont('comicsans', 35)
cor_azul = (0, 0, 255)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da Cobra')

while tela_inicial:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            tela_inicial = False
            pygame.mixer.music.stop()
            musica_de_fundo()

    imagem_tela_inicio = pygame.image.load('imagem_inicio.jpeg')
    tela.blit(imagem_tela_inicio, (0, 0))

    texto_botao = fonte_botao.render('Pressione ESPAÇO para iniciar', True, cor_azul)
    texto_botao_rect = texto_botao.get_rect()
    texto_botao_rect.center = (largura // 2, altura // 2 + 125)

    tela.blit(texto_botao, texto_botao_rect)
    pygame.display.update()

while True:
    relogio.tick(30)

    cenario = pygame.image.load('tela_de_fundo.png')
    tela.blit(cenario, (0, 0))

    mensagem = f'Pontos: {pontos}'
    texto_formatado = fonte.render(mensagem, True, (0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT and x_controle != velocidade:
                x_controle = -velocidade
                y_controle = 0
            if event.key == K_RIGHT and x_controle != -velocidade:
                x_controle = velocidade
                y_controle = 0
            if event.key == K_UP and y_controle != velocidade:
                x_controle = 0
                y_controle = -velocidade
            if event.key == K_DOWN and y_controle != -velocidade:
                x_controle = 0
                y_controle = velocidade
    if x_controle == - velocidade and y_controle == 0:
        head_left = pygame.image.load('cabeca_esquerda.png')
        tela.blit(head_left, ((x_cobra - 32), (y_cobra - 13)))
    if x_controle == velocidade and y_controle == 0:
        head_right = pygame.image.load('cabeca_direita.png')
        tela.blit(head_right, ((x_cobra + 11), (y_cobra - 14)))
    if y_controle == -velocidade and x_controle == 0:
        head_up = pygame.image.load('cabeca_cima.png')
        tela.blit(head_up, ((x_cobra - 10), (y_cobra - 43)))
    if y_controle == velocidade and x_controle == 0:
        head_down = pygame.image.load('cabeca_baixo.png')
        tela.blit(head_down, ((x_cobra - 9), (y_cobra + 10)))

    x_cobra = x_cobra + x_controle
    y_cobra = y_cobra + y_controle

    cobra = pygame.draw.rect(tela, (1, 55, 4), (x_cobra, y_cobra, 26, 26))
    maca = pygame.draw.circle(tela, (255, 255, 255), (x_maca + 10, y_maca + 6.5), 11)

    apple_img = pygame.image.load('apple.png')
    tela.blit(apple_img, ((x_maca - 20), (y_maca - 26)))

    if cobra.colliderect(maca):
        x_maca = randint(40, 660)
        y_maca = randint(50, 530)
        pontos += 1
        comprimento_inicial = comprimento_inicial + 1
        som_colisao = pygame.mixer.Sound("som_comi.mp3")
        som_colisao.play()

    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)
    lista_cobra.append(lista_cabeca)

    if lista_cobra.count(lista_cabeca) > 1:
        som_morte = pygame.mixer.Sound("som_morri.mp3")
        som_morte.play()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("musica_morte.mp3")
        pygame.mixer.music.play(-1)
        fonte2 = pygame.font.SysFont('comicsans', 30)
        mensagem = f'Você perdeu! Sua pontuação: {pontos}'
        texto_formatado = fonte2.render(mensagem, True, (0, 0, 0))
        ret_texto = texto_formatado.get_rect()
        fonte3 = pygame.font.SysFont("comicsans", 35)
        mensagem2 = "Pressione ESPAÇO para reiniciar"
        texto_formatado2 = fonte3.render(mensagem2, True, (255, 150, 0))
        ret_texto2 = texto_formatado2.get_rect()
        morte_cobra = True
        while morte_cobra:
            imagem_tela_morte = pygame.image.load('imagem_morte.jpeg')
            tela.blit(imagem_tela_morte, (0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        x_cobra = int(largura / 2)
                        y_cobra = int(altura / 2)
                        reiniciar_jogo()
                        pygame.mixer.music.stop()
                        musica_de_fundo()
            # CONFIG TEXTO DE REINICIO DO GAME
            ret_texto.center = (largura // 2, 75)
            tela.blit(texto_formatado, ret_texto)
            ret_texto2.center = (largura // 2, 150)
            tela.blit(texto_formatado2, ret_texto2)

            pygame.display.flip()

    # CONDIÇÕES PARA QUE A COBRA REAPAREÇA NUMA POSIÇÃO OPOSTA
    if x_cobra > largura:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = largura
    if y_cobra < 0:
        y_cobra = altura
    if y_cobra > altura:
        y_cobra = 0

    # CONDIÇÃO PARA APAGAR A POSIÇÃO MAIS ANTIGA DA LISTA
    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    # COLOCAR O TEXTO NA TELA
    tela.blit(texto_formatado, (530, 5))

    # ATUALIZAR A TELA
    pygame.display.update()
