import numpy as np
import uncertainties 
from uncertainties import ufloat
import string
from tokenize import String
from matplotlib.pyplot import plot
import serial
import time
import ROOT
import math



###MACRO PER FARE LE SOTTRAZIONI ED OTTENERE VHALL E VLONG.
# 
# PORCO DIO GLI ERRORI SONO STATISTICI DEVO FARLI A MANO 
# 
# QUINDI QUESTA MACRO NON SERVE AD UN CAZZO




with open("file con V hall e B+", 'r') as plus:
    num_lines = sum(1 for line in plus if line.rstrip())


with open("file con V hall e B-", 'r') as minus:
    num_lines = sum(1 for line in minus if line.rstrip())

v_long = open("vlong","a")
v_hall = open("vhall","a")

for l in range(0,num_lines):

    line_plus = (plus.readline()).split()
    line_plus_float = [ float(x) for x in line_plus]  #MAIUSCOLE PER LE COSE ASSOCIATE A B+
    V = line_plus_float [0] 
    B = line_plus_float[1]
    EV = line_plus_float[2]
    EB = line_plus_float[3]
    line_minus = (minus.readline()).split()
    line_minus_float = [ float(x) for x in line_minus]  #MMINUSCOLE PER LE COSE ASSOCIATE A B-
    v = line_minus_float [0] 
    b = line_minus_float[1]
    ev = line_minus_float[2]
    eb = line_minus_float[3]


    V_inc = ufloat(V, EV)
    B_inc = ufloat(B, EB)
    v_inc = ufloat(v, ev)
    b_inc = ufloat(b, eb)

    V_hall = (V-v)/2
    V_long = (V+v)/2
 
    vlong = V_long.n 
    evlong = V_long.s

    vhall = V_hall.n 
    evhall = V_hall.s

    v_long.write( vlong + " " + B + " " + evlong +  EB )
    v_hall.write( vhall + " " + B + " " + evhall +  EB )









