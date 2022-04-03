


import pgwidget_pkg.pgwidget.pgwidget_core as pgw


import pygame



glc=pgw.GuiLayoutContext()

geh=pgw.GuiEventHandler(glc)

gth=pgw.GuiTimeHandler(glc,geh)




#gth.time_triggers.append(pgw.TimeTrigger(500,function1))

#gth.time_triggers.append(pgw.TimeTrigger(1000,function2))










def click_button(pos):
    print("CLICK BUTTON")
    for i,button in enumerate(buttons.elements):
        if button.is_point_in_rectangle(pos):
            button.run_function(button.function_args)
    


buttons=pgw.PgWidget(click_button)

button1=pgw.Button([630,500],[150,20],"Button",function=lambda *args:None)
buttons.elements.append(button1)




glc.labels.append(pgw.Label("",(0,0,0),pos=[100,300],font_size=16))
glc.labels.append(pgw.Label("",(0,0,0),pos=[100,330],font_size=16))
glc.labels.append(pgw.Label("",(0,0,0),pos=[100,360],font_size=16))
glc.labels.append(pgw.Label("",(0,0,0),pos=[100,390],font_size=16))


glc.entries.append(pgw.PgwEntry("",[500,500],[100,30]))
glc.entries.append(pgw.PgwEntry("",[500,535],[100,30]))


glc.labels.append(pgw.Label("Name",(0,0,0),pos=[400,500],font_size=16))
glc.labels.append(pgw.Label("Password",(0,0,0),pos=[400,535],font_size=16))



pgwidgets=[buttons]
 



glc.pgwidgets=pgwidgets


pgw.main_program_loop(glc, geh, gth)
   