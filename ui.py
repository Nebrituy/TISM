from tkinter import *
import requests
import socket
import re
import time

mac_list = """ v2473- 4c:5e:0c:c2:2e:b8   -   xe-0/0/30.2473         0         0
    v2473- 6c:b2:ae:22:21:54     -   et-0/0/48.2473         0         0
    v2473-  6c:b2:ae:bb:d1:20    -   et-0/0/48.2473         0         0

"""
mac = "64d1-54d0-a9b5"
ip = '8.8.8.8'
url = 'https://www.youtube.com/'

def gom():
    pattern = r'(?<!:)\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b(?!:)|(?<!:)\b(?:[0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}\b(?!:)|(?<!:)\b(?:[0-9A-Fa-f]{4}-){2}[0-9A-Fa-f]{4}\b(?!:)'
    pattern1 = r'\.'
    list_of_macs = text.get(1.0, END)
    list_of_macs = re.findall(pattern, list_of_macs)
    for mac in list_of_macs:
        time.sleep(1)
        index_of_mac = text.search(mac, 1.0, END)
        # print(index_of_mac)
        i, j = re.split(pattern1, index_of_mac)
        vendor = get_info_mac(mac)
        i = int(i)
        j = int(j) + 17
        text.insert(f'{i}.{j}', " "+vendor)
        print(f'{i}.{j}', " "+vendor)


def get_info_by_ip(ip):
    pis_data = ""
    data = {
        '[IP]': ('query'),
        '[Провайдер]': ('isp'),
        '[Организация]': ('org'),
        '[As]': ('as'),
        '[AsName]': ('asname'),
        '[Страна]': ('country'),
        '[Регион]': ('regionName'),
        '[Город]': ('city'),
        '[ZIP]': ('zip'),
        '[District???]': ('district'),
        '[Lat]': ('lat'),
        '[Lon]': ('lon'),
    }
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        for k, v in data.items():
            # print(f'{k} : {response.get(v)}')
            pis_data = pis_data + f'{k}  :  {response.get(v)} \n'
        latitude = response.get('lat')
        longitude = response.get('lon')
        pis_data = pis_data + f'https://maps.google.com/maps?q={latitude},{longitude}'
        return pis_data
    except requests.exceptions.ConnectionError:
        print('[!] Please check your connection!')


def get_info_mac(mac):
    try:
        responce = requests.get('https://api.macvendors.com/' + mac)
        if responce.status_code == 200:
            return responce.text
        else:
            return 'Vendor not found.'
    except ImportError:
        from urllib import request, error
        try:
            responce = request.urlopen('https://api.macvendors.com/' + mac)
            print(type(responce.read().decode('utf-8')))
            return responce.read().decode('utf-8')
        except error.HTTPError:
            return 'Vendor not found.'


def get_ip_by_hostname(hostname):
   hostname = hostname.strip("http://").strip("https://").strip("www.")
   if hostname.find('/') != -1:
      hostname = hostname[:hostname.find('/')]

   try:
      return get_info_by_ip(socket.gethostbyname(hostname))
      # return f'Hostname: {hostname}\nIP address: {socket.gethostbyname(hostname)}'
   except socket.gaierror as error:
      return f'Invalid Hostname - {error}'


def clear_board():
   text.delete('1.0', END)



def ins(info):
   clear_board()
   text.insert(INSERT, info)


def gim():
    info = get_info_mac(e_mac.get())
    ins(info)


def gih():
    info = get_ip_by_hostname(e_url.get())
    ins(info)





root = Tk()
root.geometry('750x580+100+150')
root.resizable(0,0)
root.title("TISM")

e_mac = Entry(root)
e_mac.grid(row=4, column=0, padx=10, sticky=W + E)
e_mac.insert(0, mac)

e_url = Entry(root)
e_url.grid(row=5, column=0, padx=10, sticky=W + E)
e_url.insert(0, ip)

text = Text(root, width=93, height=30)
text.grid(row=6, column=0, columnspan=30)
text.insert(0.0, mac_list)

# canvas = Canvas(text, bg='Yellow')
# canvas.grid(row=0, column=0)
#
# scroll = Scrollbar(text, orient=VERTICAL, command=yview)
# scroll.grid(row=1, column=0, sticky=EW)
# canvas.configure(yscrollcommand=vsbar.set)

btn_MAC = Button(root, text='Чекнуть МАК', padx=5, command=gim)
btn_MAC.grid(row=4, column=3, pady=10)

btn_MAC = Button(root, text='Чекнуть МАКи в тексте', padx=5, command=gom)
btn_MAC.grid(row=4, column=4, pady=10)

btn_info = Button(root, text='Чекнуть IP/URL', padx=5, command=gih)
btn_info.grid(row=5, column=3, pady=10)



root.mainloop()
