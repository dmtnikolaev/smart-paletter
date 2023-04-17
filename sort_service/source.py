import cv2
import os

# filling array 
# with upload images
def fill_array(array: list):
    for filename in os.listdir(os.path.join(os.path.dirname(__file__),'array')):
        if filename[filename.rfind(".") + 1:] in ['jpg', 'jpeg', 'png']:
            print(filename)
            # name = str(filename)
            img = cv2.imread(os.path.join(os.path.dirname(__file__),'array', filename))
            array.append(img)
    return array

# try to calculate average image's colour 
def mean_colour(array: list):
    img_list = []
    scale_percent = 10 # percent of original size for percent resize

    for image in array:

        # one size resize
        # width = 150
        # height = 150
        # dim = (width, height)

        # percent resize
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = image.copy() #copy for resizing
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        img_list.append(img)
    
    average_value_colour = []
    for img in img_list:
        size = img.shape
        sq = [0,0,0] #Массив для общего подсчета
        width = size[0] #Ширина
        height = size[1] #Высота
        count = width*height #Ширина * Высота

        for i in range(width): #Цикл по ширине
            for j in range(height): #Цикл по высоте
                sq[0] += img[i, j][0] #b
                sq[1] += img[i, j][1] #g
                sq[2] += img[i, j][2] #r
	
        out = [0, 0, 0] #Массив для средних значений
        out[0] = int(sq[0]/count) #Средние значения
        out[1] = int(sq[1]/count)
        out[2] = int(sq[2]/count)
        average_value_colour.append(out)
        print(f'Средний цвет: rgb({out[2]}, {out[1]}, {out[0]})')
        hexed = '#' + format(out[2], 'x') + format(out[1], 'x') + format(out[0], 'x') #Перевод в HEX
        print(f'hex: {hexed}')
    return average_value_colour
    
def temp_processing():
    pass

if __name__ == '__main__':
    array = []
    array = fill_array(array)
    average_colour_value = mean_colour(array)