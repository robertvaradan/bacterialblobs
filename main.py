import os.path
import time

import matplotlib.pyplot as plt
from imageio import imread
from skimage.color import rgb2gray
from skimage.feature import blob_doh
from os import listdir
from os.path import isfile, join
import numpy
from math import pi

while True:

    print("Available images:")

    images = [f for f in listdir('./extracted') if isfile(join('./extracted', f))]

    for image in images:
        print("-", image)
    print ("- all")

    input_image_name = input("Input image name (no extension): ")
    input_images = []
    if str.lower(input_image_name) == 'all':
        input_images += [str.lower(image_caps[:-4]) for image_caps in images]
    else:
        input_images += [str.lower(input_image_name)]

    image_bitmaps = []

    for input_image in input_images:
        filename = './extracted/%s.png' % input_image

        if not os.path.exists(filename):
            print("ERROR: Bad filename \"%s\". Try again:" % filename)
            continue

        image = imread(filename)
        image_bitmaps += [(image, input_image)]

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

    index = 1
    blobs_list = []
    size = 22
    linewidth = 2
    fontsize = 'xx-large'

    if len(image_bitmaps) > 1:
        size = 88
        linewidth = 1
        fontsize = 'x-small'

    for image_bitmap, image_name in image_bitmaps:
        print("Generating blobs using Determinant of Hessian algorithm... image %d/%d" % (index, len(image_bitmaps)))

        image_gray = rgb2gray(image_bitmap)

        # Use the Determinant of Hessian method to find the bright spots in the image
        blobs = blob_doh(image_gray, min_sigma=min_sigma, max_sigma=max_sigma, threshold=threshold / 1000)
        print("Done. Found %d blobs" % len(blobs))
        title = image_name

        blobs_list += [(title, blobs, image_bitmap)]
        index += 1

    # 2200x2200 canvas or 4400x4400 for 9 images
    fig = plt.figure(figsize=(size, size))
    color = 'white'

    plot_index = 1

    for pair in blobs_list:
        ax = fig.add_subplot(3 if len(blobs_list) > 1 else 1, ((len(blobs_list) - 1) // 3) + 1, plot_index)
        ax.set_title(pair[0], fontsize=fontsize)
        plt.imshow(pair[2])
        ax.set_axis_off()
        total_blob_volume = 0

        # Draw a circle on screen around the blobs
        for blob in pair[1]:
            y, x, r = blob

            # Sum the squared radii
            total_blob_volume += r**2
            c = plt.Circle((x, y), r, color=color, linewidth=linewidth, fill=False)
            ax.add_patch(c)

        # Multiply the squared radii by pi to get the area in pixels^2
        total_blob_volume *= pi
        # Convert from sq. pixels to sq. inches
        total_blob_volume /= 1000
        total_blob_volume = round(total_blob_volume, 3)
        count_text = "Count: " + str(len(pair[1]))
        total_volume_text = "Detected Area: " + str(total_blob_volume) + " inches^2"
        min_sigma_text = "Min Sigma: " + str(min_sigma)
        max_sigma_text = "Max Sigma: " + str(max_sigma)
        threshold_text = "Blob Threshold: " + str(threshold)

        plt.text(x=20, y=600, fontsize=fontsize, color=color, s=count_text)
        plt.text(x=20, y=620, fontsize=fontsize, color=color, s=total_volume_text)
        plt.text(x=20, y=640, fontsize=fontsize, color=color, s=min_sigma_text)
        plt.text(x=20, y=660, fontsize=fontsize, color=color, s=max_sigma_text)
        plt.text(x=20, y=680, fontsize=fontsize, color=color, s=threshold_text)

        plot_index += 1

    if size == 22:
        plt.tight_layout()
    plt.show()

    should_save = input("Save? y/n\n")
    if should_save == 'y':
        timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
        savepath = './resultant/%s_at_%s' % (input_image_name, timestr)
        fig.savefig(savepath, dpi=100)
        print("Saved to", savepath)
    print("*** The program will now restart. ***")
