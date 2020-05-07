import cv2
import numpy as np
import threading
import time

#Klasse fü Hntergrund arbeiten
class Background():



    #Timer
    def start_timer():
        current_milli_time = int(round(time.time() * 1000))
        return current_milli_time

    def result_timer(start_time):
        current_milli_time = int(round(time.time() * 1000))
        final_time= current_milli_time-start_time
        return final_time

       

    #Kamera
    def camera_initialize():
        cap = cv2.VideoCapture(0)
        return cap

    def live_view(cap):
        while True:
            try:
                c = cv2.waitKey(1)
                ret, frame = cap.read()
                frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA) 
                cv2.imshow('Input', frame)
                #widt_webcam = cap.get(3) #Width
                #height_webcam = cap.get(4) #Height
                #frame_rate = cap.get(5) #FPS
                #print(frame_rate,widt_webcam)                
                if c == 27:
                    cv2.destroyAllWindows()
                    return cap
                    break
            except:
                print("Kamera macht Probleme")
                cv2.destroyAllWindows()
                break
        cv2.destroyAllWindows()

    def start_round(cap, RundenZeit, Schwelle, flag_dauerlauf):
        #Kamera etwas durchlauf geben
        i=0
        while i<30:
            ret, frame = cap.read()
            i+=1

        Flag = True
        value = 0
        Runde =0 
        value_alt = 0
        Start_flag=False

        while Flag==True:
            if(Start_flag==False):
                while i<30:
                    ret, frame = cap.read()
                    i+=1
                Start_flag==True
            #Kamera jetzt Bildauswerten lassen
            ret, frame = cap.read()
            frame = cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA) 
            #Rot extrahieren
            #BGR->HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_red = np.array([0,50,50])
            upper_red = np.array([40,255,255])

            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, lower_red, upper_red)            
            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(frame,frame, mask= mask)

            #Einzelne Bilder anzeigen
            #cv2.imshow('frame',frame)
            #cv2.waitKey(0)
            #cv2.imshow('mask',mask) #Entscheidend
            #cv2.imshow('res',res)
            #cv2.waitKey(0)
            value= np.sum(mask)
            v1 = value-value_alt
            v2 = value_alt-value
            if(v1>v2):
                vges=v2
            else:
                vges=v1
            if(vges/1000>Schwelle and Runde == 0):
                Start_Zeit = Background.start_timer()
                Runde+=1
                print("Start!")
                time.sleep((RundenZeit/2)-5) 
                while i<5:
                    ret, frame = cap.read()
                    i+=1
                value=0
                value_alt=0
            elif(vges/1000>Schwelle and Runde == 1):
                Zwischen_Zeit = Background.result_timer(Start_Zeit)
                Runde+=1
                print("...Zwischenzeit: "+str(Zwischen_Zeit/1000))
                time.sleep((RundenZeit/2)-5)
                while i<5:
                    ret, frame = cap.read()
                    i+=1
                value=0
                value_alt=0
            elif(vges/1000>Schwelle and Runde == 2):
                End_Zeit = Background.result_timer(Start_Zeit) 
                
                #Return Werte [Kamera Handle, Zwischenzeit, Finale Zeit] Wenn flag_dauerlauf gesetzt ist
                if(flag_dauerlauf==False):
                    Fehler = int(input("Anzahl der Fehler (Nicht Straf Sekunden, Tor-Fehler = 5)"))
                    print("Finale Zeit mit Fehler: "+str(End_Zeit+Fehler*2))
                    back = [cap, Zwischen_Zeit, End_Zeit]
                    return back
                else:
                    Fehler = int(input("Anzahl der Fehler (Nicht Straf Sekunden, Tor-Fehler = 5, Dauer Modus Beenden = 99)"))
                    if(Fehler==99):
                        back = [cap, Zwischen_Zeit, End_Zeit]
                        return back
                    print("Finale Zeit mit Fehler: "+str(End_Zeit/1000+Fehler*2))
                    Runde =0
                    time.sleep(5) 
                    while i<5:
                        ret, frame = cap.read()
                        i+=1
                    value=0
                    value_alt=0
            
            #Schwelle Anzeigen lassen
            #print(vges/1000)
            value_alt =value
            
            
        