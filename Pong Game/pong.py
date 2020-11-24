import turtle
import random
import pygame

#Initialise game sounds
pygame.mixer.init()
bounceSound = pygame.mixer.Sound("bounce.wav")
paddleSound = pygame.mixer.Sound("paddle.wav")
pointSound = pygame.mixer.Sound("point.wav")

# Initialise the game window
window = turtle.Screen()
window.title("PONG")
window.bgcolor("black")
window.setup(width = 800, height = 600)
window.tracer(0)    # Prevents the window from updating so that it can be manually updated
                    # which allows us to run the game at a much faster refresh rate

#Initilaise the welcome pen object
welcomeText = turtle.Turtle()
welcomeText.color("white")
welcomeText.penup()
welcomeText.hideturtle()
welcomeText.sety(100)
welcomeText.speed(0)
welcomeText.write("Weclome to Pong\nW UP         S DOWN\nPress W to begin", align = "center", font=("8BIT WONDER", 16, "normal"), move = False)

#Initialise the score counters
paddleLeftScore = 0
paddleRightScore = 0

#Initialise the score tracking pen object
scoreTrackingText = turtle.Turtle()
scoreTrackingText.color("white")
scoreTrackingText.penup()
scoreTrackingText.hideturtle()
scoreTrackingText.sety(275)
scoreTrackingText.speed(0)
scoreTrackingText.write("             {}                                                    {}".format(paddleLeftScore, paddleRightScore), align = "center", font=("8BIT WONDER", 16, "normal"), move = False)

#Initialise the player names pen object
playerComputerText = turtle.Turtle()
playerComputerText.color("white")
playerComputerText.penup()
playerComputerText.hideturtle()
playerComputerText.sety(275)
playerComputerText.speed(0)
playerComputerText.write("Player                       ", align = "right", font=("8BIT WONDER", 16, "normal"), move = False)
playerComputerText.write("               Computer", align = "left", font=("8BIT WONDER", 16, "normal"), move = False)

# Paddle Left Properties
paddleLeft = turtle.Turtle()    # Initialises the paddle as a turle object
paddleLeft.speed(0)             # sets the speed to the maximum possible speed
paddleLeft.shape("square")
paddleLeft.color("white")
paddleLeft.penup()              # The object does not draw as it moves
paddleLeft.goto(-350, 0)        # Initialises the starting position of the left paddle on the left of the screen
paddleLeft.shapesize(stretch_wid=5, stretch_len=1)  # The default object is 20px's by 20px's here we stretch the width to make it wider
                                                    # and keep the length the default size of 20px's

# Paddle Right Properties
paddleRight = turtle.Turtle()       # Initialises the paddle as a turle object
paddleRight.speed(0)                # Sets the speed to the maximum possible speed
paddleRight.shape("square")
paddleRight.color("white")
paddleRight.penup()                 # The object does not draw as it moves
paddleRight.goto(350, 0)            # Initialises the starting position of the riight paddle on the right of the screen
paddleRight.shapesize(stretch_wid=5, stretch_len=1)     #The default object is 20px's by 20px's here we stretch the width to make it wider
                                                        #and keep the length the default size of 20px's

# Ball Properties
ball = turtle.Turtle()    # Initialises the ball as a turle object
ball.speed(0)             # Sets the speed to the maximum possible speed
ball.shape("square")
ball.color("white")
ball.penup()              # The object does not draw as it moves
ball.goto(0, 0)           # Initialises the starting position of the ball on the center of the screen in between the two paddles
ball.dx = 0.25            
ball.dy = 0.25

# FUNCTIONS
#----LEFT PADDLE FUNCTIONS----
# Paddle left move up function
def paddleLeftMoveUp():
    paddleLeftYCor = paddleLeft.ycor()  # Sets the Y co-ordinate to the current Y Co-oridnate of the paddle
    if paddleLeft.ycor() < 245 :
        paddleLeftYCor += 20            # Updates the Y co-ordinate to be 20 pixels up
    paddleLeft.sety(paddleLeftYCor)     # Sets the paddles Y co-ordinate to the new Y co-ordinate that was moved 20 pixels up 

# Paddle left move down function
def paddleLeftMoveDown():
    paddleLeftYCor = paddleLeft.ycor()  # Sets the Y co-ordinate to the current Y Co-oridnate of the paddle
    if paddleLeft.ycor() > -240 :
        paddleLeftYCor -= 20            # Updates the Y co-ordinate to be 20 pixels down
    paddleLeft.sety(paddleLeftYCor)     # Sets the paddles Y co-ordinate to the new Y co-ordinate that was moved 20 pixels down

#----RIGHT PADDLE FUNCTIONS----
#Paddle right move choice function
#Essentially the brain of the right paddle. My first AI :)
def paddleRightMoveChoice():
    if ball.dx < 0 and ball.xcor() > 0:     # If the ball is moving away from you and is still on your half of the field
        paddleRightMoveTowardsMiddle(0.15)  # move the paddle towards the middle 
    elif ball.dx < 0 and ball.xcor() < 0:       # If the ball is moving away from you and is in the left paddles half of the field
        paddleRightMoveTowardsBall(0.08, 180)   # Move towards the ball with a very slow movement speed and large follow trigger value
    
    if ball.dx > 0 and ball.xcor() < 0:                             # If the ball is moving towards you and is in the left paddles half of the field 
        paddleRightMoveTowardsBall(0.2, 180)  # slowly follow the balls Y co-ordinate with a large follow trigger
    elif ball.dx > 0 and ball.xcor() > 100 and ball.xcor() < 190:   # If the ball is moving towards you and is within a certain area on the right half of the field
        paddleRightMoveTowardsBall(0.35, 120)  # follow the balls Y Co-ordinate with reasonable speed and a smaller trigger value
    elif ball.dx > 0 and ball.xcor() > 0:                           # If the ball is moving towards you and the balls X co-ordinate is more than 190 pixels
        paddleRightMoveTowardsBall(0.45, 90)   # quickly move towards with the balls Y co-ordinate with a smaller follow trigger value

#Moves the right paddle to the middle of the field and once it reaches the middle it keeps it there
def paddleRightMoveTowardsMiddle(MovementSpeed):
    if paddleRight.ycor() > 0:
        paddleRightMoveDown(MovementSpeed)
    if paddleRight.ycor() < 0:
        paddleRightMoveUp(MovementSpeed)
    if paddleRight.ycor() == 0:
        paddleRight.sety(0)

#Compares the y Co-ordinates of the ball and the right paddle to move the paddle towards the ball
def paddleRightMoveTowardsBall(MovementSpeed, FollowTrigger):
    if ball.ycor() > paddleRight.ycor() + random.randint(0, FollowTrigger): #The follow trigger creates room for the paddle to make mistakes when tracking the ball.
        paddleRightMoveUp(MovementSpeed)                                    #If the random int is large enough the paddle will not track the ball Y co-ordinate for that game tick
    if ball.ycor() < paddleRight.ycor()  - random.randint(0, FollowTrigger):
        paddleRightMoveDown(MovementSpeed)

# Paddle right move up function
def paddleRightMoveUp(MovementSpeed):
    paddleRightYCor = paddleRight.ycor()    # Sets the Y co-ordinate to the current Y Co-oridnate of the paddle
    if paddleRight.ycor() < 245 :
        paddleRightYCor += MovementSpeed            # Updates the Y co-ordinate to be 20 pixels up
    paddleRight.sety(paddleRightYCor)       # Sets the paddles Y co-ordinate to the new Y co-ordinate that was moved 20 pixels up 

# Paddle right move down function
def paddleRightMoveDown(MovementSpeed):
    paddleRightYCor = paddleRight.ycor() # Sets the Y co-ordinate to the current Y Co-oridnate of the paddle
    if paddleRight.ycor() > -240 :
        paddleRightYCor -= MovementSpeed            # Updates the Y co-ordinate to be 20 pixels down
    paddleRight.sety(paddleRightYCor)    # Sets the paddles Y co-ordinate to the new Y co-ordinate that was moved 20 pixels down 

# KEYBOARD BINDINGS
window.listen()

#Paddle left key bindings
window.onkeypress(paddleLeftMoveUp, "w")
window.onkeypress(paddleLeftMoveDown, "s")

#Start screen before the game starts
while True:
    window.update()
    if paddleLeft.ycor() > 0 or paddleLeft.ycor() < 0:
        welcomeText.clear()
        break



#Main game loop
while True:
    window.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    #Calls  the right paddle to make a move
    paddleRightMoveChoice()

    #Screen Border Checking
    #Top of the screen
    if ball.ycor() > 285:
        bounceSound.play()
        ball.sety(285)
        ball.dy *= -1

    #Bottom of the sceen
    if ball.ycor() < -285:
        bounceSound.play() 
        ball.sety(-285)
        ball.dy *= -1

    #Right of the screen
    if ball.xcor() > 385:
        pointSound.play() 
        ball.goto(120, 0)
        ball.dx *= -1
        paddleLeftScore += 1
        scoreTrackingText.clear()
        scoreTrackingText.write("             {}                                                    {}".format(paddleLeftScore, paddleRightScore), align = "center", font=("8BIT WONDER", 16, "normal"), move = False)

    #Left of the sceen
    if ball.xcor() < -385:
        pointSound.play() 
        ball.goto(-120, 0)
        ball.dx *= -1
        paddleRightScore += 1
        scoreTrackingText.clear()
        scoreTrackingText.write("             {}                                                    {}".format(paddleLeftScore, paddleRightScore), align = "center", font=("8BIT WONDER", 16, "normal"), move = False)

    #Colissions between ball and paddles
    #Right paddle collisions
    if ball.xcor() > 340 and ball.xcor() < 350 and ball.ycor() < (paddleRight.ycor() + 50) and ball.ycor() > (paddleRight.ycor() - 50):
        paddleSound.play() 
        ball.setx(340)
        ball.dx *= -1

    #Left paddle collisions
    if (ball.xcor() < -340 and ball.xcor() > -350) and ball.ycor() < (paddleLeft.ycor() + 50) and ball.ycor() > (paddleLeft.ycor() - 50):
        paddleSound.play() 
        ball.setx(-340)
        ball.dx *= -1

