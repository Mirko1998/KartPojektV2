
from Background import Background

Message="Kart_Tool_V1.1\n"
Message = Message+"\nStart Timer: 1"
Message = Message+"\nTime Result: 2\n"
Message = Message+"Initialize Camera: 3\n"
Message = Message+"Strecken Parameter: 99\n"
Message = Message+"Camera live view: 4\n"
Message = Message+"Start Zeitmessung!: 5\n"


#Variablen
Number =0
Exit=False
camera_handle=0
Rundenzeit=20
Schwelle=100
flag_dauerlauf =True
Fahrer = "Tester"

while(Exit==False):
    print("\n\n\n")
    try:
        Number = int(input(Message))
    except:
        Exit=False
        Number=-1
    if(Number == 0):
        Exit = True
    elif(Number == 1):
        StartTimer = Background.start_timer()
        #print("Timer startet: "+str(StartTimer))
    elif(Number ==2):
        result_time = Background.result_timer(StartTimer)  
        print("Time: "+str(result_time))
    elif(Number ==99):
        Message2 ="Bitte geben sie die geschätze Rundenzeit in Sekunden an (Zahl): \n"
        Rundenzeit = int(input(Message2))
        Message2 ="Bitte geben sie eine Schwelle an (Zahl): \n"
        Schwelle = int(input(Message2))
        Message2 ="Welcher Fahrer fährt gerade? (Text): \n"
        Schwelle = str(input(Message2))
        Message2 ="Dauerlauf? (True/False): \n"
        Schwelle = bool(input(Message2))
    elif(Number ==3):
        print("Initialisiere... (Kann bis 10 Sekunden dauern)")
        camera_handle = Background.camera_initialize()
        print("Kamera initialisiert!")
    elif(Number ==4):
        if(camera_handle==0):
            print("Bitte erst Kamera Initialisieren!")
        else:   
            camera_handle = Background.live_view(camera_handle)
    elif(Number ==5):
        print("")
        #Prüfen ob Kamera initialisiert ist
        if(camera_handle==0 or Rundenzeit==0 or Schwelle ==0):
            print("Bitte erst Kamera Initialisieren (3) oder Streckenparameter eingeben (99)!")
        else:
            Zeiten = Background.start_round(camera_handle, Rundenzeit, Schwelle, flag_dauerlauf)
            camera_handle= Zeiten[0]
            end_zeit= Zeiten[1]
            zwischen_zeit= Zeiten[2]
    else:
        Exit=False
