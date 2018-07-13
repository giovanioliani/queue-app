from cmd import Cmd
from collections import deque

class centerOperator(object):
	state = 'avalilable'
	call = ""
	def __init__(self, id):
		self.id = id

class centerPrompt(Cmd):
	def initialize(self):
		self.operators = dict.fromkeys('A','B')
		self.operators['A'] = centerOperator('A')
		self.operators['B'] = centerOperator('B')
		self.available = [self.operators['B'], self.operators['A']]
		self.waiting = deque()
		self.busy = dict()

	def do_call(self,id):
		""" Usage: call <id> """
		print("Call", id, "received")
		if len(self.available) == 0:
			print("Call", id, "is waiting in queue")
			self.waiting.append(id)
		else:
			op = self.available.pop()
			op.state = 'busy'
			print("Call", id, "answered by operator", op.id)
			self.busy[id] = op
	def do_hangup(self, id):
		""" Usage: hangup <id> """
		op = self.busy[id]
		op.state = "available"
		print("Call", id, "finished and operator", op.id, "available")
		if len(waiting) > 0:
			call = self.waiting.popleft()
			self.busy[id] = op
		else:
			self.available.append(op)
	def do_reject(self, id):
		for call in self.waiting:
			if call == id:
				


if __name__ == '__main__':
	prompt = centerPrompt()
	prompt.initialize()
	prompt.prompt = '$ '
	prompt.cmdloop()