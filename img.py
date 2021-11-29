from pathlib import Path

# pip install imgaug, imagecorruptions, imageio

import imageio
import imgaug as ia
import imgaug.augmenters as iaa

ia.seed(98765)

def get_iaa_name(func):
    # return str(func).split('.')[-1][:-2].lower()
    return str(func).split('(')[0]

filters = [
    ["cartoon", 5, iaa.Cartoon()],
    ["voronoiRegGrid", 5, iaa.RegularGridVoronoi((10, 30))],
    ["voronoiUniform", 5, iaa.UniformVoronoi((100, 500))],
    ["kmeans", 5, iaa.KMeansColorQuantization(n_colors=(4, 16))],
    ["superpixels", 5, iaa.Superpixels(p_replace=(0.1, 1.0), n_segments=(16, 128))],

    ["rotate0_10", 5, iaa.Affine(rotate=(-10, 10))],
    ["rotate90_10", 5, iaa.Affine(rotate=(80, 100))],
    ["rotate-90_10", 5, iaa.Affine(rotate=(-100, -80))],

    ["speckle", 3, iaa.imgcorruptlike.SpeckleNoise(severity=(1, 3))], 
    ["gaussian", 3, iaa.imgcorruptlike.GaussianNoise(severity=(1, 3))],
    ["snow", 3, iaa.Snowflakes(flake_size=(0.7, 0.95), speed=(0.001, 0.03))],
    ["rain", 3, iaa.Rain(drop_size=(0.10, 0.20))],

    ["fliplr", 1, iaa.Fliplr()],
    ["flipud", 1, iaa.Flipud()],

    ["cannyEdge", 7, iaa.Canny(alpha=(0.0, 0.5))],
    ["scale", 7, iaa.Affine(scale=(0.75, 1.25))],
    ["shear", 7, iaa.Affine(shear=(-30, 30))],
]

filters_severity = [
    ["jpeg", 1, iaa.imgcorruptlike.JpegCompression],
    ["saturate", 1, iaa.imgcorruptlike.Saturate],
    ["defocus", 1, iaa.imgcorruptlike.DefocusBlur],
]


master = imageio.imread("image_db/" + "orig.jpg")
# ia.imshow(master)

for test in filters:
    print("Processing " + test[0] + ": ", end='')
    Path("image_db/" + test[0]).mkdir(parents=True, exist_ok=True)
    seq = iaa.Sequential([test[2]])
    
    for i in range(0, test[1]):
        imageio.imwrite("image_db/" + test[0] + '/' + chr(i+97) + ".jpg", seq.augment_image(master))
        print('.', end='')
    print('')

for test in filters_severity:
    print("Processing " + test[0] + ": ", end='')
    Path("image_db/" + test[0]).mkdir(parents=True, exist_ok=True)
    
    for i in range(0, 5):
        seq = iaa.Sequential([test[2](severity=i+1)])
        imageio.imwrite("image_db/" + test[0] + '/' + chr(i+97) + ".jpg", seq.augment_image(master))
        print('.', end='')
    print('')







