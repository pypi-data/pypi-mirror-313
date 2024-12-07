import pyautogui
from time import sleep

_default_autopath = r'C:\\'
_default_altpath = None

def set_autopath(path):
    global _default_autopath
    _default_autopath = path

def set_altpath(path):
    global _default_altpath
    _default_altpath = path

def optimiseWait(filename, dontwait=False, specreg=None, clicks=1, xoff=0, yoff=0, autopath=None, altpath=None):
    global _default_autopath, _default_altpath
    autopath = autopath if autopath is not None else _default_autopath
    altpath = altpath if altpath is not None else _default_altpath

    if not isinstance(filename, list):
        filename = [filename]
    if not isinstance(clicks, list):
        clicks = [clicks] + [1] * (len(filename) - 1)
    elif len(clicks) < len(filename):
        clicks = clicks + [1] * (len(filename) - len(clicks))
    
    if not isinstance(xoff, list):
        xoff = [xoff] * len(filename)
    elif len(xoff) < len(filename):
        xoff = xoff + [0] * (len(filename) - len(xoff))
        
    if not isinstance(yoff, list):
        yoff = [yoff] * len(filename)
    elif len(yoff) < len(filename):
        yoff = yoff + [0] * (len(filename) - len(yoff))

    clicked = 0
    while True:
        findloc = None
        found_in_alt = False
        
        for i, fname in enumerate(filename):
            # Try main path first
            try:
                if specreg is None:
                    loc = pyautogui.locateCenterOnScreen(fr'{autopath}\{fname}.png', confidence=0.9)
                else:
                    loc = pyautogui.locateOnScreen(fr'{autopath}\{fname}.png', region=specreg, confidence=0.9)
                
                if loc and clicked == 0:
                    findloc = loc
                    clicked = i + 1
                    found_in_alt = False
                    break
            except pyautogui.ImageNotFoundException:
                pass
            
            # Try alt path if provided and image wasn't found in main path
            if altpath and not findloc:
                try:
                    if specreg is None:
                        loc = pyautogui.locateCenterOnScreen(fr'{altpath}\{fname}.png', confidence=0.9)
                    else:
                        loc = pyautogui.locateOnScreen(fr'{altpath}\{fname}.png', region=specreg, confidence=0.9)
                    
                    if loc and clicked == 0:
                        findloc = loc
                        clicked = i + 1
                        found_in_alt = True
                        break
                except pyautogui.ImageNotFoundException:
                    continue

        if dontwait is False:
            if findloc:
                break
        else:
            if not findloc:
                return {'found': False, 'image': None}
            else:
                return {'found': True, 'image': filename[clicked - 1]}
        sleep(1)

    if findloc is not None:
        if specreg is None:
            x, y = findloc
        else:
            x, y, width, height = findloc
        
        current_xoff = xoff[clicked - 1] if clicked > 0 else 0
        current_yoff = yoff[clicked - 1] if clicked > 0 else 0
        xmod = x + current_xoff
        ymod = y + current_yoff
        sleep(1)

        click_count = clicks[clicked - 1] if clicked > 0 else 0
        if click_count > 0:
            for _ in range(click_count):
                pyautogui.click(xmod, ymod)
                sleep(0.1)
        
        return {'found': True, 'image': filename[clicked - 1]}
    
    return {'found': False, 'image': None}