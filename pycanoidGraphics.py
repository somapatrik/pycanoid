#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import time
import math
import random
#import pickle
import yaml
import os


class GameGraphics:
    def __init__(self,game,velikost_okna = (1024, 768)):
        
        self.game = game
        self.velikost_okna = velikost_okna
        # BARVY
        self.bila = 250, 250, 250
        self.cerna = 0, 0, 0
        self.zelena = 0, 250, 0
        self.modra = 0, 0, 250

        # Rozměry
        self.odsazeni = int(self.velikost_okna[0] / 6.8)
        self.odsazeni_dole = int(self.velikost_okna[1] / 13.6)
        self.herni_velikost = (self.velikost_okna[0] - (self.odsazeni * 2), self.velikost_okna[1] - self.odsazeni_dole) # velikost plochy kde létá kulička 

        # Výpočty okrajů pro hraní
        self.horni_levy = ((self.velikost_okna[0] - self.herni_velikost[0]) / 2, 0)
        self.horni_pravy = (self.horni_levy[0] + self.herni_velikost[0], self.horni_levy[1])
        self.spodni_levy = (self.horni_levy[0], self.herni_velikost[1])
        self.spodni_pravy = (self.horni_pravy[0], self.herni_velikost[1])
        # Mys
        pygame.mouse.set_visible(0)

        # Pismo
        self.pismo = pygame.font.Font('freesansbold.ttf', 20)

        # Inicializace okna
        self.obrazovka = pygame.display.set_mode(self.velikost_okna)
        pygame.display.set_caption('Pycanoid')

        # Surface pro kreslení všeho vzadu
        self.pozadi = pygame.Surface(self.velikost_okna)
        self.pozadi.fill(self.cerna)

        # Surface pro desku
        self.deska_surface = pygame.Surface(self.game.paddle1.size)
        self.deska_surface.fill(self.zelena)
        self.deska_surface = pygame.image.load("grafika/paddledown.png")#HOLI
        
       # Surface pro kuličku
        self.ball_surface = pygame.Surface(self.game.ball.size)

        #ball_surface.fill(bila)
        self.ball_surface = pygame.image.load("grafika/ball.png")#HOLI

        # Výpočty okrajů pro hraní
        self.horni_levy = ((self.velikost_okna[0] - self.herni_velikost[0]) / 2, 0)
        self.horni_pravy = (self.horni_levy[0] + self.herni_velikost[0], self.horni_levy[1])
        self.spodni_levy = (self.horni_levy[0], self.herni_velikost[1])
        self.spodni_pravy = (self.horni_pravy[0], self.herni_velikost[1])

        # Surface pro herni oblast HOLI
        self.oblast_surface = pygame.Surface((self.horni_pravy[0]-self.horni_levy[0]-1,self.spodni_levy[1]- self.horni_levy[1]-1))
        self.oblast_surface = pygame.image.load("grafika/test.jpg")

        # Surface pro vypis HOLI
        self.vypis_surfaceBall = pygame.Surface((300,200))
        self.vypis_surfaceBall.fill(self.cerna)
        self.vypis_surfaceDeska1 = pygame.Surface((200,200))
        self.vypis_surfaceDeska1.fill(self.cerna)

        self.prava = self.horni_pravy[0]  # X souřadnice pro pravou herní plochu
        self.leva = self.horni_levy[0]    # X souřadnice pro levou herní plochu
        self.nahore = self.horni_levy[1]  # Y souřadnice pro horní stranu
        self.dole = self.spodni_levy[1]   # Y souřadnice spodního kraje

        # Vykreslení okrajů
        pygame.draw.line(self.pozadi, self.bila, self.horni_levy, self.horni_pravy)
        pygame.draw.line(self.pozadi, self.bila, self.spodni_levy, self.spodni_pravy)
        pygame.draw.line(self.pozadi, self.bila, self.horni_levy, self.spodni_levy)
        pygame.draw.line(self.pozadi, self.bila, self.horni_pravy, self.spodni_pravy)

    
    def CreateBackground(self):
        """
    Tvoří základní pozadí, vše co je vidět
        """
        self.obrazovka.blit(self.pozadi, (0, 0))
        #HOLI
        self.obrazovka.blit(self.oblast_surface, (self.horni_levy[0]+1, self.horni_levy[1]+1))
        self.obrazovka.blit(self.vypis_surfaceBall, (10, self.dole+10))
        self.obrazovka.blit(self.vypis_surfaceDeska1, (400, self.dole+10))

    def DrawBallBegin(self):
        """
    Vykresluje kuličku na začátku hry
        """
        self.game.ball.x = (self.game.paddle1.x + self.game.paddle1.size[0] / 2) - (self.game.ball.size[0] / 2)
        self.game.ball.y = self.game.paddle1.y - self.game.ball.size[1]
        self.obrazovka.blit(self.ball_surface, (self.game.ball.x, self.game.ball.y))

    def DrawDesk(self,position, ddeska, ndeska = 0):
        """
    Kontrola spravneho umisteni odrazeci desky
    :param position:
        deska: objekt desky
        ndeska: 0 - dole, 1 - nahore
    """
        if ndeska == 0:
            deskay = self.herni_velikost[1] - ddeska.size[1]-50
        else:
            deskay = 50 # herni_velikost[1] - ddeska.size[1] - 30

        # podminka pro herni oblast
        if (position[0] - ddeska.size[0] / 2 >= self.spodni_levy[0]) and (position[0] + ddeska.size[0] / 2 <= self.spodni_pravy[0]):
            ddeska.x = position[0] - ddeska.size[0] / 2
            ddeska.y = deskay
            self.obrazovka.blit(self.deska_surface, (ddeska.x, ddeska.y))

        # oblast nalevo od herni plochy
        elif position[0] - ddeska.size[0] / 2 <= self.spodni_levy[0]:
            ddeska.x = self.spodni_levy[0]
            ddeska.y = deskay
            self.obrazovka.blit(self.deska_surface, (ddeska.x, ddeska.y))

        # oblast napravo od herni plochy
        elif position[0] - ddeska.size[0] / 2 >= self.spodni_levy[0]:
            ddeska.x = self.spodni_pravy[0] - ddeska.size[0]
            ddeska.y = deskay
            self.obrazovka.blit(self.deska_surface, (ddeska.x, ddeska.y))

    def DrawInformations(self,game):
        """
    Vykresluje ladící výpisy přímo do hry
        """
        text = "ball| x:" + str(round(game.ball.x)) + "| y:" + str(round(game.ball.y))
        self.vypis_surfaceBall = self.pismo.render(text,  1, self.modra, self.cerna)
        textDeska1 = "deska1 dolni|  x:" + str(round(game.paddle1.x))
        self.vypis_surfaceDeska1 = self.pismo.render(textDeska1,  1,self.modra, self.cerna)
        
