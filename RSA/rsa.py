#!/usr/bin/env python
#coding: UTF-8

import argparse
import sys

import bigNumber.bigNumber as bigNumber
import primes


def GCDEx(a, b):        
    if b == 0:
        return a, 1, 0
    if a == 0:
        return b, 1, 0
    
    x1 = bigNumber.bigNumber(0)
    x2 = bigNumber.bigNumber(1)
    y1 = bigNumber.bigNumber(1)
    y2 = bigNumber.bigNumber(0)
    
    while b != 0:
        q = a / b
        r = a % b
        a = b
        b = r
        
        xx = x2 - x1 * q
        yy = y2 - y1 * q
        x2 = x1
        x1 = xx
        y2 = y1
        y1 = yy
    x = x2
    y = y2

    return a, x, y

    
def LinCon (a, b, m):
    """Решение линейного сравнение ax = b mod m
    """
    d, t1, t2 = GCDEx(a, m)    
    if b % d != 0:
        return False, 0
    
    if (a == 0 and b % m == 0) or (b == 0 and a % m == 0):
        return True, -1
    
    # находим одно из решений, используя расширенный алгоритм Евклида
    a1 = a / d
    b1 = b / d
    m1 = m / d
    d1, x, y = GCDEx(a1, m1)    
    res0 = ( b1 * x ) % m
    while res0 < 0:
        res0 += m

    # теперь находим оставшиеся d-1 решения
    resAll = []
    resAll.append(res0)
    d = d - 1
    while d > 0:
        resAll.append( (resAll[-1] + m1) % m )
        if resAll[-1] < 0:
            resAll[-1] += m
        d -= 1
    
    return True, resAll

def decrypt(d, n, c):
    m = bigNumber.Pow(c, d, n)
    return m


def encrypt(e, n, m):
    if m >= n:
        raise ValueError('Message is too large!')
    
    c = bigNumber.Pow(m, e, n)
    return c

if __name__ == "__main__":
    
    #генерирование простых чисел p и q, с заданной длиной, причем p!=q
    p = primes.GeneratePrime(32)
    q = primes.GeneratePrime(32)
    while p == q:
        q = primes.GeneratePrime(32)
    
    #расчет n
    n = p * q
    #расчет функции эйлера
    Fi = (p-1) * (q-1)
    #выбор экспоненты
    e = bigNumber.bigNumber(65537)
    
    #расчет секретной экспоненты d
    Bool, d = LinCon(e, bigNumber.bigNumber(1), Fi)
    if not Bool or d == -1:
        raise ValueError('Something went worng...')
    d = d[0]
    
    #получение сообщения и перевод его в большое число
    File = open("m.txt","r") #открываем файл на чтение
    m = int(File.read())#считываем файл целиком
    File.close()
    m = bigNumber.bigNumber(m)
    
    #шифрование исходного сообщения и запись его в файл
    c=encrypt(e,n,m)
    File1 = open("c.txt","w")
    EncryptedText=str(c)    
    File1.write(EncryptedText)	
    File1.close()
    
    #дешифрование и запись его в файл
    k=decrypt(d,n,c)
    File2 = open("DecryptTxt","w")
    DecryptText=str(k)
    File2.write(DecryptText)
    File2.close()
    


    
