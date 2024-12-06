import numpy as np

class AnimationCurvePoint():
	def __init__(self, x : float, y : float, slope : float):
		self.x = x
		self.y = y
		self.m = slope

class AnimationCurve():
	def __init__(self, minX, maxX, points : list[AnimationCurvePoint]):
		self.minX = minX
		self.maxX = maxX
		self.points = points
		self.cache = [[0,0,0,0]]*len(self.points)
	def smooth_transition(self, i1, i2, value : float):
		if self.cache[i1][0] == 0:
			point1 = self.points[i1]
			point2 = self.points[i2]
			x1 = point1.x
			x2 = point2.x
			y1 = point1.y
			y2 = point2.y
			m1 = point1.m
			m2 = point2.m
			A = np.array([
	        [x1**3, x1**2, x1, 1],
	        [x2**3, x2**2, x2, 1],
	        [3*x1**2, 2*x1, 1, 0],
	        [3*x2**2, 2*x2, 1, 0]
	    ])
			b = np.array([y1, y2, m1, m2])
	    
			coeffs = np.linalg.solve(A, b)
			a, b, c, d = coeffs 
			self.cache[i1] = [a, b, c, d]
		return self.transition_function(value, i1)
	def transition_function(self, x, i):
		a,b,c,d = self.cache[i]
		return round(a*x**3 + b*x**2 + c*x + d, 6)
	def Evaluate(self, value : float):
		value = max(self.minX ,min(value, self.maxX))
		for i in range(len(self.points)-1):
			point = self.points[i]
			point2 = self.points[i+1]
			if point.x <= value and point2.x >= value:
				result = self.smooth_transition(i, i+1, value)
				return result