import pickle
import os# import path
import numpy as np
import random

def get_Data(filename):
    file = open(filename,'rb')
    log = pickle.load(file)
    frames = []
    ball = []
    ball_speed = []
    blocker = []
    #Commands = []
    platform_1p = []
    platform_2p = []
    for scene_info in log:
        """
        #Frames.append(sceneInfo.frame)
        ball.append(scene_info["ball"][0], scene_info["ball"][1])
        ball_speed.append(scene_info["ball_speed"][0], scene_info["ball_speed"][1])
        blocker.append(scene_info["blocker"][0], scene_info["blocker"][1])
        #Commands.append(str(sceneInfo.command))
        platform_1p.append(scene_info["platform_1P"][0], scene_info["platform_1P"][1])
        platform_2p.append(scene_info["platform_2P"][0], scene_info["platform_2P"][1])
        """
        frames.append(scene_info["frame"])
        ball.append(scene_info["ball"][0])
        ball.append(scene_info["ball"][1])
        ball_speed.append(scene_info["ball_speed"][0])
        ball_speed.append(scene_info["ball_speed"][1])
        blocker.append(scene_info["blocker"][0])
        blocker.append(scene_info["blocker"][1])
        #Commands.append(str(sceneInfo.command))
        platform_1p.append(scene_info["platform_1P"][0])
        platform_1p.append(scene_info["platform_1P"][1])
        platform_2p.append(scene_info["platform_2P"][0])
        platform_2p.append(scene_info["platform_2P"][1])
    
    frame_arr = np.array([frames])
    frame_arr = frame_arr.reshape((len(frames), 1))
    ball_arr = np.array([ball])
    ball_arr = ball_arr.reshape((len(ball) // 2, 2))
    ball_speed_arr = np.array([ball_speed])
    ball_speed_arr = ball_speed_arr.reshape((len(ball_speed) // 2, 2))
    blocker_arr = np.array([blocker])
    blocker_arr = blocker_arr.reshape((len(blocker) // 2, 2))
    pf_1_arr = np.array([platform_1p])
    pf_1_arr = pf_1_arr.reshape((len(platform_1p) // 2, 2))
    pf_2_arr = np.array([platform_2p])
    pf_2_arr = pf_2_arr.reshape((len(platform_2p) // 2, 2))
    """
    print(ball_arr)
    print(ball_speed_arr)
    print(blocker_arr)
    print(pf_1_arr)
    print(pf_2_arr)
    """
    """
    commands_ary = np.array([Commands])
    commands_ary = commands_ary.reshape((len(Commands), 1))
    frame_ary = np.array(Frames)
    frame_ary = frame_ary.reshape((len(Frames), 1))
    """
    Fdata = np.hstack((ball_arr, ball_speed_arr, blocker_arr, pf_1_arr, pf_2_arr, frame_arr))
    Fdata_arr = np.array(Fdata)
    Fdata_arr = Fdata_arr[1::]
    this_blocker = Fdata_arr[:, 4]
    next_blocker = np.array(this_blocker[1:])
    blocker_dir = next_blocker - this_blocker[:-1]
    blocker_dir = blocker_dir.reshape((len(blocker_dir), 1))
    Fdata = np.hstack((Fdata_arr[1:, :], blocker_dir))
    return Fdata

if __name__ == '__main__':
    
    dictPath = os.path.join(os.path.dirname(__file__), 'games', 'pingpong', 'log')
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    data_arr = np.array(data)
    data_arr = data_arr.reshape(1, 12)
    for file in os.listdir(dictPath):
        filePath = os.path.join(os.path.dirname(__file__), 'games', 'pingpong', 'log', file)
        if filePath != os.path.join(os.path.dirname(__file__), 'games', 'pingpong', 'log', 'finalFile.pickle') and\
            filePath != os.path.join(os.path.dirname(__file__), 'games', 'pingpong', 'log', 'hi.txt'):
            tempData = get_Data(filePath)
            tempData_arr = np.array(tempData)
            data_arr = np.concatenate((data_arr, tempData_arr))
   
    data_arr = np.array(data_arr[1::])
    newZero = np.zeros((len(data_arr),), dtype=np.int)
    newZero = newZero.reshape((len(newZero), 1))
    data_arr = np.hstack((data_arr, newZero))

    loopFlag = 0
    
    data_arr[:, 4] = data_arr[:, 4] + 15
    for i in range(1, len(data_arr)) :
        if data_arr[i, 1] > 260 and data_arr[i - 1, 1] <= 260 :#from up to down(pass blocker)
            loopFlag = i
        elif data_arr[i, 1] < 240 and data_arr[i - 1, 1] >= 240 :#from down to up(pass blocker)
            loopFlag = i
        if data_arr[i, 1] > 80 and data_arr[i - 1, 1] < 80:
            loopFlag = i
        elif data_arr[i, 1] < 420 and data_arr[i - 1, 1] > 420:
            loopFlag = i
        if data_arr[i, 3] < 0 and data_arr[i - 1, 3] > 0 and ((data_arr[i, 1] + data_arr[i - 1, 1]) / 2) < 240 :#case 3 -> above blocker
            for j in range(loopFlag, i) :
                data_arr[j, 12] = 3
            loopFlag = i
        elif data_arr[i, 3] > 0 and data_arr[i - 1, 3] < 0 and ((data_arr[i, 1] + data_arr[i - 1, 1]) / 2) > 260 :#case 1 -> beneath blocker
            for j in range(loopFlag, i) :
                data_arr[j, 12] = 1
            loopFlag = i
        elif data_arr[i, 2] > 0 and data_arr[i - 1, 2] < 0 and ((data_arr[i, 0] + data_arr[i - 1, 0]) / 2) > 30 and\
            ((data_arr[i, 1] + data_arr[i - 1, 1]) / 2) < 280 and ((data_arr[i, 1] + data_arr[i - 1, 1]) / 2) > 220:#case 2 -> right of blocker
            for j in range(loopFlag, i):
                data_arr[j, 12] = 2
            loopFlag = i
        elif data_arr[i, 2] < 0 and data_arr[i - 1, 2] > 0 and ((data_arr[i, 0] + data_arr[i - 1, 0]) / 2) < 170 and\
            ((data_arr[i, 1] + data_arr[i - 1, 1]) / 2) < 280 and ((data_arr[i, 1] + data_arr[i - 1, 1]) / 2) > 220:#case 4 -> left of blocker
            for j in range(loopFlag, i) :
                data_arr[j, 12] = 4
            loopFlag = i

    data_arr[:, 0] = data_arr[:, 0] + 3
    data_arr[:, 1] = data_arr[:, 1] + 3

    ball_dir = []
    
    wantToDelete = []
    
    for i in range(len(data_arr)):
        if data_arr[i, 2] > 0 and data_arr[i, 3] < 0:#右上
            ball_dir.append(0)
        elif data_arr[i, 2] < 0 and data_arr[i, 3] < 0:#左上
            ball_dir.append(1)
        elif data_arr[i, 2] < 0 and data_arr[i, 3] > 0:#左下
            ball_dir.append(2)
        elif data_arr[i, 2] > 0 and data_arr[i, 3] > 0:#右下
            ball_dir.append(3)
        
        elif data_arr[i, 2] == 0 or data_arr[i, 3] == 0:
            wantToDelete.append(i)
    
    ball_dir = np.array(ball_dir)
    ball_dir = ball_dir.reshape((len(ball_dir), 1))

    data_arr = np.delete(data_arr, wantToDelete, axis = 0)
    
    data_arr = np.hstack((data_arr, ball_dir))
    
    next_ballPos = []
    hitBlockerDir = []

    for i in range(len(data_arr)):
        next_dir = data_arr[i, 13]
        if data_arr[i, 1] < 263 and data_arr[i, 1] > 238:
            if data_arr[i, 13] == 0 or data_arr[i, 13] == 1:#go up
                yPath = data_arr[i, 13] - 238
                next_spendTime = (yPath // abs(data_arr[i, 3])) + 1
            else:
                yPath = 263 - data_arr[i, 13]
                next_spendTime = (yPath // data_arr[i, 3]) + 1
            next_X = data_arr[i, 0] + next_spendTime * data_arr[i, 2]
            next_Y = data_arr[i, 1] + next_spendTime * data_arr[i, 3]
            while True:
                if next_X > 198:
                    next_X = 296 - next_X
                    if next_dir == 3:
                        next_dir = 2
                    else :
                        next_dir = 1
                elif next_X < 3:
                    next_X = 6 - next_X
                    if next_dir == 2:
                        next_dir = 3
                    else :
                        next_dir = 0
                else:
                    break
            next_Y = data_arr[i, 1] + next_spendTime * data_arr[i, 3]
        elif data_arr[i, 1] < 263:#在障礙物之上
            if data_arr[i, 13] == 0 or data_arr[i, 13] == 1:#go up
                yPath = 97 + data_arr[i, 1]
                next_spendTime = (yPath // abs(data_arr[i, 3])) + 1
                #print(data_arr[i, 3])
            else:#go down
                yPath = 263 - data_arr[i, 1]
                next_spendTime = (yPath // data_arr[i, 3]) + 1
            next_X = data_arr[i, 0] + next_spendTime * data_arr[i, 2]
            
            while True:
                if next_X > 198:
                    next_X = 396 - next_X
                    if next_dir == 3:
                        next_dir = 2
                    else :
                        next_dir = 1
                elif next_X < 3:
                    next_X = 6 - next_X
                    if next_dir == 2:
                        next_dir = 3
                    else :
                        next_dir = 0
                else:
                    break
            next_Y = data_arr[i, 1] + next_spendTime * data_arr[i, 3]
            if next_Y < 83 :
                next_Y = 166 - next_Y
                if next_dir == 0:
                    next_dir = 3
                else:
                    next_dir = 2
            
        elif data_arr[i, 1] > 238:
            if data_arr[i, 13] == 2 or data_arr[i, 13] == 3:#go down
                yPath = 573 - data_arr[i, 1]
                next_spendTime = (yPath // data_arr[i, 3]) + 1############
            else:#go up
                yPath = data_arr[i, 1] - 238
                next_spendTime = (yPath // abs(data_arr[i, 3])) + 1
            next_X = data_arr[i, 0] + next_spendTime * data_arr[i, 2]
            while True:
                if next_X > 198:
                    next_X = 396 - next_X
                    if next_dir == 3:
                        next_dir = 2
                    else :
                        next_dir = 1
                elif next_X < 3:
                    next_X = 6 - next_X
                    if next_dir == 2:
                        next_dir = 3
                    else :
                        next_dir = 0
                else:
                    break
            next_Y = data_arr[i, 1] + next_spendTime * data_arr[i, 3]
            if next_Y > 418:
                next_Y = 836 - next_Y
                if next_dir == 3:
                    next_dir = 0
                else:
                    next_dir = 1
        Y_awayFromBlocker = 250 - next_Y
        blockerX = data_arr[i, 4] + next_spendTime * data_arr[i, 11]
        while True:
            if blockerX > 185:
                blockerX = 370 - blockerX
            elif blockerX < 15:
                blockerX = 30 - blockerX
            else :
                break
        X_awayFromBlocker = blockerX - next_X

        hitBlockerDir.append(next_dir)
        next_ballPos.append(X_awayFromBlocker)
        next_ballPos.append(Y_awayFromBlocker)
    next_ballPos = np.array(next_ballPos)
    next_ballPos = next_ballPos.reshape((len(next_ballPos) // 2, 2))
    hitBlockerDir = np.array(hitBlockerDir)
    hitBlockerDir = hitBlockerDir.reshape((len(hitBlockerDir), 1))
    data_arr = np.hstack((data_arr, next_ballPos, hitBlockerDir))
    
    wantToDelete = []
    for i in range(1, len(data_arr)):
        if data_arr[i, 12] == data_arr[i - 1, 12] and data_arr[i, 14] == data_arr[i - 1, 14] and\
            data_arr[i, 15] == data_arr[i - 1, 15] and data_arr[i - 1, 16] == data_arr[i, 16]:
            wantToDelete.append(i)
    
    data_arr = np.delete(data_arr, wantToDelete, axis = 0)


    
    with open(os.path.join(os.path.dirname(__file__), 'games', 'pingpong', 'log', 'hi.txt'), 'w') as f:
        for i in range(0, len(data_arr)):
            out_arr = np.array_str(data_arr[i,:]) 
            f.write(out_arr + "\n")
    
    
    with open(os.path.join(os.path.dirname(__file__), 'games', 'pingpong', 'log', 'finalFile.pickle'), 'wb') as f:
        pickle.dump(data_arr, f)
    
    
    #X = data[:, :]
    #Y = data[:, -1]
    #print(X)
    # print(Y)

    
