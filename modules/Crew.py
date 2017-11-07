# leftExp for future extension

class ExpCalc:
	# Function for print-
	def run_diff(self, start, end, leftExp = 0):
		# IMPORTANT ASSUMPTION : All inputs are filtered

		# Covering Exception
		if start == end:
			return ""
		elif start > end:
			start, end = end, start

		result = self.exp(start, end, leftExp)
		text = "필요한 경험치 > " + str(result) + " | [ " +  self.expToSkills(start)
		if leftExp != 0:
			text += " with left-exp " + str(leftExp)
		text += " > " + self.expToSkills(end) + " ]"

		return text

	def run_acc(self, start, gain, leftExp = 0):
		# IMPORTANT ASSUMPTION : All inputs are filtered

		overExp = gain - leftExp
		result = start

		if 0 != leftExp:
			result += 1

		while self.getNext(result) <= overExp:
			overExp -= self.getNext(result)
			result += 1

		text = "결과 > " + self.expToSkills(result)
		if 0 != overExp:
			text += " (잔여 " + str(overExp) + ")"
		text += " = " + self.expToSkills(start)
		if 0 != leftExp:
			text += " with left-exp " + str(leftExp)
		text += " + " + str(gain) + "경험치"

		return text

	def exp(self, start, end, leftExp = 0):
		# Covering Exception
		if start == end:
			return 0
		elif start > end:
			start, end = end, start

		acc = 0
		if leftExp != 0:
			acc = leftExp
			start += 1
		for exp in range(start,end):
			acc += self.getNext(exp)
		
		return acc

	def getNext(self, start):
		skill = start // 100 + 1
		per = (start % 100) / 100
		return round((2 ** skill) * 25 * (100 ** per))

	def testPrint(self, a, b, c=0):
		print(a, 'to', b, 'with expression [LeftExp]', c, '=', exp(a, b, c))

	def expToSkills(self, val):
		# val : 50~999
		skill = val // 100
		percent = val % 100
		if percent == 0:
			skill -= 1
			percent = 100
		return str(skill) + "스킬 " + str(percent) + "%"
