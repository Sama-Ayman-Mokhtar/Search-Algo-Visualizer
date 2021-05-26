import networkx as nx
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib import animation
from queue import Queue
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from queue import PriorityQueue
from networkx.drawing.nx_pydot import pydot_layout, graphviz_layout
from collections import defaultdict
#####################################################################################################
#                                         N O T E S                                                #
####################################################################################################
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

0 1 4
0 7 8
1 7 11
1 2 8
7 8 7
7 6 1
2 8 2
8 6 6
2 5 4
6 5 2
2 3 7
3 5 14
3 4 9
5 4 10

1 2 1
1 3 1
2 3 3
3 4 4
4 1 5
//another input (modify goal and initial as well)
A B D
B C
D C
'''

class Node:
    def __init__(self, value, parent=None, depth = 0, cost = -100):
        self.value = value
        self.parent = parent
        self.depth = depth
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

#####################################################################################################
#                                        START OF GRAPH                                             #
####################################################################################################
class Graph:
    def __init__(self, formatted_input, weighted=False, isGreedy=False, isIter=False):
        '''
        self.graph = {'A': ['B', 'D'],
                'B': ['C'],
                'D': ['C'],
                }
        '''
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
        self.graph = defaultdict(list)
        self.dictDistance = {}
        self.weight = weighted
        self.isGreedy = isGreedy
        self.isIter = isIter
        self.index= 0
        self.varStart = 0

        if not weighted:
            for lst in formatted_input:
                self.graph[lst[0]] = lst[1:]
        else:
            for lst in formatted_input:
                self.dictDistance[lst[0]] = 10e9
                self.dictDistance[lst[1]] = 10e9
                self.graph[lst[0]].append(Node(value=lst[1], cost=lst[2]))
                self.graph[lst[1]]

        self._Gr = nx.DiGraph()

        if not weighted:
            for key_node in self.graph:
                self._Gr.add_node(key_node)
                for adj in self.graph[key_node]:
                    self._Gr.add_node(adj)
                    self._Gr.add_edge(key_node, adj)
        else:
            for line in formatted_input:
                self._Gr.add_node(line[0], distance=self.dictDistance[line[0]])
                self._Gr.add_node(line[1], distace=self.dictDistance[line[1]])
                self._Gr.add_edge(line[0], line[1], weight=line[2])
            self.labels = nx.get_edge_attributes(self._Gr, 'weight')
            self.nodeLabels = nx.get_node_attributes(self._Gr, 'distance')

        self._l = []
        self._itrL = []
        self.shortestPath = []
        self.solution = ""
        self.solItr = []
        self.heuristic = {}
        self._colors = ['blue'] * self._Gr.number_of_nodes()
        self._layout = graphviz_layout(self._Gr)
        #self._layout = nx.spring_layout(self._Gr)

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
        stack.append(Node(value=init))
        self._l.append(init)

        if init in goal:
            self.trace(Node(value=init))
            print("Initial is goal")
            return 1

        while stack:
            curr_node = stack.pop()
            visited.append(curr_node.value)

            if curr_node.value not in self._l:
                self._l.append(curr_node.value)
                print("visitied ", visited)

            for adj in self.graph.get(curr_node.value) or []:
                if adj not in visited:
                    temp = Node(value=adj, parent = curr_node)

                    for x in goal:
                        if adj == x:
                            self._l.append(x)
                            self.trace(temp)
                            print()
                            return 1
                    stack.append(temp)

        self.solution = "GOAL NOT FOUND"
        print("Goal not found")
        return 0

    def limited_dfs(self, init, goal, depth_limit):
        visited = []
        stack = []
        self.solution = ""
        self._l.clear()
        stack.append(Node(value=init))
        self._l.append(init)
        self._itrL.append(init)

        if init in goal:
            self.trace(Node(value=init))
            print("Initial is goal")
            return 1
        isCutOff = False

        while stack:
            curr_node = stack.pop()
            visited.append(curr_node.value)

            if curr_node.value not in self._l:
                self._l.append(curr_node.value)
                self._itrL.append(curr_node.value)
                print("visitied ", visited)

            for adj in self.graph.get(curr_node.value) or []:
                if curr_node.depth + 1 > depth_limit:
                    isCutOff = True

                if adj not in visited and curr_node.depth + 1 <= depth_limit:
                    temp = Node(value=adj, parent=curr_node, depth=curr_node.depth + 1)

                    for x in goal:
                        if adj == x:
                            self._l.append(x)
                            self._itrL.append(x)
                            self.trace(temp)
                            self.solItr.append(self.solution)
                            print()
                            return 1
                    stack.append(temp)

        if isCutOff:
            self.solution = "GOAL NODE NOT FOUND WITHIN DEPTH OF    " + str(depth_limit)
            self.solItr.append("GOAL NODE NOT FOUND WITHIN DEPTH OF    " + str(depth_limit))
            print("GOAL NODE NOT FOUND WITHIN DEPTH OF    " + str(depth_limit))
            return 2  # cutOff
        else:
            self.solution = "GOAL NOT FOUND"
            self.solItr.append( "GOAL NOT FOUND")
        return 0

    def iterDeeping(self, intial, goal):
        res = 2 #cutOff
        depth_limit = 0
        while res != 0:
            res = self.limited_dfs(intial, goal,depth_limit)
            if res == 1:
                return 1
            self._itrL.append("break")
            depth_limit += 1
        return 0

    def bfs(self, initial, goal):
        visited = []
        q = Queue()
        q.put(Node(value=initial))
        self._l.append(initial)

        if initial in goal:
            self.trace(Node(value=initial))
            print("The goal is " + initial)
            return 1

        while not (q.empty()):
            currentNode = q.get()
            visited.append(currentNode.value)

            for adj in self.graph.get(currentNode.value) or []:
                if adj not in visited:
                    temp = Node(value=adj, parent=currentNode)
                    if adj not in self._l and adj != []:
                        self._l.append(adj)

                    for x in goal:
                        if adj == x:
                            self._l.append(x)
                            self.trace(temp)
                            print()
                            return 1
                        q.put(temp)
        self.solution = "GOAL NOT FOUND"
        return 0

    def uniformCost(self, initial, goal):
        pq = PriorityQueue()
        self.dictDistance[initial] = 0
        pq.put(Node(value=initial, cost=0))
        self._l.append(Node(value=initial, cost=self.dictDistance.get(initial)))

        if initial in goal:
            self.trace(Node(value=initial))
            print("The goal is " + initial)
            return 1

        while not (pq.empty()):
            currentN = pq.get()
            for cn in goal:
                if cn == currentN.value:
                    self.trace(currentN)
                    print("The goal is " + currentN.value)
                    return 1

            for adjNode in self.graph.get(currentN.value) or []:
                if ((self.dictDistance.get(currentN.value) + int(adjNode.cost)) < (
                        self.dictDistance.get(adjNode.value))):
                    self.dictDistance[adjNode.value] = self.dictDistance.get(currentN.value) + int(adjNode.cost)
                    self._l.append(Node(value=adjNode.value, cost=self.dictDistance.get(adjNode.value)))
                    temp = Node(value=adjNode.value, parent=currentN, cost=self.dictDistance.get(adjNode.value))
                    pq.put(temp)
                    print("pq", pq)

        self.solution = "GOAL NOT FOUND"
        return 0

    def helper(self, initial, goal):
        pq = PriorityQueue()
        dis={}
        for nodes in self._Gr.nodes:
            dis[nodes]=10E9
        dis[initial]=0
        pq.put(Node(value=initial, cost=0))

        if initial == goal:
            return dis[initial]

        while not (pq.empty()):
            currentN = pq.get()
            if currentN.value == goal:
                return dis[goal]

            for adjNode in self.graph.get(currentN.value) or []:
                if ((dis.get(currentN.value) + int(adjNode.cost)) < (
                       dis.get(adjNode.value))):
                    dis[adjNode.value] = dis.get(currentN.value) + int(adjNode.cost)
                    temp = Node(value=adjNode.value, parent=currentN, cost=self.dictDistance.get(adjNode.value))
                    pq.put(temp)
                    print("pq", pq)

        return 10E9

    def greedy(self, initial, goal):
        for node in self._Gr.nodes:
            for x in goal:
                if node == x:
                    goal[0] = x
                    break
        print("goal[0] is ", goal[0])

        for nodeVal in self._Gr.nodes:
            self.heuristic[nodeVal] = self.helper(nodeVal,goal[0])
            print(self.heuristic)

        pq = PriorityQueue()
        visited = []
        pq.put(Node(value=initial, cost = self.heuristic[initial]))
        self._l.append(initial)

        if initial == goal[0]:
            self.trace(Node(value=initial))
            print("The goal is " + initial)
            return 1

        while not (pq.empty()):
            currentN = pq.get()
            visited.append(currentN.value)
            if currentN.value == goal[0]:
                self.trace(currentN)
                print("The goal is " + currentN.value)
                return 1

            for adjNode in self.graph.get(currentN.value) or []:
                if adjNode.value not in visited:
                    self._l.append(adjNode.value)
                    visited.append(adjNode.value)
                    pq.put(Node(value=adjNode.value,parent=currentN,cost = self.heuristic[adjNode.value]))
                    print("pq", pq)
        self.solution = "GOAL NOT FOUND"
        return 0

    def aStar(self, initial, goal):
        for node in self._Gr.nodes:
            for x in goal:
                if node == x:
                    goal[0] = x
                    break
        print("goal[0] is ", goal[0])

        for nodeVal in self._Gr.nodes:
            self.heuristic[nodeVal] = self.helper(nodeVal, goal[0])
            print(self.heuristic)

        pq = PriorityQueue()
        visited = []
        self.dictDistance[initial] = 0
        pq.put(Node(value=initial, cost=0 + self.heuristic[initial]))
        self._l.append(Node(value=initial, cost=self.dictDistance.get(initial) + self.heuristic[initial]))

        if initial == goal[0]:
            self.trace(Node(value=initial))
            print("The goal is " + initial)
            return 1

        while not (pq.empty()):
            currentN = pq.get()
            visited.append(currentN.value)
            if currentN.value == goal[0]:
                self.trace(currentN)
                print("The goal is " + currentN.value)
                return 1

            for adjNode in self.graph.get(currentN.value) or []:
                if adjNode.value not in visited:
                    if ((self.dictDistance.get(currentN.value) + int(adjNode.cost) + int(
                            self.heuristic[adjNode.value]))) < (
                            self.dictDistance.get(adjNode.value) + int(self.heuristic[adjNode.value])):
                        self.dictDistance[adjNode.value] = self.dictDistance.get(currentN.value) + int(adjNode.cost)
                        self._l.append(Node(value=adjNode.value,
                                            cost=self.dictDistance.get(adjNode.value) + self.heuristic[adjNode.value]))
                        temp = Node(value=adjNode.value, parent=currentN,
                                    cost=self.dictDistance.get(adjNode.value) + self.heuristic[adjNode.value])
                        pq.put(temp)
                        print("The cost of the node ", temp.value, " is ", temp.cost)
                        print("pq", pq)

        self.solution = "GOAL NOT FOUND"
        return 0

    def update(self, frames, a):
        a.clear()

        if self.isGreedy:
            if frames < len(self._l):
                i = 0
                for node in self._Gr.nodes:
                    if node == self._l[frames]:
                        break
                    i += 1

                self._colors[i] = 'orange'
                pos_attrs = {}
                for node, coords in self._layout.items():
                    pos_attrs[node] = (coords[0], coords[1] + 4)

                custom_node_attrs = {}
                for node in self.heuristic.keys():
                    custom_node_attrs[node] = "{'h': '" + str(self.heuristic[node]) + "'}"
                nx.draw_networkx(self._Gr, pos=self._layout, node_color=self._colors, ax=a)
                nx.draw_networkx_edge_labels(self._Gr, pos=self._layout, edge_labels=self.labels, ax=a)
                nx.draw_networkx_labels(self._Gr, pos=pos_attrs, labels=custom_node_attrs, ax=a)
                a.set_title("Frame {}".format(frames))
            else:
                a.clear()

                i = 0
                for node in self._Gr.nodes:
                    if node == self.shortestPath[frames - len(self._l)]:
                        break
                    i += 1

                self._colors[i] = 'red'
                pos_attrs = {}
                for node, coords in self._layout.items():
                    pos_attrs[node] = (coords[0], coords[1] + 4)

                custom_node_attrs = {}
                for node in self.heuristic.keys():
                    custom_node_attrs[node] = "{'h': '" + str(self.heuristic[node]) + "'}"
                nx.draw_networkx(self._Gr, pos=self._layout, node_color=self._colors, ax=a)
                nx.draw_networkx_edge_labels(self._Gr, pos=self._layout, edge_labels=self.labels, ax=a)
                nx.draw_networkx_labels(self._Gr, pos=pos_attrs, labels=custom_node_attrs, ax=a)
                a.set_title("Frame {}".format(frames))

            if frames == len(self._l + self.shortestPath) - 1:
                self._colors = ['blue'] * self._Gr.number_of_nodes()

        elif self.isIter:

            if frames < len(self._itrL):
                if self._itrL[frames] == "break":
                    self.varStart = frames + 1
                    self._colors = ['blue'] * self._Gr.number_of_nodes()
                    lbl_bottom['text'] = self.solItr[self.index]
                    self.index += 1

                else:
                    i = 0
                    for node in self._Gr.nodes:
                        if node == self._itrL[frames]:
                            break
                        i += 1
                    self._colors[i] = 'orange'

                nx.draw_networkx(self._Gr, pos=self._layout, node_color=self._colors, ax=a)
                a.set_title("Frame {}".format(frames))

            else:
                a.clear()

                i = 0
                for node in self._Gr.nodes:
                    if node == self.shortestPath[frames - len(self._itrL)]:
                        break
                    i += 1

                self._colors[i] = 'red'
                lbl_bottom['text'] = self.solItr[len(self.solItr)-1]
                nx.draw_networkx(self._Gr, pos=self._layout, node_color=self._colors, ax=a)
                a.set_title("Frame {}".format(frames))

            if frames == len(self._itrL + self.shortestPath) - 1:
                self._colors = ['blue'] * self._Gr.number_of_nodes()

        elif self.weight:

            if frames < len(self._l):
                i = 0
                for node in self._Gr.nodes:
                    if node == self._l[frames].value:
                        break
                    i += 1

                self._colors[i] = 'orange'
                self.nodeLabels[self._l[frames].value] = self._l[frames].cost
                pos_attrs = {}
                for node, coords in self._layout.items():
                    pos_attrs[node] = (coords[0], coords[1] + 4)

                custom_node_attrs = {}
                for node, attr in self.nodeLabels.items():
                    custom_node_attrs[node] = "{'d': '" + str(attr) + "'}"
                nx.draw_networkx(self._Gr,pos=self._layout, with_labels=True, node_color=self._colors,
                                 ax=a)
                nx.draw_networkx_edge_labels(self._Gr, pos = self._layout, edge_labels=self.labels, ax=a)
                nx.draw_networkx_labels(self._Gr, pos=pos_attrs, labels=custom_node_attrs, ax=a)
                a.set_title("Frame {}".format(frames))

            else:
                a.clear()

                i = 0
                for node in self._Gr.nodes:
                    if node == self.shortestPath[frames - len(self._l)]:
                        break
                    i += 1

                self._colors[i] = 'red'
                pos_attrs = {}
                for node, coords in self._layout.items():
                    pos_attrs[node] = (coords[0], coords[1] + 4)

                custom_node_attrs = {}
                for node, attr in self.nodeLabels.items():
                    custom_node_attrs[node] = "{'d': '" + str(attr) + "'}"
                nx.draw_networkx(self._Gr,  pos=self._layout, with_labels=True, node_color=self._colors,
                                 ax=a)
                nx.draw_networkx_edge_labels(self._Gr, pos=self._layout, edge_labels=self.labels, ax=a)
                nx.draw_networkx_labels(self._Gr, pos=pos_attrs, labels=custom_node_attrs, ax=a)
                a.set_title("Frame {}".format(frames))

            if frames == len(self._l + self.shortestPath) - 1:
                self._colors = ['blue'] * self._Gr.number_of_nodes()
                for key in self.nodeLabels.keys():
                    self.nodeLabels[key] = 10e9
        else:

            if frames < len(self._l):
                i = 0
                for node in self._Gr.nodes:
                    if node == self._l[frames]:
                        break
                    i += 1

                self._colors[i] = 'orange'
                nx.draw_networkx(self._Gr,  pos=self._layout, node_color=self._colors, ax=a)
                a.set_title("Frame {}".format(frames))

            else:
                a.clear()

                i = 0
                for node in self._Gr.nodes:
                    if node == self.shortestPath[frames - len(self._l)]:
                        break
                    i += 1

                self._colors[i] = 'red'
                nx.draw_networkx(self._Gr,  pos=self._layout, node_color=self._colors, ax=a)
                a.set_title("Frame {}".format(frames))

            if frames == len(self._l + self.shortestPath) - 1:
                self._colors = ['blue'] * self._Gr.number_of_nodes()

    def anim(self):
        fig = plt.Figure(figsize=(7, 5))
        ax = fig.add_subplot(111)
        plt.axis('off')
        canvas = FigureCanvasTkAgg(fig, frm_left)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
        print(len(self._l))

        if self.isIter:
            ani = animation.FuncAnimation(fig, self.update, frames=len(self._itrL + self.shortestPath), interval=400,
                                          fargs={ax})
        else:
            ani = animation.FuncAnimation(fig, self.update, frames=len(self._l + self.shortestPath), interval=1000,fargs={ax})
        canvas = FigureCanvasTkAgg(fig, frm_left)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
#####################################################################################################
#                                         END OF GRAPH                                              #
####################################################################################################

#####################################################################################################
#                               START OF BUTTON EVENT LISTENER                                      #
####################################################################################################

def onClickRun(user_firstNode,user_goal, user_txtBox, type_var,user_depthlmt=0):
  input = user_txtBox.get("1.0", "end-1c").split('\n')
  inputFirstNode = user_firstNode.get("1.0", "end-1c")
  inputGoal= user_goal.get("1.0", "end-1c").split(' ')
  inputDepthLmt = user_depthlmt.get("1.0", "end-1c")

  formatted_input = []
  for x in input:
      formatted_input.append((x.split(' ')))

  first = False
  goal = False

  if type_var == 5 or type_var == 6:
      for item in formatted_input:
              if item[0]==inputFirstNode or item[1]==inputFirstNode:
                  first=True
              for x in inputGoal:
                  if item[0] == x or item[1] == x:
                      goal = True

  else:
      for item in formatted_input:
          for list in item:
              if list == inputFirstNode:
                  first = True

  if first == True:
      if(type_var == 0):
          print("DFS starting")
          dfs_inst = Graph(formatted_input)
          dfs_inst.dfs(inputFirstNode, inputGoal)
          dfs_inst.anim()
          lbl_bottom['text'] = dfs_inst.solution

      if (type_var == 1):
          print("BFS starting")
          bfs_inst = Graph(formatted_input)
          bfs_inst.bfs(inputFirstNode,inputGoal)
          bfs_inst.anim()
          lbl_bottom['text'] = bfs_inst.solution

      if (type_var == 2):
          print("UCS starting")
          ucs_inst = Graph(formatted_input,weighted=True)
          ucs_inst.uniformCost(inputFirstNode, inputGoal)
          ucs_inst.anim()
          lbl_bottom['text'] = ucs_inst.solution

      if (type_var == 3):
          print("Depth limit starting")
          if inputDepthLmt == '':
              tk.messagebox.showinfo("Error", "Enter the depth limit")

          else:
              lmtDfs_inst = Graph(formatted_input)
              lmtDfs_inst.limited_dfs(inputFirstNode, inputGoal, int(inputDepthLmt))
              lmtDfs_inst.anim()
              lbl_bottom['text'] = lmtDfs_inst.solution

      if (type_var == 4):
          print("iterative starting")
          iterDeepening_inst = Graph(formatted_input,isIter=True)
          iterDeepening_inst.iterDeeping(inputFirstNode, inputGoal)
          iterDeepening_inst.anim()

      if (type_var == 5):
          if goal == False:
              tk.messagebox.showinfo("Error", "Check that the goal exists in the graph")
          else:
              print("Greedy starting")
              greedy_inst = Graph(formatted_input, weighted=True, isGreedy=True)
              greedy_inst.greedy(inputFirstNode, inputGoal)
              greedy_inst.anim()
              lbl_bottom['text'] = greedy_inst.solution

      if (type_var == 6):
          if goal == False:
              tk.messagebox.showinfo("Error", "Check that the goal exists in the graph")
          else:
              print("Astar starting")
              aStar_inst = Graph(formatted_input, weighted=True)
              aStar_inst.aStar(inputFirstNode, inputGoal)
              aStar_inst.anim()
              lbl_bottom['text'] = aStar_inst.solution

  else:
      tk.messagebox.showinfo("Error", "Check that the initial node is entered in the graph")

#####################################################################################################
#                              END OF OF BUTTON EVENT LISTENER                                     #
####################################################################################################

#####################################################################################################
#                                    START OF GUI                                                   #
####################################################################################################
root = Tk()
root.resizable(FALSE,FALSE)
root.title("Search Methods Visualizer")
root.config(background="dark cyan")

frm_right = tk.Frame()
frm_right.config(background="dark cyan")
var1 = tk.StringVar()
lbl_goalNode = tk.Label(master=frm_right, text="Enter the goal node(s)", height=1, background="dark cyan", font=("Verdana",12,'bold'),fg="white")
txtgoalNode = tk.Text(master=frm_right, height=2, width=12,font=("Verdana",12),fg="black")
lbl_depthLmt = tk.Label(master=frm_right, text="Enter the depth limit", height=1, background="dark cyan",font=("Verdana",12,'bold'),fg="white")
txtDepthLmt = tk.Text(master=frm_right, height=2, width=5,font=("Verdana",12),fg="black")

btn_Run = tk.Button(master=frm_right, text="   Run   ",command=lambda:onClickRun(txtFirstNode,txtgoalNode,txt,algorithmChosen.current(),txtDepthLmt) ,height=1,background="dark cyan",font=("Verdana",12,'bold'),fg="white")
algorithmChosen = ttk.Combobox(master=frm_right,textvariable = var1,font=("Verdana",12))
algorithmChosen['values'] = ('Depth first',
                          'Breadth first',
                          'Uniform cost',
                          'Depth limited',
                          'Iterative deepening',
                             'Greedy',
                             'A*')

lbl_goalNode.grid(row=0, column=0,pady=0)
txtgoalNode.grid(row=1, column=0,pady=(5,24))
lbl_depthLmt.grid(row=2, column=0, padx=5, pady=5)
txtDepthLmt.grid(row=3, column=0, padx=5, pady=(5,24))
algorithmChosen.grid(row=4, column=0,pady=(5,130))
btn_Run.grid(row=5, column=0, padx=5, pady=(5,100))
algorithmChosen.current(1)

frm_middle=tk.Frame()
frm_middle.config(background="dark cyan")
lbl_firstNode = tk.Label(master=frm_middle, text="Enter the initial node", height=1, background="dark cyan", font=("Verdana",12,'bold'),fg="white")
txtFirstNode = tk.Text(master=frm_middle, height=2, width=5,font=("Verdana",12),fg="black")
lbl_nodes = tk.Label(master=frm_middle,width=15,height=1, text="Enter the nodes", background="dark cyan",font=("Verdana",12,'bold'),fg="white")
txt = tk.Text(master=frm_middle, height=20, width=18,font=("Verdana",12),fg="black")

lbl_firstNode.grid(row=0, column=0,pady=0)
txtFirstNode.grid(row=1, column=0, pady=(5,20))
lbl_nodes.grid(row=2, column=0, padx=8, pady=8)
txt.grid(row=3, column=0, pady=1)

scroll = ttk.Scrollbar(frm_middle)
scroll.config(command=txt.yview)
txt.config(yscrollcommand=scroll.set)
scroll.grid(row=3, column=3,sticky='NS',padx=0)

frm_left = tk.Frame()
frm_left.config(background="dark cyan")
lbl_top = tk.Label(master=frm_left, text="Graph Visualizer",  background="dark cyan", font=("Verdana",12,'bold'),fg="white")
lbl_bottom = tk.Label(master=frm_left, text="Written Results", background="dark cyan", font=("Verdana",12,'bold'),fg="white")

lbl_top.grid(row=0, column=0, padx=5, pady=5)
lbl_bottom.grid(row=2, column=0, padx=5, pady=(30,30))

fig = plt.Figure(figsize=(8, 5))
canvas = FigureCanvasTkAgg(fig, frm_left)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0,padx=30)

frm_right.grid(row=0, column=2, padx=5, pady=5)
frm_middle.grid(row=0, column=1, padx=5, pady=5)
frm_left.grid(row=0, column=0, padx=5, pady=5)

root.mainloop()
#####################################################################################################
#                                    END OF GUI                                                     #
####################################################################################################

