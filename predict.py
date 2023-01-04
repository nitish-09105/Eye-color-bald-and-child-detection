import numpy as np
import cv2
import keras

def predict(img,model):
    data = cv2.resize(img, (64, 64))
    data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    data = np.reshape(data, (1, 64, 64, 3)) / 255.0
    res = model.predict(data)[0][0]
    return  res
    # 'Bald:',res)
def bald(x):
    model = keras.models.load_model('models\\bald_classifity.h5')
    image=cv2.imread(x)
    res=predict(image,model)
    return ('NO bald' if res <0.3 else 'YES bald')
if __name__ == '__main__':

    # image 
    image = cv2.imread('test_data\\5.png')
        # detect color percentage
    bald(image)
    cv2.imwrite('sample/result.jpg', image)    
    cv2.waitKey(0)
