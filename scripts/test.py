from qi import Session
import time

IP = "192.168.1.104"  # Sostituiscilo con l'IP del tuo Pepper
PORT = 9559

session = Session()
session.connect("tcp://{}:{}".format(IP, PORT))
tablet_service = session.service("ALTabletService")

# Se hai caricato il file su Pepper (esempio: /home/nao/html/index.html)
tablet_service.showWebview("file:///home/nao/test.html")
time.sleep(5)
time.sleep(30)
tablet_service.hideWebview()
