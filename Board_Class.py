from Matrix_Class import Matrix,V
"""
Bugs:
() will allow different similarity rule in different direction
() will allow placing separate block
() doesn't understand quirkle
() will double count scores
() allow 2 blocks in one spot

"""
def get_bonus(spot):
    #return 1
    if spot[0]%8==0 and spot[1]%7==0:
        return 3
    elif spot[0]%5==0 and spot[1]%5==0:
        return 2
    return 1

class Board(Matrix):
    def original_is_legal(self,tiles,spots):
        if len(spots)==0: return False
        local_spots = [spot - self.offset for spot in spots]
        directions = [V(i) for i in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
        def repeat_spots():
            for i,x in enumerate(spots):
                for j,y in enumerate(spots[i+1:]):
                    if x==y:
                        print("two tiles one spot")
                        return True
            return False
        if repeat_spots(): return False

        def spots_filled():
            for spot in local_spots:
                if self.get(spot)!=None:
                    print("spots aren't empty")
                    return True
            return False
        if spots_filled(): return False

        def in_a_line():
            sdiff=[(i-spots[0]).absify() for i in spots]
            sum_diff=V((0,0))
            for i in sdiff:
                sum_diff+=i
            if min(sum_diff)==0:
                return True
            print("Not in a line")
            return False
        if not in_a_line(): return False

        def touching_main():
            if self.is_empty():
                # print("It's empty")
                return True
            for spot in local_spots:
                for d in directions:
                    if self.get(spot+d):
                        return True
            print("not connected to main")
            return False
        if not touching_main(): return False

        board=Board([row[:] for row in self])
        board.offset=self.offset
        shared=[]
        for tile,spot in zip(tiles,spots):
            board=board.place_click(tile,spot)
        local_spots = [spot - board.offset for spot in spots]

        for tile,spot in zip(tiles,local_spots):
            has_neighbor=False
            shared=[]
            for d in directions:
                shared.append(None)
                if board.get(spot+d)!=None:
                    has_neighbor=True
                    looking=spot+d
                    if tile.color==board.get(looking).color:
                        shared[-1]="color"
                        # print("Shared color between {} and {}".format(spot,looking))
                        while board.get(looking)!=None:
                            if tile.color!=board.get(looking).color or tile.shape==board.get(looking).shape:
                                print("Color difference problem in direction {} for {}".format(d,str(tile)))
                                return False
                            looking+=d
                    elif tile.shape==board.get(looking).shape:
                        shared[-1]="shape"
                        while board.get(looking)!=None:
                            if tile.shape!=board.get(looking).shape or tile==board.get(looking):
                                print("Shape difference problem in direction {}".format(d))
                                return False
                            looking+=d
                    else:
                        print("No similarity in direction {}".format(d))
                        return False
            if not has_neighbor:
                print("No neighbor for {}".format(tile))
                return False
            if shared[0] and shared[2]:
                if shared[0] != shared[2]:
                    return False
            if shared[1] and shared[3]:
                if shared[1] != shared[3]:
                    return False
        return True
    def is_legal(self,tiles,spots):
        if len(spots)==0: return False
        local_spots = [spot - self.offset for spot in spots]
        directions = [V(i) for i in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
        def repeat_spots():
            for i,x in enumerate(spots):
                for j,y in enumerate(spots[i+1:]):
                    if x==y:
                        print("two tiles one spot")
                        return True
            return False
        if repeat_spots(): return False

        def spots_filled():
            for spot in local_spots:
                if self.get(spot)!=None:
                    print("spots aren't empty")
                    return True
            return False
        if spots_filled(): return False

        def touching_main():
            if self.is_empty():
                # print("It's empty")
                return True
            for spot in local_spots:
                for d in directions:
                    if self.get(spot+d):
                        return True
            print("not connected to main")
            return False
        if not touching_main(): return False
        sum_diff=V((0,0))
        for i in [(j-spots[0]).absify() for j in spots[1:]]:
            sum_diff+=i
        if sum_diff[1] == 0:
            primary = V((1, 0))
            secondary = V((0, 1))
        elif sum_diff[0]==0:
            primary = V((0, 1))
            secondary = V((1, 0))
        else:
            return False
        score=0
        # Place the tiles on the board
        board=Board([row[:] for row in self])
        board.offset=self.offset
        for tile,spot in zip(tiles,spots):
            board=board.place_click(tile,spot)
        # Get local spots
        local_spots = [spot - board.offset for spot in spots]
        # Gets the primary line
        prim_line = []
        looking = local_spots[0]+primary
        while board.get(looking):
            prim_line.append(board.get(looking))
            looking+=primary
        looking = local_spots[0]
        while board.get(looking):
            prim_line.append(board.get(looking))
            looking-=primary
        # Checking if everyone is in the primary line
        for i in tiles:
            if not (i in prim_line): return False
        # check if primary line works
        color_sim,shape_sim=(True,True)
        for i,x in enumerate(prim_line):
            for y in prim_line[i+1:]:
                if x.color!=y.color or x.shape==y.shape:
                    color_sim=False
        for i,x in enumerate(prim_line):
            for y in prim_line[i+1:]:
                if x.color==y.color or x.shape!=y.shape:
                    shape_sim=False
        # IF the primary line doesn't work, kill it
        if not (color_sim or shape_sim):
            return False
        lnt=len(prim_line)
        if lnt==6:
            score+=12
        elif lnt==1:
            pass
        else:
            score+=lnt
        if 3 in [get_bonus(i) for i in spots]:
            score*=3
        elif 2 in [get_bonus(i) for i in spots]:
            score*=2
            print("bonus")
        pscore=score

        for spot in local_spots: #Check all the secondary lines
            sec_line = []
            # Generate the secondary line
            looking = spot+secondary
            while board.get(looking):
                sec_line.append(board.get(looking))
                looking += secondary
            looking = spot
            while board.get(looking):
                sec_line.append(board.get(looking))
                looking -= secondary
            # Check the secondary line:
            color_sim, shape_sim = (True, True)
            for i,x in enumerate(sec_line):
                for y in sec_line[i + 1:]:
                    if x.color != y.color or x.shape == y.shape:
                        color_sim = False
            for i,x in enumerate(sec_line):
                for y in sec_line[i + 1:]:
                    if x.color == y.color or x.shape != y.shape:
                        shape_sim = False
            if not (color_sim or shape_sim): return False
            lnt=len(sec_line)
            if lnt == 6:
                lnt*=2
            if lnt==1:
                pass
            else:
                lnt*=get_bonus(spot+board.offset)
                score += lnt
        return score
    def score(self,spots):
        sdiff = [(i - spots[0]).absify() for i in spots]
        sum_diff = V((0, 0))
        for i in sdiff:
            sum_diff += i
        # rint("sum_diff is {}".format(sum_diff))
        if sum_diff[1]==0:
            primary=V((1,0))
            secondary=V((0,1))
        else:
            primary=V((0,1))
            secondary=V((1,0))
        score=0
        local_spots = [spot - self.offset for spot in spots]
        # Scoring the PRIMARY axis
        looking=local_spots[0]
        while self.get(looking):
            score+=1
            looking+=primary
        looking=local_spots[0]-primary
        while self.get(looking):
            score+=1
            looking-=primary
        prscore=score
        # print("Primary Score: ",score)
        # Scoring the SECONDARY AXIS
        for spot in local_spots:
            looking=spot+secondary
            exists=False
            while self.get(looking):
                if not exists:
                    exists=True
                    score+=1
                score+=1
                looking+=secondary
            looking=spot-secondary
            while self.get(looking):
                if not exists:
                    exists=True
                    score+=1
                score+=1
                looking-=secondary
        # print("Secondary Score: ",score-prscore)
        return score



    def get(self,spot):
        if spot[1]<0 or spot[1]>=len(self) or spot[0]<0 or spot[0]>=len(self[0]):
            return None
        return self[spot[1]][spot[0]]
    def place(self,tile,spot):
        tile.grid_pos=spot+self.offset
        if spot[1]<0 or spot[1]>=len(self) or spot[0]<0 or spot[0]>=len(self[0]):
            tiles=[i for row in self for i in row if i]
            tiles.append(tile)
            b= make_board(tiles)
            tile.grid_pos=spot+b.offset
            return b
        tile.grid_pos=spot-self.offset
        self[spot[1]][spot[0]]=tile
        return self
    def place_click(self,tile,spot):
        tile.grid_pos=spot
        spot=spot-self.offset
        if spot[1]<0 or spot[1]>=len(self) or spot[0]<0 or spot[0]>=len(self[0]):
            tiles=[i for row in self for i in row if i]
            tiles.append(tile)
            return make_board(tiles)
        tile.grid_pos=spot+self.offset
        self[spot[1]][spot[0]]=tile
        return self
    def all_tiles(self):
        return [i for row in self for i in row if i]
    def is_empty(self):
        # print("Checking if empty")
        for row in self:
            for i in row:
                # print(i)
                if i:
                    return False
        return True

def make_board(tile_list):#=[Tile("no shape","red")]):
    min_x,min_y=tile_list[0].grid_pos
    max_x,max_y=min_x,min_y
    for tile in tile_list:
        x,y=tile.grid_pos

        if x<min_x:
            min_x=x
        if x>max_x:
            max_x=x
        if y<min_y:
            min_y=y
        if y>max_y:
            max_y=y
    board=Board([[None for i in range(max_x-min_x+1)] for j in range(max_y-min_y+1)])
    board.offset=V((min_x,min_y))
    board.center=V(((min_x+max_x+1)/2,(min_y+max_y+1)/2))
    for tile in tile_list:
        x,y=tile.grid_pos-board.offset
        board[y][x]=tile
    return board