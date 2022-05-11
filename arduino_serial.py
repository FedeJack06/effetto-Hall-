import string
from tokenize import String
from matplotlib.pyplot import plot
import serial
import time
import ROOT
import numpy as np
import uncertainties
from uncertainties import ufloat
import math


#begin serial

ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(1)
ser.close()
time.sleep(1)
ser.open()
stato = 0
s =1

## PREOCESSING

I = 0

#MEDIA SU N MSIURE

mediaVarduino_suN = 0
mediaVhall_suN = 0
devStdVard_suN = 0
devStdVh_suN = 0
vArdArray = np.array([])
vHallArray = np.array([])

#MEDIA SU M MISURE DI N MISURE (PRENDIAMO I VALORI MEDI DI N MISURE E LI METTIAMO IN UN ISTOGRAMMA) SOLO PER V HALL

mediaVarduino_suM = 0
mediaVhall_suM = 0
devStdVard_suM = 0
devStdVh_suM = 0
vArdArray_M = np.array([])
vHallArray_M = np.array([])


#COSTANTI PER IL CALCOLO DI B

N = 1000    #numero di spire elettromagnete
mu = 1000
mu_0 = 4*math.pi*10**(-7)
l1 = ufloat(15e-2,1e-3)
l2 = ufloat(18e-2,1e-3)
l3 = ufloat(3e-2 , 1e-3)
l4 = ufloat(3e-2 , 1e-3)
l5 = ufloat(6e-2 , 1e-3)
l_t = ufloat(7e-2 , 5e-5)
l_m_calc = 3*l1 + 2*l2 - 5*l4 - l_t 
l_m_n = l_m_calc.n
l_m_s = l_m_calc.s
l_m = ufloat( l_m_n , l_m_s )

#APERTURA FILE 

output = open("Vhall", "a")   #file con i Vhall mediato (sono M valori)
plot_rough = open("plotV_HvsB_schifo.dat" , "a")   #schifo perche non c'è la correzione su B long e cose

#CICLO LETTURA E CALCOLI

while True:
	#### INPUT DATI DA ARDUINO
	if stato == 0:
		data = ser.readline().decode('utf-8').rstrip()
		print (data)
	if data == "CORRENTE" or stato == 3:
		I = ser.readline().decode('utf-8').rstrip()
		print ("corr " + I)
		stato = 0

		###CALCOLO CAMPO MAGNETICO NELL'ELETTROMAGNETE DALLA CORRENTE

		B_rough = (N*I)*mu/(l_m+(mu/mu_0)*l_t)    #restituisce una cosa del tipo B +- eB
		B = B_rough.n
		eB = B_rough.s/np.sqrt(3)    #calcolo e statisticizzazione errore di B

	vArduino = open("vArduino"+ str(I) +".dat", "a")
	vHall = open("vHall" + str(I) + ".dat", "a")
	if data == "VARD":
		stato = 1
	if stato == 1:
		data = ser.readline().decode('utf-8').rstrip() #12.6
		print (data)

		if data == "VHALL":
			stato = 2
		else:
			vArduino.write(data + "\n")
			vArduino.close()
			for word in data.split():
				vArdArray = np.append(vArdArray, float(word))
			
			###CALCOLO LA MEDIA SULLA TENSIONE DI ARDUINO DI N VALORI MISURATI (SPERO)
		
			mediaVarduino_suN = np.mean(vArdArray)  #ancora non so bene cosa farci
			devStdVard_suN = np.std(vArdArray)

			vArdArray_M = np.append(vArdArray_M, float(mediaVarduino_suN)) 

	if stato == 2:
		data = ser.readline().decode('utf-8').rstrip()
		print (data)

		if data == "CORRENTE":
			stato = 3

			#TENISONE DI HALL

			
			print("Vh: " + str(mediaVhall_suN)+ "+/-" + str(devStdVh_suN))
			output.write(str(mediaVhall_suN) + "\n")

			#PARTE DI ROOT

			h = "h{}".format(I) 
			c = "c{}".format(I)
			c = ROOT.TCanvas("c", "tensione di hall grezza")
			h = ROOT.TH1D("isto", "up" , 20) 
			c.Draw()
			h.Draw()
			name_isto = "istoV_hall{}.jpg".format(I)
			c.SaveAs(name_isto)
			V_hall_mean = h.GetMean() 
			V_hall_dev = h.GetStdDev()

			#SCRIVO I RISLUATI IN UN FILE DEL TIPO V_HALL B eV_HALL eB

			plot_rough.write(V_hall_mean + B + " " + V_hall_dev + " " + eB)

		elif data == "BREAK":
			mediaVarduino_suN = np.mean(vArdArray)
			devStdVard_suN = np.std(vArdArray)

			vArdArray_M = np.append(vArdArray_M, float(mediaVarduino_suN)) #inutili come l merda ma non sono sicro che lo siano quindi li lascio

			print("Vard: " + str(mediaVarduino_suN) + "+/-" + str(devStdVard_suN))
			mediaVhall_suN = np.mean(vHallArray)
			devStdVh_suN = np.std(vHallArray)

			vHallArray_M = np.append(vHallArray_M, float(mediaVhall_suN)) 

			h.Fill(mediaVhall_suN)

			print("Vh: " + str(mediaVhall_suN)+ "+/-" + str(devStdVh_suN))
			output.write(str(mediaVhall_suN) + "\n")
			ser.close()
			break
		elif data == "VARD":
			stato = 1
		else:
			vHall.write(data + "\n")
			vHall.close()
			for word in data.split():
				vHallArray = np.append(vHallArray, float(word))

			#CALCOLO LA MEDIA SU N VALORI MISURATI (SPERO)
				
			mediaVhall_suN = np.mean(vHallArray)
			devStdVh = np.std(vHallArray)

			vHallArray_M = np.append(vHallArray_M, float(mediaVhall_suN))   #inutili come l merda ma non sono sicro che lo siano quindi li lascio

			h.Fill(mediaVhall_suN)


		
			


#CHIUSURA FILE

output.close()
out_v_hall.close()
vHall.close()
vArduino.close()
plot_rough.close()




"""            
                 _   
 _ __ ___   ___ | |_ 
| '__/ _ \ / _ \| __|
| | | (_) | (_) | |_ 
|_|  \___/ \___/ \__|
      
"""


plot1 = open("plotV_HvsB_schifo.dat" , "r")
line = []

gr = 	ROOT.TGraphErrors
f = ROOT.TF1("f" ,"[0]+[1]*x + [2]*pow(x,2)")

#NUMERO DI RIGHE NEL FILE 

with open("plotV_HvsB_schifo.dat", 'r') as fp:
    num_lines = sum(1 for line in fp if line.rstrip())

#AGGIUNGO PUNTI AL GRAFICO

for l in range(0,num_lines):
	line = (plot1.readline()).split()
	line_float = [ float(x) for x in line]  
	hall = line_float [0] 
	b = line_float[1]
	ehall = line_float[2]
	eb = line_float[3]
	gr.SetPoint(l, b , hall)
	gr.SetPointError(l, eb , ehall)



#DISEGNO

gr.Draw("AP") 
gr.Fit("f")


'''
alla fine vogliamo trovarci un con un file del tipo:

V_hall B eV_hall eB
   .   .
   .   .
   .   .



un istogrammi con V_hall_+ - V_hall_- /2 cosi da avere V_hall e uno con V_hall_+ + V_hall_- /2 
cosi da avere V_long che dipenda da B^2

con B = (N*I)*mu/(l_m+(mu/mu_0)*l_t) , l'errore di b lo calcoliamo con la propagazione
degli errroi, V_hall viene furoi dall'istogramma e il suo errore lo calcoliamo con deviazione
standard


cosa ci facciamo dei valori di V_ard? li usiamo in quelche modo con i dati ricavati dalla
caratterizzazione del generatore di corrente.

'''







'''
stato = 0
while True:
	if ser.readline().decode('utf-8').rstrip() == "CORRENTE" and stato == 0: #corrente
		I = ser.readline().decode('utf-8').rstrip() #0.00
		vHall = open("vHall" + str(I) + ".dat", "a")
		stato = 1
	elif ser.readline().decode('utf-8').rstrip() == "VARD" and stato == 1:
		vArduino = open("vArduino"+ str(I) +".dat", "a")
		data = ser.readline().decode('utf-8').rstrip()
		vArduino.write(data + "\n")
		vArduino.close()
	if ser.readline().decode('utf-8').rstrip() == "CORRENTE"
'''
