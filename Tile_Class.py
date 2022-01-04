import pygame as pg
from Matrix_Class import V
from pygame import gfxdraw
from math import cos,sin,pi
def tile_transform(point,zoom,shift):
    return V(point)*zoom+shift

window_size=V((1000,600))
pg.init()
tile_color=(30,30,30)
shadow_color=(60,60,60)
image_fill=.6
tile_fill=0.9
waiting_fill=1.02
colors={}
colors["red"]=(150,30,30)
colors["green"]=(0,150,0)
colors["blue"]=(50,50,170)
colors["purple"]=(119,63,155)
colors["yellow"]=(240,228,0)
colors["orange"]=(255,119,28)
colors["teal"]=(0,180,150)
ts=V((1000,1000))


class Tile():
    def __init__(self,shape,color,lazy=True):
        self.shape=shape
        self.color=color
        self.grid_pos=V((0,0))
        self.float_pos=V((0,0))
        self.float_size=V((110,110))
        self.target_pos=V((0,0))
        self.target_size=V((110,110))
        self.selected=False
        self.waiting=False
        if lazy:
            self.surf=pg.image.load("Tiles/{}_{}.png".format(color,shape)).convert_alpha()
        else:
            self.surf=pg.Surface(ts,pg.SRCALPHA,32)
            pg.draw.rect(self.surf,tile_color,pg.Rect((0,0),(ts)),border_radius=100)
            if shape=="square":
                self.draw_square(colors[color])
            elif shape=="diamond":
                self.draw_diamond(colors[color])
            elif shape=="ninja":
                self.draw_ninja(colors[color])
            elif shape=="star":
                self.draw_star(colors[color])
            elif shape=="circle":
                self.draw_circle(colors[color])
            elif shape=="clover":
                self.draw_clover(colors[color])
            elif shape=="triangle":
                self.draw_triangle(colors[color])
            pg.image.save(self.surf, "Tiles/{}_{}.png".format(color, shape))
            self.surf=self.surf.convert_alpha()
        self.shadow = pg.Surface(ts, pg.SRCALPHA, 32)
        pg.draw.rect(self.shadow, shadow_color, pg.Rect((0, 0), (ts)), border_radius=100)
        self.hand_surf= pg.transform.scale(self.surf, V((110, 110)))
        self.hand_shadow=pg.transform.scale(self.shadow,V((110,110)))
        self.selected_surf=pg.transform.scale(self.surf, V((120,120)))
        self.selected_shadow=pg.transform.scale(self.shadow,V((120,120)))
    def show_on_board(self,screen,zoom,shift):
        surf=pg.transform.scale(self.surf,V((zoom,zoom))*tile_fill)
        actpos=tile_transform(self.grid_pos+V((1,1))*(1-tile_fill)/2-(.01,.03),zoom,shift)
        apos = tile_transform(self.grid_pos + V((1, 1)) * (1 - tile_fill) / 2+(.01,.03), zoom, shift)
        screen.blit(pg.transform.scale(self.shadow,V((zoom,zoom))*tile_fill),apos)
        screen.blit(surf,actpos)
    def show_in_hand(self,screen,index):
        if self.selected:
            # surf = pg.transform.scale(self.surf, V((120, 120)))
            pos = hand_pos(index)-(5,5)
            apos = hand_pos(index)-(3,-1)
            surf=self.selected_surf
            shadow=self.selected_shadow
        else:
            # surf = pg.transform.scale(self.surf, V((110,110)))
            pos = hand_pos(index)
            apos = hand_pos(index)+(2,6)
            surf=self.hand_surf
            shadow=self.hand_shadow
        screen.blit(shadow,apos)
        screen.blit(surf,pos)
    def show_moving(self,screen):
        self.float_size+=(self.target_size-self.float_size)/7
        self.float_pos += (self.target_pos - self.float_pos)/7
        image=pg.transform.scale(self.surf,self.float_size)
        shadow=pg.transform.scale(self.shadow,self.float_size)
        screen.blit(shadow,self.float_pos+V((.02,.06)).pmul(self.float_size))
        screen.blit(image,self.float_pos)
    def dragging(self,index,zoom):
        mpos=pg.mouse.get_pos()
        self.target_pos=mpos-self.float_size/2
        self.target_size=V((zoom,zoom))*waiting_fill
        rect=pg.Rect(hand_pos(index),(110,110))
        if rect.collidepoint(mpos):
            self.target_pos=hand_pos(index)
            self.target_size=(110,110)
    def __eq__(self,other):
        return isinstance(other,Tile) and self.color==other.color and self.shape==other.shape
    def same_shape(self,other):
        return self.shape==other.shape
    def same_color(self,other):
        return self.color==other.color
    def __str__(self):
        return "{} {}".format(self.color,self.shape)
    def set_hand_pos(self,i):
        self.float_pos=hand_pos(i)+(0,150)
        self.target_pos=hand_pos(i)
        self.target_size=V((110, 110))
        self.waiting=False
    def to_target(self):
        self.float_size=self.target_size
        self.float_pos=self.target_pos
    def send_to_hand(self,i):
        self.target_pos = hand_pos(i)
        self.waiting = False
        self.target_size = V((110, 110))





    def draw_square(self,color):
        the_square=pg.Rect(ts*(1-image_fill)/2,ts*image_fill)
        rad=image_fill*30
        pg.draw.rect(self.surf,color,the_square,border_radius=int(rad))
    def draw_diamond(self,color):
        p=[(0.5,0),(0,0.5),(0.5,1),(1,0.5)]
        points = [V(i) for i in p]
        imf=image_fill*2**(1/2)
        for i in range(len(points)):
            points[i]*=imf
            points[i]+=(V((1,1))*(1-imf)/2)
            points[i]*=ts[0]
        pg.draw.polygon(self.surf,color,points)
    def draw_ninja(self,color):
        crmp=.25
        p=[(0,0),(crmp,.5),(0,1),(.5,1-crmp),(1,1),(1-crmp,.5),(1,0),(.5,crmp)]
        points=[V(i) for i in p]
        imf=image_fill*1.3
        for i in range(len(points)):
            points[i]*=imf
            points[i]+=(V((1,1))*(1-imf)/2)
            points[i]*=ts[0]
        pg.draw.polygon(self.surf,color,points)
    def draw_circle(self,color):
        imf = image_fill * 1.2*ts
        pg.draw.ellipse(self.surf,color,pg.Rect((ts-imf)/2,imf))
    def draw_star(self,color):
        r2=2**(1/2)/2
        crmp=.55
        spec_shift=((1-crmp)/2,(1-crmp)/2)
        p1=[(.5,0),((1-r2)/2,(1-r2)/2),(0,0.5),((1-r2)/2,(1+r2)/2),(.5,1),((1+r2)/2,(1+r2)/2),(1,.5),((1+r2)/2,(1-r2)/2),(.5,0)]
        p1=[V(p) for p in p1]
        p2=[(p1[i]+p1[i+1])/2*crmp+spec_shift for i in range(len(p1)-1)]
        points=[]
        for i in range(len(p2)):
            points.append(p1[i])
            points.append(p2[i])
        imf = image_fill*1.3
        # points=p1
        for i in range(len(points)):
            points[i] *= imf
            points[i] += (V((1, 1)) * (1 - imf) / 2)
            points[i] *= ts[0]
        pg.draw.polygon(self.surf, color, points)
    def draw_clover(self,color):
        imf=image_fill*1.4
        crad=.2
        angle=pi/12
        avec=V((cos(angle),sin(angle)))
        cpos=[(.5-crad,0),(0,.5-crad),(.5-crad,1-2*crad),(1-2*crad,0.5-crad)]
        cpos=[V(p) for p in cpos]
        ccent = [p + (crad, crad) for p in cpos]
        for p in cpos:
            p*=imf
            p+=((1-imf)/2,(1-imf)/2)
            tangle=pg.Rect(p*ts[0],ts*crad*2*imf)
            pg.draw.ellipse(self.surf,color,tangle)

        directions=[V(i) for i in [(1,0),(0,1),(-1,0),(0,-1)]]
        for i,cent in enumerate(ccent):
            d1=directions[-i]
            d2=directions[(2-i)%4]
            polypoints=[avec.cmul(d1)*crad+cent,avec.conj().cmul(d2)*crad+cent]
            polypoints.append(polypoints[1]-.4*(directions[(3-i)%4]+d2*avec[1]))
            polypoints.append(polypoints[0] - .4 * (directions[(3-i) % 4] + d1 * avec[1]))
            for p in polypoints:
                p *= imf
                p += ((1 - imf) / 2, (1 - imf) / 2)
                p*=ts[0]
                # pg.draw.ellipse(self.surf,(255,255,0),pg.Rect(p,(20,20)))
            points=[(p*imf+((1-imf)/2,(1-imf)/2))*ts[0] for p in polypoints]
            pg.draw.polygon(self.surf,color,points)
        # for i,c in enumerate(ccent):
        #     pg.draw.ellipse(self.surf,(255,0,0),pg.Rect((c*imf+((1-imf)/2,(1-imf)/2))*ts[0],(20,20)))
        #     pg.draw.ellipse(self.surf, (255, 0, 0),pg.Rect(((c+.1*directions[i]) * imf + ((1 - imf) / 2, (1 - imf) / 2)) * ts[0], (20, 20)))
        # pg.draw.rect(self.surf,color,pg.Rect(ts/2-V((.5-crad,crad))*ts[0]*imf,V((1-2*crad,2*crad))*ts[0]*imf))
        # pg.draw.rect(self.surf,color,pg.Rect(ts/2-V((crad,.5-crad))*ts[0]*imf,V((2*crad,1-2*crad))*ts[0]*imf))
    def draw_triangle(self,color):
        crmp=.25
        p=[(.5,.5-3**(1/2)/4),(0,.5+3**(1/2)/4),(1,.5+3**(1/2)/4)]
        points=[V(i) for i in p]
        imf=image_fill*1.3
        for i in range(len(points)):
            points[i]*=imf
            points[i]+=(V((1,1))*(1-imf)/2)
            points[i]*=ts[0]
        pg.draw.polygon(self.surf,color,points)

def hand_pos(index):
    return V((window_size[0] / 2 + 130 * (index - 3) + 10, window_size[1] - 130))