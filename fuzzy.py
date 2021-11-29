import os
import sys
# import subprocess
import base64

from PIL import Image
import imagehash
# from imaeg_match.goldberg import ImageSignature
from perception import hashers
import perception
import photohash

images = []
master = 'image_db/orig.jpg'
HASH_SIZE = 32
HASH_SIZE = 8
if len(sys.argv) > 1:
    HASH_SIZE = int(sys.argv[1])

libs = {}
# lib_ref = {imagehash: [imagehash.average_hash, imagehash.crop_resistant_hash, imagehash.dhash, imagehash.whash, imagehash.colorhash, imagehash.phash]}
lib_ref = {
    imagehash:  [imagehash.average_hash, imagehash.dhash, imagehash.whash, imagehash.phash],
    # perception: [hashers.PHash(), hashers.DHash(), hashers.AverageHash(), hashers.MarrHildreth(), hashers.BlockMean(), hashers.WaveletHash(), hashers.ColorMoment()],
    perception: [hashers.PHash(), hashers.DHash(), hashers.AverageHash(), hashers.WaveletHash()],
    photohash:  [photohash.average_hash]
}

working_libs = [imagehash, perception, photohash]
working_libs = working_libs[0:1]

for files in os.walk("image_db"):
    # if not len(files[0]) > 1:
    #     continue
    for file in files[2]:
        filepath = files[0] + '/' + file
        images.append(filepath)

# temp1 = 0
# temp2 = 0

for img in images:
    pil_img = Image.open(img)
    # img = img[9:-4]
    for lib in working_libs:
        if lib not in libs:
            libs[lib] = {}
        for func in lib_ref[lib]:
            if func not in libs[lib]:
                libs[lib][func] = {}
            if lib == imagehash:
                libs[lib][func][img] = func(pil_img, hash_size=HASH_SIZE)
                # if not temp1:
                #     temp1 = 1
                #     print(str(func(pil_img, hash_size=8)))
            elif lib == perception:
                libs[lib][func][img] = func.compute(pil_img)
                # print(img, func.compute(img))
                # if not temp2:
                #     temp2 = 1
                #     print(str(base64.b64decode(func.compute(pil_img)).hex()))

# 8    16    8b ffefc0400040f002
# 16   64   32b fffffffffc7ff87ff0207020700000000000001800007600ff800ce02238008e
# 32  256  128b fffffffffffffffffffffffffffa7ffffff83ffffff03fff7fc03fff7f803d9c7f801c007f8018003f8008003f8008003f8608003f00000030000000000000000000000000000000010003ff000000000000000000c000001f7000007f1c00007fc70000dff380009df8f00080963c000e1e0f000a1a01c00000c0780010601e
with open("output.csv", 'w') as f:
    f.write("hash_diff,")
    f.write("image,")
    f.write("library,")
    f.write("function,")
    f.write("\n")
    with open("averages.csv", 'w') as f2:
        f2.write("hash_diff,")
        f2.write("image,")
        f2.write("library,")
        f2.write("function,")
        f2.write("\n")
        for lib in working_libs:
            library = str(lib).split()[1].strip("'")
            for func in libs[lib]:
                if lib == perception:
                    funcname = str(func).split('.')[-1].split()[0]
                elif lib == imagehash:
                    funcname = str(func).split()[1]
                for img in libs[lib][func]:
                    if img[9:-4] == 'orig':
                        continue
                    if lib == imagehash:
                        hash_diff = libs[lib][func][master] - libs[lib][func][img]
                    elif lib == perception:
                        hash_diff = lib_ref[perception][0].compute_distance(libs[lib][func][master], libs[lib][func][img])
                        # hash_diff = (1 - lib_ref[perception][0].compute_distance(libs[lib][func][master], libs[lib][func][img])) * 64
                    # print(library.rjust(14), '-', funcname.ljust(15), img[9:-4].ljust(16), str(hash_diff))
                    # print(img[9:-4].ljust(16), library.rjust(14), '-', funcname.ljust(15), str(hash_diff))
                    # print(str(hash_diff).ljust(4), img[9:-4].ljust(16), library.rjust(14), '-', funcname.ljust(15))
                    f.write(str(hash_diff) + ',')
                    f.write(img[9:-4] + ',')
                    f.write(library + ',')
                    f.write(funcname + ',')
                    f.write("\n")

            for func in libs[lib]:
                if lib == perception:
                    funcname = str(func).split('.')[-1].split()[0]
                elif lib == imagehash:
                    funcname = str(func).split()[1]
                # print(libs[lib][func].keys())
                # files = [file[9:-4] for file in list(libs[lib][func].keys())]
                files = list(libs[lib][func].keys())
                aug_types = {}
                for file in files:
                    if file[9:-4].split('/')[0] not in aug_types:
                        aug_types[file[9:-4].split('/')[0]] = []
                    aug_types[file[9:-4].split('/')[0]].append(file)
                # print(aug_types)
                for aug in aug_types:
                    sum = 0
                    for file in aug_types[aug]:
                        if lib == imagehash:
                            hash_diff = libs[lib][func][master] - libs[lib][func][file]
                        elif lib == perception:
                            hash_diff = lib_ref[perception][0].compute_distance(libs[lib][func][master], libs[lib][func][file])
                        sum += hash_diff
                    # print(aug, sum, len(aug_types[aug]), sum / len(aug_types[aug]))
                    f2.write(str(sum / len(aug_types[aug])) + ',')
                    f2.write(aug + '-avg,')
                    f2.write(library + ',')
                    f2.write(funcname + ',')
                    f2.write("\n")








