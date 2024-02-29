import pyautogui
import os
import subprocess
import time
import datetime

CIC_PATH_GEN = "C:/Users/Houssem/Downloads/CICFlowmeter/CICFlowmeter/bin"
CIC_ORIGNAL_PATH_DIRECTORY = 'C:/Users/Houssem/Downloads/CICFlowmeter/CICFlowmeter/bin/data/daily/'
CIC_RUN = "CICFlowMeter.bat"
CMD_COMMAND = f'cd {CIC_PATH_GEN} && {CIC_RUN}'
file_date = f"{datetime.datetime.now().strftime("%Y-%m-%d")}_Flow.csv"
# file_path = os.path.join(CIC_ORIGNAL_PATH_DIRECTORY,file_date)
imgs_path = os.getcwd()
save_path = f'C:/Users/Houssem/Desktop/IDS Project/{file_date}'

print(os.path.join(imgs_path, 'load_button.png'))



# screenWidth, screenHeight = pyautogui.size() # Returns two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)

# currentMouseX, currentMouseY = pyautogui.position() # Returns two integers, the x and y of the mouse cursor's current position.

# print('screenHeight',screenHeight)
# print('screenWidth',screenWidth)
# print('currentMouseX',currentMouseX)
# print('currentMouseY',currentMouseY)
# print('OS_PATH',CIC_PATH_GEN)

# subprocess.Popen(CIC_PATH_GEN, shell=True)

#os.system(f'cmd /c "cd {CIC_PATH_GEN} && {CIC_RUN}')



def load_buttonFun(path): 
    time.sleep(3)
    # locate to load button and then click on it 
    load_button = pyautogui.locateCenterOnScreen('load_button.png')
    pyautogui.moveTo(load_button)
    pyautogui.click()
    # time sleep to load the UI
    time.sleep(1)

    
def capture_flow(ar_path , ntw_path, start_path, stp_path):
    # locate to arrow button and then click on it 
    arrow_btn = pyautogui.locateCenterOnScreen('arrow.png')
    pyautogui.moveTo(arrow_btn)
    pyautogui.doubleClick()

    # time sleep to load the UI
    time.sleep(1)

    # locate to network driver and then click on it 
    ntw_btn = pyautogui.locateCenterOnScreen('network.png')
    pyautogui.moveTo(ntw_btn)
    pyautogui.click()

    # time sleep to load the UI
    time.sleep(1)

    # locate to start button and then click on it 
    start_btn = pyautogui.locateCenterOnScreen('start.png')
    pyautogui.moveTo(start_btn)
    pyautogui.click()


    #close the CICFlowMeter after 24Hours to save the csv file daily
    time.sleep(60)

    # locate to start button and then click on it 
    stop_btn = pyautogui.locateCenterOnScreen('stop.png')
    pyautogui.moveTo(stop_btn)
    pyautogui.click()        


resulut = subprocess.Popen(CMD_COMMAND , shell=True)
    

#filepath="C:/Users/Houssem/Downloads/CICFlowmeter/CICFlowmeter/bin/CICFlowMeter.bat"
#p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

#stdout, stderr = p.communicate()


#resultat = subprocess.run([r"C:/Users/Houssem/Downloads/CICFlowmeter/CICFlowmeter/bin/CICFlowMeter.bat"])

# subprocess.run(CIC_ORIGNAL_PATH_DIRECTORY, CIC_RUN)

#subprocess.call([CMD_COMMAND])

if resulut:
    load_buttonFun(os.path.join(imgs_path, 'load_button.png'))
    capture_flow(os.path.join(imgs_path, 'arrow.png'),
                 os.path.join(imgs_path, 'network.png'), 
                 os.path.join(imgs_path, 'start.png'),
                 os.path.join(imgs_path, 'stop.png'),)



# Then, we need to click on 'OK' and redo  all steps again




# os.system("taskkill /F /IM CICFlowMeter.bat")




