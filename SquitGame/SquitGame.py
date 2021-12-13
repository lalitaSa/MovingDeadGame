import cv2

cap = cv2.VideoCapture(0) #ระบุหมายเลขกล้อง
check , frame1 = cap.read() #รับภาพจากกล้องเป็นframe หาคอนทัวร์
check , frame2 = cap.read() #รับภาพจากกล้องเป็นframe หาข้อมูล

while (cap.isOpened()): #ตั้งเพื่อให้มันรับภาพอยู่ตลอดเวลาแล้วแสดงแบบเรียลไทม์
    if check == True:
        motion = cv2.absdiff(frame1, frame2) #หาผลต่างเพื่อจะให้รู้ว่ามีอะไรขยับไหม
        gray = cv2.cvtColor(motion, cv2.COLOR_BGR2GRAY) #แปลงรูปหรือวีดีโอให้เป็นขาวดำ
        blur = cv2.GaussianBlur(gray, (5,5), 0) #เบลอเพื่อให้ได้พื้นที่เพิ่มขึ้น
        thresh, result = cv2.threshold(blur, 15, 255, cv2.THRESH_BINARY) #แปลงข้อมูลให้ขาวดำอยู่ในอยู่รูปของไบนารี่
        dilation = cv2.dilate(result, None, iterations=3) #ขยายพิ้นที่อีกรอบ
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) #หาเส้นตอนทัวร์
        #วาดสีเหลี่ยมในสิ่งที่กำลังขยับ       
    for con_ck in contours:
        (x, y, w, h) = cv2.boundingRect(con_ck) 
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)
        boxbox = cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Squid Game", frame1) #แสดงรูปภาพ    
    frame1 = frame2
    check , frame2 = cap.read()
    if cv2.waitKey(1) & 0xFF == ord("q"): #ถ้าปุ่มกดนี้แล้วจะปิดกล้อง
        break
cap.release()
cv2.destroyAllWindows()
