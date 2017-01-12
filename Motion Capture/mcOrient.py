import numpy
import cv2
from Motion_Capture import error


CHESS_REFINE_SIZE = 50

def orientationFromSetup(cameraCount, chessboardSize):
    # Setup cameras

    cameras = [None] * cameraCount
    chessboardsFound = chessboards = [None] * cameraCount
    homographyPerspectives = [None] * cameraCount
    for i in range(cameraCount):
        cameras[i] = cv2.VideoCapture(i)
        chessboardsFound[i] = False
        chessboards[i] = None
        homographyPerspectives[i] = None

    # Enter selection loop (look for checkerboards)
    while(True):
        failedCameras = []
        for camIndex, cam in enumerate(cameras):
            # Capture frame-by-frame
            camOk, camFrame = cam.read()

            # Filter out missed frames
            if not camOk:
                failedCameras.append(camIndex)
                continue

            # Attempt to find checkerboard
            # Warp frame from homography from last time to better find the new homography (chessboard) 
            chessCheckFrame = cv2.warpPerspective(camFrame, homographyPerspectives[camIndex], (640, 480)) if chessboardsFound[camIndex] else camFrame.copy()
            chessFound, chess = cv2.findChessboardCorners(chessCheckFrame, chessboardSize, flags = cv2.CALIB_CB_ADAPTIVE_THRESH)
            displayFrame = cv2.drawChessboardCorners(camFrame, chessboardSize, chess, chessFound)

            # Draw chessboards to screen
            if chessFound:
                # Undo - warped homograpahy
                if chessboardsFound[camIndex]:
                    chess = cv2.perspectiveTransform(chess, cv2.invert(homographyPerspectives[camIndex])[1])

                chessTiles = []
                for y in range(chessboardSize[1]):
                    for x in range(chessboardSize[0]):
                        chessTiles.append([a - b / 2 for a, b in zip([x,y], chessboardSize)])
                chessTilesCentered = 20*numpy.array(chessTiles) + numpy.array([320,240])

                #Homography
                homography, _ = cv2.findHomography(chess,chessTilesCentered)
                homographyPerspectives[camIndex] = homography
                displayFrame = cv2.warpPerspective(displayFrame, homography, (640, 480))
            chessboardsFound[camIndex] = chessFound

            # Display the resulting frame
            cv2.imshow("camera" + str(camIndex), displayFrame)
            cv2.imshow("cameraCheck" + str(camIndex), chessCheckFrame)

        if len(failedCameras) != 0:
            print("Failed to grab frame for camera(s): " + ",".join([str(c) for c in failedCameras]))

        # Keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            # Quit
            exit()
        elif key == ord('p'):
            # Pause
            key = 0xFF
            while (key == 0xFF):
                key = cv2.waitKey(10)
                pass
        if key == ord('t'):
            if len(chessBoards) == cameraCount and all([chess[0] for chess, _ in chessBoards]):
                # Take shot with all checkerboards
                break
            else:
                print("Could not take shot, not all checkerboards were found")
                break

    # Refine chessboard data
    #refinedChess = [cv2.cornerSubPix(frame, chess[1], (CHESS_REFINE_SIZE, CHESS_REFINE_SIZE), (-1, -1), 
    #    (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 1)) for chess, frame in chessBoards]
    refinedChess = range(cameraCount)

    # Get camera orientation
    cameraOrient = []

    # When everything done, release the capture
    [cam.release() for cam in cameras]
    cv2.destroyAllWindows()
    return