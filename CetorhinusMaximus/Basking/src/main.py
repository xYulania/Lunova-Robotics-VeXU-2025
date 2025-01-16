# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       Basking Main Code                                            #
# 	Author:       Yulania                                                      #
# 	Created:      1/4/2025, 6:19:05 PM                                         #
# 	Description:  Default code for Basking VeXU Robot - Python                 #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

brain = Brain()
controller = Controller()
intake = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
intake.set_velocity(200, RPM)
frontIntake = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)
frontIntake.set_velocity(200, RPM)

allIntakes = MotorGroup(intake, frontIntake)

frontRightMotor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
backRightMotor = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)

TopRightMotor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)

frontLeftMotor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, True)
backLeftMotor = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)

TopLeftMotor = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)

rightGears = MotorGroup(frontRightMotor, backRightMotor, TopRightMotor)
leftGears = MotorGroup(frontLeftMotor, backLeftMotor, TopLeftMotor)

allGears = MotorGroup(frontRightMotor, backRightMotor, TopRightMotor, frontLeftMotor, backLeftMotor, TopLeftMotor)

digOut = DigitalOut(brain.three_wire_port.a)
digOut.set(True)


def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    while True:
        wait(20, MSEC)


def userControl():
    brain.screen.clear_screen()
    brain.screen.print("driver control")

    digOutState = True  # Track the state of digOut (open or closed)
    buttonAState = False  # Track the previous state of buttonA (pressed or not)

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

        # Handle buttonA press for toggling digOut
        if controller.buttonA.pressing() and not buttonAState:  # Detect a new press
            digOutState = not digOutState  # Toggle the pneumatic state
            digOut.set(digOutState)  # Apply the toggle to the pneumatic system
            if digOutState:
                brain.screen.set_cursor(3, 1)
                brain.screen.print("Pneumatic Opened")
            else:
                brain.screen.set_cursor(3, 1)
                brain.screen.print("Pneumatic Closed")
            buttonAState = True  # Mark the button as pressed

        if not controller.buttonA.pressing():
            buttonAState = False  # Reset the button state when released


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
