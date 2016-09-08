#!D:\Python27\python.exe
#-*- coding: utf-8 -*-

#add something

'''
Telnet远程登录：Windows客户端连接Linux服务器
TFTP传输文件：Linux客户端连接Windows服务器
'''

from Tkinter import *
import tkMessageBox

import telnetlib



# 配置选项

#板
clientPath = '/'
srcFile = 'sepuyi'
tftpServerIP = '192.168.1.104'
tftpClientIP = '192.168.1.109' # Telnet服务器IP
userName = 'root'   # 登录用户名
passWord = ''  # 登录密码
Finish = '# '      # 命令提示符（标识着上一条命令已执行完毕）

'''
#PC
clientPath = './zh'
srcFile = 'sepuyi'
tftpServerIP = '192.168.1.104'
tftpClientIP = '192.168.1.109' # Telnet服务器IP
userName = 'student'   # 登录用户名
passWord = '111111'  # 登录密码
Finish = '$ '      # 命令提示符（标识着上一条命令已执行完毕）
'''

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.serverLabel = Label(self, text=u'服务器')
        self.serverLabel.grid(row=0,column=0)
        self.serverIPLabel = Label(self, text=u'IP地址:')
        self.serverIPLabel.grid(row=0,column=1)
        serverIPInputStr = StringVar()
        serverIPInputStr.set(tftpServerIP)
        self.serverIPInput = Entry(self, textvariable = serverIPInputStr)
        self.serverIPInput.grid(row=0,column=2)
        self.localLabel = Label(self, text=u'(本机)')
        self.localLabel.grid(row=1,column=0)

        self.Label00 = Label(self, text=u'----------')
        self.Label00.grid(row=2,column=0)
        self.Label01 = Label(self, text=u'----------------------')
        self.Label01.grid(row=2,column=1)
        self.Label02 = Label(self, text=u'----------------------')
        self.Label02.grid(row=2,column=2)
        
        self.serverLabel = Label(self, text=u'客户端')
        self.serverLabel.grid(row=3,column=0)
        self.clientIPLabel = Label(self, text=u'IP地址:')
        self.clientIPLabel.grid(row=3,column=1)
        clientIPInputStr = StringVar()
        clientIPInputStr.set(tftpClientIP)
        self.clientIPInput = Entry(self, textvariable = clientIPInputStr)
        self.clientIPInput.grid(row=3,column=2)
        self.serverLabel = Label(self, text=u'(核心板)')
        self.serverLabel.grid(row=4,column=0)
        self.targetLabel = Label(self, text=u'客户端路径:')
        self.targetLabel.grid(row=4,column=1)
        clientPathInputStr = StringVar()       
        clientPathInputStr.set(clientPath)
        self.clientPathInput = Entry(self, textvariable = clientPathInputStr)
        self.clientPathInput.grid(row=4,column=2)
        
        self.Label10 = Label(self, text=u'----------')
        self.Label10.grid(row=5,column=0)
        self.Label11 = Label(self, text=u'----------------------')
        self.Label11.grid(row=5,column=1)
        self.Label12 = Label(self, text=u'----------------------')
        self.Label12.grid(row=5,column=2)

        self.srcLabel = Label(self, text=u'文件名:')
        self.srcLabel.grid(row=6,column=1)
        srcInputStr = StringVar()
        srcInputStr.set(srcFile)
        self.srcInput = Entry(self, textvariable = srcInputStr)
        self.srcInput.grid(row=6,column=2)

        #self.quitButton = Button(self, text=u'退出', command=self.quit)
        #self.quitButton.grid(row=7,column=0)
        self.getButton = Button(self, text=u'服务器->客户端', command=self.getFile)
        self.getButton.grid(row=7,column=1)
        self.putButton = Button(self, text=u'客户端->服务器', command=self.putFile)
        self.putButton.grid(row=7,column=2)

    def getFile(self):
        #telnet 登陆
        # 连接Telnet服务器
        tn = telnetlib.Telnet(self.clientIPInput.get())
        # 输入登录用户名
        tn.read_until('login: ')
        tn.write(userName + '\n')
        # 输入登录密码
        tn.read_until('Password: ')
        tn.write(passWord + '\n')

        # 登录完毕后，执行cd命令
        tn.read_until(Finish)
        tn.write('cd' + ' ' + self.clientPathInput.get() + '\n')
        tn.read_until(Finish)

        #板 linux       
        tn.write('tftp -g -r' + ' ' + self.srcInput.get() + ' ' + self.serverIPInput.get() + '\n')
        tn.read_until(Finish)

        #pc linux
        #tn.write('tftp' + ' ' + self.serverIPInput.get() + '\n')
        #tn.read_until("tftp>")
        #tn.write('get' + ' ' + self.srcInput.get() + '\n')
        #tn.read_until("tftp>")
        
        # ls命令执行完毕后，终止Telnet连接（或输入exit退出） 
        tn.close() # tn.write('exit\n')
        tkMessageBox.showinfo(u'提示', u'服务器->客户端 文件传输成功!')

    def putFile(self):
        #telnet 登陆
        # 连接Telnet服务器
        tn = telnetlib.Telnet(self.clientIPInput.get())
        # 输入登录用户名
        tn.read_until('login: ')
        tn.write(userName + '\n')
        # 输入登录密码
        tn.read_until('Password: ')
        tn.write(passWord + '\n')

        # 登录完毕后，执行cd命令
        tn.read_until(Finish)
        tn.write('cd' + ' ' + self.clientPathInput.get() + '\n')
        tn.read_until(Finish)

        #板 linux
        tn.write('tftp -p -l' + ' ' + self.srcInput.get() + ' ' + self.serverIPInput.get() + '\n')
        tn.read_until(Finish)

        #pc linux       
        #tn.write('tftp' + ' ' + self.serverIPInput.get() + '\n')
        #tn.read_until("tftp>")
        #tn.write('put' + ' ' + self.srcInput.get() + '\n')
        #tn.read_until("tftp>")
        
        # ls命令执行完毕后，终止Telnet连接（或输入exit退出）
        tn.close() # tn.write('exit\n')
        tkMessageBox.showinfo(u'提示', u'客户端->服务器 文件传输成功!')

app = Application()
# 设置窗口标题:
app.master.title(u'更新程序')
# 主消息循环:
app.mainloop()
