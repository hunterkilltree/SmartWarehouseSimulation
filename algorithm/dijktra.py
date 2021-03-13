
class Dijkstra:
    def __init__(self, input, occupy_node):
        self.occupy_node = occupy_node
        self.input = input
        self.path = []

    def calculate(self):
        return [self.calculateFromOrigin(i) for i, v in enumerate(self.input)]

    def calculateFromOrigin(self, origin):
        distance = [-1 for i in range(len(self.input))]
        path = [-1 for i in range(len(self.input))]  # vector to get the best path

        # Distance from origin to itself is always 0
        distance.pop(origin)
        distance.insert(origin, 0)
        # priority = list(range(len(self.input)))

        priority = []
        for i in range(0, len(self.input)):
            if self.occupy_node[i] == False:
                priority.append(i)
        print("This is priority  {}".format(priority))


        while True:
            if len(priority) == 0: break
            frm = self.getSmallestPossibleVertex(distance, priority)
            priority.remove(frm)
            options = self.getOptionList(self.input[frm])
            for [position, weight] in options:
                dist = distance[frm] + weight
                if distance[position] == -1 or dist < distance[position]:
                    distance.pop(position)
                    distance.insert(position, dist)
                    path.pop(position)
                    path.insert(position, frm)
        print("This is path in calculateFromOrigin {}".format(path))
        self.path.insert(origin, path)

        return distance

    def getSmallestPossibleVertex(self, distances, priority):
        smallestKey = -1
        smallestValue = -1
        for i, item in enumerate(distances):
            if (smallestValue == -1 or (item >= 0 and item < smallestValue)) and i in priority:
                smallestValue = item
                smallestKey = i
        return smallestKey

    def getOptionList(self, vector):
        return [[i, weight] for i, weight in enumerate(vector) if weight > 0]

    def getPath(self):
        return self.path

    def getBestPath(self, frm, to):
        print("What is this {}".format([to]))
        return [i for i in reversed(self._getBestPath(frm, to, [to]))]

    def _getBestPath(self, frm, to, path):
        print()
        print("This is the from {} to {} path {}".format(frm, to, path))
        path_ = self.path[frm]
        lastNode = path_[to]
        path.append(lastNode)
        if (lastNode == frm):
            return path
        elif lastNode in path: # fix bug 13/03/2021
            return path
        else:
            return self._getBestPath(frm, lastNode, path)


class DijkstraModify:

    def __init__(self):
        self.path = []

    def minDistance(self, dist, queue):
        # Initialize min value and min_index as -1
        minimum = float("Inf")
        min_index = -1

        # from the dist array,pick one which
        # has min value and is till in queue
        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index

    def printPath(self, parent, j):
        self.path.append(parent)

    def printSolution(self, dist, parent):
        src = 0
        for i in range(1, len(dist)):
            self.printPath(parent, i)

    def dijkstra(self, graph, src):
        row = len(graph)
        col = len(graph[0])
        # The output array. dist[i] will hold
        # the shortest distance from src to i
        # Initialize all distances as INFINITE
        dist = [float("Inf")] * row

        # Parent array to store
        # shortest path tree
        parent = [-1] * row

        # Distance of source vertex
        # from itself is always 0
        dist[src] = 0

        # Add all vertices in queue
        queue = []
        for i in range(row):
            queue.append(i)

            # Find shortest path for all vertices
        while queue:

            # Pick the minimum dist vertex
            # from the set of vertices
            # still in queue
            print("this is queue {}".format(dict))
            u = self.minDistance(dist, queue)

            # remove min element
            print("This is u {}".format(u))
            if u != -1:
                break
            queue.remove(u)

            # Update dist value and parent
            # index of the adjacent vertices of
            # the picked vertex. Consider only
            # those vertices which are still in
            # queue
            for i in range(col):
                '''Update dist[i] only if it is in queue, there is 
                an edge from u to i, and total weight of path from 
                src to i through u is smaller than current value of 
                dist[i]'''
                if graph[u][i] and i in queue:
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u

                        # print the constructed distance array
        self.printSolution(dist, parent)

    def getBestPath(self, frm, to):
        return [i for i in reversed(self._getBestPath(frm, to, [to]))]

    def _getBestPath(self, frm, to, path):
        print("This is the path {}".format(path))
        path_ = self.path[frm]
        lastNode = path_[to]
        path.append(lastNode)
        if (lastNode == frm):
            return path
        else:
            return self._getBestPath(frm, lastNode, path)