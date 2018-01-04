import cv2

BLUR_KSIZE = (9, 9)
BLUR_SIGMAX = 2
BLUR_SIGMAY = 2

CIRCLE_DP = 2
CIRCLE_MINDIST_DIV = 4
CIRCLE_CANNY_THRESHOLD = 200
CIRCLE_ACC_THRESHOLD = 100
CIRCLE_MIN_RADIUS = 40
CIRCLE_MAX_RADIUS = 90

def preprocess_image(im):
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_blur = cv2.GaussianBlur(im_gray, BLUR_KSIZE, BLUR_SIGMAX, BLUR_SIGMAY)
    return im_blur

def detect_circles(im):
    circles = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT,
                               CIRCLE_DP,
                               im.shape[0] / CIRCLE_MINDIST_DIV,
                               CIRCLE_CANNY_THRESHOLD,
                               CIRCLE_ACC_THRESHOLD,
                               minRadius=CIRCLE_MIN_RADIUS,
                               maxRadius=CIRCLE_MAX_RADIUS)
    return None if circles is None else circles[0]
