# imports 
import torch
import pyglet

import speech_recognition as sr
import soundfile as sf

from pvrecorder import PvRecorder
from config import porcupine, synthesiser, speaker_embedding, chater
from gtts import gTTS
from time import sleep
from transformers import Conversation


# global variables
recoder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
r = sr.Recognizer()
mic = sr.Microphone()


# produce sound on mac ("Russian default")
def say(text: str, lang: str):
    if lang == 'ru':
        tts = gTTS(text=f'{text}', lang=f'{lang}', )
        tts.save("out.mp3")
        music = pyglet.media.load("out.mp3", streaming=False)
        music.play()
        sleep(music.duration)


    elif lang == 'en':
        # text = gs.translate(text, 'en')
        speech = synthesiser(f"{text}", forward_params={"speaker_embeddings": speaker_embedding})
        sf.write("out.mp3", speech["audio"], samplerate=speech["sampling_rate"])
        music = pyglet.media.load("out.mp3", streaming=False)
        music.play()
        sleep(music.duration)
        
        

    

# wake word function
def wake_func():
    try:
        recoder.start()

        while True:
            keyword_index = porcupine.process(recoder.read())
            if keyword_index >= 0:
                print(f"Detected")
                return True

    except KeyboardInterrupt:
        recoder.stop()
    finally:
        porcupine.delete()
        recoder.delete()

def conversation(lang: str):

    if lang == 'ru':
        while True:
            try: 
                with mic as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source)
                    transcript = r.recognize_google(audio, language="ru-RU")

                    return transcript.lower().strip()

            except sr.UnknownValueError:
                say("простите, что вы сказали?", lang)
                continue
    else:
        lang == "en"
        while True:
            try: 
                with mic as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source)
                    transcript = r.recognize_google(audio, language="en-EN")

                    return transcript.lower().strip()

            except sr.UnknownValueError:
                say("Sorry, what you just said?", lang)
                continue


def dialog_with_AI(user: str):
    lang = 'en'
    while user != 'exit smart mode':
        conversation = Conversation(user)
        conversation = chater(conversation)
        say(conversation.generated_responses[-1], lang)
        
        try:    
            with mic as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
                user = r.recognize_google(audio, language="en-EN")
                if user == 'exit smart mode':
                    break
                
                conversation.add_user_input(user)
                conversation = chater(conversation)
                say(conversation.generated_responses[-1], lang)

                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
                user = r.recognize_google(audio, language="en-EN")
                if user == 'exit smart mode':
                    break

                conversation.add_user_input(user)
                conversation = chater(conversation)
                say(conversation.generated_responses[-1], lang)

                conversation = Conversation()
        except sr.UnknownValueError:
            say("i didn't hear you well can your repeat what you said?", lang)
            continue



