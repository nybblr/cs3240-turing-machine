import sys
from utility import *

class TuringMachine:
	def __init__(self, input, states, trans, start=None):
		self.sm = StateMachine(self, states, trans, start)
		self.tape = [Cell(input[i]) for i in range(len(input))]
		self.head = 0
		
	def run(self):
		# self.printDebug()
		self.printConfig()

		while True:
			self.sm.step(self.currCell().char)

			self.printConfig()

			if self.sm.accepts():
				print("Accept: "+str(self.sm.curr))
				break
			if self.sm.rejects():
				print("Reject: "+str(self.sm.curr))
				break

	def currCell(self):
		if self.tape[self.head] is None:
			self.tape[self.head] = Cell(None)
		return self.tape[self.head]

	def printConfig(self):
		string = ""
		for cell in self.tape:
			string += str(cell)+' '
		
		string += "=> "+str(self.sm.curr)
		print(string)
		print('  '*self.head + '^')

	def printDebug(self):
		print("-------------DEBUG----------------")
		print(self.sm.states)
		print(self.sm.trans)
		print("----------------------------------")

class Cell:
	def __init__(self, char, mark=False):
		self.char = char
		self.mark = mark

	def __repr__(self):
		s = self.char
		if s is None or s is '':
			s = '~'

		return self.char

class StateMachine:
	def __init__(self, tm, states, transitions, start=None):
		if start:
			self.curr = start
		else:
			self.curr = states[0]
		self.states = states
		self.trans = transitions
		self.tm = tm

	def step(self, char):
		if (self.curr, char) in self.trans:
			transition = self.trans[(self.curr, char)]
			self.curr = transition.to
			transition.apply(self.tm)
		else:
			raise Exception("No such transition from {0} on {1} exists!".format(str(self.curr), char))

	def accepts(self):
		return self.curr.accepting()

	def rejects(self):
		return self.curr.rejecting()

class State:
	L = -1
	R = 1
	# S = 0
	def __init__(self, action, label=None):
		self.action = action
		self.label = label

	def __repr__(self):
		s = self.label
		if self.accepting():
			s = "+"+s 
		if self.rejecting():
			s = "-"+s

		return s

	def accepting(self):
		return self.action is True

	def rejecting(self):
		return self.action is False

class Transition:
	def __init__(self, to, char, head):
		self.to = to
		self.char = char
		self.head = head

	def apply(self, tm):
		# Overwrite current cell if given
		if self.char:
			tm.currCell().char = self.char

		# Move head
		tm.head += self.head
		tm.head = max(tm.head, 0)

	def __repr__(self):
		return str((self.to, self.char, self.head))

if __name__ == "__main__":
	L = State.L; R = State.R

	input = "$"+sys.argv[1]+"#"

	states = [
			('reject', False),
			('1', None),
			('2', None),
			('3', None),
			('4', None),
			('5', None),
			('6', None),
			('accept', True),
	]

	transitions = {
		(1, '0'): (1,'0',L),	(1, '1'): (1,'1',L),	(1, '$'): (2,'$',R),	(1, 'X'): (1,'X',L),	(1, '#'): (1,'#',L),
		(2, '0'): (3,'0',R),	(2, '1'): (4,'X',L),	(2, '$'): (0,'#',R),	(2, 'X'): (2,'X',R),	(2, '#'): (7,'#',R),
		(3, '0'): (3,'0',R),	(3, '1'): (4,'X',L),	(3, '$'): (0,'#',R),	(3, 'X'): (3,'X',R),	(3, '#'): (0,'#',R),
		(4, '0'): (4,'0',L),	(4, '1'): (4,'1',L),	(4, '$'): (5,'$',R),	(4, 'X'): (4,'X',L),	(4, '#'): (4,'#',L),
		(5, '0'): (6,'X',R),	(5, '1'): (5,'1',R),	(5, '$'): (0,'#',R),	(5, 'X'): (5,'X',R),	(5, '#'): (0,'#',R),
		(6, '0'): (1,'X',L),	(6, '1'): (6,'1',R),	(6, '$'): (0,'#',R),	(6, 'X'): (6,'X',R),	(6, '#'): (0,'#',R),
	}

	states = [State(s[1], s[0]) for s in states]
	trans = {}
	for f, t in transitions.items():
		(f, pc) = f
		(t, nc, h) = t
		trans[(states[f], pc)] = Transition(states[t], nc, h)

	machine = TuringMachine(input, states, trans, start=states[1])
	machine.run()
