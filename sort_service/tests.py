import unittest
import source # tested module
import os
import cv2
# import re


class Test_source(unittest.TestCase):

    target_path = '/home/kefear/Documents/maga_2_sem/group_proj/smart-paletter/sort_service/array/pink1.jpg'
    target_path_black = '/home/kefear/Documents/maga_2_sem/group_proj/smart-paletter/sort_service/array/black1.jpeg'
    target_path_blue = '/home/kefear/Documents/maga_2_sem/group_proj/smart-paletter/sort_service/array/blue1.jpg'
    target_path_green = '/home/kefear/Documents/maga_2_sem/group_proj/smart-paletter/sort_service/array/green1.jpg'
    target_path_red = '/home/kefear/Documents/maga_2_sem/group_proj/smart-paletter/sort_service/array/red1.jpeg'
    array_path = 'Documents/maga_2_sem/group_proj/smart-paletter/sort_service/array'
    dic = {}
    val_dict = {}

    def fill_array(path:str, array: dict) -> dict:
        path_list = path.split(sep='/')
        # print (path_list)
        array_path = os.path.join(*path_list)
        for filename in os.listdir(array_path):
            if filename[filename.rfind(".") + 1:] in ['jpg', 'jpeg', 'png']:
                img = cv2.imread(os.path.join(os.path.dirname(__file__),'array', filename))
                array[str(filename)] = img
                # print(filename)
        # for x in array:
        #     print(x)
            # for y in array[x]:
            #     print (y,':',array[x][y])
        return array
    
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

    def resize_image(image):
        # one size resize
        width = 1
        height = 1
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

    

    val_dict=fill_array(array_path,val_dict)
    target_image = cv2.imread(target_path)
    target_image_hsv = format_hsv_image(target_image)
    target = calculate_mean_colour(target_image_hsv)

    target_black = cv2.imread(target_path_black)
    tih_black = format_hsv_image(target_black)
    t_black = calculate_mean_colour(tih_black)

    target_blue = cv2.imread(target_path_blue)
    tih_blue = format_hsv_image(target_blue)
    t_blue = calculate_mean_colour(tih_blue)

    target_green = cv2.imread(target_path_green)
    tih_green = format_hsv_image(target_green)
    t_green = calculate_mean_colour(tih_green)


    thresholds = {}
    thresholds[0] = [255, 30, 30] # for black or white images
    thresholds[1] = [20, 30, 30]
    thresholds[2] = [30,60,60]
    thresholds[3] = [30,150,150]
    thresholds[4] = [40,200,200]
    thresholds[5] = [50, 205, 205]
    #fill_array
    # format_hsv_image
    # def test_format_hsv_image(self):
    # resize_image
    # mean_colour
    # hsv_processing
    # do_this
    def test_fill_array(self):
        result = source.fill_array(path= self.array_path, array=self.dic) 
        self.assertListEqual(list(result.keys()), list(self.val_dict.keys()))

    def test_1(self):
        result = source.do_harder(self.array_path, self.t_black, threshold=self.thresholds[0])
        self.assertListEqual(['black1.jpeg', 'black3.jpg', 'black2.jpg'], result)

    def test_2(self):
        result = source.do_harder(self.array_path, self.t_blue, threshold=self.thresholds[3])
        self.assertListEqual(['blue2.jpeg', 'blue1.jpg', 'blue3.jpg'], result)

    def test_3(self):
        result = source.do_harder(self.array_path, self.t_green, threshold=self.thresholds[3])
        self.assertListEqual(['blue2.jpeg', 'blue1.jpg', 'blue3.jpg'], result)

    # def test_do_this_black(self):
    #     result = source.do_this('black')
    #     matches = [match for match in result if 'black' in match]
    #     self.assertIn('black1.jpeg', matches)
    #     self.assertIn('black2.jpg', matches)
    #     self.assertIn('black3.jpg', matches)
    # def test_do_this_blue(self):
    #     result = source.do_this('blue')
    #     matches = [match for match in result if 'blue' in match]
    #     self.assertIn('blue1.jpg', matches)
    #     self.assertIn('blue1.jpg', matches)
    # def test3_do_this(self):
    #     result = source.do_this('black')
    #     matches = [match for match in result if 'black' in match]
    #     self.assertIn('black3.jpg', matches)

if __name__=='__main__':
    unittest.main()


