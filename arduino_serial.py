import serial
import time
import ROOT
import numpy as np

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
#histo = ROOT.THD1("dist","title", 50, 0, 5
