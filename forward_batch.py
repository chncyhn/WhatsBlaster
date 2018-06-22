from WhatsBlaster import WhatsBlaster

with open("names.txt", "r") as f:
    names = [line.strip() for line in f.readlines()]

W = WhatsBlaster("chromedriver.exe")
W.forward_message(names)
W.close()
