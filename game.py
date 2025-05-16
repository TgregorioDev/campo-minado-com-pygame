import pygame
import random
import sys

TAMANHO_CELULA = 40
MARGEM = 2
LINHAS = 8
COLUNAS = 8
MINAS = 10

pygame.init()
tela = pygame.display.set_mode((COLUNAS * (TAMANHO_CELULA + MARGEM), LINHAS * (TAMANHO_CELULA + MARGEM)))
pygame.display.set_caption("Campo Minado")
fonte = pygame.font.SysFont(None, 24)

CINZA = (160, 160, 160)
BRANCO = (240, 240, 240)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 150, 0)
AZUL_ESCURO = (0, 0, 150)

campo_real = []
campo_visivel = []
jogo_ativo = True
primeiro_clique = True

def criar_campo(linhas, colunas, minas):
    global campo_real, campo_visivel, LINHAS, COLUNAS, MINAS, jogo_ativo, tela
    LINHAS, COLUNAS, MINAS = linhas, colunas, minas
    campo_real = [[' ' for _ in range(COLUNAS)] for _ in range(LINHAS)]
    campo_visivel = [[' ' for _ in range(COLUNAS)] for _ in range(LINHAS)]
    jogo_ativo = True
    largura = COLUNAS * (TAMANHO_CELULA + MARGEM)
    altura = LINHAS * (TAMANHO_CELULA + MARGEM)
    tela = pygame.display.set_mode((largura, altura))

def posicionar_minas(evitar_i=None, evitar_j=None):
    minas = 0
    while minas < MINAS:
        i = random.randint(0, LINHAS - 1)
        j = random.randint(0, COLUNAS - 1)
        if campo_real[i][j] != 'X' and (i, j) != (evitar_i, evitar_j):
            campo_real[i][j] = 'X'
            minas += 1

def contar_minas(i, j):
    total = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            ni, nj = i + x, j + y
            if 0 <= ni < LINHAS and 0 <= nj < COLUNAS:
                if campo_real[ni][nj] == 'X':
                    total += 1
    return total

def preencher_numeros():
    for i in range(LINHAS):
        for j in range(COLUNAS):
            if campo_real[i][j] != 'X':
                count = contar_minas(i, j)
                if count > 0:
                    campo_real[i][j] = str(count)

def revelar(i, j, visitados):
    if (i, j) in visitados or campo_visivel[i][j] != ' ':
        return
    visitados.add((i, j))
    campo_visivel[i][j] = campo_real[i][j]
    if campo_real[i][j] == ' ':
        for x in range(-1, 2):
            for y in range(-1, 2):
                ni, nj = i + x, j + y
                if 0 <= ni < LINHAS and 0 <= nj < COLUNAS:
                    revelar(ni, nj, visitados)

def verificar_vitoria():
    for i in range(LINHAS):
        for j in range(COLUNAS):
            if campo_visivel[i][j] == ' ' and campo_real[i][j] != 'X':
                return False
    return True

def desenhar_botao(tela, texto, x, y, largura, altura, cor_fundo, cor_texto):
    pygame.draw.rect(tela, cor_fundo, (x, y, largura, altura))
    fonte_botao = pygame.font.SysFont(None, 30)
    texto_render = fonte_botao.render(texto, True, cor_texto)
    texto_rect = texto_render.get_rect(center=(x + largura // 2, y + altura // 2))
    tela.blit(texto_render, texto_rect)
    return pygame.Rect(x, y, largura, altura)

def tela_fim_de_jogo(tela, mensagem_1, mensagem_2):
    largura_tela, altura_tela = 800, 300
    global TAMANHO_CELULA, MARGEM
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    fonte_msg = pygame.font.SysFont(None, 48)
    fonte_sub = pygame.font.SysFont(None, 36)

    rodando_fim = True
    botao_sim = None
    botao_dificuldade = None

    while rodando_fim:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if botao_sim and botao_sim.collidepoint(mouse_pos):
                    rodando_fim = False
                    return 'reiniciar'
                elif botao_dificuldade and botao_dificuldade.collidepoint(mouse_pos):
                    rodando_fim = False
                    return 'dificuldade'

        tela.fill((30, 30, 30))

        texto_1 = fonte_msg.render(mensagem_1, True, (255, 255, 255))
        texto_2 = fonte_sub.render(mensagem_2, True, (255, 255, 255))

        rect_1 = texto_1.get_rect(center=(largura_tela // 2, altura_tela // 3))
        rect_2 = texto_2.get_rect(center=(largura_tela // 2, altura_tela // 3 + 60))

        tela.blit(texto_1, rect_1)
        tela.blit(texto_2, rect_2)

        botao_sim = desenhar_botao(tela, "Sim", largura_tela // 3 - 70, 2 * altura_tela // 3, 120, 50, VERDE, BRANCO)
        botao_dificuldade = desenhar_botao(tela, "Selecionar dificuldade", 2 * largura_tela // 3 - 130, 2 * altura_tela // 3, 260, 50, AZUL_ESCURO, BRANCO)

        pygame.display.flip()

def selecionar_dificuldade():
    largura_tela, altura_tela = 600, 400
    global tela
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    fonte_msg = pygame.font.SysFont(None, 40)

    opcoes = [
        ("Fácil (8x8, 10 minas)", 8, 8, 10),
        ("Médio (12x12, 20 minas)", 12, 12, 20),
        ("Difícil (16x16, 40 minas)", 16, 16, 40),
    ]

    botoes = []
    rodando = True

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for idx, (texto, l, c, m) in enumerate(opcoes):
                    if botoes[idx].collidepoint(mouse_pos):
                        criar_campo(l, c, m)
                        rodando = False

        tela.fill((30, 30, 30))
        texto_render = fonte_msg.render("Selecione a dificuldade", True, (255, 255, 255))
        texto_rect = texto_render.get_rect(center=(largura_tela//2, altura_tela//5))
        tela.blit(texto_render, texto_rect)

        botoes = []
        for i, (texto, l, c, m) in enumerate(opcoes):
            botao = desenhar_botao(tela, texto, largura_tela//2 - 150, altura_tela//3 + i*70, 300, 50, AZUL_ESCURO, BRANCO)
            botoes.append(botao)

        pygame.display.flip()

def reiniciar_jogo():
    criar_campo(LINHAS, COLUNAS, MINAS)

def desenhar_campo():
    tela.fill(PRETO)
    for i in range(LINHAS):
        for j in range(COLUNAS):
            x = j * (TAMANHO_CELULA + MARGEM)
            y = i * (TAMANHO_CELULA + MARGEM)
            rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)

            if campo_visivel[i][j] == ' ':
                pygame.draw.rect(tela, CINZA, rect)
            elif campo_visivel[i][j] == 'F':
                pygame.draw.rect(tela, CINZA, rect)
                pygame.draw.polygon(tela, VERMELHO, [(x+10,y+30),(x+10,y+10),(x+25,y+20)])
            elif campo_visivel[i][j] == 'X':
                pygame.draw.rect(tela, VERMELHO, rect)
                pygame.draw.circle(tela, PRETO, rect.center, TAMANHO_CELULA//4)
            else:
                pygame.draw.rect(tela, BRANCO, rect)
                texto_render = fonte.render(campo_visivel[i][j], True, AZUL)
                texto_rect = texto_render.get_rect(center=rect.center)
                tela.blit(texto_render, texto_rect)
    pygame.display.flip()

selecionar_dificuldade()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN and jogo_ativo:
            x, y = evento.pos
            linha = y // (TAMANHO_CELULA + MARGEM)
            coluna = x // (TAMANHO_CELULA + MARGEM)

            if 0 <= linha < LINHAS and 0 <= coluna < COLUNAS:

                if evento.button == 1:
                    if campo_visivel[linha][coluna] == ' ':
                        if primeiro_clique:
                            posicionar_minas(linha, coluna)
                            preencher_numeros()
                            primeiro_clique = False

                        if campo_real[linha][coluna] == 'X':
                            campo_visivel[linha][coluna] = 'X'
                            jogo_ativo = False
                            acao = tela_fim_de_jogo(tela, " Você pisou em uma mina!", "Tentar novamente?")
                            if acao == 'reiniciar':
                                primeiro_clique = True
                                reiniciar_jogo()
                            elif acao == 'dificuldade':
                                primeiro_clique = True
                                selecionar_dificuldade()

                        else:
                            revelar(linha, coluna, set())
                            if verificar_vitoria():
                                jogo_ativo = False
                                acao = tela_fim_de_jogo(tela, " Parabéns! Você venceu!", "Jogar novamente?")
                                if acao == 'reiniciar':
                                    primeiro_clique = True
                                    reiniciar_jogo()
                                elif acao == 'dificuldade':
                                    primeiro_clique = True
                                    selecionar_dificuldade()

                elif evento.button == 3:
                    if campo_visivel[linha][coluna] == ' ':
                        campo_visivel[linha][coluna] = 'F'
                    elif campo_visivel[linha][coluna] == 'F':
                        campo_visivel[linha][coluna] = ' '

    desenhar_campo()