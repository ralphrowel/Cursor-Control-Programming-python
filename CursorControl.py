import cv2
import numpy as np
import pyautogui
import os
import time

# import your patterns
from patterns import testpattern

# ---- CONFIG ----
maps_folder = r"C:\Users\ralph\OneDrive\Desktop\python\Cursor-Control-Programming\images"
THRESHOLD = 0.85
SCALE_MIN, SCALE_MAX, STEPS = 0.7, 1.4, 20
SEARCH_INTERVAL = 0.25
# ----------------

pyautogui.PAUSE = 0.05
pyautogui.FAILSAFE = False   # UI will handle abort later

# preload templates
templates = {}
for fname in os.listdir(maps_folder):
    if fname.lower().endswith(('.png', '.jpg')):
        path = os.path.join(maps_folder, fname)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            templates[fname] = img
print(f"Loaded {len(templates)} templates.")

def grab_screen():
    shot = pyautogui.screenshot()
    bgr = cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return gray

def find_template_on_image(template_gray, screen_gray):
    h0, w0 = template_gray.shape[:2]
    best_val, best_loc, best_scale = -1, None, None
    for s in np.linspace(SCALE_MIN, SCALE_MAX, int(STEPS)):
        tw, th = int(w0 * s), int(h0 * s)
        if tw < 10 or th < 10: continue
        if tw > screen_gray.shape[1] or th > screen_gray.shape[0]: continue
        resized = cv2.resize(template_gray, (tw, th))
        res = cv2.matchTemplate(screen_gray, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > best_val:
            best_val, best_loc, best_scale = max_val, max_loc, s
    return best_val, best_loc, best_scale

# mapping: which file triggers which pattern
ACTION_MAP = {
    'attack.png': testpattern.spam_keys,
    'heal.png': testpattern.simple_click,
    # add more: 'image.png': pattern_function
}

def scan_and_act():
    screen_gray = grab_screen()
    for fname, tmpl in templates.items():
        score, loc, scale = find_template_on_image(tmpl, screen_gray)
        print(f"{fname}: {score:.3f}")
        if score >= THRESHOLD and loc:
            th, tw = int(tmpl.shape[0] * scale), int(tmpl.shape[1] * scale)
            center = (loc[0] + tw // 2, loc[1] + th // 2)
            action = ACTION_MAP.get(fname)
            if action:
                action(center)
                print(f"Executed action for {fname}")
            else:
                print(f"No action mapped for {fname}")

if __name__ == "__main__":
    print("Backend running... Ctrl+C to stop.")
    time.sleep(2)
    while True:
        scan_and_act()
        time.sleep(SEARCH_INTERVAL)
