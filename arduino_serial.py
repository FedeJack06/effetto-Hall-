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

mediaVarduino = 0
mediaVhall = 0
devStdVard = 0
devStdVh = 0
vArdArray = np.array([])
vHallArray = np.array([])

output = open("IvsVh", "a")
while True:
	#### INPUT DATI DA ARDUINO
	if stato == 0:
		data = ser.readline().decode('utf-8').rstrip()
		print (data)
	if data == "CORRENTE" or stato == 3:
		I = ser.readline().decode('utf-8').rstrip()
		print ("corr " + I)
		stato = 0
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
	if stato == 2:
		data = ser.readline().decode('utf-8').rstrip()
		print (data)
		if data == "CORRENTE":
			stato = 3
			mediaVarduino = np.mean(vArdArray)
			devStdVard = np.std(vArdArray)
			print("Vard: " + str(mediaVarduino) + "+/-" + str(devStdVard))
			mediaVhall = np.mean(vHallArray)
			devStdVh = np.std(vHallArray)
			print("Vh: " + str(mediaVhall)+ "+/-" + str(devStdVh))
			output.write(str(I) + " " + str(mediaVhall) + " " + str(mediaVarduino) + " " + str(devStdVard) + " " + str(devStdVh) + "\n")
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





bfile = open("B.dat","a")

i = [ ]
i.append(I) #da mettere nel ciclo che legge I
for l in i:
	mu = 1000
	mu_0 = 4*pi*10**(-7)
	l_t = ufloat( "METTI IL VALORE" , "METTI INCERTEZZA" )
	l_m = ufloat( "METTI IL VALORE" , "METTI INCERTEZZA" )
	B = (N*l)*mu/(l_m+(mu/mu_0)*l_t) #N,mu,mu_0,l_m,l_t sono tutti parametri del magente che ci troviamo

	w =  "{} + " " {} +  " " +/n".format(B.n,B.s)
	bfile.write(w)





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
