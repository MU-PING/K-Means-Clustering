"""
Created on Tue Nov 24 22:02:29 2020

@author: Mu-Ping
"""
import math
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

from tkinter import ttk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import animation

class PointNode():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.plot = None
        
    def setPlot(self, plot):
        self.plot = plot
        
    def beSelected(self):
        self.plot.set_color("#ff7f0e")
        
    def beProcessed(self):
        self.plot.set_color("#d62728")
        
class K_mean():
    
    def __init__(self):
        self.data = []
        self.center = []       
        self.center_data = None 
        self.plot = []          
        self.ani =None
        
        
    def gen_data(self):
        
        # set plot
        plt.clf()
        plt.title("Data Distribution", fontsize=28)
        plt.xlabel('x asix', fontsize=20)
        plt.ylabel('y asix', fontsize=20)
        plt.xlim(-1200, 1200)
        plt.ylim(-1200, 1200)
        
        # generate points--------------------------------------------
        data=[]
        for _ in range(clusters_num.get()): #群數
            center_x = np.random.randint(-1000, 1000)
            center_y = np.random.randint(-1000, 1000)
            for _ in range(np.random.randint(20, 50)): #一群的點數
                new_x = center_x + np.random.uniform(-120, 120)
                new_y = center_y + np.random.uniform(-120, 120)
                
                data.append(PointNode(new_x, new_y))
                plt.plot(new_x, new_y, 'o', ms=5 , color = 'gray', alpha=1) #畫圖 ms：折點大小
        self.data = np.array(data)
        canvas.draw()
        
    def start(self):   
        self.center_data = [[] for _ in range(clusters_num.get())]
        self.ani = animation.FuncAnimation(fig=fig, func=self.update, frames=self.frames, init_func = self.init, interval=1200, blit=False, repeat=False) #動畫
        canvas.draw()
        
    def init(self): 

        for i in range(clusters_num.get()): #群心
            center_x = np.random.randint(-1000, 1000)
            center_y = np.random.randint(-1000, 1000)
            self.center.append((center_x, center_y))
            self.plot.append(plt.plot(center_x, center_y, 'o', ms=7 , color = color[i], alpha=1)[0]) 
        
        canvas.draw()
        
    def update(self, i):
        if(i==0):
            for i in self.plot:
                i[0].remove()
            self.plot=[]
            
            for i in range(clusters_num.get()): #更新群心
                data_count = 0
                sum_x = 0
                sum_y = 0
                for j in self.center_data[i]:
                    sum_x+=j[0]
                    sum_y+=j[1]
                    data_count+=1
                    
                if(data_count==0):
                    self.center[i] = self.center[i]
                else:
                    self.center[i] = [sum_x/data_count, sum_y/data_count]
                self.plot.append(plt.plot(self.center[i][0], self.center[i][1], 'o', ms=5 , color = color[i], alpha=1))
                
        elif(i==1):
            plt.clf()
            plt.title("Data")
            
            self.plot=[]
            self.center_data = [[] for _ in range(clusters_num.get())]
            for i in range(clusters_num.get()):
                self.plot.append(plt.plot(self.center[i][0], self.center[i][1], 'o', ms=5 , color = color[i], alpha=1))
            
            for i in self.data:                 #更新資料
                min_x = 0
                min_y = 0
                min_distance = float("inf")
                min_index = 0
                for center_index in range(clusters_num.get()):
                    distance = ((self.center[center_index][0]-i[0])**2 + (self.center[center_index][1]-i[1])**2)**0.5 # 採取歐基里德距離，其他評估標準亦可
                    if(distance < min_distance):
                        min_x = i[0]
                        min_y = i[1]
                        min_distance = distance
                        min_index = center_index
                        
                self.center_data[min_index].append([min_x, min_y]) 
                plt.plot(i[0], i[1], 'o', ms=5 , color = color[min_index], alpha=.2) 
            
    def frames(self):
        for i in range(60):
            yield i%2

    def stop(self):
        # stop animation
        self.ani.event_source.stop()
        
        self.clearStructure()
        
        # set plot
        plt.clf()
        plt.title("Data Distribution", fontsize=28)
        plt.xlabel('x asix', fontsize=20)
        plt.ylabel('y asix', fontsize=20)
        plt.xlim(-1200, 1200)
        plt.ylim(-1200, 1200)
        
        # make points--------------------------------------------
        for point in self.points:
            point.setPlot(plt.plot(point.x, point.y, 'o', ms=5 , color = '#1f77b4', alpha=1)[0]) # ms: point size
            
        canvas.draw()
        
# disable Buttom & Entry
def disable(component):
    component['state'] = 'disable'

def enable(component):
    component['state'] = 'normal'
    
window = tk.Tk()
window.geometry("750x650")
window.resizable(False, False)
window.title("K-means-clustering Algorithm ")
window.configure(bg='#E6E6FA')

# Global var
clusters_num = tk.IntVar()
clusters_num.set(5)
color = ["#FF0000", "#0000E3", "#FFD306", "#F75000", "#02DF82", "#6F00D2", "#73BF00"]

# tk Frame
setting1 = tk.Frame(window, bg="#F0FFF0")
setting1.pack(side='top', pady=10)
separator = ttk.Separator(window, orient='horizontal')
separator.pack(side='top', fill=tk.X)
setting2 = tk.Frame(window)
setting2.pack(side='top', pady=10)

# Plot
fig = plt.figure(figsize=(9, 8))
canvas = FigureCanvasTkAgg(fig, setting2)  # A tk.DrawingArea.
canvas.get_tk_widget().grid()

# Algorithm
brain = K_mean()
brain.gen_data()

# GUI
tk.Label(setting1, font=("Calibri", 15, "bold"), text="Clusters:", bg="#F0FFF0").pack(side='left', padx=5)
ent = tk.Entry(setting1, width=5, textvariable=clusters_num)
ent.pack(side='left')
btn1 = tk.Button(setting1, font=("Calibri", 12, "bold"), text='Generate points', command=lambda:[brain.gen_data()])
btn1.pack(side='left', padx=(10, 5), pady=5)
btn2 = tk.Button(setting1, font=("Calibri", 12, "bold"), text='Start clustering', command=lambda:[brain.start(), disable(btn1), disable(btn2), disable(ent),  enable(btn3)])
btn2.pack(side='left', padx=(5, 10), pady=5)
btn3 = tk.Button(setting1, font=("Calibri", 12, "bold"), text='Reset', command=lambda:[brain.stop(), enable(btn1), enable(btn2), enable(ent), disable(btn3)])
btn3.pack(side='left', padx=(5, 10), pady=5)
btn3['state'] = 'disable'

window.mainloop()