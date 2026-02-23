import turtle
import time
import random
wn=turtle.Screen()
wn.title("game snake_habib")
wn.bgcolor("black")
wn.setup(width=600,height=600)
wn.tracer(0)
head=turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0,0)
head.direction="stop"

food=turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100) 

segments=[]

def go_up():
    if head.directiom != "down":
        head.direction ="up"
def go_down():
    if head.direction != "up":
        head.direction = "down"    
def go_left():
    if head.direction!= "right":
        head.direction= "left"
def go_right():
    if head.direction!= "left":
        head.direction= "right"
def move():
    if head.direction== "up":
        y=head.ycor()
        head.sety(y+20)
    if head.direction=="down":
        y=head.sety(y-20)    
    if head.direction=="left":
        x=head.xcor()
        head.setx(x-20)
    if head.direction=="right":
        x=head.setx(x+20)

wn.listen()                               
wn.onkeypreess(go_up,"up")
wn.onkeypreess(go_down,"down")
wn.onkeypreess(go_left,"left")
wn.onkeypreess(go_right,"right")

while True:
    wn.update()
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
     time.sleep(1)
    head.goto(0,0)
    head.direction="stop"
    for segment in segments:
        segment.goto(1000,1000)
        segment.clear()
    if head.distance(food)< 20:
        x=random.randint(-280,280)
        y=random.randint(-280,280)
        food.goto(x,y)
        new_segment= turtle.Turtle()
        new_segment.speed(0)
    new_segment.shape("square")
    new_segment.color("grey")
    new_segment.penup()
    segments.append(new_segment)
    for index in range(len(segments)-1,0,1):
        x= segments[index].xcor()
        y= segments[index].ycor()
        segments[index].goto(x,y)
    if len(segments)>0:
        x=head.xcor()
        y=head.ycor()
        segments[0].goto(x,y)
    move()
    time.sleep(0.1)
    wn.mainloop()    
