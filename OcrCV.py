import cv2
import pytesseract
import pandas as pd
import os
from openai import OpenAI


os.environ["OPENAI"] = ''


def save_text(entrada, path):
    with open(f'{path}.txt', 'w') as arquivo:
        arquivo.write(entrada)


def scan(diretorio_raiz, extensao_arquivo):
    for pasta_raiz, subpastas, arquivos in os.walk(diretorio_raiz):
        entrada = ''
        for arquivo in arquivos:
            if arquivo.endswith(extensao_arquivo):
                caminho_arquivo = os.path.join(pasta_raiz, arquivo)
                saida = f'{caminho_arquivo.split(os.path.sep)[0]}/{os.path.basename(os.path.dirname(caminho_arquivo))}'
                filename = f'{caminho_arquivo}'
                entrada += (f'{filename}\n'
                            f'{imgtotxt(caminho_arquivo)}'
                            f'\n')
        save_text(entrada, saida)

def imgtotxt(imagem):
    imgsample = imagem
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract"
    )
    img = cv2.imread(imgsample)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Adding custom options
    custom_config = r'--oem 3 --psm 6'
    txtraw = pytesseract.image_to_string(gray, config=custom_config)
    return txtraw

def mml(txtraw):
    chat = [{"role": "system",
             "content": "Corrija o texto em portugues de Portugal:"}]
    chat.append({"role": "user", "content": txtraw})
    print(chat)
    bot = client.chat.completions.create(model="gpt-3.5-turbo",
                                       temperature=0.0,
                                       messages=chat)

    response = bot.choices[0].message.content
    chat.append({"role": "assistant", "content": response})
    print(f"Assistant: {response}")
    return response

if __name__ == '__main__':
    #client = OpenAI(api_key=os.environ["OPENAI"],)
    log_filename = 'ocr.txt'
    imagem = "./teste/test3.jpg"
    pasta = './teste'
    scan(pasta, 'jpg')
    ocr = imgtotxt(imagem)
    #assistente = mml(ocr)
    #save_log(assistente)
    print (ocr)