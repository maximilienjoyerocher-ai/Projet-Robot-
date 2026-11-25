from controller import Robot

TIME_STEP = 32
MAX_SPEED = 6.28

robot = Robot()

# Moteurs
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# Capteurs au sol (gs0 = gauche, gs1 = milieu, gs2 = droite)
gs = []
for i in range(3):
    s = robot.getDevice(f'gs{i}')
    s.enable(TIME_STEP)
    gs.append(s)

SEUIL = 500  # en dessous : on voit la ligne noire

while robot.step(TIME_STEP) != -1:
    valeurs = [s.getValue() for s in gs]
    print(valeurs)

    ligne_gauche = valeurs[0] < SEUIL
    ligne_milieu = valeurs[1] < SEUIL
    ligne_droite = valeurs[2] < SEUIL

    if ligne_milieu:
        # Ligne au centre : tout droit
        vitesse_g = MAX_SPEED
        vitesse_d = MAX_SPEED
    elif ligne_gauche:
        # Ligne à gauche : tourner à gauche
        vitesse_g = 0.3 * MAX_SPEED
        vitesse_d = MAX_SPEED
    elif ligne_droite:
        # Ligne à droite : tourner à droite
        vitesse_g = MAX_SPEED
        vitesse_d = 0.3 * MAX_SPEED
    else:
        # Ligne perdue : avancer doucement et chercher
        vitesse_g = 0.5 * MAX_SPEED
        vitesse_d = 0.5 * MAX_SPEED

    left_motor.setVelocity(vitesse_g)
    right_motor.setVelocity(vitesse_d)
