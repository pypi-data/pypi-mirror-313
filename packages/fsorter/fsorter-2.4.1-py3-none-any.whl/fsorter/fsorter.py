import os
import re
def fileSort(path = str(), extensions=list()):
        if len(extensions) == 0:
            extensions = ['.jpg', '.png', '.jpeg', '.tif', '.tiff', '.nii', '.JPG', '.JPEG', '.TIFF', '.TIF', '.NII']

        control_1_sentence ='filename.endswith(\'' + extensions[0] + '\')'
        for z in range(1, len(extensions)):
            control_1_sentence += ' or filename.endswith(\'' + extensions[z] + '\')'
        if(path==''):
            path='./'
        path = os.listdir(path)

        list_not = list()
        img_list = []
        for filename in path:
           if eval(control_1_sentence):
               img_list.append(filename)
           else:
               list_not.append(filename)
        if len(list_not) > 0:
            print(str(list_not)+' files not found.')
        digits = list()
        digits_temp = list()
        non_numeric_list = [filename for filename in img_list if not re.search(r'\d', filename)] # MOVED!
        if(len(img_list)==0):
            print('no files !!!')
            return -1
        control_1 = 0
        result = contains_digit_optimized(img_list) 
        if result == True:
            control_1 += 1
        control_5 = split_image_string(img_list)
        int_counts = []
        for sublist in control_5:
            if isinstance(sublist, list):  # Sadece alt listeleri kontrol et
                int_count = sum(1 for item in sublist if isinstance(item, int))
                int_counts.append(int_count)
            else:
                int_counts.append(0)  # Eğer alt liste değilse 0 ekle
        max_int_value = max(int_counts)
        if(control_1==0):
            list_final = sorted(img_list, key=str.lower)
            print('filename without digits ! \nFiles are sorted alphabetically.')
            return list_final
        elif(control_1>0): # 1
            list_zeros=list()
            for control_1_value in range(0,max_int_value):
                maxx = -1
                for i in range(len(img_list)):
                    index = natural_keys(img_list[i])
                    control_2 = 0
                    for ii2 in range(len(index)):
                        if type(index[ii2]) == int:
                            if (control_2 == control_1_value):
                                if (index[ii2] > maxx):
                                    maxx = index[ii2]
                            control_2+=1
                list_zeros.append(len(str(maxx)))
            if non_numeric_list:
                non_numeric_list = sorted(non_numeric_list, key=str.lower)
                img_list = [filename for filename in img_list if re.search(r'\d', filename)]
            for i in range(len(img_list)):
                index = natural_keys(img_list[i])
                check_3 = 0
                list2=''
                for ii in range(len(index)):
                    if type(index[ii]) == int:
                        if(check_3>0):
                            number_zeros=list_zeros[check_3-1]-len(str(index[ii]))
                            for j in range(0,number_zeros):
                                list2 += '0'
                            list2 += str(index[ii])
                        else:
                            list2 += str(index[ii])
                        check_3+=1
                digits.append(int(list2))
                digits_temp.append(int(list2))
            digits.sort()
            list_final = create_final_list(img_list, digits, digits_temp, non_numeric_list)
        return list_final
    

def create_final_list(img_list, digits, digits_temp, non_numeric_list = None):
    list_final = list()
    for c in range(len(img_list)):
        v = digits_temp.index(digits[c])
        list_final.append(img_list[v])
        
    if non_numeric_list is not None:
        list_final.extend(non_numeric_list) 
        
    return list_final


def contains_digit_optimized(strings):
    """
    Listedeki string türündeki elemanlarda rakam olup olmadığını kontrol eder.
    İlk rakam bulunduğunda döngüyü kırar.
    
    :param strings: List (String elemanlar içerir)
    :return: True (Eğer herhangi bir stringde rakam varsa), aksi halde False
    """
    for s in strings:
        if isinstance(s, str) and any(char.isdigit() for char in s):
            return True  # İlk rakam bulunduğunda True döner
    return False  # Hiçbir elemanda rakam bulunmadıysa False döner


def split_image_string(image_string):
    """
    Belirtilen formatta bir stringi parçalayıp listeye dönüştürür.

    :param image_string: String (Örneğin 'IMG_20240814_165737_1_TIMEBURST3.jpg')
    :return: List (Örneğin ['IMG', 20240814, 165737, 1, 'TIMEBURST', 3])
    """
    
    result_list = list()
    for i in image_string:
        # .jpg uzantısını kaldır
        cleaned_string = i.replace(".jpg", "")
        
        # Stringi düzenli ifadelerle parçala
        parts = re.findall(r'[A-Z]+|\d+', cleaned_string)
    
        # Rakamları (dijitleri) integer türüne dönüştür
        result = [int(part) if part.isdigit() else part for part in parts]
        result_list.append(result)
    return result_list

def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)',text) ]