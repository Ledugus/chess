import pygame as p
def get_font(size): # Returns Press-Start-2P in the desired size
    return p.font.Font('freesansbold.ttf', size)

def is_over(rect, pos):
    if pos[0] >= rect[0] and pos[0] <= rect[0]+rect[2] and pos[1] >= rect[1] and pos[1] <= rect[1]+rect[3]:
        return True
    return False