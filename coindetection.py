import cv2
import numpy as np

img = cv2.imread("data/capstone_coins.png")
output = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7,7), 1.5)

def detect_circles(input_img):
    circles = cv2.HoughCircles(input_img, cv2.HOUGH_GRADIENT, 1, 175, param1=50, param2=30, minRadius=30, maxRadius=200)
    return np.uint16(np.around(circles))

def detect_material(input_img, x, y, box_size):
    mean_brightness = np.mean(input_img[(y-box_size):(y+box_size), (x-box_size):(x+box_size)])
    if mean_brightness >= 140:
        c_mat = "silver" 
    else:
        c_mat ="copper"
    return c_mat


def get_coin_value(c_radius, c_mat):
    # identified coin no 7 as a 2p-coin.
    # 2p is usually 25.9 mm in diameter. Detected size = 82 => 82*2/25.9 = 6.33
    caf = 6.33
    if c_radius*2 / caf <= 22:
        if c_mat == "copper":
            return "p1"
        elif c_mat == "silver":
            return "p5"
    else:
        if c_mat == "copper":
            return "p2"
        elif c_mat == "silver":
            return "p10"
        





detected_circles = detect_circles(gray)

# visualize results:
count = 1
for (x, y, r) in detected_circles[0, :]:
    cv2.circle(output, (x, y), r, (0, 255, 0), 3)
    cv2.circle(output, (x, y), 2, (0, 0, 255), 5)
    c_mat = detect_material(gray, x, y, 15)
    c_value = get_coin_value(r, c_mat)
    cv2.putText(output,f"c:{count}/v:{c_value}",(x,y), cv2.FONT_ITALIC, fontScale= 1, color = (255, 0, 0), thickness = 2)
    count += 1

cv2.imshow("output", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
