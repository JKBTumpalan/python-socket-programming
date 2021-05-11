from os import sendfile
import socket
import time

HOST = "127.0.0.1"
PORT = 65432

vowels = ['a', 'e', 'i', 'o', 'u']

#Get piglatin of a WORD
def get_piglatin(pig_string):
    word_index = 0
    if pig_string[0] in vowels: #If first letter is vowel, just add 'ay'.
        return pig_string + 'ay'
    while (pig_string[word_index] not in vowels): #Else, iterate until the first consonant substring
        if(word_index == len(pig_string) - 1):
            return pig_string + 'ay'
        word_index += 1

    #Generate new string according to iterated index.    
    new_string = pig_string[word_index: len(pig_string)] + pig_string[0: word_index] + "ay"

    return new_string

#Iterative call of get_piglatin to translate the whole sentence to Pig Latin language.
def pig_translate(whole_pig_string):
    pig_word_list = []
    for word in whole_pig_string.split(" "):
        pig_word_list.append(get_piglatin(word).lower())

    return ' '.join(pig_word_list)

#Create socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    #Enable socket address re-use
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #Bind to host and port.
    s.bind((HOST, PORT))
    s.listen()
    exit_status = 0

    while exit_status != -1:
        conn, addr = s.accept()

        with conn:
            #Initial connection, connected to a socket.
            print('Connected by', addr)
            conn.sendall(b'Acknowledged.')

            #Block program by waiting data.
            while True:
                #Receive message from client
                data = conn.recv(1024)
                print(f"Received data: {data.decode(encoding='utf-8')}.")
                #Translate message
                if exit_status % 2 == 0:
                    pig_string = pig_translate(str(data.decode('utf-8')))
                    print(f"Translated to: {pig_string}.")
                else:
                    pig_string = data.decode('utf-8')
                if not data:
                    break

                #Send the translated message.
                print("Sending translated data..")
                conn.sendall(bytes(pig_string, encoding="utf-8"))
                exit_status += 1

                time.sleep(0.5)
                if exit_status % 2 == 1:
                    #Send choice continuation prompt
                    conn.sendall(bytes("Translate again? (Y/N)", encoding="utf-8"))
                    while True:
                        #Wait for continuiation choice.
                        data2 = conn.recv(1024)
                        if data2:
                            #Receive choice, break if N.
                            print(f"Received client choice: {data2.decode('utf-8')}")
                            data2string = data2.decode('utf-8')
                            if (data2string == 'N' or data2string == 'n'):
                                exit_status = -1
                            break

                if (exit_status == -1): break
                exit_status += 1