# import pandas as pd
# import progressbar as pbar
# import cv2
# import matplotlib.pyplot as plt

# split = "train"

# file = pd.read_csv('./bbox_label_%s.csv' % (split), header=None)
# contours_area_list = []
# bar = pbar.ProgressBar(max_value=len(file))
# for i in range(len(file)):
#     dat = file.iloc[i]
#     img = cv2.imread('./pavementsDataset/mask/%s/%s.png' % (split, dat[0]), cv2.IMREAD_GRAYSCALE)
#     _, thresh = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     for contour in contours:
#         if cv2.contourArea(contour) < 20000:
#             contours_area_list.append(cv2.contourArea(contour))

#     bar.update(i)

# print("Length: ", len(contours_area_list))

# plt.hist(contours_area_list, bins=500)
# plt.show()
# plt.savefig('./hist.png')
# plt.close()

import pandas as pd
import progressbar as pbar
import cv2

split = "val"

class_dic = {'pothole': 0,
             'lateral_crack': 1,
             'longitudinal_crack': 2,
             'alligator_crack': 3,
             'repair_area': 4,
             'rut': 5}
file = pd.read_csv('./bbox_label_%s.csv' % (split), header=None)
# contours_area_list = []
bar = pbar.ProgressBar(max_value=len(file))
for i in range(len(file)):
    dat = file.iloc[i]
    classname = dat[5]
    x1 = int(dat[1])
    y1 = int(dat[2])
    x2 = int(dat[3])
    y2 = int(dat[4])

    img = cv2.imread('./pavementsDataset/mask/%s/%s.png' % (split, dat[0]), cv2.IMREAD_GRAYSCALE)
    roi = img[y1:y2, x1:x2]

    imgh, imgw = img.shape
    _, thresh = cv2.threshold(roi, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    polygons = []
    with open("./mask_labels/%s/%s.txt" % (split, dat[0]), "a+") as f:
        f.write("%s " % str(class_dic[classname]))

        for contour in contours:
            if len(contour) >= 20:
                contour = contour.flatten().tolist()
                contour_adjusted = [contour[i] + x1 if i % 2 == 0 else
                                    contour[i] + y1 for i in range(len(contour))]

                # epsilon = 0.01 * cv2.arcLength(contour_adjusted, True)
                # approx = cv2.approxPolyDP(contour_adjusted, epsilon, True)
                # contour_adjusted = approx.flatten().tolist()

        for j in range(0, len(contour_adjusted), 2):
            x1_norm = contour_adjusted[j] / imgw
            y1_norm = contour_adjusted[j + 1] / imgh
            f.write("%f %f " % (x1_norm, y1_norm))
        f.write('\n')

    bar.update(i)
