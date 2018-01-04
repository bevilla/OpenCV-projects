#!/usr/bin/env python

import cv2
import circle_detect as cd
import paint_tools as pt

def blur_ksize_callback(value):
    value = int(value)
    value = value * 2 + 1
    cd.BLUR_KSIZE = (value, value)

def blur_sigma_callback(value):
    value = int(value)
    cd.BLUR_SIGMAX = value
    cd.BLUR_SIGMAY = value

def circle_param_callback(value, attr):
    value = int(value)
    if hasattr(cd, attr) and value > 0:
        setattr(cd, attr, int(value))

def init_gui(win_name, paint):
    cv2.createTrackbar('Blur ksize', win_name, 4, 20, blur_ksize_callback)
    cv2.createTrackbar('Blur sigma', win_name, 2, 10, blur_sigma_callback)
    cv2.createTrackbar('Circle dp', win_name, 2, 10, lambda v: circle_param_callback(v, 'CIRCLE_DP'))
    cv2.createTrackbar('Circle min dist', win_name, 4, 12, lambda v: circle_param_callback(v, 'CIRCLE_MINDIST_DIV'))
    cv2.createTrackbar('Circle canny', win_name, 200, 800, lambda v: circle_param_callback(v, 'CIRCLE_CANNY_THRESHOLD'))
    cv2.createTrackbar('Circle acc', win_name, 100, 800, lambda v: circle_param_callback(v, 'CIRCLE_ACC_THRESHOLD'))
    cv2.createTrackbar('Circle min radius', win_name, 40, 200, lambda v: circle_param_callback(v, 'CIRCLE_MIN_RADIUS'))
    cv2.createTrackbar('Circle max radius', win_name, 90, 400, lambda v: circle_param_callback(v, 'CIRCLE_MAX_RADIUS'))
    cv2.createTrackbar('Timeout', win_name, 1, 10, lambda v: setattr(paint, 'timeout', int(v)))

if __name__ == '__main__':
    video = cv2.VideoCapture(0)
    ret, im = video.read()
    if not ret:
        print('Error: cannot read video')
        exit(-1)
    win_name = 'my_circle_paint'
    win2_name = 'im2'
    #cv2.namedWindow(win2_name)
    cv2.namedWindow(win_name)
    paint = pt.PaintTools()
    init_gui(win_name, paint)
    #out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
    while video.isOpened() and not im.data is None and ret:
        im = cv2.flip(im, 1)
        im2 = cd.preprocess_image(im)
        paint.add_coords(cd.detect_circles(im2))
        im = paint.draw(im)
        #cv2.imshow(win2_name, im2)
        cv2.imshow(win_name, im)
        #out.write(im)
        if cv2.waitKey(16) == 27:
            break
        ret, im = video.read()
    video.release()
    #out.release()
    cv2.destroyAllWindows()
