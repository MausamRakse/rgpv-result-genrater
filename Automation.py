# import the necessary packages
from selenium import webdriver
from selenium.webdriver.common.by import By
import google.generativeai as genai
import pathlib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os

# take input from user
# code=input("Enter college code: ")
# branch=input("Enter branch code: ")
# year=int(input("Enter year of admission: "))
# enrollment=code+branch+str(year)
# Sem=int(input("Enter semester: "))
# start=int(input("Enter starting roll number: "))
# end=int(input("Enter ending roll number: "))
# nol=int(input("Enter number of lateral students: "))

# take input from command line
code=sys.argv[1]
branch=sys.argv[2].upper()
year=int(sys.argv[3])
enrollment=code+branch+str(year)
Sem=int(sys.argv[4])
start=int(sys.argv[5])
end=int(sys.argv[6])
nol=int(sys.argv[7])
file_name=sys.argv[8]
lateral=False

# configure the api key
genai.configure(api_key="your api key")
model = genai.GenerativeModel('gemini-1.5-flash')

#create a csv file
first=True    

# function to solve captcha
def solve_captcha():
    # get the captcha image
    cap_img=browser.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_pnlCaptcha"]/table/tbody/tr[1]/td/div/img').screenshot_as_png
    time.sleep(1.5)
    # save the image
    with open('new.png','wb') as img:
        img.write(cap_img)

    # ask to model to solve the captcha
    cookie_picture = {
        'mime_type': 'image/png',
        'data': pathlib.Path('new.png').read_bytes()
    }
    prompt = '''Extract text from these images and always respond only the image text will contain only english
                alphabets and numbers and it will not contain any subscripts or superscripts'''

    # get the response
    response = model.generate_content(
        contents=[prompt, cookie_picture]
    )
    time.sleep(2)

    try:
        capcha=response.text
        # clean the response
        capcha=response.text.replace(' ','').upper()
        # fill the captcha
        browser.find_element(By.CSS_SELECTOR,'#ctl00_ContentPlaceHolder1_TextBox1').click() # click captcha
        browser.find_element(By.CSS_SELECTOR,'#ctl00_ContentPlaceHolder1_TextBox1').send_keys(capcha) # fill captcha
        try:
            # click submit if applicable
            browser.find_element(By.CSS_SELECTOR,'#ctl00_ContentPlaceHolder1_btnviewresult').click() # click submit
        except:
            pass
        # print the captcha
        print(f'captcha solved : {capcha}')
    except:
        print('captcha not solved')
        # handling wrong captcha
        solve_captcha()

# function to get result
def get_result(i):
    # generate the roll number
    if(lateral):
        on_roll=("{:02d}".format(i))
    else:
        on_roll=("{:03d}".format(i))

    #open the result page
    browser.get('http://result.rgpv.ac.in/Result/ProgramSelect.aspx')
    
    # wait for the page to load
    WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="radlstProgram_1"]')))

    # select btech from list
    btech=browser.find_element(By.XPATH,'//*[@id="radlstProgram_1"]').click()
    WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_drpSemester"]')))

    # fill the details
    sem=browser.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_drpSemester"]').send_keys(Sem)
    if(lateral):
        roll=browser.find_element(By.ID,'ctl00_ContentPlaceHolder1_txtrollno').send_keys(f'{enrollment}3D{str(on_roll)}')
        print(f'Processing {enrollment}3D{str(on_roll)}')
    else:
        roll=browser.find_element(By.ID,'ctl00_ContentPlaceHolder1_txtrollno').send_keys(f'{enrollment}1{str(on_roll)}')
        print(f'Processing {enrollment}1{str(on_roll)}')

    # send image to model
    solve_captcha()
    try:
        try:
            # check for invalid captcha
            if(browser.switch_to.alert.text=='Invalid Captcha'):
                browser.switch_to.alert.accept()
                solve_captcha()
        except:
            pass
        try:
            # check if result is not found
            if(browser.switch_to.alert.text=='Result for this Enrollment No. not Found'):
                browser.switch_to.alert.accept()
                print('Result not exist')
                return
        except:
            pass
        WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH,'//*[contains(text(), "Name")]')))
        print('Result Found')
    except:
        print('Error in getting result')
        get_result(i)
        return

# def start_automation(thread_name):       
    # open the browser

ons=webdriver.ChromeOptions()
ons.add_argument('--headless')
browser=webdriver.Chrome()
# browser.maximize_window()

# create a file
f=open(f'files/{file_name}.csv','a+')

# loop through all students
for i in range(start,end+nol+1):

    try:
        # get the result
        if(lateral):
            on_roll=("{:02d}".format(i))
            get_result(i%end)
        else:
            on_roll=("{:03d}".format(i))
            get_result(i)

        # store the information
        name=browser.find_element(By.ID,'ctl00_ContentPlaceHolder1_lblNameGrading').text
        result=browser.find_element(By.ID,'ctl00_ContentPlaceHolder1_lblResultNewGrading').text.replace(',',' ')
        sgpa=browser.find_element(By.ID,'ctl00_ContentPlaceHolder1_lblSGPA').text
        cgpa=browser.find_element(By.ID,'ctl00_ContentPlaceHolder1_lblcgpa').text
        table=browser.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_pnlGrading"]/table/tbody/tr[3]/td')
        table=table.text.splitlines()[1:]
        subjects=[]
        grades=[]
        for k in table:
            sub=k.split()
            subjects.append(sub[0]+sub[1])
            grades.append(sub[-1])
        # write the information to csv
        # with open(f'{code}{branch} sem - {Sem}.csv','a+')as f:
        # with open(f'files/{file_name}.csv','a+')as f:
        if(first):
            f.write(f'Name,ENROLLMENT NO,{subjects},Result,SGPA,CGPA\n')
            first=False  
        elif(lateral==True):
            print(on_roll)
            print(f'Processing {enrollment}3D{str(on_roll[-2:])}')
            roll=f'{enrollment}3D{str(on_roll[-2:])}'
            print(roll)
        
        else:
            roll=f'{enrollment}1{str(on_roll)}'
        
        f.write(f'{name},{roll},{grades},{result},{sgpa},{cgpa}\n')
        time.sleep(1)

    except Exception as e:
        if(i==end):
            print(i)
            lateral=True
            year+=1
            enrollment=code+branch+str(year)
        # print(e)
        continue
    if(i==end and lateral==False):
        print(i)
        lateral=True
        year+=1
        enrollment=code+branch+str(year)
f.close()
browser.quit()
print('--------------------Done-----------------------')