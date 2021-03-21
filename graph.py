from queue import Queue
import heapq
import sys
from haversine import haversine

class AdjNode:
    def __init__(self,data):
        self.vertex = data
        self.adjacent = None
        self.weight = 0

class Graph:

    def __init__(self,vertices,keys):
        self.vertices = len(keys)
        self.vertexNames = keys
        self.adjList = {}
        for key in keys:
            self.adjList[key] = None
        self.visited = [0]*vertices
        self.path = []
        self.distance = 0

    def addEdge(self,src,dest,weight=0,directed=False):
        if directed:
            vertex = AdjNode(dest)
            vertex.adjacent = self.adjList[src]
            vertex.weight = weight
            self.adjList[src] = vertex
        else:
            vertex = AdjNode(dest)
            vertex.adjacent = self.adjList[src]
            vertex.weight = weight
            self.adjList[src] = vertex
            vertex = AdjNode(src)
            vertex.adjacent = self.adjList[dest]
            vertex.weight = weight
            self.adjList[dest] = vertex

    def printGraph(self):

        for i in self.vertexNames:
            print(f"Edges of vertex {i} are: \n")
            temp = self.adjList[i]
            while temp:
                print(f"{i} -> {temp.vertex} with weight: {temp.weight}\n")
                temp = temp.adjacent
            print("\n")

    def adjacentNodes(self,i):
        node = self.adjList[i]
        while node:
            print(node.vertex)
            node = node.adjacent

    # Time Complexity: O(V)
    def dfs(self,src):
        self.visited[src] = 1
        print(self.visited)
        print("Source element: ",src)
        temp = self.adjList[src]
        while temp:
            connectedVertex = temp.vertex
            if not self.visited[connectedVertex]:
                self.dfs(connectedVertex)
            temp = temp.adjacent

    def bfs(self,src):

        queue = Queue()
        u = src
        self.visited[u] = 1
        temp = self.adjList[src]
        while True:
            while temp:
                connectedVertex = temp.vertex
                if not self.visited[connectedVertex]:
                    queue.enqueue(connectedVertex)
                    self.visited[connectedVertex] = 1
                    print(self.visited)
                    # print("Source element: ",connectedVertex)
                if queue.isEmpty():
                    return
                temp = temp.adjacent
            element = queue.dequeue()
            print("Element to be traversed: ",element)
            temp = self.adjList[element]

    def printPath(self, parent, j):
        if parent[j] == -1 : 
            print(j,end=" ")
            self.path.append(j) 
            return
        self.printPath(parent , parent[j]) 
        print(j,end=" ")
        self.path.append(j)

    def initializeVertexVal(self,value):
        data = {}
        for vertex in self.vertexNames:
            data[vertex] = value
        return data

    def shortestPath(self,src,dest):
        h = []
        dist = self.initializeVertexVal(1000)
        sptList = self.initializeVertexVal(False)
        heapq.heappush(h,(0,src))
        dist[src] = 0
        parent = self.initializeVertexVal(-1)
        while len(h)!=0:
            cost,vertex = heapq.heappop(h)
            sptList[vertex] = True
            temp = self.adjList[vertex]
            print(f"---------The cost from {src} to vertex {vertex} is {cost}---------")
            if vertex == dest:
                print(f"Path exists {src} to {dest} with cost: {cost}")
                break
            
            while temp:
                connectedVertex = temp.vertex
                vertexWeight = temp.weight

                if sptList[connectedVertex] is False and dist[connectedVertex] > cost + vertexWeight:
                    dist[connectedVertex] = cost + vertexWeight
                    parent[connectedVertex] = vertex
                    heapq.heappush(h,(dist[connectedVertex],connectedVertex))
                temp = temp.adjacent
        print(f"The path is with distance: {cost}")
        self.distance = cost
        self.printPath(parent,dest)

# vertices = 6
# keys = [0,1,2,3,4,5]
# graph = Graph(vertices,keys)

# graph.addEdge(0,1,4,False)
# graph.addEdge(0,2,2,False)
# graph.addEdge(1,2,5,False)
# graph.addEdge(1,3,10,False)
# graph.addEdge(2,4,3,False)
# graph.addEdge(4,3,4,False)
# graph.addEdge(3,5,11,False)

# graph.printGraph()
# graph.shortestPath(0,5)
# print(graph.path)

