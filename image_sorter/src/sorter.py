################################################################################################
# python 3.10 
# cv2
################################################################################################
import cv2
import os
import numpy as np

from src.api.models import Image

# filling array 
# with upload images
def fill_array(array: dict) -> dict:
    for filename in os.listdir(os.path.join(os.path.dirname(__file__),'array')):
        if filename[filename.rfind(".") + 1:] in ['jpg', 'jpeg', 'png']:
            # print(filename)
            # name = str(filename)
            img = cv2.imread(os.path.join(os.path.dirname(__file__),'array', filename))
            array[str(filename)] = img
    return array

# RGB -> resize -> hsv
def format_hsv_image(image):
    # one size resize
    width = 1
    height = 1

    # percent resize
    # width = int(array[image].shape[1] * scale_percent / 100)
    # height = int(array[image].shape[0] * scale_percent / 100)

    dim = (width, height)
    img = image.copy() #copy for resizing
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return img

# RGB resize
def resize_image(image):
    # one size resize
    width = 1
    height = 1

    # percent resize
    # scale_percent = 2
    # width = int(array[image].shape[1] * scale_percent / 100)
    # height = int(array[image].shape[0] * scale_percent / 100)

    dim = (width, height)
    img = image.copy() #copy for resizing
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return img


def calculate_mean_colour(image):
    size = image.shape
    sq = [0,0,0] #Массив для общего подсчета
    width = size[0] #Ширина
    height = size[1] #Высота
    count = width*height #Ширина * Высота

    for i in range(width): #Цикл по ширине
        for j in range(height): #Цикл по высоте
            sq[0] += image[i, j][0] #b or h (hue)
            sq[1] += image[i, j][1] #g or s (saturation)
            sq[2] += image[i, j][2] #r or v (value)

    out = [0, 0, 0] #Массив для средних значений
    out[0] = int(sq[0]/count) #Средние значения
    out[1] = int(sq[1]/count)
    out[2] = int(sq[2]/count)
    return out

# try to calculate average image's colour 
def mean_colour(array: dict) -> dict:
    img_list = {}

    # resize/format
    for image in array.keys():

        # this one for RGB (BGR actualy) 
        # img_list[image] = resize_image(array[image])

        # this one for HSV
        img_list[image] = format_hsv_image(array[image])
    
    average_value_colour = {}
    for img in img_list.keys():
        average_value_colour[img] = calculate_mean_colour(img_list[img])
        # print for rgb
        # print(f'Средний цвет: {img}({average_value_colour[img][0]}, {average_value_colour[img][1]}, {average_value_colour[img][2]})')
        # hexed = '#' + format(out[2], 'x') + format(out[1], 'x') + format(out[0], 'x') #Перевод в HEX
        # print(f'hex: {hexed}')

    return average_value_colour
    
# try to processing palette rgb
# def temp_processing(average_arr: dict, target_colour: str):
#     result = []

#     #conditions needs to be changed
#     match target_colour:
#         case 'black':
#             for filename in average_arr.keys():
#                 acceptable_black_or_white_range = range(min(average_arr[filename]), min(average_arr[filename])+10, 1)

#                 if average_arr[filename][0] in acceptable_black_or_white_range and \
#                     average_arr[filename][1] in acceptable_black_or_white_range and \
#                         average_arr[filename][1] in acceptable_black_or_white_range and \
#                             min(acceptable_black_or_white_range) <= 120:
#                     result.append(filename)

#         case 'white':
#             for filename in average_arr.keys():
#                 acceptable_black_or_white_range = range(min(average_arr[filename]), min(average_arr[filename])+10, 1)

#                 if average_arr[filename][0] in acceptable_black_or_white_range and \
#                     average_arr[filename][1] in acceptable_black_or_white_range and \
#                         average_arr[filename][1] in acceptable_black_or_white_range and \
#                             min(acceptable_black_or_white_range) >= 120:
#                     result.append(filename)

#         case 'blue':
#             for filename in average_arr.keys():
#                 if average_arr[filename][0] > average_arr[filename][1] and \
#                     average_arr[filename][0] > average_arr[filename][2]:
#                     result.append(filename)

#         case 'green':
#             for filename in average_arr.keys():
#                 if average_arr[filename][1] > average_arr[filename][0] and \
#                     average_arr[filename][1] > average_arr[filename][2]:
#                     result.append(filename)

#         case 'yellow':
#             for filename in average_arr.keys():
#                 if average_arr[filename][2] == max(average_arr[filename]) and \
#                     average_arr[filename][1] in range(average_arr[filename][0]+20, average_arr[filename][2]):
#                     result.append(filename)

#         case 'red':
#             for filename in average_arr.keys():
#                 if average_arr[filename][2] == max(average_arr[filename]) and \
#                     average_arr[filename][2]-10 > (average_arr[filename][0]+average_arr[filename][0])/2:
#                     result.append(filename)
#         case 'pink':
#             for filename in average_arr.keys():
#                 # if average_arr[filename][2] >= 190 and \
#                 if max(average_arr[filename]) == average_arr[filename][2] and \
#                 average_arr[filename][1] == min(average_arr[filename]) and \
#                 average_arr[filename][1] < 200 and \
#                 average_arr[filename][0] in range(average_arr[filename][1], average_arr[filename][2]-20):
#                     result.append(filename)

#         case _:
#             print('oh hellow there, your colour is not supported')

#     return result

# try to processing palette in hsv colours
# def hsv_processing(average_arr: dict, target_colour:str) -> list:
#     # red (h = 0 +- 10) (s = 255) (v = 255)
#     # yellow (h = 30 +- 10) (s = 255) (v = 255)
#     # lime (h = 60 +- 10) (s = 255) (v = 255)
#     # teal (h = 90 +- 10) (s = 255) (v = 128)
#     # blue (h = 120 +- 10) (s = 255) (v = 255)
#     # violet (h = 150 +- 10) (s = 116) (v = 238)
#     # purple (h = 150 +- 10) (s = 255) (v = 128)

#     # black (h = 0 +- 10) (s = 0) (v = 0)
#     # gray 0 0 128
#     # white 0 0 255
#     color_table = {
#         'black': [range(0, 179), range(0, 30), range(0,50)],
#         'gray': [range(0, 179), range(0, 30), range(51,189)],
#         'white': [range(0, 179), range(0, 30), range(190,255)],
#         'red': [range(0, 10), range(70, 255), range(40,255)],
#         'red2': [range(161, 179), range(70, 255), range(40,255)],
#         'orange': [range(11, 25), range(60, 255), range(40,170)],
#         'yellow': [range(20, 40), range(140, 255), range(100,255)],
#         'green': [range(41, 79), range(50, 255), range(50,255)],
#         'teal': [range(80, 100), range(50, 255), range(50,255)],
#         'blue': [range(101, 139), range(50, 255), range(50,255)],
#         'purple': [range(140, 160), range(50, 255), range(50,255)]
#     }
#     result = []

#     match target_colour:
#         case 'black':
#             for filename in average_arr.keys():
#                 if average_arr[filename][1] in color_table['black'][1] and \
#                 average_arr[filename][2] in color_table['black'][2]:
#                     result.append(filename)
#         case 'gray':
#             for filename in average_arr.keys():
#                 if average_arr[filename][1] in color_table['grey'][1] and \
#                 average_arr[filename][2] in color_table['grey'][2]:
#                     result.append(filename)
#         case 'white':
#             for filename in average_arr.keys():
#                 if average_arr[filename][1] in color_table['white'][1] and \
#                 average_arr[filename][2] in color_table['white'][2]:
#                     result.append(filename)
#         case 'red':
#             for filename in average_arr.keys():
#                 if (average_arr[filename][0] in color_table['red'][0] and \
#                     average_arr[filename][1] in color_table['red'][1] and \
#                     average_arr[filename][2] in color_table['red'][2]) or \
#                     (average_arr[filename][0] in color_table['red'][0] and \
#                     average_arr[filename][1] in color_table['red2'][1] and \
#                     average_arr[filename][2] in color_table['red2'][2]):
#                     result.append(filename)
#         case 'orange':
#             for filename in average_arr.keys():
#                 if average_arr[filename][0] in color_table['orange'][0] and \
#                     average_arr[filename][1] in color_table['orange'][1] and \
#                     average_arr[filename][2] in color_table['orange'][2]:
#                     result.append(filename)
#         case 'yellow':
#             for filename in average_arr.keys():
#                 if average_arr[filename][0] in color_table['yellow'][0] and \
#                     average_arr[filename][1] in color_table['yellow'][1] and \
#                     average_arr[filename][2] in color_table['yellow'][2]:
#                     result.append(filename)
#         case 'green':
#             for filename in average_arr.keys():
#                 if average_arr[filename][0] in color_table['green'][0] and \
#                     average_arr[filename][1] in color_table['green'][1] and \
#                     average_arr[filename][2] in color_table['green'][2]:
#                     result.append(filename)
#         case 'teal':
#             for filename in average_arr.keys():
#                 if average_arr[filename][0] in color_table['teal'][0] and \
#                     average_arr[filename][1] in color_table['teal'][1] and \
#                     average_arr[filename][2] in color_table['teal'][2]:
#                     result.append(filename)
#         case 'blue':
#             for filename in average_arr.keys():
#                 if average_arr[filename][0] in color_table['blue'][0] and \
#                     average_arr[filename][1] in color_table['blue'][1] and \
#                     average_arr[filename][2] in color_table['blue'][2]:
#                     result.append(filename)
#         case 'purple':
#             for filename in average_arr.keys():
#                 if average_arr[filename][0] in color_table['purple'][0] and \
#                     average_arr[filename][1] in color_table['purple'][1] and \
#                     average_arr[filename][2] in color_table['purple'][2]:
#                     result.append(filename)
#         case _:
#             print("oh hellow there! \n the program was created by a guy, who doesn't know this color name, try something simpler")
#             return
#     return result

# def do_this(target:str) -> list:
#     dick = {}
#     dick = fill_array(dick)
#     average_colour_value_dick = mean_colour(dick)
#     # print('\n'.join("{}\t{}".format(k, v) for k, v in average_colour_value_dick.items()))
#     result = hsv_processing(average_arr=average_colour_value_dick, target_colour = target)
#     return result

def hsv_processing_harder(average_arr: dict, target_colour: list, threshold: list) -> list:
    result = []
    threshold_range = [[],[],[]]
    threshold_range[0] = range(target_colour[0]-threshold[0], target_colour[0]+threshold[0])
    threshold_range[1] = range(target_colour[1]-threshold[1], target_colour[1]+threshold[1])
    threshold_range[2] = range(target_colour[2]-threshold[2], target_colour[2]+threshold[2])
    for filename in average_arr.keys():
        if average_arr[filename][0] in threshold_range[0] and \
            average_arr[filename][1] in threshold_range[1] and \
            average_arr[filename][2] in threshold_range[2]:
                    result.append(filename)    
    return result

def do_harder(target:list, threshold:list) -> list:
    dick = {}
    dick = fill_array(dick)
    average_colour_value_dick = mean_colour(dick)
    # print('\n'.join("{}\t{}".format(k, v) for k, v in average_colour_value_dick.items()))
    result = hsv_processing_harder(average_arr=average_colour_value_dick, target_colour = target, threshold=threshold)
    return result

def sort_images(images: list) -> list:
    for im in images:
        im_np = np.frombuffer(im.data, dtype='uint8')
        target_im = cv2.imdecode(im_np, cv2.IMREAD_COLOR)
        target_im_hsv = format_hsv_image(target_im)
        im.mean_colour = calculate_mean_colour(target_im_hsv)

    images = sorted(images, key=lambda x: x.mean_colour)
    return images

if __name__ == '__main__':
    target_image_path = '/home/kefear/Documents/maga_2_sem/group_proj/smart-paletter/sort_service/array/pink1.jpg'
    target_image = cv2.imread(target_image_path)
    target_image_hsv = format_hsv_image(target_image)
    target = calculate_mean_colour(target_image_hsv)
    # print(target)

    # result = do_this('blue')
    thresholds = {}
    thresholds['black_or_white'] = [255, 30, 30]
    thresholds[1] = [20, 30, 30]
    thresholds[2] = [30,60,60]
    thresholds[3] = [30,150,150]
    thresholds[4] = [40,200,200]
    thresholds[5] = [50, 205, 205]

    result = do_harder(target, threshold = thresholds[2])
    print(result)
