# -*- coding: utf-8 -*-
'''
迷宫生成例子
ienlaw
2017-08-31
'''
__author__ = 'IENLAW'


import os, time, random
from Tkinter import *

class base_maze_grid(object):
    
    def __init__(self):
        self.access = False
        self.up = False
        self.down = False
        self.left = False
        self.right = False

class generate_maze(object):
    
    def __init__(self, high=20, wide=20):
        self.high = high
        self.wide = wide

        self.show_maze_gui()
        
        
    def init_maze(self):
        u'''初始化迷宫'''
        self.maze = list()
        self.maze_path = []
        self.high = int(self.grid_sum.get())
        self.wide = int(self.grid_sum.get())
    
    
        for i in range(self.high):
            temp = []
            for i1 in range(self.wide):
                temp.append(base_maze_grid())
            self.maze.append(temp)
        
     
    def mode_recursive_backtracker(self):
        u'''递归回溯算法'''
        self.init_maze()            
            
        history = list()
        current = (0,0)
        self.maze[current[0]][current[1]].access = True

        while len([False for i in self.maze for i1 in i if i1.access == False]) > 0 :
            adjacent_grid = self.get_adjacent_grid(current)
            if adjacent_grid:
                new_grid = random.choice(adjacent_grid)
                history.append(current)
                self.get_through(current,new_grid)
                current = new_grid
                self.maze[current[0]][current[1]].access = True
            elif history:
                current = history.pop()
            if not self.maze_path:
                if current == (self.high-1, self.wide-1):                          
                    self.maze_path = history[:]
                    self.maze_path.append(current)
                    # print len(self.maze_path)
                    
        self.draw_maze()
                    
    def get_adjacent_grid(self, xy):
        u'''获取附近未访问的格子'''
        temp = []

        for xy_int in [(xy[0]+1,xy[1]), (xy[0]-1,xy[1]), (xy[0],xy[1]+1), (xy[0],xy[1]-1)]:
            if 0 <= xy_int[0] <= self.high-1 and 0 <= xy_int[1] <= self.wide-1:                
                if not self.maze[xy_int[0]][xy_int[1]].access:
                    temp.append(xy_int)
        
        return temp
    
    def get_through(self, a, b):
        u'''打通格子的墙'''
        if a[0] < b[0]:
            self.maze[a[0]][a[1]].right = True
            self.maze[b[0]][b[1]].left = True
        elif a[0] > b[0]:
            self.maze[a[0]][a[1]].left = True
            self.maze[b[0]][b[1]].right = True       

        if a[1] < b[1]:
            self.maze[a[0]][a[1]].down = True
            self.maze[b[0]][b[1]].up = True
        elif a[1] > b[1]:
            self.maze[a[0]][a[1]].up = True
            self.maze[b[0]][b[1]].down = True
            
            
    def show_maze_gui(self):
        u'''显示迷宫界面'''
        root=Tk()
        root.title('Maze Example')
        self.cwidth = 750
        self.cheight = 750
        control1 = LabelFrame(root) # 实例化 Frame容器
        control1['text'] = u'设置格数'
        default_value = StringVar()
        default_value.set('20')
        self.grid_sum = Entry(control1, textvariable = default_value)
        self.grid_sum.pack(side=LEFT, expand=YES,fill=X)
        control1.pack(fill=X,padx=5,pady=5)
        control = LabelFrame(root) # 实例化 Frame容器
        control['text'] = u'迷宫控制'
        self.start = Button(control, text=u'生成迷宫',command=self.mode_recursive_backtracker)
        self.start.pack(fill=X)
        self.show_path = Button(control, text=u'显示路线',command=self.draw_path)
        self.show_path.pack(side=LEFT, expand=YES,fill=X)
        self.show_path = Button(control, text=u'隐藏路线',command=self.draw_maze)
        self.show_path.pack(side=LEFT, expand=YES,fill=X)
        control.pack(fill=X,padx=5,pady=5)
        
        self.canvas = Canvas(root,width=self.cwidth+1, height=self.cheight+1, bg='white') 
        self.canvas.pack()
        
        self.mode_recursive_backtracker()
        
        root.mainloop()
        
    def draw_maze(self):
        u'''画出迷宫'''
        self.canvas.create_rectangle( 0, 0 , self.cwidth+5, self.cheight+5,fill='white')
        xspacing = self.cheight/self.high
        yspacing = self.cwidth/self.wide
        
        self.maze[0][0].left = True
        self.maze[-1][-1].right = True
        
        
        a_x = 2
        a_y = 2
        self.temp={}
        for x,i in enumerate(self.maze):
            for y,i1 in enumerate(i):                    
                if not self.maze[x][y].up:
                    self.canvas.create_line(a_x, a_y, a_x+xspacing, a_y)
                if not self.maze[x][y].down:
                    self.canvas.create_line(a_x, a_y+yspacing, a_x+xspacing, a_y+yspacing)
                if not self.maze[x][y].left:
                    self.canvas.create_line(a_x, a_y, a_x, a_y+yspacing)
                if not self.maze[x][y].right:
                    self.canvas.create_line(a_x+xspacing, a_y, a_x+xspacing, a_y+yspacing)                
                if (x, y) in self.maze_path :
                    # self.canvas.create_oval(a_x+(xspacing/4), a_y+(yspacing/4), a_x+xspacing-xspacing/4, a_y+yspacing-yspacing/4, fill = "green")
                    self.temp[(x, y)]=(a_x+xspacing/2, a_y+yspacing/2)
                a_y += yspacing                
            a_y = 2
            a_x += xspacing
            
    def draw_path(self):
        u'''画出迷宫路径'''
        for i,s in enumerate(self.maze_path[:-1]):
            self.canvas.create_line(self.temp[s][0], self.temp[s][1], self.temp[self.maze_path[i+1]][0], self.temp[self.maze_path[i+1]][1], fill = "green")

         

    
if __name__ == "__main__":
    m = generate_maze()
    
    
