#engine desktop, or webengine
import pygame
#import webengine
import os

from remi import start, App
import remi.gui as gui

import remi.server


class MouseEngine:
    def __init__(self,engine_type="desktop"):
        self.engine_type=engine_type

    
    def get_pos(self):
        if self.engine_type=="desktop":
            return(pygame.mouse.get_pos())
        elif self.engine_type=="web":
            print("GET POS")
    
    

K_RIGHT=pygame.K_RIGHT
K_LEFT=pygame.K_LEFT
K_UP=pygame.K_UP
K_DOWN=pygame.K_DOWN
K_RETURN=pygame.K_RETURN
K_BACKSPACE=pygame.K_BACKSPACE
K_DELETE=pygame.K_DELETE



class TransformEngine:
    def __init__(self,engine_type="desktop"):
        self.smoothscale=pygame.transform.smoothscale

class FontEngine:
    def __init__(self,engine_type="desktop"):
        self.SysFont=pygame.font.SysFont
        
        
class ImageEngine:
    def __init__(self,engine_type="desktop"):
        self.load=pygame.image.load
                


class DrawEngine:
    def __init__(self,engine_type="desktop"):
        self.engine_type=engine_type
            
        if self.engine_type=="web":
            self.screen = gui.Container(margin='0px auto')
            self.screen.set_size(1600, 900)
            self.screen.set_layout_orientation(gui.Container.LAYOUT_VERTICAL)
            self.screen.style['position']='relative'
            
        elif self.engine_type=="desktop":
            #self.screen = None
            is_resizable=True
            if is_resizable:
                self.screen = pygame.display.set_mode([1366,768],pygame.RESIZABLE)
            else:
                self.screen = pygame.display.set_mode([1366,768])
        
    
        
        
        
    def rect(self,screen,color,pos_size,width=0):
        if self.engine_type=="desktop":
            pygame.draw.rect(screen,color,pos_size,width)
        else:
            pos=pos_size[:2]
            size=pos_size[2:]
            
            container = gui.Container()
            container.style['left'] = str(pos[0])+'px'
            container.style['top'] = str(pos[1])+'px'
            container.style['height'] = str(size[0]-2*width)+'px'
            container.style['width'] = str(size[1]-2*width)+'px'
            container.style['position'] = 'absolute'
            if width==0:
                container.style['background-color'] = "rgb"+str(color)
            else:
                container.style['background-color'] = 'transparent'
                container.style['border'] = str(width)+'px solid rgb'+str(color)
                container.style['opacity'] = str(1)
            screen.append(container)
            print(container)
            return(container)
        
        
    def line(self,screen,color,point1,point2,width=1):
        if self.engine_type=="desktop":
            pygame.draw.line(screen,color,point1,point2,width)
        else:
            label = gui.Label('Forloop.ai')
            label.set_size(100, 30)
            label.style['position'] = 'absolute'
            label.style['left'] = '1250px'
            label.style['top'] = '850px'
            label.style['height'] = '20px'
            label.style['width'] = '20px'
            label.style['color'] = "rgb"+str(color)
            
            screen.append(label)
            return(label)
                
        
        
draw=DrawEngine("desktop")
mouse=MouseEngine("desktop")
font=FontEngine("desktop")
transform=TransformEngine("desktop")
image=ImageEngine("desktop")


class MyApp(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'png')
        super(MyApp, self).__init__(*args, static_file_path={'png': res_path})
        
    def main(self):
        
        draw.screen.onmousedown.connect(self.onmousedown) #,x,y
        
        return draw.screen
    
    
    def onmousedown(self, emitter, x, y):
        print("the mouse position is: ", x, y)
        draw.rect(draw.screen,(100,200,100),[x,y,20,20])
    


if __name__ == "__main__":
    server=start(MyApp, multiple_instance=True, address='0.0.0.0', port=0, debug=True, start_browser=True)

