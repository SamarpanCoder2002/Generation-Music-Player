                                   # Generation Music Player #       
from tkinter import *
from tkinter import filedialog,messagebox,colorchooser
import time,pygame
from PIL import ImageTk,Image
from mutagen.mp3 import MP3

class MusicPlayer:
    def __init__(self, root, backward_img, play_img, pause_img, stop_image_btn, forward_img):
        self.window = root
        # Some variables initialize with None 
        self.heading_label = None
        self.my_list_song = None
        self.empty_indicator = None
        self.mute_scale = None
        self.loop_bar = None
        self.shuffle_bar = None
        self.heading_window = None
        self.new_label_entry = None
        self.new_song_entry = None
        # Some integer variable initialization
        self.bg_custom_color = IntVar()
        self.fg_custom_color = IntVar()
        self.default_bg_color = IntVar()
        self.default_fg_color = IntVar()
        self.heading_change = IntVar()
        self.default_heading_name = IntVar()
        self.shuffle_change = IntVar()
        self.repeat_change = IntVar()
        self.mute_change = IntVar()
        self.shuffle_counter = IntVar()
        self.repeat_counter = IntVar()

        # Default activation
        self.default_heading_name.set(1)
        self.default_fg_color.set(1)
        self.default_bg_color.set(1)

        # Btn img initialization
        self.forward_btn = forward_img
        self.backward_btn = backward_img
        self.pause_btn = pause_img
        self.play_btn = play_img
        self.stop_btn = stop_image_btn

        # Value initialization
        self.add_one_song = 0
        self.add_multiple_song = 0
        self.status_bar = 0
        self.song_length = 0
        self.volume_scale = 0
        self.repeat_counter = 1
        self.shuffle_counter = 0
        self.clear_listbox = 0
        self.total_song = 0
        self.music_menu = 0
        self.shuffle_status = 1
        self.repeat_status = 1
        self.mute_status = 1

        # py_game initialization
        pygame.mixer.init()

        # Default function calling
        self.make_listbox()
        self.all_labels()
        self.text_button_set()
        self.image_button_function_set()
        self.status()
        self.muter()
        self.repeat_controller()
        self.shuffle_controller()
        self.create_menu()

    def make_listbox(self):# Song Collection to play
        self.my_list_song = Listbox(self.window,bg="brown",fg="gold",width=120,height=10,font=("Arial",8,"bold"),relief=SUNKEN,borderwidth=20)
        self.my_list_song.place(x=25,y=80)

    def all_labels(self):# Some default labels initialization
        self.heading_label = Label(self.window,text="Generation Music Player", font=("Arial",20,"bold","italic"),bg="orange",fg="blue")
        self.heading_label.place(x=240,y=25)

        self.empty_indicator = Button(self.window,text="Empty List",relief=FLAT,bd=10,command=self.add_song, font=("Arial",43,"bold","italic"),bg="brown",fg="gold")
        self.empty_indicator.grid(row=0,column=0,padx=220,pady=105,ipadx=10,ipady=10)

        self.empty_indicator.bind('<Enter>', self.on_hover_effect)# Overmouse effect
        self.empty_indicator.bind('<Leave>', self.out_hover_effect)# Outmouse effect

    def text_button_set(self): # Some button initialization
        self.add_one_song = Button(self.window,text="Add Song",font=("Helvetica",15,"bold","italic"), bg="black",fg="green",width=12,height=1,relief=RAISED,borderwidth=8,command=self.add_song)
        self.add_one_song.place(x=480,y=352)

        self.add_multiple_song = Button(self.window, text="Delete Selected Song", font=("Helvetica", 14, "bold", "italic"), bg="black", fg="green", width= 25, relief=RAISED, borderwidth=10,command=self.delete_selected_song)
        self.add_multiple_song.place(x=478, y=432)

        self.total_song = Button(self.window, text="Song Counter", width="11",font=("Helvetica", 15, "bold", "italic"), bg="black", fg="green", relief=RAISED, borderwidth=8, command=self.song_counter)
        self.total_song.place(x=647, y=352)

    def image_button_function_set(self):# Instructional buttons
        self.play_btn.config(command=lambda: self.play_song('<Return>'))
        self.window.bind('<Return>',self.play_song)
        self.window.bind('<Double-Button-1>', self.play_song)

        self.pause_btn.config(command=lambda: self.pause_song('<space>'))
        self.window.bind('<space>',self.pause_song)

        self.stop_btn.config(command=lambda: self.stop_song('<0>'))
        self.window.bind('<0>', self.stop_song)

        self.forward_btn.config(command=lambda: self.next_song('<Right>'))
        self.window.bind('<Right>', self.next_song)

        self.backward_btn.config(command=lambda: self.previous_song('<Left>'))
        self.window.bind('<Left>', self.previous_song)

    def add_song(self):# Adding songs
        self.add_multiple_song = filedialog.askopenfilenames(title="Select one or multiple song",filetypes=(("MP3 files", "*mp3"), ("WAV files","*.wav")))
        self.empty_indicator.grid_forget()
        for song in self.add_multiple_song:
            self.my_list_song.insert(END, song)
            time.sleep(1)
            window.update()

    def delete_selected_song(self):# Delete a particular song
        self.stop_song('<0>')
        self.my_list_song.delete(ACTIVE)
        if self.my_list_song.size() == 0:
           self.empty_indicator.grid(row=0, column=0, padx=220, pady=105, ipadx=10, ipady=10)

    def status(self):# Make status bar
        global status_bar
        status_bar = Label(self.window, text="Song Duration", font=("Arial",17,"bold"),
                                fg="green", bg="orange",width=25)
        status_bar.place(x=220, y=285)

    def song_counter(self):# Total song present in the list
        messagebox.showinfo("Song Counter", "Total song in the list: " + str(self.my_list_song.size()))
        
    def on_hover_effect(self,e):# On mouse effect
        self.empty_indicator.config(bg="green",fg="orange",relief=RAISED,bd=6)

    def out_hover_effect(self,e):# Out mouse effect
        self.empty_indicator.config(bg="brown",fg="gold",relief=FLAT)

    def play_song(self,e):# Play a song
        try:
            song_concatenate = self.my_list_song.get(ACTIVE)
            pygame.mixer.music.load(song_concatenate)
            pygame.mixer.music.play(loops=self.repeat_counter)

            # song length founder
            song_type = MP3(song_concatenate)
            self.song_length = time.strftime("%H:%M:%S", time.gmtime(song_type.info.length))
            self.song_duration_time()
        except:
            self.next_song('<Right>')

    def song_duration_time(self):# Song duration time controller
        get_time = pygame.mixer.music.get_pos()/1000
        converted_time = time.strftime("%H:%M:%S",time.gmtime(get_time))
        status_bar.config(text="Time is: "+str(converted_time)+" of "+str(self.song_length))
        status_bar.place(x=210,y=285)
        if self.song_length == converted_time  and self.repeat_counter == 1:
           self.next_song('<Right>')
        elif self.song_length == converted_time and self.repeat_counter == -1:
            self.play_song('<Return>')
        else:
           status_bar.after(1000,self.song_duration_time)# Recursive function call after 1 sec

    def pause_song(self,e):
        pygame.mixer.music.pause()
        self.pause_btn.config(command=lambda: self.play_after_pause('<space>'))
        self.window.bind('<space>', self.play_after_pause)

    def play_after_pause(self,e):# Play the song after pause
        pygame.mixer.music.unpause()
        self.pause_btn.config(command=lambda: self.pause_song('<space>'))
        self.window.bind('<space>', self.pause_song)

    def stop_song(self,e):# Stop playing song
        pygame.mixer.music.stop()
        status_bar.destroy()
        self.status()

    def next_song(self,e):# Next song control
        try:
            current_song = self.my_list_song.curselection()
            self.my_list_song.selection_clear(ACTIVE)
            current_song = current_song[0]+1

            if current_song < self.my_list_song.size():

                   self.my_list_song.selection_set(current_song)
                   self.my_list_song.activate(current_song)
                   self.play_song('<Return>')

            elif self.shuffle_counter ==0:
                   self.stop_song('<0>')

            else:
                   self.my_list_song.selection_set(0)
                   self.my_list_song.activate(0)
                   self.play_song('<Return>')
        except:
            pass

    def previous_song(self,e):# Previous song control
        try:
            song = self.my_list_song.curselection()
            self.my_list_song.selection_clear(ACTIVE)
            song = song[0]-1

            if song>-1:

               self.my_list_song.activate(song)
               self.my_list_song.selection_set(song)
               self.play_song('<Return>')

            elif self.shuffle_counter ==0:
                   self.stop_song('<0>')

            else:
                 self.my_list_song.selection_set(0)
                 self.my_list_song.activate(0)
                 self.play_song('<Return>')
        except:
            pass

    def muter(self):# Mute a song
        self.mute_scale = Scale(self.window,from_=1,to=0,orient=HORIZONTAL,bg="tan",command=self.get_mute, activebackground="red",font=("Arial",15,"bold"),length=47,relief=RIDGE,bd=3)
        self.mute_scale.place(x=25,y=430)

        self.mute_scale.set(self.mute_status)

        mute_indicator = Label(self.window,text="Mute",font=("Arial",10,"bold"),fg="brown",bg="tan")
        mute_indicator.place(x=35,y=435)

    def get_mute(self,x):# Mute indicator
        pygame.mixer.music.set_volume(int(x))
        if int(x)==1:
            self.mute_change.set(0)
        else:
            self.mute_change.set(1)

    def repeat_controller(self):
        self.loop_bar = Scale(self.window,from_=1,to=0,orient=HORIZONTAL,bg="tan",command=self.repeat_maintain, activebackground="red",font=("Arial",15,"bold"),length=140,relief=RIDGE,bd=3)
        self.loop_bar.place(x=115,y=430)

        self.loop_bar.set(self.repeat_status)

        loop_bar_indicator = Label(self.window,text="Off    Repeat    On",font=("Arial",10,"bold"),fg="brown",bg="tan")
        loop_bar_indicator.place(x=130,y=435)

    def repeat_maintain(self, y):# Repeat indicator
        if int(y) == 1:
            self.repeat_counter = 1
            self.repeat_change.set(0)
        else:
            self.repeat_counter = -1
            self.repeat_change.set(1)

        self.window.update()

    def shuffle_controller(self):
        self.shuffle_bar = Scale(self.window,from_=1,to=0,orient=HORIZONTAL,bg="tan",command=self.shuffle_maintain, activebackground="red",font=("Arial",15,"bold"),length=140,relief=RIDGE,bd=3)
        self.shuffle_bar.place(x=305,y=430)

        self.shuffle_bar.set(self.shuffle_status)

        shuffle_bar_indicator = Label(self.window,text="  Off    Shuffle    On",font=("Arial",10,"bold"),fg="brown",bg="tan")
        shuffle_bar_indicator.place(x=310,y=435)

    def shuffle_maintain(self, y):# Shuffle indicator
        if int(y) ==1:
            self.shuffle_counter = 0
            self.shuffle_change.set(0)
        else:
            self.shuffle_counter = 1
            self.shuffle_change.set(1)

    def create_menu(self):# menu_bar with functionality check
        self.music_menu = Menu(self.window)
        window.config(menu=self.music_menu)

        color_menu = Menu(self.music_menu,tearoff=False)
        self.music_menu.add_cascade(label="Color", menu=color_menu)
        color_menu.add_checkbutton(variable=self.bg_custom_color,label="Background Color change",activebackground="black", activeforeground="red", font=("Arial",10,"bold"),foreground="blue",command=self.bg_color_change)
        color_menu.add_checkbutton(variable=self.fg_custom_color,label="Foreground Color change", activebackground="black", activeforeground="red", font=("Arial", 10, "bold"), foreground="blue",command=self.fg_color_change)
        color_menu.add_checkbutton(variable=self.default_bg_color,label="Default Background Color", activebackground="black", activeforeground="red", font=("Arial", 10, "bold"), foreground="blue",command=self.default_background_color)
        color_menu.add_checkbutton(variable=self.default_fg_color,label="Default Foreground Color", activebackground="black", activeforeground="red", font=("Arial", 10, "bold"), foreground="blue", command=self.default_foreground_color)

        option_menu = Menu(self.music_menu,tearoff=False)
        self.music_menu.add_cascade(label="Option", menu=option_menu)
        option_menu.add_command(label="Clear the list",command=self.clear,activebackground="black",activeforeground="green",font=("Arial",10,"bold"),foreground="brown")
        option_menu.add_checkbutton(variable=self.heading_change,label="Change the Heading",activebackground="black",activeforeground="green",font=("Arial",10,"bold"),foreground="brown",command=self.change_heading)
        option_menu.add_checkbutton(variable=self.default_heading_name,label="Set Default Heading",activebackground="black",activeforeground="green",font=("Arial",10,"bold"),foreground="brown",command=self.default_heading)
        option_menu.add_command(label="Play the target song",activebackground="black",activeforeground="green",font=("Arial",10,"bold"),foreground="brown",command=self.active_target_song)
        option_menu.add_checkbutton(variable=self.shuffle_change,label="Shuffle",activebackground="black",activeforeground="green",font=("Arial",10,"bold"),foreground="brown",command=self.shuffle_activation)
        option_menu.add_checkbutton(variable=self.repeat_change,label="Repeat",activebackground="black",activeforeground="green",font=("Arial",10,"bold"),foreground="brown",command=self.repeat_activation)
        option_menu.add_checkbutton(variable=self.mute_change,label="Mute",activebackground="black",activeforeground="green",font=("Arial",10,"bold"),foreground="brown",command=self.mute_activation)

    def clear(self):# Clear the song list
        self.stop_song('<0>')
        self.my_list_song.delete(0, END)
        self.empty_indicator.grid(row=0, column=0, padx=220, pady=105, ipadx=10, ipady=10)

    def change_heading(self):# Heading chenge manually
        self.heading_window = Tk()
        self.heading_window.title("Heading changer")
        self.heading_window.geometry("400x400")
        self.heading_window.iconbitmap("Pictures/music_icon.ico")
        self.heading_window.config(bg="tan")

        new_label_heading = Label(self.heading_window,text="Enter the new heading",bg="tan",fg="brown", font=("Helvetica",25,"bold","italic"))
        new_label_heading.place(x=25,y=100)

        self.new_label_entry = Entry(self.heading_window,font=("Arial",17,"bold"),fg="red",bg="black",width=25, relief=SUNKEN,bd=15)
        self.new_label_entry.focus_force()
        self.new_label_entry.place(x=25,y=170)

        ok_btn = Button(self.heading_window,text="Ok",bg="green",fg="yellow",relief=RAISED,bd=10,font=("Arial",13,"bold"),padx=10,pady=7,command=lambda: self.new_heading('<Return>'))
        ok_btn.place(x=170,y=260)
        self.heading_window.bind('<Return>',self.new_heading)

    def new_heading(self,e):# New heading setting
        self.heading_label.config(text=self.new_label_entry.get())
        self.heading_window.destroy()
        self.default_heading_name.set(0)
        self.heading_change.set(1)

    def default_heading(self):# Default heading setting
        self.heading_label.config(text="Generation Music Player")
        self.default_heading_name.set(1)
        self.heading_change.set(0)

    def active_target_song(self):# Selected song play
        self.heading_window = Tk()
        self.heading_window.title("Heading changer")
        self.heading_window.geometry("400x400")
        self.heading_window.config(bg="tan")
        self.heading_window.iconbitmap("Pictures/music_icon.ico")

        new_label_heading = Label(self.heading_window, text="-:Enter the target song number:-", bg="tan", fg="brown", font=("Helvetica", 18, "bold", "italic"))
        new_label_heading.place(x=15, y=100)

        self.new_song_entry = Entry(self.heading_window, font=("Arial", 17, "bold"), fg="red", bg="black", width=25, relief=SUNKEN, bd=15)
        self.new_song_entry.focus_force()
        self.new_song_entry.place(x=25, y=170)

        ok_btn = Button(self.heading_window, text="Ok", bg="green", fg="yellow", relief=RAISED, bd=10, font=("Arial", 13, "bold"), padx=10, pady=7, command=lambda: self.target_song_set('<Return>'))
        ok_btn.place(x=170, y=260)
        self.heading_window.bind('<Return>', self.target_song_set)

    def target_song_set(self,e):
        if  int(self.new_song_entry.get())  <= int(self.my_list_song.size()):
            self.my_list_song.selection_clear(ACTIVE)
            self.my_list_song.activate(int(self.new_song_entry.get())-1)
            self.my_list_song.selection_set(int(self.new_song_entry.get())-1)
            self.heading_window.destroy()
            self.play_song('<Return>')
        else:
            messagebox.showerror("Error","Target song not found")
            self.heading_window.destroy()

    def shuffle_activation(self):
        if  self.shuffle_status == 1:
            self.shuffle_status = 0
            self.shuffle_bar.set(self.shuffle_status)
            self.shuffle_counter = 1
            self.shuffle_change.set(1)
        else:
            self.shuffle_status = 1
            self.shuffle_bar.set(self.shuffle_status)
            self.shuffle_counter = 0
            self.shuffle_change.set(0)

    def repeat_activation(self):
        if  self.repeat_status == 1:
            self.repeat_status = 0
            self.loop_bar.set(self.repeat_status)
            self.repeat_counter = -1
            self.repeat_change.set(1)
        else:
            self.repeat_status = 1
            self.loop_bar.set(self.repeat_status)
            self.repeat_counter = 1
            self.repeat_change.set(0)

    def mute_activation(self):
        if  self.mute_status == 1:
            self.mute_status = 0
            self.mute_scale.set(self.mute_status)
            self.get_mute(0)
        else:
            self.mute_status = 1
            self.mute_scale.set(self.mute_status)
            self.get_mute(1)

    def bg_color_change(self):
        new_color = colorchooser.askcolor()
        self.window.config(bg=new_color[1])
        self.heading_label.config(bg=new_color[1])
        status_bar.config(bg=new_color[1])
        self.default_bg_color.set(0)
        self.bg_custom_color.set(1)

    def default_background_color(self):
        self.window.config(bg="orange")
        self.heading_label.config(bg="orange")
        status_bar.config(bg="orange")
        self.default_bg_color.set(1)
        self.bg_custom_color.set(0)

    def fg_color_change(self):
        new_color = colorchooser.askcolor()
        self.heading_label.config(fg=new_color[1])
        status_bar.config(fg=new_color[1])
        self.empty_indicator.config(fg=new_color[1])
        self.default_fg_color.set(0)
        self.fg_custom_color.set(1)

    def default_foreground_color(self):
        self.heading_label.config(fg="blue")
        status_bar.config(fg="green")
        self.empty_indicator.config(fg="yellow")
        self.default_fg_color.set(1)
        self.fg_custom_color.set(0)


if __name__ == '__main__':
    window = Tk()
    window.title("Generation Music player")
    window.iconbitmap("Pictures/music_icon.ico")
    window.geometry("820x515")
    window.maxsize(820,515)
    window.minsize(820,515)
    window.config(bg="orange")

    backward_image_take = ImageTk.PhotoImage(Image.open('Pictures/backward.png'))
    backward_btn_img = Button(window,image=backward_image_take,bg="yellow",relief=RAISED,bd=7)
    backward_btn_img.place(x=25,y=350)

    play_image_take = ImageTk.PhotoImage(Image.open('Pictures/play.png'))
    play_btn_img = Button(window,image=play_image_take,bg="white",relief=RAISED,bd=7)
    play_btn_img.place(x=115,y=350)

    pause_image_take = ImageTk.PhotoImage(Image.open('Pictures/pause.png'))
    pause_btn_img = Button(window,image=pause_image_take,bg="pink",relief=RAISED,bd=7)
    pause_btn_img.place(x=210,y=350)

    stop_image_take = ImageTk.PhotoImage(Image.open('Pictures/stop.jpg'))
    stop_btn_img = Button(window,image=stop_image_take,bg="white",relief=RAISED,bd=7)
    stop_btn_img.place(x=305,y=350)

    forward_image_take = ImageTk.PhotoImage(Image.open('Pictures/forward.png'))
    forward_btn_img = Button(window,image=forward_image_take,bg="yellow",relief=RAISED,bd=7)
    forward_btn_img.place(x=400,y=350)

    MusicPlayer(window,backward_btn_img,play_btn_img,pause_btn_img,stop_btn_img,forward_btn_img)

    window.mainloop()
