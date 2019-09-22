from tkinter import *
import tkinter.messagebox
from time import time, sleep

'''
===== SUDOKU REPRESENTATION AND NAVIGATION =====

sudoku is represented by a list of values
they are ordered this way for clear view only
numbers inside brackets represent indexes
[ 0][ 1][ 2] | [ 3][ 4][ 5] | [ 6][ 7][ 8]
[ 9][10][11] | [12][13][14] | [15][16][17]
[18][19][20] | [21][22][23] | [24][25][26]
-------------+--------------+-------------
[27][28][29] | [30][31][32] | [33][34][35]
[36][37][38] | [39][40][41] | [42][43][44]
[45][46][47] | [48][49][50] | [51][52][53]
-------------+--------------+-------------
[54][55][56] | [57][58][59] | [60][61][62]
[63][64][65] | [66][67][68] | [69][70][71]
[72][73][74] | [75][76][77] | [78][79][80]

For extracting the row:
start = index // 9 * 9
end = start + 9
row = sudoku[start:end]

For extracting the column:
start = index % 9
end = start + 72
column = [sudoku[i] for i in range(start, end+1, 9)]

For extracting the 3x3 square:
First find the row and column nums
of top-left cell of a square:
row_num = (index // 9 * 9) // 27 * 27
col_num = (index % 9) // 3 * 3
start = row_num + col_num
end = start + 18
square = []
for col in range(start, end+1, 9):
	for row in range(3):
		square.append(sudoku[col+row])


===== BACKTRACK ALGORITHM =====

list of rules violations:
- if number is greater than 9
- if number already exists in sudoku row
- if number already exists in sudoku column
- if number already exists in sudoku 3x3 square

Each loop cycle increments the given number by 1

while number index does not reach end of the list of numbers:
add 1 to current number
(set an upper limit to possible numbers)
if number > 9:
	set number and respective cell value to 0 and go back to prev number
else:
	check if this number doesn't violate the rules
	if no violations:
		set respective cell value to this number
		advance to the next number
if current number index is negative:
	(it means that algo did not find a solution without violations)
'''

def timer(func):
	def wrapper(*args):
		time1 = round(time(), 4)
		func(*args)
		time2 = round(time(), 4)
		msg = 'Solved with {0} algorythm in {1} m, {2} s.'.format(
			func.__name__.title(),
			round((time2-time1)//60),
			round(((time2-time1) - (time2-time1)//60*60)))
		tkinter.messagebox.showinfo('Message', msg)
	return wrapper


class Sudoku():

	# permitted input for sudoku cells
	DIGITS = ('1','2','3','4','5','6','7','8','9')

	def __init__(self, size=3):
		self.cells = []
		self.size = size if size >= 3 else 3

		def close_the_window():
		    if tkinter.messagebox.askokcancel(
				'Quit', 'Do you really wish to quit?'):
		        root.destroy()

		def update_status_bar(event):
			if event.widget == solve:
				statusbar.config(text=' Solve the grid.')
			elif event.widget == clear:
				statusbar.config(text=' Clear the grid.')
			elif event.widget == quit:
				statusbar.config(text=' Close the program.')
			else:
				loc = self.cells.index(event.widget)
				row=loc // 9 + 1
				col=loc % 9 + 1
				statusbar.config(
					text=f' Cell [{row}, {col}]')

		def grid_navigation(event):
			if event.keysym == 'Up':
				loc = self.cells.index(event.widget)
				if not loc // 9 == 0: self.cells[loc-9].focus()
			if event.keysym == 'Down':
				loc = self.cells.index(event.widget)
				if not loc // 9 == 8: self.cells[loc+9].focus()
			if event.keysym == 'Left':
				loc = self.cells.index(event.widget)
				if not loc % 9 == 0: self.cells[loc-1].focus()
			if event.keysym == 'Right':
				loc = self.cells.index(event.widget)
				if not loc % 9 == 8: self.cells[loc+1].focus()

		def clear_status_bar(event):
			statusbar.config(text='')

		root = Tk()
		self.root = root
		root.title(string='Sudoku Solver')
		root.resizable(width=False, height=False)
		root.protocol('WM_DELETE_WINDOW', close_the_window)
		outer_frame = Canvas(root,
			highlightbackground='black',
			highlightthickness=1)
		outer_frame.pack(padx=5, pady=5)
		inner_frame = Canvas(outer_frame,
			highlightbackground='black',
			highlightthickness=1,
			bg='grey')
		inner_frame.pack(padx=1, pady=1)
		line1 = inner_frame.create_line(96, 0, 96, 300, width=2.0)
		line2 = inner_frame.create_line(192, 0, 192, 300, width=2.0)
		line3 = inner_frame.create_line(0, 90, 300, 90, width=2.0)
		line4 = inner_frame.create_line(0, 180, 300, 180, width=2.0)
		# make a grid in tkinter
		# 'cells' is a list of pointers to Entry fields
		# 'coordinates' is a list of coordinates of respective cells in 'cells'
		for cell_num in range(81):
			e = Entry(
				inner_frame,
				width=2,
				justify=CENTER,
				relief=FLAT,
				fg='black')
			e.insert(0, string='')
			self.cells.append(e)
			self.cells[cell_num].bind('<Enter>', update_status_bar)
			self.cells[cell_num].bind('<Leave>', clear_status_bar)
			self.cells[cell_num].bind('<Up>', grid_navigation)
			self.cells[cell_num].bind('<Down>', grid_navigation)
			self.cells[cell_num].bind('<Left>', grid_navigation)
			self.cells[cell_num].bind('<Right>', grid_navigation)
			e.grid(
				row=cell_num // 9,
				column=cell_num % 9,
				padx=1,
				pady=1)


		solve = Button(root, text='Solve', command=self.backtrack)
		solve.bind('<Enter>', update_status_bar)
		solve.bind('<Leave>', clear_status_bar)
		solve.pack(side=LEFT, padx=5, pady=5)

		clear = Button(root, text='Clear', command=self.clear_the_grid)
		clear.bind('<Enter>', update_status_bar)
		clear.bind('<Leave>', clear_status_bar)
		clear.pack(side=LEFT, padx=5, pady=5)

		quit = Button(root, text='Quit', command=root.quit, fg='red')
		quit.bind('<Enter>', update_status_bar)
		quit.bind('<Leave>', clear_status_bar)
		quit.pack(side=LEFT, padx=5, pady=5)

		statusbar = Label(root, text='', bd=1, relief=SUNKEN, anchor=W)
		statusbar.pack(side=BOTTOM, fill=X, padx=5, pady=5)
		root.mainloop()

	def clear_the_grid(self):
		for cell in self.cells:
			cell.delete(0, END)
			cell.insert(0, '')
			cell.config(fg='black')

	def parse_input(self):
		# create a list of digits extracted from Entry fields
		grid = []
		for cell in self.cells:
			grid.append(int(cell.get())) if \
				cell.get() in self.DIGITS else grid.append(0)
		return grid

	@staticmethod
	def cannot_solve():
		tkinter.messagebox.showinfo('Message', 'Sudoku can not be solved.')

	# if inserting num in sudoku[index]  doesn't cause
	# violations of rules return True, otherwise return Fasle
	@staticmethod
	def check_for_violations(grid, num, index):
		# check for row violations
		row_start = index // 9 * 9
		row_end = row_start + 9
		row = grid[row_start:row_end]
		# check for column violations
		col_start = index % 9
		col_end = col_start + 72
		column = [grid[i] for i in range(col_start, col_end+1, 9)]
		# check for square violations
		row_num = (index // 9 * 9) // 27 * 27
		col_num = (index % 9) // 3 * 3
		sqr_start = row_num + col_num
		sqr_end = sqr_start + 18
		square = []
		for row_count in range(sqr_start, sqr_end+1, 9):
			for col_count in range(3):
				square.append(grid[col_count+row_count])
		return not (num in row or num in column or num in square)

	def put_new_number(self, index, num, success=True):
		self.cells[index].delete(0, END)
		foreground = 'white' if num == 0 else 'green' if success else 'red'
		self.cells[index].config(fg=foreground)
		self.cells[index].insert(0, string=str(num))
		sleep(0.025)
		self.root.update()

	# ***** Backtrack method *****

	@timer
	def backtrack(self):
		grid = self.parse_input()
		# 'solved_cells' is a list, where every item is
		# a list containing number and its index in grid
		# it contains only those numbers,
		# which are not inserted manually
		solved_cells = [[0, i] for i in range(len(grid)) if grid[i] == 0]
		cell_cursor = 0
		while cell_cursor < len(solved_cells):
			# increment current number by 1
			solved_cells[cell_cursor][0] += 1
			num = solved_cells[cell_cursor][0]
			index = solved_cells[cell_cursor][1]
			if num > 9:
				# change value to 0 and empty the cell
				solved_cells[cell_cursor][0] = 0
				num = solved_cells[cell_cursor][0]
				index = solved_cells[cell_cursor][1]
				grid[index] = 0
				self.put_new_number(index, num, success=False)
				# go to prev cell and paint it red
				cell_cursor -= 1
				num = solved_cells[cell_cursor][0]
				index = solved_cells[cell_cursor][1]
				self.put_new_number(index, num, success=False)
			elif self.check_for_violations(grid, num, index):
				#assign current value and paint it green
				grid[index] = num
				num = solved_cells[cell_cursor][0]
				index = solved_cells[cell_cursor][1]
				self.put_new_number(index, num)
				cell_cursor += 1
			# condition for declaring grid unsolvable
			if cell_cursor < 0:
				return self.cannot_solve()


sudoku = Sudoku()
