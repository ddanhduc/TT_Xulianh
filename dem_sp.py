from tracker import *
import cv2
import numpy as np


#TẠO ĐỐI TƯỢNG TRACKER lớp DistTracker
tracker = DistTracker()

cap = cv2.VideoCapture("C:\\Users\\20161\\Downloads\\sanpham.mp4")


kernalOp = np.ones((3,3),np.uint8)
kernalCl = np.ones((11,11),np.uint8)
fgbg=cv2.createBackgroundSubtractorMOG2(detectShadows=True)
kernal_e = np.ones((5,5),np.uint8)

while(True):
    ret,frame=cap.read()
    if not ret:
        break

    #chỉnh tương phản 
    normalized_frame = cv2.normalize(frame, None, alpha=0, beta=200, norm_type=cv2.NORM_MINMAX)
    
    #xác định vùng cần xử lý 
    roi = normalized_frame[50:450,100:600]
    
    #chuyển thành ảnh nhị phân 
    fgmask  =  fgbg.apply(roi)
    ret, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    
    #xử lý viền 
    mask1 = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernalOp)
    mask2 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernalCl)
    e_img = cv2.erode(mask2, kernal_e)
    
    #tìm tất cả đường viền trong frame 
    contours,_ = cv2.findContours(e_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    detections = []

    for cnt in contours:
            area = cv2.contourArea(cnt)
            if 13000 > area > 3000:#diện tích viền trong khoảng được lưu lại 
                x, y, w, h = cv2.boundingRect(cnt)
                detections.append([x, y, w, h])

    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x,y,w,h,id = box_id
        #vẽ hình và đánh id 
        cv2.putText(roi,str(id),(x,y-15), cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # đếm 
        if (tracker.f[id] == 1 ):
            count=tracker.capture(id)


    cv2.line(roi, (0, 200), (500, 200), (0, 0, 255), 2)

    cv2.imshow("DEM SAN PHAM",roi)
    key=cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()

print("số sản phẩm có trên băng tải: ",str(count))

