from .libbarpy import *  # Import symbols from the .pyd file
import numpy as np


def get_matrix(item : Baritem):
	matrix = np.array(item.getBarcodeLines()[0].getPoints())
	return matrix

def append_line_to_matrix(barline : Barline, matrix : np.array):
	ksize = barline.getMatrixSize()
	for i in range(ksize):
		p = barline.getMatrixValue(i)
		matrix[p.y,p.x] += p.value.value()

def combine_components_into_matrix(barlines : list[Barline] | Barline, shape : tuple, type = np.uint8):

	if barlines is Barline:
		barlines = [barlines]

	binmap = np.zeros(shape, type)

	# isRgb = len(shape) == 3
	for bl in barlines:
		append_line_to_matrix(bl, binmap)

	return binmap


class Barcode:
	def __init__(self, img, bstruct : barstruct = barstruct()):
		self.shape = (0,0)
		self.type = np.uint8
		self.item = create(img, bstruct)
		self.revert = bstruct.proctype == ProcType.f0t255
		pass

	def get_largest_component(self):
		biggestMatrixId = 0
		lines = self.item.getBarcodeLines()
		msize = lines[0].getMatrixSize()
		for i in range(1, len(lines)):
			if lines[i].getMatrixSize() > msize:
				biggestMatrixId = i
				msize = lines[i].getMatrixSize()

		return lines[biggestMatrixId]

	def get_first_component(self):
		return self.item.getBarcodeLines()[0]

	def get_first_component_matrix(self):
		matrix = np.array(self.item.getBarcodeLines()[0].getPoints())
		return matrix


	def split_components(self, threshold : int):
		if threshold > len(self.item.getBarcodeLines()):
			a = combine_components_into_matrix(self, self.item.getBarcodeLines(), self.shape, type)
			b = np.zeros(self.shape, type)
			return (a, b)

		a = self.item.getBarcodeLines()[:threshold]
		b = self.item.getBarcodeLines()[threshold:]
		a = combine_components_into_matrix(self, a, self.shape, type)
		b = combine_components_into_matrix(self, b, self.shape, type)
		return (a, b)


	def combine_components_into_matrix(self):
		return combine_components_into_matrix(self.item.getBarcodeLines(), self.shape, self.type)


	def filter(img, revert, LL = 180):
		struct = BarConstructor()
		struct.returnType = ReturnType.barcode2d
		struct.createBinaryMasks = True
		struct.createGraph = False
		struct.setPorogStep(255)
		struct.addStructure(ProcType.f0t255 if not revert else ProcType.f255t0, ColorType.gray, ComponentType.Component)

		containet = create(img, struct)

		item = containet.getItem(0)
		bar = item.getBarcodeLines()

		binmap = np.zeros(img.shape, np.uint8)
		for bl in bar:

			if bl.len() < LL:
				continue

			#! Третий(самый быстрый (в теории)):
			append_line_to_matrix(bl, binmap)


		if not revert:
			binmap = 255 - binmap

		return binmap

	def segmentation(img, revert, minSize, useBinarySegment = True):
		struct = barstruct()
		struct.returnType = ReturnType.barcode2d
		struct.createBinaryMasks = True
		struct.createGraph = False
		struct.setPorogStep(minSize)
		struct/(ProcType.f0t255 if not revert else ProcType.f255t0, ColorType.gray, ComponentType.Component)

		containet = create(img, struct)

		item = containet.getItem(0)
		bar = item.getBarcodeLines()

		# red=(0,0,255)
		# blue =(255,0,0)
		# green=(0,255,0)
		# colors=[red, blue, green]

		from random import randint
		colors = []
		if not useBinarySegment:
			for i in range(len(bar)):
				colors.append(np.array([randint(0, 255),randint(0, 255),randint(0, 255)]))

			binmap = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
		else:
			binmap = np.zeros((img.shape[0],img.shape[1]), np.uint8)

		i=0
		for bl in bar:
			keyvals = bl.getPoints()

			if bl.len() < 40: #and len(keyvals)<500:
				continue

			if (len(keyvals)>img.shape[0]*img.shape[1]*0.9):
				continue

			for p in keyvals:
				binmap[p.y,p.x] = 255 if useBinarySegment else colors[i%len(colors)]

			i+=1

		return binmap



def create_barcode(img, struct : barstruct):
	return Barcode(img, struct)
