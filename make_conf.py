from getmac import get_mac_address as get_mac
from urllib.request import urlopen
from datetime import datetime
import platform as pf
import http.client
import requests
import socket
# import psutil
import time
import json
import sys
import wmi
import os

def get_sys_info(path_to_save):
    """ Gathering information about current PC configuration. """

    def add_zero(value):
        """ Adds a zero before a number if it is less than ten. """
        if value < 10:
            final_value = f"0{value}"
        elif value >= 10:
            final_value = value

        return final_value

    def get_name():
        """ Gets the current date and time to use it as a name for a new file. """
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


        result = f"SystemConf_{current_month}_{current_day}_{full_date.year}_"
        result += f"{current_hour}_{current_minute}_{current_second}.json"

        return result

    def wmi_parser(response):
        """ Parser for returned data from modules from the 'wmi' library. """
        result = {}
        extra_strings = ['\n', '\t', '{', '}', '"']
        possible_instances = ['ComputerSystem', 'OperatingSystem',
            'Processor', 'VideoController']

        other = []

        for instance in possible_instances:
            extra_strings.append(f'instance of Win32_{instance}')

        for element in extra_strings:
            response = str(response).replace(element, '')
        response = str(response).replace(';', ',')
        response = response.split(',')
        # print(response)

        for i in range(2):
            del response[-1]

        for element in response:
            separated_part = element.split('=')
            separated_part = [text.strip() for text in separated_part]

            try:
                result[separated_part[0]] = separated_part[1]
            except IndexError:
                other.append(separated_part[0])

        # There may be installed several of display drivers.
        if other:
            if 'InstalledDisplayDrivers' in result.keys():
                result['InstalledDisplayDrivers'] = [result['InstalledDisplayDrivers']]

                for value in other:
                    result['InstalledDisplayDrivers'].append(value)

        return result


    all_collected = {}

    # External IP-address.
    try:
        connection = http.client.HTTPConnection("ifconfig.me")
        connection.request("GET", "/ip")
        external_ip = str(connection.getresponse().read())[2:-2]
    except socket.gaierror:
        
        try:
            external_ip = requests.get('https://ramziv.com/ip').text
            
        except:
            external_ip = 'No_Network_Access'

    # Internet service provider's location.
    try:
        with urlopen("https://ipinfo.io/json") as loc:
            json_format = loc.read()

        location = json.loads(json_format)

        try:
            del location["readme"]
        except KeyError:
            pass

    except:
        location = 'UNKNOWN'

    this_pc = wmi.WMI()
    computer_info = this_pc.Win32_ComputerSystem()[0]
    computer_info = wmi_parser(computer_info)

    os_info = this_pc.Win32_OperatingSystem()[0]
    parsed_os_info = wmi_parser(os_info)

    cpu = this_pc.Win32_Processor()[0]
    cpu = wmi_parser(cpu)

    gpu = this_pc.Win32_VideoController()[0]
    gpu = wmi_parser(gpu)

    total_ram = os_info.TotalVisibleMemorySize
    total_ram = "{} KB ({:.2F} GB usable)".format(total_ram, float(total_ram)/1048576)

    # Adding a collected information to the dictionary.
    keys_list = ['local_time', 'user_name', 'host_name', 'local_ip', 'external_ip', 
        'host_mac', 'wifi_ap_mac', 'provider_location', 'general_info', 'os_info', 'cpu_info', 'cpu_arch',
        'gpu_info', 'total_ram_size']
    
    try:
        mac_1 = get_mac()
    
    except OSError:
        mac_1 = 'None'
    
    
    try:
        mac_2 = get_mac(ip='192.168.1.1')
        
    except OSError:
        mac_2 = 'None'
        
        
    values_list = [time.ctime(), os.environ['USERNAME'], (socket.gethostname(), os.environ['COMPUTERNAME']),
        socket.gethostbyname(socket.gethostname()), external_ip,
        mac_1, mac_2, location, computer_info, parsed_os_info, cpu,
        os.environ['PROCESSOR_ARCHITECTURE'], gpu, total_ram]
    
   
        
    
    index = -1
    for key in keys_list:
        index += 1

        if key == 'host_name':
            try:
                all_collected[key] = values_list[index][0]
            except:
                all_collected[key] = values_list[index][1]

        elif (key == 'wifi_ap_mac') and (values_list[index] == None):
            all_collected[key] = get_mac(ip='192.168.0.1')

        else:
            all_collected[key] = values_list[index]

    # os.system("netsh wlan show profile > cmd_output.txt")
    # with open()

    new_file = get_name()
    with open(f'{path_to_save}\\{new_file}', 'w', encoding='utf-8') as file_object:
        json.dump(all_collected, file_object, ensure_ascii=False, indent=4)
 