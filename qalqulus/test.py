
import argparse, cv2 # image recognition stuff

# load the input image and convert it to grayscale
image = cv2.cvtColor(cv2.imread('resources/leithold-11.jpg'), cv2.COLOR_BGR2GRAY)
template = cv2.cvtColor(cv2.imread('resources/leithold-n-8.png'), cv2.COLOR_BGR2GRAY)

img = image.copy()
method = cv2.TM_SQDIFF_NORMED

# Apply template Matching
res = cv2.matchTemplate(image,template,method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
print(min_val, max_val, min_loc, max_loc)

top_left = min_loc
bottom_right = (top_left[0] + 64, top_left[1] + 32)

cv2.rectangle(img,top_left, bottom_right, 128, 2)
cv2.imwrite('out.png',img)
