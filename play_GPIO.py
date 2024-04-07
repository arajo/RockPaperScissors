import sys
import pygame
import RPi.GPIO as GPIO
from pygame.locals import QUIT, MOUSEBUTTONDOWN,Rect,KEYDOWN,K_LEFT,K_DOWN,K_RIGHT,K_RETURN,K_ESCAPE
from random import randint
pygame.init()

disp_wd=640
disp_hg=480

SURFACE=pygame.display.set_mode((disp_wd,disp_hg), pygame.FULLSCREEN)
FPSL=pygame.time.Clock()




#GPIO setup

GPIO.setmode(GPIO.BCM)
gpio_k1=18 #가위 pin
gpio_k2=15 #바위 pin
gpio_k3=14 #보 pin
gpio_k4=23 #코인 pin
gpio_k5=24 #종료 pin
GPIO.setup(gpio_k1,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(gpio_k2,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(gpio_k3,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(gpio_k4,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(gpio_k5,GPIO.IN, pull_up_down = GPIO.PUD_UP)

#GPIO setup done





start_btn_img=(pygame.image.load("imgs/btn_s0.png").convert_alpha(),
               pygame.image.load("imgs/btn_s1.png").convert_alpha())

ring_img=(pygame.image.load("imgs/L00.png").convert_alpha(),
          pygame.image.load("imgs/L01.png").convert_alpha(),
          pygame.image.load("imgs/L02.png").convert_alpha(),
          pygame.image.load("imgs/L03.png").convert_alpha(),
          pygame.image.load("imgs/L04.png").convert_alpha(),
          pygame.image.load("imgs/L05.png").convert_alpha(),
          pygame.image.load("imgs/L06.png").convert_alpha(),
          pygame.image.load("imgs/L07.png").convert_alpha(),
          pygame.image.load("imgs/L08.png").convert_alpha(),
          pygame.image.load("imgs/L09.png").convert_alpha(),
          pygame.image.load("imgs/L10.png").convert_alpha(),
          pygame.image.load("imgs/L11.png").convert_alpha(),
          pygame.image.load("imgs/LWL.png").convert_alpha(),
          pygame.image.load("imgs/LWR.png").convert_alpha(),
          pygame.image.load("imgs/LDR.png").convert_alpha(),
          pygame.image.load("imgs/LLS.png").convert_alpha())


ring_x=(191,260,314,331,293,239,167,104,68,64,71,118,16,330,290,19)
ring_y=(89,100,149,234,304,348,357,326,280,213,142,100,63,77,283,277)

exit_btn_img=pygame.image.load("imgs/btn_exit.png").convert_alpha()

play_btn_img=(pygame.image.load("imgs/btn_00.png").convert_alpha(),
              pygame.image.load("imgs/btn_01.png").convert_alpha(),
              pygame.image.load("imgs/btn_10.png").convert_alpha(),
              pygame.image.load("imgs/btn_11.png").convert_alpha(),
              pygame.image.load("imgs/btn_20.png").convert_alpha(),
              pygame.image.load("imgs/btn_21.png").convert_alpha())

num_img=(pygame.image.load("imgs/n0.png").convert_alpha(),
         pygame.image.load("imgs/n1.png").convert_alpha(),
         pygame.image.load("imgs/n2.png").convert_alpha(),
         pygame.image.load("imgs/n3.png").convert_alpha(),
         pygame.image.load("imgs/n4.png").convert_alpha(),
         pygame.image.load("imgs/n5.png").convert_alpha(),
         pygame.image.load("imgs/n6.png").convert_alpha(),
         pygame.image.load("imgs/n7.png").convert_alpha(),
         pygame.image.load("imgs/n8.png").convert_alpha(),
         pygame.image.load("imgs/n9.png").convert_alpha())

bgimg=pygame.image.load("imgs/back_img.jpg").convert()

himg=pygame.image.load("imgs/hands.png").convert_alpha()

logo=pygame.image.load("imgs/logo.png").convert_alpha()

coin_img=(pygame.image.load("imgs/coin0.png").convert_alpha(),
          pygame.image.load("imgs/coin1.png").convert_alpha())

reset_img=pygame.image.load("imgs/reset.png").convert_alpha()






snd_jk=pygame.mixer.Sound("sound/jk.wav")
snd_insert=pygame.mixer.Sound("sound/insert.wav")
snd_bb=pygame.mixer.Sound("sound/bb.wav")
snd_win=pygame.mixer.Sound("sound/win.wav")
snd_lose=pygame.mixer.Sound("sound/lose.wav")
snd_draw=pygame.mixer.Sound("sound/draw.wav")
snd_rule=pygame.mixer.Sound("sound/rule.wav")
snd_yap=pygame.mixer.Sound("sound/yap.wav")
snd_get_coin=pygame.mixer.Sound("sound/get_coin.wav")


def num_print(num,loc):

    tem=999999
    if num>9999999:
        num=9999999

    for i in range(0,7):
        if num>tem:            
            SURFACE.blit(num_img[num//(tem+1)],(i*23+466,loc*91+93))
            num=num%(tem+1)
        else:
            SURFACE.blit(num_img[0],(i*23+466,loc*91+93))

        tem=tem//10




        
        

def start_btn(psh):
    SURFACE.blit(start_btn_img[psh],(479,psh*3+232))

def hand_play(num):
    SURFACE.blit(himg,(141,168),Rect(num*195,0,195,195))

def reset_btn(psh):
    if psh:
        SURFACE.blit(reset_img,(11,55))
    else:
        SURFACE.blit(reset_img,(11,59))

def exit_btn(psh):
    if psh:
        SURFACE.blit(exit_btn_img,(11,55))
    else:
        SURFACE.blit(exit_btn_img,(11,59))

def ring_on(num):
    SURFACE.blit(ring_img[num],(ring_x[num],ring_y[num]))
    
def play_btn(num):
    for i in range(0,3):
        if i==num:
            SURFACE.blit(play_btn_img[i*2+1],(i*148+53,437))
        else:
            SURFACE.blit(play_btn_img[i*2],(i*148+53,431))

def main():

    fps=30
    coin=20
    all_coin=0
    exit_press=0
    coin_press=0
    win_led=0
    get_coin=0
    coin_cnt=0
    tg_ring=0
    coin_x=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    coin_y=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    coin_i=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


    can_play=0
    mode=0
    alp=0
    hand_flk=0
    cur_hand=0
    ring_num=0
    time_del=0

    mouse_loc=[]
    click_loc=9

    
    while True:
        
        click_loc=9
                   
        
        for event in pygame.event.get():
            if event.type==QUIT:
                GPIO.cleanup()
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                   
                    mouse_loc=pygame.mouse.get_pos()
                    if mouse_loc[1]>431 and mouse_loc[1]<476:
                        
                        if mouse_loc[0] >52 and mouse_loc[0] < 130:
                           
                            click_loc=0
                        elif mouse_loc[0] >199 and mouse_loc[0] < 279:
                            
                            click_loc=1
                        elif mouse_loc[0] >348 and mouse_loc[0] < 427:
                           
                            click_loc=2
                    else:
                        if mouse_loc[0] >481 and mouse_loc[0] < 622 and mouse_loc[1]>236 and mouse_loc[1]<288:
                            
                            click_loc=3
                        if mouse_loc[0] >12 and mouse_loc[0] < 56 and mouse_loc[1]>58 and mouse_loc[1]<106:
                           
                            click_loc=4
            else:
                click_loc=9
            if click_loc==9:
                if event.type==KEYDOWN:
                    if event.key==K_LEFT:
                         click_loc=0
                    elif event.key==K_DOWN:
                         click_loc=1
                    elif event.key==K_RIGHT:
                         click_loc=2
                    elif event.key==K_RETURN:
                         click_loc=3
                    elif event.key==K_ESCAPE:
                         click_loc=4
                


        #GPIO read
                         
        if click_loc==9:            
            if not GPIO.input(gpio_k1):
                click_loc=0                
            elif not GPIO.input(gpio_k2):
                click_loc=1
            elif not GPIO.input(gpio_k3):
                click_loc=2
            elif not GPIO.input(gpio_k4):
                click_loc=3
            elif not GPIO.input(gpio_k5):
                click_loc=4 

        #GPIO read done



        if mode==0:
            #intro
            SURFACE.fill((0,0,0))
            SURFACE.blit(logo,(163,145))

            alp+=1
            if alp>40:
                alp=0
                mode=1
                
                
        else:
            if mode==1:
                #idle
                SURFACE.blit(bgimg,(0,0))

                hand_flk+=1
                if hand_flk >= fps*1:
                    hand_flk=0
                    cur_hand+=1
                    if cur_hand>2:
                        cur_hand=0    

                hand_play(cur_hand)
                num_print(all_coin*100,0)
                num_print(coin*100,1)
                play_btn(4)  

               
                if click_loc==3 and coin>0:
                    if not coin_press:
                        snd_insert.play()                    
                    coin_press=1
                    start_btn(1)  
                else:
                    if coin_press:                            
                        coin_press=0
                        all_coin+=1
                        coin-=1
                        can_play=1
                        snd_jk.play()
                        mode=2

                    start_btn(0)

            elif mode==2:
                
                SURFACE.blit(bgimg,(0,0))
                num_print(all_coin*100,0)
                num_print(coin*100,1)
                start_btn(0)


                if click_loc<3:
                    snd_jk.stop()
                    snd_draw.stop()
                   
                    play_btn(click_loc) 
                    if can_play:
                        can_play=0
                        res=randint(0,50)
                        hand_flk=0
                        snd_bb.play()
                        
                        if res<8:
                            
                            ring_num=12
                            cur_hand=click_loc-1
                            
                            if cur_hand<0:
                                cur_hand=2


                        elif res<30:
                            
                            ring_num=14
                            cur_hand=click_loc
                            

                        else:
                            
                            ring_num=15
                            cur_hand=click_loc+1
                            if cur_hand>2:
                                cur_hand=0


                else:
                    play_btn(4) 

                if can_play:
                     hand_flk+=1
                     if hand_flk >= 2:
                         hand_flk=0
                         cur_hand+=1
                         if cur_hand>2:
                             cur_hand=0
                     

                else:   
                    hand_flk+=1
                    if hand_flk==7:
                        if ring_num==15:
                            snd_lose.play()
                            
                        elif ring_num==14:
                            snd_draw.play() 
                            
                        else:
                            snd_win.play()



                    if hand_flk>23:
                        if ring_num==15:                            
                            mode=1
                        elif ring_num==14:                            
                            can_play=1
                        else:
                            mode=3 
                            snd_rule.play(loops=-1)
                            ring_num=0
                            time_del=0

                    ring_on(ring_num)

                hand_play(cur_hand)


            elif mode==3:
            
                if time_del<60:
                    time_del+=1

                if time_del==59:
                    res=randint(0,342)
                    if res<20:
                        get_coin=4
                        tg_ring=0
                    elif res<80:
                        get_coin=1
                        tg_ring=1
                    elif res<115:
                        get_coin=2
                        tg_ring=2
                    elif res<123:
                        get_coin=7
                        tg_ring=3
                    elif res<143:
                        get_coin=4
                        tg_ring=4
                    elif res<178:
                        get_coin=2
                        tg_ring=5
                    elif res<184:
                        get_coin=20
                        tg_ring=6
                    elif res<244:
                        get_coin=1
                        tg_ring=7
                    elif res<279:
                        get_coin=2
                        tg_ring=8
                    elif res<299:
                        get_coin=4
                        tg_ring=9
                    elif res<307:
                        get_coin=7
                        tg_ring=10
                    else:
                        get_coin=2
                        tg_ring=11


                SURFACE.blit(bgimg,(0,0))
                num_print(all_coin*100,0)
                num_print(coin*100,1)
                start_btn(0)
                hand_play(cur_hand)

                hand_flk+=1
                if hand_flk>2:
                    hand_flk=0
                    win_led=not win_led
                    ring_num+=1
                    
                    if ring_num>11:
                        ring_num=0

                ring_on(win_led+12)
                ring_on(ring_num)
                if ring_num==tg_ring and time_del==60:
                    snd_rule.stop()
                    snd_yap.play()
                    time_del=-20
                    coin_cnt=0
                    mode=4






                if click_loc<3:                   
                    play_btn(click_loc) 
                else:
                    play_btn(4) 

            elif mode==4:
                


                SURFACE.blit(bgimg,(0,0))



                time_del+=1
                if time_del==4 and get_coin > coin_cnt:
                    
                    time_del=0
                    
                    coin_x[coin_cnt]=randint(475,565)
                    coin_y[coin_cnt]=randint(385,407)
                    coin_i[coin_cnt]=randint(0,1)
                    coin_cnt+=1
                    coin+=1
                    snd_get_coin.play()




                for i in range(0,coin_cnt):
                    SURFACE.blit(coin_img[coin_i[i]],(coin_x[i],coin_y[i]))

                num_print(all_coin*100,0)
                num_print(coin*100,1)
                start_btn(0)
                hand_play(cur_hand)
                ring_on(win_led+12)
                ring_on(ring_num)
                play_btn(4)

                if time_del==30:
                    mode=1

      

            if click_loc==4:
                    #exit/reset
                    exit_press=1
                    if mode==1 and coin==0:
                        reset_btn(0)

                    else:
                        exit_btn(0)
                    
                    
            else:
                    if exit_press:
                         if mode==1 and coin==0:
                            exit_press=0
                            coin=20
                            all_coin=0
                           
                         else:
                            GPIO.cleanup()
                            pygame.quit()
                            sys.exit()
                           
                    

                    else:
                         if mode==1 and coin==0:
                            reset_btn(1)

                         else:
                             exit_btn(1)


          

        pygame.display.flip()            
        FPSL.tick(fps)
            
    
if __name__ == '__main__':
    main()
