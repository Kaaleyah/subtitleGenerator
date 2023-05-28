import azure.cognitiveservices.speech as speechsdk
import time
import datetime

speechKey = "75636e87415245a18d99b6be109b1c76"
serviceRegion = "eastus"

fileName = input("Enter the sound file name: ")
audioConfig = speechsdk.AudioConfig(filename=fileName)

speechConfig = speechsdk.SpeechConfig(subscription=speechKey, region=serviceRegion)
speechRecognizer = speechsdk.SpeechRecognizer(speech_config=speechConfig, audio_config=audioConfig)

subtitles = []

def formatSubtitles(index, subtitle):
    startTime = datetime.timedelta(seconds=subtitle[0] / 10**7)
    endTime = datetime.timedelta(seconds=(subtitle[0] + subtitle[1]) / 10**7)
    subtitleText = subtitle[2]

    startTime = str(startTime).replace('.', ',')[:-3]
    endTime = str(endTime).replace('.', ',')[:-3]

    return f"{index}\n{startTime} --> {endTime}\n{subtitleText}\n"


def stop_cb(evt):
    """callback that stops continuous recognition upon receiving an event `evt`"""
    print('CLOSING on {}'.format(evt))
    speechRecognizer.stop_continuous_recognition()
    

def recognized(evt):
    print('RECOGNIZED: {}'.format(evt))
    subtitles.append((evt.result.offset, evt.result.duration, evt.result.text))

def finished(evt):
    print('SESSION STOPPED {}'.format(evt))
    compileSubtitles()


speechRecognizer.recognized.connect(recognized)
speechRecognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
speechRecognizer.session_stopped.connect(finished)
speechRecognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

# Stop in error
speechRecognizer.session_stopped.connect(stop_cb)
speechRecognizer.canceled.connect(stop_cb)

speechRecognizer.start_continuous_recognition()

def compileSubtitles():

    with open("subtitles.srt", "w") as f:
        for i in range(len(subtitles)):
            subtitle = formatSubtitles(i + 1, subtitles[i])

            f.write(subtitle)
            f.write("\n")

while True:
    # This is just an example. The actual code will depend on your specific application.
    # You can use a loop or other mechanism to keep the program running until the user
    # indicates that they want to stop the program.
    time.sleep(1)