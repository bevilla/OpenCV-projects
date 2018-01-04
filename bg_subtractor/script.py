#!/usr/bin/env python

# CHECK IF SCRIPT IS RUNNING INSIDE VENV
import sys
if not hasattr(sys, 'real_prefix'):
    raise(Exception('script isn\'t running inside a virtualenv\nHave you runned \'source venv/bin/activate\'?'))

import cv2
import numpy as np
import argparse

class BGSubtract:

    def get_next_image(self):
        raise Exception('get_next_image not implemented')

    def start(self, bg):
        key = 0
        frame_number = 1
        mog = cv2.createBackgroundSubtractorMOG2(varThreshold=75)
        while not (key is 27):
            im = self.get_next_image()
            if im is None:
                break

            # implement background subtract using mog
            mask = mog.apply(im)
            cv2.imshow('mask', mask)
            fg = im * ((mask / 255)[:,:,None].astype(im.dtype))
            bg2 = bg * ((~mask / 255)[:,:,None].astype(bg.dtype))
            cv2.imshow('final', fg + bg2)

            # display
            cv2.rectangle(im, (10, 2), (75, 20), (255, 255, 255), -1)
            cv2.putText(im, str(frame_number), (15, 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
            cv2.imshow('original frames', im)
            key = cv2.waitKey(30)

            frame_number += 1

class BGSubtractImage(BGSubtract):

    def __init__(self, filepath):
        self.filepath = filepath

    def get_next_image(self):
        array = self.filepath.split('/')
        filename = array[-1].split('.')
        filename[0] = str(int(filename[0]) + 1)
        array[-1] = '.'.join(filename)
        self.filepath = '/'.join(array)
        return cv2.imread(self.filepath)

class BGSubtractVideo(BGSubtract):

    def __init__(self, filepath):
        self.video = cv2.VideoCapture(filepath)

    def get_next_image(self):
        ret, im = self.video.read()
        return cv2.resize(im, (640, 480))

class BGSubtractWebcam(BGSubtract):

    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def get_next_image(self):
        ret, im = self.video.read()
        return cv2.resize(im, (640, 480))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--images',
                        type=str,
                        help='the image files to use instead of webcam')
    parser.add_argument('--video',
                        type=str,
                        help='the video to use instead of webcam')
    parser.add_argument('bg_filename', help='background file name (image)')
    args = parser.parse_args()
    bg = cv2.resize(cv2.imread(args.bg_filename), (640, 480))
    if not (args.images is None):
        BGSubtractImage(args.images).start(bg)
    elif not (args.video is None):
        BGSubtractVideo(args.video).start(bg)
    else:
        BGSubtractWebcam().start(bg)
