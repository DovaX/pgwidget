
import pgwidget.engine as engine

import pygame



import sys

import os

import pandas as pd
from multinherit.multinherit import multi_super

from helper import c

import datetime

"""TKINTER PART"""

import tkinter as tk

import abc
#from tkinter import LEFT



import doxyplot.doxyplot_core as dp







root = tk.Tk()
root.withdraw()





"""

WINDOW_SIZE=[1366,768]

embed = tk.Frame(root, width = WINDOW_SIZE[0], height = WINDOW_SIZE[1]) #creates embed frame for pygame window
embed.grid(columnspan = (600), rowspan = 500) # Adds grid
#embed.pack(side = LEFT) #packs window to the left

#buttonwin = tk.Frame(root, width = 75, height = 500)
#buttonwin.pack(side = LEFT)

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
"""

"""TKINTER END PART"""

def initialize_pg(is_resizable=True):
    
    global bg_color
    global color
    
    bg_color=(150,150,150) #tuple
    
    if is_resizable:
        screen = engine.display.set_mode([1366,768],engine.RESIZABLE)
    else:
        screen = engine.display.set_mode([1366,768])
       
        
    print("SCREEN",screen)
    engine.init()
    engine.display.set_caption("Forloop")
    #clock=pygame.time.Clock()
    try:
        screen.fill(bg_color)
    except AttributeError: #web has no fill function
        print("Screen fill - engine disable")
        
    """
    try:
        window_icon = engine.image.load('png//click.png')
        pygame.display.set_icon(window_icon)
    except FileNotFoundError:
        print("Warning: Icon (icon.png) not found, skipped")
        pass
    """
    color=(200,200,200)
    return(screen)


#screen=initialize_pg()

"""TKINTER PART"""

"""
def open_file(): 
    file = askopenfile(mode ='r', filetypes =[('Python Files', '*.py')]) 
    filename=""
    if file is not None: 
        content = file.read() 
        #print(content) 
        filename=file.name
        
    return(filename)



def run_script_from_file(): 
    file = askopenfile(mode ='r', filetypes =[('Python Files', '*.py')]) 
    filename=""
    if file is not None: 
        content = file.read() 
        #print(content) 
        filename=file.name
    os.system("python "+filename) 
    #return(filename)

global loaded_filename

def open_xlsx_file(*args): 
    table1=args[0]
    file = askopenfile(mode ='r', filetypes =[('Excel files', '*.xlsx')]) 
    filename=""
    if file is not None: 
        #content = file.read() 
        #print(content) 
        filename=file.name
    
    global loaded_filename
    loaded_filename=filename
    df=pd.read_excel(loaded_filename)
    table1.update_data(df)
    return(filename)


def file_save():
    global text
    f = asksaveasfile(mode='w', defaultextension=".txt")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = str(text.get(1.0, END)) # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close() # `()` was missing.


from tkinter import END
from tkinter.filedialog import askopenfile,asksaveasfile

#button1 = Button(buttonwin,text = 'Draw',  command=open_file)
#button1.pack(side=LEFT)
"""




root.update()
    
"""TKINTER END PART"""


class Label:
    def __init__(self,text,color=(0,0,0),pos=[0,0],relative_pos=[0,0],font_type="Calibri",font_size=14,max_text_length=None,visible=True,shown_text_max_length=1000,is_cursor_drawing=False):
        """
        shown_text_max_length = 1000 ... default because of rendering speed
        """
        
        self._text=text
        self.color=color
        self.pos=pos
        self.max_text_length=max_text_length #in pixels
        self.font_type=font_type
        self.font_size=font_size
        self.relative_pos=relative_pos
        self.myfont = engine.font.SysFont(self.font_type, self.font_size)
        self.lbl=self.myfont.render(self.text, True, self.color)
        self.visible=visible
        self.visibility_layer=100
        self.cursor_position=None
        self._cursor_offset_index=None
        self.is_cursor_drawing=is_cursor_drawing
        self.highlighted_text_indices=None #list
        
        self.shown_text_index_offset=0 #how many letters is the shown text offset against original self.text
        self.shown_text=self.text
        self.shown_text_max_length=shown_text_max_length # in letters
        self.selected=False #must be initialized after shown_text_max_length
        self.shown_cursor_offset_index=0
        
        
    @property
    def selected(self):
        return(self._selected)


    @selected.setter
    def selected(self,selected):
        self._selected=selected
        self.refresh_shown_text()
    
        
    @property
    def text(self):
        return(self._text)
        
    @text.setter
    def text(self,text):
        
        self._text=str(text)
        self.refresh_shown_text()
        self.shown_text_index_offset=len(self._text)-len(self.shown_text)
        
    @property
    def cursor_offset_index(self):
        return(self._cursor_offset_index)
    
    @cursor_offset_index.setter
    def cursor_offset_index(self,cursor_offset_index):
        if cursor_offset_index is not None:
            self._cursor_offset_index=max(cursor_offset_index,0)
            
            self.shown_cursor_offset_index=self._cursor_offset_index-self.shown_text_index_offset
        else:
            self._cursor_offset_index=None
        self._recalculate_cursor_position() #TODO: add on_drag
     
          
     
        
    def refresh_shown_text(self):
        if len(self._text)>self.shown_text_max_length:
            self.shown_text=self._text[:self.shown_text_max_length] #needs to be restricted before myfont.size calculation (which takes long)
        else:
            self.shown_text=self._text
    
        self.text_length=self.myfont.size(self.shown_text)[0]
        if self.max_text_length is not None:
            
            while self.text_length>self.max_text_length:
                if self.selected:
                    self.shown_text=self.shown_text[1:]
                else:
                    self.shown_text=self.shown_text[:-1]  
                self.text_length=self.myfont.size(self.shown_text)[0]
        
    def draw(self,screen):
        
        
        #engine.draw.rect(screen,(255,0,0),self.pos+[self.text_length,16])
        if self.is_cursor_drawing:
            self._draw_cursor(screen)
            
            
        
        if self.visible:
            if self.highlighted_text_indices is not None and self.cursor_position is not None: 
                
                pixel_length=self.get_text_pixel_length(letter_index=self.highlighted_text_indices[0])
                pixel_length2=self.get_text_pixel_length(letter_index=self.highlighted_text_indices[1])
                highlighted_length=abs(pixel_length2-pixel_length)
                print("HIGHLIGHT",pixel_length,pixel_length2,highlighted_length)
                
                engine.draw.rect(screen,(0,0,200),self.cursor_position+[highlighted_length,20])
            try:
                self.lbl=self.myfont.render(self.shown_text, True, self.color)
            except pygame.error as e:
                print("Warning: Text has zero width:", e)
                self.lbl = self.myfont.render("", True, self.color)
            except TypeError as e:
                print("Warning: Text might not be unicode - hidden")
                self.shown_text=""
                self.lbl = self.myfont.render("", True, self.color)
            screen.blit(self.lbl, (self.pos[0], self.pos[1]))
            
    def _draw_cursor(self,screen):
        if self.cursor_position is not None:
            engine.draw.line(screen,c.black,[self.cursor_position[0],self.pos[1]-2],[self.cursor_position[0],self.pos[1]+15+(self.font_size-16)])
            
    
    
    
    def is_point_in_rectangle(self,pos):
        
        self.text_length=self.myfont.size(self.shown_text)[0]
        if pos[0]<self.pos[0]+self.text_length and self.pos[0]<pos[0] and pos[1]<self.pos[1]+16 and self.pos[1]<pos[1]:
            return(True)
        else:
            return(False)
    
    def _round_to_nearer_bound(self,value,bound1,bound2):
            """Example: bound1=21, bound2=28; 24.5 is the midpoint; if value greater or equal returns 28, else returns 21"""
            avg=(bound1+bound2)/2
            if value>=avg:
                return(bound2)
            else:
                return(bound1)
    
    
    def get_text_pixel_length(self,letter_index=None):
        """returns text_pixel_length on request"""
        if letter_index is None:
            text_length=self.myfont.size(self.shown_text)[0]
        else:
            text_length=self.myfont.size(self.shown_text[:letter_index])[0]
        return(text_length)
    
    def _round_cursor_position_to_nearest_letter(self,pos):
        x_offset=pos[0]-self.pos[0]
        total_shown_text_length=self.myfont.size(self.shown_text)[0]
        text_length=0
        print(text_length,total_shown_text_length)
        if x_offset>total_shown_text_length:
            letter_index=len(self.shown_text) #
        else:
            letter_index=0       
            while text_length<x_offset:        
                print(text_length,x_offset,total_shown_text_length)
                text_length=self.get_text_pixel_length(letter_index)
                letter_index+=1
            letter_index-=1 # while loop loops incrementing 1 one more time than it should to check stop criterion - this is correction to reference right index in string
        letter_before_index=letter_index-1
        text_before_length=self.myfont.size(self.shown_text[:letter_before_index])[0]
        text_after_length=self.myfont.size(self.shown_text[:letter_before_index+1])[0]
        cursor_x_offset=self._round_to_nearer_bound(x_offset,text_before_length,text_after_length)

        if cursor_x_offset==text_before_length:
            return(letter_before_index)
        elif cursor_x_offset==text_after_length:
            return(letter_before_index+1)
        else:
            return(None)
    
    def _recalculate_cursor_position(self):
        if self.cursor_offset_index is not None: #i.e. if cursor exists (it is not correct to put here shown_cursor_offset_index)
            text_length=self.get_text_pixel_length(self.shown_cursor_offset_index)
            self.cursor_position=[self.pos[0]+text_length-1,self.pos[1]]
        else:
            self.cursor_position=None
    
    def on_click(self,click_around_label_permitted=False,click_with_shift=False):
        """click_around_label_permitted ... when not clicked exactly on label, it still calculates cursor position"""
        self.visible = True
        pos=engine.mouse.get_pos()
        
        print("SHIFT",self.cursor_offset_index,click_with_shift)
        if click_with_shift:
            cursor_offset_index_memory=self.cursor_offset_index
            
        else:
            cursor_offset_index_memory=None
        
        
        if self.is_point_in_rectangle(pos) or click_around_label_permitted:
            self.shown_cursor_offset_index=self._round_cursor_position_to_nearest_letter(pos)
            self.cursor_offset_index=self.shown_cursor_offset_index+self.shown_text_index_offset
            
            if cursor_offset_index_memory is not None:
                self.highlighted_text_indices=sorted([self.cursor_offset_index,cursor_offset_index_memory])
                
            
        else:
            self.cursor_offset_index=None
            self.highlighted_text_indices=None
            
            
    def on_key_down(self,event):
        if self.cursor_offset_index is not None:
            if event.key == engine.K_RIGHT:
                self.shown_cursor_offset_index=min(self.shown_cursor_offset_index+1,len(self.shown_text))
                self.cursor_offset_index=self.shown_cursor_offset_index+self.shown_text_index_offset
            
                
                
            elif event.key == engine.K_LEFT:    
                self.shown_cursor_offset_index=max(self.shown_cursor_offset_index-1,0)
                self.cursor_offset_index=self.shown_cursor_offset_index+self.shown_text_index_offset
            
    
                
                
    
        
            
            
    
        
            
    def get_pixel_length(self):
        text_pixels=self.myfont.size(self.text)[0]
        return(text_pixels)
        
"""          
def refresh(pgwidgets):
    #TO BE DEPRECATED
    screen.fill(bg_color)
        
    for j,widget_type in enumerate(pgwidgets):
        for i,widget in enumerate(widget_type.elements):
            widget.draw(screen)
"""            

 
         
class CollidableComponent(abc.ABC):    
    def is_collided(self,rects):
        is_collided_at_least_once=False
        collision_entry = None
        for i in range(len(rects)):
            if rects[i]!=self:
                
                #print("collision")
                #print(rects[i].pos,self.pos)
                collision=False
                if self.is_point_in_rectangle([rects[i].pos[0],rects[i].pos[1]]):
                    collision=True
                if self.is_point_in_rectangle([rects[i].pos[0]+rects[i].size[0],rects[i].pos[1]]):
                    collision=True
                if self.is_point_in_rectangle([rects[i].pos[0],rects[i].pos[1]+rects[i].size[1]]):
                    collision=True
                if self.is_point_in_rectangle([rects[i].pos[0]+rects[i].size[0],rects[i].pos[1]+rects[i].size[1]]):
                    collision=True
                if rects[i].is_point_in_rectangle([self.pos[0],self.pos[1]]):
                    collision=True
                if rects[i].is_point_in_rectangle([self.pos[0]+self.size[0],self.pos[1]+self.size[1]]):
                    collision=True
                if rects[i].is_point_in_rectangle([self.pos[0],self.pos[1]]):
                    collision=True
                if rects[i].is_point_in_rectangle([self.pos[0]+self.size[0],self.pos[1]+self.size[1]]):
                    collision=True
                    
                    
                if collision:
                    is_collided_at_least_once=True
                    collision_entry = rects[i]
                    #print("collision function")
                    self.collision_function(rects[i])
                    
        if not is_collided_at_least_once:
            self.non_collision_function()
            
        return(is_collided_at_least_once,collision_entry)
    
    
    
    def collision_function(self,target_rect):
        pass
    
    def non_collision_function(self):
        pass
      
        
        
class SelectableComponent(abc.ABC):
    @abc.abstractmethod
    def __init__(self,selection_color=c.red):
        self.selection_count=0
        self.function=lambda *x:None
        self.function_args=[]
        self.is_drawing_selection_frame=True
        self.selection_color=selection_color
        
        
    def draw_selection_frame(self,screen):
        if self.selection_count>0:
            if self.is_drawing_selection_frame:    
                engine.draw.rect(screen,self.selection_color,[self.pos[0],self.pos[1],self.size[0],self.size[1]],1) 
    
    def on_click(self,*args):    
        #show
        self.visible=True
        self.selection_count+=1
        
     
        if len(self.function_args)>0:
            self.function(self.function_args)
        else:
            self.function()  
            
    
   
class ComponentContainingLabels(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        self.labels=[]
        
        
    def draw_labels(self,screen):
        for i,label in enumerate(self.labels):
            if label.visible:
                label.pos=[self.pos[0]+label.relative_pos[0]+5,self.pos[1]+label.relative_pos[1]+5]
                label.draw(screen)
   

class DraggableRect(CollidableComponent,SelectableComponent,ComponentContainingLabels):
    def __init__(self,pos,size,color,is_draggable=True,frame_color=c.frame,relative_pos=[0,0],has_frame=True,fill_color:bool=True,selection_color=c.red):
        multi_super(SelectableComponent,self,selection_color=selection_color)
        multi_super(ComponentContainingLabels,self)
        self.pos=pos
        self.size=size
        self.color=color
        self.is_draggable=is_draggable
        self.is_dragged=False
        self.selected=False
        self.visible=True
        self.visibility_layer=100
        
        self.frame_color=frame_color
        self.relative_pos=relative_pos
        self.has_frame=has_frame
        self.fill_color=fill_color #Fills the 
         
    def draw(self,screen,auto_draw_labels=True): 
        #Warning: Image descendant does not inherit draw method
        if self.visible:
            if self.fill_color:
                engine.draw.rect(screen,self.color,[self.pos[0],self.pos[1],self.size[0],self.size[1]])   
            
            if self.has_frame:
                engine.draw.rect(screen,self.frame_color,[self.pos[0],self.pos[1],self.size[0],self.size[1]],1) 
            self.draw_selection_frame(screen)
             
            if auto_draw_labels:
                self.draw_labels(screen)   
    
    def is_point_in_rectangle(self,pos):
        if self.pos[0]<pos[0] and pos[0]<self.pos[0]+self.size[0] and self.pos[1]<pos[1] and pos[1]<self.pos[1]+self.size[1]:
            return(True)
        else:
            return(False)
    
    
class Cell(DraggableRect):
    def __init__(self,pos,size,color,coor=[0,0],relative_pos=[0,0]):
        super().__init__(pos,size,color,is_draggable=False,has_frame=False)
        self.coor=coor
        self.label=Label("",(0,0,0),[pos[0]+2,pos[1]+4],font_type="Calibri",font_size=15,max_text_length=size[0]-1)
                
    @property
    def text(self):
        return(self.label.text)
    
    @text.setter
    def text(self,text):
        self.label.text=text
        
    def draw(self,screen):
        if not self.selected:
            super().draw(screen)
        else:
            engine.draw.rect(screen,self.color,[self.pos[0],self.pos[1],self.size[0],self.size[1]])  
        
        self.label.draw(screen)  

        

class Scrollbar(DraggableRect): #ImprovedDraggableRect
    def __init__(self,pos,size,percentage=0.2):
        super().__init__(pos,size,color=(240,240,240),frame_color=(200,200,200))
        self.is_clicked=False
        self.percentage=percentage
        self.scrollbar_handle=ScrollbarHandle([pos[0],pos[1]+15],[size[0],(size[1]-30)],self.percentage)
        self.max_handle_offset=(1-self.percentage)*(size[1]-30)
        self.scrollbar_handle_ratio=0
    
    def calculate_handle_offset(self): 
        offset=self.scrollbar_handle.pos[1]-self.pos[1]-15
        #print(offset,self.max_handle_offset,offset/self.max_handle_offset)
        return(offset)
        #self.scrollbar_handle
        
    def calculate_handle_ratio_position(self):
        offset=self.calculate_handle_offset()
        self.scrollbar_handle_ratio=offset/self.max_handle_offset
        print(self.scrollbar_handle_ratio)
        return(self.scrollbar_handle_ratio)
        
    def draw(self,screen):
        super().draw(screen)

        engine.draw.line(screen,(96,96,96),[self.pos[0]+self.size[0]/2,self.pos[1]+6],[self.pos[0]+self.size[0]-5,self.pos[1]+10],2)
        engine.draw.line(screen,(96,96,96),[self.pos[0]+self.size[0]/2,self.pos[1]+6],[self.pos[0]+4,self.pos[1]+10],2)
        engine.draw.line(screen,(96,96,96),[self.pos[0]+self.size[0]/2,self.pos[1]+self.size[1]-6],[self.pos[0]+self.size[0]-5,self.pos[1]+self.size[1]-10],2)
        engine.draw.line(screen,(96,96,96),[self.pos[0]+self.size[0]/2,self.pos[1]+self.size[1]-6],[self.pos[0]+4,self.pos[1]+self.size[1]-10],2)
        
        self.scrollbar_handle.draw(screen)
        
    
    def on_click(self):
        self.scrollbar_handle.on_click()
        self.is_clicked=True
        
        pos=engine.mouse.get_pos()
        
        if pos[1]<self.pos[1]+15: #upper arrow
            self.shift_scrollbar(-10)    
        
        if pos[1]>self.pos[1]+self.size[1]-15: #upper arrow
            self.shift_scrollbar(10)
            
    def shift_scrollbar(self,pixel_offset):
        print(pixel_offset)
        self.scrollbar_handle.pos[1]+=pixel_offset
        #check if valid move
        if self.calculate_handle_ratio_position()<=1 and self.calculate_handle_ratio_position()>=0:
            pass
            #Valid
        else:
            self.scrollbar_handle.pos[1]-=pixel_offset #Revert back
  
                
    def on_unclick(self):
        self.scrollbar_handle.on_unclick()
        self.is_clicked=False
                
    def on_drag(self,offset_pos_y):
        print(offset_pos_y,engine.mouse.get_pos())
        
        self.scrollbar_handle.pos=[self.scrollbar_handle.pos[0],offset_pos_y]
        self.calculate_handle_ratio_position()
        
        if self.scrollbar_handle_ratio<0:
            self.scrollbar_handle.pos=[self.pos[0],self.pos[1]+15]
        elif self.scrollbar_handle_ratio>1:
            self.scrollbar_handle.pos=[self.pos[0],self.pos[1]+self.size[1]-self.scrollbar_handle.size[1]-15]
            
        
 #To be migrated to pgwidget
class ScrollbarHandle(DraggableRect): #ImprovedDraggableRect
    def __init__(self,pos,size,percentage):
        super().__init__(pos,[size[0],size[1]*percentage],color=(240,240,240),frame_color=(200,200,200))
        self.is_clicked=False
              
    def draw(self,screen):
        super().draw(screen)
        if self.is_clicked:
            engine.draw.rect(screen,(166,166,166),[self.pos[0],self.pos[1],self.size[0],self.size[1]])
    
        else:    
            engine.draw.rect(screen,(205,205,205),[self.pos[0],self.pos[1],self.size[0],self.size[1]])
    
    def on_click(self):
        self.is_clicked=True
        
    def on_unclick(self):
        self.is_clicked=False
        


class ScrollableComponent:
    def __init__(self,pos,size,horizontal_offset=-15): 
        self.scrollbar=Scrollbar([pos[0]+size[0]+horizontal_offset,pos[1]],[15,size[1]],0.3)
        self.total_height=size[1]/self.scrollbar.percentage
        self.handle_offset=0 
        
       
    def draw(self,screen):
        self.scrollbar.draw(screen)
 
        
    def on_click(self):
        print("Scrollable component on click")
        pos=engine.mouse.get_pos()
        if self.scrollbar.is_point_in_rectangle(pos):
            self.scrollbar.on_click()
            self.handle_offset = self.scrollbar.calculate_handle_offset()
            
        
    def on_drag(self,offset_pos_y):
        pos=engine.mouse.get_pos()
        print("SCROLLABLE",pos,offset_pos_y)
        if self.scrollbar.is_clicked: 
            self.scrollbar.on_drag(offset_pos_y) 
            self.handle_offset=self.scrollbar.calculate_handle_offset()
       
        
        

class Grid(ScrollableComponent):
    def __init__(self,pos,cell_size,rows,cols,margin=1,frame_cell_color=(212,212,212),frame_border_width=2,scrollbar_horizontal_offset=-15):
        self.pos=pos
        self.cell_size=cell_size
        self.rows=rows
        self.cols=cols
        self.margin=margin
        self.visible=True
        self.table_cells=[]
        self.frame_cell_color=frame_cell_color
        self.frame_border_width=frame_border_width
        self.has_scrollbar=True
        self.camera_row_offset=0
        self.camera_col_offset=0
        
        
        self.table_size=[(self.cell_size[0]+self.margin)*self.cols+int(self.has_scrollbar)*15,(self.cell_size[1]+self.margin)*(self.rows+1)]
        self.frame_cell=Cell(self.pos,self.table_size,self.frame_cell_color)
        self.selected_cell_index=None
        if type(self)==Grid:
            self._initialize_cells()
        super().__init__(pos,self.table_size,scrollbar_horizontal_offset)
        
    
    
    
    def _initialize_cells(self):
        for j in range(self.cols):
            i=0
            for i in range(self.rows):    
                new_pos=[self.pos[0]+j*self.cell_size[0]+j*self.margin,self.pos[1]+i*self.cell_size[1]+i*self.margin]
                self.table_cells.append(Cell(new_pos,self.cell_size,(255,255,255),coor=[i,j]))
            
 
    def is_point_in_rectangle(self,pos):
        if self.pos[0]<pos[0] and pos[0]<self.pos[0]+self.table_size[0] and self.pos[1]<pos[1] and pos[1]<self.pos[1]+self.table_size[1]:
            return(True)
        else:
            return(False)  
        
    def which_cell_is_clicked(self,pos):
        new_j=(pos[0]-self.pos[0])//(self.cell_size[0]+self.margin) #col
        new_i=(pos[1]-self.pos[1])//(self.cell_size[1]+self.margin) #row
        return(new_i,new_j)
        
    def get_row_and_col_of_cell(self,cell):
        """
        Gets row and column indices counted from zero, 0,1,2,...
        self.table_cells is ordered by columns (i.e. first column initialized first,...) - has impact on % and // functions
        """
        index=self.table_cells.index(cell)
    
        row_index=index%(self.rows+1)
        col_index=index//(self.rows+1)
        return(row_index,col_index)
    
    
    def find_cell_index(self,row,col):
        """Assumes rectangular shape of cells"""
        index=row+col*self.rows #+1 for table
        return(index)
            
    def deselect_all_cells(self):
        #print("DESELECTING")
        for index,cell in enumerate(self.table_cells):
            self.table_cells[index].selected=False #redundant at the moment
            self.table_cells[index].label.selected=False
          
        self.selected_cell_index=None
            
    
    def select_cell(self,selected_cell_index):
        #print("SELECT CELL",selected_cell_index)
        self.selected_cell_index=selected_cell_index
        #is_outside_index=self.selected_cell_index>=len(self.table_cells)
        #if is_outside_index:
        #    self.selected_cell_index=None #e.g. clicking on scrollbar (index out of table)

        if self.selected_cell_index is not None:
            self.table_cells[self.selected_cell_index].selected=True #redundant at the moment
            self.table_cells[self.selected_cell_index].label.selected=True
            
    
    def highlight_selected(self,pos):
        if self.is_point_in_rectangle(pos):
            i,j=self.which_cell_is_clicked(pos)
            selected_cell_index=self.find_cell_index(i,j)
            self.deselect_all_cells()
            self.select_cell(selected_cell_index)        
 
    def move_selected(self,direction):
        if self.selected_cell_index is not None:
            i,j=self.table_cells[self.selected_cell_index].coor
            #print(i,j)
            if direction==1:
                target_coordinates=(i,j+1) #right
            if direction==2:
                target_coordinates=(i-1,j) #up
            if direction==3:
                target_coordinates=(i,j-1) #left
            if direction==4:
                target_coordinates=(i+1,j) #down
            target_cell_index=self.find_cell_index(*target_coordinates) 
            if target_cell_index is not None:
                self.deselect_all_cells()
                self.select_cell(target_cell_index)
            else:
                print("Move cam, branch")
                self.move_camera(*target_coordinates)
           
 
        
    def draw(self,screen):
        
        self.frame_cell.draw(screen)
        
        for i,cell in enumerate(self.table_cells):
            
            cell.draw(screen)
        
        for i,cell in enumerate(self.table_cells):
            for j,label in enumerate(cell.labels):
                label.draw(screen)
        
        
        if self.frame_border_width!=-1:
            engine.draw.rect(screen,(130,130,130),[self.pos[0]-1,self.pos[1]-1]+self.table_size,self.frame_border_width)
        
        #selected cell
        
        if self.selected_cell_index is not None:
            cell=self.table_cells[self.selected_cell_index]
            engine.draw.rect(screen,(33,115,70),[cell.pos[0]-2+1,cell.pos[1]-2+1,cell.size[0]+3-1,cell.size[1]+3-1],2) 
            engine.draw.rect(screen,(255,255,255),[cell.pos[0]+cell.size[0]-3,cell.pos[1]+cell.size[1]-3,6,6],2) 
            engine.draw.rect(screen,(33,115,70),[cell.pos[0]+cell.size[0]-2,cell.pos[1]+cell.size[1]-2,5,5]) 
        
        
        
        super().draw(screen)
        
   
    
   
    def on_click(self,pos):
        if self.is_point_in_rectangle(pos):
            self.which_cell_is_clicked(pos)
            self.highlight_selected(pos)
            if self.scrollbar.is_point_in_rectangle(pos):
                self.scrollbar.on_click()
                 
    def on_unclick(self):
        self.scrollbar.on_unclick()
             
    #def on_drag(self,offset_pos_y):
    #    pos=engine.mouse.get_pos()
    #    if self.scrollbar.is_clicked:    
    #        self.scrollbar.on_drag(offset_pos_y) 
   
    def move_camera(self,target_row_index,target_col_index):
        """moves if target cell [row,col] is not visible"""
        self.camera_row_offset #0
        self.camera_col_offset #0
        self.rows #25
        self.cols #16
        #print(target_row_index,self.rows)
        if target_row_index>=self.rows+1: #+1 for header row
            
            #print("Move cam, branch2")
            self.camera_row_offset+=1
            self.update_data(self.df)



class Table(Grid):
    def __init__(self,pos,cell_size,rows,cols,margin=1,include_header=True,frame_cell_color=(212,212,212),header_color=(230,230,230),frame_border_width=2,col_width_dict={},scrollbar_horizontal_offset=-15):
        super().__init__(pos,cell_size,rows,cols,margin=margin,frame_cell_color=frame_cell_color,frame_border_width=frame_border_width,scrollbar_horizontal_offset=scrollbar_horizontal_offset)
        self.include_header=include_header
        
        self.header_color=header_color
        self.col_width_dict=col_width_dict  #key=index of column, value=size_x in pixels
        
        self._init_col_width_dict()
        self._initialize_cells() #Overrides Grid
        
        self.df=None
        self.visibility_layer=100
        
        self.is_ready_for_updating_df_subset=True
        
        
        
     
    def which_cell_is_clicked(self,pos):
        
        
        col_sizes=[0] #initialize first vertical line - splitting columns
        for i in range(self.cols):
            if i in list(self.col_width_dict.keys()):    
                col_sizes.append(self.col_width_dict[i]+self.margin)
            else:
                col_sizes.append(self.cell_size[0]+self.margin)
        
        new_j=None #init
        for j in range(len(col_sizes)):
            
            if pos[0]-self.pos[0]>=sum(col_sizes[:(j+1)]) and pos[0]-self.pos[0]<sum(col_sizes[:(j+2)]):
                new_j=j
                
        
        #new_j=(pos[0]-self.pos[0])//(self.cell_size[0]+self.margin) #col #OLD IMPLEMENTATION
        new_i=(pos[1]-self.pos[1])//(self.cell_size[1]+self.margin) #row
        return(new_i,new_j)
    
    
    
        
    def find_cell_index(self,row,col):
        """Assumes rectangular shape of cells"""
        if row is not None and col is not None:    
            index=row+col*(self.rows+1) #overrides Grid definition
        else:
            index=None
        return(index)
    """
    def _get_cell_size(self,col_index):
        if col_index in self.col_width_dict.keys():
            x_cell_size=self.col_width_dict[col_index]
        else:
            x_cell_size=self.cell_size[0]
        cell_size=(x_cell_size,self.cell_size[1])
        return(cell_size)
    """
    def _init_col_width_dict(self):
        for j in range(self.cols):
            if not j in self.col_width_dict.keys():
                self.col_width_dict[j]=self.cell_size[0]
                
       

    
    def _initialize_cells(self):
        #Overrides Grid
        #print(self.col_width_dict)
        cumulative_x_pos=0
        for j in range(self.cols):
            i=0
            new_pos=[self.pos[0]+cumulative_x_pos+j*self.margin,self.pos[1]+i*self.cell_size[1]+i*self.margin]
            self.table_cells.append(Cell(new_pos,[self.col_width_dict[j],self.cell_size[1]],self.header_color,coor=[i,j]))
            for i in range(1,self.rows+1):    
                new_pos=[self.pos[0]+cumulative_x_pos+j*self.margin,self.pos[1]+i*self.cell_size[1]+i*self.margin]
                self.table_cells.append(Cell(new_pos,[self.col_width_dict[j],self.cell_size[1]],(255,255,255),coor=[i,j]))
            
            cumulative_x_pos+=self.col_width_dict[j]
            
                
    def draw(self,screen):
        super().draw(screen)
        
        
          
    def draw_children(self):
        pass
        
       

        
    
    
    def show_data_subset(self,df,row_index=0,col_index=0):
        #a=datetime.datetime.now()
        
        subset_df=df.iloc[row_index:(row_index+self.rows),col_index:(col_index+self.cols)]
        #b=datetime.datetime.now()
        #print("SUBSET",b-a)
        return(subset_df)
    
    
    
    
    def on_drag(self,offset_pos_y):
        maximal_row_index_of_top_cell=0
        if self.df is not None:
            maximal_row_index_of_top_cell=max(len(self.df)-self.rows,0)
        current_camera_offset=int(self.scrollbar.scrollbar_handle_ratio*maximal_row_index_of_top_cell)
        super().on_drag(offset_pos_y)
        if current_camera_offset!=int(self.scrollbar.scrollbar_handle_ratio*maximal_row_index_of_top_cell):    
            self.is_ready_for_updating_df_subset=True
                
    
                
    def update_data(self,df, rows = None):
        """data layer"""
        
        self.df=df
        
        
        
        """TODO: Maybe this could be refactored to not update the whole dataframe, just the view and save some computational power"""
        maximal_row_index_of_top_cell=max(len(self.df)-self.rows,0)  #shouldnt be negative
        normalized_scrollbar_handle_ratio=max(min(self.scrollbar.scrollbar_handle_ratio,1),0)
        row_index_of_current_scrolled_cell=int(normalized_scrollbar_handle_ratio*maximal_row_index_of_top_cell)
        self.camera_row_offset=row_index_of_current_scrolled_cell #integer index (how many rows is the table shifted downwards)
        
        
        
        
        self.subset_df=self.show_data_subset(df,self.camera_row_offset,self.camera_col_offset)
        self.table_cells=[]
        self._initialize_cells()
        if rows is None:
            rows = self.subset_df.shape[0]
        
        list1=self.subset_df.values.tolist()
        
        column_names=self.subset_df.columns
        i=0
        #b=datetime.datetime.now()
        #print(b-a)
        for j in range(len(column_names)):
            cell_index=self.find_cell_index(0,j)
            if cell_index is not None:
                self.table_cells[cell_index].label.text=str(column_names[j])     
        for i in range(min(len(list1), rows)):
            b=datetime.datetime.now()
            #print(i,b-a)
            for j in range(len(list1[i])):
                cell_index=self.find_cell_index(i+1,j) #skipping header -> +1
                if cell_index is not None:
                    self.table_cells[cell_index].label.text=str(list1[i][j]) 
                    
        #b=datetime.datetime.now()
        #print(b-a)
        
                    
    
        
    

class ButtonImage(DraggableRect):
    def __init__(self,pos,size,img,text="",function=lambda *args:None,draggable=False): #default: do nothing function
        super().__init__(pos,size,(0,0,0),is_draggable=draggable)    
        self.pos=pos
        self.size=size
        self.img=img
        
        self.rescale()
        self.function=function
        self.animation_index=0
        self.animation_drawings_per_frame=5
        self.animation_drawings_index=0
    
    def rescale(self):
        if type(self.img)!=list: #animation
            self.img=engine.transform.smoothscale(self.img, (self.size[0], self.size[1]))
                
    def draw(self,screen):   
        if type(self.img)==list: #animation
            screen.blit(self.img[self.animation_index],self.pos)    
            
            self.animation_drawings_index+=1
            self.animation_drawings_index%=self.animation_drawings_per_frame
            
            if self.animation_drawings_index==0:
                self.animation_index+=1
                self.animation_index%=len(self.img)
            
            
        else: #static img
            screen.blit(self.img,self.pos)
        
    def run_function(self):
        self.function()


def save_df(table1):
    table1.df.to_excel("name.xlsx")
  

class RadioButton(DraggableRect):
    def __init__(self,pos,text,radio_group,selected=False):
        self.size=[20,20]
        super().__init__(pos,self.size,(0,0,0),is_draggable=False)
        self.pos=pos
        self.text=text
        self.radio_group=radio_group
        self.selected=selected
                
        try:
            self.img_empty = engine.image.load('radio_empty.png')
        except:
            self.img_empty = engine.image.load('img//radio_empty.png')
            
        try:
            self.img_full = engine.image.load('radio_full.png')
        except:
            self.img_full = engine.image.load('img//radio_full.png')
            
        #self.img_empty=engine.image.load("radio_empty.png")
        #self.img_full=engine.image.load("radio_full.png")
        self.rescale()

    def rescale(self):
        self.img_empty=engine.transform.smoothscale(self.img_empty, (self.size[0], self.size[1]))
        self.img_full=engine.transform.smoothscale(self.img_full, (self.size[0], self.size[1]))
           
        
    
    def draw(self,screen):
        if self.selected:
            screen.blit(self.img_full,self.pos)
        else:
            screen.blit(self.img_empty,self.pos)

class CheckBox(DraggableRect):
    def __init__(self, pos, relative_pos=[0,0], selected=False,color=c.forloop_lighter,):
        self.size=[18,18]
        super().__init__(pos,self.size,(0,0,0),is_draggable=False,relative_pos=relative_pos)
        self.pos=pos
        self.selected=selected
        try:
            self.img_unticked = engine.image.load('src//png//checkbox_unticked.png')
        except:
            self.img_unticked = engine.image.load('png//checkbox_unticked.png')
            
        try:
            self.img_ticked = engine.image.load('src//png//checkbox_ticked.png')
        except:
            self.img_ticked = engine.image.load('png//checkbox_ticked.png')
        
            
        self.rescale()
        
    def rescale(self):
        self.img_unticked=engine.transform.smoothscale(self.img_unticked, (self.size[0], self.size[1]))
        self.img_ticked=engine.transform.smoothscale(self.img_ticked, (self.size[0], self.size[1]))
    
    def on_click(self):
        pos=engine.mouse.get_pos()
        if self.is_point_in_rectangle(pos):
            self.selected = not self.selected
    
    def draw(self,screen):
        if self.visible:
            if self.selected:
                #engine.draw.rect(screen,(250,0,0),self.pos+self.size)
                screen.blit(self.img_ticked,self.pos)
            else:
                screen.blit(self.img_unticked,self.pos)
                #super().draw(screen)
                #screen.blit(self.img_empty,self.pos)
    



class TextContainerRect(DraggableRect,abc.ABC):
    def __init__(self, text, pos, size, color=c.white, is_draggable=True, relative_pos=[0, 0],selection_color=c.red):
        super().__init__(pos, size, color, is_draggable=is_draggable, frame_color=c.frame,relative_pos=relative_pos,selection_color=selection_color)
        self.labels = [Label(text, c.black)]
        self.visible = True
        self.is_child = False
        self.relative_pos = relative_pos
        self.selected=False
        self.text=text#text
    
    @property
    def selected(self):
        return(self._selected)
    
    @selected.setter
    def selected(self,selected):
        if len(self.labels)>0:
            self.labels[0].selected=selected
        self._selected=selected
    
    @property
    def visible(self):
        return(self._visible)

    @visible.setter
    def visible(self,visible):
        if len(self.labels)>0:
            self.labels[0].visible=visible
        #if hasattr(self,"forloop_temp_variable_rect"):
        #    if self.forloop_temp_variable_rect is not None:
        #        self.forloop_temp_variable_rect.visible=visible
                
        self._visible=visible

    @property
    def text(self):
        
        
        return (self._text)

    @text.setter
    def text(self, text):
        self._text = text
        self.labels[0].text = text
        

        # Entry inherits draw method


    def draw(self, screen):
        super().draw(screen)
        for i, label in enumerate(self.labels):
            # print("Drawing",label.text)
            # print("Drawing",label.shown_text)
            label.draw(screen)

    def on_click(self, glc, click_with_shift=False):
        # print("TRYING DESELECT")
        # glc.table1.deselect_all_cells() #deselect cells in order to be able to write in Entry
        # print("SELECTED_CELL",glc.table1.selected_cell_index)
        self.labels[0].on_click(click_around_label_permitted=True,click_with_shift=click_with_shift)
        super().on_click(glc)
        glc.text = self.text
        glc.selected_entry = self
        self.selected=True
        # print("ENTRY CLICKED",self,self.text,self.labels)
        

    def on_unclick(self, glc):
        self.selected=False
        

class Entry(TextContainerRect):
    def __init__(self, text, pos, size, color=c.white, is_draggable=True, relative_pos=[0, 0],is_password=False,selection_color=c.red):
        self.is_password=is_password #must be initialized before text definition (in super())
        super().__init__(text, pos, size, color=color, is_draggable=is_draggable, relative_pos=relative_pos,selection_color=selection_color)
        self.labels = [Label(text, c.black)]
        self.is_child = False
        self.relative_pos = relative_pos
        
    
    @property
    def text(self):        
        self._asterisk_text="".join(len(self._text)*["*"])
        return (self._text)

    @text.setter
    def text(self, text):
        self._text = text
        if self.is_password:   
            self._asterisk_text="".join(len(self._text)*["*"])
            self.labels[0].text = self._asterisk_text
        else:
            
            self.labels[0].text = text
        

    def draw(self, screen):
        super().draw(screen)
        for i, label in enumerate(self.labels):
            # print("Drawing",label.text)
            # print("Drawing",label.shown_text)
            label.draw(screen)

    def on_click(self, glc, click_with_shift=False):
        print("TRYING DESELECT",click_with_shift)
        # glc.table1.deselect_all_cells() #deselect cells in order to be able to write in Entry
        # print("SELECTED_CELL",glc.table1.selected_cell_index)
        self.labels[0].on_click(click_around_label_permitted=True,click_with_shift=click_with_shift)
        super().on_click(glc)
        glc.text = self.text
        glc.selected_entry = self
        self.selected=True
        # print("ENTRY CLICKED",self,self.text,self.labels)
        








class TextArea(TextContainerRect):
    def __init__(self,pos,size,text,border_color=(0,0,0),color=(255,255,255),is_draggable=False,relative_pos=[0,0],editable_text=True):
        super().__init__(text, pos, size, color=color, is_draggable=is_draggable, relative_pos=relative_pos)
        
        #super().__init__(pos,size,color,is_draggable=False)
        self.pos=pos
        self.size=size
        self.text=text
        self.labels=[]
        self.labels.append(Label(self.text,(0,0,0),[pos[0]+2,pos[1]+4],font_type="Calibri",font_size=15,max_text_length=size[0]-1))
        self.border_color=border_color
        self.color=color
        self.fit_text_to_textarea()
        
        self.visible = True
        self.selected=False
        
        self.editable_text=editable_text
       
    @property
    def text(self):
        return (self._text)

    @text.setter
    def text(self, text):
        self._text = text
        self.labels[0].text = text 
       
    @property
    def visible(self):
        return(self._visible)

    @visible.setter
    def visible(self,visible):
        if len(self.labels)>0:
            self.labels[0].visible=visible
        #if hasattr(self,"forloop_temp_variable_rect"):
        #    if self.forloop_temp_variable_rect is not None:
        #        self.forloop_temp_variable_rect.visible=visible
                
        self._visible=visible
        
    @property
    def selected(self):
        return(self._selected)
    
    @selected.setter
    def selected(self,selected):
        if len(self.labels)>0:
            self.labels[0].selected=selected
        self._selected=selected
        
    @property
    def label(self):
        return(self.labels[0])
    
    @label.setter
    def label(self,label):
        self.labels[0]=label

    def blit_text(self, surface, text, color=(0,0,0)):
        words = [word.split(' ') for word in self.label.text.splitlines()]
        space = self.label.myfont.size(' ')[0]
        max_height = self.size[1]-10
        x, y = self.label.pos
        for line in words:
            for word in line:
                word_surface = self.label.myfont.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= self.label.max_text_length + self.label.pos[0]:
                    x = self.label.pos[0]
                    y += word_height
                    if y+word_height >= self.label.pos[1] + max_height:
                        
                        break
                    
        
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = self.label.pos[0]
            y += word_height
            if y >= self.label.pos[1] + max_height:
                break
        
    def draw(self,screen):
        super().draw(screen)
        engine.draw.rect(screen,self.border_color,[self.pos[0],self.pos[1],self.size[0],self.size[1]],1)
        self.blit_text(screen, self.label.text)
        #self.label.draw = self.blit_text
        #self.label.draw(screen, self.label.text)

    def fit_text_to_textarea(self):
        words = self.text.split()
        final_text = ""
        line = ""
        for word in words:
            if line:
                if self.label.myfont.size(line + " " + word)[0] > self.size[0] + 3:
                    final_text += line + "\n"
                    line = word
                else:
                    line += " " + word
            # empty line
            else:
                line += word
        if line:
            final_text += line + "\n"
        self.label.text = final_text
        
        
    def on_click(self, glc):
        # print("TRYING DESELECT")
        # glc.table1.deselect_all_cells() #deselect cells in order to be able to write in Entry
        # print("SELECTED_CELL",glc.table1.selected_cell_index)
        self.labels[0].on_click(click_around_label_permitted=True)
        super().on_click(glc)
        glc.text = self.text
        glc.selected_entry = self
        self.selected=True
        # print("ENTRY CLICKED",self,self.text,self.labels)
        

    def on_unclick(self, glc):
        self.selected=False




class Button(DraggableRect):
    def __init__(self,pos,size,text,function=lambda *args:None,function_args=None,border_color=(0,0,0),color=(200,200,200),relative_pos=[0,0],visible=True,hover_color=(120,120,120),hover_label_color=(0,0,0)):
        super().__init__(pos,size,color,is_draggable=False)
        self.pos=pos
        self.size=size
        self.border_color=border_color
        self.color=color
        self.text=text
        self.label=Label(self.text,(0,0,0),[pos[0]+2,pos[1]+4],font_type="Calibri",font_size=15,max_text_length=size[0]-1,relative_pos=[2,4])
        self.function=function
        self.is_clicked=False
        self.function_args=function_args
        self.relative_pos=relative_pos
        self.visible=visible
        self.visibility_layer=100
        self.hover_color=hover_color
        self.hover_label_color=hover_label_color
        

        
    def draw(self,screen):
        #print(self.label.color)
        if self.visible:
            if self.is_clicked:
                engine.draw.rect(screen,(180,180,180),[self.pos[0],self.pos[1],self.size[0],self.size[1]]) 
            else:
                super().draw(screen)
            engine.draw.rect(screen,self.border_color,[self.pos[0],self.pos[1],self.size[0],self.size[1]],1)  
            self.label.draw(screen)
            
            pos=engine.mouse.get_pos()
            self.on_hover(screen,pos)
    
    def on_hover(self,screen,pos):
        if self.is_point_in_rectangle(pos):
            engine.draw.rect(screen,self.hover_color,[self.pos[0],self.pos[1],self.size[0],self.size[1]])  
            engine.draw.rect(screen,self.border_color,[self.pos[0],self.pos[1],self.size[0],self.size[1]],1)  
            
            orig_label_color=self.label.color
            self.label.color=self.hover_label_color
            self.label.draw(screen) 
            self.label.color=orig_label_color
            
    def run_function(self,*args):
        if len(args)>0:
            self.function(args)
        elif self.function_args is not None:
            self.function(self.function_args)
        else:
            self.function()
            
            
    def on_click(self):
        if self.visible:
            self.run_function()
        

class ComboBox(DraggableRect):
    def __init__(self, pos, size, values, text=None, color=(212,212,212), border_color=(0,0,0),hover_color=(120,120,120),hover_label_color=(0,0,0),relative_pos=[0,0]):
        super().__init__(pos, size, color, is_draggable=False)
        self.values = values
        #self.text = text
        self.border_color = border_color
        #self._cells = []
        self._cells = self._init_option_cells()
        
        self._is_rolled = False
        self.visible=True
        self.function=lambda *x:None
        self.function_args=[]
        self.relative_pos=relative_pos
        self.multiselect_indices=None #dict for multiselect
        self.multiselect_values=[True,False] #True must be always the first element, False must be always the last element (Can be also 1 and 0)
        self.hover_color=hover_color
        self.hover_label_color=hover_label_color
        
        if text:
            self.cell = Cell(self.pos, self.size, self.color, coor=[0, 0],relative_pos=[2,2])
            self.cell.text = text
            #self.cell.label.pos[0]=self.cell.label.pos[0]+4#2 pixels from border
            #self.cell.label.pos[1]=self.cell.label.pos[1]+3
            #self.cell.label.relative_pos[0]=self.cell.label.relative_pos[0]+2#2 pixels from border
            #self.cell.label.relative_pos[1]=self.cell.label.relative_pos[1]+2
        #TODO elif - create empty Cell
       
        
       
     
        
    @property
    def chosen_cell(self):
        return(self.cell)
    
    
    @chosen_cell.setter
    def chosen_cell(self,chosen_cell):
        index=self._cells.index(chosen_cell)
        self.choose_by_index(index)
        self.cell=chosen_cell    
    
    
    
    def choose_cell_by_string(self,string):
        chosen_index=None
        #print("CHOOSE",self._cells)
        #print("CHOOSE STRING",string)
        for i,x in enumerate(self._cells):
            #print(x,x.text,string)
            if x.text==string:
                chosen_index=i
                #print("CHOSEN_INDEX",i)
        if chosen_index is not None:        
            self.choose_by_index(chosen_index+1) #+1 for empty cell
            self.roll()
    

    def draw(self,screen):
        if self.visible:
            
            self._update_cells_positions()
            if hasattr(self, "cell"):
                engine.draw.rect(screen,self.color,self.cell.pos+self.cell.size)    
                self.cell.draw(screen)
                engine.draw.rect(screen,self.border_color,self.cell.pos+self.cell.size,1)
                engine.draw.line(screen,(0,0,0),[self.pos[0]+self.size[0]-15,self.pos[1]+self.size[1]/2-2],[self.pos[0]+self.size[0]-10,self.pos[1]+self.size[1]/2+3],3)
                engine.draw.line(screen,(0,0,0),[self.pos[0]+self.size[0]-10,self.pos[1]+self.size[1]/2+3],[self.pos[0]+self.size[0]-5,self.pos[1]+self.size[1]/2-2],3)
                #engine.draw.line(screen,(0,0,0),[self.pos[0]+self.size[0]-18,self.pos[1]],[self.pos[0]+self.size[0]-18,self.pos[1]+self.size[1]],1)
                
            if self._is_rolled:
                pos=engine.mouse.get_pos()
                for cell, value in zip(self._cells, self.values):
                    cell.text = value
                    cell.draw(screen)
                self.on_hover(screen,pos)
                
                self._draw_multiselect_crosses(screen)
     
        
            
    def on_hover(self,screen,pos):
        if self.pos[0]<pos[0] and pos[0]<self.pos[0]+self.size[0] and self.pos[1] < pos[1] and pos[1] < self.pos[1] + self.size[1] * (len(self.values) + 1): #hovering
            #super().draw(auto_draw_labels=False)
            y=pos[1]-self.pos[1]
            option_height=self.size[1]
            index=y//option_height #0 - selected item
            if index!=0: #not hover over selected item
                engine.draw.rect(screen,self.hover_color,[self.pos[0],self.pos[1]+index*option_height,self.size[0],option_height])    
                self._cells[index-1].label.color=self.hover_label_color
                self._cells[index-1].label.draw(screen)
                self._cells[index-1].label.color=(0,0,0)
                
    def _draw_multiselect_crosses(self,screen):
        if self.multiselect_indices is not None:
            for multiselect_index,value in self.multiselect_indices.items(): 
                if value!=self.multiselect_values[-1]: #i.e. value!=False
                    engine.draw.line(screen,(0,0,0),[self.pos[0]+self.size[0]-12,self.pos[1]+self.size[1]*(1/4+multiselect_index)+3],[self.pos[0]+self.size[0]-8    ,self.pos[1]+self.size[1]*(1/4+multiselect_index)+7],2)
                    engine.draw.line(screen,(0,0,0),[self.pos[0]+self.size[0]-8,self.pos[1]+self.size[1]*(1/4+multiselect_index)+3],[self.pos[0]+self.size[0]-12,self.pos[1]+self.size[1]*(1/4+multiselect_index)+7],2)
                    #engine.draw.line(screen,(0,0,0),[self.pos[0]+self.size[0]-18,self.pos[1]],[self.pos[0]+self.size[0]-18,self.pos[1]+self.size[1]],1)
                    

    
    def is_point_in_rectangle(self,pos):
        if not self._is_rolled:
            result=super().is_point_in_rectangle(pos)
            return(result)
        else:
            if self.pos[0]<pos[0] and pos[0]<self.pos[0]+self.size[0] and self.pos[1] < pos[1] and pos[1] < self.pos[1] + self.size[1] * (len(self.values) + 1):
                return(True)
            else:
                return(False)  
                    
    def on_click(self):
        pos=engine.mouse.get_pos()
        #if self.visible:   
            
            
        if self._is_rolled and self.pos[1] < pos[1] and pos[1] < self.pos[1] + self.size[1] * (len(self.values) + 1):
            self.choose(pos)
            
        elif not self._is_rolled and self.is_point_in_rectangle(pos):
            self.roll()
            
            

    def roll(self):
        if not self._is_rolled: 
            self._cells = self._init_option_cells()
            self._dy = self.size[1] * (len(self.values) + 1)        
        else:
            self.run_function()
        self._is_rolled = not self._is_rolled
    
    def run_function(self):
        self.function(self.function_args)
    
    
    def choose_by_index(self,index):
        """Accepts index where 0 is empty choice, 1 is first choice,..."""
        
        if self.multiselect_indices is None:
            if index == 0:
                self.roll()
            else:
                self.cell.text = self.values[index - 1]
                self.roll()
        else:
            if index == 0:
                self.roll()
            elif index in list(self.multiselect_indices.keys()):
                next_multiselect_value=self._get_next_multiselect_value(self.multiselect_indices[index])
                self.multiselect_indices[index]=next_multiselect_value
            elif index<=len(self.values):
                self.multiselect_indices[index]=self.multiselect_values[0]
    
    
    def choose(self, pos):
        index = abs((pos[1] - self.pos[1]) // self.size[1])
        self.choose_by_index(index)

    def _get_next_multiselect_value(self,value):
        index=self.multiselect_values.index(value)
        if index+1>=len(self.multiselect_values):
            final_index=0
        else:
            final_index=index+1
        return(self.multiselect_values[final_index])

    def _init_option_cells(self):
        tmp = []
        for i in range(len(self.values)):
            cell=Cell([self.pos[0], self.pos[1] + self.size[1] * (i + 1)], self.size, self.color, coor=[0, i + 1])
            cell.text=self.values[i]
            tmp.append(cell)
        return (tmp)

    def _update_cells_positions(self):
        self.cell.pos=[self.pos[0], self.pos[1]]
        self.cell.label.pos=[self.pos[0], self.pos[1]]
        
        for i in range(len(self._cells)):
            self._cells[i].pos=[self.pos[0], self.pos[1] + self.size[1] * (i + 1)]
            self._cells[i].label.pos=[self.pos[0], self.pos[1] + self.size[1] * (i + 1)]



    


class CascadeMenu(Button):
    def __init__(self,pos,size,text,color=(100,100,100),border_color=(0,0,0)):
        super().__init__(pos,size,text,color=color,border_color=border_color)       


    def draw(self,screen):
        super().draw(screen)


"""
import tkinter as tk

def donothing():
    pass


root = tk.Tk()


menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

"""



class DoxyplotImage(ButtonImage,dp.Doxyplot):  
    """Not used at the moment"""
    def __init__(self,pos,size,img=None,is_draggable=True,frame_color=c.frame,relative_pos=[0,0],has_frame=True):
        multi_super(ButtonImage,self,pos=pos,size=size,img=img,draggable=True)
        multi_super(dp.Doxyplot,self)
        #self.selection_count=0
        

    def plot(self):
        pass
    
    
    def draw(self,screen):
        engine.draw.rect(screen,(100,200,100),self.pos+self.size,1)
        super().draw(screen)
        
        






class PgWidget:
    def __init__(self,click_element_function=lambda *args:None,drawable=True): #lambda ~ do nothing function
        self.drawable=drawable
        self.elements=[]
        self.click_element_function=click_element_function
        print("Warning: PgWidget class will be deprecated in future versions")




import inspect




class TimeTrigger:
    def __init__(self,frequency,function=lambda *x:None,args=None):
        self.frequency=frequency
        self.function=function
        self.args=args


class GuiTimeHandler:
    def __init__(self,glc,geh,refresh_period=10):
        self.glc=glc
        self.geh=geh
        self.t=0
        self.time_triggers=[]
        self.refresh_period=refresh_period #10 ticks
       
    def tick(self):
        self.t=self.t+10
        
        print(self.t)
        #print(self.time_triggers)
        #print(self.refresh_period,"PERIOD")
        
        self.glc.refresh(self.glc.screen)
        if self.t%50==0:
            if hasattr(self.geh,"direction_list"):    
                for i in range(len(self.geh.direction_list)):
                    if self.geh.direction_list[i]==1:
                        self.glc.table1.move_selected(i+1) 
            
        if self.t%self.refresh_period==0:
            self.glc.refresh(self.glc.screen)
            print("REFRESH")
            print([(x.visible,x.pos) for x in self.glc.rects.elements])
            """
            for i,rect in enumerate(rects):
                rect.is_collided()  
            """
        if self.t%1000==0:
            print("TIME",self.t)
            
        for i,trigger in enumerate(self.time_triggers):
            if self.t%trigger.frequency==0:
                print("TRIGGER EXECUTED")
                if trigger.args is not None:
                    trigger.function(trigger.args)
                else:
                    trigger.function()
                    print("Trigger executed")
                
        engine.time.wait(10)
        
        
      




class GuiEventHandler:
    def __init__(self,glc):
        self.glc=glc
        self.direction_list=[0,0,0,0]
        self.actively_selected_draggable_component=None
    
        
    
    def handle_left_click(self):
        self.glc.text = ""  # on click remove all text
        pos = engine.mouse.get_pos()

        for i, widget_type in enumerate(self.glc.pgwidgets):
            widget_type.click_element_function(pos)

        # Dynamic drawing of button,combo click
        for i, widget_type in enumerate(self.glc.pgwidgets):
            for j, widget in enumerate(widget_type.elements):

                if widget.visible:
                    if type(widget) == ComboBox:
                        if widget._is_rolled and widget.pos[1] < pos[1] and pos[1] < widget.pos[1] + widget.size[1] * (
                                len(widget.values) + 1):
                            widget.choose(pos)
                        elif not widget._is_rolled and widget.is_point_in_rectangle(pos):
                            widget.choose(pos)
                        else:
                            pass

                    elif type(widget) == Button:
                        if widget.is_point_in_rectangle(pos):
                            self.glc.pgwidgets[i].elements[j].is_clicked = True

                    elif type(widget) == Table:
                        if widget.is_point_in_rectangle(pos):
                            self.actively_selected_draggable_component = widget

        for i,element in enumerate(self.glc.rects+self.glc.entries+self.glc.tables):
            if element.is_point_in_rectangle(pos):
                print(element,"CLICKED")
                #try:
                element.on_click(self.glc)
                #except:
                #    element.on_click()


    def handle_unclick(self):
        pos = engine.mouse.get_pos()
                    
                    
        #Dynamic drawing of button click
        for i,widget_type in enumerate(self.glc.pgwidgets):
            for j,widget in enumerate(widget_type.elements):
                if type(widget)==Button:
                    self.glc.pgwidgets[i].elements[j].is_clicked=False
        
        selected = None
        new_select_possible=True


    def handle_key_down(self,event):
        direction_list=[0,0,0,0]   
        if event.key == engine.K_RIGHT:  
            direction_list[0]=1
              
        elif event.key == engine.K_UP:
            direction_list[1]=1
            
        elif event.key == engine.K_LEFT:
            direction_list[2]=1
            
        elif event.key == engine.K_DOWN:
            direction_list[3]=1
          
            
        if event.key == engine.K_RETURN:
            try:
                self.glc.table1.move_selected(4)
            except AttributeError:
                pass
           
        try:
            text=self.glc.table1.table_cells[self.glc.table1.selected_cell_index].label.text 
        except AttributeError:
            text=""
        
        if event.key == engine.K_BACKSPACE:
            self.glc.erase_letter_from_text()
            self.glc._propagate_glc_text_to_entries()
            
            
        elif event.key == engine.K_DELETE:
            text = ""
        else:
            letter=event.unicode
            self.glc.append_letter_to_text(letter)
            
        #self.glc.text=text
        self.glc._propagate_glc_text_to_entries()
        try:
            self.glc.table1.table_cells[self.glc.table1.selected_cell_index].label.text=text
        except AttributeError:
            pass
        
        
        
   
    def handle_key_up(self,event):
        if event.key == engine.K_RIGHT:  
            self.direction_list[0]=0
              
        elif event.key == engine.K_UP:
            self.direction_list[1]=0
            
        elif event.key == engine.K_LEFT:
            self.direction_list[2]=0
            
        elif event.key == engine.K_DOWN:
            self.direction_list[3]=0
   
    



class GuiLayoutContext:
    def __init__(self):
        self.screen=initialize_pg()
        self.labels=[]
        self.entries=[]
        self.rects=[]
        self.pgwidgets=[]
        self.tables=[]
        self.table1=None
        self.selected_entry=None
        self.text=""



    def refresh(self,screen):
        
        #try:
        screen.fill(c.selected_background)
        #except AttributeError: #can't globally fill
        #    print("Screen fill - engine disable")
        
        pgw_widgets=[widget for widget_type in self.pgwidgets for widget in widget_type.elements] #fancy double list comprehension
        print(pgw_widgets)
        for i,shape in enumerate(pgw_widgets):
            if shape.visible:
                draw_arguments=list(inspect.signature(shape.draw).parameters.keys()) #analyzes if there's glc in the draw function args
                if "screen" in draw_arguments:
                    print("SHAPE",shape)
                    shape.draw(screen) #screen arg - most natural?
                else:
                    shape.draw()
                

        drawable_shapes=[]
        drawable_shapes+=self.rects
        drawable_shapes+=self.entries
        drawable_shapes+=self.labels
        drawable_shapes.sort(key=lambda shape:shape.visibility_layer)
        
        for i,shape in enumerate(drawable_shapes):
            if shape.visible:
                draw_arguments=list(inspect.signature(shape.draw).parameters.keys()) #analyzes if there's glc in the draw function args
                if "glc" in draw_arguments:
                    shape.draw(self) #glc arg
                elif "screen" in draw_arguments:
                    shape.draw(screen) #glc arg
                else:
                    shape.draw()
                
        for i,shape in enumerate(drawable_shapes):
            if hasattr(shape,"is_drawing_children"):
                if shape.is_drawing_children:
                    shape.draw_children(self)
                    
        

    def _propagate_glc_text_to_entries(self):
        #myfont = pygame.font.SysFont("Calibri", 20)

        try:
            print(self.selected_entry, self.selected_entry.pos)
        except:
            pass
        if self.selected_entry is not None:
            if len(self.selected_entry.labels) > 0 and self.selected_entry.selection_count > 0:
                self.selected_entry.text = self.text
                #self.selected_entry.labels[0].text = self.text
                
                #try:
                #    self.selected_entry.labels[0].lbl = myfont.render(self.text, 20, (0, 0, 0))
                #except pygame.error as e:
                #    print("Warning: Text has zero width:", e)  # do not remove (error with special chars)
    
    def append_letter_to_text(self,letter):
        if self.selected_entry is not None:
            split_index=self.selected_entry.labels[0].cursor_offset_index
            if split_index is not None:
                self.text = self.text[:split_index]+letter+self.text[split_index:]
            else:
                self.text += letter
                
            self._propagate_glc_text_to_entries() #must be here because otherwise it can't move cursor +1
            if split_index is not None:
                self.selected_entry.labels[0].cursor_offset_index+=1
            else:
                self.selected_entry.labels[0].cursor_offset_index=len(self.text)#1
            
        else:  
            self.text += letter
    
    def erase_letter_from_text(self):
        if self.selected_entry is not None:
            split_index=self.selected_entry.labels[0].cursor_offset_index
            if split_index is None:
                split_index=len(self.text)
            
            if split_index>0: #dont erase if on position 0
                self.text = self.text[:split_index-1]+self.text[split_index:]
                self.selected_entry.labels[0].cursor_offset_index=split_index-1
                
        else:
            self.text = self.text[:-1]









#import time
#time.sleep(10)
#if __name__ == "crypto_dashboard":


import threading

def remote_main_program_loop(glc,geh,gth):
    """GuiLayoutContext,GuiEventHandler,GuiTimeHandler"""
    done=False
    t=0
    new_select_possible=True
    selected=None
    
    
    class MyApp(engine.App):
        def __init__(self, *args):
            self.stop_flag=False
            self.time=0
            
            
            res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'png')
            super(MyApp, self).__init__(*args, static_file_path={'png': res_path})
        
            
        def display_time(self):
            print("display_time",self.time)
            self.lblTime.set_text('Play time: ' + str(self.time))
        
            self.time += 1
            engine.display.clear()
            gth.tick()
            
            #glc.refresh(engine.display.screen)
            
            if not self.stop_flag:
                threading.Timer(1, self.display_time).start() #must be last row
            
            
            
            
        def main(self):
            
            self.lblTime = engine.gui.Label('Time')
            #self.lblTime.set_size(100, 30)
            self.lblTime.set_text('Play time: ' + str(self.time))
            
            engine.display.screen.onmousedown.connect(self.onmousedown) #,x,y
            #engine.display.screen.onmouseover.connect(self.onmouseover) #,x,y
            glc.refresh(engine.display.screen)
            
            self.display_time()
        
            engine.display.screen.append(self.lblTime)
            return engine.display.screen
        
        
        def onmousedown(self, emitter, x, y):
            print("the mouse position is: ", x, y)
            
            class Event:
                def __init__(self,x,y):
                    self.pos=[int(float(x)),int(float(y))]
                    
            event=Event(x,y)
            geh.handle_left_click() 
            
            geh.handle_left_click_not_refactored(event) 
                               
                        
            #engine.draw.rect(engine.display.screen,(100,200,100),[x,y,20,20])
            
            
        def onmouseover(self):
            print("MOUSE")
            
        def on_close(self):
            self.stop_flag = True
            super(MyApp, self).on_close()
    
    
    #server=
    engine.start(MyApp, multiple_instance=True, address='0.0.0.0', port=0, debug=True, start_browser=True)

    
    """        
    while not done:
        try:
            for event in engine.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1: #Left button of mouse
                    geh.handle_left_click()                                
                                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button==3: #Right button of mouse
                    geh.handle_right_click(event)
                             
                elif event.type == pygame.MOUSEBUTTONUP:
                    geh.handle_unclick()
                                    
                elif event.type == pygame.MOUSEMOTION:                
                    for i,table in enumerate(glc.tables):
                        if geh.actively_selected_draggable_component==table:
                            geh.drag_table(table,event)
                    
                    for i,rect in enumerate(glc.rects+glc.entries):
                        if geh.actively_selected_draggable_component==rect:
                            geh.drag_rect(rect,event)
                            
                elif event.type == pygame.KEYDOWN:
                    geh.handle_key_down(event)
                    
                    
                elif event.type == pygame.KEYUP: 
                    geh.handle_key_up(event)
            
                elif event.type == pygame.QUIT:
                    done = True
            
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                    
                
                
            try: #Handling tkinter and pygame loops
                root.update()
            except tk.TclError as e:
                sys.exit(0)
                print(e)
            
                
            engine.display.flip()   
    
        except KeyboardInterrupt:
            pygame.display.quit()
            pygame.quit()
            sys.exit(0)
    
        gth.tick()
      
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
    """




def main_program_loop(glc,geh,gth):
    """GuiLayoutContext,GuiEventHandler,GuiTimeHandler"""
    done=False
    t=0
    new_select_possible=True
    selected=None
    
    
               
    while not done:
        try:
            for event in engine.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1: #Left button of mouse
                    geh.handle_left_click()                                
                                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button==3: #Right button of mouse
                    geh.handle_right_click(event)
                             
                elif event.type == pygame.MOUSEBUTTONUP:
                    geh.handle_unclick()
                                    
                elif event.type == pygame.MOUSEMOTION:                
                    for i,table in enumerate(glc.tables):
                        if geh.actively_selected_draggable_component==table:
                            geh.drag_table(table,event)
                    
                    for i,rect in enumerate(glc.rects+glc.entries):
                        if geh.actively_selected_draggable_component==rect:
                            geh.drag_rect(rect,event)
                            
                elif event.type == pygame.KEYDOWN:
                    geh.handle_key_down(event)
                    
                    
                elif event.type == pygame.KEYUP: 
                    geh.handle_key_up(event)
            
                elif event.type == pygame.QUIT:
                    done = True
            
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                    
                
                
            try: #Handling tkinter and pygame loops
                root.update()
            except tk.TclError as e:
                sys.exit(0)
                print(e)
            
                
            engine.display.flip()   
    
        except KeyboardInterrupt:
            pygame.display.quit()
            pygame.quit()
            sys.exit(0)
    
        gth.tick()
      
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)

#main_program_loop(glc,geh)