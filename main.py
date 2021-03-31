import os.path
import time

import matplotlib.pyplot as plt
from imageio import imread
from skimage.color import rgb2gray
from skimage.feature import blob_doh
from os import listdir
from os.path import isfile, join
from math import pi

while True:

    print("Available images:")

    images = [f for f in listdir('./extracted') if isfile(join('./extracted', f))]

    for image in images:
        print("-", image)

    input_image = input("Input image name (no extension): ")
    input_image = str.lower(input_image)
    filename = './extracted/%s.png' % input_image

    if not os.path.exists(filename):
        print("ERROR: Bad filename. Try again:")
        continue

    image = imread(filename)
    image_gray = rgb2gray(image)

    min_sigma = 5
    try:
        min_sigma = int(input("Input min_sigma (min blob size): "))
    except ValueError:
        pass

    print("Using min_sigma %d" % min_sigma)

    max_sigma = 80
    try:
        max_sigma = int(input("Input max_sigma (max blob size): "))
    except ValueError:
        pass

    print("Using min_sigma %d" % max_sigma)

    threshold = 5
    try:
        threshold = int(input("Input threshold (prominence of blobs): "))
    except ValueError:
        pass

    print("Using threshold %d" % threshold)

    print("Generating blobs using Determinant of Hessian algorithm...")

    # Use the Determinant of Hessian method to find the bright spots in the image
    blobs = blob_doh(image_gray, min_sigma=min_sigma, max_sigma=max_sigma, threshold=threshold / 1000)
    print("Done. Found %d blobs" % len(blobs))
    color = 'white'
    title = input_image

    # 2200x2200 canvas
    fig = plt.figure(figsize=(22, 22))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(title, fontsize='xx-large')
    plt.imshow(image)
    ax.set_axis_off()
    total_blob_volume = 0

    # Draw a circle on screen around the blobs
    for blob in blobs:
        y, x, r = blob

        # Sum the squared radii
        total_blob_volume += r**2
        c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
        ax.add_patch(c)

    # Multiply the squared radii by pi to get the area in pixels²
    total_blob_volume *= pi
    # Convert from sq. pixels to sq. inches
    total_blob_volume /= 1000
    total_blob_volume = round(total_blob_volume, 3)
    count_text = "Count: " + str(len(blobs))
    total_volume_text = "Detected Area: " + str(total_blob_volume) + " inches²"
    min_sigma_text = "Min Sigma: " + str(min_sigma)
    max_sigma_text = "Max Sigma: " + str(max_sigma)
    threshold_text = "Blob Threshold: " + str(threshold)

    plt.text(x=20, y=600, fontsize='xx-large', color=color, s=count_text)
    plt.text(x=20, y=620, fontsize='xx-large', color=color, s=total_volume_text)
    plt.text(x=20, y=640, fontsize='xx-large', color=color, s=min_sigma_text)
    plt.text(x=20, y=660, fontsize='xx-large', color=color, s=max_sigma_text)
    plt.text(x=20, y=680, fontsize='xx-large', color=color, s=threshold_text)

    plt.tight_layout()
    plt.show()

    should_save = input("Save? y/n\n")
    if should_save == 'y':
        timestr = time.strftime("%Y-%m-%d-%H:%M:%S")
        savepath = './resultant/%s at %s' % (input_image, timestr)
        fig.savefig(savepath, dpi=100)
        print("Saved to", savepath)
    print("*** The program will now restart. ***")
