import os
os.environ['KIVY_TEXT'] = 'pil'
import enchant
import kivy
from cryptography.fernet import Fernet
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.textinput import TextInput
from re import findall
import random


kivy.require('1.10.0')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')

class ScreenManagement(ScreenManager):
    pass

class MainScreen(Screen):
    pass    

class CaesarScreen(Screen):
    def caesar_encrypt(self,message, key,final=''):
        for symbol in message:
            final += chr((ord(symbol) - key - 13)%26 + ord('A'))
        self.ids.caesar_out.text = final
    def caesar_decrypt(self,message, key,final=''):
        for symbol in message:
            final += chr((ord(symbol) + key - 13)%26 + ord('A'))
        self.ids.caesar_out.text = final
    
class VishenerScreen(Screen):

    def vishener_encrypt(self,message,key,final=''):
        key *= len(message) // len(key) + 1
        for i, j in enumerate(message):
            temp = ord(j) + ord(key[i])
            final += chr(temp % 26 + ord('A'))
        self.ids.vishener_out.text = final
    
    def vishener_decrypt(self,message,key,final=''):
        key *= len(message) // len(key) + 1
        for i, j in enumerate(message):
            temp = ord(j) - ord(key[i])
            final += chr(temp % 26 + ord('A'))
        self.ids.vishener_in.text = final
        
class PolibiyScreen(Screen):
    global keysPolibiy
    keysPolibiy = {
        'A':'11', 'B':'12', 'C':'13', 'D':'14',
        'E':'15', 'F':'16', 'G':'21', 'H':'22',
        'I':'23', 'J':'24', 'K':'25', 'L':'26',
        'M':'31', 'N':'32', 'O':'33', 'P':'34',
        'Q':'35', 'R':'36', 'S':'41', 'T':'42',
        'U':'43', 'V':'44', 'W':'45', 'X':'46',
        'Y':'51', 'Z':'52', '0':'53', '1':'54',
        '2':'55', '3':'56', '4':'61', '5':'62',
        '6':'63', '7':'64', '8':'65', '9':'66'
    }
    def regular(self,text):
        template = r"[0-9]{2}"
        return findall(template, text)
    def polibiy_encrypt(self,message,final=''):
        for symbol in message:
                if symbol in keysPolibiy:
                    final += keysPolibiy[symbol]
        self.ids.polibiy_out.text = final
    def polibiy_decrypt(self,message,final=''):
        for twoNumbers in self.regular(message):
                for key in keysPolibiy:
                    if twoNumbers == keysPolibiy[key]:
                        final += key
        self.ids.polibiy_in.text = final

class AtbashScreen(Screen):
    def atbash(self,message,final=''):
        alphaDefault = [chr(x) for x in range(65,91)]
        alphaReverse = list(alphaDefault); alphaReverse.reverse()
        for symbolMessage in message:
            for indexAlpha, symbolAlpha in enumerate(alphaDefault):
                if symbolMessage == symbolAlpha:
                    final += alphaReverse[indexAlpha]
            self.ids.atbash_out.text = final


class PlayfairScreen(Screen):
    global matrixKey,addSymbol  
    matrixKey = [
        ['S','O','M','E','T'],
        ['H','I','N','G','A'],
        ['B','C','D','F','K'],
        ['L','P','Q','R','U'],
        ['V','W','X','Y','Z']
    ]; addSymbol = 'X'
    
    def regular(self, text):
        template = r"[A-Z]{2}"
        return findall(template, text)
    
    def encryptDecrypt(self, mode, message, final = ""):
        
        if mode == True:
            for symbol in message:
                if symbol not in [chr(x) for x in range(65,91)]:
                    message.remove(symbol)
            for index in range(len(message)):
                if message[index] == 'J': message[index] = 'I'
            for index in range(1,len(message)):
                if message[index] == message[index - 1]:
                    message.insert(index,addSymbol)
            if len(message) % 2 != 0:
                message.append(addSymbol)

        binaryList = self.regular("".join(message))
        for binary in range(len(binaryList)):
            binaryList[binary] = list(binaryList[binary])
            for indexString in range(len(matrixKey)):
                for indexSymbol in range(len(matrixKey[indexString])):
                    if binaryList[binary][0] == matrixKey[indexString][indexSymbol]:
                        y0, x0 = indexString, indexSymbol
                    if binaryList[binary][1] == matrixKey[indexString][indexSymbol]:
                        y1, x1 = indexString, indexSymbol
            for indexString in range(len(matrixKey)):
                if matrixKey[y0][x0] in matrixKey[indexString] and matrixKey[y1][x1] in matrixKey[indexString]:

                    if mode == True:
                        x0 = x0 + 1 if x0 != 4 else 0
                        x1 = x1 + 1 if x1 != 4 else 0
                    else:
                        x0 = x0 - 1 if x0 != 0 else 4
                        x1 = x1 - 1 if x1 != 0 else 4

            y0,y1 = y1,y0
            binaryList[binary][0] = matrixKey[y0][x0]
            binaryList[binary][1] = matrixKey[y1][x1]
        for binary in range(len(binaryList)):
            for symbol in binaryList[binary]:
                final += symbol
        self.ids.playfair_out.text = final
            
class FernetScreen(Screen):
    def fernetenc(self,msg):
        global f, key
        key = Fernet.generate_key()
        f = Fernet(key)
        token = str(f.encrypt(msg.encode()))
        self.ids.lbl.text = token[2:-1]
    def fernetdec(self,token):
        dec = str(f.decrypt(token.encode()))
        self.ids.my_msg.text = dec[2:-1]

class EmojiScreen(Screen):
    def emoenc(self,msg):
        global t,c
        t=msg
        a=[]
        for i in range(len(msg)):
            a.append(chr(random.randrange(128513, 128590)))
        c=str(a)
        b="[],' "
        for char in b:
            c = c.replace(char,"")
        self.ids.emo.text=c        
    def emodec(self):
        self.ids.my_msg.text=t

class MyApp(App):
    def build(self):
        self.title = 'Crypto'
        Builder.load_file("main.kv")
        return ScreenManagement()

if __name__ == "__main__":
    MyApp().run()