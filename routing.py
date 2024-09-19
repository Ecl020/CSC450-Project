import sys 
import csv
import heapq

def dijkstra(graph, start):
    # Initialize distances with infinity and set the distance for the start node to 0
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    # Priority queue is used to manage how nodes are being explored. First node to be explored is starting node since it weight is 0
    priorityQueue = [(0, start)]
    # Dictionary to keep track of predecessors for path reconstruction
    predecessors = {node: None for node in graph}
    
    while priorityQueue:
        current_distance, current_node = heapq.heappop(priorityQueue)
        # If the current distance is greater than the known distance, skip processing
        if current_distance > distances[current_node]:
            continue
        # Process each neighbor of the current node
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight    
            # Update distance and predecessor if a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                # Here we are pushing the neighbor onto the priority queue with the most updated distances
                heapq.heappush(priorityQueue, (distance, neighbor))
    
    # Reconstruct the shortest paths from the start node
    shortestPath = {}
    for node in graph:
        path = []
        current = node
        while current is not None:
            path.append(current)
            current = predecessors[current]
        # Reverses the path to obtain the correct order
        path.reverse()
        # Stores the shortest path in the shortestPath directory
        shortestPath[node] = path
    
    return shortestPath, distances

def convert_matrix(matrix):
    # So here im converting the remaining elements in the file to either a integer or an        
    # if an item of the file is 9999 then its converted to an if. Otherwise an int
    return [
        [float('inf') if x == '9999' else int(x) for x in row]
        for row in matrix]

def fileHandler(fileName): 
    try:    
        with open(fileName, 'r') as file:
            # This reads the content from the CSV file
            reader = csv.reader(file)
            # Here we are extracting the items from te first row
            nodes = next(reader)[1:]
            # Extract the content after the first row
            matrix = [row[1:] for row in reader] 
            # Here we are converting the remaning file elements
            matrix = convert_matrix(matrix)
            return nodes, matrix
    except FileNotFoundError:
        print("Error, the file {} not found".format(fileName))

def matrixBuilder(matrix, nodes):
    adj_list = {node: {} for node in nodes}
    # Here were itterating through the nodes and their indincies 
    for i, node in enumerate(nodes):
        # For each node, iterate over its corresponding row in the matrix
        for j, weight in enumerate(matrix[i]):
             # Ignores self-loops and infinities
            if weight != float('inf') and weight != 0: 
                adj_list[node][nodes[j]] = weight
    return adj_list

def dijstraHandler(nodes, matrix, startingPoint):
    # constructs the graph in a matrix
    graph = matrixBuilder(matrix, nodes)
    # Here is where we call the algorithm to get a return on both shortests paths and distances
    shortestPath, distances = dijkstra(graph,startingPoint)
    # Sort the nodes by distance to the starting node
    sortedNodes = sorted(distances.keys(), key=lambda node: distances[node])
    # A list to hold the shortests paths for visual 
    shortestPathTree = []
    # A list to hold the costs for the least-cost paths
    costStrings = []

    # If the source node doesn't exist. This will return a message saying that it doesn't exist in the graph
    if starting_Point not in graph:
        print("The source node you have given is not found in the graph")
        return

    # Printing out the shortest path tree sequence 
    print("Shortest path tree for node {}:".format(startingPoint))
    for node in sortedNodes:
        if node != startingPoint:
            path_str = ''.join(shortestPath[node])
            shortestPathTree.append(path_str)
    print(', '.join(shortestPathTree))      

    # Print the Costs of the least-cost paths
    print(f"Costs of the least-cost paths for node {startingPoint}:")
    for node, distance in distances.items():
        costStrings.append("{}:{}".format(node,distance))
    print(', '.join(costStrings))

############################################### 
### Main Function #############################
###############################################

if __name__ == "__main__":
    # Checking to see if there are two arguments provided
    if(len(sys.argv) == 2):
        fileName = sys.argv[1]
        # function call to parse the file into the required components
        nodes, matrix = fileHandler(fileName)    
        starting_Point = input("Please, provide the source node:").strip()
        # this helper function helps proccessing the dijstra algorithm
        dijstraHandler(nodes, matrix,starting_Point)        
    else:
        # Error handeling for a case where there isn't two arguments
        print("Invalid Command")
        
        
