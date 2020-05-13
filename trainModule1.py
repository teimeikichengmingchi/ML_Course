import pickle
import numpy as np
#from os import path
import os# import path
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import metrics
import random


if __name__ == '__main__':
    
    filename = os.path.join(os.path.dirname(__file__), 'games', 'pingpong', 'log', 'finalFile.pickle')
    file = open(filename,'rb')
    feature = pickle.load(file)
    
    wantToDelete = []
    for i in range(len(feature)):
        if feature[i, 12] != 0:
            feature[i, 12] = 1
        elif random.random() > 0.5:
            wantToDelete.append(i)
        feature[i, 14] = abs(feature[i, 14])
    feature = np.delete(feature, wantToDelete, axis = 0)
    print(len(feature))
    mask = [14, 15, 16]
    X = feature[:, mask]
    Y = feature[:, 12]
    x_train , x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2)
    """
    predict_clf = KMeans(n_clusters=4, random_state=0).fit(x_train,y_train)        
    y_predict = predict_clf.predict(x_test)
    #print(y_predict)
    accuracy = metrics.accuracy_score(y_test, y_predict)
    print("Accuracy(正確率) ={:8.3f}%".format(accuracy*100))
    """
    predict_clf = SVC(C=50, kernel='rbf').fit(x_train,y_train)
    y_predict = predict_clf.predict(x_test)
    accuracy = metrics.accuracy_score(y_test, y_predict)
    print("Accuracy(正確率) ={:8.3f}%".format(accuracy*100))

    cpX = np.copy(X)
    cpY = np.copy(Y)
    wantToDelete = []
    for i in range(len(cpX)):
        if Y[i] == 1:
            wantToDelete.append(i)
    cpX = np.delete(cpX, wantToDelete, axis = 0)
    cpY = np.delete(cpY, wantToDelete, axis = 0)
    y_predict = predict_clf.predict(cpX)
    accuracy = metrics.accuracy_score(cpY, y_predict)
    print("Accuracy(正確率)(分辨0) ={:8.3f}%".format(accuracy*100))

    cpX = np.copy(X)
    cpY = np.copy(Y)
    wantToDelete = []
    for i in range(len(cpX)):
        if Y[i] == 0:
            wantToDelete.append(i)
    cpX = np.delete(cpX, wantToDelete, axis = 0)
    cpY = np.delete(cpY, wantToDelete, axis = 0)
    y_predict = predict_clf.predict(cpX)
    accuracy = metrics.accuracy_score(cpY, y_predict)
    print("Accuracy(正確率)(分辨1) ={:8.3f}%".format(accuracy*100))
    
    #y_predict = predict_clf.predict(X)
    with open(os.path.join(os.path.dirname(__file__), 'games', 'pingpong', 'ml', 'save', 'hitBlockerPredict.pickle'), 'wb') as f:
        pickle.dump(predict_clf, f) 
   
    with open(os.path.join(os.path.dirname(__file__), 'games', 'pingpong', 'ml', 'save', 'hitBlockerPredictValue.txt'), 'w') as f:
        for i in range(len(y_predict)) :
            out = y_predict[i].astype(int)
            f.write(str(out) + "\n")
    with open(os.path.join(os.path.dirname(__file__), 'games', 'pingpong', 'ml', 'save', 'hitBlockerRealValue.txt'), 'w') as f:
        for i in range(len(y_test)) :
            out = y_test[i].astype(int)
            f.write(str(out) + "\n")