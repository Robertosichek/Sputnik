import speech_recognition as sr
import telebot
import soundfile as sf
bot = telebot.TeleBot('YOUR_TOKEN')


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('new_file.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
        new_file.close()
    data, samplerate = sf.read('new_file.ogg')
    sf.write('new_file.wav', data, samplerate)
    text = speech_to_text('new_file.wav') # Здесь хранится сообщение пользователя в текстовом формате
    print(text)


def speech_to_text(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='ru-RU')
        return text


bot.polling(none_stop=True, interval=0)
