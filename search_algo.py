import networkx as nx
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib import animation
from queue import Queue
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#####################################################################################################
#                                         N O T E S                                                #
####################################################################################################
#TO_DO : Handel cases when goals is not found and goal equals start
#TO_DO : Di_Graph
'''
0 1 2 3 4
1 4 5
2 6 7
3 8 9
4 10 11
5 12 13
6 14 15
7 16 17
8 18
9 19 20
10 21 22
11 23 24
//another input (modify goal and initial as well)
A B D
B C
D C
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
    def __init__(self, formatted_input):
        '''
        self.graph = {'A': ['B', 'D'],
                'B': ['C'],
                'D': ['C'],
                }
        '''
        #formatted_input = []
        #for x in user_input:
            #formatted_input.append(list(x.split(' ')))
        self.graph ={}
        for lst in formatted_input:
            self.graph[lst[0]] = lst[1:]
        print("TTTTTTTTT " , self.graph)
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
        '''
        self._Gr = nx.Graph()
        for key_node in self.graph:
            self._Gr.add_node(key_node)
            print(self.graph[key_node])
            for adj in self.graph[key_node]:
                self._Gr.add_node(adj)
                self._Gr.add_edge(key_node, adj)
        self._l = []
        self.shortestPath = []
        self.solution = ""
        self._colors = ['blue'] * self._Gr.number_of_nodes()
        # self._layout = nx.spring_layout(self._Gr,scale=30, k=1/math.sqrt(self._Gr.order()))
        self._layout = nx.spring_layout(self._Gr)

    def trace(self, goal):
        if goal.parent is None:
            print(goal.value, end=" ")
            self.solution = self.solution + str(goal.value)
            self.shortestPath.append(goal.value)
            return
        self.trace(goal.parent)
        self.solution = self.solution + " -> " + str(goal.value)
        self.shortestPath.append(goal.value)
        print(" -> ", goal.value, end=" ")

    def dfs(self, init, goal):
        visited = []
        stack = []
        stack.append(Node(init))
        self._l.append(init)
        if init in goal:
            print("Initial is goal")
            return 1
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
                    print("sama " , adj , goal)
                    for x in goal:
                        if adj == x:
                            self._l.append(x)
                            self.trace(temp)
                            print()
                            return 1
                    stack.append(temp)
            for node in stack:
                print(node.value, end=" ")
            print()
        print("Goal not found")
        return 0
    

    def bfs(self, initial, goal):
        visited = []
        q = Queue()
        q.put(Node(initial))
        self._l.append(initial)
        if initial in goal:
            print("The goal is " + initial)
            return 1
        while not (q.empty()):
            currentNode = q.get()
            visited.append(currentNode.value)
            for adj in self.graph.get(currentNode.value) or []:
                if adj not in visited:
                    temp = Node(adj, currentNode)
                    if adj not in self._l and adj != []:
                        self._l.append(adj)
                    for x in goal:
                        if adj == x:
                            self._l.append(x)
                            self.trace(temp)
                            print()
                            return 1
                        q.put(temp)
        return 0

    def update(self, frames, a):
        a.clear()
        if (frames < len(self._l)):
            #print(self._Gr.node[self._l[frames]])
            i = 0
            for node in self._Gr.nodes:
                print(node, " ", self._l[frames])
                if node == self._l[frames]:
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
                if node == self.shortestPath[frames - len(self._l)]:
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

def onClickRun(user_firstNode,user_goal,user_txtBox, type_var):
  input = user_txtBox.get("1.0", "end-1c").split('\n') #list of list
  #inputFirstNode = user_firstNode.get("1.0", "end-1c").split(' ')
  inputFirstNode = user_firstNode.get("1.0", "end-1c")
  inputGoal= user_goal.get("1.0", "end-1c").split(' ')

  formatted_input = []
  for x in input:
      formatted_input.append((x.split(' ')))

  print("AAA")
  print(formatted_input)
  print(inputFirstNode)
  print(inputGoal)
  first = False

  for item in formatted_input:
      for list in item:
          if list == inputFirstNode:
              first = True



  if first == True:
      if(type_var == 0):
          dfs_inst = DFS(formatted_input)
          if dfs_inst.dfs(inputFirstNode, inputGoal) == 1:
              lbl_bottom['text'] = dfs_inst.solution
          else:
              lbl_bottom['text'] = "Goal does not exist"

          # print(input, 'whatever', '15' is '15')
          # dfs_inst.dfs('A','C')
          dfs_inst.anim()

          print(dfs_inst.solution)
          print(dfs_inst._l)
      if (type_var == 1):
          bfs_inst = DFS(formatted_input)
          # bfs_inst.draw_graph()
          bfs_inst.bfs(inputFirstNode,inputGoal)
          bfs_inst.anim()
          lbl_bottom['text'] = bfs_inst.solution
          print(bfs_inst._l)
      print(input , 'whatever' )

  else:
      tk.messagebox.showinfo("Error", "Check that the initial node is entered in the graph")

#####################################################################################################
#                              END OF OF BUTTON EVENT LISTENER                                     #
####################################################################################################

#####################################################################################################
#                                    START OF GUI                                                   #
####################################################################################################
root = Tk()
root.title("Search Methods Visualizer")

frm_right = tk.Frame()
lbl_nodes = tk.Label(master=frm_right,width=15,height=1, text="Enter the nodes", foreground="#CD5C5C")
# ent = tk.Entry(master=frm_right, fg="#CD5C5C", width=50)
var1 = tk.StringVar()
lbl_firstNode = tk.Label(master=frm_right, text="Enter the initial node", width=15, height=1, fg="#CD5C5C")
txtFirstNode = tk.Text(master=frm_right, height=1, width=3)
lbl_goalNode = tk.Label(master=frm_right, text="Enter the goal node(s)", width=17, height=1, fg="#CD5C5C")
txtgoalNode = tk.Text(master=frm_right, height=1, width=10)
txt = tk.Text(master=frm_right, height=2, width=15)
btn_Run = tk.Button(master=frm_right, text="Run",command=lambda:onClickRun(txtFirstNode,txtgoalNode,txt,algorithmChosen.current()) , width=15, height=1, fg="#CD5C5C")
algorithmChosen = ttk.Combobox(master=frm_right, width = 27, textvariable = var1)
algorithmChosen['values'] = ('dfs',
                          'bfs',
                          'dijkstra',
                          'lim_dfs',
                          'itr_dfs')

lbl_nodes.grid(row=0, column=0, padx=5, pady=5)
txt.grid(row=1, column=0, padx=5, pady=1)
lbl_firstNode.grid(row=0, column=1, padx=5, pady=5)
txtFirstNode.grid(row=1, column=1, padx=5, pady=1)
lbl_goalNode.grid(row=2, column=1, padx=5, pady=5)
txtgoalNode.grid(row=3, column=1, padx=5, pady=1)
# ent.grid(row=1, column=0, padx=5, pady=5)
btn_Run.grid(row=4, column=0, padx=5, pady=5)
algorithmChosen.grid(row=4, column=1)
algorithmChosen.current(1)



frm_left = tk.Frame()
lbl_top = tk.Label(master=frm_left, text="Title", foreground="#CD5C5C")
fig = plt.Figure(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, frm_left)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0)
lbl_bottom = tk.Label(master=frm_left, text="Written Results", foreground="#CD5C5C")
lbl_top.grid(row=0, column=0, padx=5, pady=5)
lbl_bottom.grid(row=2, column=0, padx=5, pady=5)



frm_right.grid(row=0, column=1, padx=5, pady=5)
frm_left.grid(row=0, column=0, padx=5, pady=5)

root.mainloop()
#####################################################################################################
#                                    END OF GUI                                                     #
####################################################################################################







