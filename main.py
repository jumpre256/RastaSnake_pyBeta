import pygame
import gameCore, gameProperties
import eventHandler
from gameCore import Field, FieldBackground
from gameObjects import SnakeSegment, SnakeHead

pygame.init()

window = pygame.display.set_mode((gameCore.DISPLAY_WIDTH, gameCore.DISPLAY_HEIGHT));
pygame.display.set_caption(gameProperties.GAME_CAPTION)
clock = pygame.time.Clock()

class GameState():

    def __init__(self):
        self.scene = gameCore.Scene.GAMEPLAY
        self.snakeSpeed = 4
        self.snakeNextDirection = gameCore.GridDirection.RIGHT
        self.snake = SnakeHead(52, 52, self.snakeSpeed, gameCore.Color.rasta_head_green, 3)
        self.snakeDead = False
    
    def getScore(self):
        return self.snake.getScore()
        

def initiateGame():
    Field.destroyFruitList()
    Field.generateFruit(5, 0, 1)
    return GameState()

def main():
    FieldBackground._init()
    FieldBackground.window = window
    FieldBackground.setHighlightSquareColor(gameCore.Color.squaresHighlightColor)
    Field.window = window
    gameState = initiateGame()

    while True:

        if gameState.scene == gameCore.Scene.RESTART:
            gameState = initiateGame()

        eventHandler.eventHandler(gameState)

        gameState.snake.setNextDirection(gameState.snakeNextDirection)
    
        if gameState.snakeDead == True and gameState.scene == gameCore.Scene.GAMEPLAY:
            gameState.scene = gameCore.Scene.GAMEOVER

        if gameState.scene == gameCore.Scene.GAMEPLAY:
            gameState.snake.setNextDirection(gameState.snakeNextDirection)
            gameState.snakeDead = gameState.snake.tick()
            window.fill(gameCore.Color.gameplay_bg_color)
            FieldBackground.drawBackground()
            Field.draw()
            gameState.snake.draw(window)
            gameCore.FontHandler.displayText_topleft(window, "Score: " + str(gameState.getScore()), 0, 0, 38, gameCore.Color.trueBlack)
        else:
            window.fill(gameCore.Color.gameover_bg_color)
            gameCore.FontHandler.displayText_center(window, "GAME OVER", gameCore.DISPLAY_WIDTH/2, 120, 64, gameCore.Color.trueBlack)
            gameCore.FontHandler.displayText_center(window, "Score: " + str(gameState.getScore()), gameCore.DISPLAY_WIDTH/2, gameCore.DISPLAY_HEIGHT/2, 38, gameCore.Color.trueBlack)
            gameCore.FontHandler.displayText_center(window, "(press space to play again)", gameCore.DISPLAY_WIDTH/2, (gameCore.DISPLAY_HEIGHT/2) + 120, 38, gameCore.Color.trueBlack)

        pygame.display.update()
        clock.tick(gameCore.FPS)


if __name__ == "__main__":
    main()
