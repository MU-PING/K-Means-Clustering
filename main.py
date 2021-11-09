"""
Created on Tue Nov 24 22:02:29 2020

@author: Mu-Ping
"""

import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import animation

class k_mean():
    def __init__(self):
        self.data = []
        self.center = []        #群心
        self.center_data = None #群心資料
        self.plot = []          #群心圖
        
    def gen_data(self):
        plt.clf()
        plt.title("Data")
        
        data=[]
        for _ in range(cluster.get()): #群數
            center_x = np.random.randint(-350, 350)
            center_y = np.random.randint(-350, 350)
            for _ in range(np.random.randint(20, 50)): #一群的點數
                new_x = center_x + np.random.uniform(-35, 35)
                new_y = center_y + np.random.uniform(-35, 35)
                data.append([new_x, new_y])
                plt.plot(new_x, new_y, 'o', ms=5 , color = 'gray', alpha=1) #畫圖 ms：折點大小
        self.data = np.array(data)
        canvas.draw()
        
        
    def start(self):   
        self.center_data = [[] for _ in range(cluster.get())]
        ani = animation.FuncAnimation(fig=fig, func=self.update, frames=self.frames, init_func = self.init, interval=1200, blit=False, repeat=False) #動畫
        canvas.draw()
        
    
    def init(self): 
        for i in range(cluster.get()): #群心
            center_x = np.random.randint(-290, 290)
            center_y = np.random.randint(-290, 290)
            self.center.append((center_x, center_y))
            self.plot.append(plt.plot(center_x, center_y, 'o', ms=7 , color = color[i], alpha=1)) 
            
    def update(self, i): #2維資料更新參數
        if(i==0):
            for i in self.plot:
                i[0].remove()
            self.plot=[]
            
            for i in range(cluster.get()): #更新群心
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
            self.center_data = [[] for _ in range(cluster.get())]
            for i in range(cluster.get()):
                self.plot.append(plt.plot(self.center[i][0], self.center[i][1], 'o', ms=5 , color = color[i], alpha=1))
            
            for i in self.data:                 #更新資料
                min_x = 0
                min_y = 0
                min_distance = float("inf")
                min_index = 0
                for center_index in range(cluster.get()):
                    distance = ((self.center[center_index][0]-i[0])**2 + (self.center[center_index][1]-i[1])**2)**0.5 # 採取歐基里德距離，其他評估標準亦可
                    if(distance < min_distance):
                        min_x = i[0]
                        min_y = i[1]
                        min_distance = distance
                        min_index = center_index
                        
                self.center_data[min_index].append([min_x, min_y]) 
                plt.plot(i[0], i[1], 'o', ms=5 , color = color[min_index], alpha=.2) 
            
            
    def frames(self): # 禎數生成器
        for i in range(60):
            yield i%2

window = tk.Tk()
window.geometry("480x390")
window.resizable(False, False)
window.title("k-means 演算法")

#全域變數
cluster = tk.IntVar()#群
cluster.set(3)
color = ["#FF0000", "#0000E3", "#FFD306", "#F75000", "#02DF82", "#6F00D2", "#73BF00"]
brain = k_mean()

setting1 = tk.Frame(window)
setting1.grid(row=0, column=0, padx=10, pady=10)
tk.Label(setting1, font=("微軟正黑體", 12, "bold"), text="群數(k值)").grid(row=0, sticky=tk.W, pady=5)
tk.Entry(setting1, width=10, textvariable=cluster).grid(row=1, sticky=tk.W)

btn = tk.Button(setting1, text='隨機產生資料', command = brain.gen_data)
btn.grid(row=8, sticky=tk.W, pady=20)
btn = tk.Button(setting1, text='開始分類', command = brain.start)
btn.grid(row=9, sticky=tk.W)

setting2 = tk.Frame(window)
setting2.grid(row=0, column=1, pady=10)
fig = plt.figure(figsize=(5,5))
plt.title("Data")
canvas = FigureCanvasTkAgg(fig, setting2)  # A tk.DrawingArea.
canvas.get_tk_widget().grid()

window.mainloop()
