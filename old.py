# pip.exe install openai, scipy, speech_recognition , audiofile, gtts, pyttsx3, keyboard, scipy.io.wavfile
import openai
import pandas as pd
openai.api_key = "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"
log_filename = 'ocr.txt'
chat = [{"role": "system", "content": "You are helpful, carefull and patient assistant made to help older people, give your answers in english and if you does not know the answer to a question, it truthfully says it does not know."}]

# save log
def save_log(conversation):
    data = pd.DataFrame(conversation)
    data.to_csv(log_filename, index=False)
    print('== Log Created ==')
    print('Thank you')


def main():
    while True:
        transcription = audio_to_txt()
        print(transcription)
        if transcription['text'].lower() == 'thank you.':
            save_log(chat)
            break
        chat.append({"role": "user", "content": transcription['text']})
        print(f"\nUser: {transcription['text']}")

        # Testar por texto: Não funciona sair com thank you
        # transcription = input(">>>")
        # chat.append({"role": "user", "content": f'{transcription}'})
        # print(f"\nUser: {transcription}")

        bot = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                           temperature=0.0,
                                           messages=chat)

        response = bot.choices[0].message.content
        chat.append({"role": "assistant", "content": response})
        print(f"Assistant: {response}")
        print("\n=== Press enter to stop the answer and start a new question ===\n")
        speech(response)


if __name__ == '__main__':
    main()