import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from life import Life

def main():

    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 400
    WINDOW_NAME = "GAME OF LIFE"
    WINDOW_SIZE = "490x575"
    NEIGHBORHOOD = (10, 10)
    START = (3, 3)
    SPEED = [2000, 1000, 100, 10, 1]
    
    # Generate random starting neighborhood on canvas
    def generate():
        canvas.bind('<Button-1>', paint)
        neighbor_width = nsizex_entry.get()
        neighbor_height = nsizey_entry.get()
        start_width = ssizex_entry.get()
        start_height = ssizey_entry.get()

        if neighbor_width and neighbor_height and start_width and start_height:
            life.scale = int(min(CANVAS_HEIGHT/int(neighbor_height), CANVAS_WIDTH/int(neighbor_width)))
            life.configure((int(start_height), int(start_width)), (int(neighbor_height), int(neighbor_width)))
        else:
            life.scale = 40
            life.make_empty()

        life.generate()
        life.update_img()
        canvas.itemconfigure(life.curr_img, image = life.get_img())

        start_button.configure(state = "normal")
        stop_button.configure(state = "disabled")
        reset_button.configure(state = "normal")

    # Change block state when block is clicked
    def paint(event):
        row = int(event.y / life.scale)
        col = int(event.x / life.scale)
        life.change_cell(row, col)
        life.update_img()
        canvas.itemconfigure(life.curr_img, image = life.get_img())

    # Start animation
    def start():
        life.unpause()
        ssizex_entry.configure(state = "disabled")
        ssizey_entry.configure(state = "disabled")
        nsizex_entry.configure(state = "disabled")
        nsizey_entry.configure(state = "disabled")
        gen_button.configure(state = "disabled")
        reset_button.configure(state = "disabled")
        stop_button.configure(state = "normal")
        start_button.configure(state = "disabled")
        update()
    
    # Update the neighborhood every frame
    def update():
        if not life.is_paused:
            life.update()
            life.update_img()
            canvas.itemconfigure(life.curr_img, image = life.get_img())
            window.after(int(SPEED[speed_slider.get() - 1]), update)

    # Stop the animation
    def stop():
        life.pause()
        reset_button.configure(state = "normal")
        stop_button.configure(state = "disabled")
        start_button.configure(state = "normal")

    # Reset canvas
    def reset():
        canvas.delete("all")
        canvas.unbind("<Button-1>")
        life.make_empty()
        life.update_img()

        life.curr_img = canvas.create_image(0,0, anchor="nw", image=life.get_img())

        start_button.configure(state = "disabled")
        stop_button.configure(state = "disabled")
        reset_button.configure(state = "disabled")
        ssizex_entry.configure(state = "normal")
        ssizey_entry.configure(state = "normal")
        nsizex_entry.configure(state = "normal")
        nsizey_entry.configure(state = "normal")
        gen_button.configure(state = "normal")

    # Creates game of life manager, window, and canvas to draw on
    life = Life(START, NEIGHBORHOOD)
    window = tk.Tk()
    window.title(WINDOW_NAME)
    window.geometry(WINDOW_SIZE)
    canvas = tk.Canvas(window, width=CANVAS_WIDTH,height=CANVAS_HEIGHT, bg="white")
    canvas.place(x = 10, y = 150)

    # Initial animation image
    array = np.zeros((CANVAS_WIDTH, CANVAS_HEIGHT))
    img =  ImageTk.PhotoImage(image=Image.fromarray(array))
    life.curr_img = canvas.create_image(0,0, anchor="nw", image=img)

    # Creates widgets

    # Entries for neighborhood size
    tk.Label(window, text="neighborhood size", font=("Times New Roman", 15)).place(x = 30,y = 10)
    nsizex_entry = tk.Entry(window, width = 5, font=("Times New Roman", 15))
    nsizex_entry.place(x = 35, y = 40)

    tk.Label(window, text="x", font=("Times New Roman", 15)).place(x = 95,y = 40)
    nsizey_entry = tk.Entry(window, width = 5, font=("Times New Roman", 15))
    nsizey_entry.place(x = 115, y = 40)

    # Entries for starting neighborhood size
    tk.Label(window, text="start size", font=("Times New Roman", 15)).place(x = 230,y = 10)
    tk.Label(window, text="x", font=("Times New Roman", 15)).place(x = 260, y = 40)
    ssizex_entry = tk.Entry(window, width = 5, font=("Times New Roman", 15))
    ssizex_entry.place(x = 200, y = 40)
    ssizey_entry = tk.Entry(window, width = 5, font=("Times New Roman", 15))
    ssizey_entry.place(x = 280, y = 40)

    # Button to generate canvas
    gen_button = tk.Button(window, text = "generate", font=("Times New Roman", 15), 
                            activebackground="white", width = 7, 
                            command = generate)
    gen_button.place(x = 380, y = 20)

    # Start animation button
    start_button = tk.Button(window, text = "start", font=("Times New Roman", 18), 
                            activebackground="white", width = 6, state = "disabled",
                            command = start)
    start_button.place(x = 35, y = 85)

    # Stop animation button
    stop_button = tk.Button(window, text = "stop", font=("Times New Roman", 18), 
                            activebackground="white", width = 6, state = "disabled",
                            command = stop)
    stop_button.place(x = 180, y = 85)

    # Reset button
    photo = Image.open("reset.png")
    img = photo.resize((40,40))
    final_img = ImageTk.PhotoImage(img)
    reset_button = tk.Button(window, image=final_img, state = "disabled", command = reset)
    reset_button.place(x = 320, y = 85)

    # Speed slider
    tk.Label(window, text = "speed", wraplength = 1).place(x = 460, y = 300)
    speed_slider = tk.Scale(window, from_=1, to=len(SPEED), length = 250)
    speed_slider.set(3)
    speed_slider.place(x = 430, y = 220)

    window.mainloop()

if __name__ == "__main__":
    main()