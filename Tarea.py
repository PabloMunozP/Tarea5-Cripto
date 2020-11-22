import imaplib,email,webbrowser,os,string
from email.header import decode_header

correo_personal= 'frosty98.pmo@gmail.com'
password='tzsvnonchwmkmajs'
correo_testeo='noreply@redditmail.com '


def get_IDs(correo,password):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(correo,password)
    messages_count = imap.select('INBOX')[1]
    status,mails_id=imap.search(None,'(FROM "noreply@redditmail.com")')
    mails_id=str(mails_id)[3:-2].rsplit(' ')
    outFile=open('Message-IDs.txt','w')
    for id in mails_id:
        print(id)
        res,msg = imap.fetch(id,'(RFC822)')
        for msg_data in msg:
            if isinstance(msg_data,tuple):
                msg_= email.message_from_bytes(msg_data[1])
                print(msg_['Message-ID'],'\n')
                outFile.write(msg_['Message-ID'][1:-1]+'\n')
    
    outFile.close()



if __name__ == "__main__":
    print('El correo utilizado es: ',correo_personal,' y se revisaran los correos provenientes de: ',correo_testeo )
    get_IDs(correo_personal,password)