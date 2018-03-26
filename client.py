# This is the chat-client script of the multithreaded, python chat applicaiton. This uses Tkinter
import sys
from string import *
from socket import *
import select
from Tkinter import *
import thread
from random import randint
from modules.word import Word #importing the custom word class to read, input, and, update data
import pdb

#pdb.set_trace() #for debug mode

limit=80               #amount of lines kept inside the window
PORT=8888              #chose a high number random port that is not likely used by another app
#checks to see if the correct number of args have been passed
if len(sys.argv) != 2:
     print "Must enter the following: script, IP address of server"
     exit()
HOST= str(sys.argv[1])
#a function to have the client listen for received messages on the connection
def listening():
 global tekst,limit
 try:
   while 1:
     temp=s.recv(1024)+chr(10)
      #listen for messages, users and user status
     tekst.tag_config("a", foreground="#000000")
     tekst.tag_config("b", foreground="#000000")
     if limit%2==0:
       tekst.insert(END, temp, "b")
     else:
       tekst.insert(END, temp, "a")
     tekst.see(END)
     limit=limit-1
     if limit<0:
       tekst.delete(1.0, 2.0)
     #for updating the user list with client's usernames and status'
     if "('username:" in temp:
       userDisplay.insert(END,temp)
       userDisplay.see(END)
     #This is where the shutdown signal is executed
     print temp
     if "terminate client" in temp:
       print("terminating connection to server...")
       import tkMessageBox
       tkMessageBox.showerror("Chat","Your connection to the chat room has been terminated. Goodbye!")
       print("termination was terminated.")
       chatWindow.destroy()
 except:
   return
#a function for transmitting messages sent by the given username
def SayIt(event):
 global s, pole, username, limit, count
 temp=pole.get()
 pole.delete(0,END)
 try:
   #send the message to the server
   s.send(temp)
 except:
   #if the message cannot be sent notify the user that the server is not working
   import tkMessageBox
   tkMessageBox.showerror("Chat", "[server not available!]")
   sys.exit()
 return

try:
 s=socket(AF_INET, SOCK_STREAM)
 s.connect((HOST,PORT))
except:
 import tkMessageBox
 tkMessageBox.showerror("Chat", "[server not available!]")
 sys.exit()
chatWindow = Tk()
chatWindow.title("Chat")
chatWindow.resizable(width=FALSE, height=FALSE)
#setting the dimensions of the chat window
canv=Canvas(width=50, height=15)
import tkFont

temp="Py Chat"

#canv.coords(userList,10, 50, 240, 210)
#This is the text area that contains the dialog between the clients
import ScrolledText
tekst = ScrolledText.ScrolledText(height=25)
userDisplay = ScrolledText.ScrolledText(height=25, width=25)
tekst.config(fg="black", bg="#ffffff")
userDisplay.config(fg="black", bg="yellow")
tekst.grid(row=0, column=0)
#userListBox=Label(chatWindow,width=25, height=25, text=userArray, bg="purple")
userDisplay.grid(row=0, column=1)

#This is where the user can enter their message
pole = Entry(chatWindow)
pole.bind("")
pole.bind("<Return>", SayIt)
pole.config(width=70, fg="black", bg="#ffffff")
pole.grid()
import tkSimpleDialog
#When the client starts they are assigned a user name
username=tkSimpleDialog.askstring("Chat", "Enter your username to login:")
try:
 strip(username)
except:
 sys.exit()
if username=="":
 import tkMessageBox
    #if there is no user name entered, then the user cannot join the chat room
 tkMessageBox.showerror("Chat", "No user name entered. Cannot join chat room")
 sys.exit()
 #validate to see if the username already exists. If it does, assign another username **
 #Here is the logic for read/insert of username.txt files with the given username
 #1. Create a new instance of the word class
wordValue = Word()
 #2.If the username does exist in the file, check to see if it is in the blacklist.txt files
badCheck = wordValue.searchWord(username, "blacklist.txt")
print badCheck
 #3. Check to see if the user name already exists in the username.txt files
if badCheck == False:
     #userCheck = wordValue.searchWord(username, "test-username.txt")
     #if userCheck == False:
         #4. If the username is not in the blacklist.txt file and not in the username.txt file, insert the username into the username.txt files
 wordValue.insertWord(username, "username.txt")
    # else:
         #tkMessageBox.showerror("Chat", "This username already exists. Enter another username")
else:
 import tkMessageBox
 tkMessageBox.showerror("Chat", "You are on the blacklist. You cannot join the chat.")
 sys.exit()
pole.focus()

#send the username to the connected server
s.send(username)
#start a new thread for sending messages from this client
thread.start_new_thread(listening,())

chatWindow.mainloop()
