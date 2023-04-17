import cv2
import os

# try to calculate average image's colour 
def mean_colour():
    #i don't know how i receive images
    picture_name = os.path.join(os.path.dirname(__file__),'screen.jpg')
    # print(picture_name)

    image = cv2.imread(picture_name) #image

    img = image.copy() #copy for resizing
    scale_percent = 20 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    # cv2.imshow('resized', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

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

    print(f'Средний цвет: rgb({out[2]}, {out[1]}, {out[0]})')
    hexed = '#' + format(out[2], 'x') + format(out[1], 'x') + format(out[0], 'x') #Перевод в HEX
    print(f'hex: {hexed}')
    

if __name__ == '__main__':
    mean_colour()