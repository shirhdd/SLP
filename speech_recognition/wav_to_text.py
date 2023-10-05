import speech_recognition as sr

recognizer = sr.Recognizer()


def textIt(file_path):

    with sr.AudioFile(file_path) as source:
        recorded_audio = recognizer.listen(source)
        print("Done recording")

    ''' Recorgnizing the Audio '''
    try:
        print("Recognizing the text")
        text = recognizer.recognize_google(
            recorded_audio,
            language="en-US"
        )
        print("Decoded Text : {}".format(text))
        return text

    except Exception as ex:
        print(f"error while decode: ", ex)
