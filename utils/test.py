import turtle

# 设置画笔
turtle.penup()
turtle.goto(-50, -100)
turtle.pendown()

# 绘制海绵宝宝的正方形身体
turtle.color("yellow")
turtle.begin_fill()
for i in range(4):
    turtle.forward(100)
    turtle.left(90)
turtle.end_fill()

# 绘制海绵宝宝的眼睛和嘴巴
turtle.penup()
turtle.goto(-35, 0)
turtle.pendown()

turtle.color("white")
turtle.begin_fill()
turtle.circle(15)
turtle.end_fill()

turtle.penup()
turtle.goto(35, 0)
turtle.pendown()

turtle.color("white")
turtle.begin_fill()
turtle.circle(15)
turtle.end_fill()

turtle.penup()
turtle.goto(0, -50)
turtle.pendown()

turtle.color("red")
turtle.pensize(5)
turtle.right(90)
turtle.circle(25, 180)

turtle.hideturtle()
turtle.done()
