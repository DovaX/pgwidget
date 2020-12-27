
import pygame
import sys

import os



import pandas as pd


"""TKINTER PART"""
"""
import tkinter as tk

from tkinter import LEFT

root = tk.Tk()


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


bg_color=(150,150,150) #tuple

screen = pygame.display.set_mode([1366,768])
        
pygame.init()
pygame.display.set_caption("Drag and drop")
#clock=pygame.time.Clock()
screen.fill(bg_color)
window_icon = pygame.image.load('icon.png')
pygame.display.set_icon(window_icon)

color=(100,100,100)


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

def open_xlsx_file(): 
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

root.update()

"""
"""TKINTER END PART"""


class Label:
    def __init__(self,pos,text,color,font="Cambria",fontsize=20,max_text_length=None):
        self.pos=pos
        self.text=text
        self.color=color
        self.font=font
        self.fontsize=fontsize
        self.myfont = pygame.font.SysFont(self.font, self.fontsize)
        self.max_text_length=max_text_length
        self.selected=False
        
    def draw(self):
       
        #print("Pixels",self.myfont.size(self.text))
        self.shown_text=self.text
        
        if self.max_text_length is not None:
            #print("HEUREKA",self.max_text_length)
            #print(self.shown_text)
            self.text_length=self.myfont.size(self.shown_text)[0]
            #print("text_length",self.text_length,self.myfont.size(self.shown_text))
            while self.text_length>self.max_text_length:
                #print(self.text_length)
                if self.selected:
                    self.shown_text=self.shown_text[1:]
                else:
                    self.shown_text=self.shown_text[:-1]
                
                self.text_length=self.myfont.size(self.shown_text)[0]
            
        
        try:
            lbl = self.myfont.render(self.shown_text, 1, self.color)
        except pygame.error as e:
            lbl = self.myfont.render("", 1, self.color)
        screen.blit(lbl, (self.pos[0], self.pos[1]))
           
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
        self.x=pos[0]
        self.y=pos[1]
        self.dx=size[0]
        self.dy=size[1]
        self.color=color
        self.draggable=draggable
        self.selected=False
        
    def draw(self): 
        pygame.draw.rect(screen,self.color,[self.x,self.y,self.dx,self.dy])    
    
    def is_point_in_rectangle(self,pos):
        if self.x<pos[0] and pos[0]<self.x+self.dx and self.y<pos[1] and pos[1]<self.y+self.dy:
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
    def __init__(self,pos,size,color,coor=[0,0]):
        super().__init__(pos,size,color,draggable=False)
        self.coor=coor
        self.label=Label([pos[0]+2,pos[1]+4],"",(0,0,0),font="Calibri",fontsize=15,max_text_length=size[0]-1)
                
    def draw(self):
        if not self.selected:
            super().draw()
        else:
            pygame.draw.rect(screen,self.color,[self.x,self.y,self.dx,self.dy])              
        self.label.draw()              

class Table:
    def __init__(self,pos,cell_size,rows,cols,margin=1):
        self.pos=pos
        self.cell_size=cell_size
        self.rows=rows
        self.cols=cols
        self.margin=margin
        self.table_size=[(self.cell_size[0]+self.margin)*self.cols,(self.cell_size[1]+self.margin)*self.rows]
        self.frame_cell=Cell(self.pos,self.table_size,(212,212,212))
        self.table_cells=[]
        self.initialize_cells()
        self.selected_cell_index=None
        self.df=None
        
    def initialize_cells(self):
        for i in range(self.rows):
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
            pygame.draw.rect(screen,(33,115,70),[cell.x-2,cell.y-2,cell.dx+3,cell.dy+3],2) 
            pygame.draw.rect(screen,(255,255,255),[cell.x+cell.dx-3,cell.y+cell.dy-3,6,6],2) 
            pygame.draw.rect(screen,(33,115,70),[cell.x+cell.dx-2,cell.y+cell.dy-2,5,5]) 
            
            
    def is_clicked(self,pos):
        print("bla")
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
                
                
    def update_data(self,df):
        """data layer"""  
        self.df=df
        
        list1=df.values.tolist()
        for i in range(len(list1)):
            for j in range(len(list1[i])):
                cell_index=self.find_cell_index(i,j)
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

"""
def save_df(table1):
    table1.df.to_excel("name.xlsx")
"""    

class RadioButton(DraggableRect):
    def __init__(self,pos,text,radio_group,selected=False):
        self.size=[20,20]
        super().__init__(pos,self.size,(0,0,0),draggable=False)
        self.pos=pos
        self.text=text
        self.radio_group=radio_group
        self.selected=selected
        self.img_empty=pygame.image.load("radio_empty.png")
        self.img_full=pygame.image.load("radio_full.png")
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
        self.img_empty=pygame.image.load("checkbox_empty.png")
        self.img_full=pygame.image.load("checkbox_full.png")
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
        self.label=Label([pos[0]+2,pos[1]+4],self.text,(0,0,0),font="Calibri",fontsize=15,max_text_length=size[0]-1)
        self.border_color=border_color
        self.color=color
        
    def draw(self):
        super().draw()
        pygame.draw.rect(screen,self.border_color,[self.x,self.y,self.dx,self.dy],1)  
        self.label.draw()  
        
    


class Button(DraggableRect):
    def __init__(self,pos,size,text,function=lambda *args:None,border_color=(0,0,0),color=(200,200,200)):
        super().__init__(pos,size,color,draggable=False)
        self.pos=pos
        self.size=size
        self.border_color=border_color
        self.color=color
        self.text=text
        self.label=Label([pos[0]+2,pos[1]+4],self.text,(0,0,0),font="Calibri",fontsize=15,max_text_length=size[0]-1)
        self.function=function
        
        
    def draw(self):
        super().draw()
        pygame.draw.rect(screen,self.border_color,[self.x,self.y,self.dx,self.dy],1)  
        self.label.draw() 
    
    def run_function(self):
        self.function()


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
                        
                                
                elif event.type == pygame.MOUSEBUTTONUP:
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