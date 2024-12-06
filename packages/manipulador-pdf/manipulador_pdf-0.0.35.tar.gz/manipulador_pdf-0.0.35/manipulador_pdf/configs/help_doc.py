import json
import os


def help_doc(option: int) -> None:
    os.startfile(os.getcwd() + fr'\configs\sample\{option}.pdf')
    with open('configs/READMEs.json', 'r', encoding='utf-8') as file:
        print(json.load(file)[str(option)])
    print('Um modelo deste arquivo está sendo aberto...')