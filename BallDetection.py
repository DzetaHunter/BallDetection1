import numpy as np
import cv2

if __name__ == '__main__':
    def nothing(*arg):
        pass
 
cap = cv2.VideoCapture('20190109_193309_001.mp4')
winname = 'VideoWindow'

Write_fps = 30.0
Write_size = (1920, 1080)

#cv2.CAP_PROP_FPS   cv2.VideoWriter_fourcc(*'DIVX')'i', 'Y', 'U', 'V'
#Writer = cv2.VideoWriter("test.avi", -1, Write_fps, Write_size)
#Writer = cv2.VideoWriter("test.avi", cv2.VideoWriter_fourcc('X', '2', '6', '4'), Write_fps, Write_size)
#Writer = cv2.VideoWriter("test.avi", cv2.VideoWriter_fourcc('i', 'Y', 'U', 'V'), Write_fps, Write_size)
#Writer = cv2.VideoWriter("test.avi", cv2.VideoWriter_fourcc(*'DIVX'), Write_fps, Write_size)
Writer = cv2.VideoWriter('test.avi',-1, Write_fps, Write_size)

cv2.namedWindow(winname,cv2.WINDOW_NORMAL)
cv2.namedWindow( "settings" ) # создаем окно настроек

# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
crange = [0,0,0, 0,0,0]

cv2.resizeWindow(winname,1280,720)

ret, frame = cap.read()

hsv_min = np.array((53, 0, 0), np.uint8)
hsv_max = np.array((83, 255, 255), np.uint8)

points = list()

while(ret):
    ret, frame = cap.read()       

    if ret == False:
        continue

    #Writer.write(frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV )
 
    # считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    # формируем начальный и конечный цвет фильтра
    #h_min = np.array((h1, s1, v1), np.uint8)
    #h_max = np.array((h2, s2, v2), np.uint8)

    h_min = np.array((33, 37, 157), np.uint8)
    h_max = np.array((112, 255, 255), np.uint8)

    colfil = cv2.inRange(hsv, h_min, h_max)
    
    #Writer.write(colfil)

    kont = cv2.Canny(colfil,0,255)

    Writer.write(kont)

    krugi = cv2.HoughCircles(kont, cv2.HOUGH_GRADIENT, 1, 20, param1=13, param2=15, minRadius=0, maxRadius=40)

    if krugi is not None:
        krugi = np.uint16(np.around(krugi))

        #Количиство распознанных кругов
        CirNum = len(krugi[0])
        cv2.putText(frame,str(CirNum),(10,60), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255),2,cv2.LINE_AA)

        for krug in krugi[0,:]:
            xy = (krug[0],krug[1])

            if (xy[0] != 0) & (xy[1] !=0):
                points.append(xy)

            cv2.circle(frame,xy,krug[2],(0,255,0),2)

    #Массив кортежей  
    for (Xcor,Ycor) in points:
        if (Xcor != 0) & (Ycor != 0):
            cv2.circle(frame,(Xcor,Ycor),2,(255,0,0),2)

    cv2.imshow(winname,frame)

    #Writer.write(frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break
 
cap.release()
Writer.release()
cv2.destroyAllWindows()