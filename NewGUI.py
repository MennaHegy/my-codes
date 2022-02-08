from tkinter import *
from tkinter import messagebox
from datetime import datetime
import subprocess, sys
import tkinter.font
import os
import pickle
import pi_face_recognition_noarg_class
import Register_Haar_live_class

p = open("/home/pi/Desktop/finished_project/logfile.pickle", "rb")
log = pickle.load(p)

window = Tk()
window.title("Face Recognition In A Two Way Security System")
window.configure(background="bisque2",width=700,height=700)
window.resizable(0,0)
window.geometry('+100+150')

#Exit btn   
def close_window():
    p = open("/home/pi/Desktop/finished_project/logfile.pickle", "wb")
    p.write(pickle.dumps(log))
    p.close()
    window.destroy()
    raise SystemExit

def Reg_new_user():
    class Register(Frame):
        def __init__(self,master):
            Frame.__init__(self, master)
            self.grid()
            self.create_widgets()
            
        def create_widgets(self):
        # create user label
            self.user_lbl_reg = Label(self, text = "New User Name: ")
            self.user_lbl_reg.grid(pady = 5,padx=20,row =0, column = 0, columnspan = 2, sticky = W)
            # create user entry
            self.user_ent_reg = Entry(self)
            #self.user_ent_reg.config(state=NORMAL)
            self.user_ent_reg.grid(pady = 5,padx=20,row = 0, column = 1, sticky = W)
            #create Ps Label
            self.pw_lbl_reg = Label(self, text = "Enter Password: ")
            self.pw_lbl_reg.grid(pady = 5,padx=20,row = 1,column = 0, sticky = W)
            # Create Ps Entry
            self.pw_ent_reg = Entry(self,show="*")
            self.pw_ent_reg.grid(pady = 5,padx=20,row = 1, column = 1, sticky = W)
            #self.pw_ent_reg.config(state=NORMAL)
            self.pw_lbl2_reg = Label(self, text = "Confirm Password: ")
            self.pw_lbl2_reg.grid(pady = 5,padx=20,row = 2,column = 0, sticky = W)
            # Create Ps Entry
            self.pw_ent2_reg = Entry(self,show="*")
            self.pw_ent2_reg.grid(pady = 5,padx=20,row = 2, column = 1, sticky = W)
            #Create Submit button
            self.reg_btn = Button(self, text = "Register", command = self.reveal)
            self.reg_btn.grid(pady = 5,padx=20,row = 3,column = 0, sticky = W)
            self.cncl_btn = Button(self, text = "Cancel", command = self.close_win)
            self.cncl_btn.grid(pady = 5,padx=20,row = 3,column = 1, sticky = W)
            # Create Txt
            
            self.statein = Label(self,text="",fg="black")
            self.statein.grid(pady = 5,padx=20,row = 4,column = 0,columnspan=2,sticky=W)
            

        def close_win(self):
            #Admin().root.deiconify()
            root_reg.destroy()
        def reveal(self):
            # Get what the user typed into the ps entry
           self._newuser = self.user_ent_reg.get()
           self._newpass = self.pw_ent_reg.get()
           self._conf_newpass = self.pw_ent2_reg.get()
           
           if self._newpass == self._conf_newpass:
               self.Reg = Register_Haar_live_class.Reg(self._newuser,self._newpass)
               
               if self.Reg.Check() is 1:
                   self.statein.config(text = "UserName Already Registered",fg="red")
                   self.user_ent_reg.delete(0, "end")
                   self.pw_ent_reg.delete(0, "end")
                   self.pw_ent2_reg.delete(0, "end")
                   log.append("user: {} already registered at {}".format(self._newuser,datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
               else:
                   self.statein.config(text = "please face the camera\n press q to abort",fg="black")
                   self.statein.update_idletasks()
                   self._newuser_reg = self.Reg.Start()
                   if  self._newuser_reg is 1:
                       self.statein.config(text = "Registeration Succssful",fg="green")
                       self.user_ent_reg.delete(0, "end")
                       self.pw_ent_reg.delete(0, "end")
                       self.pw_ent2_reg.delete(0, "end")
                       log.append("new user: {} with password: {} registered at {}".format(self._newuser,self._newpass,datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                   elif self._newuser_reg is 0:
                       self.statein.config(text = "operation aborted",fg="red")
                       self.user_ent_reg.delete(0, "end")
                       self.pw_ent_reg.delete(0, "end")
                       self.pw_ent2_reg.delete(0, "end")
                       log.append("registeration aborted at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                   else:
                       self.statein.config(text = "camera timed out!\n try again!",fg="red")
                       self.user_ent_reg.delete(0, "end")
                       self.pw_ent_reg.delete(0, "end")
                       self.pw_ent2_reg.delete(0, "end")
                       log.append("camera timed out at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


           else:
               self.statein.config(text = "Mismatched passwords!",fg="red")
               log.append("mismatched passwords at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    root_reg = Tk()
    root_reg.title("Admin Login")
    root_reg.configure(width=450,height=450)
    root_reg.geometry("+250+250")
    log.append("admin logged in at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    app_reg = Register(root_reg)
    root_reg.mainloop()

#Reg btn
def Admin():
    class Application(Frame):
        def __init__(self, master):
            Frame.__init__(self, master)
            self.grid()
            self.create_widgets()

        def create_widgets(self):
        # create user label
            
            self.reg_btn = Button(self, text = "Register New User", command = self.open_reg_NU)
            self.reg_btn.grid(pady = 5,padx=20,row = 0,column = 0, sticky = W)
            
            self.log_btn = Button(self, text = "View Log File", command = self.openlog)
            self.log_btn.grid(pady = 5,padx=20,row = 1,column = 0, sticky = W)
            # Create Txt
            self.logout_btn = Button(self, text = "Logout", command = self.logout)
            self.logout_btn.grid(pady = 5,padx=20,row = 2,column = 0, sticky = W)
            #window.withdraw()
        def logout(self):
            log.append("admin logged out at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            #window.deiconify()
            User.delete(0, "end")
            Pass.delete(0, "end")
            state.config(text = "logout success!",fg="green")
            root.destroy()
            
        def open_reg_NU(self):
            #root.withdraw()
            Reg_new_user()
        
        def openlog(self):
            self.mylog = open("log_file.txt","w+")
            for i in log:
                self.mylog.write(i+"\n")
            self.mylog.close()
            self.opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([self.opener,"log_file.txt"])

    if User.get()=='Ahmed' and Pass.get() == "ahmed":
        
        btns_mode(0)

        state.config(text = "Please wait. . .",fg="black")
        state.update_idletasks()
        
        admin_Rec = pi_face_recognition_noarg_class.Rec(User.get(),Pass.get())
            
        state.config(text = "Please face the camera\n press q to stop",fg="black")
        state.update_idletasks()
        admin_camcheck = admin_Rec.Start()
        if admin_camcheck is 1:
            btns_mode(1)
            state.config(text = "Admin Access Granted!",fg="green")
            root = Tk()
            root.title("Admin Login")
            root.configure(width=450,height=450)
            root.geometry("+200+200")
            log.append("admin logged in at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            app = Application(root)
            root.mainloop()
            
        elif admin_camcheck is 0:
            state.config(text = "Admin Access Denied!",fg="red")
            log.append("admin faild login at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            btns_mode(1)

        elif admin_camcheck is 2:
            state.config(text = "operation stopped!",fg="red")
            log.append("admin login aborted at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            btns_mode(1)
        else:
            state.config(text = "camera timed out!\n try again!",fg="red")
            log.append("admin login timed out at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            btns_mode(1)

    # End of new Reg btn                
    else:
        state.config(text = "wrong administrator credintals!",fg="red")
        messagebox.showinfo("Alert !","Please Use Your Adminstrator Credintals or Log In As A User")
        log.append("admin faild login at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

#new Log  btn
def Log_In():
    btns_mode(0)
    
    state.config(text = "Please wait. . .",fg="black")
    state.update_idletasks()
    
    _user = User.get()
    _pass = Pass.get()
    Rec = pi_face_recognition_noarg_class.Rec(_user,_pass)
    
    Check = Rec.CheckPass()
    if Check is 2:
        state.config(text = "Wrong Username or Password!",fg="red")
        log.append("user: {} entered wrong password: {} at {}".format(_user,_pass,datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif Check is 1:
        state.config(text = "All filds are required!",fg="red")
        log.append("user entered missing fields at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    else:
        state.config(text = "Please face the camera\n press q to stop",fg="black")
        state.update_idletasks()
        _camcheck = Rec.Start()
        if _camcheck is 1:
            state.config(text = "Access Granted!",fg="green")
            log.append("access granted for user: {} at {}".format(_user,datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        elif _camcheck is 0:
            state.config(text = "Access Denied!",fg="red")
            log.append("access denied for username: {}, password: {} at {}".format(_user,_pass,datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        elif _camcheck is 2:
            state.config(text = "operation stopped!",fg="red")
            log.append("user login aborted at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            state.config(text = "camera timed out!\n Try gain!",fg="red")
            log.append("user login timed out at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    btns_mode(1)

def btns_mode(i):
    if i is 1:
        user_btn['state'] = 'normal'
        admin_btn['state'] = 'normal'
        exit_btn['state'] = 'normal'
        about_btn['state'] = 'normal'
    else:
        user_btn['state'] = 'disabled'
        admin_btn['state'] = 'disabled'
        exit_btn['state'] = 'disabled'
        about_btn['state'] = 'disabled'

#about   btn
def about():
    class Application(Frame):
        def __init__(self, master):
            Frame.__init__(self, master)
            self.grid()
            self.create_widgets()

        def create_widgets(self):
            # create user label
            self.user_lbl_log = Label(self, text = "Project Supervised By Prof.Dr.Rehab Farouk Abdelkader, Computer & Control Engineering dept.")
            self.user_lbl_log.grid(row =0, column = 0, columnspan = 2, sticky = W)
    #main
    root1 = Tk()
    root1.title("about")
    root1.geometry("600x100+120+250")

    root1.resizable(0,0)
    #root1.configure(background="bisque2",width=700,height=700)
    #create your obj
    app = Application(root1)
    root1.mainloop()
# End of about btn                

#label Title#
Label(window,text="Username",bg="bisque2",fg="black",font="Times 16 bold").grid(padx=15,row=0,column=0,sticky=W)
#text entery box#
User=Entry(window,width=20,bg="white")
User.grid(padx=15,row=1,column=0,sticky=W)
#label pass#
Label(window,text="Password",bg="bisque2",fg="black",font="Times 16 bold").grid(row=0,column=2,sticky=W)
#text entery box#
Pass=Entry(window,width=20,bg="white",show="*")
Pass.grid(row=1,column=2,sticky=W,padx=3)

#confirm Button #
user_btn = Button(window,text="User Log In",font="Times 13 bold",width=8,command= Log_In)
user_btn.grid(padx=5,pady=5,row=4,column=1,sticky=W)
admin_btn = Button(window,text="Admin Log In",font="Times 13 bold",width=10,command= Admin)
admin_btn.grid(pady=5,row=5,column=1,sticky=W)

#New regestration button #
#Button(window,text="Regestration",width=10,command= Reg).grid(row=3,column=1,sticky=W)
# About btn
about_btn = Button(window,text="about",font="Times 13 bold",width=10,command= about)
about_btn.grid(padx=20,row=9,column=0,sticky=W)

#exit button#
exit_btn = Button(window,text="Exit",font="Times 13 bold",width=6,command= close_window)
exit_btn.grid(padx=20,row=9,column=2,sticky=W)

state = Label(window,text="",bg="bisque2",fg="black")
state.grid(row = 3,column = 1,columnspan = 2,sticky=W)

window.mainloop()