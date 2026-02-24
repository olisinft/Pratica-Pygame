import os
import pygame
import random
CAMINHO_BASE= os.path.dirname(__file__)
CAMINHO_IMAGENS = os.path.join(CAMINHO_BASE, 'imagens')
#tamanho tela
LARGURA_TELA = 500
ALTURA_TELA = 800

#aumentando o tamanho da imagem e fazendo o caminho dentro do sistema para dar loading nela
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join(CAMINHO_IMAGENS, 'base.png')))
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join(CAMINHO_IMAGENS, 'pipe.png')))
IMAGEM_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join(CAMINHO_IMAGENS, 'bg.png')))
IMAGENS_PASSARO = [pygame.transform.scale2x(pygame.image.load(os.path.join(CAMINHO_IMAGENS, 'bird1.png'))),
                    pygame.transform.scale2x(pygame.image.load(os.path.join(CAMINHO_IMAGENS, 'bird2.png'))),
                    pygame.transform.scale2x(pygame.image.load(os.path.join(CAMINHO_IMAGENS, 'bird3.png')))]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 60)
FONTE_FIM = pygame.font.SysFont('arial', 20, bold=True)

class Passaro:
    IMAGENS = IMAGENS_PASSARO
    #Rotação do pássaro 
    ROTACAO_MAX = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5
    def __init__(self, eixo_x, eixo_y):

        self.eixo_x = eixo_x
        self.eixo_y = eixo_y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.eixo_y
        self.tempo = 0
        self.unidade_imagem = 0
        self.imagem = self.IMAGENS[0]

    def pular(self):
        #isso indica a velocidade do pulo 
        self.velocidade = -10
        self.tempo = 0
        self.altura = self.eixo_y

    def mover(self):
        #calculo deslocamento
        self.tempo += 1
        deslocamento = 1.5 * self.tempo**2 + self.velocidade * self.tempo
        #restrição do deslocamento
        if deslocamento > 12.5:
            deslocamento = 12.5
        elif deslocamento < 0:
            deslocamento -= 3

        self.eixo_y += deslocamento
        
        #Ângulo
        if deslocamento < 0 or self.eixo_y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAX:
                    self.angulo = self.ROTACAO_MAX
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO
    
    def desenhar(self, tela):
        self.unidade_imagem += 1
        #qual imageem do passaro
        if self.unidade_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMAGENS[0]
        elif self.unidade_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMAGENS[1]
        elif self.unidade_imagem < self.TEMPO_ANIMACAO *3:
            self.imagem = self.IMAGENS[2]
        elif self.unidade_imagem < self.TEMPO_ANIMACAO * 4: 
            self.imagem = self.IMAGENS[1]
        elif self.unidade_imagem <= self.TEMPO_ANIMACAO * 4 + 1: 
            self.imagem = self.IMAGENS[0]
            self.unidade_imagem = 0

        #queda
        if self.angulo <= -75: 
            self.imagem = self.IMAGENS[1]
            self.unidade_imagem = self.TEMPO_ANIMACAO * 2
        #"criação da imagem"
        roda_imagem = pygame.transform.rotate(self.imagem, self.angulo)
        centro_imagem = self.imagem.get_rect(topleft=(self.eixo_x, self.eixo_y)).center
        retangulo = roda_imagem.get_rect(center=centro_imagem) #desenha um retÂngulo em volta da imagem
        tela.blit(roda_imagem, retangulo.topleft) 

    def get_mask(self):
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        return pygame.mask.from_surface(imagem_rotacionada)#Hitbox mais adequada sendo a do pássaro e não um retângulo
        
class Cano:
    DISTANCIA = 225
    VELOCIDADE = 5

    def __init__(self, eixo_x):
        self.eixo_x = eixo_x
        self.altura = 0
        self.topo = 0
        self.base = 0
        self.CANO_BASE = IMAGEM_CANO
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True) # inverter apenas no eixo y
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(75, 485)
        self.topo = self.altura - self.CANO_TOPO.get_height()
        self.base = self.altura + self.DISTANCIA

    def mover(self):
        self.eixo_x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.eixo_x, self.topo))
        tela.blit(self.CANO_BASE, (self.eixo_x, self.base))
        
    def colisao(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.eixo_x - passaro.eixo_x, self.topo - round(passaro.eixo_y))
        distancia_base = (self.eixo_x - passaro.eixo_x, self.base - round(passaro.eixo_y))
        colisao_topo = passaro_mask.overlap(topo_mask, distancia_topo)
        colisao_base = passaro_mask.overlap(base_mask, distancia_base)

        if colisao_topo or colisao_base:
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA_CHAO = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, eixo_y):
        self.eixo_y = eixo_y
        self.chao1 = 0
        self.chao2 = self.LARGURA_CHAO

    def mover(self):
        self.chao1 -= self.VELOCIDADE
        self.chao2 -= self.VELOCIDADE

        if self.chao1 + self.LARGURA_CHAO < 0:
            self.chao1 = self.chao2 + self.LARGURA_CHAO
        if self.chao2 + self.LARGURA_CHAO < 0:
            self.chao2 = self.chao1 + self.LARGURA_CHAO            
        
    def desenhar(self,tela):
        tela.blit(self.IMAGEM, (self.chao1, self.eixo_y))
        tela.blit(self.IMAGEM, (self.chao2, self.eixo_y))

def desenhar_tela(tela, passaro, canos, chao, pontos):
    tela.blit(IMAGEM_FUNDO, (0,0))
    passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
    texto = FONTE_PONTOS.render(f'Pontuação: {pontos}', 1, (255,255,255))
    tela.blit(texto, (LARGURA_TELA - 10 - texto.get_width(), 10)) 
    chao.desenhar(tela)
    pygame.display.update()

def main():
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    passaro =  Passaro(230, 350)
    canos = [Cano(700)]
    chao = Chao(730)
    pontos = 0
    clock = pygame.time.Clock()
    
    fim_de_jogo = False
    while True:
        #ações do usuário
        clock.tick(45)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
                break
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    passaro.pular()
                    
        if not fim_de_jogo:
            passaro.mover()
            chao.mover()  
        criar_cano = False
        remover_canos = []
        fim = FONTE_FIM.render(f'Fim de jogo. Pontuação: {pontos}', 1, (255,255,255))
        posicao = fim.get_rect(center=(LARGURA_TELA//2, ALTURA_TELA//2))
        for cano in canos:
            if not fim_de_jogo:
                cano.mover()

            if cano.colisao(passaro):
                fim_de_jogo = True
            if not cano.passou and passaro.eixo_x > cano.eixo_x:
                cano.passou = True
                criar_cano = True
  
                if cano.eixo_x + cano.CANO_TOPO.get_width() < 0:
                    remover_canos.append(cano)
        if criar_cano:
            pontos += 1 
            canos.append(Cano(750))

        for cano in remover_canos:
            canos.remove(cano)

        if passaro.eixo_y + passaro.imagem.get_height() >= chao.eixo_y or passaro.eixo_y < 0:
            fim_de_jogo = True
            tela.blit(fim, posicao)
        if fim_de_jogo:
            tela.blit(fim, posicao)
            pygame.display.update()
            continue

        desenhar_tela(tela,passaro,canos,chao,pontos)

if __name__ == '__main__': 
    main()