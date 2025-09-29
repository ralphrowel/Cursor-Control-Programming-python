import pyautogui
import os
import time

time.sleep(3)

maps_folder = "maps"

for filename in os.listdir(maps_folder):
    if filename.endswith(".png"):
        map_path = os.path.join(maps_folder, filename)
        print(f"Searching for {filename}...")

        pyautogui.scroll(-500)


        location = pyautogui.locateOnScreen(map_path, confidence=0.8)

        if location:
            center = pyautogui.center(location)
            pyautogui.moveTo(center.x, center.y, duration=1)
            pyautogui.click()
            print(f"Clicked on {filename} at {center}")
        else:
            print(f"{filename} not found on screen.")
