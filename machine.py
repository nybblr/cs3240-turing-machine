from utility import *

class TuringMachine:
	def __init__(self, input, states, trans):
		self.sm = StateMachine(self, states, trans)
		self.tape = [Cell(input[i]) for i in range(len(input))]
		self.head = 0

	def run(self):
		while True:
			self.sm.step(currCell().char)

			print("We are in "+str(self.sm.curr)+ "with the tape:\n")
			print(self.tape)

			if self.sm.accepts():
				pass
			if self.sm.rejects():
				pass

	def currCell(self):
		if self.tape[self.head] is None:
			self.tape[self.head] = Cell(None)
		return self.tape[self.head]

class Cell:
	def __init__(self, char, mark=False):
		self.char = char
		self.mark = mark

	def __repr__(self):
		return char

class StateMachine:
	def __init__(self, tm, states, transitions):
		self.curr = states[0]
		self.states = states
		self.trans = transitions
		self.tm = tm

	def step(self, char):
		if (self.curr, char) in self.trans:
			transition = self.transitions[(self.curr, char)]
			self.curr = transition.to
			transition.apply(tm)
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
		s = label
		if s.accepting():
			s = "+"+s 

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
			tm.currCell.char = self.char

		# Move head
		tm.head += self.head

if __name__ == "__main__":
	states = [
			('Start', None),
			('Accept', True),
			('Reject', False)
	]

	transitions = {
			(0, '0'): (1, 'm', State.L),
	}

	states = [State(s[1], s[0]) for s in states]
	trans = {}
	for f, t in transitions.items():
		(f, c) = f
		(t, c, h) = t
		trans[(states[s], c)] = Transition(states[t], c, h)

	machine = TuringMachine(input, states, trans)