import random
import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model 
import pygame, time
import sys


pygame.init()

def inFrame(lst):
	if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility>0.6 and lst[16].visibility>0.6:
		return True 
	return False

class Text():
  def __init__(self,text_color, x,y,size,font,text = '',):
    self.text_color = text_color
    self.x = x
    self.y = y
    self.size = size
    self.font = font
    self.text = text
  
  def draw(self,win,outline=None):
    font = pygame.font.Font(self.font, self.size)
    text = font.render(self.text, True, self.text_color)
    win.blit(text, (self.x, self.y))
  
class Button():
    def __init__(self, color,text_color, x,y,width,height,font_size,font, text=''):
        self.color = color
        self.text_color = text_color
        self.font_size = font_size
        self.font = font
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.Font(self.font, self.font_size)
            text = font.render(self.text, 1, self.text_color)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

    def check_click(self):
      pos = pygame.mouse.get_pos()
      if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height and pygame.mouse.get_pressed()[0]:
                return True
      return False

def home_page():
  global page

  start_time = time.time()
  while True:
    for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              break
    window.blit(bg4, (0,0))
    window.blit(pygame.transform.scale(title_with_man,(800,800)), (200,-150))

    button_start = Button("#000000","#ffffff",270, 500, 300,100,70,marcellus, text="Start")
    button_start.draw(window,"#ffffff")
    button_quit = Button("#000000","#ffffff",670, 500, 300,100,70,marcellus, text="Quit")
    button_quit.draw(window,"#ffffff")

    if button_start.check_click():
      page = "start"
      break
    if button_quit.check_click() and time.time() - start_time > 4:
      pygame.display.quit()
      pygame.quit()
      sys.exit()

def start_page():

  

  global page

  for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break


  window.blit(bg1, (0,0))
  high_score_text = Text("#1c1e38",10,10,35,gow,f"HighScore")
  high_score_number = Text("#1c1e38",10,50,50,gow,f"{high_score}")
  high_score_text.draw(window)
  high_score_number.draw(window)

  lst = []
  success, img = cap.read()
  img = cv2.flip(img, 1) 
  imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  res = holis.process(imgRGB)
  imgRGB = np.rot90(imgRGB)
  frame = pygame.surfarray.make_surface(imgRGB).convert()
  frame = pygame.transform.flip(frame, True, False)
  window.blit(frame, (220, 0))
  

  window.blit(title, (335,335))
  button_start = Button("#34eb5b","#000000",1030, 200, 200,70,50,marcellus, text="Start")
  button_start.draw(window,"#000000")
  button_back = Button((255,0,0),"#000000",1030, 300, 200,70,50,marcellus, text="Back")
  button_back.draw(window, (0,0,0))
  if button_start.check_click():
    page = "game"
  if button_back.check_click():
    page = "home"

  if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
      for i in res.pose_landmarks.landmark:
        lst.append(i.x - res.pose_landmarks.landmark[0].x)
        lst.append(i.y - res.pose_landmarks.landmark[0].y)

      lst = np.array(lst).reshape(1,-1)

      p = model.predict(lst)
      pred = label[np.argmax(p)]
      print(pred)

def game_page():

  global page,high_score


  start_time = time.time()
  current_time = time.time()
  given_time = 30
  total_time = start_time + given_time
  score = 0
  increment = 1
  level_completed = False
  level_name = label[random.randint(0, len(label) -1)]
  previous_level_name = ""

  while current_time < total_time:
    current_time = time.time()
    remaining_time = int(total_time - current_time)
    total_time = start_time + given_time

    

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
          break
  

    window.blit(bg1, (0,0))

    score_text = Text("#f2e30f",1040,5,50,silkscreen,f"Score:").draw(window)
    score_number = Text("#f2e30f",1150,50,60,silkscreen,f"{score}").draw(window)
    level_name_text = Text("#ffffff",150,570,70,gow,f"{level_name}").draw(window)
    window.blit(poseImages[level_name],(800,500))


    window.blit(clockimg, (10,10))
    remaining_time_text = Text("#1c1e38",100,10, 50,silkscreen,f"{remaining_time}").draw(window)

    lst = []
    success, img = cap.read()
    img = cv2.flip(img, 1) 
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = holis.process(imgRGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    window.blit(frame, (220, 0))


    button_quit = Button((255,0,0),"#000000",1030, 300, 200,70,50,marcellus, text="QUIT")
    button_quit.draw(window, (0,0,0))
    if button_quit.check_click():
      break

    if level_completed:
      previous_level_name = level_name
      while(level_name == previous_level_name) and level_name == "kicking":
        level_name = label[random.randint(0, len(label) -1)]
        level_completed = False


      
    
    if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
      for i in res.pose_landmarks.landmark:
        lst.append(i.x - res.pose_landmarks.landmark[0].x)
        lst.append(i.y - res.pose_landmarks.landmark[0].y)

      lst = np.array(lst).reshape(1,-1)

      p = model.predict(lst)
      pred = label[np.argmax(p)]
      print(pred)
      if pred == level_name:
        given_time += increment
        score += 1
        level_completed = True
    else:
      notvisible_text = Text((255,0,0),140,450,40,silkscreen,"! Make Sure your whole body is visible")
      notvisible_text.draw(window)
      window.blit(notvisible,(0,230))
      pred = None

    high_score = max(high_score,score)
    pygame.display.update()
    clock.tick(fps)
  end_game(score, current_time - start_time)

def end_game(score, time_taken):
  
  global page

  start_time = time.time()
  gotime = 1.5
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
          break
    
    window.blit(bg2, (0,0))

    if (time.time() - start_time < gotime):
      window.blit(pygame.transform.scale(gameover,(600,400)), (300, 100))
    else:
      window.blit(pygame.transform.scale(title,(800,800)), (250,-200))
      score_text = Text("#252945",100,300,50,silkscreen,f"Score: {score}").draw(window)
      time_taken_text = Text("#252945",600,300,50,silkscreen,f"Time Played: {int(time_taken)} s ").draw(window)
      high_score_text = Text("#252945",100,400,50,silkscreen,f"HighScore: {high_score}").draw(window)
      time_per_move_text = Text("#252945",600,400,50,silkscreen,f"Time / Move: {round(int(time_taken) if score == 0 else time_taken/(score + 1),2)} s").draw(window)

      button_exit = Button("#e32938","#000000",620, 550, 430,100,60,marcellus, text="Main Menu")
      button_exit.draw(window, (0,0,0))
      button_play_again = Button("#49e68a","#000000",220, 550, 430,100,60,marcellus, text="Play Again")
      button_play_again.draw(window,"#000000")
      if button_play_again.check_click():
        page = "start"
        break
      if button_exit.check_click():
        page = "home"
        break
      


    pygame.display.update()
    clock.tick(fps)

  

#fonts
marcellus = "Fonts\Marcellus-Regular.ttf"
silkscreen = "Fonts\Silkscreen-Regular.ttf"
nabla = "Fonts\\Nabla.ttf"
gow = "Fonts\god-of-war.ttf"

##button area


#/////


#important variables do not touch
model  = load_model("model.h5")
label = np.load("labels.npy")
holistic = mp.solutions.pose
holis = holistic.Pose()
drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3,800)
cap.set(4,100)

width, height = 1240 , 700
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hole in the Screen")
fps = 30
clock = pygame.time.Clock()
#/////////


#Images
bg1 = pygame.image.load('Background_Images\Background1.png').convert_alpha()
bg1 = pygame.transform.scale(bg1,(width,height))
bg2 = pygame.image.load('Background_Images\Background2.png').convert_alpha()
bg2 = pygame.transform.scale(bg2,(width,height))
bg3 = pygame.image.load('Background_Images\Background3.png').convert_alpha()
bg3 = pygame.transform.scale(bg3,(width,height))
bg4 = pygame.image.load('Background_Images\Background4.png').convert_alpha()
bg4 = pygame.transform.scale(bg4,(width,height))
notvisible = pygame.image.load(r'Images\not_visible.png').convert_alpha()
notvisible = pygame.transform.scale(notvisible, (220,220))
clockimg = pygame.image.load(r'Images\clock.png').convert_alpha()
clockimg = pygame.transform.scale(clockimg, (70,70))
title = pygame.image.load(r'Images\title.png').convert_alpha()
title = pygame.transform.scale(title, (600,600))
title_with_man = pygame.image.load(r'Images\title_with_man.png').convert_alpha()
poseImages = {i: pygame.transform.scale(pygame.image.load(f"poseImages\{i}.png").convert_alpha(),(200,200)) for i in label}
gameover = pygame.image.load("Images\gameover3.png").convert_alpha()



#game variables
page = "home"
high_score = 10

#main loop
while True:

  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
  if page == "home":
    home_page(time.time())
  elif page == "start":
    start_page()
  elif page == "game":
    game_page()

  

  pygame.display.update()
  clock.tick(fps)
