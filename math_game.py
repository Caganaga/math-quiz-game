# -*- coding: utf-8 -*-
# pgzero

import random

WIDTH = 1920
HEIGHT = 1080
TITLE = "Matematik Oyunu"

start = Actor('start', (960, 540))
soru_ekrani = Actor('soru', (960, 540))
orta = Actor('orta', (960, 550))
zor = Actor('zor', (960, 450))
kolay = Actor('kolay', (960, 650))
dogru_isaret = Actor('dogru', (960, 540))
yanlis_isaret = Actor('yanlis', (960, 540))

secenek1 = Actor('secenek', (660, 700))
secenek2 = Actor('secenek', (1260, 700))
secenek3 = Actor('secenek', (660, 500))
secenek4 = Actor('secenek', (1260, 500))

oyun_durum = "ana_menu"
aktif_soru = None
aktif_cevap = ""
aktif_siklar = []
soru_sayaci = 0
maksimum_soru = 3

soru_suresi = 30  # saniye
kalan_sure = 0
aktif_zorluk = "kolay"

def rastgele_ustlu_soru(zorluk):
    if zorluk == "kolay":
        taban = random.randint(2, 4)
        us = random.randint(1, 2)
    elif zorluk == "orta":
        taban = random.randint(3, 5)
        us = random.randint(2, 3)
    elif zorluk == "zor":
        taban = random.randint(4, 7)
        us = random.randint(3, 4)
    else:
        taban = 2
        us = 2

    dogru = str(taban ** us)
    yanlislar = set()
    while len(yanlislar) < 3:
        yanlis = str(random.randint(taban**us - 10, taban**us + 10))
        if yanlis != dogru:
            yanlislar.add(yanlis)
    tum_siklar = list(yanlislar) + [dogru]
    random.shuffle(tum_siklar)
    soru_metni = f"{taban}^{us} kactir?"
    return (soru_metni, dogru, tum_siklar)

def draw():
    screen.clear()
    if oyun_durum == "ana_menu":
        start.draw()

    elif oyun_durum == "zorluk_sec":
        soru_ekrani.draw()
        kolay.draw()
        orta.draw()
        zor.draw()

    elif oyun_durum == "soru":
        soru_ekrani.draw()
        screen.draw.filled_rect(Rect((560, 150), (800, 100)), (240, 240, 240))
        screen.draw.text(aktif_soru[0], center=(960, 200), fontsize=60, color="black")
        screen.draw.text(f"Kalan Sure: {int(kalan_sure)}", topleft=(60, 60), fontsize=50, color="red")

        secenek1.draw()
        secenek2.draw()
        secenek3.draw()
        secenek4.draw()
        screen.draw.text(aktif_siklar[0], center=secenek1.pos, fontsize=40, color="black")
        screen.draw.text(aktif_siklar[1], center=secenek2.pos, fontsize=40, color="black")
        screen.draw.text(aktif_siklar[2], center=secenek3.pos, fontsize=40, color="black")
        screen.draw.text(aktif_siklar[3], center=secenek4.pos, fontsize=40, color="black")

    elif oyun_durum == "dogru":
        dogru_isaret.draw()

    elif oyun_durum == "yanlis":
        yanlis_isaret.draw()

def update(dt):
    global kalan_sure, oyun_durum
    if oyun_durum == "soru":
        kalan_sure -= dt
        if kalan_sure <= 0:
            oyun_durum = "yanlis"

def on_mouse_down(pos, button):
    global oyun_durum, aktif_soru, aktif_cevap, aktif_siklar, kalan_sure, soru_sayaci, aktif_zorluk

    if button == mouse.LEFT:
        if oyun_durum == "ana_menu" and start.collidepoint(pos):
            oyun_durum = "zorluk_sec"
            soru_sayaci = 0

        elif oyun_durum == "zorluk_sec":
            if kolay.collidepoint(pos):
                aktif_zorluk = "kolay"
            elif orta.collidepoint(pos):
                aktif_zorluk = "orta"
            elif zor.collidepoint(pos):
                aktif_zorluk = "zor"
            else:
                return
            aktif_soru = rastgele_ustlu_soru(aktif_zorluk)
            aktif_cevap = aktif_soru[1]
            aktif_siklar = aktif_soru[2]
            kalan_sure = soru_suresi
            oyun_durum = "soru"
            soru_sayaci = 1

        elif oyun_durum == "soru":
            dogru_bilindi = False
            if secenek1.collidepoint(pos) and aktif_siklar[0] == aktif_cevap:
                dogru_bilindi = True
            elif secenek2.collidepoint(pos) and aktif_siklar[1] == aktif_cevap:
                dogru_bilindi = True
            elif secenek3.collidepoint(pos) and aktif_siklar[2] == aktif_cevap:
                dogru_bilindi = True
            elif secenek4.collidepoint(pos) and aktif_siklar[3] == aktif_cevap:
                dogru_bilindi = True

            if dogru_bilindi:
                if soru_sayaci < maksimum_soru:
                    soru_sayaci += 1
                    aktif_soru = rastgele_ustlu_soru(aktif_zorluk)
                    aktif_cevap = aktif_soru[1]
                    aktif_siklar = aktif_soru[2]
                    kalan_sure = soru_suresi
                else:
                    oyun_durum = "dogru"
            else:
                oyun_durum = "yanlis"

        elif oyun_durum == "dogru" or oyun_durum == "yanlis":
            oyun_durum = "ana_menu"
