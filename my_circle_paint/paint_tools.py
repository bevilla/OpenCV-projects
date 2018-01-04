import cv2
import time

class PointItem:

    def __init__(self, coords, thickness, time_start):
        self.coords = coords
        self.thickness = thickness
        self.time_start = time_start

    def circle_to_item(circle):
        return PointItem((circle[0], circle[1]), int((circle[2] - 40)), time.time())

class PaintTools:

    items = []
    timeout = 1

    def add_coords(self, circles):
        if not (circles is None):
            for circle in circles:
                self.items.append(PointItem.circle_to_item(circle))

    def draw(self, im):
        im2 = im.copy()
        for i in range(len(self.items) - 1):
            pt1 = self.items[i]
            pt2 = self.items[i + 1]
            cv2.line(im2, pt1.coords, pt2.coords, (0, 0, 255), pt1.thickness)
        self.update()
        return im2
        #return cv2.addWeighted(im2, 0.5, im, 0.5, 0.0)

    def update(self):
        i = 0
        now = time.time()
        for item in self.items:
            if now - item.time_start < self.timeout:
                break
            i += 1
        self.items = self.items[i:]

    def clear(self):
        self.items = []
