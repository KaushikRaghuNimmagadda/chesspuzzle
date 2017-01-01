# https://pythonspot.com/en/speech-recognition-using-google-speech-api/
# The code used in this was taken from this link (it was super helpful)
import speech_recognition as sr

def getVoice():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Speak your move")
		audio = r.listen(source)
		
	try:
   		move = r.recognize_google(audio)
	except sr.UnknownValueError:
   		print("Google Speech Recognition could not understand audio")
   		move = "invalid input"
	except sr.RequestError:
    		print("Out of API queries OR internet connection doesn't work.  Input will be switched to text.")
    		move = 'voice'
	return move

# NATO ALPHABET
# a -> alpha
# b -> beta/bravo
# c -> charlie
# d -> delta
# e -> epsilon/echo
# f -> fox/foxtrot
# h -> hotel/hospital
