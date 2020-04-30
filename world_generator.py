from random import shuffle, randrange
from util.create_room import rooms
from django.contrib.auth.models import User
from adventure.models import Player, Room

Room.objects.all().delete()

class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x
            
        # Randomizes room order
        shuffled_rooms = list(rooms.keys())
        shuffle(shuffled_rooms)
    

        # Start from lower-left corner (0,0)
        x = -1 # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west


        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                x += 1
            elif direction < 0 and x > 0:
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                y += 1
                direction *= -1

            # Initializes first room of the world.
            if room_count == 0:
                room = Room(room_id=room_count, title="Foyer", description="As you enter the castle, the door slams shut locking you in. Can you find your way out?", x=x, y=y)
            # Creates room objects using the rooms dictionary.
            else:
                room = Room(room_id=room_count, title=shuffled_rooms[room_count-1], description=rooms[shuffled_rooms[room_count-1]], x=x, y=y)
            # Save the room in the World grid
            self.grid[y][x] = room
            # Save room object in the database
            room.save()
            # Increae room count to be used to index both the room key list and to assign room id
            room_count += 1

        # Connect the rooms using a technique common to maze generation
        # Visited array will keep track of rooms that our walker has visited

        vis = [[0] * self.width for _ in range(self.height)] 

        # walk is a recursive function used to connect the rooms randomly with a "walker"   
        def walk(x, y):
            # Setting the value of the visited array element as 1 indicates a room has been visited.
            vis[y][x] = 1
            # Reverse direction dictionary is used to make sure rooms are connected in both directions 
            reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
            # d is an array of neighboring rooms 
            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            # shuffling allows for randomization of the stack as the function is called recursively
            shuffle(d)
            # Create connections between visited rooms and their neighbors
            for (xx, yy) in d:
                # Check to make sure the array indexes are within the range of self.grid
                if xx in range(self.width) and yy in range(self.height): 
                    if vis[yy][xx]: continue
                    if xx == x :
                        if yy < y:
                            room_direction = "s"
                            reverse_dir = reverse_dirs[room_direction]
                            self.grid[y][x].connectRooms(self.grid[yy][xx], room_direction)
                            self.grid[yy][xx].connectRooms(self.grid[y][x], reverse_dir)
                        else:
                            room_direction = "n"
                            reverse_dir = reverse_dirs[room_direction]
                            self.grid[y][x].connectRooms(self.grid[yy][xx], room_direction)
                            self.grid[yy][xx].connectRooms(self.grid[y][x], reverse_dir)
                    if yy == y:
                        if xx < x:
                            room_direction = "w"
                            reverse_dir = reverse_dirs[room_direction]
                            self.grid[y][x].connectRooms(self.grid[yy][xx], room_direction)
                            self.grid[yy][xx].connectRooms(self.grid[y][x], reverse_dir)
                        else: 
                            room_direction = "e"
                            reverse_dir = reverse_dirs[room_direction]
                            self.grid[y][x].connectRooms(self.grid[yy][xx], room_direction)
                            self.grid[yy][xx].connectRooms(self.grid[y][x], reverse_dir)
                    walk(xx, yy)

        # Select random indexes to begin the recursive walk function
        start_x = randrange(self.width)
        start_y = randrange(self.height)
        
        walk(start_x, start_y)


   

# Create world object instance
w = World()
num_rooms = 100
width = 10
height = 10
# Generate rooms
w.generate_rooms(width, height, num_rooms)

#Initialize all players to begin at the 
players=Player.objects.all()
for p in players:
  p.currentRoom=0
  p.save()

print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")