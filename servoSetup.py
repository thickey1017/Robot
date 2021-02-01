from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Set frequency to 50hz, good for servos.
# TPH - Originally was 60hz. Datasheet indicates 50hz.
pwm.set_pwm_freq(50)

# setInitial - sets robot to starting position
def setInitial(currentLoc):
    print('Setting initial position...')
    i=0
    for i in range(len(currentLoc)):
        pwm.set_pwm(i, 0, currentLoc[i]) #sets servo 5 to align with x_0-axis
    time.sleep(1)
    print('   ... set initial position. \n')

# testIndividualMotor - allows you to specify motor and test it to min and max
def testIndividualMotor(currentLoc,minLoc,maxLoc):
    print('Running testIndividualMotor... \n')
    print(currentLoc)
    print('\nSelect one motor, start at min, increment up with w and down with s')
    servNum=input('Pick motor to test: ')
    servPos=currentLoc[servNum]
    #print('Setting to min')
    time.sleep(2)
    flag=True
    #pwm.set_pwm(servNum, 0, servPos)
    while flag:
        servInc=raw_input('UP (w), DOWN (s), MIN (n), MAX (x), CHANGE SERVO (c), QUIT (q): ')
        if servInc=='c':
            servNum=input('Choose servo to increment: ')
            servPos=currentLoc[servNum]
        elif servInc=='q':
            flag=False
        elif servInc=='w':
            servPos=servPos+10
            currentLoc[servNum]=servPos
        elif servInc=='s':
            servPos=servPos-10
            currentLoc[servNum]=servPos
        elif servInc=='n':
            servPos=servo_min
            currentLoc[servNum]=servPos
        elif servInc=='x':
            servPos=servo_max
            currentLoc[servNum]=servPos
        if (servInc<>'c') and (servInc<>'q'):
            if servPos > maxLoc[servNum]:
                servPos=maxLoc[servNum]
                currentLoc[servNum]=servPos
                print('Already at max position')
            elif servPos < minLoc[servNum]:
                servPos=minLoc[servNum]
                currentLoc[servNum]=servPos
                print('Already at min position')
            print('Servo: ',servNum,'. Position: ',servPos,'.')
            pwm.set_pwm(servNum, 0, servPos)
    print('\n\n   ...testIndividualMotor complete.\n')
    return currentLoc

# testAllMotorsRange - sets robot to initial position and then puts each motor to min and max positions
def testAllMotorsRange(currentLoc,minLoc,maxLoc):
    print('Running testAllMotorsRange...')
    setInitial(currentLoc)
    print('Moves all motors from min to max')
    servNum=0
    for servNum in range(len(minLoc)):
        print('...max cycle ',servNum)
        pwm.set_pwm(servNum, 0, maxLoc[servNum]) 
        time.sleep(2)
        print('...min cycle ',servNum)
        pwm.set_pwm(servNum, 0, minLoc[servNum])
        time.sleep(2)
    setInitial(currentLoc)
    print('   ...test all motors complete.\n')

# incrementToLocation - accepts current location list and desired location list; moves robot to location
def incrementToLocation(currentLoc,desiredLoc,minLoc,maxLoc):
    checkFlag = True
    check = [1, 1, 1, 1, 1]
    while checkFlag:
        i=0
        checkSum=0
        for i in range(len(currentLoc)):
            delta=int(currentLoc[i]-desiredLoc[i])
            if (delta == 0):
                check[i]=0
            elif (delta > 0):
                currentLoc[i] = currentLoc[i]-10
                pwm.set_pwm(i, 0, currentLoc[i])
            else:
                currentLoc[i] = currentLoc[i]+10
                pwm.set_pwm(i, 0, currentLoc[i])
        j=0
        for j in range(len(currentLoc)):
            checkSum = checkSum + check[j]
        if checkSum == 0:
            checkFlag = False
        time.sleep(.05)
    currentLoc=desiredLoc
    return currentLoc


#pinchManeuver - does the pinch motion and spins the arm
def pinchManeuver(currentLoc,minLoc,maxLoc):
    print('Performing pinch maneuver...')
    for i in range(10):
	if i % 2 == 0:
            pwm.set_pwm(0,0,minLoc[0])
            pwm.set_pwm(1,0,minLoc[1])
        else:
            pwm.set_pwm(0,0,maxLoc[0])
            pwm.set_pwm(1,0,maxLoc[1])
        time.sleep(.5)
    pwm.set_pwm(0,0,minLoc[0])
    pwm.set_pwm(1,0,minLoc[1])
    currentLoc[0]=minLoc[0]
    currentLoc[1]=minLoc[0]
    print('   ...pinch maneuver complete.')
    return currentLoc


#fullDance - do the dang thing
def fullDance(currentLoc,minLoc,maxLoc):
    print('Performing full dance...')
    sittingLoc = [maxLoc[0], maxLoc[1], maxLoc[2], maxLoc[3], minLoc[4]] #SITTING POSITION
    currentLoc = incrementToLocation(currentLoc, sittingLoc, minLoc, maxLoc)
    time.sleep(1)
    desiredLoc = [minLoc[0], minLoc[1], 230, minLoc[3], maxLoc[4]] #ERECT POSITION
    currentLoc = incrementToLocation(currentLoc, desiredLoc, minLoc, maxLoc)
    currentLoc = pinchManeuver(currentLoc,minLoc,maxLoc)
    sittingLoc = [maxLoc[0], maxLoc[1], maxLoc[2], maxLoc[3], minLoc[4]] #SITTING POSITION
    currentLoc = incrementToLocation(currentLoc, sittingLoc, minLoc, maxLoc)
    print(' ...full dance complete.')
    return(currentLoc)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#        Begin Routine           #

print('Begin...\n')


minLoc = [240, 150, 150, 150, 270]
maxLoc = [370, 450, 450, 390, 450]
currentLoc = [240, 150, 330, 300, 290]

setInitial(currentLoc)
time.sleep(.5)

print('Choose test type...')
testType=input('(1) Test individual motor\n(2) Test all motors\n(3) Pinch maneuver\n(4) Full dance\n...')
print('\n')

if testType == 1:
    currentLoc = testIndividualMotor(currentLoc,minLoc,maxLoc)
elif testType == 2:
    currentLoc = testAllMotorsRange(currentLoc,minLoc,maxLoc)
elif testType == 3:
    currentLoc = pinchManeuver(currentLoc,minLoc,maxLoc)
elif testType == 4:
    currentLoc = fullDance(currentLoc,minLoc,maxLoc)

time.sleep(1)
#desiredLoc = [150, 150, 450, 150, 410, 300] #point to 'button'
#currentLoc = incrementToLocation(currentLoc,desiredLoc)
print('Final positions: ',currentLoc,'\n')
print('\n\nComplete...')
