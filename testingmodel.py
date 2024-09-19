import cv2
from controller import doorAutomate 
import time 
from datetime import date 
today = date.today() 
import sqlite3 
conn = sqlite3.connect('C:\\Users\\yasha\\Desktop\\class.db') 
cursor=conn.cursor() 
 
video=cv2.VideoCapture(0) 
 
 
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") 
 
recognizer = cv2.face.LBPHFaceRecognizer_create() 
recognizer.read("Trainer.yml") 
 
name_list = ["", "BTECH/25022/21", "BTECH/25017/21"] 
 
imgBackground = cv2.imread("Face Recognition Door Lock.png") 
 
while True: 
    ret,frame=video.read() 
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    #faces = facedetect.detectMultiScale(gray, 1.3, 5) 
    faces = facedetect.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=7) 
    for (x,y,w,h) in faces: 
        serial, conf = recognizer.predict(gray[y:y+h, x:x+w]) 
        if conf>50: 
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1) 
            cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2) 
            cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1) 
            cv2.putText(frame, name_list[serial], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2) 
        else:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1) 
            cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2) 
            cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1) 
            cv2.putText(frame, "Unknown", (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2) 
    frame=cv2.resize(frame, (640, 480)) 
    imgBackground[162:162 + 480, 55:55 + 640] = frame 
    cv2.imshow("Frame",imgBackground) 
     
    k=cv2.waitKey(1) 
     
    if k==ord('o') and conf>50: 
        doorAutomate(0) 
        table_name="BTECH_CSE_2021" 
        column_name=str(today) 
        column_name="Date_"+column_name.replace("-","_") 
        print(column_name) 
        check_query = f"PRAGMA table_info('{table_name}')" 
        cursor.execute(check_query) 
        column_exists = any(row[1] == column_name for row in cursor.fetchall()) 
        if not column_exists: 
            create_column_query = f"ALTER TABLE {table_name} ADD {column_name} CHAR(1) NOT NULL 
DEFAULT 'A'" 
            update_condition = f"ROLLNO={name_list[serial]}" 
            attendence="P" 
            update_query = f"UPDATE {table_name} SET {column_name} = {attendence} WHERE 
{update_condition}" 
            try: 
                cursor.execute(create_column_query) 
                conn.commit() 
                cursor.execute(update_query) 
                rows_updated = cursor.rowcount 
                doorAutomate(0) 
                time.sleep(10) 
                doorAutomate(1)
                 break 
            except sqlite3.Error as err: 
                print(f"Error creating column1: {err}") 
        else: 
            update_condition = f"ROLLNO='{name_list[serial]}'" 
            attendence="P" 
            update_query = f"UPDATE {table_name} SET {column_name} ='{attendence}' WHERE {update_condition}" 
            print(update_query) 
            try: 
                cursor.execute(update_query) 
                rows_updated = cursor.rowcount 
                doorAutomate(0) 
                time.sleep(10) 
                doorAutomate(1) 
                break 
            except sqlite3.Error as err: 
                print(f"Error updating column: {err}") 
                break 
        time.sleep(10) 
        doorAutomate(1) 
    if k==ord("q"): 
        break 
conn.commit() 
conn.close() 
video.release() 
cv2.destroyAllWindows()
