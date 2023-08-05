import cv2
import math
import numpy as np


class DistTracker:

    def __init__(self):
        # CHỨA ĐIỂM TÂM CỦA VẬT 
        self.center_points = {}
        #ID VẬT 0->N
        self.id_count = 0
        #MẢNG KIỂM TRA ID NÀY ĐÃ ĐƯỢC ĐẾM HAY CHƯA
        self.capf=np.zeros(1000)
        #BIẾN ĐẾM SP
        self.count = 0
        #MẢNG KIỂM TRA QUA LINE HAY CHƯA 
        self.f = np.zeros(1000)

    def update(self, objects_rect):
        objects_bbs_ids = []

        # LẤY ĐIỂM TRUNG TÂM CỦA VẬT 
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # KIỂM TRA XEM VẬT ĐÃ ĐƯỢC ĐÁNH ID CHƯA 
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                if dist < 100:
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
           
           #ĐÁNH DẤU ĐỂ ĐẾM VẬT 
                    if (y > 200):# QUA LINE  
                        self.f[id] = 1

            # NẾU LÀ VẬT CHƯA ĐƯỢC ĐÁNH ID 
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # TẠO ID MỚI CHO VẬT 
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center
        self.center_points = new_center_points.copy()
        return objects_bbs_ids
    
    def capture(self, id):
        if (self.capf[id] == 0):
            self.f[id] = 0
            self.capf[id] = 1
            self.count += 1
        return self.count

