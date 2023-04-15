import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

pwm_min_fw = 307
pwm_max_fw = 217
pwm_stop = 318
pwm_min_rev = 329
pwm_max_rev = 419

right_channel = 8
left_channel = 9

# return pwm setting for forward speeds 0 - 100
def getPwmFwSpeed(s=0):
	x = int(s)
	if (x > 99):
		return pwm_max_fw
	elif (x < 1):
		return pwm_stop
	else:
		return pwm_min_fw - round((x * 90)/100)

# return pwm setting for reverse speeds 0 - 100
def getPwmRevSpeed(s=0):
	x = int(s)
	if (x > 99):
        	return pwm_max_rev
	elif (x < 1):
		return pwm_stop
	else:
		return pwm_min_rev + round((x * 90)/100)

def rightTrack(speed=0):
	if (speed < 0):
		pwm.set_pwm(right_channel, 0, getPwmRevSpeed(-speed))
	else:
		pwm.set_pwm(right_channel, 0, getPwmFwSpeed(speed))

def leftTrack(speed=0, reverse=False):
        if (speed < 0):
                pwm.set_pwm(left_channel, 0, getPwmFwSpeed(-speed))
        else:
                pwm.set_pwm(left_channel, 0, getPwmRevSpeed(speed))

if __name__ == '__main__':
	import argparse
	argParser = argparse.ArgumentParser()
	argParser.add_argument("-s", "--speed", help="speed 0-100")
	argParser.add_argument("-r", "--reverse", required=False, action="store_const", const = True, help="reverse direction") 
	args = argParser.parse_args()
	channel = 0	# servo port number.
	if (args.reverse):
		pwm.set_pwm(channel, 0, getPwmRevSpeed(args.speed))
	else:
		pwm.set_pwm(channel, 0, getPwmFwSpeed(args.speed))

