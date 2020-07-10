from selenium import webdriver  
from time import sleep     
import smtplib, ssl         #for sending emails

#email stuff
port = 465
password = "ML5WHkg7X4cSKjG"
sender = "gthousingnotify17@gmail.com"
receiver = "charlieliu2222@gmail.com"

class Scraper:
    def __init__(self): #creating webscraper
        self.driver = webdriver.Firefox(executable_path="C:\\Users\\Charlie\\Documents\\Coding\\geckodriver.exe") 
        self.driver.get("http://housing.gatech.edu/available-rooms")    #Navigates to the available housing website


        self.dorms = ["Brown", "Hopkins", "Hanson", "Harris", "Harrison", "Perry", "Field", "Glenn", "Matheson"] #dorms to look out for
        
    def search(self):
        i = 1   #iteration variable
        while True:                 #find element   look for tbody tag, it should have rowgroup attribute, go through child nodes, look at their child first element, which
                                    # is the dorm name
            dormName = self.driver.find_element_by_xpath("//*tbody[@role=\"rowgroup\"]/child::tr[{}]/child::td[1]".format(i)).text
            gender = self.driver.find_element_by_xpath("//*tbody[@role=\"rowgroup\"]/child::tr[{}]/child::td[3]".format(i)).text #third element is gender
            if dormName is None:    # theoretically the loop stops when i variable is too high and dormName cannot be assigned to any element anymore
                break
            if dormName not in self.dorms or (gender != "Male" or gender != "Dynamic"): #Keeps loop going if row isn't what is desired
                i += 1
                continue
            else:      #if it hits this, then it's time to send email with link
                emailtext = """\
                                Subject: Housing Opening at {}

                                There is an opening in {} for you right now. Check your housing. 
                                https://starrez.housing.gatech.edu/StarRezPortalX/1567CF75/27/335/SELF_ASSIGN-Term_Selector """.format(dormName, dormName)
                context = ssl.create_default_context()      #email stuff i copied pasted
                with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                    server.login(sender, password)  #variables at top
                    server.sendmail(sender, receiver, emailtext)    #variables at top

    def refresh(self):
        self.driver.refresh()

houser = Scraper()            
while True:
    houser.search() #search
    sleep(600)  #wait 10 minutes
    houser.refresh()    #Refresh and loop
