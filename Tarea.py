import imaplib,email,re,smtplib,csv
from getpass import getpass
from email.message import EmailMessage
from email.parser import HeaderParser
from time import sleep
from dateutil import parser

def menu():
    print(''' Tarea 5 Pablo Muñoz Poblete
            1-Importar Regex.
            2-Conseguir Message-ID.
            3-Validar correos.
            4- Salir
        ''')

def import_regex(regex_file):
    try:
        regex_list=[]
        with open(regex_file,'r') as file:
            reader=csv.reader(file)
            for line in reader:
                regex_list.append(line)
        #print(regex_list)
        return regex_list
    except Exception as e:
        print('Error: ',e)

def connect_mail(user,pwd):
    try:
        imap=imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(user,pwd)
        print('Se utilizara la bandeja de entrada para la revision del correo.')
        msg_count=imap.select('INBOX')[1][0]
        print('Se encontraron ',msg_count.decode('utf-8'), ' mensajes en la bandeja de entrada.')
        return imap
    except Exception as e:
        print('Error: ', e)
    



if __name__ == "__main__":
    try:
        regex_file=input('Ingrese el nombre del archivo a importar.')
        # regex_file='regex.csv'
        regex_list=import_regex(regex_file)
        user=input('Ingrese el correo a revisar: ')
        pwd=getpass('Ingrese la contraseña: ')
        client=connect_mail(user,pwd)
        for regex in regex_list:
            status,mails_id=client.search(None,'(FROM "' +regex[0]+'")')
            regex_date=parser.parse(regex[2]).date()
            print(regex_date)
            if status != 'OK':
                print('El correo',regex[0], 'no esta disponible')
                continue
            mails_id=mails_id[0].decode('utf-8').rsplit(' ')
            print('--------Comprobando el correo: ',regex[0],', con la regex: ',regex[1],'---------------------')
            for id in mails_id:
                res,msg = client.fetch(id,'(BODY[HEADER])')
                for msg_data in msg:
                    if isinstance(msg_data,tuple):
                        msg_content=email.message_from_bytes(msg_data[1])
                        print('Comprobando el mensaje',id,'con la regex',regex[1],'y la expresion',msg_content['Message-ID'][1:-1],'...')
                        match=re.match(regex[1],msg_content['Message-ID'][1:-1])
                        if match:#el mensaje es autentico
                        print('El correo es autentico')
                        else:
                            mail_date=parser.parse(msg_content['Date']).date()
                            if regex_date > mail_date:
                                print(regex_date,mail_date)
                                print('La fecha del mensaje es anterior a la registrada, es posible que la regex no corresponda ')
                            print('El correo podria ser falso')
            sleep(1)           
    except Exception as e:
        print('Error: ',e)