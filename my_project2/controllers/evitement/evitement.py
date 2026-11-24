from controller import Robot

TIME_STEP = 64
MAX_SPEED = 6.28

robot = Robot()

# Moteurs
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# Capteurs de proximité (ps0 à ps7)
capteurs = []
for i in range(8):
    s = robot.getDevice(f'ps{i}')
    s.enable(TIME_STEP)
    capteurs.append(s)

while robot.step(TIME_STEP) != -1:
    valeurs = [s.getValue() for s in capteurs]

    obstacle_droite = valeurs[0] > 80 or valeurs[1] > 80
    obstacle_gauche = valeurs[6] > 80 or valeurs[7] > 80

    vitesse_g = 0.5 * MAX_SPEED
    vitesse_d = 0.5 * MAX_SPEED

    if obstacle_gauche:
        vitesse_g = 0.5 * MAX_SPEED
        vitesse_d = -0.5 * MAX_SPEED   # tourne à droite
    elif obstacle_droite:
        vitesse_g = -0.5 * MAX_SPEED
        vitesse_d = 0.5 * MAX_SPEED    # tourne à gauche

    left_motor.setVelocity(vitesse_g)
    right_motor.setVelocity(vitesse_d)