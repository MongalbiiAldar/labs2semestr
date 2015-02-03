#!/usr/bin/env python
#coding: UTF-8
import argparse
import sys

import bigNumber.bigNumber as bigNumber

def Generation_keys():
    p = bigNumber.bigNumber(48731)#выбирается p
    q = bigNumber.bigNumber(443)#выбирается q
    g = bigNumber.bigNumber(11444)#выбирается g
    
    w = bigNumber.GenerateRandomMax(q)#выбирается случайное число w меньшее q
    y = bigNumber.Pow(g, q - w, p)#вычисляется y
    
    return p, q, g, y, w
def TheFirstTask(p, q, g):
    r = bigNumber.GenerateRandomMax(q)
    x = bigNumber.Pow(g, r, p)
    return r,x
def get_args():
    parser = argparse.ArgumentParser(
        prog="python schnorr.py") 
    parser.add_argument('pubkey')
    parser.add_argument('privkey')
    
   
    return parser.parse_args()	
if __name__ == "__main__":
    args = get_args()
    #Генерация ключей
    p, q, g, y, w = Generation_keys()# (p,q,g,y)-открытый ключ (w)-закрытый ключ
    
    #запись открытых ключей в файл
    f = open (args.pubkey,"w")
    PubKey = "\n".join(map(str, (p, q, g, y)))
    f.write(PubKey)    
    
    #запись закрытого ключа в файл
    f = open (args.privkey,"w")
    PrivKey=str(w)
    f.write(PrivKey)
    # Алгоритм протокола. Предварительная обработка
    # Алиса выбирает случайное число r, меньшее q, и вычисляет x = g^r mod p.    	
    r, x = TheFirstTask(p,q,g)
    
    # Инициирование. Алиса посылает x Бобу.
    # Боб выбирает случайное число e из диапазона от 0 до 2^t-1 и отправляет его Алисе.
    #tmp=2^t-1
    tmp = bigNumber.GenerateRandomLen(72)
    e = bigNumber.GenerateRandomMax(tmp)
    
    # Алиса вычисляет s=r+we mod q и посылает s Бобу.
    s = (r + w * e) % q

    # Подтверждение. Боб проверяет что x=g^s * y^e mod p
    AlisaX = (bigNumber.Pow(g, s, p) * bigNumber.Pow(y, e, p)) % p

    if x == AlisaX:
        print "Success"
    else:
        print "Unsuccess"

