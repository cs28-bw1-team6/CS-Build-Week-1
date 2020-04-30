from random import shuffle, randrange
from util.create_room import rooms
from django.contrib.auth.models import User
from adventure.models import Player, Room

Room.objects.all().delete()
# class Room:
#     def __init__(self, id, name, description, x, y):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.n_to = None
#         self.s_to = None
#         self.e_to = None
#         self.w_to = None
#         self.x = x
#         self.y = y
#     def __repr__(self):
#         if self.e_to is not None:
#             return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
#         return f"({self.x}, {self.y})"
#     def connect_rooms(self, connecting_room, direction):
#         '''
#         Connect two rooms in the given n/s/e/w direction
#         '''
#         reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
#         reverse_dir = reverse_dirs[direction]
#         setattr(self, f"{direction}_to", connecting_room)
#         setattr(connecting_room, f"{reverse_dir}_to", self)
#     def get_room_in_direction(self, direction):
#         '''
#         Connect two rooms in the given n/s/e/w direction
#         '''
#         return getattr(self, f"{direction}_to")

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
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1

            # Create a room in the given direction
            # room = Room(room_count, shuffled_keys[room_count] , r_general[shuffled_keys[room_count]], x, y)
            # Note that in Django, you'll need to save the room after you create it
            # room.save()
            if room_count == 0:
                room = Room(room_id=room_count, title="Foyer", description="As you enter the castle, the door slams shut locking you in. Can you find your way out?", x=x, y=y)
            else:
                room = Room(room_id=room_count, title=shuffled_rooms[room_count], description=rooms[shuffled_rooms[room_count]], x=x, y=y)
            # Save the room in the World grid
            self.grid[y][x] = room
            room.save()
            room_count += 1

        vis = [[0] * self.width for _ in range(self.height)] 
        
            
        def walk(x, y):
            vis[y][x] = 1
 
            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if xx in range(self.width) and yy in range(self.height): 
                    if vis[yy][xx]: continue
                #     if xx == x: hor[max(y, yy)][x] = "+  "
                    if xx == x :
                        if yy < y:
                            room_direction = "s"
                            self.grid[y][x].connectRooms(self.grid[yy][xx], room_direction)

                        else:
                            room_direction = "n"
                            self.grid[y][x].connectRooms(self.grid[yy][xx], room_direction)
                #     if yy == y: ver[y][max(x, xx)] = "   "
                    if yy == y:
                        if xx < x:
                            room_direction = "w"
                            self.grid[y][x].connectRooms(self.grid[yy][xx], room_direction)
                        else: 
                            room_direction = "e"
                            self.grid[y][x].connectRooms(self.grid[yy][xx], room_direction)
                    walk(xx, yy)

        start_x = randrange(self.width)
        start_y = randrange(self.height)
        
        walk(start_x, start_y)


    # def print_rooms(self):
    #     '''
    #     Print the rooms in room_grid in ascii characters.
    #     '''

    #     # Add top border
    #     str = "# " * ((3 + self.width * 5) // 2) + "\n"

    #     # The console prints top to bottom but our array is arranged
    #     # bottom to top.
    #     #
    #     # We reverse it so it draws in the right direction.
    #     reverse_grid = list(self.grid) # make a copy of the list
    #     reverse_grid.reverse()
    #     for row in reverse_grid:
    #         # PRINT NORTH CONNECTION ROW
    #         str += "#"
    #         for room in row:
    #             if room is not None and room.n_to is not None:
    #                 str += "  |  "
    #             else:
    #                 str += "     "
    #         str += "#\n"
    #         # PRINT ROOM ROW
    #         str += "#"
    #         for room in row:
    #             if room is not None and room.w_to is not None:
    #                 str += "-"
    #             else:
    #                 str += " "
    #             if room is not None:
    #                 str += f"{room.id}".zfill(3)
    #             else:
    #                 str += "   "
    #             if room is not None and room.e_to is not None:
    #                 str += "-"
    #             else:
    #                 str += " "
    #         str += "#\n"
    #         # PRINT SOUTH CONNECTION ROW
    #         str += "#"
    #         for room in row:
    #             if room is not None and room.s_to is not None:
    #                 str += "  |  "
    #             else:
    #                 str += "     "
    #         str += "#\n"

    #     # Add bottom border
    #     str += "# " * ((3 + self.width * 5) // 2) + "\n"

    #     # Print string
    #     print(str)


w = World()
num_rooms = 100
width = 10
height = 10
w.generate_rooms(width, height, num_rooms)
# w.print_rooms()

players=Player.objects.all()
for p in players:
  p.currentRoom=0
  p.save()

print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")