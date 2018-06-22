from WhatsBlaster import WhatsBlaster

with open("names.txt", "r") as f:
    names = [line.strip() for line in f.readlines()]

with open("message.txt", "r") as f:
    mesaj = f.read()

W = WhatsBlaster("chromedriver.exe")
for name in names:
    print( W.send_message(
            name,           # exact WhatsApp contact name
            mesaj        # message to send
            )               # returns success/failure message
        )
W.close()
