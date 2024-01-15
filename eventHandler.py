import pygame
import gameCore

def eventHandler(gameState):
    snake = gameState.snake
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                currentSnakeDirection = gameState.snake.getDirection()
                if currentSnakeDirection != gameCore.directionOpposites[gameCore.GridDirection.UP]:
                    gameState.snakeNextDirection = gameCore.GridDirection.UP
            if event.key == pygame.K_a:
                currentSnakeDirection = gameState.snake.getDirection()
                if currentSnakeDirection != gameCore.directionOpposites[gameCore.GridDirection.LEFT]:
                    gameState.snakeNextDirection = gameCore.GridDirection.LEFT
            if event.key == pygame.K_s:
                currentSnakeDirection = gameState.snake.getDirection()
                if currentSnakeDirection != gameCore.directionOpposites[gameCore.GridDirection.DOWN]:
                    gameState.snakeNextDirection = gameCore.GridDirection.DOWN
            if event.key == pygame.K_d:
                currentSnakeDirection = gameState.snake.getDirection()
                if currentSnakeDirection != gameCore.directionOpposites[gameCore.GridDirection.RIGHT]:
                    gameState.snakeNextDirection = gameCore.GridDirection.RIGHT
            if event.key == pygame.K_UP:
                currentSnakeDirection = gameState.snake.getDirection()
                if currentSnakeDirection != gameCore.directionOpposites[gameCore.GridDirection.UP]:
                    gameState.snakeNextDirection = gameCore.GridDirection.UP
            if event.key == pygame.K_LEFT:
                currentSnakeDirection = gameState.snake.getDirection()
                if currentSnakeDirection != gameCore.directionOpposites[gameCore.GridDirection.LEFT]:
                    gameState.snakeNextDirection = gameCore.GridDirection.LEFT
            if event.key == pygame.K_DOWN:
                currentSnakeDirection = gameState.snake.getDirection()
                if currentSnakeDirection != gameCore.directionOpposites[gameCore.GridDirection.DOWN]:
                    gameState.snakeNextDirection = gameCore.GridDirection.DOWN
            if event.key == pygame.K_RIGHT:
                currentSnakeDirection = gameState.snake.getDirection()
                if currentSnakeDirection != gameCore.directionOpposites[gameCore.GridDirection.RIGHT]:
                    gameState.snakeNextDirection = gameCore.GridDirection.RIGHT
            if event.key == pygame.K_SPACE and gameState.scene == gameCore.Scene.GAMEOVER:
                gameState.scene = gameCore.Scene.RESTART


