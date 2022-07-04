

#engine desktop, or webengine
import pygame
#import webengine
import os

from remi import start, App
import remi.gui as gui

import remi.server

import copy

K_RIGHT=pygame.K_RIGHT
K_LEFT=pygame.K_LEFT
K_UP=pygame.K_UP
K_DOWN=pygame.K_DOWN
K_RETURN=pygame.K_RETURN
K_BACKSPACE=pygame.K_BACKSPACE
K_DELETE=pygame.K_DELETE

RESIZABLE=pygame.RESIZABLE

def init(): #pygame.init()
    pygame.init()


class MouseEngine:
    def __init__(self,engine_type="desktop"):
        self.engine_type=engine_type
        self.get_visible=pygame.mouse.get_visible #function
        self.set_visible=pygame.mouse.set_visible #function

    def get_pos(self):
        if self.engine_type=="desktop":
            return(pygame.mouse.get_pos())
        elif self.engine_type=="web":
            import win32api
            print("GET POS - temporary hot fix")
            if os.name == 'nt':  # If windows - get platform mouse position
                pos = win32api.GetCursorPos()
            pos=(pos[0]-207+55,pos[1]-134+20)
            print(pos)
            return(pos)
            
class TransformEngine:
    def __init__(self,engine_type="desktop"):
        self.engine_type=engine_type
        
    def smoothscale(self,image,size):
        
        if self.engine_type=="desktop":
            rescaled_image=pygame.transform.smoothscale(image,size)#self.smoothscale=pygame.transform.smoothscale

        elif self.engine_type=="web":
            #image.style["width"]=str(size[0])+"px"
            #image.style["height"]=str(size[1])+"px"
            #print("SMOOTHSCALE SIZE",size)
            try:
                image.set_size(size[0], size[1])
                image.size=size #to remember size
            
            except AttributeError:
                print("Size could not be set")
            rescaled_image=image
            
            #return(image)
        
        return(rescaled_image)
        
        
class FontEngine:
    def __init__(self,engine_type="desktop"):
        self.engine_type=engine_type
        
    def SysFont(self,font_type,font_size):
        if self.engine_type=="desktop":
            return(pygame.font.SysFont(font_type,font_size))
        elif self.engine_type=="web":
            
            class Font:
                def __init__(self):
                    pass
                
                def render(self,text,antialias,color):
                    
                    label=gui.Label(text)
                    label.text=text
                    return(label)
                    
                    
                def size(self,text):
                    return([len(text),20])
            font=Font()
            
            return(font)
        
    
        
    
    
    
class ImageEngine:
    def __init__(self,engine_type="desktop"):
        self.engine_type=engine_type
        
    def load(self,image_path):
        if self.engine_type=="desktop":
            return(pygame.image.load(image_path))
        elif self.engine_type=="web":
            image = gui.Image('/png:'+image_path)
            #image.style['position'] = 'absolute'
            #image.style['left'] = str(pos[0])+'px'
            #image.style['top'] = str(pos[0])+'px'
            image.path=image_path
            
            image.size=pygame.image.load(image_path).get_size()
            
            def get_size():
                return(image.size)
            image.get_size=get_size
            
            return(image)
                

class DisplayEngine:
    def __init__(self,engine_type="desktop"):
        self.engine_type=engine_type
        self.window_size=[1600,900]
        self.screen=self.set_mode(self.window_size,pygame.RESIZABLE) #generalize
        
    def get_surface(self):
        return(pygame.display.get_surface())

    def get_size_of_window(self):
        if self.engine_type=="desktop":
            screen_size = pygame.display.get_surface().get_size()  # get size of the window - default 1600x900
        else:
            screen_size = self.window_size
        return(screen_size)
    
    def clear(self):
        screen=self.set_mode(self.window_size,None)
    
    
    def set_mode(self,window_size,resizable=None): #set size
        if self.engine_type=="web":
            screen = gui.Container(margin='0px auto')
            screen.set_size(window_size[0], window_size[1])
            screen.set_layout_orientation(gui.Container.LAYOUT_VERTICAL)
            screen.style['position']='relative'
            
            screen.svg = gui.Svg()
            screen.svg.css_height = "900px"
            screen.svg.css_order = "124983688"
            screen.svg.css_position = "static"
            #screen.svg.css_top = "0px"
            screen.svg.css_width = "1600px"
            screen.svg.variable_name = "svg0"
            
            #screen functions
            def fill(color):
                screen.style['background-color']='rgb'+str(color)
                
            def blit(surface,pos):
                
                if hasattr(surface,"path"): #image
                    
                    image_path=surface.path
                    image_size=surface.size
                    #try:
                    #print("IMAGE SIZE",image_size)
                    #    image.copy()
                    #except TypeError:
                    #try:  
                    
                    image = gui.Image('/png:'+image_path)
                    #image=copy.deepcopy(image)
                    #size=[10,10]
                    #size=image.size_memory
                    image.set_size(image_size[0], image_size[1])
                    image.style['position'] = 'absolute'
                    image.style['left'] = str(pos[0])+'px'
                    image.style['top'] = str(pos[1])+'px'
                    image.style['width'] = str(image_size[0])+'px'
                    image.style['height'] = str(image_size[1])+'px'
                    
                    draw.image(screen,image) #,pos,size
                #except:
                    
                elif hasattr(surface,"text"): #label
                        
                    #    pass
                        #print("PYGAME copy")
                    text=surface.text
                    if text!="":
                        label = gui.Label(text)
                        #self.lblTime.set_size(100, 30)
                        #label.set_text('Play time: ')# + str(self.time)
                        label.style['position'] = 'absolute'
                        label.style['left'] = str(pos[0])+'px'
                        label.style['top'] = str(pos[1])+'px'
                    
                        draw.label(screen,label) #,pos,size
                    
            
                #draw.
            
            
            
            screen.fill=fill
            screen.blit=blit
            
            
            
            
            
        else:
            screen=pygame.display.set_mode(window_size,resizable)
        return(screen) # e.g. ([1366,768],pygame.RESIZABLE)
        
    def quit(self):
        pygame.display.quit()
        
    def set_caption(self,app_caption):
        pygame.display.set_caption(app_caption)
        
    def flip(self):
        if self.engine_type=="web":
            pass
        else:
            pygame.display.flip()
        
    

class DrawEngine:
    def __init__(self,engine_type="desktop"):
        self.engine_type=engine_type
        """
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
        print(self.screen)
        """
       
        
    def rect(self,screen,color,pos_size,width=0):
        #print(screen)
        if self.engine_type=="desktop":
            pygame.draw.rect(screen,color,pos_size,width)
        else:
            pos=pos_size[:2]
            size=pos_size[2:]
            
            container = gui.Container()
            container.style['left'] = str(pos[0])+'px'
            container.style['top'] = str(pos[1])+'px'
            container.style['width'] = str(size[0]-2*width)+'px'
            container.style['height'] = str(size[1]-2*width)+'px'
            
            container.style['position'] = 'absolute'
            if width==0:
                container.style['background-color'] = "rgb"+str(color)
            else:
                container.style['background-color'] = 'transparent'
                container.style['border'] = str(width)+'px solid rgb'+str(color)
                container.style['opacity'] = str(1)
            screen.append(container)
            #print(container)
            return(container)
        
        
    def line(self,screen,color,point1,point2,width=1):
        if self.engine_type=="desktop":
            pygame.draw.line(screen,color,point1,point2,width)
        else:
            
            #svg0.attr_class = "Svg"
            #svg0.attr_editor_newclass = False
            
            
            line = gui.SvgLine(point1[0],point1[1],point2[0],point1[1])
            line.set_stroke(2, 'rgb'+str(color))
            screen.svg.append( line )
            """
            label = gui.Label('Forloop.ai')
            label.set_size(100, 30)
            label.style['position'] = 'absolute'
            label.style['left'] = '1250px'
            label.style['top'] = '850px'
            label.style['height'] = '20px'
            label.style['width'] = '20px'
            label.style['color'] = "rgb"+str(color)
            """
            screen.append(screen.svg)
            return(line)
            
    def image(self,screen,image): #,pos,size
        if self.engine_type=="web":
            
            # image = gui.Image('/png:'+image_path)
            # image.set_size(size[0], size[1])
            # image.style['position'] = 'absolute'
            # image.style['left'] = str(pos[0])+'px'
            # image.style['top'] = str(pos[0])+'px'
            # image.path=image_path
            
            screen.append(image)
            return(image)
        
    def label(self,screen,label):
        if self.engine_type=="web":
            
            # image = gui.Image('/png:'+image_path)
            # image.set_size(size[0], size[1])
            # image.style['position'] = 'absolute'
            # image.style['left'] = str(pos[0])+'px'
            # image.style['top'] = str(pos[0])+'px'
            # image.path=image_path
            
            screen.append(label)
            return(label)
        
        #draw.image(screen,image) #,pos,size
        
       

    
class EventEngine:
    def __init__(self,engine_type):        
        self.engine_type=engine_type
        
    def get(self):
        return(pygame.event.get())
        
class TimeEngine:
    def __init__(self,engine_type):
        self.engine_type=engine_type
        
    def wait(self,milliseconds):    
        if self.engine_type=="desktop":
            pygame.time.wait(milliseconds)
        else:
            pass


engine_type="desktop"
        
draw=DrawEngine(engine_type)
mouse=MouseEngine(engine_type)
font=FontEngine(engine_type)
transform=TransformEngine(engine_type)
image=ImageEngine(engine_type)
display=DisplayEngine(engine_type)
time=TimeEngine(engine_type)
event=EventEngine(engine_type)

