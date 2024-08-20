import numpy as np
import cv2

def zoom(clip, mode='in', position='center', speed=1):
    fps = clip.fps
    duration = clip.duration
    total_frames = int(duration * fps)

    def main(get_frame, t):
        frame = get_frame(t)
        h, w = frame.shape[:2]
        i = t * fps
        if mode == 'out':
            i = total_frames - i
        zoom = 1 + (i * ((0.1 * speed) / total_frames))
        positions = {
            'center': [(w - (w * zoom)) / 2, (h - (h * zoom)) / 2],
            'left': [0, (h - (h * zoom)) / 2],
            'right': [(w - (w * zoom)), (h - (h * zoom)) / 2],
            'top': [(w - (w * zoom)) / 2, 0],
            'topleft': [0, 0],
            'topright': [(w - (w * zoom)), 0],
            'bottom': [(w - (w * zoom)) / 2, (h - (h * zoom))],
            'bottomleft': [0, (h - (h * zoom))],
            'bottomright': [(w - (w * zoom)), (h - (h * zoom))]
        }
        tx, ty = positions[position]
        M = np.array([[zoom, 0, tx], [0, zoom, ty]])
        frame = cv2.warpAffine(frame, M, (w, h))
        return frame

    return clip.fl(main)