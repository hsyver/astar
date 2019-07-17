import tkinter
import PriorityQueue as pq
import Grid
import sys

def heuristic(a, b):
    """
    Heuristic function that finds the manhattan distance between point a and b

    :return: The manhattan distance
    """
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def search(board):
    """
    The A star search algorithm
    :return: dictionary of previous positions so we can reconstruct path later
    """
    start = board.start
    frontier = pq.PriorityQueue()
    frontier.put(start, 0)
    prev_pos = {}                   #dictionary to keep track of where we came from
    cost_so_far = {}
    prev_pos[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == board.goal:
            break

        for next in board.neighbors(current):
            new_cost = cost_so_far[current] + board.cost(next)              #calculate the cost to the neighbor coming from current
            if next not in cost_so_far or new_cost < cost_so_far[next]:     #if we've found a cheaper path to the neighbor
                cost_so_far[next] = new_cost                                #update cost
                priority = new_cost + heuristic(board.goal, next)           #set priority f(n) = g(n) + h(n)
                frontier.put(next, priority)                                #add to frontier
                prev_pos[next] = current                                    #set where we came from

    return prev_pos


def reconstruct_path(prev_pos, start, goal):
    """
    Reconstructs the path from came_from
    :return: Path from goal to start as a list of positions
    """
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = prev_pos[current]
    path.append(start)
    return path


def visualization(board):
    """
    Creates a visual representation of the board using Tkinter with rectangles in a grid
    """
    root = tkinter.Tk()
    for y in range(board.height):
        for x in range(board.width):

            value = board.tiles[(x, y)]
            color = "white"
            if value == "#":
                color = "gray"
            elif value == "A":
                color = "red"
            elif value == "B":
                color = "gold2"
            elif value == "w":
                color = "blue"
            elif value == "m":
                color = "gray"
            elif value == "f":
                color = "forest green"
            elif value == "g":
                color = "lawn green"
            elif value == "r":
                color = "orange4"

            tile = tkinter.Canvas(width=30,height=30)                   #Create canvas to put rectangle on
            tile.create_rectangle(0,0,30,30,fill=color)

            if (x,y) in board.path:
                tile.create_oval(10,10,22,22,fill="black")              #Add circle to tile if it is on the path that was found

            tile.grid(row=y,column=x)                                   #Puts canvas in correct grid tile
    root.mainloop()                                                     #Display grid

if __name__ == "__main__":
    filename = str(sys.argv[1])
    grid = Grid.Grid(filename)
    astar = search(grid)                                                #executes the a star algorithm
    grid.set_path(reconstruct_path(astar,grid.start,grid.goal))
    visualization(grid)
