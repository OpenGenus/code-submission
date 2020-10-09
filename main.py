import requests
from lxml import html
from time import sleep # to reduce the number of requests per second
import json

# see start and end pages and specify in range

def returnAcceptedSubmissions(Username, number_of_pages):

    for foo in range(1,number_of_pages):
        sleep(5)
        # change address below accordingly
        page = requests.get('https://codeforces.com/submissions/' + Username + '/page/'+ str(foo))
        tree = html.fromstring(page.text)
    
        res = []

        #The data to obtain the URL of submissions
        checkStatus = tree.xpath('//*[@id="pageContent"]/div[4]/div[6]/table/tr[position() > 1]/td[1]/*/@class')
        verdict = tree.xpath('//*[@id="pageContent"]/div[4]/div[6]/table/tr[position() > 1]/td[6]/span/@submissionverdict')
        contestID = tree.xpath('//*[@id="pageContent"]/div[4]/div[6]/table/tr[position() > 1]/td[4]/a/@href')
        problemID = tree.xpath('//*[@id="pageContent"]/div[4]/div[6]/table/tr[position() > 1]/td[1]/*/text()')
        problem_name = []
        #Getting the contest ID

        
        for i in range(len(contestID)):
            r = list(map(str,contestID[i].split("/")))
            
            problem_name.append(r[2] + r[4])
            contestID[i] = r[2]

           

        for i in range(len(problemID)):
            res.append([contestID[i],verdict[i], problemID[i], checkStatus[i], problem_name[i]])
           

        for i in range(len(res)):
            # change verdict or don't specify at all
            # "view-source" neccessary as few submissions are not available(hidden-source)
            if res[i][1] == "OK" and res[i][3] == "view-source":
                
                solutionPage = requests.get('https://codeforces.com/contest/'+ res[i][0]+'/submission/'+ res[i][2])
                tree2 = html.fromstring(solutionPage.text)
                
                # path to the actual submission
                address = './/div[@id="pageContent"]/div[@class="roundbox SubmissionDetailsFrameRoundBox-'+res[i][2]+'"]/pre[@id="program-source-text"]//text()'
                
                code = tree2.xpath(address)

                lines = code[0].split("\r\n")

                #saving the code in a outfile
                save_data(lines, res[i][4])
                sleep(5)
            


def save_data(sub_data, file_name):
    with open(file_name + '.txt', 'a') as sub_outfile:
        json.dump(sub_data, sub_outfile)
    return



Username = input("Enter the username: ") #Username
Number_of_pages = int(input("Enter the number of pages: ")) #specify the total number of pages to inspect. Should be less than or equal to the total number.

#running the program
returnAcceptedSubmissions(Username,Number_of_pages)
