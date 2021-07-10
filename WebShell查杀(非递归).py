#-*- coding: UTF-8 -*-
import os;
import binascii;
from colorama import init, Fore, Back, Style;
import time;
import sys;
import multiprocessing;

reload(sys)
sys.setdefaultencoding('gbk')
Signature = [																	#特征码列表
"6576616C28",																	#6576616C28		eval(
"667075747328",																	#667075747328	fputs(
"73797374656D28",																#73797374656D28	system(
"61737365727428",																#61737365727428	assert(
"7368656C6C5F6578656328",														        #7368656C6C5F6578656328	shell_exec(	
"63686D6F6428",																	#63686D6F6428	chmod(
"61727261795F646966665F756B657928",												                #61727261795F646966665F756B657928	array_diff_ukey(
"6261736536345F6465636F646528"];												                #6261736536345F6465636F646528	base64_decode(
init(autoreset = True);

def shellSearchKill(path):
	allFile = set();
	for dirpath,dirnames,filenames in os.walk(path):
		for name in filenames:
			try:
				if os.path.splitext(name)[1] == ".php":
					openfile = open(os.path.join(dirpath,name), "r");
					data = openfile.read();
					ascii2bin = binascii.hexlify(data).upper();
					for sig in Signature :
						if ascii2bin.find(sig) != -1 :
							allFile.add(os.path.join(dirpath,name))
					openfile.close();
			except Exception as e:
				pass
	for str in allFile:
		print u"发现疑似WebShell:\033[1;31;40m " + str;

p = sys.argv[1];
if __name__=='__main__':
	dl = [];
	computerSystem = sys.platform;
	for i in range(65,91):
		temp = chr(i) + ":\\";
		if os.path.isdir(temp):
			dl.append(temp);
	if p == "-h" or p == "--help":
		print "\033[1;36;40mPlease select the search type.Such As:python xxx.py -h\n-f:Full Search\n-c [path]:Custom Search";
	elif p == "-f":
		if computerSystem == "win32" :
			print "\033[1;36;40mYour Computer System is Windwos,Full Searcheing..."
			pool = multiprocessing.Pool(len(dl));
			star = 	time.time();
			for i in dl:
				pool.apply_async(shellSearchKill,args=(i,))
			pool.close()
			pool.join();
			end = time.time();
			print u"共耗时：" + str(end - star) + u"秒";
		elif computerSystem.find("linux") != -1 :
			print "\033[1;36;40mYour Computer System is Unix/Liunx,Full Searcheing..."
			star = 	time.time();
			shellSearchKill("/")
			end = time.time();
			print u"共耗时：" + str(end - star) + u"秒";
	elif p == "-c":
		p = sys.argv[2];
		star = 	time.time();
		shellSearchKill(p)
		end = time.time();
		print u"共耗时：" + str(end - star) + u"秒";
	else:
		print "\033[1;31;40mUnknow Commond " + p + " Please input -h or --help to view help.";
