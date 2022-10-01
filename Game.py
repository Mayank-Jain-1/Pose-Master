import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model 
import pygame, time

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
    text = font.render(self.text, 1, self.text_color)
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

def start_page():

  

  global page

  for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break


  window.blit(bg1, (0,0))
  high_score_text = Text("#f2e30f",10,10,40,silkscreen,f"HighScore:")
  high_score_number = Text("#f2e30f",10,50,50,silkscreen,f"{high_score}")
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
  
  button_start = Button("#34eb5b","#000000",1000, 50, 180,70,50,marcellus, text="Start")
  button_start.draw(window,"#000000")
  if button_start.check_click():
    page = "game"
    print("the page was changed, the button was pressed")


  if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
      for i in res.pose_landmarks.landmark:
        lst.append(i.x - res.pose_landmarks.landmark[0].x)
        lst.append(i.y - res.pose_landmarks.landmark[0].y)

      lst = np.array(lst).reshape(1,-1)

      p = model.predict(lst)
      pred = label[np.argmax(p)]
      print(pred)

def game_page():
  
  start_time = time.time()
  current_time = time.time()
  given_time = 10
  total_time = start_time + given_time
  score = 0
  level_completed = False

  while current_time < total_time:
    current_time = time.time()
    total_time = total_time + given_time

    global page

    for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              break
  

    window.blit(bg1, (0,0))

    score_text = Text("#f2e30f",10,10,40,silkscreen,f"Score:")
    score_number = Text("#f2e30f",10,50,50,silkscreen,f"{score}")
    score_text.draw(window)
    score_number.draw(window)


    lst = []
    success, img = cap.read()
    img = cv2.flip(img, 1) 
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = holis.process(imgRGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    window.blit(frame, (220, 0))


    button_quit = Button((255,0,0),"#000000",920, 50, 200,70,50,marcellus, text="QUIT")
    button_quit.draw(window, (0,0,0))
    if button_quit.check_click():
      page = "start"
      break

    if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
        for i in res.pose_landmarks.landmark:
          lst.append(i.x - res.pose_landmarks.landmark[0].x)
          lst.append(i.y - res.pose_landmarks.landmark[0].y)

        lst = np.array(lst).reshape(1,-1)

        p = model.predict(lst)
        pred = label[np.argmax(p)]
        print(pred)
    
    pygame.display.update()
    clock.tick(fps)
  page = "start"



#fonts
marcellus = "Fonts\Marcellus-Regular.ttf"
silkscreen = "Fonts\Silkscreen-Regular.ttf"

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
bg1 = pygame.image.load('C:\D\Coding\CV Game Project\PROJECT\Background_Images\Background1.png').convert_alpha()
bg1 = pygame.transform.scale(bg1,(width,height))


#game variables
page = "start"
high_score = 10

#main loop
# while True:

#   if page == "start":
#     start_page()
#   elif page == "game":
#     game_page()

#   pygame.display.update()
#   clock.tick(fps)

print(label)