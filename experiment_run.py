import os
import sys
import time
import random
import threading
import multiprocessing
import subprocess
from pydub import AudioSegment
from pydub.playback import play
import vlc
import pygame

from mode_config import ModeManager
from head_control import HeadMotors
from torso_control import TorsoMotors

mode_manager = ModeManager()
head_motors = HeadMotors()
torso_motors = TorsoMotors()
start_exp = False #should be false
audio_playing = False
nextsection = False
jazz1 = None

def keyboard_listener(paused, eyebrow_process, yaw_process):
    global start_exp
    paused_state = True  # Track the paused state
    while True:
        user_input = input("Enter command (s to start, p to pause/resume, q to quit): ").lower()
        if user_input == 's':
            start_exp = True
            print("Experiment started.")
        elif user_input == 'p':
            if paused_state:
                paused.clear()  # Resume the eyebrow process
                print("Program resumed.")
            else:
                paused.set()  # Pause the eyebrow process
                print("Program paused.")
            paused_state = not paused_state  # Toggle paused state
        elif user_input == 'q':
            eyebrow_process.terminate()
            eyebrow_process.join()  # Ensure the process has terminated
            
            yaw_process.terminate()
            yaw_process.join()
            terminate_program()
            break

def eye_brow_idle(paused):
    while True:
        paused.wait()  # Block the loop when the event is set (paused)
        probability = 0.07  # Probability of eyebrow idle movement
        blink_speed = random.choice([500, 700, 1000])
        if random.random() < probability:
            try:
                head_motors.move("eye_brow_l", 210, blink_speed)
                time.sleep(0.01)
                head_motors.move("eye_brow_r", 510, blink_speed)
                time.sleep(0.2 if blink_speed == 1000 else 0.5 if blink_speed == 700 else 0.7)
                head_motors.move("eye_brow_l", 370, blink_speed)
                time.sleep(0.01)
                head_motors.move("eye_brow_r", 343, blink_speed)
            except Exception as e:
                print(f"Error in eyebrow movement: {e}")
                time.sleep(0.01)
                continue
        time.sleep(0.5)

def playaudio(audio, speed=1.0):
    global audio_playing
    if speed != 1.0:
        audio = audio.speedup(playback_speed=speed)
    t = threading.Thread(target=play, args=(audio,))
    t.start()

def sound_waiter(s):
    global audio_playing
    audio_playing = True
    time.sleep(s/1000)
    time.sleep(1)
    audio_playing = False
    
def terminate_program():
    print("Terminating program.")
    if jazz1:
        jazz1.terminate()
    torso_motors.release_motors()
    torso_motors.release_hands('all')
    head_motors.close()
    pygame.quit()
    sys.exit(0)

def yaw_roll(paused):
    while True:
        paused.wait()  # Block the loop when the event is set (paused)
        probability = 0.07  # Probability of eye movement
        if random.random() < probability:
            random_value = random.randint(0, 300)
            random_speed = random.randint(300, 500)
            head_motors.move("head_yaw", random_value, random_speed)
            random_rt = random.randint(1, 3)
            time.sleep(random_rt)
            head_motors.move("head_yaw", 180, random_speed)

        time.sleep(0.5)

def display_image_on_screen(image_path):
    #screen = pygame.display.set_mode((0, 0))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, screen.get_size())

    screen.blit(image, (0, 0))
    pygame.display.flip()

    return screen

def handle_pygame_events(jazz_process):
    global nextsection
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            try:
                jazz_process.terminate()
                pygame.quit()
                nextsection = True
            except Exception as e:
                print(e)


def pygame_thread(image_path):
    screen = display_image_on_screen(image_path)
    
    # Keep checking for events until nextsection is True
    while not nextsection:
        handle_pygame_events(jazz1)
        time.sleep(0.1)
"""
def play_video_on_loop(vlc_instance, video_path):
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(video_path)
    media.add_option('no-audio')  # Mute the video
    player.set_media(media)
    #player.set_fullscreen(True)
    
    player.play()
    return player
"""
def control_video_player(vlc_instance, video_path, control_event):
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(video_path)
    media.add_option('no-audio')
    player.set_fullscreen(True)
    player.set_media(media)
    player.play()

    while not control_event.is_set():
        state = player.get_state()
        if state in [vlc.State.Ended, vlc.State.Stopped, vlc.State.Error]:
            player.play()  # Loop the video
        time.sleep(0.1)

    player.stop()  # Stop the video when the event is set
    
def play_video_in_thread(vlc_instance, video_path, no_loop=False, full=False, mute=True, delay=True):
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(video_path)
    if mute == True:
        media.add_option('no-audio')  # Mute the video if needed
    if full:
        player.set_fullscreen(True)
    player.set_media(media)

    player.play()
    
    if delay:
        print("delay")
        time.sleep(1)
        
    player.play()
    while True:
        state = player.get_state()
        if state in [vlc.State.Ended, vlc.State.Stopped, vlc.State.Error]:
            break
        time.sleep(0.1)
        
    if no_loop == True:
        player.stop()  # Stop and close the player after playback ends
        
    return player  # Return the player to control it later
        
if __name__ == "__main__":
    paused = multiprocessing.Event()  # Use multiprocessing.Event directly
    paused.set()  # Start in a paused state
    random_brow_process = multiprocessing.Process(target=eye_brow_idle, args=(paused,))
    random_yaw_roll_process = multiprocessing.Process(target=yaw_roll, args=(paused,))
    
    audio_m1 = AudioSegment.from_file('experiment/voice/1.m4a')
    audio_m2 = AudioSegment.from_file('experiment/voice/2.m4a')
    audio_m3 = AudioSegment.from_file('experiment/voice/3.m4a')
    audio_m4 = AudioSegment.from_file('experiment/voice/4.m4a')
    audio_m5 = AudioSegment.from_file('experiment/voice/5.m4a')
    audio_m5_j = AudioSegment.from_file('experiment/voice/5-jazz.m4a')
    audio_m6 = AudioSegment.from_file('experiment/voice/6.m4a')
    video_m7 = '/home/mirrly/mirrly_backend/experiment/videos/7.mp4'
    audio_m8_c1 = AudioSegment.from_file('experiment/voice/8-c1.m4a')
    video_m8_c2 = '/home/mirrly/mirrly_backend/experiment/videos/8-c2.mp4'
    audio_m9 = AudioSegment.from_file('experiment/voice/9.m4a')
    audio_m10 = AudioSegment.from_file('experiment/voice/10.m4a')
    audio_m12 = AudioSegment.from_file('experiment/voice/12.m4a')
    audio_m13 = AudioSegment.from_file('experiment/voice/13.m4a')
    audio_m14 = AudioSegment.from_file('experiment/voice/14.m4a')
    
    # Initialize VLC instance
    vlc_instance = vlc.Instance('--input-repeat=999999', '--mouse-hide-timeout=0')

    # Event to control the video playback
    logo_video_event = threading.Event()
    
    logo_video_thread = threading.Thread(target=control_video_player, args=(vlc_instance, "logo_intro.mp4", logo_video_event))
    logo_video_thread.start()
        
    try:
        # Start a separate thread to listen for the keyboard inputs
        keyboard_thread = threading.Thread(target=keyboard_listener, args=(paused, random_brow_process,
                                                                           random_yaw_roll_process))
        keyboard_thread.daemon = True
        keyboard_thread.start()
        
        
        # Wake up motion
        head_motors.move("eye_brow_l", 210, 500)
        head_motors.move("eye_brow_r", 510, 500)
        head_motors.move("head_pitch", 125, 800)
        head_motors.move("head_yaw", 180, 400)

        torso_motors.arm_move("arm_r", 170, 0.001)  # 170 Down - 90 Up When screw is front
        torso_motors.arm_move("arm_l", 80, 0.001)  # 160 Up - 80 Down When screw is front
        torso_motors.arm_move("r_shoulder", 70, 0.001)  # 70 cap front - 160 cap top -
        torso_motors.arm_move("l_shoulder", 160, 0.001)  # 160 cap front - 60 cap top
        
        
        # Wait until the experiment starts
        print("Press s to start...")
        while not start_exp:
            time.sleep(1)
        
        head_motors.move("eye_brow_l", 370, 400)
        head_motors.move("eye_brow_r", 343, 400)
        head_motors.move("head_pitch", 220, 300)
        head_motors.move("eye_self", 139, 300)  # 139-277
        time.sleep(5)
        head_motors.move("head_pitch", 195, 1000)
        head_motors.move("eye_self", 277, 600)  # 139-277
        
        random_brow_process.start()
               
        time.sleep(2)
        head_motors.move("eye_self", 190, 600)  # 139-277
        head_motors.move("head_yaw", 400, 400)
        time.sleep(2)
        head_motors.move("head_yaw", 180, 700)
        time.sleep(3)
        playaudio(audio_m1)
        
        random_yaw_roll_process.start()

        torso_motors.arm_move("arm_l", 160, 0.01)  # 160 Up - 80 Down When screw is front
        torso_motors.arm_move("arm_r", 90, 0.01)  # 170 Down - 90 Up When screw is front
        time.sleep(1)
        playaudio(audio_m2)
        torso_motors.arm_move("l_shoulder", 140, 0.005)  # 160 cap front - 60 cap top
        torso_motors.arm_move("arm_l", 140, 0.01)  # 160 Up - 80 Down When screw is front
        time.sleep(0.5)
        torso_motors.arm_move("l_shoulder", 160, 0.005)  # 160 cap front - 60 cap top
        torso_motors.arm_move("arm_l", 160, 0.01)  # 160 Up - 80 Down When screw is front
        time.sleep(0.5)
        torso_motors.arm_move("l_shoulder", 140, 0.005)  # 160 cap front - 60 cap top
        torso_motors.arm_move("arm_l", 140, 0.01)  # 160 Up - 80 Down When screw is front
        time.sleep(0.5)
        torso_motors.arm_move("l_shoulder", 160, 0.005)  # 160 cap front - 60 cap top
        torso_motors.arm_move("arm_l", 160, 0.01)  # 160 Up - 80 Down When screw is front
        time.sleep(0.5)
        torso_motors.arm_move("arm_l", 80, 0.005)  # 160 Up - 80 Down When screw is front
        torso_motors.arm_move("arm_r", 170, 0.005)  # 170 Down - 90 Up When screw is front
        
        sound_waiter(len(audio_m1) + len(audio_m2) - 2500)
        playaudio(audio_m3)
        
        sound_waiter(len(audio_m3))
           
        playaudio(audio_m4)
        sound_waiter(len(audio_m4))

        
        pygame.init()
        playaudio(audio_m5)
        
        logo_video_event.set()
        time.sleep(4)
        # Start pygame thread to display image
        pygame_thread_obj = threading.Thread(target=pygame_thread, args=("/home/mirrly/mirrly_backend/experiment/images/qrpic.jpg", ))
        pygame_thread_obj.start()

        # Wait until audio_m5 is done
        sound_waiter(len(audio_m5))
        
        # Start jazz music after audio_m5 is done
        jazz1 = subprocess.Popen(['vlc', '--intf', 'dummy', '--loop', '/home/mirrly/mirrly_backend/experiment/voice/5-jazz.m4a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # pygame event handling continues in the pygame thread
        pygame_thread_obj.join()

        logo_video_event.clear()  # Allow the logo video to play again
        logo_video_thread = threading.Thread(target=control_video_player, args=(vlc_instance, "logo_intro.mp4", logo_video_event))
        logo_video_thread.start()

        playaudio(audio_m6)
        sound_waiter(len(audio_m6))
        
        logo_video_event.set()
        time.sleep(4)
        vlc_instance2 = vlc.Instance('--mouse-hide-timeout=0')
        video_thread_2 = threading.Thread(target=play_video_in_thread, args=(vlc_instance2, video_m7, True, True, False))
        video_thread_2.start()
        video_thread_2.join()  # Ensure the video plays to completion
        
        logo_video_event.clear()  # Allow the logo video to play again
        logo_video_thread = threading.Thread(target=control_video_player, args=(vlc_instance, "logo_intro.mp4", logo_video_event))
        logo_video_thread.start()
        
        playaudio(audio_m8_c1)
        sound_waiter(len(audio_m8_c1))
        
        paused.clear()
        time.sleep(1)
        
        head_motors.move("eye_brow_l", 210, 500)
        head_motors.move("eye_brow_r", 510, 500)
        head_motors.move("head_pitch", 125, 800)
        head_motors.move("head_yaw", 180, 400)

        torso_motors.arm_move("arm_r", 170, 0.001)  # 170 Down - 90 Up When screw is front
        torso_motors.arm_move("arm_l", 80, 0.001)  # 160 Up - 80 Down When screw is front
        torso_motors.arm_move("r_shoulder", 70, 0.001)  # 70 cap front - 160 cap top -
        torso_motors.arm_move("l_shoulder", 160, 0.001)  # 160 cap front - 60 cap top
        
        logo_video_event.set()
        time.sleep(4)

        vlc_instance3 = vlc.Instance('--mouse-hide-timeout=0')
        video_thread_3 = threading.Thread(target=play_video_in_thread, args=(vlc_instance3, video_m8_c2, True, True, False))
        video_thread_3.start()
        video_thread_3.join()  # Ensure the video plays to completion
        
        logo_video_event.clear()  # Allow the logo video to play again
        logo_video_thread = threading.Thread(target=control_video_player, args=(vlc_instance, "logo_intro.mp4", logo_video_event))
        logo_video_thread.start()
        
        #pygame.init()
        paused.set()
        time.sleep(2)
        
        nextsection = False
        playaudio(audio_m9)
        sound_waiter(len(audio_m9))

        playaudio(audio_m10)
        # Wait until audio_m5 is done
        sound_waiter(len(audio_m10))
        
        logo_video_event.set()
        time.sleep(4)
        # Start pygame thread to display image
        pygame_thread_obj_2 = threading.Thread(target=pygame_thread, args=("/home/mirrly/mirrly_backend/experiment/images/9_qr.jpg",))
        pygame_thread_obj_2.start()

        # Start jazz music after audio_m10 is done
        jazz1 = subprocess.Popen(['vlc', '--intf', 'dummy', '--loop', '/home/mirrly/mirrly_backend/experiment/voice/11-jazz.m4a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # pygame event handling continues in the pygame thread
        pygame_thread_obj_2.join()
        
        logo_video_event.clear()  # Allow the logo video to play again
        logo_video_thread = threading.Thread(target=control_video_player, args=(vlc_instance, "logo_intro.mp4", logo_video_event))
        logo_video_thread.start()
        
        playaudio(audio_m12)
        sound_waiter(len(audio_m12))
        
        playaudio(audio_m13)
        sound_waiter(len(audio_m13))
        
        playaudio(audio_m14)
        sound_waiter(len(audio_m14))
        
        subprocess.Popen(['vlc', '--intf', 'dummy', '--loop', '/home/mirrly/mirrly_backend/experiment/voice/15-jazz.m4a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        while True:
            time.sleep(1)
        
    except Exception as e:
        print(f"Exception occurred: {e}")
        logo_video_event.set()  # Ensure the video is stopped
        logo_video_thread.join()  # Wait for the video thread to finish
        terminate_program()
