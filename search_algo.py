import networkx as nx
from tkinter import *
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random
import tkinter as tk
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#####################################################################################################
#                                         N O T E S                                                #
####################################################################################################
#input from user should be entered in a way such that smaller numbers come first
#####################################################################################################
#                                    START OF GRAPHING                                              #
####################################################################################################
class GraphVisualization:

    def __init__(self):
        self._edgeList = []

    def addEdge(self, node, adj):
        temp_edge = [node, adj]
        self._edgeList.append(temp_edge)

    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self._edgeList)
        nx.draw_networkx(G)
        plt.show()



#####################################################################################################
#                                    END OF GRAPHING                                                #
####################################################################################################
class DFS:
    def __init__(self,user_input):
        self._adj = []
        for x in user_input:
            self._adj.append(list(map(int,x.split(' '))))
        print(user_input)
        print(self._adj)
        self._edg = []
        count = 0
        for lst in self._adj:
            for x in lst:
                print([count, x])
                self._edg.append([count, x])
            count += 1
        self._Gr = nx.Graph()
        self._Gr.add_edges_from(self._edg)
        self._visited = ['false'] * self._Gr.number_of_nodes()
        self._l=[]
        self._colors=['blue'] * self._Gr.number_of_nodes()
        self._layout = nx.spring_layout(self._Gr)
        temp = self._Gr.number_of_nodes() - len(self._adj)
        for i in range(temp):
            self._adj.append([])
        print("TEMP",temp)

    def display(self):
        print(self._adj)

    def dfs(self,node):
        self._visited[node] = 'ture'
        self._l.append(node)
        print(node)
        for x in self._adj[node]:
                self.dfs(int(x))

    def updata(self,frames, a):
        a.clear()
        self._colors[self._l[frames]] = 'orange'
        # l.remove(0)
        print(self._l[frames])
        print(self._l)

        nx.draw_networkx(self._Gr, pos=self._layout, node_color=self._colors, ax=a)
        # Set the title
        a.set_title("Frame {}".format(frames))
        if frames == len(self._l)-1:
            self._colors = ['blue'] * self._Gr.number_of_nodes()

    '''
            def dfs(node, visited, adjList, l):
            visited[node] = 'true';
            l.append(node)
            print(l)
            print(node, end=" ")
            for x in adjList[node]:
                if visited[x] == 'false':
                    dfs(x, visited, adjList, l)
            return l
    '''

    #def draw_graph(self):

    def anim(self):
        fig = plt.Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        plt.axis('off')
        #nx.draw_networkx(self._Gr, pos=self._layout, ax=ax)
        canvas = FigureCanvasTkAgg(fig, frm_left)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
        print(len(self._l))
        ani = animation.FuncAnimation(fig, self.updata, frames= len(self._l), interval=400, fargs={ax})
        canvas = FigureCanvasTkAgg(fig, frm_left)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
       # plt.show()
        #ani.save('animation_1.gif', writer='imagemagick')
        #plt.show()


#####################################################################################################
#                                    START OF LOGIC                                                 #
####################################################################################################
def dfs(node, visited, adjList):
    visited[node] = 'true';
    print(node,end=" ")
    for x in adjList[node]:
        if visited[x] == 'false':
            dfs(x,visited,adjList)



#####################################################################################################
#                                    END OF LOGIC                                                   #
####################################################################################################
def onClickRun(user_txtBox,type_var):
  input = user_txtBox.get("1.0", "end-1c").split('\n')
  if(type_var == 1):
      dfs_inst = DFS(input)
      dfs_inst.display()
      #dfs_inst.draw_graph()
      dfs_inst.dfs(0)
      dfs_inst.anim()
      print(dfs_inst._l)
  print(input , 'yaAllah' , type_var)
#####################################################################################################
#                                    START OF GUI                                                   #
####################################################################################################
root = Tk()
root.title("Search Methods Visualizer")

frm_right = tk.Frame()
lbl_uninformedSearch = tk.Label(master=frm_right, text="Uninformed Search", foreground="#CD5C5C")
# ent = tk.Entry(master=frm_right, fg="#CD5C5C", width=50)
var = IntVar()
r1 = Radiobutton(master=frm_right, text="dfs", variable=var, value=1)
r2 = Radiobutton(master=frm_right, text="bfs", variable=var, value=2)
r3 = Radiobutton(master=frm_right, text="dijkstra", variable=var, value=3)
r4 = Radiobutton(master=frm_right, text="lim_dfs", variable=var, value=4)
r5 = Radiobutton(master=frm_right, text="itr_dfs", variable=var, value=5)
txt = tk.Text(master=frm_right, height=5, width=20)
btn_Run = tk.Button(master=frm_right, text="Run",command=lambda:onClickRun(txt,var.get()) , width=15, height=1, fg="#CD5C5C")
lbl_uninformedSearch.grid(row=0, column=0, padx=5, pady=5)
r1.grid(row=1, column=0, padx=5, pady=1)
r2.grid(row=2, column=0, padx=5, pady=1)
r3.grid(row=3, column=0, padx=5, pady=1)
r4.grid(row=4, column=0, padx=5, pady=1)
r5.grid(row=5, column=0, padx=5, pady=1)
txt.grid(row=6, column=0, padx=5, pady=1)
# ent.grid(row=1, column=0, padx=5, pady=5)
btn_Run.grid(row=7, column=0, padx=5, pady=5)

frm_left = tk.Frame()
lbl_top = tk.Label(master=frm_left, text="Title", foreground="#CD5C5C")
#txt = tk.Text(master=frm_left)
lbl_bottom = tk.Label(master=frm_left, text="Written Results", foreground="#CD5C5C")
lbl_top.grid(row=0, column=0, padx=5, pady=5)
#txt.grid(row=1, column=0, padx=5, pady=5, )
lbl_bottom.grid(row=2, column=0, padx=5, pady=5)

frm_right.grid(row=0, column=1, padx=5, pady=5)
frm_left.grid(row=0, column=0, padx=5, pady=5)

'''
f = plt.Figure(figsize=(5,4))
a = f.add_subplot(111)
plt.axis('off')

G = nx.Graph()
edgeList = []
edgeList.append([0, 1])
edgeList.append([1, 2])
edgeList.append([2, 3])
edgeList.append([2, 4])
G.add_edges_from(edgeList)
#options = {"font_size": 36, "node_size": 3000, "node_color": "white", "edgecolors": "black", "linewidths": 5, "width": 5,}
#nx.draw_networkx(G,**options,pos=nx.spring_layout(G),ax=a)
nx.draw_networkx(G,pos=nx.spring_layout(G),ax=a)

#plt.show()
#nx.draw_networkx(G)

#.draw()
#plt.gcf().canvas.draw()
#plt.show()
canvas = FigureCanvasTkAgg(f,frm_left)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0)
#plt.draw()
'''



adjList = [[1],[2],[3],[4],[]]
visited = ['false','false','false','false','false']
dfs(0,visited,adjList)
print("DONE?")
root.mainloop()
#####################################################################################################
#                                    END OF GUI                                                     #
####################################################################################################
# plt.show()





