from typing import Any
import cv2 as cv
import numpy as np

blur_value: int = 5
contour_size: int = 1000

flattenMaxWidth: int = 300
flattenMaxHeight: int = 400

def detectCard(img: np.ndarray) -> (tuple[np.ndarray, None] | tuple[np.ndarray, list[np.ndarray]]):
    # remove black bars from the frame
    img = remove_black_bars(img)

    # convert to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # blur image6
    blur = cv.GaussianBlur(gray, (blur_value, blur_value), 0)

    # canny edge detection
    canny = cv.Canny(blur, 50, 150)

    # remove noise from the image using dilation and erosion
    kernel = np.ones((5, 5), np.uint8)
    dilate = cv.dilate(canny, kernel, iterations=3)
    erode = cv.erode(dilate, kernel, iterations=2)

    # find contours and filter out smaller ones
    contours, _ = cv.findContours(erode, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = [c for c in contours if cv.contourArea(c) > 1000 and not np.array_equal(c[0], c[-1])]
    contours = sorted(contours, key=cv.contourArea, reverse=True)[:1]
    # make sure the contour is a quadrilateral  (4 corners)
    contours = [c for c in contours if len(cv.approxPolyDP(c, 0.01 * cv.arcLength(c, True), True)) == 4]

    if len(contours) == 0:
        return img, None

    # draw contours
    detectedImg = img.copy()
    cv.drawContours(detectedImg, contours, -1, (255, 0, 0), 2)

    # approximate the corner points of the contours if it has 4 corners
    approx_corners = [cv.approxPolyDP(c, 0.01 * cv.arcLength(c, True), True) for c in contours]
    approx_corners = sorted(approx_corners, key=cv.contourArea, reverse=True)[:1]
    
    if len(approx_corners) == 0:
        return img, None

    # draw circles at approximated corner points
    index = 0;
    color = [(0, 0, 255), (255, 255, 255), (0, 255, 0), (0, 255, 255)]
    for c in approx_corners:
        for p in c:
            cv.circle(detectedImg, (p[0][0], p[0][1]), 10, color[index % len(color)], -1)
            index = index + 1
    
    return detectedImg, approx_corners

def transformCard(img: np.ndarray, approx_corners: list[np.ndarray]) -> np.ndarray:
    img = remove_black_bars(img)
    # using the approximated corner points, flatten the image into a top-down view of the card
    # first, find the top-left and bottom-right corner points
    top_left = approx_corners[0][0][0]
    bottom_right = approx_corners[0][0][0]
    for c in approx_corners:
        for p in c:
            if p[0][0] + p[0][1] < top_left[0] + top_left[1]:
                top_left = p[0]
            if p[0][0] + p[0][1] > bottom_right[0] + bottom_right[1]:
                bottom_right = p[0]

    # next, find the top-right and bottom-left corner points
    top_right = approx_corners[0][0][0]
    bottom_left = approx_corners[0][0][0]
    for c in approx_corners:
        for p in c:
            if p[0][0] - p[0][1] > top_right[0] - top_right[1]:
                top_right = p[0]
            if p[0][0] - p[0][1] < bottom_left[0] - bottom_left[1]:
                bottom_left = p[0]

    # create a matrix of the corner points
    pts1 = np.float32([top_left, top_right, bottom_left, bottom_right])
    # create a matrix of the desired corner points
    pts2 = np.float32([[0, 0], [flattenMaxWidth, 0], [0, flattenMaxHeight], [flattenMaxWidth, flattenMaxHeight]])

    # get the transformation matrix
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    # apply the transformation matrix to the image
    transformedImg = cv.warpPerspective(img, matrix, (flattenMaxWidth, flattenMaxHeight))
    return transformedImg

def remove_black_bars(img) -> np.ndarray:
    # Convert the image to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Threshold the image to create a binary mask
    _, mask = cv.threshold(gray, 1, 255, cv.THRESH_BINARY)

    # Find the contours of the mask
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return img

    # Find the bounding box of the contours
    x, y, w, h = cv.boundingRect(contours[0])

    # Crop the image to the bounding box
    cropped = img[y:y+h, x:x+w]

    return cropped