"""
Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera.  See more about it here:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

Use Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   First, we'll walk you through setting up the Google Cloud Platform.  Next, we will use the Raspberry Pi Camera to take a picture of an object, and then use the Raspberry Pi to upload the picture taken to Google Cloud.  We can analyze the picture and return labels (what's going on in the picture), logos (company logos that are in the picture) and faces.

This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

"""

import argparse
import base64
import picamera
import json
import urllib2
from subprocess import call
import time
import datetime


import atexit
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def takephoto():
    camera = picamera.PiCamera()
    camera.capture('image.jpg')

def sound(spk):
	#	-ven+m7:	Male voice
	#  The variants are +m1 +m2 +m3 +m4 +m5 +m6 +m7 for male voices and +f1 +f2 +f3 +f4 which simulate female voices by using higher pitches. Other variants include +croak and +whisper.
	#  Run the command espeak --voices for a list of voices.
	#	-s180:		set reading to 180 Words per minute
	#	-k20:		Emphasis on Capital letters
	call(" amixer set PCM 100 ", shell=True)	# Crank up the volume!

	cmd_beg=" espeak -ven-us+m5 -a 200 -s110 -k20 --stdout '"
	cmd_end="' | aplay"
	print cmd_beg+spk+cmd_end
	call ([cmd_beg+spk+cmd_end], shell=True)

def parse_response(json_response):
	# print json_response
	try:
		# print json.dumps(response, indent=4, sort_keys=True)	#Print it out and make it somewhat pretty.
		anger = json_response['responses'][0]['faceAnnotations'][0]['angerLikelihood']
		surprise = json_response['responses'][0]['faceAnnotations'][0]['surpriseLikelihood']
		sorrow = json_response['responses'][0]['faceAnnotations'][0]['sorrowLikelihood']
		blurr = json_response['responses'][0]['faceAnnotations'][0]['blurredLikelihood']
		joy = json_response['responses'][0]['faceAnnotations'][0]['joyLikelihood']
		headwear = json_response['responses'][0]['faceAnnotations'][0]['headwearLikelihood']		

		anger_string = (str(anger))
		surprise_string = (str(surprise))
		sorrow_string = (str(sorrow))
		# print(str(blurr))
		happy_string = (str(joy))
		headwear_string = (str(headwear))
		
		print("Happy: " + happy_string)
		print("Angry: " + anger_string)
		print("Surprise: " + surprise_string)
		print("Sorrow: " + sorrow_string)
		print("Headwear: " + headwear_string)
		# sound("You look pretty. . . . tired.  You must have an infant?")
		
		if(happy_string != "VERY_UNLIKELY"):
			sound("You seem happy!  Tell me why you are so happy!")
		elif(anger_string != "VERY_UNLIKELY"):
			sound("Uh oh, you seem angry!  I have kids, please don't hurt me!")
		elif(surprise_string != "VERY_UNLIKELY"):
			sound("You seem surprised!  ")
		else:
			sound("You seem sad!  Would you like a hug?")
		
	except:
		sound("I am sorry, I can not see your face.  May I try again?")

def take_emotion():
    takephoto() # First take a picture
    """Run a label request on a single image"""
    
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open('image.jpg', 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'FACE_DETECTION',
                    'maxResults': 10
                }]
            }]
        })
        response = service_request.execute()
        parse_response(response)

def main():

        take_emotion()

	#sound("I am ready to empathize!")  #testing TTS
if __name__ == '__main__': 

    main()
