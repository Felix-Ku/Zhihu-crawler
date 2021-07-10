# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 15:17:56 2020

@author: FelixKu 3035370363

@project: FINA2390 Project 4 - 4.1 Zhihu

Reference: https://blog.csdn.net/qq_36962569/article/details/77200118?utm_medium=distribute.pc_relevant.none-task-blog-title-3&spm=1001.2101.3001.4242
"""

# Packages
import pandas as pd
import requests
import re # For expression
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import json # For writing dictionary out to json

# Initialize the Chrome driver 
def Driver_init(Driverlocation):
    try:
        return webdriver.Chrome(executable_path=Driverlocation)
    except Exception:
        print("Error initializing Chrome Driver!")
        return 

# Read Website function
def get_website(url):
    resp=requests.get(url)
    if resp.status_code==200:
        print('[HTTP requested successfully]')
    else:
        print('Something wrong happened, the HTTP Status Code is: ',resp.status_code)
        print(resp.text)
    return(BeautifulSoup(resp.text,'lxml'))

# Retrieve web contents
def retrievesource(current):
    return (BeautifulSoup(current.page_source,'lxml'))

def shutdown(current):
    current.close()

''' 
------------------------------------------------------------------
''' 

# (User Report) Generated full user report 
def SearchU(SearchName):
    
    print("\nLoading ... Please wait")
    
    # Create URL
    url = f"https://www.zhihu.com/people/{SearchName}"
    
    # Browser part
    browser=Driver_init("chromedriver.exe")
    browser.maximize_window()
    browser.get(url)
    
    time.sleep(2)
    
    # Check the title to see whether 404 or not
    if "404" in browser.title:
        print("User not found, please check your id.")
        browser.close()
    else:
        
        try:
            # Variable
            UserInfo=[]
            interestedtopics=[]
            interestedcolumns=[]
            interestedquestions=[]
            time.sleep(1)
            
            # Click the expand button
            expand_button = browser.find_element_by_xpath("//button[@class='Button ProfileHeader-expandButton Button--plain']")
            expand_button.click()
            
            # Retrieve contents
            soup = retrievesource(browser)
            
            # Input the id
            UserInfo.append(SearchName)
            
            # Get name of the user
            try:
                UserInfo.append(soup.find("span",class_="ProfileHeader-name").text)
            except:
                UserInfo.append("")
            
            # Get other info
            Otherinfo = soup.find_all("div", class_="ProfileHeader-detailValue")
            for info in Otherinfo:
                UserInfo.append(info.text)
            
            # Get achievements of the user
            UserInfo.append(soup.find("div",class_="css-vurnku").text)    
            
            # Switch to Get the list of user's interested topics
            browser.find_element_by_xpath("//a[@href='/people/"+SearchName+"/following/topics']").click()
            # Sleep safety
            time.sleep(2)
            # See how many pages are their by check number of buttons
            page_buttons = browser.find_elements_by_xpath("//button[@class='Button PaginationButton Button--plain']")
            # Loop through all the pages
            for i in range(len(page_buttons)):
                # Extend the list to store the information
                interestedtopics.extend([x.text for x in browser.find_elements_by_xpath("//h2[@class='ContentItem-title']")])
                # Sleep to prevent page skipped before retrieving all data
                time.sleep(1)
                # To next page by pressing the next page button
                nextpage_buttons = browser.find_element_by_xpath("//button[@class='Button PaginationButton PaginationButton-next Button--plain']")
                nextpage_buttons.click()
                # Sleep and let next page load first
                time.sleep(2)
            if interestedtopics != []:
                print("User's interested topics extracted!")
            
            
            # Switch to Get the list of user's interested columns
            browser.find_element_by_xpath("//a[@href='/people/"+SearchName+"/following/columns']").click()    
            # Sleep safety
            time.sleep(2)
            page_buttons = browser.find_elements_by_xpath("//button[@class='Button PaginationButton Button--plain']")
            # Loop through all the pages
            for i in range(len(page_buttons)):
                # Extend the list to store the information
                interestedcolumns.extend([x.text for x in browser.find_elements_by_xpath("//h2[@class='ContentItem-title']")])
                # Sleep to prevent page skipped before retrieving all data
                time.sleep(1)
                # To next page by pressing the next page button
                nextpage_buttons = browser.find_element_by_xpath("//button[@class='Button PaginationButton PaginationButton-next Button--plain']")
                nextpage_buttons.click()
                # Sleep and let next page load first
                time.sleep(2)
        
            if interestedcolumns != []:
                print("User's interested columns extracted!")
        
            # Switch to Get the list of user's starred questions
            browser.find_element_by_xpath("//a[@href='/people/"+SearchName+"/following/questions']").click()
            # Sleep safety
            time.sleep(2)
            page_buttons = browser.find_elements_by_xpath("//button[@class='Button PaginationButton Button--plain']")
            # Loop through all the pages
            for i in range(len(page_buttons)):
                # Extend the list to store the information
                interestedquestions.extend([x.text for x in browser.find_elements_by_xpath("//h2[@class='ContentItem-title']")])
                # Sleep to prevent page skipped before retrieving all data
                time.sleep(1)
                # To next page by pressing the next page button
                nextpage_buttons = browser.find_element_by_xpath("//button[@class='Button PaginationButton PaginationButton-next Button--plain']")
                nextpage_buttons.click()
                # Sleep and let next page load first
                time.sleep(2)
        
            if interestedquestions != []:
                print("User's interested questions extracted!")
            
            # Sleep safety
            time.sleep(2)
            
            # Exit the browser
            browser.quit()
            
            # Output to dictionary
            UserReport={}
            Columns=["User ID", "User name", "Location", "Industry", "Education", "About", "Achievements"]
            for i in range(len(Columns)):
                UserReport[Columns[i]]=UserInfo[i]
            UserReport["Interested topics"]=interestedtopics
            UserReport["Interested columns"]=interestedcolumns
            UserReport["Interested questions"]=interestedquestions
            
            with open("UserReport_"+SearchName+".json","w+",encoding="utf-8") as file:
                file.write(json.dumps(UserReport, ensure_ascii=False, indent=4))
            file.close()
            
            print("\nUser's report generated successfully! Check the output json for results!")
        
        except:
            print("\nUser not found, please check your id.")
            browser.close()
  
    
''' 
------------------------------------------------------------------
''' 
   
# Scroll function
# Reference: https://www.codenong.com/1144805/
def Scroll(explorer):
    explorer.execute_script("""
           (function () {
               var y = document.body.scrollTop;
               var step = 100;
               window.scroll(0, y);


               function f() {
                   if (y < document.body.scrollHeight) {
                       y += step;
                       window.scroll(0, y);
                       setTimeout(f, 50);
                   }
                   else {
                       window.scroll(0, y);
                       document.title += "scroll-done";
                   }
               }
               setTimeout(f, 1000);
           })();
           """)

def SearchQ(SearchQuestion):
    
    print("\nLoading ... Please wait")
    
    # Create URL
    url = f"https://www.zhihu.com/question/{SearchQuestion}"
    
    # Initialize browser
    browser=Driver_init("chromedriver.exe")
    browser.maximize_window()
    browser.get(url)
    
    # Wait for the website to load
    time.sleep(2)
    # Check the title to see whether 404 or not
    if "404" in browser.title:
        print("Question not found, please check your id.")
        browser.close()
    else:
        # Scroll through browser
        Scroll(browser)
        
        # To scroll till the end until no reloading is happening
        test = False
        while test==False:
            try:
                # This button only occurs in the end of the question until nothing can be load
                dummy_button = browser.find_element_by_xpath("//button[@class='Button QuestionAnswers-answerButton Button--blue Button--spread']")
                test = True
            except:    
                test = False
                
        # Sleep safety
        time.sleep(3)
        
        # Extract the website contents
        soup = retrievesource(browser)
        QuestionsAnswers = soup.findAll('div',class_="RichContent-inner")
        
        int=1
        ansDict={}
        ansDict["Title"]=soup.find('h1',class_="QuestionHeader-title").text
        for answer in QuestionsAnswers:
            ansDict[int]=answer.text
            int+=1
        ansDict["Total answers retreived:"]=str(int)
        with open("AnswersReport_"+SearchQuestion+".json","w+",encoding="utf-8") as file:
            file.write(json.dumps(ansDict, ensure_ascii=False, indent=4))
        file.close()
        
        browser.close()   #close the browser
            
        print(str(len(QuestionsAnswers))+" answers have been written into json!")
        
''' 
------------------------------------------------------------------
''' 

def main():
    
    ## Choices
    print ("Please choose your action: \n 1 User report by user id \n 2 Search answers of question \n 3 Exit")
    
    Choice = input ("Please enter 1 / 2 / 3 to proceed \n")
    
    if Choice == "1":
        SearchUser = input ("Please enter user id to be searched (You may use my id for testing: felixcat-77)\n")
        try:
            SearchU(SearchUser) # For testing
        except:
            print("\nUser not found, please check your question id.")
    
    elif Choice == "2":
        SearchQuestion = input ("Please input id of question to be searched (You can try using: 423389155) \n")
        try:
            SearchQ(SearchQuestion)
        except:
            print("\nSomething went wrong, please check your user id.")
    
    print("\nThanks for using! Goodbye!")
    
    
if __name__== '__main__':
    main()