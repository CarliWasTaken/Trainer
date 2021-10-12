import cv2
import numpy as np

HSV_LOWER = [40, 0, 80]
HSV_UPPER = [180, 150, 225]

def get_data_point():
    # Get image from camera
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()

    # Process image
    image = process_image_Mask(frame)
    image = draw_lines(image)

    # Get steering angle and speed
    angle = 0
    speed = 0

    # Put frame, speed and angle together
    data_point = np.array([image, speed, angle])

    return data_point



# Implementierts de methode
#TODO: compress image

def crop_image(image):
    h, w, c = image.shape
    crop_img = image[int((h/3)*2):h, 0:w]
    return crop_img

def process_image_Canny(image):
    crop_img = crop_image(image)
    gray_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray_img,(kernel_size, kernel_size),0)

    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(crop_img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)

    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_image,(x1,y1),(x2,y2),(255,255,255),5)

    image = line_image
    return image

def process_image_Mask(image):
    crop_img = crop_image(image)
    
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    blur = cv2.medianBlur(gray, 5)
    lower = np.array(HSV_LOWER, dtype="uint8")
    upper = np.array(HSV_UPPER, dtype="uint8")
    mask = cv2.inRange(blur, lower, upper)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cv2.fillPoly(mask, cnts, (255,255,255))

    return mask

def draw_lines(img):
    h, w, c = img.shape

    for i in range(3):
        start_point = (0, int(((h-60)/2)*i)+30)
        end_point = (w, int(((h-60)/2)*i)+30)
        color = (255, 255, 255)
        thickness = 3

        img = cv2.line(img, start_point, end_point, color, thickness)

    return img

if __name__ == "__main__":
    get_data_point()