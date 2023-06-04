################################################################################################
# python 3.10 
# cv2
################################################################################################
import cv2
import os
from sys import argv

# filling array 
# with upload images
def fill_array(path:str, array: dict) -> dict:
    # for filename in os.listdir(os.path.join(os.path.dirname(__file__),'array')):
    path_list = path.split(sep='/')
    # path_list.pop(0)
    path_list.pop(-1)
    print (path_list)
    array_path = os.path.join(*path_list)
    for filename in os.listdir(array_path):
        print('filename =', filename)
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

def do_harder(array_path, target:list, threshold:list) -> list:
    dick = {}
    dick = fill_array(array_path, dick)
    average_colour_value_dick = mean_colour(dick)
    # print('\n'.join("{}\t{}".format(k, v) for k, v in average_colour_value_dick.items()))
    result = hsv_processing_harder(average_arr=average_colour_value_dick, target_colour = target, threshold=threshold)
    return result

if __name__ == '__main__':
    _, target_image_path, array_path = argv
    # target_image_path = '/home/kefear/Documents/maga_2_sem/group_proj/smart-paletter/sort_service/array/pink1.jpg'
    # path = '/home/kefear/Documents/maga_2_sem/group_proj/smart-paletter/sort_service/array/'
    target_image = cv2.imread(target_image_path)
    target_image_hsv = format_hsv_image(target_image)
    target = calculate_mean_colour(target_image_hsv)

    thresholds = {}
    thresholds['black_or_white'] = [255, 30, 30]
    thresholds[1] = [20, 30, 30]
    thresholds[2] = [30,60,60]
    thresholds[3] = [30,150,150]
    thresholds[4] = [40,200,200]
    thresholds[5] = [50, 205, 205]

    result = do_harder(array_path, target, threshold = thresholds[2])
    print(result)