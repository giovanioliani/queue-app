from cmd import Cmd
from collections import deque

class centerPrompt(Cmd):
	def __init__(self):
		super().__init__()
		self.available = ['B', 'A']
		# Contains Ids of calls waiting to be answered
		self.waiting = deque()
		# Contains mappings from busy operators into their calls and vice-versa
		self.busy = dict()
		# Contains mapping from ringing calls into their operators and vice-versa
		self.ringing = dict()

	def dictPopElement(self, mapping, id):
		ret = mapping.pop(id)
		del mapping[ret]
		return ret
	def dictInsertElement(self, mapping, op_id, call_id):
		mapping[op_id] = call_id
		mapping[call_id] = op_id

	def do_call(self, call_id):
		print("Call", call_id, "received")
		if len(self.available) == 0:
			self.waiting.append(call_id)
			print("Call", call_id, "waiting in queue")
		else:
			op_id = self.available.pop()
			self.dictInsertElement(self.ringing, op_id, call_id)
			print("Call", call_id, "ringing for operator", op_id)

	def do_answer(self, op_id):
		call_id = self.dictPopElement(self.ringing,op_id)
		self.dictInsertElement(self.busy, op_id, call_id)
		print("Call", call_id, "answered by operator", op_id)


	def do_reject(self, op_id):
		call_id = self.dictPopElement(self.ringing, op_id)
		print("Call", call_id, "rejected by operator", op_id)
		if len(self.available) == 0:
			self.available.append(op_id)
		op_id = self.available.pop()
		self.dictInsertElement(self.ringing, op_id, call_id)
		print("Call", call_id, "ringing for operator", op_id)

	def do_hangup(self, call_id):
		if call_id in self.busy:
			op_id = self.busy.pop(call_id)
			del self.busy[op_id]
			print("Call", call_id, "finished and operator", op_id, "available")
			if len(self.waiting) > 0:
				call_id = self.waiting.popleft()
				self.dictInsertElement(self.ringing, op_id, call_id)
				print("Call", call_id, "ringing for operator", op_id)
			else:
				self.available.append(op_id)
		elif call_id in self.ringing:
			op_id = self.dictPopElement(self.ringing, call_id)
			print("Call", call_id, "missed")
			if len(self.waiting) > 0:
				call_id = self.waiting.popleft()
				self.dictInsertElement(self.ringing, op_id, call_id)
				print("Call", call_id, "ringing for operator", op_id)
		else:
			self.waiting.remove(call_id)
			print("Call", call_id, "missed")

	def do_EOF(self, id):
	    exit(0)


if __name__ == '__main__':
	prompt = centerPrompt()
	prompt.prompt = ''
	prompt.cmdloop()
