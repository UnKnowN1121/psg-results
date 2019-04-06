import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time

gmail_user = 'sender@senderemail.com'  
gmail_password = 'senderemailpassword'

sent_from = gmail_user  
to = ['receiver@receiveremail.com']  
subject = 'results'  
body = "Test"

def gethtml(rollno):
    url = "http://ecampus.psgcas.ac.in/ResRollNo.aspx"
    headers = {'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",'cache-control': "no-cache" }
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"BtnSubmit\"\r\n\r\nSubmit\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"TxtRollNo\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__EVENTVALIDATION\"\r\n\r\n/wEdAAMtrcwPqeCGCJ963lVpIfCPvmRPPGfMLhuzEQNFmvZIPezM2nXGH3Ud2OBKRKYDwA4mWBXsfXmTzYSXlhYCkxqSSB8kMLnv+DYvLRbsPNI+MA==\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATE\"\r\n\r\n/wEPDwUKLTcyODI3MDAxNA9kFgICAw9kFgICBQ8PZBYCHgZvbmJsdXIFK2phdmFzY3JpcHQ6Q2FsbE1lKCdUeHRSb2xsTm8nLCAnVHh0Um9sbE5vJylkZOwzmjgcDU3VYpZuxL7uL3TSG6kDjoCZEGLk1HQfGtQ1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"%(rollno)
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.text.find('Name of the Candidate') < 0:
	    return "NO"

    try:
        fout = open('%s.htm'%(rollno), 'w')
    except:
        print('Could not open output file\n')
        return "NO"
    fout.writelines(response.text)
    fout.close()
    return "YES"

def sendfiles():
    msg = MIMEMultipart()
    files_list = ['15BCA002','15BCA006','15BCA022','15BCA035','15BCA040','15BCA050','15BCA012']
    for efiles in files_list:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open("%s.htm"%(efiles), "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s.html"'%(efiles))
        msg.attach(part)

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, msg.as_string())#email_text)
        server.close()

        print ('Email sent!')
        return "YES"
    except:  
        print ('Something went wrong...')
        return "NO"

if __name__ == "__main__":
    while True:
        print("Starting a round")
        res1 = gethtml("15BCA002")
        res2 = gethtml("15BCA006")
        res3 = gethtml("15BCA022")
        res4 = gethtml("15BCA035")
        res5 = gethtml("15BCA040")
        res6 = gethtml("15BCA050")
        res7 = gethtml("15BCA012")
        if res1 == res2 == res3 == res4 == res5 == res6 == "YES":
            print("FETCHED RESULTS, EMAILING THEM" )
            snd = sendfiles()
            if snd == "YES":
                break
        print("Sleeping")
        time.sleep(100)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
       # server.sendmail(sent_from, to, "Still working")#email_text)
        server.close()
