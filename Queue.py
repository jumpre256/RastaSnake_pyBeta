

class Queue():

    def __init__(self):
        self.__internalStructure = []
        self.__size = 0

    def getSize(self):
        return self.__size

    def enqueue(self, element):
    	#elements will be TurnCommand objects.
    	self.__internalStructure.append(element)
    	self.__size += 1

    def peek(self, _index = 0):
    	return self.__internalStructure[_index]

    def dequeue(self):
    	if(self.__size > 0):
    		self.__size -= 1
    		return self.__internalStructure.pop(0)
    	else:
    		return None