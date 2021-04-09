import networkx as nx
from tkinter import *
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#####################################################################################################
#                                         N O T E S                                                #
####################################################################################################
#TO_DO : Take input from user and parse it
#TO_DO : Print solution in result label
#TO_DO : Di_Graph
'''
1 2 3 4
4 5
6 7
8 9
10 11
12 13
14 15
16 17
18
19 20
21 22
23 24
'''

class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
    def __str__(self):
        return str(self.value)
#####################################################################################################
#                                        START OF DFS                                              #
####################################################################################################
class DFS:
    def __init__(self, user_input):
        '''
        self.graph = {'A': ['B', 'D'],
                'B': ['C'],
                'D': ['C'],
                }
        '''
        self.graph = {0: [1, 2, 3, 4],
                      1: [4, 5],
                      2: [6, 7],
                      3: [8, 9],
                      4: [10, 11],
                      5: [12, 13],
                      6: [14, 15],
                      7: [16, 17],
                      8: [18],
                      9: [19, 20],
                      10: [21, 22],
                      11: [23, 24],
                      }
        self._Gr = nx.Graph()
        for key_node in self.graph:
            self._Gr.add_node(key_node)
            print(self.graph[key_node])
            for adj in self.graph[key_node]:
                self._Gr.add_node(adj)
                self._Gr.add_edge(key_node, adj)
        self._l = []
        self.shortestPath = []
        self._colors = ['blue'] * self._Gr.number_of_nodes()
        # self._layout = nx.spring_layout(self._Gr,scale=30, k=1/math.sqrt(self._Gr.order()))
        self._layout = nx.spring_layout(self._Gr)

    def trace(self, goal):
        if goal.parent is None:
            print(goal.value, end=" ")
            self.shortestPath.append(goal.value)
            return
        self.trace(goal.parent)
        self.shortestPath.append(goal.value)
        print(" -> ", goal.value, end=" ")

    def dfs(self, init, goal):
        visited = []
        stack = []
        stack.append(Node(init))
        if init is goal:
            print("Initial is goal")
            return
        while stack:
            curr_node = stack.pop()
            visited.append(curr_node.value)
            if curr_node.value not in self._l:
                self._l.append(curr_node.value)
                print("visitied ", visited)
            for adj in self.graph.get(curr_node.value) or []:
                # if not in stack (but node vs value)
                # https://stackoverflow.com/questions/55042460/comparing-user-defined-objects-in-two-lists
                print("SSSSS")
                if adj not in visited:
                    print("ERE")
                    temp = Node(adj, curr_node)
                    if adj is goal:
                        self._l.append(goal)
                        self.trace(temp)
                        print()
                        return
                    stack.append(temp)
            for node in stack:
                print(node.value, end=" ")
            print()
        print("Goal not found")
        return

    def update(self, frames, a):
        a.clear()
        if (frames < len(self._l)):
            # print(self._Gr.node[self._l[frames]])
            i = 0
            for node in self._Gr.nodes:
                print(node, " ", self._l[frames])
                if node is self._l[frames]:
                    break
                i += 1
            self._colors[i] = 'orange'
           # print(self._l[frames])
           # print(self._l)
            nx.draw_networkx(self._Gr, pos=self._layout, node_color=self._colors, ax=a)
            # Set the title
            a.set_title("Frame {}".format(frames))
        else:
            a.clear()
            i = 0
            for node in self._Gr.nodes:
                print(node, " ", self.shortestPath[frames - len(self._l)])
                if node is self.shortestPath[frames - len(self._l)]:
                    break
                i += 1
            self._colors[i] = 'red'
            nx.draw_networkx(self._Gr, pos=self._layout, node_color=self._colors, ax=a)
            a.set_title("Frame {}".format(frames))

        if frames == len(self._l + self.shortestPath) - 1:
            self._colors = ['blue'] * self._Gr.number_of_nodes()

    def anim(self):
        fig = plt.Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        plt.axis('off')
        # nx.draw_networkx(self._Gr, pos=self._layout, ax=ax)
        canvas = FigureCanvasTkAgg(fig, frm_left)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
        print(len(self._l))
        ani = animation.FuncAnimation(fig, self.update, frames=len(self._l + self.shortestPath), interval=400,fargs={ax})
        canvas = FigureCanvasTkAgg(fig, frm_left)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)


#####################################################################################################
#                                         END OF DFS                                                #
####################################################################################################



#####################################################################################################
#                               START OF BUTTON EVENT LISTENER                                      #
####################################################################################################

def onClickRun(user_txtBox, type_var):
  input = user_txtBox.get("1.0", "end-1c").split('\n')
  if(type_var == 1):
      dfs_inst = DFS(input)
      dfs_inst.dfs(0,15)
    #  dfs_inst.dfs('A','C')
      dfs_inst.anim()
      print(dfs_inst._l)
  print(input , 'whatever' , type_var)

#####################################################################################################
#                              END OF OF BUTTON EVENT LISTENER                                     #
####################################################################################################

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
lbl_bottom = tk.Label(master=frm_left, text="Written Results", foreground="#CD5C5C")
lbl_top.grid(row=0, column=0, padx=5, pady=5)
lbl_bottom.grid(row=2, column=0, padx=5, pady=5)

frm_right.grid(row=0, column=1, padx=5, pady=5)
frm_left.grid(row=0, column=0, padx=5, pady=5)

root.mainloop()
#####################################################################################################
#                                    END OF GUI                                                     #
####################################################################################################







