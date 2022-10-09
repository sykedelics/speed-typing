import sys
import random
import time
import mysql.connector

con=mysql.connector.connect(host='localhost', user='root', password='shubh', database='scoreboard')
if con.is_connected():
    print('connection succesful')

cur=con.cursor()
'''cur.execute('Create database ScoreBoard')
print('Query executed successfully')'''

def Menu():
    print('>>>>MENU<<<<')
    print('1. Rules')
    print('2. Play')
    print('3. Display Scores')
    print('4. delete record')
    print('5. Exit')
    try:
        n=int(input('enter your choice: '))
    except ValueError:
        print('wrong key pressed')
        n=int(input('enter your choice: '))
    if n==5:
        print('HUEHUE THNAKA 4 PLAYIN :DDD')
        sys.exit()
    if n==1:
        rules()
    if n==2:
        play()
    if n==3:
        read()
    if n==4:
        delete()

def rules():
    print('             Welcome')
    print('       Test Your Typing Skills')
    print('Type as many words as you can in under 60 seconds and check your score')
    print('            Enjoy lol!')
    Menu()

def makelist():
    '''makes the list of words from words.txt file'''
    wordlist=open('words.txt', 'r')
    li=[]
    for entry in wordlist:
        entry=entry.strip()
        li.append(entry)
    wordlist.close()
    return li

def randomword(li):
    #chooses random word
    return random.choice(li)

def read():
    cur=con.cursor()
    cur.execute("select * from speed")
    data=cur.fetchall()
    for i in data:
        print(i)
    print('<><><><><><><><><><><><><><><><><><><><><><>')
    print("Total number of participants=",cur.rowcount)
    print('<><><><><><><><><><><><><><><><><><><><><><>')
    Menu()

def delete():
    cur=con.cursor()
    s=input("Enter name of the player")
    query="Delete from speed where name='{}'".format(s)
    cur.execute(query)
    con.commit()
    print("record has been deleted successfully")
    Menu()
    
def play():
    record=[]
    while True:
        '''code for the actual game'''
        TimeUsed = 0.0
        TimeLeft = 0.0
        TotalWords = 0
        CorrectWords = 0
        listi= makelist()
        name=input('enter your name: ')
        while TimeUsed <= 60:
            word = randomword(listi)
            listi.remove(word)
            TimeLeft=60.0-TimeUsed
            print(TimeLeft)
            print(word)
            start= time.clock()
            inp = input('Enter the word:')
            end= time.clock()
            if inp==word:
                CorrectWords += 1
            TimeUsed += (end-start)
            TotalWords += 1
        print("TIMES UP!") 
        print('Total words typed: ', TotalWords)
        print('correct words: ', CorrectWords,'\t incorrect words: ', TotalWords-CorrectWords)
        raw = (TotalWords/TimeUsed)*60
        actual = (CorrectWords/TimeUsed)*60
        print('Your Raw Speed: ', raw,'\t Your Actual Speed: ', actual)
        if actual<20:
            print("bro your score is embarrassing")
        query="Insert into speed values('{}',{},{})".format(name,actual, raw)
        cur.execute(query)
        con.commit()
        
        data=[name, actual]
        record.append(data)
        c = input("do you wanna play again? (y/n)")
        if c=='n':
            break
    Menu()     
            
Menu()
