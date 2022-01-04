import pygame as pg
from sys import exit
from Matrix_Class import Matrix,V
from math import sin, cos
# from Sprite_Classes import Player
from Player_Class import Player
from random import random as rand
from Tile_Class import Tile,waiting_fill
from Board_Class import Board,make_board,get_bonus
from Button_Class import Button,TextBox,Bonus
import pickle

quirkle_length=6
# pickle.dump(["" for i in range(4)],open("player_names.dat",'wb'))

def transform(point):
    global zoom,shift
    return V(point)*zoom+shift

def inverse_transform(point):
    global zoom,shift
    return (V(point)-shift)/zoom

def get_bag():
    bag = []
    for i, color in enumerate(tile_colors[:quirkle_length]):
        for j, shape in enumerate(tile_shapes[:quirkle_length]):
            bag.append(Tile(shape, color))
            bag.append(Tile(shape, color))
            bag.append(Tile(shape, color))
    return bag
def draw_grid():
    min_dx, min_dy = (inverse_transform(origin) - (1, 1)).intify()
    max_dx, max_dy = (inverse_transform(window_size) + (1, 1)).intify()
    screen.blit(background, origin)
    for line_x in range(min_dx, max_dx):
        pg.draw.line(screen, line_color, transform((line_x, min_dy)), transform((line_x, max_dy)), 2)
    for line_y in range(min_dy, max_dy):
        pg.draw.line(screen, line_color, transform((min_dx, line_y)), transform((max_dx, line_y)), 2)
    for x in range(min_dx,max_dx):
        for y in range(min_dy,max_dy):
            spt=(x,y)
            if not B.get(spt-B.offset):
                if get_bonus(spt)==2:
                    two.stamp(screen,transform(spt),(zoom,zoom))

two=Bonus("2x",(0,0,100))
def change_zoom(zoom_slide_rate):
    global zoom,shift
    for i, tile in actual_hand:
        if tile.waiting:
            tile.target_pos = inverse_transform(tile.target_pos)
    shift = shift + (1 - zoom_slide_rate) * inverse_transform(mpos) * zoom
    zoom *= zoom_slide_rate
    for i, tile in actual_hand:
        if tile.waiting:
            tile.target_pos = transform(tile.target_pos)
            tile.target_size = V((zoom, zoom)) * waiting_fill
            tile.to_target()
def start_game():
    global players,player1,turn,show_player_buttons
    players=[]
    for butt in player_name_buttons:
        if butt.player_name:
            players.append(Player(butt.player_name))
    if len(players)==0:
        return False
    for i in players: i.draw_hand(bag)
    for i in players: i.score=0
    current_score_box.changeText("Move score")
    player1=players[0]
    turn=0
    cols=[3 * (c * 2 - background_color) / 4 for c in player_button_colors]
    lst=[(i,b) for i,b in enumerate(player_name_buttons) if b.player_name]
    show_player_buttons=[Button((120,50),player_button_colors[i],"",(0,0,0),player_name_font) for i,b in lst]
    for i,b in enumerate(show_player_buttons):
        b.changeText(players[i].name)
        b.center((70,i*60+30))
        b.size_to_fit()
    return True
def try_to_place():
    global B,counting_down,countdown_timer,actual_hand
    waiting_tiles = [tile for i,tile in actual_hand if tile.waiting]
    spots = [inverse_transform(tile.float_pos).rup() for tile in waiting_tiles]
    score=B.is_legal(waiting_tiles, spots)
    if score:
        for i, tile in actual_hand:
            if tile.waiting:
                B = B.place_click(tile, inverse_transform(tile.target_pos).rup())
                player1.hand[i]=None
                player1.draw(i, bag)
        actual_hand=[(i,t) for i,t in enumerate(player1.hand) if t]
        countdown_timer = countdown_length
        counting_down = True
        player1.score+=score
        show_player_buttons[turn].changeText("{}: {}".format(player1.name,player1.score))
        # print("Score is: {}".format(B.score(spots)))
    if not actual_hand:
        player1.score+=6 #Bonus for finishing the game first
        game_over()
    pass
def click_player_button(i):
    global player_name_selected
    if player_name_selected >= 0:
        btut = player_name_buttons[player_name_selected]
        btut.changeText(btut.text[:-1])
    if player_name_selected == i:
        player_name_selected = -1
    else:
        player_name_selected = i
        player_name_buttons[i].changeText(player_name_buttons[i].text + "|")

def update_legality():
    waiting_tiles = [tile for i,tile in actual_hand if tile.waiting]
    spots = [inverse_transform(tile.target_pos).rup() for tile in waiting_tiles]
    current_score = B.is_legal(waiting_tiles, spots)
    if current_score:
        place_button.changeColor((40, 150, 50))
        current_score_box.changeText("Move score: {}".format(current_score))
    else:
        place_button.changeColor((150, 50, 50))
        current_score_box.changeText("Move score: ")

def game_over():
    screen.blit(helv.render("Game Over",True,(0,0,0)),window_size/2)
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                exit()
        clock.tick(60)

if False:
    my_list=Board([[None for i in range(3)] for j in range(4)])
    my_list.sps()
    my_list[2][1]=1
    my_list.sps()
B=Board([[None]])
B.offset=V((0,0))
B.center=V((.5,.5))

pg.init()
window_size=V((1000,600))
zoom=100
zoom_slide_rate=1.1
clock=pg.time.Clock()
shift=window_size/2
screen=pg.display.set_mode(window_size)
origin=V((0,0))
board_center=V((0.5,0.5))
leftClicking=pg.mouse.get_pressed()[0]

myFont=pg.font.SysFont("timesnewroman",50)

background=pg.Surface(window_size)
background_color=V((118,81,63))# V((139,85,0))
line_color=background_color * 19 / 20
background.fill(background_color)

turn=0

tile_colors=["red","orange","yellow","green","blue","purple","teal"]
tile_shapes=["square","diamond","ninja","star","circle","clover","triangle"]

min_dx, min_dy = (inverse_transform(origin) - (1, 1)).intify()
max_dx, max_dy = (inverse_transform(window_size) + (1, 1)).intify()
screen.blit(background, origin)
pg.display.update()
bag=get_bag()

key_numbers={
    113:"q", 119:"w",101:"e",114:"r",
    116:"t",121:"y",117:"u",105:"i",111:"o",112:"p",
    97:"a",    115:"s",    100:"d",102:"f",    103:"g",104:"h",    106:"j",
    107:"k",    108:"l",122:"z",    120:"x",99:"c",    118:"v",
    98:"b",    110:"n",109:"m",    32:" "
}
capitalize_dict={"q":"Q","w":"W","e":"E","r":"R","t":"T","y":"Y","u":"U","i":"I","o":"O",
    "p":"P","a":"A","s":"S","d":"D","f":"F","g":"G","h":"H","j":"J","k":"K","l":"L","z":"Z",
    "x":"X","c":"C","v":"V","b":"B","n":"N","m":"M"," ":" "}

hand_rects=[pg.Rect((window_size[0]/2+130*(index-3)+10,window_size[1]-130),(110,110)) for index in range(6)]

helv=pg.font.SysFont("helvetica",50)
place_button=Button((150,40),(40,140,40),"Place Tiles",(0,0,0),thickness=1)
place_button.center((900,50))
next_turn_button=Button((300,90),(30,30,30),"Pass to: ",(200,200,200),font=helv)
next_turn_button.center((window_size[0]/2,window_size[1]-100))
play_button=Button((220,70),(200,200,200),"Play Game",(0,0,0),helv)
play_button.center(window_size/2+(0,250))

number_of_players=4
player_name_selected=-1
player_button_colors=[V(i) for i in [(255,0,0),(-70,0,255),(0,255,0),(255,255,0),background_color]]
player_button_colors=[(i+3*background_color)/4 for i in player_button_colors]
player_names=pickle.load(open("player_names.dat","rb"))
player_button_colors[-1]=background_color*10/9
player_name_font=pg.font.SysFont("helvetica",30)
player_name_buttons=[Button((350,70),player_button_colors[-1],"Player {}: ".format(i+1),background_color/3,player_name_font) for i in range(number_of_players)]
for i,butt in enumerate(player_name_buttons):
    butt.center(window_size/2+(0,100*(i-1.3)))
    butt.player_name=player_names[i]
    butt.changeText("Player {}: {}".format(i+1,butt.player_name))
    if butt.player_name:
        butt.changeColor(player_button_colors[i])
        butt.size_to_fit()
show_player_buttons=[]

q_font=pg.font.SysFont("helvetica",70)
quabble_text=TextBox("Quabble",(0,0,0),q_font)
quabble_text.center(window_size/2-(0,250))

wDown = pg.key.get_pressed()[pg.K_w]
aDown = pg.key.get_pressed()[pg.K_a]
upDown  = pg.key.get_pressed()[pg.K_UP]
leftDown  = pg.key.get_pressed()[pg.K_LEFT]
downDown= pg.key.get_pressed()[pg.K_DOWN]
dDown = pg.key.get_pressed()[pg.K_d]
rightDown = pg.key.get_pressed()[pg.K_RIGHT]
sDown = pg.key.get_pressed()[pg.K_s]
space_pressed=pg.key.get_pressed()[pg.K_SPACE]

screen_dragging=False
something_happened=True
going_home=True
tile_selected=-1
tile_click=False
countdown_length=50
counting_down=False
game_state="title"

current_score_box=TextBox("Move score: ",(0,0,0))
current_score_box.center((window_size[0]/2,20))

while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            exit()
        if event.type==pg.KEYDOWN:
            # rint(event.key)
            pass
        if game_state=="playing" and not counting_down:
            if event.type==pg.MOUSEBUTTONDOWN:
                mpos=V(event.pos)
                if event.button==1:
                    leftClicking=True
                    for i,tile in actual_hand:
                        if pg.Rect(tile.float_pos,tile.float_size).collidepoint(mpos):
                            tile_selected=i
                            player1.hand[i].waiting=False
                            tile_click=True
                    if tile_click:
                        tile_click=False
                    elif place_button.collidepoint(mpos):
                        place_button.pressed=True
                    else:
                        screen_dragging=True
                elif event.button==3:
                    clicked_spot=inverse_transform(mpos).rdown()
                    B=B.place_click(tiles.pop(),clicked_spot)

                if event.button==4:
                    change_zoom(zoom_slide_rate)
                if event.button==5:
                    change_zoom(1/zoom_slide_rate)
            elif event.type==pg.MOUSEBUTTONUP:
                mpos=pg.mouse.get_pos()
                if event.button==1:
                    leftClicking=False
                    screen_dragging=False
                    if tile_selected>=0:
                        if player1.hand[tile_selected].target_pos!=hand_rects[tile_selected].topleft:
                            unclicked_spot=inverse_transform(mpos).rdown()
                            if B.get(unclicked_spot-B.offset):
                                player1.hand[tile_selected].send_to_hand(tile_selected)
                            elif unclicked_spot in [inverse_transform(tile.target_pos).rup() for i,tile in actual_hand if tile.waiting]:
                                player1.hand[tile_selected].send_to_hand(tile_selected)
                            else:
                                player1.hand[tile_selected].target_pos=transform(unclicked_spot)-V((.02,.06))*zoom
                                player1.hand[tile_selected].waiting=True
                        else:
                            player1.hand[tile_selected].waiting=False
                        update_legality()
                        tile_selected=-1
                    elif place_button.pressed:
                        place_button.pressed=False
                        if place_button.collidepoint(mpos):
                            try_to_place()

            elif event.type==pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    space_pressed=True
                    going_home=True
                    for i,tile in actual_hand:
                        tile.send_to_hand(i)
                    # for tile in player1.hand:
                    #     if tile.waiting:
                    #         print(waiting)
                    update_legality()
                elif event.key==pg.K_q:
                    for tile in B.all_tiles():
                        bag.append(tile)
                    for player in players:
                        for tile in player.hand:
                            if tile:
                                bag.append(tile)
                    B=Board([[None]])
                    B.offset=V((0,0))
                    B.center=V((.5,.5))
                    game_state="title"
        elif game_state=="next turn":
            if event.type==pg.MOUSEBUTTONDOWN:
                mpos=pg.mouse.get_pos()
                if event.button==1:
                    if next_turn_button.collidepoint(mpos):
                        next_turn_button.pressed=True
                    else:
                        screen_dragging=True
                if event.button==4:
                    change_zoom(zoom_slide_rate)
                if event.button==5:
                    change_zoom(1/zoom_slide_rate)
            elif event.type==pg.MOUSEBUTTONUP:
                if event.button==1:
                    if next_turn_button.collidepoint(mpos):
                        next_turn_button.pressed=False
                        game_state="playing"
                screen_dragging=False
            pass
        elif game_state=="title":
            if event.type==pg.MOUSEBUTTONDOWN:
                mpos=event.pos
                if event.button==1:
                    if play_button.collidepoint(mpos):
                        play_button.pressed=True
                    for butt in player_name_buttons:
                        if butt.collidepoint(mpos):
                            butt.pressed=True
            elif event.type==pg.MOUSEBUTTONUP:
                mpos=event.pos
                if event.button==1:
                    play_button.pressed = False
                    if play_button.collidepoint(mpos):
                        if start_game(): game_state="next turn"
                    for i,butt in enumerate(player_name_buttons):
                        if butt.pressed and butt.collidepoint(mpos):
                            click_player_button(i)
                        butt.pressed=False
            elif event.type==pg.KEYDOWN:
                key = event.key
                if key==9 or key==1073741905:
                    if player_name_selected>=0:
                        click_player_button((player_name_selected + 1) % 4)
                    else:
                        click_player_button(0)
                elif key==1073741906:
                    if player_name_selected>=0:
                        click_player_button((player_name_selected - 1) % 4)
                    else:
                        click_player_button(0)
                elif player_name_selected>=0:
                    butt = player_name_buttons[player_name_selected]
                    if key==8:
                        if butt.player_name!="":
                            if pg.key.get_mods()==64:
                                butt.player_name=""
                            elif pg.key.get_mods()==1:
                                butt.player_name = butt.player_name[:-1]
                                while butt.player_name and butt.player_name[-1]!=" ":
                                    butt.player_name = butt.player_name[:-1]
                            else:
                                butt.player_name=butt.player_name[:-1]
                            if butt.player_name=="":
                                butt.changeColor(player_button_colors[-1])
                    else:
                        if key in key_numbers and len(butt.player_name)<=19:
                            butt.changeColor(player_button_colors[player_name_selected])
                            letter=key_numbers[key]
                            if pg.key.get_mods()==1:
                                letter=capitalize_dict[letter]
                            butt.player_name+=letter
                    pickle.dump([i.player_name for i in player_name_buttons],open("player_names.dat","wb"))
                    butt.changeText("Player {}: {}|".format(player_name_selected+1,butt.player_name))
                    butt.size_to_fit()
    ########################################################################################

    if game_state == "title":
        screen.blit(background, origin)
        play_button.blit(screen)
        for i in player_name_buttons:
            i.blit(screen)
        quabble_text.blit(screen)
    if game_state in ("playing","next turn"):
        if going_home:
            nshift=window_size/2-B.center*zoom
            if (nshift-shift).lenSquared()<4:
                shift=nshift
                going_home=False
            else:
                shift+=(nshift-shift)/15+(nshift-shift).normalize()
            mpos=V(pg.mouse.get_pos())
        elif screen_dragging:
            newmpos=V(pg.mouse.get_pos())
            shift+=(newmpos-mpos)
            for i,tile in actual_hand:
                if tile.waiting:
                    tile.target_pos+=(newmpos-mpos)
                    tile.float_pos+=(newmpos-mpos)
            mpos=newmpos

        draw_grid()
        current_score_box.blit(screen)
        for i,b in enumerate(show_player_buttons):
            b.blit(screen,turn==i)

        tile_list=[i for row in B for i in row if i]
        for i in tile_list:
            i.show_on_board(screen,zoom,shift)
    if game_state == "playing":
        if counting_down:
            countdown_timer -= 1
            if countdown_timer == 0:
                turn = (turn + 1) % len(players)
                player1 = players[turn]
                actual_hand=[(i,t) for i,t in enumerate(player1.hand) if t]
                counting_down = False
                place_button.changeColor((150, 50, 50))
                game_state = "next turn"
        for i,tile in enumerate(player1.hand):
            if tile_selected==i:
                pg.draw.rect(screen, background_color * 2 / 3, hand_rects[i], width=4, border_radius=10)
            else:
                pg.draw.rect(screen, background_color * 2 / 3, hand_rects[i], width=2, border_radius=10)
        actual_hand=[(i,tile) for i,tile in enumerate(player1.hand) if tile]
        for i,tile in sorted(actual_hand,key=lambda t:sum(t[1].target_pos)):
            if tile:
                tile.show_moving(screen)

        # screen.blit(helv.render(player1.name,True,3*(player_button_colors[turn]*2-background_color)/4),(0,0))
        place_button.blit(screen,False)

        if tile_selected>=0:
            player1.hand[tile_selected].dragging(tile_selected,zoom)
            player1.hand[tile_selected].show_moving(screen)
    if game_state == "next turn":
        next_turn_button.changeText("Pass to {}".format(player1.name),show_player_buttons[turn].color)
        # next_turn_button.changeTe
        next_turn_button.blit(screen)

    pg.display.update()

    clock.tick(60)