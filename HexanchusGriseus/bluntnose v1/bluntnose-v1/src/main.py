from vex import *

brain = Brain()
controller = Controller()

intake = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
intake.set_velocity(200, RPM)

frontIntake = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
frontIntake.set_velocity(200, RPM)

allIntakes = MotorGroup(intake, frontIntake)

frontRightMotor = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
backRightMotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)

frontLeftMotor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
backLeftMotor = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)

rightGears = MotorGroup(frontRightMotor, backRightMotor)
leftGears = MotorGroup(frontLeftMotor, backLeftMotor)

allGears = MotorGroup(frontRightMotor, backRightMotor, frontLeftMotor, backLeftMotor)

digOutFront = DigitalOut(brain.three_wire_port.h)
digOutFront.set(False)

# def preAutonomous():

#     wait(20, MSEC)

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")

    wait(20, MSEC)


def userControl():

    brain.screen.clear_screen()
    brain.screen.print("driver control")

    digOutState = True  # Track the state of digOut (open or closed)
    buttonUpState = False  # Track the previous state of buttonUp (pressed or not)    
    digOutFrontState = False
    buttonDownState = False

    while True:

        maxRPM = 200
        ForwardBackwardJS = (controller.axis3.position() / 100) * maxRPM
        turningJS = (controller.axis1.position() / 100) * maxRPM

        rightJSspeed = ForwardBackwardJS + turningJS
        leftJSspeed = ForwardBackwardJS - turningJS

        rightGears.spin(FORWARD, leftJSspeed, RPM)
        leftGears.spin(FORWARD, rightJSspeed, RPM)

        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("Left Speed: {:.2f} RPM".format(leftGears.velocity(RPM)))
        brain.screen.set_cursor(2, 1)
        brain.screen.print("Right Speed: {:.2f} RPM".format(rightGears.velocity(RPM)))


        if controller.buttonDown.pressing() and not buttonDownState:
            digOutFrontState = not digOutFrontState
            digOutFront.set(digOutFrontState)
            if digOutFrontState:
                brain.screen.set_cursor(4, 1)
                brain.screen.print("Pneumatic Opened")
            else:
                brain.screen.set_cursor(4, 1)
                brain.screen.print("Pneumatic Closed")
            buttonDownState = True
        
        if not controller.buttonDown.pressing():
            buttonDownState = False

        maxIntakeAllRPM = 200
        intakeInOutAll = (controller.buttonL1.pressing() - controller.buttonR1.pressing()) * maxIntakeAllRPM 
        intakeInOut = (controller.buttonL2.pressing() - controller.buttonR2.pressing()) * maxIntakeAllRPM
        if intakeInOutAll != 0:
            allIntakes.spin(FORWARD, intakeInOutAll, RPM)
        else:
            allIntakes.spin(FORWARD, 0, RPM)
            intake.spin(FORWARD, intakeInOut, RPM)

        wait(20, MSEC)


# Create competition instance
comp = Competition(userControl, autonomous)

# Actions to do when the program starts
brain.screen.clear_screen()



                                                            ######### ARCHIVE #########


# rightGears = MotorGroup(frontRightMotor, backRightMotor, TopRightMotor)
# leftGears = MotorGroup(frontLeftMotor, backLeftMotor, TopLeftMotor)

# TopRightMotor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
# TopLeftMotor = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)

# allGears = MotorGroup(frontRightMotor, backRightMotor, TopRightMotor, frontLeftMotor, backLeftMotor, TopLeftMotor)
