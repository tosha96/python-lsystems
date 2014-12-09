		elif c == "[":
			saved_pos.append(t.pos())
			saved_heading.append(t.heading())
		elif c == "]":
			t.penup()
			t.setpos(saved_pos.pop())
			t.seth(saved_heading.pop())
			t.pendown()

