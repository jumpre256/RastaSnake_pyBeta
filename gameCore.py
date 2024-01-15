import pygame
from enum import Enum
from random import randint

DISPLAY_WIDTH = 960; DISPLAY_HEIGHT = 480+40
FPS = 60;

GridDirection = Enum("GridDirection", [
			"UP",
			"DOWN",
			"LEFT",
			"RIGHT"
			])

Scene = Enum("Scene", [
			"GAMEPLAY",
			"GAMEOVER",
			"RESTART"
			])

directionOpposites = {GridDirection.LEFT: GridDirection.RIGHT,
		GridDirection.RIGHT: GridDirection.LEFT,
		GridDirection.UP: GridDirection.DOWN,
		GridDirection.DOWN: GridDirection.UP}

vectorsForDirectionOpposites = {GridDirection.LEFT: (1, 0),
		GridDirection.RIGHT: (-1, 0),
		GridDirection.UP: (0, 1),
		GridDirection.DOWN: (0, -1)}

class Color():
	trueBlack = (0, 0 , 0)
	grass_green = (0, 160, 48)
	stone_gray = (120, 123, 125)
	dark_stone_gray = (62, 63, 64)
	gameplay_bg_color = stone_gray
	snakeColor = (190, 0, 0)
	squaresHighlightColor = dark_stone_gray
	red = (255, 0, 0)
	light_gray = (204, 204, 204)
	gameover_bg_color = stone_gray
	rasta_head_green = (51, 112, 50)

	@classmethod
	def generateRastaSnakeGreen(cls):
		r = randint(33, 70)
		g = randint(71, 138)
		b = randint(21, 55)
		return (r, g, b)

prev__gridSquareWidth = 60;

class Fruit():
	def __init__(self, fruitType, x, y):
		self.type = fruitType
		self.object = pygame.Rect(x, y, 40, 40)

class Field():

	fruit = []
	window = None
	__totalFruitGenerated = 0 	#for debug.

	@classmethod
	def destroyFruitList(cls):
		cls.__totalFruitGenerated = 0
		cls.fruit.clear()

	@classmethod
	def generateFruit(cls, numberOfFruit = 1, _xBoundary = 0, _yBoundary = 0):
		for i in range(numberOfFruit):
			#cls.__totalFruitGenerated += 1
			maxX = FieldBackground.getNumberOfColumns()
			maxY = FieldBackground.getNumberOfRows()
			randX = randint(_xBoundary, maxX-1)
			randY = randint(_yBoundary, maxY-1)
			#print(cls.__totalFruitGenerated, ": ", (randX, randY), sep='')
			fruitPixelLocations = FieldBackground.getPixelsFromCoordinates_snakeSegment(randX, randY)
			#print(cls.__totalFruitGenerated, ": ", fruitPixelLocations, sep='')
			cls.fruit.append(Fruit("apple", fruitPixelLocations[0], fruitPixelLocations[1]))

	@classmethod
	def draw(cls):
		GRID_SQUARE_WIDTH = FieldBackground.getGridSquareWidth()
		#fruitWidth = GRID_SQUARE_WIDTH - 20
		for fruitObj in cls.fruit:
			#fruitPos = FieldBackground.getPixelsFromCoordinates(fruitObj.object.x, fruitObj.object.y)
			#fruitRect = pygame.Rect(fruitPos[0], fruitPos[1], fruitObj.object.w, fruitObj.object.h)
			pygame.draw.rect(cls.window, Color.grass_green, fruitObj.object)

	@classmethod
	def fruitEaten(cls, fruitIndex):
		cls.fruit.pop(fruitIndex)

class FieldBackground():

	__gridSquareWidth = 60 		#value of -1 indicates we want the class to generate this value itself. This feature is not fully tested yet.
	__numOfColumns = 16
	__numOfRows = 8
	__topbarHeight = 40
	__displayWidth = DISPLAY_WIDTH
	__displayHeight = DISPLAY_HEIGHT - 40
	__leftoverWidth = 0 	#should be 0 but if the user of the class... otherwise, the class initializes this variable to the correct value: int x > 0;
	__leftoverHeight = 0 	#should be 0 but if the user of the class... otherwise, the class initializes this variable to the correct value: int x > 0;
	window = None
	highlightSquareColor = Color.trueBlack #default color is black but can be changed by the user.

	@classmethod
	def _init(cls):
		if cls.__gridSquareWidth != -1:
			cls.__leftoverWidth = cls.__displayWidth - (cls.__gridSquareWidth * cls.__numOfColumns)
			cls.__leftoverHeight = cls.__displayHeight - (cls.__gridSquareWidth * cls.__numOfRows)
			if (cls.__leftoverWidth < 0) or (cls.__leftoverHeight < 0):
				cls.computeSquareWidthFromScratch()
		else: 	#cls.__gridSquareWidth == -1
			cls.computeSquareWidthFromScratch()


	@classmethod
	def computeSquareWidthFromScratch(cls): #bad method name, rename it later.
		widthwiseSquareWidth = cls.__displayWidth // cls.__numOfColumns
		heightwiseSquareWidth = cls.__displayHeight // cls.__numOfRows
		cls.__gridSquareWidth = min(widthwiseSquareWidth, heightwiseSquareWidth)
		cls.__leftoverWidth = cls.__displayWidth - (cls.__numOfColumns * cls.__gridSquareWidth)
		cls.__leftoverHeight = cls.__displayHeight - (cls.__numOfColumns * cls.__gridSquareWidth)

	@classmethod
	def getNumberOfRows(cls):
		return cls.__numOfRows

	@classmethod
	def getNumberOfColumns(cls):
		return cls.__numOfColumns

	@classmethod
	def getTopbarHeight(cls):
		return cls.__topbarHeight

	@classmethod
	def getGridSquareWidth(cls):
		return cls.__gridSquareWidth

	@classmethod
	def setHighlightSquareColor(cls, color):
		cls.highlightSquareColor = color

	@classmethod
	def checkPixelsTurnable_snakeHead(cls, x, y) -> bool:
		isTurnable = ((x-4) % cls.__gridSquareWidth == 0) and ((y-4-cls.__topbarHeight) % cls.__gridSquareWidth == 0)
		return isTurnable

	@classmethod
	def getPixelsFromCoordinates_snakeHead(cls, coordinateX, coordinateY):
		returnX = (coordinateX*cls.__gridSquareWidth)+4
		returnY = (coordinateY*cls.__gridSquareWidth)+4 + cls.__topbarHeight
		return (returnX, returnY)

	@classmethod
	def getPixelsFromCoordinates_snakeSegment(cls, coordinateX, coordinateY):
		returnX = (coordinateX*cls.__gridSquareWidth)+10
		returnY = (coordinateY*cls.__gridSquareWidth)+10 + cls.__topbarHeight
		return (returnX, returnY)

	@classmethod
	def drawBackground(cls):
		width = cls.__gridSquareWidth
		yOffset = cls.__topbarHeight
		for x in range(cls.__numOfColumns):
			for y in range(cls.__numOfRows):
				notLastXBool = x != (cls.__numOfColumns - 1)
				notLastYBool = y != (cls.__numOfRows - 1)
				if notLastXBool and notLastYBool:
					if (x+y)%2 == 1:
						pygame.draw.rect(cls.window, cls.highlightSquareColor, pygame.Rect(x*width, (y*width)+yOffset, width, width))
				elif (not notLastXBool) and notLastYBool:
					if (x+y)%2 == 1:
						pygame.draw.rect(cls.window, cls.highlightSquareColor, pygame.Rect(x*width, (y*width)+yOffset, width+cls.__leftoverWidth, width))
				elif notLastXBool and (not notLastYBool):
					if (x+y)%2 == 1:
						pygame.draw.rect(cls.window, cls.highlightSquareColor, pygame.Rect(x*width, (y*width)+yOffset, width, width+cls.__leftoverHeight))
				else:	#in this case it is true that: (not notLastXBool) and (not notLastYBool)
					if (x+y)%2 == 1:
						pygame.draw.rect(cls.window, cls.highlightSquareColor, pygame.Rect(x*width, (y*width)+yOffset, width+cls.__leftoverWidth, width+cls.__leftoverHeight))

class FontHandler():

	fonts = {}

	@classmethod
	def displayText_topleft(cls, window, text, x, y, size, color = Color.trueBlack):
		if cls.fonts.get(size) == None:
			cls.fonts[size] = pygame.font.SysFont("arial", size)
		font = cls.fonts[size]
		textSurface = font.render(text, True, color)
		textRect = textSurface.get_rect()
		textRect.topleft = (x, y)
		window.blit(textSurface, textRect)

	@classmethod
	def displayText_center(cls, window, text, x, y, size, color = Color.trueBlack):
		if cls.fonts.get(size) == None:
			cls.fonts[size] = pygame.font.SysFont("arial", size)
		font = cls.fonts[size]
		textSurface = font.render(text, True, color)
		textRect = textSurface.get_rect()
		textRect.center = (x, y)
		window.blit(textSurface, textRect)