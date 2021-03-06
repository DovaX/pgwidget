
import pygame
import sys

import os



import pandas as pd


"""TKINTER PART"""

#import tkinter as tk

#from tkinter import LEFT



"""
root = tk.Tk()
root.withdraw()


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


def initialize_pg():
    global bg_color
    global color
    
    bg_color=(150,150,150) #tuple
    
    screen = pygame.display.set_mode([1366,768])
            
    pygame.init()
    pygame.display.set_caption("Forloop")
    #clock=pygame.time.Clock()
    screen.fill(bg_color)
    try:
        window_icon = pygame.image.load('png//start.png')
        pygame.display.set_icon(window_icon)
    except FileNotFoundError:
        print("Warning: Icon (icon.png) not found, skipped")
        pass
    color=(200,200,200)
    return(screen)


screen=initialize_pg()

"""TKINTER PART"""


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
"""

"""TKINTER END PART"""


class Label:
    def __init__(self,text,color,pos=[0,0],relative_pos=[0,0],font_type="Cambria",font_size=20,max_text_length=None,visible=True):
        self.text=text
        self.color=color
        self.pos=pos
        self.max_text_length=max_text_length
        self.font_type=font_type
        self.font_size=font_size
        self.relative_pos=relative_pos
        self.myfont = pygame.font.SysFont(self.font_type, self.font_size)
        self.lbl=self.myfont.render(self.text, True, self.color)
        self.selected=False #dbtable -> shows just beginning of string
        self.visible=visible
        self.visibility_layer=100
        
    def draw(self):       
        self.shown_text=self.text    
        if self.max_text_length is not None:
            #print(self.max_text_length,self.shown_text)
        
            self.text_length=self.myfont.size(self.shown_text)[0]
            while self.text_length>self.max_text_length:
                if self.selected:
                    self.shown_text=self.shown_text[1:]
                else:
                    self.shown_text=self.shown_text[:-1]              
                self.text_length=self.myfont.size(self.shown_text)[0]
        if self.visible:
            try:
                self.lbl=self.myfont.render(self.shown_text, True, self.color)
            except pygame.error as e:
                self.lbl = self.myfont.render("", True, self.color)
            screen.blit(self.lbl, (self.pos[0], self.pos[1]))
            

            
    def get_pixel_length(self):
        text_pixels=self.myfont.size(self.text)[0]
        return(text_pixels)
        
           
def refresh(pgwidgets):
    screen.fill(bg_color)
    """
    for i,rect in enumerate(rects):
        rect.draw()
    """
        
    for j,widget_type in enumerate(pgwidgets):
        for i,widget in enumerate(widget_type.elements):
            widget.draw()
            

class DraggableRect:
    def __init__(self,pos,size,color,draggable=True):
        self.pos=pos
        self.size=size
        self.color=color
        self.draggable=draggable
        self.selected=False
        self.visible=True
        self.visibility_layer=100
        self.is_drawing_children=True
        
    def draw(self): 
        pygame.draw.rect(screen,self.color,[self.pos[0],self.pos[1],self.size[0],self.size[1]])    
    
    def draw_children(self):
        #can be overrided
        pass
    
    
    def is_point_in_rectangle(self,pos):
        if self.pos[0]<pos[0] and pos[0]<self.pos[0]+self.size[0] and self.pos[1]<pos[1] and pos[1]<self.pos[1]+self.size[1]:
            return(True)
        else:
            return(False)
    
    def is_collided(self,rects):
        collision=False
        for i in range(len(rects)):
            if rects[i]!=self:
                if self.is_point_in_rectangle([rects[i].x,rects[i].y]):
                    collision=True
                    index=i
                if self.is_point_in_rectangle([rects[i].x+rects[i].dx,rects[i].y]):
                    collision=True
                    index=i
                if self.is_point_in_rectangle([rects[i].x,rects[i].y+rects[i].dy]):
                    collision=True
                    index=i
                if self.is_point_in_rectangle([rects[i].x+rects[i].dx,rects[i].y+rects[i].dy]):
                    collision=True
                    index=i
        if collision:
            self.collision_function(rects[index])

    def collision_function(self,collided_rect):
        pass        
 
 
class Cell(DraggableRect):
    def __init__(self,pos,size,color,coor=[0,0],relative_pos=[0,0]):
        super().__init__(pos,size,color,draggable=False)
        self.coor=coor
        self.label=Label("",(0,0,0),[pos[0]+2,pos[1]+4],font_type="Calibri",font_size=15,max_text_length=size[0]-1)
                
    def draw(self):
        if not self.selected:
            super().draw()
        else:
            pygame.draw.rect(screen,self.color,[self.pos[0],self.pos[1],self.size[0],self.size[1]])              
        self.label.draw()              

class Table:
    def __init__(self,pos,cell_size,rows,cols,margin=1,include_header=True,frame_cell_color=(212,212,212),header_color=(230,230,230),frame_border_width=3):
        
        self.include_header=include_header
        self.pos=pos
        self.cell_size=cell_size
        self.rows=rows
        self.cols=cols
        self.margin=margin
        self.frame_cell_color=frame_cell_color
        self.header_color=header_color
        
        self.table_size=[(self.cell_size[0]+self.margin)*self.cols,(self.cell_size[1]+self.margin)*(self.rows+1)]
        self.frame_cell=Cell(self.pos,self.table_size,self.frame_cell_color)
        self.table_cells=[]
        self.initialize_cells()
        self.selected_cell_index=None
        self.df=None
        self.visibility_layer=100
        self.frame_border_width=frame_border_width
        
    def initialize_cells(self):
        for j in range(self.cols):
            i=0
            new_pos=[self.pos[0]+j*self.cell_size[0]+j*self.margin,self.pos[1]+i*self.cell_size[1]+i*self.margin]
            self.table_cells.append(Cell(new_pos,self.cell_size,self.header_color,coor=[i,j]))
        
        
        for i in range(1,self.rows+1):
            for j in range(self.cols):
                new_pos=[self.pos[0]+j*self.cell_size[0]+j*self.margin,self.pos[1]+i*self.cell_size[1]+i*self.margin]
                self.table_cells.append(Cell(new_pos,self.cell_size,(255,255,255),coor=[i,j]))
                
    def draw(self):
        self.frame_cell.draw()
        
        for i,cell in enumerate(self.table_cells):
            cell.draw()
            
        #selected cell
        if self.selected_cell_index is not None:
            cell=self.table_cells[self.selected_cell_index]
            pygame.draw.rect(screen,(33,115,70),[cell.pos[0]-2,cell.pos[1]-2,cell.size[0]+3,cell.size[1]+3],2) 
            pygame.draw.rect(screen,(255,255,255),[cell.pos[0]+cell.size[0]-3,cell.pos[1]+cell.size[1]-3,6,6],2) 
            pygame.draw.rect(screen,(33,115,70),[cell.pos[0]+cell.size[0]-2,cell.pos[1]+cell.size[1]-2,5,5]) 
        
        pygame.draw.rect(screen,(0,0,0),[self.pos[0]-1,self.pos[1]-1]+self.table_size,self.frame_border_width)
        
          
    def draw_children(self):
        pass
        
       
    def is_point_in_rectangle(self,pos):
        if self.pos[0]<pos[0] and pos[0]<self.pos[0]+self.table_size[0] and self.pos[1]<pos[1] and pos[1]<self.pos[1]+self.table_size[1]:
            return(True)
        else:
            return(False)  
        
    def which_cell_is_clicked(self,pos):
        max_coor=[x+y+z for x,y,z in zip(self.pos,self.table_size,[self.cols,self.rows])]
        print(max_coor)
        print(self.table_size)
        new_j=(pos[0]-self.pos[0])//(self.cell_size[0]+self.margin)
        new_i=(pos[1]-self.pos[1])//(self.cell_size[1]+self.margin)
        print("ROW",new_i,"COL",new_j)
        return(new_i,new_j)
        
    def find_cell_index(self,row,col):
        for cell_index,cell in enumerate(self.table_cells):
            if str(cell.coor)==str([row,col]):
                return(cell_index)
            
    def deselect_all_cells(self):
        for index,cell in enumerate(self.table_cells):
            self.table_cells[index].selected=False #redundant at the moment
            self.table_cells[index].label.selected=False
    
    def select_cell(self,selected_cell_index):
        self.selected_cell_index=selected_cell_index
        if self.selected_cell_index is not None:
            self.table_cells[self.selected_cell_index].selected=True #redundant at the moment
            self.table_cells[self.selected_cell_index].label.selected=True
    
    def highlight_selected(self,pos):
        i,j=self.which_cell_is_clicked(pos)
        selected_cell_index=self.find_cell_index(i,j)
        self.deselect_all_cells()
        self.select_cell(selected_cell_index)
        
    def move_selected(self,direction):
        if self.selected_cell_index is not None:
            i,j=self.table_cells[self.selected_cell_index].coor
            print(i,j)
            if direction==1:
                target_cell_index=self.find_cell_index(i,j+1) #right
            if direction==2:
                target_cell_index=self.find_cell_index(i-1,j) #up
            if direction==3:
                target_cell_index=self.find_cell_index(i,j-1) #left
            if direction==4:
                target_cell_index=self.find_cell_index(i+1,j) #down
            if target_cell_index is not None:
                self.deselect_all_cells()
                self.select_cell(target_cell_index)
            else:
                self.move_camera(direction)
    
    def move_camera(self,direction):
        pass
                
                
    def update_data(self,df, rows = None):
        """data layer"""  
        self.df=df
        self.table_cells=[]
        self.initialize_cells()
        if rows is None:
            rows = df.shape[0]
        print("updatedata",self.df)
        
        list1=df.values.tolist()
        
        column_names=df.columns
        i=0
        for j in range(len(column_names)):
            cell_index=self.find_cell_index(0,j)
            if cell_index is not None:
                self.table_cells[cell_index].label.text=str(column_names[j])     
        for i in range(min(len(list1), rows)):
            for j in range(len(list1[i])):
                cell_index=self.find_cell_index(i+1,j) #skipping header -> +1
                if cell_index is not None:
                    self.table_cells[cell_index].label.text=str(list1[i][j])           

class ButtonImage(DraggableRect):
    def __init__(self,pos,size,img,text="",function=lambda *args:None): #default: do nothing function
        super().__init__(pos,size,(0,0,0),draggable=False)    
        self.pos=pos
        self.size=size
        self.img=img
        self.rescale()
        self.function=function
    
    def rescale(self):
        self.img=pygame.transform.smoothscale(self.img, (self.size[0], self.size[1]))
                
    def draw(self):   
        screen.blit(self.img,self.pos)
        
    def run_function(self):
        self.function()


def save_df(table1):
    table1.df.to_excel("name.xlsx")
  

class RadioButton(DraggableRect):
    def __init__(self,pos,text,radio_group,selected=False):
        self.size=[20,20]
        super().__init__(pos,self.size,(0,0,0),draggable=False)
        self.pos=pos
        self.text=text
        self.radio_group=radio_group
        self.selected=selected
                
        try:
            self.img_empty = pygame.image.load('radio_empty.png')
        except:
            self.img_empty = pygame.image.load('img//radio_empty.png')
            
        try:
            self.img_full = pygame.image.load('radio_full.png')
        except:
            self.img_full = pygame.image.load('img//radio_full.png')
            
        #self.img_empty=pygame.image.load("radio_empty.png")
        #self.img_full=pygame.image.load("radio_full.png")
        self.rescale()

    def rescale(self):
        self.img_empty=pygame.transform.smoothscale(self.img_empty, (self.size[0], self.size[1]))
        self.img_full=pygame.transform.smoothscale(self.img_full, (self.size[0], self.size[1]))
           
        
    
    def draw(self):
        if self.selected:
            screen.blit(self.img_full,self.pos)
        else:
            screen.blit(self.img_empty,self.pos)

class Checkbox(DraggableRect):
    def __init__(self,pos,text,selected=False):
        self.size=[20,20]
        super().__init__(pos,self.size,(0,0,0),draggable=False)
        self.pos=pos
        self.text=text
        self.selected=selected
        try:
            self.img_empty = pygame.image.load('checkbox_empty.png')
        except:
            self.img_empty = pygame.image.load('img//checkbox_empty.png')
            
        try:
            self.img_full = pygame.image.load('checkbox_full.png')
        except:
            self.img_full = pygame.image.load('img//checkbox_full.png')
            
        self.rescale()

    def rescale(self):
        self.img_empty=pygame.transform.smoothscale(self.img_empty, (self.size[0], self.size[1]))
        self.img_full=pygame.transform.smoothscale(self.img_full, (self.size[0], self.size[1]))
             
    def draw(self):
        if self.selected:
            screen.blit(self.img_full,self.pos)
        else:
            screen.blit(self.img_empty,self.pos)

class TextArea(DraggableRect):
    def __init__(self,pos,size,text,border_color=(0,0,0),color=(255,255,255)):
        super().__init__(pos,size,color,draggable=False)
        self.pos=pos
        self.size=size
        self.text=text
        self.label=Label(self.text,(0,0,0),[pos[0]+2,pos[1]+4],font_type="Calibri",font_size=15,max_text_length=size[0]-1)
        self.border_color=border_color
        self.color=color
        self.fit2label()

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
        
    def draw(self):
        super().draw()
        pygame.draw.rect(screen,self.border_color,[self.pos[0],self.pos[1],self.size[0],self.size[1]],1)
        self.label.draw = self.blit_text
        self.label.draw(screen, self.label.text)

    def fit2label(self):
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


class Button(DraggableRect):
    def __init__(self,pos,size,text,function=lambda *args:None,function_args=None,border_color=(0,0,0),color=(200,200,200),relative_pos=[0,0],visible=True,hover_color=(120,120,120),hover_label_color=(0,0,0)):
        super().__init__(pos,size,color,draggable=False)
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
        
        
        
    def draw(self):
        if self.visible:
            if self.is_clicked:
                pygame.draw.rect(screen,(180,180,180),[self.pos[0],self.pos[1],self.size[0],self.size[1]]) 
            else:
                super().draw()
            pygame.draw.rect(screen,self.border_color,[self.pos[0],self.pos[1],self.size[0],self.size[1]],1)  
            self.label.draw()
            
            pos=pygame.mouse.get_pos()
            self.on_hover(pos)
    
    def on_hover(self,pos):
        if self.is_point_in_rectangle(pos):
            pygame.draw.rect(screen,self.hover_color,[self.pos[0],self.pos[1],self.size[0],self.size[1]])  
            self.label.draw() 
            
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
        super().__init__(pos, size, color, draggable=False)
        self.values = values
        #self.text = text
        self.border_color = border_color
        self._cells = []
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
            self.cell = Cell(self.pos, self.size, self.color, coor=[0, 0],relative_pos=[0,0])
            self.cell.label.text = text
            #self.cell.label.pos[0]=self.cell.label.pos[0]+4#2 pixels from border
            #self.cell.label.pos[1]=self.cell.label.pos[1]+3
            #self.cell.label.relative_pos[0]=self.cell.label.relative_pos[0]+2#2 pixels from border
            #self.cell.label.relative_pos[1]=self.cell.label.relative_pos[1]+2
        #TODO elif - create empty Cell

    def draw(self):
        if self.visible:
            self._update_cells_positions()
            if hasattr(self, "cell"):
                pygame.draw.rect(screen,self.color,self.cell.pos+self.cell.size)    
                self.cell.draw()
                pygame.draw.rect(screen,(0,0,0),self.cell.pos+self.cell.size,1)
                pygame.draw.line(screen,(0,0,0),[self.pos[0]+self.size[0]-15,self.pos[1]+self.size[1]/2-2],[self.pos[0]+self.size[0]-10,self.pos[1]+self.size[1]/2+3],3)
                pygame.draw.line(screen,(0,0,0),[self.pos[0]+self.size[0]-10,self.pos[1]+self.size[1]/2+3],[self.pos[0]+self.size[0]-5,self.pos[1]+self.size[1]/2-2],3)
                #pygame.draw.line(screen,(0,0,0),[self.pos[0]+self.size[0]-18,self.pos[1]],[self.pos[0]+self.size[0]-18,self.pos[1]+self.size[1]],1)
                
            if self._is_rolled:
                pos=pygame.mouse.get_pos()
                for cell, value in zip(self._cells, self.values):
                    cell.label.text = value
                    cell.draw()
                self.on_hover(pos)
                
                self._draw_multiselect_crosses()
     
        
            
    def on_hover(self,pos):
        if self.pos[0]<pos[0] and pos[0]<self.pos[0]+self.size[0] and self.pos[1] < pos[1] and pos[1] < self.pos[1] + self.size[1] * (len(self.values) + 1): #hovering
            #super().draw(auto_draw_labels=False)
            y=pos[1]-self.pos[1]
            option_height=self.size[1]
            index=y//option_height #0 - selected item
            print("HOVERING",y,index)   
            if index!=0: #not hover over selected item
                pygame.draw.rect(screen,self.hover_color,[self.pos[0],self.pos[1]+index*option_height,self.size[0],option_height])    
                self._cells[index-1].label.color=self.hover_label_color
                self._cells[index-1].label.draw()
                self._cells[index-1].label.color=(0,0,0)
                
    def _draw_multiselect_crosses(self):
        if self.multiselect_indices is not None:
            for multiselect_index,value in self.multiselect_indices.items(): 
                if value!=self.multiselect_values[-1]: #i.e. value!=False
                    pygame.draw.line(screen,(0,0,0),[self.pos[0]+self.size[0]-15,self.pos[1]+self.size[1]*(1/4+multiselect_index)],[self.pos[0]+self.size[0]-5,self.pos[1]+self.size[1]*(1/4+multiselect_index)+10],3)
                    pygame.draw.line(screen,(0,0,0),[self.pos[0]+self.size[0]-5,self.pos[1]+self.size[1]*(1/4+multiselect_index)],[self.pos[0]+self.size[0]-15,self.pos[1]+self.size[1]*(1/4+multiselect_index)+10],3)
                    #pygame.draw.line(screen,(0,0,0),[self.pos[0]+self.size[0]-18,self.pos[1]],[self.pos[0]+self.size[0]-18,self.pos[1]+self.size[1]],1)
                    

    
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
        pos=pygame.mouse.get_pos()        
        if self._is_rolled and self.pos[1] < pos[1] and pos[1] < self.pos[1] + self.size[1] * (len(self.values) + 1):
            self.choose(pos)
            
        elif not self._is_rolled and self.is_point_in_rectangle(pos):
            self.roll()
            
        
        #self.choose(pos)

    def roll(self):
        if not self._is_rolled: 
            self._cells = self._get_option_cells()
            self._dy = self.size[1] * (len(self.values) + 1)        
        else:
            self.run_function()
        self._is_rolled = not self._is_rolled
    
    def run_function(self):
        self.function(self.function_args)
    
    
    def choose(self, pos):
        index = abs((pos[1] - self.pos[1]) // self.size[1])
        if self.multiselect_indices is None:
            if index == 0:
                self.roll()
            else:
                self.cell.label.text = self.values[index - 1]
                
                self.roll()
        else:
            if index == 0:
                self.roll()
            elif index in list(self.multiselect_indices.keys()):
                next_multiselect_value=self._get_next_multiselect_value(self.multiselect_indices[index])
                self.multiselect_indices[index]=next_multiselect_value
            elif index<=len(self.values):
                self.multiselect_indices[index]=self.multiselect_values[0]

    def _get_next_multiselect_value(self,value):
        index=self.multiselect_values.index(value)
        if index+1>=len(self.multiselect_values):
            final_index=0
        else:
            final_index=index+1
        return(self.multiselect_values[final_index])

    def _get_option_cells(self):
        tmp = []
        for i in range(len(self.values)):
            tmp.append(Cell([self.pos[0], self.pos[1] + self.size[1] * (i + 1)], self.size, self.color, coor=[0, i + 1]))
        return (tmp)

    def _update_cells_positions(self):
        self.cell.pos=[self.pos[0], self.pos[1]]
        self.cell.label.pos=[self.pos[0], self.pos[1]]
        
        for i in range(len(self._cells)):
            self._cells[i].pos=[self.pos[0], self.pos[1] + self.size[1] * (i + 1)]
            self._cells[i].label.pos=[self.pos[0], self.pos[1] + self.size[1] * (i + 1)]


class PgWidget:
    def __init__(self,click_element_function=lambda *args:None,drawable=True): #lambda ~ do nothing function
        self.drawable=drawable
        self.elements=[]
        self.click_element_function=click_element_function
    






def main_program_loop(pgwidgets,table1):
    done=False
    t=0
    new_select_possible=True
    direction_list=[0,0,0,0]
    selected=None

    while not done:
        try:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if new_select_possible: #Because of popping from the list
                        pos = pygame.mouse.get_pos()
                        
                        
                        """
                        for i,rect in enumerate(rects):
                            if pos[0]>rect.x and pos[0]<rect.x+rect.dx and pos[1]>rect.y and pos[1]<rect.y+rect.dy:
                                selected=i
                                offset_x = rect.x - event.pos[0]
                                offset_y = rect.y - event.pos[1]
                        """
                        for i,widget_type in enumerate(pgwidgets):
                            widget_type.click_element_function(pos)
                            
                        #Dynamic drawing of button,combo click
                        for i,widget_type in enumerate(pgwidgets):
                            for j,widget in enumerate(widget_type.elements):
                                if type(widget)==Button:
                                    if widget.is_point_in_rectangle(pos):
                                        pgwidgets[i].elements[j].is_clicked=True
                                        
                                if type(widget)==ComboBox:
                                    widget.on_click()
                                    
                            
                        
                                
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    
                    
                    #Dynamic drawing of button click
                    for i,widget_type in enumerate(pgwidgets):
                        for j,widget in enumerate(widget_type.elements):
                            if type(widget)==Button:
                                pgwidgets[i].elements[j].is_clicked=False
                        
                        
                    
                    
                    selected = None
                    new_select_possible=True
                elif event.type == pygame.MOUSEMOTION:
                    """
                    for i,rect in enumerate(rects):
                        if selected==i and rect.draggable:
                            rect.x = event.pos[0] + offset_x
                            rect.y = event.pos[1] + offset_y
                    """
                    
                    
                
                elif event.type == pygame.KEYDOWN:
                    #if active:
                    
                    direction_list=[0,0,0,0]   
                    if event.key == pygame.K_RIGHT:  
                        direction_list[0]=1
                          
                    elif event.key == pygame.K_UP:
                        direction_list[1]=1
                        
                    elif event.key == pygame.K_LEFT:
                        direction_list[2]=1
                        
                    elif event.key == pygame.K_DOWN:
                        direction_list[3]=1
                      
                        
                    if event.key == pygame.K_RETURN:
                        table1.move_selected(4)
                       
                    
                    text=table1.table_cells[table1.selected_cell_index].label.text 
                    
                    
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        
                        
                    elif event.key == pygame.K_DELETE:
                        text = ""
                    else:
                        text += event.unicode
                    table1.table_cells[table1.selected_cell_index].label.text=text
                    text=""
                    
                
                elif event.type == pygame.KEYUP: 
                    if event.key == pygame.K_RIGHT:  
                        direction_list[0]=0
                          
                    elif event.key == pygame.K_UP:
                        direction_list[1]=0
                        
                    elif event.key == pygame.K_LEFT:
                        direction_list[2]=0
                        
                    elif event.key == pygame.K_DOWN:
                        direction_list[3]=0
                        
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                
            """    
            try: #Handling tkinter and pygame loops
                root.update()
            except tk.TclError as e:
                sys.exit(0)
                print(e)
            """
                
            pygame.display.flip()   
    
        except KeyboardInterrupt:
            pygame.display.quit()
            pygame.quit()
            sys.exit(0)
    
        t=t+10
        if t%1000==0:
            pass
        
        if t%5000==0:
            pass
        
        
        if t%50==0:
            for i in range(len(direction_list)):
                if direction_list[i]==1:
                    table1.move_selected(i+1) 
        
        if t%10==0:
            refresh(pgwidgets)
            """
            for i,rect in enumerate(rects):
                rect.is_collided()  
            """
        if t%1000==0:
            print(t)
        pygame.time.wait(10)
        
      
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)


#main_program_loop()