import string
from tokenize import String
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
mediaVarduino_suN = 0
mediaVhall_suN = 0
devStdVard_suN = 0
devStdVh_suN = 0
vArdArray = np.array([])
vHallArray = np.array([])


#COSTANTI

N = 1000    #numero di spire elettromagnete
mu = 1000
mu_0 = 4*math.pi*10**(-7)
l_t = ufloat( "METTI IL VALORE" , "METTI INCERTEZZA" )
l_m = ufloat( "METTI IL VALORE" , "METTI INCERTEZZA" )

#APERTURA FILE 

output = open("IvsVh", "a")
out_v_hall = open("Vhall.dat", "a")
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

		#CALCOLO CAMPO MAGNETICO NELL'ELETTROMAGNETE DALLA CORRENTE

		B_rough = (N*I)*mu/(l_m+(mu/mu_0)*l_t)    #restituisce una cosa del tipo B +- eB
		B = B_rough.n
		eB = B_rough.s/np.sqrt(3)    #statisticizzazione errore di B

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
			
			#CALCOLO LA MEDIA SULLA TENSIONE DI ARDUINO DI N VALORI MISURATI (SPERO)
		
			mediaVarduino_suN = np.mean(vArdArray)
			devStdVard_suN = np.std(vArdArray)
	if stato == 2:
		data = ser.readline().decode('utf-8').rstrip()
		print (data)

		if data == "CORRENTE":
			stato = 3

			#TENSIONE IN USCITA DA ARUDINO


			#TENISONE DI HALL

			"""
			print("Vh: " + str(mediaVhall_suN)+ "+/-" + str(devStdVh_suN))
			output.write(str(I) + " " + str(mediaVhall_suN) + " " + str(mediaVarduino_suN) + " " + str(devStdVard_suN) + " " + str(devStdVh_suN) + "\n")
			"""
			out_v_hall.write(mediaVhall_suN + "/n") #scrivo M vhall medio in un file per ogni I

			#PARTE DI ROOT

			"""
			h = "h{}".format(I) 
			c = "c{}".format(I)
			c = ROOT.TCanvas("c", "tensione di hall")
			h = ROOT.TH1D("isto", "up" , 20) 
			h.Fill(mediaVhall)
			c.Draw()
			h.Draw()
			name_isto = "istoV_hall{}.jpg".format(I)
			c.SaveAs(name_isto)
			V_hall_mean = h.GetMean() 
			V_hall_dev = h.GetStdDev()
			"""

		elif data == "BREAK":
			mediaVarduino = np.mean(vArdArray)
			devStdVard = np.std(vArdArray)
			print("Vard: " + str(mediaVarduino) + "+/-" + str(devStdVard))
			mediaVhall = np.mean(vHallArray)
			devStdVh = np.std(vHallArray)
			print("Vh: " + str(mediaVhall)+ "+/-" + str(devStdVh))
			output.write(str(I) + " " + str(mediaVhall) + " " + str(mediaVarduino) + " " + str(devStdVard) + " " + str(devStdVh) + "\n")
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


#CHIUSURA FILE

output.close()
out_v_hall.close()
vHall.close()
vArduino.close()



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
#histo = ROOT.THD1("dist","title", 50, 0, 5)
