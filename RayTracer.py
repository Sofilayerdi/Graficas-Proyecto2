import pygame
import random
from gl import *
from BMP_Writer import GenerateBMP
from model import Model
from OBJLoader import OBJ
from figures import *
from lights import *
from material import REFLECTIVE, OPAQUE, TRANSPARENT, Material
from BMPTexture import BMPTexture

width = 250
height = 250

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.envMap = BMPTexture("fondo.bmp")

cuarzo = Material(diffuse=[1.0, 0.6, 0.8], spec=120, ks=0.5, matType=OPAQUE)
table = Material(diffuse=[0.55, 0.35, 0.2], spec=0.3, ks=0.1, matType=OPAQUE)
yellow = Material(diffuse=[1.0, 1.0, 0.2], spec=16, ks=0.1, matType=OPAQUE)
tray = Material(diffuse=[0.95, 0.95, 0.9], spec=0.8, ks=0.2, matType=OPAQUE)
grapes = Material(diffuse=[0.4, 0.08, 0.25], spec=64, ks=0.6, matType=OPAQUE)
grapesG = Material(diffuse=[0.35, 0.45, 0.15], spec=64, ks=0.6, matType=OPAQUE)

apple = Material(diffuse=[0.8, 0.1, 0.1], spec=0.6, ks=0.1, matType=OPAQUE)
corcho = Material(diffuse=[0.6, 0.45, 0.25], spec=0.3, ks=0.1, matType=OPAQUE)


silver = Material(diffuse= [0.9, 0.9, 0.9], spec = 150, ks = 0.92, matType = REFLECTIVE)
gold = Material(diffuse = [1.0, 0.8, 0.2], spec = 120, ks = 0.85, matType = REFLECTIVE)
emerald = Material(diffuse=[0.0, 0.6, 0.3], spec=100, ks=0.8, matType=REFLECTIVE)

bottleGold = Material(diffuse=[0.8, 0.65, 0.1], spec=1.0, ks=1.0, matType=REFLECTIVE)



zafiro = Material(diffuse = [1.0, 0.7, 0.85], ior = 1.78, matType= TRANSPARENT)
water = Material(diffuse = [0.9, 0.95, 1.0], ior = 1.33, matType= TRANSPARENT)
ruby = Material(diffuse=[1.0, 0.2, 0.3], ior=1.77, matType=TRANSPARENT)

brick = Material(diffuse = [1, 0, 0])
grass = Material(diffuse = [0, 1, 0], spec = 32, ks = 0.4)
mirror = Material(diffuse= [0.9, 0.9, 0.9], spec = 128, ks = 0.5, matType = REFLECTIVE)
blueMirror = Material(diffuse = [0, 0, 0.9], spec = 64, ks = 0.2, matType = REFLECTIVE)

bottleGreen = Material(diffuse=[0.15, 0.45, 0.2], spec=1.0, ks=0.9, ior=1.5, matType=TRANSPARENT)





rend.scene.append(Plane(position=[0, -3, 0], normal=[0, 1, 0], material=table))

# rend.scene.append(Sphere(position=[-1.7, -1, -8], radius=1.3, material=bottleGold))
# rend.scene.append(Cone(position=[-1.7, 1.5, -8], height=5, radius=1.2, material=bottleGreen))
# rend.scene.append(Toroide(position=[-1.7, 3.6, -8], R=0.3, r=0.16, material= corcho))

rend.scene.append(Toroide(position=[-0.2, -1.4, -7], R=0.3, r=0.75, material= apple))
rend.scene.append(Cilindro(position=[-0.2, -1, -7], height=2, radius=0.05, material= corcho))



#rend.scene.append(Disk(position=[2, -0.8, -8], normal = [-1, 1, 0.5], radius= 1.5, material = tray))

# rend.scene.append(Elipsoide(position=[1, -0.5, -6], radius=[0.15, 0.3, 0.15], material=grapes))
# rend.scene.append(Elipsoide(position=[1, -0.1, -6], radius=[0.15, 0.3, 0.15], material=grapes))
# rend.scene.append(Elipsoide(position=[0.8, -0.5, -6], radius=[0.15, 0.3, 0.15], material=grapes))
# rend.scene.append(Elipsoide(position=[0.9, -0.9, -6], radius=[0.15, 0.3, 0.15], material=grapes))
# rend.scene.append(Elipsoide(position=[1.2, -0.5, -6], radius=[0.15, 0.3, 0.15], material=grapes))
# rend.scene.append(Elipsoide(position=[1.2, -0.8, -6], radius=[0.15, 0.3, 0.15], material=grapes))

# rend.scene.append(Elipsoide(position=[1.0, -1.2, -6], radius=[0.15, 0.3, 0.15], material=grapes))
# rend.scene.append(Elipsoide(position=[0.9, -1.4, -6], radius=[0.15, 0.3, 0.15], material=grapes))
# rend.scene.append(Elipsoide(position=[0.8, -1.6, -6], radius=[0.15, 0.3, 0.15], material=grapes))
# rend.scene.append(Elipsoide(position=[0.9, -1.8, -6], radius=[0.15, 0.3, 0.15], material=grapes))
# rend.scene.append(Elipsoide(position=[1.1, -1.9, -6], radius=[0.15, 0.3, 0.15], material=grapes))
# rend.scene.append(Elipsoide(position=[1.3, -2.1, -6], radius=[0.12, 0.25, 0.12], material=grapes))

# rend.scene.append(Elipsoide(position=[0.7, -0.3, -6], radius=[0.14, 0.28, 0.14], material=grapes))
# rend.scene.append(Elipsoide(position=[1.3, -0.3, -6], radius=[0.14, 0.28, 0.14], material=grapes))
# rend.scene.append(Elipsoide(position=[0.8, -0.8, -6.1], radius=[0.15, 0.3, 0.15], material=grapes))
# rend.scene.append(Elipsoide(position=[1.25, -0.9, -5.9], radius=[0.15, 0.3, 0.15], material=grapes))
# rend.scene.append(Elipsoide(position=[0.75, -1.2, -6.1], radius=[0.14, 0.28, 0.14], material=grapes))
# rend.scene.append(Elipsoide(position=[1.35, -1.3, -5.9], radius=[0.14, 0.28, 0.14], material=grapes))
# rend.scene.append(Elipsoide(position=[0.85, -1.6, -6.1], radius=[0.13, 0.26, 0.13], material=grapes))
# rend.scene.append(Elipsoide(position=[1.25, -1.7, -5.9], radius=[0.13, 0.26, 0.13], material=grapes))
# rend.scene.append(Elipsoide(position=[1.0, -2.0, -6], radius=[0.12, 0.25, 0.12], material=grapes))
# rend.scene.append(Elipsoide(position=[1.5, -2.0, -6], radius=[0.12, 0.25, 0.12], material=grapes))
# rend.scene.append(Elipsoide(position=[1.5, -0.3, -6], radius=[0.12, 0.25, 0.12], material=grapes))
# rend.scene.append(Elipsoide(position=[1.3, 0, -6], radius=[0.12, 0.25, 0.12], material=grapes))
# rend.scene.append(Elipsoide(position=[1.5, -0.8, -6], radius=[0.12, 0.25, 0.12], material=grapes))
# rend.scene.append(Elipsoide(position=[1.8, -0.7, -6], radius=[0.12, 0.25, 0.12], material=grapes))
# rend.scene.append(Elipsoide(position=[1.6, -0.6, -6], radius=[0.12, 0.25, 0.12], material=grapes))
# rend.scene.append(Elipsoide(position=[1.6, -0.3, -6], radius=[0.12, 0.25, 0.12], material=grapes))
# rend.scene.append(Elipsoide(position=[1.6, -1, -6], radius=[0.12, 0.25, 0.12], material=grapes))
# rend.scene.append(Elipsoide(position=[1.5, -1.6, -6], radius=[0.12, 0.25, 0.12], material=grapes))
# rend.scene.append(Elipsoide(position=[1.6, -1.4, -6], radius=[0.12, 0.25, 0.12], material=grapes))
# rend.scene.append(Elipsoide(position=[1.15, -1.35, -6], radius=[0.12, 0.25, 0.12], material=grapes))
# rend.scene.append(Elipsoide(position=[0.6, -1, -6], radius=[0.12, 0.25, 0.12], material=grapes))





# rend.scene.append(Cilindro(position=[-2, -1.4, -6], height=1.5, radius=0.75, material= gold))
# rend.scene.append(Elipsoide(position=[-1, 0.5, -6], radius=[0.5, 0.2, 0.5], material= emerald))

# rend.scene.append(Cilindro(position=[2, -1.4, -6], height=2, radius=0.4, material= zafiro))
# rend.scene.append(Elipsoide(position=[1, 0.5, -6], radius=[0.4, 0.3, 0.4], material= ruby))

rend.lights.append(AmbientLight(intensity=0.35))
rend.lights.append(PointLight(position=[0, 3, -4], intensity=0.6))
rend.lights.append(PointLight(position=[2, 1, -3], intensity=0.3))
rend.lights.append(PointLight(position=[-2, 0, -5], intensity=0.3))
#rend.lights.append(PointLight(position=[0, 0, -9], intensity=0.5))
rend.lights.append(DirectionalLight(direction=[1, -1, -1], intensity=0.2))

#rend.lights.append(SpotLight(intensity= 1.2, position = [0, 2, -4], direction = [0, -1, 0]))

                   

# rend.glRender()

isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                rend.camera.translation[0] += 0.1
            elif event.key == pygame.K_LEFT:
                rend.camera.translation[0] -= 0.1

            elif event.key == pygame.K_UP:
                rend.camera.translation[1] += 0.1
            elif event.key == pygame.K_DOWN:
                rend.camera.translation[1] -= 0.1


            elif event.key == pygame.K_q:
                rend.camera.translation[2] += 2 * deltaTime  
            elif event.key == pygame.K_e:
                rend.camera.translation[2] -= 2 * deltaTime


            elif event.key == pygame.K_a:
                rend.camera.rotation[1] -= 45 * deltaTime
            elif event.key == pygame.K_d:
                rend.camera.rotation[1] += 45 * deltaTime
            elif event.key == pygame.K_w:
                rend.camera.rotation[0] -= 45 * deltaTime
            elif event.key == pygame.K_s:
                rend.camera.rotation[0] += 45 * deltaTime
        

    

    #rend.glClearBackground()
    rend.glRender()


GenerateBMP("output.bmp", width, height, 3, rend.frameBuffer)

pygame.quit()
