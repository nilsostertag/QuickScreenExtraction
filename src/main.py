import pytesseract
from PIL import Image
import pyautogui
import keyboard
import pyscreenshot as ImageGrab
import time
import tkinter as tk
from screeninfo import get_monitors

from config_reader import config
from editor import open_in_notepad

setupcfg = config('config\\config.json')

# Path to tesseract.exe (Windows)
pytesseract.pytesseract.tesseract_cmd = setupcfg.path_tesseract

# one time execution for screenshots
is_processing = False

# detect screens
def screenshot_and_ocr():
    global is_processing
    
    if is_processing:
        print("Please wait while the previous screenshot is being processed.")
        return
    
    is_processing = True  # Processing initiated, block image recording
    
    print("Please select an area to take a screenshot.")
    
    # transparent white effect
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.2)  # tanslucent overlay
    root.config(bg='white')

    # canvas
    canvas = tk.Canvas(root, cursor="cross", bg='white', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # starting point
    start_x = start_y = None
    rect = None

    # on click -> set starting coordinates of selection
    def on_click(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y
        if rect:
            canvas.delete(rect)

    # draw rectangle
    def on_drag(event):
        nonlocal rect
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline='black', width=2)

    # rtake screenshot on mouse release
    def on_release(event):
        global is_processing

        # detect screen
        monitors = get_monitors()
        selected_monitor = None
        
        # calculate screen coordinates
        for monitor in monitors:
            if monitor.x <= event.x_root <= monitor.x + monitor.width and \
               monitor.y <= event.y_root <= monitor.y + monitor.height:
                selected_monitor = monitor
                break
        
        if selected_monitor:
            screen_start_x = selected_monitor.x + start_x
            screen_start_y = selected_monitor.y + start_y
            screen_end_x = selected_monitor.x + event.x
            screen_end_y = selected_monitor.y + event.y

            # close root
            root.quit()
            root.destroy()

            # take screenshot in selected area
            im = ImageGrab.grab(bbox=(screen_start_x, screen_start_y, screen_end_x, screen_end_y))
            
            #TODO Saving screenshots with text and timestamp
            # save screenshot (optional)
            # im.save("screenshot.png")
            
            # OCR on screenshot
            text = pytesseract.image_to_string(im, lang=setupcfg.language_mode)
            print("Output\n------")
            print(text)

            open_in_notepad(text)
        else:
            print("No available Screen detected.")

        # processing finished
        is_processing = False

    # bind mouse events
    canvas.bind("<ButtonPress-1>", on_click)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)

    # Tkinter-GUI
    root.mainloop()

# close program
def close_program():
    print("Shutting down.")
    exit()


# hotkeys
def main():
    print("'Strg+Alt+P' to extract text from your screen.")
    print("'Strg+Alt+E' or 'Esc' to close the program.")

    # Hotkey zum Starten des Screenshot-Tools
    keyboard.add_hotkey('ctrl+alt+p', screenshot_and_ocr)

    # Hotkey zum Beenden des Programms
    keyboard.add_hotkey('ctrl+alt+e', close_program)

    # Programm läuft, bis 'Esc' oder 'Strg+Alt+E' gedrückt wird
    keyboard.wait('esc')

if __name__ == "__main__":
    main()