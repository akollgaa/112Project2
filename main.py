from cmu_graphics import *
from Graphics import Graphics
from Model import *
import time
import random

def onAppStart(app):
    app.width = 1024
    app.height = 768

###############################################################################
# Menu Screen
###############################################################################

def menuScreen_onScreenActivate(app):
    app.mx = 0
    app.my = 0
    app.hovering = False

def menuScreen_redrawAll(app):
    # Draw the mouse positions for debugging/testing
    drawLabel(f'({app.mx}, {app.my})', 30, 30)

    drawLabel('StarFox', app.width / 2, app.height / 4, size=80, bold=True)
    color = 'lightgreen' if app.hovering else 'white'
    drawRect(app.width / 3, app.height * 3/4, app.width / 3, 100, fill=color, border='lightgreen')
    textColor = 'white' if app.hovering else 'lightgreen'
    drawLabel('Play', app.width / 2, app.height * 3/4 + 50, size=20, fill=textColor)

def menuScreen_onMouseMove(app, mouseX, mouseY):
    app.mx = mouseX
    app.my = mouseY
    app.hovering = (app.width / 3 < mouseX < app.width * 2/3 and 
        app.height * 3/4 < mouseY < app.height * 3/4 + 100)

def menuScreen_onMousePress(app, mouseX, mouseY):
    if (app.width / 3 < mouseX < app.width * 2/3 and 
        app.height * 3/4 < mouseY < app.height * 3/4 + 100):
        setActiveScreen('playScreen')

###############################################################################
# Losing Screen
###############################################################################

def losingScreen_onScreenActivate(app):
    pass

def losingScreen_redrawAll(app):
    drawLabel('You lost! Out of Bounds', app.width / 2, app.height / 2, size=50)
    drawLabel("Press r to restart", app.width / 2, app.height / 2 + 40, size=40)

def losingScreen_onKeyPress(app, key):
    if key == 'r':
        setActiveScreen('menuScreen')

###############################################################################
# Play Screen
###############################################################################

def playScreen_onScreenActivate(app):
    app.direction = []
    app.move = []
    app.tilt = []
    app.xBounds = 40
    app.buildingDistance = 35
    app.stepsPerSecond = 25
    app.fpsCounter = 0
    app.fps = 0
    app.startTime = time.time()
    app.engine = Graphics(app.width, app.height)
    app.player = 0 # Index for the ship array
    app.endOfBuildings = 0
    app.thirdPerson = True
    addShapes(app)

def addShapes(app):
    # We must have a ship

    #app.engine.addShip(createRectangularPrism(1, 2, 1), 'Adam', 2, 4, 30)
    app.engine.addShip(shipModel(0.5), 'Adam', 2, 4, 30)
    # We must have a ground
    floor = [(-(app.xBounds + 25), 0, 500),
             (-(app.xBounds + 25), 0, -500),
             ((app.xBounds + 25), 0, -500),
             ((app.xBounds + 25), 0, 500)]
    ground = [(floor, 'green')]
    app.engine.addGround(ground)
    # Create a sequences of random heights of buildings
    for i in range(0, 20):
        height = random.randrange(20, 50)
        building1 = createBuilding(10, 10, height)
        height2 = random.randrange(20, 50)
        building2 = createBuilding(10, 10, height2)
        # Center of buildings are 20 units from middle
        app.engine.addShape(building1, [app.xBounds + 5, height / 2, app.buildingDistance * i])
        app.engine.addShape(building2, [-(app.xBounds + 5), height2 / 2, app.buildingDistance * i])
        app.endOfBuildings += 1

def playScreen_redrawAll(app):
    shapes, shapeIndexes, ground, groundIndexes = app.engine.render(app.thirdPerson)
    # First we must draw the ground
    allPoints = ground[groundIndexes[0]][0]
    colors = ground[groundIndexes[0]][1]
    indexes = ground[groundIndexes[0]][2]
    for index in indexes:
        # Based on the y position of the rendered ground we can create a new ground
        # that looks better because it is drawn in all directions
        y1 = allPoints[index][3]
        x1 = allPoints[index][2]
        y2 = allPoints[index][5]
        x2 = allPoints[index][4]
        m = (y2 - y1) / (x2 - x1)
        b = y1 - (m * x1)
        y1 = b
        y2 = m * app.width + b
        drawPolygon(0, y1, app.width, y2, app.width, app.height, 0, app.height, fill=colors[index], border='black')
    # Loops through a sorted list of the z-indexes
    for i in shapeIndexes:
        allPoints = shapes[i][0]
        colors = shapes[i][1]
        indexes = shapes[i][2]
        for index in indexes:
            drawPolygon(*allPoints[index], fill=colors[index], border='black')

    # Draw player health
    drawRect(20, app.height - 75, 75, 25, fill='white', border='black')
    width = 71 * (app.engine.ships[app.player].health / 30)
    if width <= 0: # We don't want a negative health bar
        width = 1
    drawRect(22, app.height - 73, width, 21, fill='red')

    # Draw player boost
    drawRect(100, app.height - 75, 75, 25, fill='white', border='black')
    width = 71 * (app.engine.ships[app.player].boostCooldown / 40)
    if width <= 0: # We don't want a negative boost bar
        width = 1
    drawRect(102, app.height - 73, width, 21, fill='blue')

    drawCameraStatus(app)

def drawCameraStatus(app):
    drawLabel(f'({app.engine.cameraPosition[0]:0.1f},\
{app.engine.cameraPosition[1]:0.1f},\
{app.engine.cameraPosition[2]:0.1f})', 50, 20)
    drawLabel(f'({app.engine.cameraOrientation[0]:0.1f},\
{app.engine.cameraOrientation[1]:0.1f},\
{app.engine.cameraOrientation[2]:0.1f})', 50, 50)
    drawLabel(f'({app.engine.fov:0.1f})', 50, 80)
    drawLabel(f'FPS: {app.fps}', 50, 110)
    drawLabel(f'({app.engine.ships[app.player].position[0]:0.1f},\
{app.engine.ships[app.player].position[1]:0.1f},\
{app.engine.ships[app.player].position[2]:0.1f})', 50, 140)

def playScreen_onKeyPress(app, key):
    if key == 'w' and app.thirdPerson:
        app.move.append('w')
        app.tilt.append('w')
    elif key == 's' and app.thirdPerson:
        app.move.append('s')
        app.tilt.append('s')
    elif key == 'd' and app.thirdPerson:
        app.move.append('d')
        app.tilt.append('d')
    elif key == 'a' and app.thirdPerson:
        app.move.append('a')
        app.tilt.append('a')
    elif key == 'space':
        laser = projectileModel(0.25)
        # Make sure the laser is not inside in the ship
        app.engine.addProjectile(laser, 8, 10, 2, app.engine.ships[app.player].position)
    elif key == 'm':
        setActiveScreen('menuScreen')
    elif key == 'f':
        app.engine.ships[app.player].startBoost()
    elif key == 'h':
        app.thirdPerson = not app.thirdPerson
        if app.thirdPerson:
            app.engine.cameraOrientation = (-15, 0, 0.5)
            app.engine.moveCameraPosition(0, 4, -12)
        else:
            app.move = []
            app.tilt = []
            app.engine.cameraPosition = app.engine.ships[app.player].position

def playScreen_onKeyRelease(app, key):
    if not app.thirdPerson: return
    if key == 'w' and 'w' in app.move and 'w' in app.tilt:
        app.move.remove('w')
        app.tilt.remove('w')
    elif key == 's' and 's' in app.move and 's' in app.tilt:
        app.move.remove('s')
        app.tilt.remove('s')
    elif key == 'd' and 'd' in app.move and 'd' in app.tilt:
        app.move.remove('d')
        app.tilt.remove('d')
    elif key == 'a' and 'a' in app.move and 'a' in app.tilt:
        app.move.remove('a')
        app.tilt.remove('a')

def playScreen_onMouseMove(app, mouseX, mouseY):
    if app.thirdPerson: return
    # Controlling camera orientation based on mouse position
    y = ((mouseX / app.width)) * 180 - 90
    r = app.engine.cameraOrientation[1]
    x = (1 - (mouseY / app.height)) * 180 - 90

    if x > 5: 
        if 'w' not in app.move: app.move.append('w')
    elif x < -5:
        if 's' not in app.move: app.move.append('s')
    else:
        if 'w' in app.move:
            app.move.remove('w')
        if 's' in app.move:
            app.move.remove('s')

    if y > 5: 
        if 'd' not in app.move: app.move.append('d')
        r -= 2 if r > -25 else 0
    elif y < -5:
        if 'a' not in app.move: app.move.append('a')
        r += 2 if r < 25 else 0
    else:
        if 'd' in app.move:
            app.move.remove('d')
        if 'a' in app.move:
            app.move.remove('a')
        if r > 0:
            r -= 2
        elif r < 0:
            r += 2

    app.engine.cameraOrientation = (x, r, y)

def playScreen_onMousePress(app, mx, my):
    if app.thirdPerson:
        app.engine.ships[app.player].startBarrelRoll()
    else: # Perform a barrel roll with the camera
        pass

def playScreen_onStep(app):

    #app.engine.ships[app.player].moveShip(0, 0, app.engine.ships[app.player].speed)
    
    app.engine.moveCameraPosition(0, 0, app.engine.ships[app.player].speed)
    # There is only one ground so we can index at 0
    app.engine.ground[0].updateGround(app.engine.ships[app.player].speed)

    rate = 1
    for move in app.move:
        if move == 'w': app.engine.moveCameraPosition(0, rate, 0)
        elif move == 's': app.engine.moveCameraPosition(0, -rate, 0)
        elif move == 'd': app.engine.moveCameraPosition(-rate, 0, 0)
        elif move == 'a': app.engine.moveCameraPosition(rate, 0, 0)

    # We check tilt seperately than move in order to account for max tilts
    rate = app.engine.ships[app.player].jerk
    for tilt in app.tilt:
        if tilt == 'w' and app.engine.ships[app.player].orientation[0] > -20: 
            app.engine.ships[app.player].tiltShip(-rate, 0, 0)
        elif tilt == 's' and app.engine.ships[app.player].orientation[0] < 20: 
            app.engine.ships[app.player].tiltShip(rate, 0, 0)
        elif tilt == 'd' and app.engine.ships[app.player].orientation[2] > -20: 
            app.engine.ships[app.player].tiltShip(0, 0, -rate)
        elif tilt == 'a' and app.engine.ships[app.player].orientation[2] < 20: 
            app.engine.ships[app.player].tiltShip(0, 0, rate)

    if 'w' not in app.tilt and app.engine.ships[app.player].orientation[0] < 0:
        app.engine.ships[app.player].tiltShip(rate, 0, 0)
    elif 's' not in app.tilt and app.engine.ships[app.player].orientation[0] > 0:
        app.engine.ships[app.player].tiltShip(-rate, 0, 0)
    if 'd' not in app.tilt and app.engine.ships[app.player].orientation[2] < 0:
        app.engine.ships[app.player].tiltShip(0, 0, rate)
    elif 'a' not in app.tilt and app.engine.ships[app.player].orientation[2] > 0:
        app.engine.ships[app.player].tiltShip(0, 0, -rate)

    # Check the FPS counter
    app.fpsCounter += 1
    if (time.time() - app.startTime) >= 1:
        app.fps = app.fpsCounter
        app.fpsCounter = 0
        app.startTime = time.time()

    # Most of what is below is updating shape data 
    if app.thirdPerson:
        app.engine.resetShipToCamera()
    else:
        app.engine.ships[app.player].position = app.engine.cameraPosition

    removed = app.engine.removeShapes()
    if removed: # If we removed shapes we then need to create a new building
        height = random.randrange(20, 50)
        building1 = createBuilding(10, 10, height)
        height2 = random.randrange(20, 50)
        building2 = createBuilding(10, 10, height2)
        app.engine.addShape(building1, (app.xBounds + 5, height / 2, app.buildingDistance * app.endOfBuildings))
        app.engine.addShape(building2, (-(app.xBounds + 5), height2 / 2, app.buildingDistance * app.endOfBuildings))
        app.endOfBuildings += 1

    for projectile in app.engine.projectiles:
        projectile.move()

    for enemy in app.engine.enemies:
        if enemy.shoot():
            laser = projectileModel(0.75)
            pos = (enemy.position[0], enemy.position[1], enemy.position[2] - 5)
            app.engine.addProjectile(laser, -6, 5, 2, pos)
        for projectile in app.engine.projectiles:
            if shapeCollision(enemy, projectile):
                enemy.health -= projectile.power
                app.engine.projectilesToRemove.add(projectile)
                enemy.hit += 1
        if enemy.hit >= 5:
            enemy.hit = 0
        enemy.moveToStandPosition()

    for projectile in app.engine.projectiles:
        if shapeCollision(app.engine.ships[app.player], projectile):
            app.engine.ships[app.player].health -= projectile.power
            app.engine.projectilesToRemove.add(projectile)
            app.engine.ships[app.player].hit += 1

    for obstacle in app.engine.obstacles:
        if obstacleCollision(app.engine.ships[app.player], obstacle):
            app.engine.ships[app.player].health -= obstacle.power
            app.engine.ships[app.player].hit += 1

    for powerup in app.engine.powerups:
        if powerupCollision(app.engine.ships[app.player], powerup):
            app.engine.ships[app.player].health += powerup.healthValue
            if app.engine.ships[app.player].health >= 30: # 30 is the max health
                app.engine.ships[app.player].health = 30
            app.engine.ships[app.player].heal += 1
            app.engine.powerupsToRemove.add(powerup)
        powerup.rotateOrbs()

    app.engine.removeProjectile()
    app.engine.removeEnemies()
    app.engine.removePowerUps()

    if app.engine.ships[app.player].hit >= 3:
        app.engine.ships[app.player].hit = 0
    if app.engine.ships[app.player].heal >= 3:
        app.engine.ships[app.player].heal = 0

    checkPlayerBounds(app)
    app.engine.ships[app.player].performBarrelRoll()
    app.engine.ships[app.player].performBoost()

    # Randomly create an enemy
    if random.randrange(0, 40) < 1:
        enemy = shipModel(2, True)
        x = random.randrange(-15, 15)
        y = random.randrange(10, 25)
        shipZ = app.engine.ships[app.player].position[2]
        shipY = app.engine.ships[app.player].position[1]
        app.engine.addEnemy(enemy, (0, shipY + 30, shipZ + 5), (x, y, shipZ + 150), 20, 5)

    # Randomly create an obstacle
    if random.randrange(0, 40) < 1:
        obstacle = createObstacle(5, 5, 40)
        x = random.randrange(-20, 20)
        app.engine.addObstacle(obstacle, (x, 20, app.buildingDistance * app.endOfBuildings), 5)

    # Randomly create a powerup
    if random.randrange(0, 40) < 1:
        orb = createRectangularPrism(1, 1, 1)
        x = random.randrange(-20, 20)
        y = random.randrange(5, 60)
        shipZ = app.engine.ships[app.player].position[2]
        app.engine.addPowerUp(orb, (x, y, shipZ + 100), 10)

def distance(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)**0.5

# shape2 must be a projectile
def shapeCollision(shape1, shape2):
    if ((type(shape1) == Ship and shape2.speed > 0) or 
        type(shape1) == Enemy and shape2.speed < 0):
        return False
    isProjectileInfront = shape2.midpoint[2] + shape2.speed >= shape1.midpoint[2]
    if shape2.speed < 0:
        isProjectileInfront = shape2.midpoint[2] + shape2.speed <= shape1.midpoint[2]
    if (shape1.midpoint[0] - shape1.radius < shape2.midpoint[0] < shape1.midpoint[0] + shape1.radius and 
        shape1.midpoint[1] - shape1.radius < shape2.midpoint[1] < shape1.midpoint[1] + shape1.radius and 
        isProjectileInfront):
        return True

# shape2 must be a obstacle
def obstacleCollision(shape1, shape2):
    if (shape2.midpoint[0] - shape2.radius < shape1.midpoint[0] < shape2.midpoint[0] + shape2.radius and
        shape1.midpoint[2] >= shape2.midpoint[2] - shape2.radius and
        shape1.midpoint[1] < shape2.height):
        return True
    
# shape2 must be a powerup
def powerupCollision(shape1, shape2):
    if (shape2.midpoint[0] - shape2.radius < shape1.midpoint[0] < shape2.midpoint[0] + shape2.radius and
        shape2.midpoint[1] - shape2.radius < shape1.midpoint[1] < shape2.midpoint[1] + shape2.radius and
        shape2.midpoint[2] < shape1.midpoint[2]):
        return True

def checkPlayerBounds(app):
    player = app.engine.ships[app.player]
    if (player.position[0] > app.xBounds or player.position[0] < -app.xBounds or player.position[1] < 0 or player.position[1] > 80):
        setActiveScreen('losingScreen')

def main():
    runAppWithScreens(initialScreen='menuScreen', height=768, width=1024)

main()