import sys
import pygame
import random

pygame.init()

# Scenes
scene = 0

# Load images
slime = pygame.image.load("phone1.png")
slime2 = pygame.image.load("phone2.png")
slime3 = pygame.image.load("mp3.png")
slimes = [slime, slime2, slime3]
rSlime = pygame.transform.flip(slime, True, False)

#should be an hourglass
powerup_img = pygame.image.load("powerup.png")

# Screen setup
width = 600
height = 400
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Don't Let the Slime Splat!")
pygame.display.set_icon(slime)

# Colors
green = (74, 93, 35)
orange = (243, 121, 78)
black = (0, 0, 0)

# Fonts and Titles
titleY = 100
titleFont = pygame.font.SysFont("Arial", 65)
slimeTitle = titleFont.render("Screen Saver", False, green)
gameOverTitle = titleFont.render("Cracked", False, green)

playY = 300
btnMargin = 10
btnFont = pygame.font.SysFont("Arial", 30)
playWord = btnFont.render("PLAY", False, green)
quitWord = btnFont.render("QUIT", False, green)
restartWord = btnFont.render("RESTART", False, orange)

playBtn = pygame.draw.rect(screen, black, (0, 0, 0, 0))
quitBtn = pygame.draw.rect(screen, black, (0, 0, 0, 0))
restartBtn = pygame.draw.rect(screen, black, (0, 0, 0, 0))

# Slime Setup
numOfThings = 7
slimeImage = []
slimeX = []
slimeY = []
slimeSpeed = []
baseSpeed = .01
speedMulti = 1.2

for _ in range(numOfThings):
    slimeImage.append(random.choice(slimes))
    slimeX.append(random.randint(0, width - slime.get_width()))
    slimeY.append(0 - random.randint(slime.get_height(), slime.get_height() * 2))
    slimeSpeed.append(baseSpeed + random.random() / 100)

# Power-Up Setup
powerupX = -1000
powerupY = -1000
powerup_active = False
powerup_visible = False
powerup_timer = 0
next_powerup_time = pygame.time.get_ticks() + 10000

# Game loop
gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    if pygame.mouse.get_pressed()[0]:
        coords = pygame.mouse.get_pos()
        if scene == 0:
            if pygame.Rect.collidepoint(playBtn, coords):
                scene = 1
        elif scene == 1:
            for i in range(numOfThings):
                if slimeX[i] <= coords[0] <= slimeX[i] + slime.get_width() and slimeY[i] <= coords[1] <= slimeY[i] + slime.get_height():
                    slimeImage[i] = random.choice(slimes)
                    slimeX[i] = random.randint(0, width - slime.get_width())
                    slimeY[i] = 0 - random.randint(slime.get_height(), slime.get_height() * 2)
                    slimeSpeed[i] *= speedMulti

            # Clicked on power-up
            if powerup_visible and not powerup_active:
                if powerupX <= coords[0] <= powerupX + powerup_img.get_width() and powerupY <= coords[1] <= powerupY + powerup_img.get_height():
                    for i in range(numOfThings):
                        slimeSpeed[i] *= 0.5
                    powerup_active = True
                    powerup_visible = False
                    powerup_timer = pygame.time.get_ticks()
                    powerupX = -1000
                    powerupY = -1000

        elif scene == 2:
            if pygame.Rect.collidepoint(quitBtn, coords):
                gameOver = True
            if pygame.Rect.collidepoint(restartBtn, coords):
                for i in range(numOfThings):
                    slimeImage[i] = random.choice(slimes)
                    slimeX[i] = random.randint(0, width - slime.get_width())
                    slimeY[i] = 0 - random.randint(slime.get_height(), slime.get_height() * 2)
                    slimeSpeed[i] = baseSpeed + random.random() / 100
                scene = 0
                powerup_active = False
                powerup_visible = False
                next_powerup_time = pygame.time.get_ticks() + 10000

    # Game update
    if scene == 1:
        current_time = pygame.time.get_ticks()

        # Update slimes
        for i in range(numOfThings):
            slimeY[i] += slimeSpeed[i]
            if slimeY[i] + slime.get_height() > height:
                scene = 2

        # Spawn power-up
        if not powerup_visible and not powerup_active and current_time >= next_powerup_time:
            powerupX = random.randint(0, width - powerup_img.get_width())
            powerupY = random.randint(100, height - 100)
            powerup_visible = True

        # End power-up effect after 7 seconds
        if powerup_active and current_time - powerup_timer >= 7000:
            for i in range(numOfThings):
                slimeSpeed[i] *= 2
            powerup_active = False
            next_powerup_time = current_time + 10000

    # Drawing
    if scene == 0:
        screen.fill(orange)
        screen.blit(slimeTitle, ((width / 2) - (slimeTitle.get_width() / 2), titleY))
        screen.blit(slime, ((width / 2) - (slimeTitle.get_width() / 2) - slime.get_width(), titleY + (slimeTitle.get_height() - slime.get_height())))
        screen.blit(rSlime, ((width / 2) + (slimeTitle.get_width() / 2), titleY + (slimeTitle.get_height() - slime.get_height())))

        coords = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(playBtn, coords):
            playBtn = pygame.draw.rect(screen, green, ((width / 2) - (playWord.get_width() / 2) - btnMargin, playY - btnMargin, playWord.get_width() + (btnMargin * 2), playWord.get_height() + (btnMargin * 2)), 0)
        else:
            playBtn = pygame.draw.rect(screen, black, ((width / 2) - (playWord.get_width() / 2) - btnMargin, playY - btnMargin, playWord.get_width() + (btnMargin * 2), playWord.get_height() + (btnMargin * 2)), 0)
        screen.blit(playWord, ((width / 2) - (playWord.get_width() / 2), playY))

    elif scene == 1:
        screen.fill(green)
        for i in range(numOfThings):
            screen.blit(slimeImage[i], (slimeX[i], slimeY[i]))
        if powerup_visible:
            screen.blit(powerup_img, (powerupX, powerupY))

    else:
        screen.fill(black)
        screen.blit(gameOverTitle, ((width / 2) - (gameOverTitle.get_width() / 2), titleY))
        screen.blit(slime, ((width / 2) - (gameOverTitle.get_width() / 2) - slime.get_width(), titleY + (gameOverTitle.get_height() - slime.get_height())))
        screen.blit(rSlime, ((width / 2) + (gameOverTitle.get_width() / 2), titleY + (gameOverTitle.get_height() - slime.get_height())))

        coords = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(quitBtn, coords):
            quitBtn = pygame.draw.rect(screen, green, ((width / 4) - (quitWord.get_width() / 2) - btnMargin, playY - btnMargin, quitWord.get_width() + (btnMargin * 2), quitWord.get_height() + (btnMargin * 2)), 0)
        else:
            quitBtn = pygame.draw.rect(screen, orange, ((width / 4) - (quitWord.get_width() / 2) - btnMargin, playY - btnMargin, quitWord.get_width() + (btnMargin * 2), quitWord.get_height() + (btnMargin * 2)), 0)
        screen.blit(quitWord, ((width / 4) - (quitWord.get_width() / 2), playY))

        if pygame.Rect.collidepoint(restartBtn, coords):
            restartBtn = pygame.draw.rect(screen, orange, ((width * .75) - (restartWord.get_width() / 2) - btnMargin, playY - btnMargin, restartWord.get_width() + (btnMargin * 2), restartWord.get_height() + (btnMargin * 2)), 0)
        else:
            restartBtn = pygame.draw.rect(screen, green, ((width * .75) - (restartWord.get_width() / 2) - btnMargin, playY - btnMargin, restartWord.get_width() + (btnMargin * 2), restartWord.get_height() + (btnMargin * 2)), 0)
        screen.blit(restartWord, ((width * .75) - (restartWord.get_width() / 2), playY))

    pygame.display.flip()

pygame.quit()
