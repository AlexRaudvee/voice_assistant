# imports
import speech_recognition as sr

from func_ import say, wake_func, conversation, dialog_with_AI

# global variables
r = sr.Recognizer()
mic = sr.Microphone()

# language 
lang = 'ru'

# run the main program 
if __name__ == "__main__":
    lang = 'ru'
    print('start...')
    if wake_func():
        say("привет черномазый", lang)
        while True:
            transcript = conversation(lang)
            if transcript == 'отмена':
                say("ладно, я офф!", lang)
                break
            elif (transcript == "сменить язык") or (transcript == 'change language'):
                if lang == "ru":
                    lang = 'en'
                    say("The language changed to english", lang)
                else:
                    lang = 'ru'
                    say("Язык сменён на русский", lang)
            elif (transcript == "switch to smart mode") or (transcript == 'сменить на умный режим'):
                
                say("пока что я говорю только на английском в умном режиме!", lang='ru')
                with mic as source:
                        say('welcome to smart mode what you want to talk about?', lang='en')
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        audio = r.listen(source)
                        transcript = r.recognize_google(audio, language="en-EN")

                lang = 'en'
                dialog_with_AI(f"{transcript}")

            else:
                say(f"вы сказали {transcript}?", lang)


