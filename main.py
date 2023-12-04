#!/usr/bin/env python3

from queue import Queue
import threading
import cv2

in_filename = 'clip.mp4'

process_queue = Queue[cv2.typing.MatLike]()
display_queue = Queue[cv2.typing.MatLike]()


def extract():
    """
    Extracts frames from a video file and inserts them into the process queue.
    """
    count = 0
    vidcap = cv2.VideoCapture(in_filename)
    success, image = vidcap.read()
    while success:
        # print(f'Extracting frame {count}...', image.shape)
        process_queue.insert(image)
        success, image = vidcap.read()
        count += 1


def process():
    """
    Converts frames to grayscale and inserts them into the display queue.
    """
    count = 0
    while True:
        image = process_queue.remove()
        # print(f'Processing frame {count}...', image.shape)
        gs_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        display_queue.insert(gs_image)
        count += 1


def display():
    """
    Displays frames from the display queue in a window.
    """
    count = 0
    while True:
        image = display_queue.remove()
        # print(f'Displaying frame {count}...', image.shape)
        cv2.imshow('Video', image)

        # wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(42) & 0xFF == ord("q"):
            break

        count += 1

    cv2.destroyAllWindows()


if __name__ == '__main__':
    threading.Thread(target=extract).start()
    threading.Thread(target=process).start()
    threading.Thread(target=display).start()
