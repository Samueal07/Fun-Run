
import pygame
from sys import exit
from random import randint

def display_score():
    current_time=int(pygame.time.get_ticks()/1000)-start_time
    score_surf=test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect=score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)
    return current_time #make it a global variable to be sued to display score at intro screen
# for bringing the obstacles
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x-=5 # right to left movement (900---)

            if obstacle_rect.bottom==300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)

    
        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x > -100]# only append when its inside the screen and get rid of it once beyong left
        return obstacle_list #makes it global

    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):return False
    #if no collision then
    return True
#for animation
def player_animation():
    global player_surf,player_index

    if player_rect.bottom<300:  
        player_surf=player_jump #jump
    else:
        player_index+=0.1#walk1 to walk2 slowly
        if player_index>=len(player_walk):
            player_index=0
        player_surf=player_walk[int(player_index)]
    # walking animation

    #when jumping


#intialising py game
pygame.init()
screen=pygame.display.set_mode((800,400)) #width and height of display
pygame.display.set_caption('Fun Run')
clock=pygame.time.Clock() #sets fps for the game
game_active=False
test_font=pygame.font.Font('font/Pixeltype.ttf',50) #font used for displaying score
start_time=0
score=0
bg_music=pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.5
)# volume 0-1
bg_music.play(loops=-1)#infintely play it

sky_surface=pygame.image.load('graphics/Sky.png').convert() # background image , converts helps optimise game
ground_surface=pygame.image.load('graphics/ground.png').convert() # same as above

# score_surf=test_font.render("Score 0",False,(64,64,64)) #used for fonts
# score_rect=score_surf.get_rect(center=(400,50))#to align score

#displays enemy animation
snail_frame_1=pygame.image.load('graphics/snail/snail1.png').convert_alpha() 
snail_frame_2=pygame.image.load('graphics/snail/snail2.png').convert_alpha() 
snail_frames=[snail_frame_1,snail_frame_2]
snail_frame_index=0
snail_surf=snail_frames[snail_frame_index]
#for fly animation
fly_frame1=pygame.image.load('graphics/fly/fly1.png').convert_alpha() 
fly_frame2=pygame.image.load('graphics/fly/fly2.png').convert_alpha() 
fly_frames=[fly_frame1,fly_frame2]
fly_frame_index=0
fly_surf=fly_frames[fly_frame_index]


fly_surf=pygame.image.load('graphics/fly/fly1.png').convert_alpha()
obstacle_rect_list=[] #used to bring in and out the obstacle by appending values

player_walk_1= pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2= pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk=[player_walk_1,player_walk_2]
player_index=0 # to pick either walk 1 or walk 2
player_jump=pygame.image.load('graphics/player/jump.png').convert_alpha()
player_surf=player_walk[player_index]# at first walk 1 as its at index 0
player_rect=player_surf.get_rect(midbottom=(80,300))

player_gravity=0
#intro Screen
player_stand=pygame.image.load('graphics/player/player_stand.png').convert_alpha()#importing image
player_stand=pygame.transform.rotozoom(player_stand,0,2)#updating image scale (what to,angle,scale)
player_stand_rect=player_stand.get_rect(center=(400,200))

game_name=test_font.render('Fun Run',False,(111,196,169))#name of game above image
game_name_rect=game_name.get_rect(center=(400,80))

game_message=test_font.render('Press space to run',False,(111,196,169))
game_message_rect=game_message.get_rect(center=(400,320))

#timer for diff obstacle
obstacle_timer=pygame.USEREVENT + 1 #some events are already reserved for pygame so we need to add 1 to avoid conflict
pygame.time.set_timer(obstacle_timer,1500)#triggering the timer for 

snail_animation_timer=pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer=pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200)


while True:
    for event in pygame.event.get(): # helps act acc. to input on keyboard
        if event.type == pygame.QUIT: # event to quit game
            pygame.quit()
            exit()
        if game_active:
            if event.type==pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.post) and player_rect.bottom is 300:
                    player_gravity=-20
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and player_rect.bottom==300: # corelates to line 52
                    player_gravity=-20
        else:
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game_active=True
                start_time=int(pygame.time.get_ticks()/1000)
        if game_active:
            if event.type==obstacle_timer :
                if randint(0,2): # 0 for False 1  for True
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900,1100),300))) # For True
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900,1100),210))) # For False
            #for snail animation
            if event.type==snail_animation_timer:
                if snail_frame_index==0:snail_frame_index=1 #alternate between images via index
                else:snail_frame_index=0
                snail_surf=snail_frames[snail_frame_index]
            #for fly animation
            if event.type==fly_animation_timer:
                if fly_frame_index==0:fly_frame_index=1 #alternate between images via index
                else:fly_frame_index=0
                fly_surf=fly_frames[fly_frame_index]



    if game_active:
        screen.blit(sky_surface,(0,0)) # displaying surface 
        screen.blit(ground_surface,(0,300))
        score=display_score()#updates score and is then displayed via else statement in the main else 

        # snail_rect.x-=4 # in sync with clock at line 8 
        # if snail_rect.right<=0:snail_rect.left=800 # to move snail
        # screen.blit(snail_surf,snail_rect)
        
        #player mechanics
        player_gravity+=1
        #300 then 301,302   ...
        player_rect.y+=player_gravity
        #for collison we just change player rect position
        if player_rect.bottom>=300:player_rect.bottom=300
        player_animation()
        screen.blit(player_surf,player_rect)

        # obstacle movement
        obstacle_rect_list=obstacle_movement(obstacle_rect_list) # updates list via the above obstacle_movement function made

        #collisions
        game_active=collisions(player_rect,obstacle_rect_list) # if collision then becomes false and goes to else i.e intro screen

        
    #for the start screen
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear() # this clears the screen after we hit a snail or fly and prevents crashing 
        player_rect.midbottom=(80,300)
        player_gravity=0

        score_message=test_font.render(f'Your Score:{score}',False,(111,196,169))
        score_message_rect=score_message.get_rect(center=(400,330))
        screen.blit(game_name,game_name_rect)
        if score==0:  # above we declared it
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

        
                


    # keys=pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     print('jump')

    pygame.display.update() # very important to update display all inside while

    clock.tick(60) # 60 fps




