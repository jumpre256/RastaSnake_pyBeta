import pygame, gameCore
from overrides import override
from Queue import Queue

class TurnCommand():

	def __init__(self, square, direction):
		self.__square = square
		self.__direction = direction

	def getSquare(self):
		return self.__square

	def getDirection(self):
		return self.__direction


class SnakeSegment():
    def __init__(self, width, height, speed, direction, color):
        self.__x = -1
        self.__y = -1
        self._speed = speed
        self.object = pygame.Rect(0, 0, width, height)
        self.color = color
        self._direction = direction
        self.__commandsQueue = Queue()

    def setX(self, x):
        self.__x = x
        self.object.x = self.__x

    def setY(self, y):
        self.__y = y
        self.object.y = self.__y

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getColor(self):
        return self.color

    def getDirection(self):
        return self._direction

    def getCopyOfCommandsQueue(self) -> list:
        queue = self.__commandsQueue
        returnStruct = []
        size = queue.getSize()
        for i in range(size):
            returnStruct.append(TurnCommand(queue.peek(i).getSquare(), queue.peek(i).getDirection()))
        return returnStruct

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.object)

    def tick(self):
        self._turnLogic()
        self._doRun()

    def addTurnCommand(self, turnCommand):
        if type(turnCommand) == TurnCommand:
            self.__commandsQueue.enqueue(turnCommand)

    def _doRun(self):
        if self._direction == gameCore.GridDirection.UP:
            self.setY(self.getY() - self._speed)
        elif self._direction == gameCore.GridDirection.LEFT:
            self.setX(self.getX() - self._speed)
        elif self._direction == gameCore.GridDirection.DOWN:
            self.setY(self.getY() + self._speed)
        elif self._direction == gameCore.GridDirection.RIGHT:
            self.setX(self.getX() + self._speed)

    def _turnLogic(self):
        if self.__commandsQueue.getSize() > 0:
            requiredSquareX = self.__commandsQueue.peek().getSquare()[0]
            requiredSquareY = self.__commandsQueue.peek().getSquare()[1]
            segmentHasCorrectX = self.getX() == requiredSquareX
            segmentHasCorrectY = self.getY() == requiredSquareY
            if segmentHasCorrectX and segmentHasCorrectY:
                self._direction = self.__commandsQueue.dequeue().getDirection()



class SnakeHead(SnakeSegment):

    def __init__(self, width, height, speed, color, size = 0):
        super().__init__(width, height, speed, gameCore.GridDirection.RIGHT, color)
        self._score = 0
        self._nextDirection = gameCore.GridDirection.RIGHT
        self.__size = size
        self.__children = []

        #initialize the snake:
        GRID_SQUARE_WIDTH = gameCore.FieldBackground.getGridSquareWidth()
        headPosition = gameCore.FieldBackground.getPixelsFromCoordinates_snakeHead(size, 0)
        self.setX(headPosition[0])
        self.setY(headPosition[1])
        childIndex = 0
        for i in range(size):
            childIndex += 1
            self.__children.append(SnakeSegment(40, 40, self._speed, gameCore.GridDirection.RIGHT, gameCore.Color.generateRastaSnakeGreen()))
            childPosition = gameCore.FieldBackground.getPixelsFromCoordinates_snakeSegment(size-childIndex, 0)
            self.__children[childIndex-1].setX(childPosition[0])
            self.__children[childIndex-1].setY(childPosition[1])

    def getScore(self):
        return self._score

    def resetScore(self):
        self._score = 0

    def setNextDirection(self, value):
        if type(value) == gameCore.GridDirection:
            self._nextDirection = value

    def __increaseInSize(self):
        self.__naiveApproachToIncreaseInSize()

    def __naiveApproachToIncreaseInSize(self):
        GRID_SQUARE_WIDTH = gameCore.FieldBackground.getGridSquareWidth()
        lastChild = self.__children[self.__size - 1]
        keyVector = gameCore.vectorsForDirectionOpposites[lastChild.getDirection()]
        newX = lastChild.getX() + (keyVector[0]*GRID_SQUARE_WIDTH)
        newY = lastChild.getY() + (keyVector[1]*GRID_SQUARE_WIDTH)
        self.__size += 1
        prevTail = self.__children[self.__size - 2]
        self.__children.append(SnakeSegment(40, 40, self._speed, prevTail.getDirection(), gameCore.Color.generateRastaSnakeGreen()))
        newTail = self.__children[self.__size - 1]
        newTail.setX(newX)
        newTail.setY(newY)
        commandsQueue = prevTail.getCopyOfCommandsQueue()
        for command in commandsQueue:
            newTail.addTurnCommand(command)

    @override
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.object)
        for bodySegment in self.__children:
            bodySegment.draw(window)

    @override
    def tick(self):
        self._testIfEatFruit()
        deadByOutOfBounds = self._outOfBoundsLogic()
        deadByCollisionWithSelf = self._collideWithSelfLogic()
        isDead = deadByOutOfBounds or deadByCollisionWithSelf
        self._turnLogic()
        self._doRun()
        for bodySegment in self.__children:
            bodySegment.tick()
        return isDead

    def _testIfEatFruit(self):
        eatFruit = []
        fruitIndex = -1
        isEaten = False
        for fruitObj in gameCore.Field.fruit:
            fruitIndex += 1
            isEaten = self.object.colliderect(fruitObj.object)
            if isEaten == True:
                eatFruit.append(fruitIndex)
        if len(eatFruit) > 0:
            for fruitIndex in eatFruit:
                gameCore.Field.fruitEaten(fruitIndex)
                self._score += 1
                self.__increaseInSize()
                gameCore.Field.generateFruit()

    def _collideWithSelfLogic(self):
        isDead = False
        for segmentIndex in range(len(self.__children)):
            if segmentIndex != 0:
                isDead = self.object.colliderect(self.__children[segmentIndex].object)
                if isDead == True:
                    break;
        return isDead

    def _outOfBoundsLogic(self):
        isDead = False
        outsideWidthBoundaryBool = self.getX() < 0 or self.getX() > gameCore.DISPLAY_WIDTH - self.object.w
        outsideHeightBoundaryBool = self.getY() < gameCore.FieldBackground.getTopbarHeight() or self.getY() > gameCore.DISPLAY_HEIGHT - self.object.h
        if outsideWidthBoundaryBool or outsideHeightBoundaryBool:
            isDead = True
        return isDead

    @override
    def _turnLogic(self):
        newTurnCommand = None
        GRID_SQUARE_WIDTH = gameCore.FieldBackground.getGridSquareWidth()
        #print((self.getX(), self.getY()))    #debug
        snakeWantsToTurnBool = self._direction != self._nextDirection
        snakeMayTurnBool = gameCore.FieldBackground.checkPixelsTurnable_snakeHead(self.getX(), self.getY())
        if snakeWantsToTurnBool and snakeMayTurnBool:
            self._direction = self._nextDirection
            square = (self.getX()-4+10, self.getY()-4+10)
            newTurnCommand = TurnCommand(square, self._direction)
        if newTurnCommand != None:
            for bodySegment in self.__children:
                bodySegment.addTurnCommand(newTurnCommand)