#!/usr/local/bin/python
# encoding:utf-8
# Author : Jason.Wu
# Version : 1.0
# Date : 1/16/2019

import wx
import paramiko
import os
from stat import S_ISDIR as isdir

def download_remote(sftp, remote_path, local_path):
	"""Remote Download File"""
	remote_file = sftp.stat(remote_path)
	if isdir(remote_file.st_mode):
		# Download DIR
		check_local_dir(local_path)
		print('Download dir :' + remote_path)
		for remote_file_name in sftp.listdir(remote_path):
			sub_remote = os.path.join(remote_path, remote_file_name)
			sub_remote = sub_remote.replace('\\', '/')
			sub_local = os.path.join(local_path, remote_file_name)
			sub_local = sub_local.replace('\\', '/')
			download_remote(sftp, sub_remote, sub_local)
	else:
		# Download FILE
		print('Download file :' + remote_path)
		sftp.get(remote_path, local_path)

def remote_scp(host_ip, remote_path, local_path, username, password):
	t = paramiko.Transport((host_ip, 22))
	t.connect(username=username, password=password)  # Login Remote Server
	sftp = paramiko.SFTPClient.from_transport(t)  # SFTP Transfer Protocol
	download_remote(sftp, remote_path, local_path)
	t.close()

def check_local_dir(LOCAL_PATH):
	if not os.path.isdir(LOCAL_PATH):
		os.makedirs(LOCAL_PATH)

class MyFrame(wx.Frame):

	def __init__( self, parent ,title):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = title , pos = wx.DefaultPosition, size = wx.Size( -1, 300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		bSizer = wx.BoxSizer( wx.VERTICAL )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		self.m_staticText = wx.StaticText( self, wx.ID_ANY, u"Username :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.username = wx.TextCtrl( self, wx.ID_ANY, 'jason', wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_staticText, 0, wx.ALL, 5 )
		bSizer1.Add( self.username, 0, wx.ALL, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Password :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.password = wx.TextCtrl( self, wx.ID_ANY, '123456', wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		bSizer2.Add( self.m_staticText2, 0, wx.ALL, 5 )
		bSizer2.Add( self.password, 0, wx.ALL, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Host ip :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.hostip = wx.TextCtrl( self, wx.ID_ANY, '10.11.108.18', wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )
		bSizer3.Add( self.hostip, 0, wx.ALL, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Remote_path :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.remotepath = wx.TextCtrl( self, wx.ID_ANY, '/home/jason/work/FireNow-Nougat/rockdev/Image-rk3399_firefly_box', wx.DefaultPosition, wx.Size( 250, -1 ), 0 )
		bSizer4.Add( self.m_staticText4, 0, wx.ALL, 5 )
		bSizer4.Add( self.remotepath, 0, wx.ALL, 5 )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Local Path :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.localpath = wx.TextCtrl( self, wx.ID_ANY, './proc', wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_staticText6, 0, wx.ALL, 5 )
		bSizer5.Add( self.localpath, 0, wx.ALL, 5 )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		self.btn = wx.Button( self, wx.ID_ANY, u"Download", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.btn, 0, wx.ALL, 5 )

		bSizer.Add( bSizer1, 1, wx.EXPAND, 5 )
		bSizer.Add( bSizer2, 1, wx.EXPAND, 5 )
		bSizer.Add( bSizer3, 1, wx.EXPAND, 5 )
		bSizer.Add( bSizer4, 1, wx.EXPAND, 5 )
		bSizer.Add( bSizer5, 1, wx.EXPAND, 5 )
		bSizer.Add( bSizer6, 1, wx.EXPAND, 5 )
		self.SetSizer( bSizer )

		menuBar = wx.MenuBar()
		helpmenu = wx.Menu()
		about = wx.MenuItem(helpmenu, id = wx.ID_ABOUT, text = 'About\tF1', kind = wx.ITEM_NORMAL)
		helpmenu.Append(about)
		menuBar.Append(helpmenu, title="Help" )

		self.SetMenuBar(menuBar)
		self.Centre( wx.BOTH )

		self.Bind(wx.EVT_MENU, self.menuHandler)
		self.btn.Bind( wx.EVT_BUTTON, self.download )

	def download( self, event ):
		HOST_IP = self.hostip.GetValue()
		REMOTE_PATH = self.remotepath.GetValue()
		LOCAL_PATH = self.localpath.GetValue()
		USERNAME = self.username.GetValue()
		PASSWORD = self.password.GetValue()

		self.btn.Disable()
		remote_scp(HOST_IP, REMOTE_PATH, LOCAL_PATH, USERNAME, PASSWORD)
		self.btn.Enable()

	def menuHandler(self, event):
		id = event.GetId()
		if id == wx.ID_ABOUT :
			wx.MessageBox("Download Remote File!\n\n Version : 1.0\n\n Date:1/16/2019\n\n Author : Jason.Wu ",\
			"About...",wx.OK | wx.ICON_INFORMATION)

def main():
    app = wx.App()
    ex = MyFrame(None, title="Download Remote File")
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()