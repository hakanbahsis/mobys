import cv2
import os

def pattern(image,res_adi):
    # Mermer yüzeyinin fotoğrafını oku

    image_path=image
    img = cv2.imread(image_path,0)
    resim_adi=res_adi

    # Görüntüyü gri seviyelerine dönüştür
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Görüntüyü elastik büyütme (dilate) işlemine tabi tut
    # Bu işlem, çatlakların daha belirgin hale gelerek
    # tespit edilmesini kolaylaştırır
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.dilate(gray, kernel)

    # Önceden eğitilmiş bir Canny kenar tespit modeli kullanarak
    # çatlakları tespit et
    canny = cv2.Canny(dilated, 30, 150)
    cv2.imwrite(os.getcwd()+"\\static\\sonuclar\\"+resim_adi,img)
    return [canny]
    # Çatlakları göster
    #cv2.imshow('Cracks', canny)
    #cv2.waitKey(0)