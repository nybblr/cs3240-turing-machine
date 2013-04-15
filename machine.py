import sys
from utility import *

class TuringMachine:
	def __init__(self, input, states, trans):
		self.sm = StateMachine(self, states, trans)
		self.tape = [Cell(input[i]) for i in range(len(input))]
		self.head = 0
		
	def run(self):
		self.printDebug()

		while True:
			self.sm.step(self.currCell().char)

			self.printConfig()

			if self.sm.accepts():
				print("We accepted!")
				break
			if self.sm.rejects():
				print("We rejected!")
				break

	def currCell(self):
		if self.tape[self.head] is None:
			self.tape[self.head] = Cell(None)
		return self.tape[self.head]

	def printConfig(self):
		print("We are in "+str(self.sm.curr)+ " with the tape:")
		print(self.tape)

	def printDebug(self):
		print("-------------DEBUG----------------------")
		print(self.sm.states)
		print(self.sm.trans)
		print(self.tape)
		print(self.head)
		print("----------------------------------------")

class Cell:
	def __init__(self, char, mark=False):
		self.char = char
		self.mark = mark

	def __repr__(self):
		return self.char

class StateMachine:
	def __init__(self, tm, states, transitions):
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

	def __repr__(self):
		return str((self.to, self.char, self.head))

if __name__ == "__main__":
	input = sys.argv[1]

	states = [
			('Start', None),
			('Accept', True),
			('Reject', False)
	]

	transitions = {
			(0, '0'): (2, 'e', State.L),
			(0, '1'): (1, None, State.L),
	}

	states = [State(s[1], s[0]) for s in states]
	trans = {}
	for f, t in transitions.items():
		(f, pc) = f
		(t, nc, h) = t
		trans[(states[f], pc)] = Transition(states[t], nc, h)

	machine = TuringMachine(input, states, trans)
	machine.run()
