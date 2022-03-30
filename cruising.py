cruising = False
speed = 40 #mph
def cruiseButton():
    pass

# toggle
def cruiseMain():
    if cruiseButton() and not cruising:
        cruising = True
        speed = get_speed()
    elif cruising:
        setSpeed(speed)