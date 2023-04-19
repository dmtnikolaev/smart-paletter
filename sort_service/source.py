import cv2
import os

# filling array 
# with upload images
def fill_array(array: dict):
    for filename in os.listdir(os.path.join(os.path.dirname(__file__),'array')):
        if filename[filename.rfind(".") + 1:] in ['jpg', 'jpeg', 'png']:
            # print(filename)
            # name = str(filename)
            img = cv2.imread(os.path.join(os.path.dirname(__file__),'array', filename))
            array[str(filename)] = img
    return array

# try to calculate average image's colour 
def mean_colour(array: dict):
    img_list = {}
    scale_percent = 5 # percent of original size for percent resize
    # print(array.keys())
    for image in array.keys():

        # one size resize
        width = 4
        height = 4

        # percent resize
        # width = int(array[image].shape[1] * scale_percent / 100)
        # height = int(array[image].shape[0] * scale_percent / 100)
        dim = (width, height)
        img = array[image].copy() #copy for resizing
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        img_list[image] = img
    
    average_value_colour = {}
    for img in img_list.keys():
        size = img_list[img].shape
        sq = [0,0,0] #Массив для общего подсчета
        width = size[0] #Ширина
        height = size[1] #Высота
        count = width*height #Ширина * Высота

        for i in range(width): #Цикл по ширине
            for j in range(height): #Цикл по высоте
                sq[0] += img_list[img][i, j][0] #b
                sq[1] += img_list[img][i, j][1] #g
                sq[2] += img_list[img][i, j][2] #r
	
        out = [0, 0, 0] #Массив для средних значений
        out[0] = int(sq[0]/count) #Средние значения
        out[1] = int(sq[1]/count)
        out[2] = int(sq[2]/count)
        average_value_colour[img] = out
        # print(f'Средний цвет: rgb({out[2]}, {out[1]}, {out[0]})')
        # hexed = '#' + format(out[2], 'x') + format(out[1], 'x') + format(out[0], 'x') #Перевод в HEX
        # print(f'hex: {hexed}')
    return average_value_colour
    
def temp_processing(average_arr: dict, target_colour: str):
    # colour_dict = {'black':0, 'blue':1, 'green':2, 'red':3, 'white':4}
    result = []
    # try:
        # for colour in colour_dict.keys():
        #     if tagret_colour.lower() == colour:
        #         target = colour_dict[colour]
        # print(target)
        
        #conditions needs to be changed
    match target_colour:
        case 'black':
            for filename in average_arr.keys():
                if (average_arr[filename][0] == average_arr[filename][1]) and \
                    (average_arr[filename][0] == average_arr[filename][2]) and (average_arr[filename][0] <= 120):
                    result.append(filename)
        case 'white':
            for filename in average_arr.keys():
                if (average_arr[filename][0] == average_arr[filename][1]) and \
                    (average_arr[filename][0] == average_arr[filename][2]) and (average_arr[filename][0] >= 150):
                    result.append(filename)
        case 'blue':
            for filename in average_arr.keys():
                if average_arr[filename][0] > average_arr[filename][1] and \
                    average_arr[filename][0] > average_arr[filename][2]:
                    result.append(filename)
        case 'green':
            for filename in average_arr.keys():
                if average_arr[filename][1] > average_arr[filename][0] and \
                    average_arr[filename][1] > average_arr[filename][2]:
                    result.append(filename)
        case 'red':
            for filename in average_arr.keys():
                if average_arr[filename][2] > average_arr[filename][1] and \
                    average_arr[filename][2] > average_arr[filename][0]:
                    result.append(filename)
        case _:
            print('oh hellow there, your colour is not supported')

    return result

    # except:
    #     print('your colour is not supported')

if __name__ == '__main__':
    dick = {}
    dick = fill_array(dick)
    average_colour_value_dick = mean_colour(dick)
    print('\n'.join("{}\t{}".format(k, v) for k, v in average_colour_value_dick.items()))
    result = temp_processing(average_arr=average_colour_value_dick, target_colour = 'black')
    print(result)