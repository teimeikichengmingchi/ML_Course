"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    
    Rmove = False
    Lmove = False
    s = [0, 0]

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        if s != [0, 0]:
            rate = [scene_info.ball[0] - s[0], scene_info.ball[1] - s[1]]

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information
        if scene_info.ball[1] == 395:
            Rmove = False
            Lmove = False
        elif scene_info.ball[1] > 170:
            if  rate[0] > 0 and \
                rate[1] > 0 and \
                (scene_info.ball[0] + 400 - scene_info.ball[1] > scene_info.platform[0] + 35):
                Rmove = True
                Lmove = False
                if scene_info.ball[0] + 400 - scene_info.ball[1] > 250:
                    if scene_info.platform[0] + 20 < 100:
                        Rmove = True
                        Lmove = False
                    else:
                        Lmove = True
                        Rmove = False
            elif  rate[0] > 0 and \
                rate[1] > 0 and \
                (scene_info.ball[0] + 400 - scene_info.ball[1] < scene_info.platform[0] + 5):
                Lmove = True
                Rmove = False
            elif rate[0] < 0 and \
                rate[1] > 0 and \
                (scene_info.ball[0] + 400 - scene_info.ball[1] < scene_info.platform[0] + 5):
                Lmove = True
                Rmove = False
                if scene_info.ball[0] + 400 - scene_info.ball[1] < -50:
                    if scene_info.platform[0] + 20 < 100:
                        Rmove = True
                        Lmove = False
                    else:
                        Lmove = True
                        Rmove = False
            elif rate[0] < 0 and \
                rate[1] > 0 and \
                (scene_info.ball[0] + 400 - scene_info.ball[1] > scene_info.platform[0] + 35):
                Rmove = True
                Lmove = False
            else:
                #Rmove = False
                #Lmove = False
                if scene_info.platform[0] + 20 < 100:
                    Rmove = True
                    Lmove = False
                else:
                    Lmove = True
                    Rmove = False
        else:
            if scene_info.platform[0] + 20 < 100:
                Rmove = True
                Lmove = False
            else:
                Lmove = True
                Rmove = False

        s[0] = scene_info.ball[0]
        s[1] = scene_info.ball[1]
                    

        # 3.4. Send the instruction for this frame to the game process
        if Lmove:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        elif Rmove:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
