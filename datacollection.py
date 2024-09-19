# pip install opencv-python==4.5.2 
import cv2 
 
# Replace "0" with the camera index if you have multiple cameras
cap = cv2.VideoCapture(0) 
 
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") 
 
id = input("Enter Your ID: ") 
id = int(id) 
count = 0 
 
while True: 
    ret, frame = cap.read() 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    #faces = facedetect.detectMultiScale(gray, 1.3, 5) 
    faces = facedetect.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=7) 
    for (x, y, w, h) in faces: 
        count += 1 
        cv2.imwrite('./images/User.'+str(id)+"."+str(count)+".jpg", gray[y:y+h, x:x+w]) 
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1) 
 
    cv2.imshow("Frame", frame) 
 
    k = cv2.waitKey(1) 
 
    if count > 1000 or k == ord('q'): 
        break 
 
cap.release() 
cv2.destroyAllWindows() 
print("Dataset Collection Done..................")
