from numpy import abs
from random import (randrange, choice)
import tkinter as tk
import os
import sys


class Game_Mechanics:    
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    def pull_images(self):
        self.player_up_image_source = tk.PhotoImage(file=self.resource_path("img/human_fa_up.gif"))
        self.player_down_image_source = tk.PhotoImage(file=self.resource_path("img/human_fa_down.gif"))
        self.player_left_image_source = tk.PhotoImage(file=self.resource_path("img/human_fa_left.gif"))
        self.player_right_image_source = tk.PhotoImage(file=self.resource_path("img/human_fa_right.gif"))
        self.world_border_image_source = tk.PhotoImage(file=self.resource_path("img/border_stone.gif"))                     
        self.ground_grass_image_source = tk.PhotoImage(file=self.resource_path("img/ground_grass.gif"))
    def timer_clock(self): 
        self.tk_frame.delete(tk.ALL) 
        self.game_clock += 1
        if self.game_clock >= 10:
            self.game_clock = 0
        self.write_view_frame()
        self.draw_view_frame()
        self.tk_frame.after(self.game_delay, self.timer_clock)
    def key_pressed(self, tk_command):
        self.tk_frame = tk_command.widget.tk_frame
        if (tk_command.char == "p") and (self.instance == 0):
            self.write_first_instance() 
        if tk_command.keysym == "Up": 
            self.move_player(-1, 0) 
        if tk_command.keysym == "Down":
            self.move_player(+1, 0) 
        if tk_command.keysym == "Left":
            self.move_player(0,-1) 
        if tk_command.keysym == "Right":
            self.move_player(0,+1)

class World_Modeling:
    def write_board(self):
        self.grid_list = []
        for row in range(self.board_size): 
            self.grid_list += [[0] * self.board_size] 
        for row in range(self.board_size-40): 
            self.grid_list[20][row+20] = 40
            self.grid_list[self.board_size-20][row+20] = 40  
        for col in range(self.board_size-39):
            self.grid_list[col+20][20] = 40
            self.grid_list[col+20][self.board_size-20] = 40 
    def write_view_frame(self):
        self.view_list = []
        self.view_h_size = 10
        self.view_w_size = 14
        for i in range(self.view_h_size):
            self.view_list += [self.grid_list[i+(self.player_row_pos+1-int(self.view_h_size/2))][self.player_col_pos+1-int(self.view_w_size/2):self.player_col_pos+1+int(self.view_w_size/2)]]
    def draw_view_frame(self):
        for i_row in range(self.view_h_size): 
            for f_col in range(self.view_w_size):
                rect_left = 5 + f_col * self.object_size+ 12
                rect_right = rect_left + self.object_size + 12
                rect_top = 5 + i_row * self.object_size + 110
                rect_bottom = rect_top + self.object_size + 110
                if self.view_list[i_row][f_col] == 1:
                    self.add_background(rect_left, rect_top)
                    self.draw_player_frame(rect_left, rect_top)
                if self.view_list[i_row][f_col] == 40: 
                    self.add_background(rect_left, rect_top)
                    self.tk_frame.create_image(rect_left+10, rect_top+10, image=self.world_border_image_source)
                if self.view_list[i_row][f_col] == 0: 
                    self.add_background(rect_left, rect_top)
                if self.view_list[i_row][f_col] == 41: 
                    self.add_background(rect_left, rect_top)
                    self.tk_frame.create_image(rect_left+10, rect_top+10, image=self.bush_wall_image_source)
                self.tk_frame.create_text(50,200, text=self.game_clock, fill="black")
    def add_background(self, rect_left, rect_top):
        self.tk_frame.create_image(rect_left+10, rect_top+10, image=self.ground_grass_image_source)
    def write_first_instance(self):
        self.write_board() 
        self.move_player(0,0)
        self.timer_clock()
    def write_ui_instance(self): 
        self.instance = 0
        self.tk_frame.create_text(self.frame_width/2, (self.frame_height/2) - 250, 
                                  text='x v.x', fill="black")
        self.tk_frame.create_text(self.frame_width/2, (self.frame_height/2) - 200, 
                                  text='Press P to play', fill="black")
        self.tk_frame.create_text(self.frame_width/2, (self.frame_height/2) - 150, 
                                  text='x', fill="black")
        self.tk_frame.create_text(self.frame_width/2, (self.frame_height/2) - 100, 
                                  text='x', fill="black")
        self.tk_frame.create_text(self.frame_width/2, (self.frame_height/2) - 50, 
                                  text='x', fill="black")
        self.tk_frame.create_text(self.frame_width/2, (self.frame_height/2), 
                                  text='x)', fill="black")
        
class Player_Method:    
    player_row_pos = 45
    player_col_pos = 45
    def draw_player_frame(self, rect_left, rect_top):
        if self.player_row_vec == -1 and self.player_col_vec == 0:
            self.tk_frame.create_image(rect_left+10, rect_top+10, image=self.player_up_image_source)
        elif self.player_row_vec == 1 and self.player_col_vec == 0:
            self.tk_frame.create_image(rect_left+10, rect_top+10, image=self.player_down_image_source)
        elif self.player_row_vec == 0 and self.player_col_vec == -1:
            self.tk_frame.create_image(rect_left+10, rect_top+10, image=self.player_left_image_source)
        elif self.player_row_vec == 0 and self.player_col_vec == 1:
            self.tk_frame.create_image(rect_left+10, rect_top+10, image=self.player_right_image_source)
        else:
            self.tk_frame.create_image(rect_left+10, rect_top+10, image=self.player_down_image_source)      
    
    def move_player(self, dist_row, dist_col):
        self.player_row_vec = dist_row
        self.player_col_vec = dist_col
        if self.grid_list[self.player_row_pos + dist_row][self.player_col_pos + dist_col] == 0: 
            self.grid_list[self.player_row_pos][self.player_col_pos] = 0
            self.player_row_pos = self.player_row_pos + dist_row
            self.player_col_pos = self.player_col_pos + dist_col
            self.grid_list[self.player_row_pos][self.player_col_pos] = 1
class Game_Init(tk.Tk, Game_Mechanics, World_Modeling, Player_Method):
    game_delay = 71 
    game_clock = 0 
    object_size = 40
    board_size = 100
    view_size = 14
    message_log_size = 100
    frame_width = 2*5 + view_size * object_size 
    frame_height = 2*5 + view_size * object_size + message_log_size
    def __init__(self):
        super().__init__()
        self.bind("<Key>", self.key_pressed)
        self.tk_frame = tk.Canvas(self, width=self.frame_width, height=self.frame_height) 
        self.tk_frame.pack()
        self.pull_images()
        self.write_ui_instance()
        self.eval('tk::PlaceWindow %s center' % self.winfo_pathname(self.winfo_id()))
init_grid = Game_Init()
init_grid.mainloop()