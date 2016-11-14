//initiated by python1.py , this is where all sensors will run and communicate with python2.py 
import sys
import time 
import RPi.GPIO as GPIO
import os
from time import sleep
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO_TRIGGER_1 = 35
GPIO_ECHO_1    = 37

GPIO_TRIGGER_2 = 36
GPIO_ECHO_2    = 38

print "Ultrasonic Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER_1,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO_1,GPIO.IN)      # Echo
# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER_1, False)

GPIO.setup(GPIO_TRIGGER_2, GPIO.OUT)
GPIO.setup(GPIO_ECHO_2, GPIO.IN)
# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER_2, False)

j1=0   #this j=0 is to initialise smoothValue for lowPassFilter 
j2=0

safetyValue = 100 #Distance must not be lesser than 100cm 

ultrasonicFormat = [0,1,2,3,4,5]
#LEFT,RIGHT,FRONT, BACK, NONE
#data = sys.stdin.readline()

ultrasonicFormat[0] = "\n"
ultrasonicFormat[1] = "L"
ultrasonicFormat[2] = "R"
ultrasonicFormat[3] = "F"
ultrasonicFormat[4] = "B"

# Allow module to settle
time.sleep(0.5)

def distanceMeasureOne(): 
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER_1, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_1, False)
    start = time.time()
    
    while GPIO.input(GPIO_ECHO_1)==0:
      start = time.time()
    
    while GPIO.input(GPIO_ECHO_1)==1:
      stop = time.time()
    
    # Calculate pulse length
    elapsed = stop-start
    
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distanceTemp = elapsed * 34300
    
    
    # That was the distance there and back so halve the value
    distanceTemp = distanceTemp / 2
    
    global distance
    
    if (distanceTemp < 400 and distanceTemp > 2):
		distance = distanceTemp 
    
    print "Distance for Ultrasonic Sensor 1 : %.1f" % distance
    
    time.sleep (0.06)
    return distance
    
def distanceMeasureTwo(): 
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER_2, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_2, False)
    start = time.time()
    
    while GPIO.input(GPIO_ECHO_2)==0:
      start = time.time()
    
    while GPIO.input(GPIO_ECHO_2)==1:
      stop = time.time()
    
    # Calculate pulse length
    elapsed = stop-start
    
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distanceTemp = elapsed * 34300
    
    
    # That was the distance there and back so halve the value
    distanceTemp = distanceTemp / 2
    
    global distance
    
    if (distanceTemp < 400 and distanceTemp > 2):
		distance = distanceTemp 
    
    print "Distance for Ultrasonic Sensor 2 : %.1f" % distance
    
    time.sleep (0.06)
    return distance 
    
    
def filterDistance (whichSensor, sensorDistance):
	global smoothedValue_1
	global smoothedValue_2
	filterValue = 0.5
	if (whichSensor == 1):
		if (j1==0):
			global j1
			smoothedValue_1 = sensorDistance
			j1 +=1
		smoothedValue_1 = (sensorDistance * (1 - filterValue)) + (smoothedValue_1 * filterValue)	
		return smoothedValue_1
		
	elif (whichSensor == 2):
		if (j2==0):
			global j2
			smoothedValue_2 = sensorDistance
			j2 +=1
		smoothedValue_2 = (sensorDistance*(1-filterValue))+(smoothedValue_2*filterValue)
		return smoothedValue_2
			   
    
def dataLogging(whichSensor, distance, filteredDistance):
	if (whichSensor == 1):
		file = open("/home/pi/dataLogging/sensorData_1.csv", "a")
		if os.stat("/home/pi/dataLogging/sensorData_1.csv").st_size == 0:
			file.write("Time,ultrasonicSensor1, filteredDistance\n")
	elif (whichSensor == 2):
		file = open("/home/pi/dataLogging/sensorData_2.csv", "a")
		if os.stat("/home/pi/dataLogging/sensorData_2.csv").st_size == 0:
			file.write("Time,ultrasonicSensor2, filteredDistance\n")
	now = datetime.now()
	file.write(str(now)+","+str(distance)+","+str(filteredDistance)+"\n")
	file.flush()
	#<br>file.close() 


while True: 
    #left ultrasonic sensor    
    sensorDistance = distanceMeasureOne()
    filteredDistance = filterDistance(1,sensorDistance)
    if (filteredDistance , safetyValue):
		obstacleStatus = ultrasonicFormat[1]
	else:
		obstacleStatus = ''
    dataLogging(1,sensorDistance, filteredDistance)

	#right ultrasonic sensor 
    sensorDistance = distanceMeasureTwo()
    filteredDistance = filterDistance (2,sensorDistance)
    if (filteredDistance , safetyValue):
		obstacleStatus = ultrasonicFormat[2]
	else:
		obstacleStatus = ''
    dataLogging(2,sensorDistance, filteredDistance)
    
    #front ultrasonic sensor 
    
    
    #back ultrasonic sensor 

	
	#final preparation before sending the data
	obstacleStatus = obstacleStatus + '\n'   #requires \n as a protocol 
	
	if (obstacleStatus == '\n'):
		obstacleStatus = 'NONE\n'
	
	sys.stdout.write(obstacleStatus)
	sys.stdout.flush()
	
	obstacleStatus = ''   #restarts again 




"""
sys.stdout.write("R\n")
sys.stdout.flush()

time.sleep(1)


sys.stdout.write("F\n")
sys.stdout.flush()

time.sleep(1)

sys.stdout.write("B\n")
sys.stdout.flush()

time.sleep(1)

sys.stdout.write("LR\n")
sys.stdout.flush()

time.sleep(1)

sys.stdout.write("LF\n")
sys.stdout.flush()

time.sleep(1)

sys.stdout.write("LB\n")
sys.stdout.flush()

time.sleep(1)

sys.stdout.write("RF\n")
sys.stdout.flush()

time.sleep(1)

sys.stdout.write("RB\n")
sys.stdout.flush()

time.sleep(1)

sys.stdout.write("FB\n")
sys.stdout.flush()

time.sleep(1)

sys.stdout.write("LRF\n")
sys.stdout.flush()

time.sleep(1)

sys.stdout.write("LRFB\n")
sys.stdout.flush()

time.sleep(1)



"""
