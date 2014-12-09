import turtle
def func_A(n):
	if n == 0:
		return "A"
	else:
		return func_B(n-1) + "-" + func_A(n-1) + "-" + func_B(n-1) 
def func_B(n):
	if n == 0:
		return "B"
	else:
		return func_A(n-1) + "+" + func_B(n-1) + "+" + func_A(n-1) 
def draw(n,t,d):
	string = func_A(n)
	saved_pos = []
	saved_heading = []
	for c in string:
		if c == "+":
			t.left(60)
		if c == "-":
			t.right(60)
		if c == "A":
			t.forward(d)
		if c == "B":
			t.forward(d)
s = turtle.Screen()
turtle = turtle.Turtle()
turtle.hideturtle()
turtle.penup()
#turtle.setpos(-200,-200)
turtle.pendown()
turtle.speed("fastest")