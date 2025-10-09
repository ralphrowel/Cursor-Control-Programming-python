import pyautogui
import time

def simple_click(center):
    """Move to center and click."""
    x, y = center
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()

def spam_keys(center):
    """Click on the center and spam keys for demo."""
    x, y = center
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()
    for key in ['a', 's', 'd']:
        # Safety: abort if user moves mouse
        if pyautogui.position() != (x, y):
            print("⛔ Aborted by user movement.")
            return
        pyautogui.press(key)
        time.sleep(0.05)
