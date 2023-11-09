import pyautogui, webbrowser
from time import sleep

webbrowser.open('https://web.whatsapp.com/send?phone=+525632507504')

sleep(25)

for i in range(1):
    pyautogui.typewrite('prueba')
    pyautogui.press('enter')