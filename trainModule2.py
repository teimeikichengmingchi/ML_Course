import pickle
import numpy as np
#from os import path
import os# import path
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import metrics


if __name__ == '__main__':
    
    filename = os.path.join(os.path.dirname(__file__), 'games', 'pingpong', 'log', 'finalFile.pickle')
    file = open(filename,'rb')
    feature = pickle.load(file)
        
    """
    沒有零目前看來是可行的
    有一些零也可以接受
    """
    count0 = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    wantToDelete = []
    for i in range(len(feature)):
        if feature[i, 12] == 0:
            count0 = count0 + 1
            #if random.random() > 0.3:
            wantToDelete.append(i)
        elif feature[i, 12] == 1:
            count1 = count1 + 1
            #if random.random() > 0.7:
                #wantToDelete.append(i)
        elif feature[i, 12] == 2:
            count2 = count2 + 1
        elif feature[i, 12] == 3:
            count3 = count3 + 1
            #if random.random() > 0.7:
                #wantToDelete.append(i)
        elif feature[i, 12] == 4:
            count4 = count4 + 1
    feature = np.delete(feature, wantToDelete, axis = 0)
    print(str(count0)+" "+str(count1)+" "+str(count2)+" "+str(count3)+" "+str(count4)+" ")
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
        if Y[i] == 3 or Y[i] == 4 or Y[i] == 2:
            wantToDelete.append(i)
    cpX = np.delete(cpX, wantToDelete, axis = 0)
    cpY = np.delete(cpY, wantToDelete, axis = 0)
    y_predict = predict_clf.predict(cpX)
    accuracy = metrics.accuracy_score(cpY, y_predict)
    print("Accuracy(正確率)(分辨1) ={:8.3f}%".format(accuracy*100))

    cpX = np.copy(X)
    cpY = np.copy(Y)
    wantToDelete = []
    for i in range(len(cpX)):
        if Y[i] == 4 or Y[i] == 1 or Y[i] == 3:
            wantToDelete.append(i)
    cpX = np.delete(cpX, wantToDelete, axis = 0)
    cpY = np.delete(cpY, wantToDelete, axis = 0)
    y_predict = predict_clf.predict(cpX)
    accuracy = metrics.accuracy_score(cpY, y_predict)
    print("Accuracy(正確率)(分辨2) ={:8.3f}%".format(accuracy*100))

    cpX = np.copy(X)
    cpY = np.copy(Y)
    wantToDelete = []
    for i in range(len(cpX)):
        if Y[i] == 1 or Y[i] == 2 or Y[i] == 4:
            wantToDelete.append(i)
    cpX = np.delete(cpX, wantToDelete, axis = 0)
    cpY = np.delete(cpY, wantToDelete, axis = 0)
    y_predict = predict_clf.predict(cpX)
    accuracy = metrics.accuracy_score(cpY, y_predict)
    print("Accuracy(正確率)(分辨3) ={:8.3f}%".format(accuracy*100))

    cpX = np.copy(X)
    cpY = np.copy(Y)
    wantToDelete = []
    for i in range(len(cpX)):
        if Y[i] == 1 or Y[i] == 2 or Y[i] == 3:
            wantToDelete.append(i)
    cpX = np.delete(cpX, wantToDelete, axis = 0)
    cpY = np.delete(cpY, wantToDelete, axis = 0)
    y_predict = predict_clf.predict(cpX)
    accuracy = metrics.accuracy_score(cpY, y_predict)
    print("Accuracy(正確率)(分辨4) ={:8.3f}%".format(accuracy*100))

    
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
    
"""
    ax = plt.subplot(111, projection='3d')  
    ax.scatter(X[Y==0][:,0], X[Y==0][:,1], X[Y==0][:,3], c='#FF0000', alpha = 1)  
    ax.scatter(X[Y==1][:,0], X[Y==1][:,1], X[Y==1][:,3], c='#2828FF', alpha = 1)
    ax.scatter(X[Y==2][:,0], X[Y==2][:,1], X[Y==2][:,3], c='#007500', alpha = 1)
    
    
    plt.title("KMeans Prediction")    
    ax.set_xlabel('Ball_x')
    ax.set_ylabel('Ball_y')
    ax.set_zlabel('Direction')
        
    plt.show()
 """   


       

