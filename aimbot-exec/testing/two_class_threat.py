from cv2 import line


def threat_handling(frame, threat_alist, recoil_ctrl, frame_height, frame_width):
    x0, y0, fire_range, fire_pos, fire_close, fire_ok = 0, 0, 0, 0, 0, 0
    if len(threat_alist):
        threat_alist.sort(key=lambda x:x[0])
        x_tht, y_tht, w_tht, h_tht = threat_alist[0][1]

        # 指向距离最近威胁的位移(class0为头部,class1为身体)
        x0 = x_tht + (w_tht - frame_width) / 2
        if h_tht > w_tht:  # and threat_alist[0][2]
            y1 = y_tht + h_tht / 6 - frame_height / 2  # 爆头优先
            y2 = y_tht + h_tht / 3 - frame_height / 2  # 击中优先
            fire_close = (1 if frame_width / w_tht <= 8 else 0)
            if abs(y1) <= abs(y2) or fire_close:
                y0 = y1
                fire_range = w_tht / 6
                fire_pos = 1
            else:
                y0 = y2
                fire_range = w_tht / 4
                fire_pos = 2
        else:
            y0 = y_tht + (h_tht - frame_height) / 2
            fire_range = min(w_tht, h_tht) / 2
            fire_pos = 0

        # 查看是否已经指向目标
        if 1/4 * w_tht > abs(x0) and 2/5 * h_tht > abs(y0):
            fire_ok = 1

        y0 += recoil_ctrl
        xpos, ypos = x0 + frame_width / 2, y0 + frame_height / 2
        line(frame, (frame_width // 2, frame_height // 2), (int(xpos), int(ypos)), (0, 0, 255), 2)

    return x0, y0, fire_range, fire_pos, fire_close, fire_ok, frame
