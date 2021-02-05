from control.ui import *

app = Application()
app.button_move()
reset = app.button_reset()
print(reset)
app.button_start()
app.button_stop()
app.button_generate()
app.button_exit()

app.drop_down_menu()

app.check_button()

robot = 1
goal = 2
app.text_box(robot, goal)




# if :
#     print("hello")
#     robot = 0
#     goal = 0
#     app.text_box(robot, goal)


app.notification()

app.mainloop()
