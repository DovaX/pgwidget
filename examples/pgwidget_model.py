import pgwidget.pgwidget_core as pgw
import pygame


def click_checkbox(pos):
    for i,checkbox in enumerate(checkboxes.elements):
        if checkbox.is_point_in_rectangle(pos):
            checkboxes.elements[i].selected=not checkboxes.elements[i].selected     

def click_radiobutton(pos):
    for i,radiobutton in enumerate(radiobuttons.elements):
        if radiobutton.is_point_in_rectangle(pos):
            for j,radiobutton2 in enumerate(radiobuttons.elements):
                if radiobutton2.radio_group==radiobutton.radio_group:        
                    radiobuttons.elements[j].selected=False                                     
            radiobuttons.elements[i].selected=True
            
def click_buttonimage(pos):
    for i,buttonimage in enumerate(buttonimages.elements):
        if buttonimage.is_point_in_rectangle(pos):
            buttonimage.run_function()
            
def click_button(pos):
    for i,button in enumerate(buttons.elements):
        if button.is_point_in_rectangle(pos):
            button.run_function()
        
def click_table(pos):    
    for i,table in enumerate(tables.elements):
        print("table")
        table.is_clicked(pos)
        table.which_cell_is_clicked(pos)
        table.highlight_selected(pos)

def click_combobox(pos):
    for i, combobox in enumerate(comboboxes.elements):
        if combobox.is_point_in_rectangle(pos):
            combobox.roll()
                            
        
        
#img1=pygame.image.load("click.png")

#buttonimages=[]
buttonimages=pgw.PgWidget(click_button)


"""
buttonimage1=ButtonImage([100,100],[50,50],img1,function=open_xlsx_file)
buttonimages.elements.append(buttonimage1)

buttonimage1=ButtonImage([100,160],[50,50],img1,function=save_df)
buttonimages.elements.append(buttonimage1)

buttonimage1=ButtonImage([100,220],[50,50],img1,function=file_save)
buttonimages.elements.append(buttonimage1)

buttonimage1=ButtonImage([100,280],[50,50],img1,function=run_script_from_file)
buttonimages.elements.append(buttonimage1)
"""



buttons=pgw.PgWidget()
button1=pgw.Button([800,100],[80,20],"Submit")
buttons.elements.append(button1)

textareas=pgw.PgWidget()
textarea1=pgw.TextArea([500,50],[200,120],"ahoj")
textareas.elements.append(textarea1)


radiobuttons=pgw.PgWidget(click_radiobutton)
radio1=pgw.RadioButton([50,60],"radio1",1)
radiobuttons.elements.append(radio1)
radio1=pgw.RadioButton([100,50],"radio2",1)
radiobuttons.elements.append(radio1)
radio1=pgw.RadioButton([150,40],"radio3",1)
radiobuttons.elements.append(radio1)

table1=pgw.Table([200,200],[63,19],25,17)
tables=pgw.PgWidget(click_table)
tables.elements.append(table1)

checkboxes=pgw.PgWidget(click_checkbox)
checkbox1=pgw.Checkbox([1000,100],"blabla")
checkboxes.elements.append(checkbox1)

comboboxes = pgw.PgWidget(click_combobox)
combobox = pgw.ComboBox([10, 150], [63, 19], ['klingons', 'humans', 'vulcans'])
comboboxes.elements.append(combobox)

rects=[]#[DraggableRect([50,50],[30,30],(200,200,200)),DraggableRect([150,100],[30,30],(200,200,200))]

pgwidgets=[buttonimages,textareas,radiobuttons,tables,buttons,checkboxes, comboboxes]


""" END OF CUSTOM PART """

pgw.main_program_loop(pgwidgets,table1)
