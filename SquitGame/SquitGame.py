import cv2
from random import randint

cap = cv2.VideoCapture(0) #ระบุหมายเลขกล้อง
check , frame1 = cap.read() #รับภาพจากกล้องเป็นframe หาคอนทัวร์
check , frame2 = cap.read() #รับภาพจากกล้องเป็นframe หาข้อมูล
box_ck = False
num_ck = randint(15, 30)
num_ck2 = randint(30, 40)
die = False
score = 0
iceice = False
while (cap.isOpened()): #ตั้งเพื่อให้มันรับภาพอยู่ตลอดเวลาแล้วแสดงแบบเรียลไทม์
    if check == True:
        if num_ck >= 0 and die == False:
            if num_ck <= 3:
                 cv2.putText(frame1, "MOVE", (250, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 204, 255), cv2.LINE_4)
                 num_ck -= 0.1
            else:
                cv2.putText(frame1, "MOVE", (250, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 0), cv2.LINE_4)
                num_ck -= 0.1

        else:
            if num_ck2 >= 0:
                iceice = True
                num_ck2 -= 0.1
            else:
                num_ck = randint(15, 30)
                num_ck2 = randint(30, 40)
                print(num_ck)
                iceice = False
                print(num_ck2)
    motion = cv2.absdiff(frame1, frame2) #หาผลต่างเพื่อจะให้รู้ว่ามีอะไรขยับไหม
    gray = cv2.cvtColor(motion, cv2.COLOR_BGR2GRAY) #แปลงรูปหรือวีดีโอให้เป็นขาวดำ
    blur = cv2.GaussianBlur(gray, (5,5), 0) #เบลอเพื่อให้ได้พื้นที่เพิ่มขึ้น
    thresh, result = cv2.threshold(blur, 15, 255, cv2.THRESH_BINARY) #แปลงข้อมูลให้ขาวดำอยู่ในอยู่รูปของไบนารี่
    dilation = cv2.dilate(result, None, iterations=3) #ขยายพิ้นที่อีกรอบ
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) #หาเส้นตอนทัวร์
    #วาดสีเหลี่ยมในสิ่งที่กำลังขยับ

    for con_ck in contours:
        (x, y, w, h) = cv2.boundingRect(con_ck) 
        if cv2.contourArea(con_ck) > 1000 and iceice == True and score < 1000:
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)
            boxbox = cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)
            box_ck = True
        else:
            if cv2.contourArea(con_ck) > 10000 and box_ck != True:
                if score <=1000:
                    cv2.putText(frame1, str(score), (450, 450), cv2.FONT_HERSHEY_COMPLEX, 2.5, (0, 255, 0), cv2.LINE_4)
                    score += 1
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)
                boxbox = cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Squid Game", frame1) #แสดงรูป    
    frame1 = frame2
    check , frame2 = cap.read()
    if box_ck == True and score < 1000:
        cv2.putText(frame1, "YOU DIE", (150, 100), cv2.FONT_HERSHEY_COMPLEX, 2.5, (0, 0, 255), cv2.LINE_4)
        cv2.putText(frame1, "Press 'q' to exit the game.", (100, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), cv2.LINE_4)
        die = True
    if score >= 1000 and box_ck != True:
        cv2.putText(frame1, "YOU Win", (150, 100), cv2.FONT_HERSHEY_COMPLEX, 2.5, (0, 255, 0), cv2.LINE_4)
        die = True
    if cv2.waitKey(1) & 0xFF == ord("q"): #ถ้าปุ่มกดนี้แล้วจะปิดกล้อง
        break

cap.release()
cv2.destroyAllWindows()