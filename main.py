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

class Node():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.plot = None
        
    def setPlot(self, plot):
        self.plot = plot
        
class ClusterNode(Node):
    
    def __init__(self, x, y):
        super().__init__(x, y)
        
    def setColor(self, color):
        self.plot.set_color(color)
        
class CenterNode(Node):
    
    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.color = color
        self.cluster = []
        
    def removePlot(self):
        self.plot.remove()
        
    def addClusterNode(self, clusterNode):
        self.cluster.append(clusterNode)
        
    def resetCluster(self):
        self.cluster.clear()
        
class K_mean():
    
    def __init__(self):
        self.clusterNodes = []    # record ClusterNode
        self.centerNodes = []   # record CenterNode             
        self.ani = None
        
    def clearPlot(self):
        plt.clf()
        plt.title("Data Distribution", fontsize=28)
        plt.xlabel('x asix', fontsize=20)
        plt.ylabel('y asix', fontsize=20)
        plt.xlim(-1200, 1200)
        plt.ylim(-1200, 1200)
        
    def gen_data(self):
        
        # clear plot
        self.clearPlot()
        
        # generate points--------------------------------------------
        for _ in range(clusters_num.get()): #群數
            center_x = np.random.randint(-1000, 1000)
            center_y = np.random.randint(-1000, 1000)
            for _ in range(np.random.randint(20, 50)): #一群的點數
                new_x = center_x + np.random.uniform(-120, 120)
                new_y = center_y + np.random.uniform(-120, 120)
                
                point = ClusterNode(new_x, new_y)
                point.setPlot(plt.plot(point.x, point.y, 'o', ms=3 , color = 'gray', alpha=1)[0]) # ms: point size   
                self.clusterNodes.append(point)   
                
        canvas.draw()
        
    def start(self):   
        self.ani = animation.FuncAnimation(fig=fig, func=self.update, frames=self.frames, init_func = self.init, interval=1200, blit=False, repeat=False) #動畫
        canvas.draw()
        
    def init(self): 

        for i in range(clusters_num.get()): #群心
            center_x = np.random.randint(-1000, 1000)
            center_y = np.random.randint(-1000, 1000)
            point = CenterNode(center_x, center_y, color[i])
            point.setPlot(plt.plot(point.x, point.y, 'o', ms=5 , color = color[i], alpha=1)[0]) 
            self.centerNodes.append(point)

        canvas.draw()
        
    def update(self, i):
        if(i==0):
            for centerNode in self.centerNodes:
                cluster = centerNode.cluster
                numData = len(cluster)

                if(numData!=0):
                    sumX = 0
                    sumY = 0
                    
                    for clusterNode in cluster:
                        sumX += clusterNode.x
                        sumY += clusterNode.y   
                        
                    centerNode.removePlot()
                    centerNode.x = sumX/numData
                    centerNode.y = sumY/numData
                    centerNode.setPlot(plt.plot(centerNode.x, centerNode.y, 'o', ms=5 , color = centerNode.color, alpha=1)[0]) 
                
        elif(i==1):
            self.clearPlot()

            for centerNode in self.centerNodes:
                centerNode.setPlot(plt.plot(centerNode.x, centerNode.y, 'o', ms=5 , color = centerNode.color, alpha=1)[0])
                centerNode.resetCluster()
                
            for clusterNode in self.clusterNodes:
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
        self.clearPlot()
        
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
tk.Label(setting1, font=("Calibri", 15, "bold"), text="Number of clusters:", bg="#F0FFF0").pack(side='left', padx=5)
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