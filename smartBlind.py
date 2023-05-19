import RPi.GPIO as GPIO
import time
import os

# GPIO pin numbers for ultrasonic sensor
TRIG_PIN = 17
ECHO_PIN = 27

# Threshold distance in centimeters
THRESHOLD_DISTANCE = 30

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    # Send ultrasonic pulse
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.0001)
    GPIO.output(TRIG_PIN, False)

    # Measure echo time
    start_time = time.time()
    end_time = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        end_time = time.time()

    # Calculate distance in centimeters
    duration = end_time - start_time
    distance = (duration * 34300) / 2

    return distance

def speak(message):
    os.system("espeak -ven-us+f3 -s150 '" + message + "'")

def main():
    try:
        while True:
            distance = get_distance()
            print("Distance: %.2f cm" % distance)

            if distance < THRESHOLD_DISTANCE:
                speak("Obstacle detected at %.2f centimeters!" % distance)
            else:
                speak("No obstacle detected.")

            time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
