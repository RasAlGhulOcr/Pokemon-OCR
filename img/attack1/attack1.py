# For a tutorial on how to use Normbox please watch this video on YouTube: https://youtu.be/34cgrzyaOzE
import os
import cv2
import keyboard


class GCVWorker:
    def __init__(self, width, height):
        os.chdir(os.path.dirname(__file__))
        self.gcvdata = bytearray([0x00])
        self.X = width
        self.Y = height
        self.index = 0
        self.nextIndez = True
        self.nextIndex = 0
        self.x1 = 1382
        #self.x1 = 1326
        self.y1 = 705
        self.x2 = 1642
        #self.x2 = 1381
        self.y2 = 735
        self.image = True
        self.showFrozenFrame = False
        self.freeze = True

    def __del__(self):
        del self.gcvdata
        del self.X
        del self.Y
        del self.x1
        del self.x2
        del self.y1
        del self.y2
        del self.index
        del self.nextIndez
        del self.nextIndex
        del self.image
        del self.freeze
        del self.showFrozenFrame

    def process(self, frame):
        # If the user activate the frozenFrame function then it will always display the same frame
        if self.showFrozenFrame:
            frame = cv2.imread('frozenFrame.jpg')

        # Extract an image of the box | Button q
        if keyboard.is_pressed("q") and self.image:
            # Image extracted from the x and y coordinates
            cv2.imwrite('xy.jpg', frame[self.y1:self.y1 + (self.y2 - self.y1), self.x1:self.x1 + (self.x2 - self.x1)])

            # String variables that will be saved as txt file
            text = "\"x1\": {}, \n\"y1\": {}, \n\"x2\": {}, \n\"y2\": {}, \n\"w\": {}, \n\"h\": {}\n".format(
                self.x1,
                self.y1,
                self.x2,
                self.y2,
                (self.x2 - self.x1),
                (self.y2 - self.y1))

            variable = "\nframe = frame[{}:{}, {}:{}]".format(self.y1, self.y1 + (self.y2 - self.y1), self.x1, self.x1 + (self.x2 - self.x1))
            f = open('xy.txt', 'w+')
            f.write(text)
            f.write(variable)
            f.close()

            # Inform the user where the files have been saved
            print('A JPG and TXT file has been created on directory: {}'.format(os.path.dirname(__file__)))
            self.image = False
        elif keyboard.is_pressed("q"):
            pass
        else:
            self.image = True

        # Grab the current frame and freeze it so that the user can extract the image easier | Button RS/R3
        if keyboard.is_pressed("e") and self.freeze:
            self.freeze = False
            self.showFrozenFrame = not self.showFrozenFrame

            # Display the current state of the frame
            if self.showFrozenFrame:
                # Create an image of the current frame and save it to display it
                cv2.imwrite('frozenFrame.jpg', frame)
                print('Showing the frozen frame')
            else:
                print('Unfreezing the frame')

        elif keyboard.is_pressed("e"):
            pass
        else:
            self.freeze = True

        # X1 cord
        cv2.putText(frame, "X1: " + str(self.x1), (5, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                    cv2.LINE_AA)

        # Y1 cord
        cv2.putText(frame, "Y1: " + str(self.y1), (5, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                    cv2.LINE_AA)

        # X2 cord
        cv2.putText(frame, "X2: " + str(self.x2), (5, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                    cv2.LINE_AA)

        # Y2 cord
        cv2.putText(frame, "Y2: " + str(self.y2), (5, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                    cv2.LINE_AA)

        # Width
        cv2.putText(frame, "Width: " + str((self.x2 - self.x1)), (5, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                    cv2.LINE_AA)

        # Height
        cv2.putText(frame, "Height: " + str((self.y2 - self.y1)), (5, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                    cv2.LINE_AA)

        # Changes the x and y index | Button LB/L1
        if keyboard.is_pressed("y") and self.nextIndez:
            self.index = self.index + 1
            self.nextIndez = False
            if self.index > 1 or self.index == 0:
                self.index = 0
                print('Now changing X1, Y1')
            elif self.index == 1:
                print('Now changing X2, Y2')

        # Moves the square being drawn on the square
        if keyboard.is_pressed("w"):  # D-Pad up
            if self.index == 0:
                self.y1 = self.y1 - 1
            else:
                self.y2 = self.y2 - 1

        elif keyboard.is_pressed("s"):  # D-Pad Down
            if self.index == 0:
                self.y1 = self.y1 + 1
            else:
                self.y2 = self.y2 + 1

        elif keyboard.is_pressed("d"):  # D-Pad Right
            if self.index == 0:
                self.x1 = self.x1 + 1
            else:
                self.x2 = self.x2 + 1

        elif keyboard.is_pressed("a"):  # D-Pad Left
            if self.index == 0:
                self.x1 = self.x1 - 1
            else:
                self.x2 = self.x2 - 1

        if keyboard.is_pressed("x") <= 1.0:
            self.nextIndez = True

        # Draws a box around the specified area
        cv2.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), (255, 0, 0), 1)

        return (frame, None)