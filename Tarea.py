import imaplib,email,re,smtplib
from email.message import EmailMessage

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
    regex=[]
    for id in mails_id:
        print(id)
        res,msg = imap.fetch(id,'(RFC822)')
        for msg_data in msg:
            if isinstance(msg_data,tuple):
                msg_= email.message_from_bytes(msg_data[1])
                print(msg_['Message-ID'],'\n')
                regex.append((id,msg_['Message-ID'][1:-1]))
                outFile.write(msg_['Message-ID'][1:-1]+'\n')
    outFile.close()
    return regex

def get_regex(FileName):
    inFile = open(FileName,'r')
    line = inFile.readline()
    line = line.rsplit(',')
    return line
    
def send_mail():
   pass

def menu():
    print(''' Tarea 5 Pablo Muñoz Poblete
            1- Obtener los Message IDs.
            2- Comprobar IDs con regex importada.
            3- Suplantar el correo 
            4- Revisar alertas
            5- Salir
        ''')

if __name__ == "__main__":
    try:
        while True:
            menu()
            op=input('Ingresa la opcion deseada: ') 
            while op not in ['1','2','3','4','5']:
                op=input('Ingresa la opcion deseada: ')
            if op == '1':
                print('El correo utilizado es: ',correo_personal,' y se revisaran los correos provenientes de: ',correo_testeo )
                msg_ids=get_IDs(correo_personal,password)
            if op == '2':
                if not msg_ids:
                    print('Debe obtener los Message-ID primero')
                else:
                    regex=get_regex('regex.txt')#regex,correo,fecha
                    print('Chequeando si los Message-ID corresponden con el regex entregado...')
                    for id in msg_ids:
                        #id, msg_id
                        match=re.match('r'+regex,id[1])
                        if match:#el msg_id es correcto
                            print('El correo cumple con la regex y su Message_ID es:',id[1])
                        else:
                            print('El correo no cumple con la regex y su Message_ID es: ',id[1])
            if op == '3':
                send_mail()
            if op == '4':
                pass 
            if op == '5':
                exit()       
    except KeyboardInterrupt :
        exit()
    