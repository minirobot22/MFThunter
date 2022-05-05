#!/usr/bin/env python3

# MFThunter.py V1.0 (BETA Version)
# Auther: Osama Radwan
# LinkedIn: https://www.linkedin.com/in/osama-mustafa
# More Features to Come


import sqlite3
import pandas as pd
from pathlib import Path
import glob
import getopt
import os
import sys
import Levenshtein


def print_usage():
    print('Usage: ' + os.path.basename(sys.argv[0]) + ' -m [method_number]' + ' [options]')
    print(' ')
    print('Options:')
    print('        -m [1,2], --method [1,2]   hunt method, specify 1 for Levenshtein distance (measure similarity between two executables)')
    print('                                                specify 2 for checking all duplicate executables located in different directories')
    print('        -h, --help                 Show this help')
    print('        -p, --path                 specify the folder path which contain MFT files in CSV format')
    print('        -d, --distance             mandatory for method = 1, specify the Levenshtein distance, a value of 1 is recommended')
    print(' ')
    print('Examples:')
    print('  ' + os.path.basename(sys.argv[0]) + ' -m 1 -p /home/MFT/ -d 1')
    print('  ' + os.path.basename(sys.argv[0]) + ' -m 2 -p /home/MFT/ ')
    print(' ')

# Keep all args but the first
argument_list = sys.argv[1:]

options = "hm:p:d:"
long_options = ["help","method","path","distance"]

if len(argument_list) < 1:
	print_usage()
	sys.exit(2)

def lev(path,distance):
	#Create the DB
	if os.path.isfile('data.db'):
		os.remove('data.db')
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
	else:
		Path('data.db').touch()
		conn = sqlite3.connect('data.db')
		c = conn.cursor()
	#Get CSV files list from a folder
	MFT_files = glob.glob(path + "/*.csv")
	if not MFT_files:
		print("error reading MFT files, check the path specified")
		sys.exit(2)

	print("Please wait ... it might take a while, depending on the the Size of your MFT files \r")
	#Specify columns to be loaded
	columns = ["ParentPath","FileName","Extension"]

	#Read MFT files and concat them in single dataframe
	def readcsv(params):
	    return pd.read_csv(params,usecols=columns)

	df = pd.concat(map(readcsv, MFT_files))

	#convert the dataframe to SQL Tables
	df.to_sql("df",conn, if_exists='append', index = False)
	c.execute('''SELECT DISTINCT FileName FROM df where Extension = ".exe" OR Extension = ".dat" AND ParentPath NOT LIKE "%WinSxS%"''')
	results = c.fetchall()
	list = set()
	if len(results) > 0:
		for row in results:
		    list.add(row[0])


	normal_list = [u'audiodg.exe', u'usrclass.dat',u'ntuser.dat',u'autochk.exe',u'auditpol.exe',
	                    u'autoconv.exe',u'autofmt.exe',u'dcdiag.exe',u'mpiexec.exe',u'amcache.hve',
                            u'bcdboot.exe', u'bcdedit.exe',u'csc.exe', u'bitsadmin.exe', u'bootcfg.exe', u'bthudtask.exe',
                            u'cacls.exe', u'calc.exe', u'certenrollctrl.exe', u'certreq.exe', u'certutil.exe',
                            u'change.exe', u'charmap.exe', u'chglogon.exe', u'chgport.exe', u'chgusr.exe', u'chkdsk.exe',
                            u'chkntfs.exe', u'choice.exe', u'cipher.exe', u'cleanmgr.exe', u'cliconfg.exe', u'clip.exe',
                            u'cmdl32.exe', u'cmmon32.exe', u'cmstp.exe', u'rsconfig.exe',u'cofire.exe', u'colorcpl.exe', u'comp.exe',
                            u'compact.exe', u'compmgmtlauncher.exe', u'computerdefaults.exe', u'taskhostw.exe',u'conhost.exe',
                            u'consent.exe', u'control.exe', u'convert.exe', u'credwiz.exe', u'cscript.exe', u'csrss.exe',
                            u'ctfmon.exe', u'cttune.exe', u'cttunesvr.exe', u'dccw.exe', u'dcomcnfg.exe', u'ddodiag.exe',
                            u'defrag.exe', u'devicedisplayobjectprovider.exe', u'attrib.exe', u'deviceeject.exe',
                            u'devicepairingwizard.exe', u'deviceproperties.exe', u'jsc.exe', u'dfdwiz.exe', u'dfrgui.exe',
                            u'dialer.exe', u'diantz.exe', u'dinotify.exe', u'diskpart.exe', u'diskperf.exe',
                            u'diskraid.exe', u'dism.exe', u'dispdiag.exe', u'displayswitch.exe', u'djoin.exe',
                            u'dllhost.exe', u'dllhst3g.exe', u'dnscacheugc.exe', u'doskey.exe', u'dpapimig.exe',
                            u'dpiscaling.exe', u'dpnsvr.exe', u'driverquery.exe', u'drvinst.exe', u'dvdplay.exe',
                            u'dvdupgrd.exe', u'dwm.exe', u'dwwin.exe', u'dxdiag.exe', u'dxpserver.exe', u'eap3host.exe',
                            u'efsui.exe', u'ehstorauthn.exe', u'esentutl.exe', u'eudcedit.exe', u'eventcreate.exe',
                            u'eventvwr.exe', u'expand.exe', u'extrac32.exe', u'fc.exe', u'find.exe', u'findstr.exe',
                            u'finger.exe', u'fixmapi.exe', u'fltmc.exe', u'fontview.exe', u'forfiles.exe', u'fsquirt.exe',
                            u'fsutil.exe', u'ftp.exe', u'fvenotify.exe', u'fveprompt.exe', u'fxscover.exe', u'fxssvc.exe',
                            u'fxsunatd.exe', u'getmac.exe', u'gettingstarted.exe', u'gpscript.exe',
                            u'gpupdate.exe', u'grpconv.exe', u'hdwwiz.exe', u'help.exe', u'hostname.exe', u'hwrcomp.exe',
                            u'hwrreg.exe', u'icacls.exe', u'icardagt.exe', u'icsunattend.exe', u'ie4uinit.exe',
                            u'ieunatt.exe', u'iexpress.exe', u'infdefaultinstall.exe', u'ipconfig.exe', u'irftp.exe',
                            u'iscsicli.exe', u'iscsicpl.exe', u'iscsiexe.dll', u'isoburn.exe', u'klist.exe', u'ksetup.exe',
                            u'ktmutil.exe', u'label.exe', u'locationnotifications.exe', u'locator.exe', u'lodctr.exe',
                            u'logagent.exe', u'logman.exe', u'logoff.exe', u'logonui.exe', u'lpksetup.exe', u'lpremove.exe',
                            u'lsass.exe', u'lsm.exe', u'magnify.exe', u'makecab.exe', u'manage-bde.exe', u'mblctr.exe',
                            u'mcbuilder.exe', u'mctadmin.exe', u'gpresult.exe',u'mdres.exe', u'mdsched.exe', u'mfpmp.exe',
                            u'migautoplay.exe', u'mmc.exe', u'mobsync.exe', u'mountvol.exe', u'mpnotify.exe', u'mrinfo.exe',
                            u'msconfig.exe', u'msdt.exe', u'msdtc.exe', u'msfeedssync.exe', u'msg.exe', u'mshta.exe',
                            u'msiexec.exe', u'msinfo32.exe', u'mspaint.exe', u'msra.exe', u'mstsc.exe', u'mtstocom.exe',
                            u'muiunattend.exe', u'multidigimon.exe', u'napstat.exe', u'narrator.exe', u'nbtstat.exe',
                            u'ndadmin.exe', u'net.exe', u'net1.exe', u'netbtugc.exe', u'netcfg.exe', u'netiougc.exe',
                            u'netplwiz.exe', u'netproj.exe', u'netsh.exe', u'netstat.exe', u'newdev.exe', u'nltest.exe',
                            u'notepad.exe', u'nslookup.exe', u'ntoskrnl.exe', u'ntprint.exe', u'ocsetup.exe',
                            u'odbcad32.exe', u'odbcconf.exe', u'openfiles.exe', u'optionalfeatures.exe', u'osk.exe',
                            u'p2phost.exe', u'pathping.exe', u'pcalua.exe', u'pcaui.exe', u'pcawrk.exe', u'pcwrun.exe',
                            u'perfmon.exe', u'ping.exe', u'pkgmgr.exe', u'plasrv.exe', u'pnpunattend.exe', u'pnputil.exe',
                            u'poqexec.exe', u'powercfg.exe', u'presentationhost.exe', u'presentationsettings.exe',
                            u'prevhost.exe', u'print.exe', u'printbrmui.exe', u'printfilterpipelinesvc.exe',
                            u'printisolationhost.exe', u'printui.exe', u'proquota.exe', u'psr.exe', u'qappsrv.exe',
                            u'qprocess.exe', u'query.exe', u'quser.exe', u'qwinsta.exe', u'rasautou.exe', u'rasdial.exe',
                            u'raserver.exe', u'rasphone.exe', u'rdpclip.exe', u'rdrleakdiag.exe', u'reagentc.exe',
                            u'recdisc.exe', u'recover.exe', u'reg.exe', u'regedt32.exe', u'regini.exe',
                            u'registeriepkeys.exe', u'regsvr32.exe', u'rekeywiz.exe', u'relog.exe', u'relpost.exe',
                            u'repair-bde.exe', u'replace.exe', u'reset.exe', u'resmon.exe', u'rmactivate.exe',
                            u'rmactivate_isv.exe', u'rmactivate_ssp.exe', u'rmactivate_ssp_isv.exe', u'rmclient.exe',
                            u'robocopy.exe', u'route.exe', u'rpcping.exe', u'rrinstaller.exe', u'rstrui.exe', u'runas.exe',
                            u'rundll32.exe', u'runlegacycplelevated.exe', u'runonce.exe', u'rwinsta.exe', u'sbunattend.exe',
                            u'sc.exe', u'schtasks.exe', u'sdbinst.exe', u'sdchange.exe', u'sdclt.exe', u'sdiagnhost.exe',
                            u'searchfilterhost.exe', u'searchindexer.exe', u'searchprotocolhost.exe', u'secedit.exe',
                            u'secinit.exe', u'services.exe', u'sethc.exe', u'setieinstalleddate.exe', u'setspn.exe',
                            u'setupcl.exe', u'setupugc.exe', u'setx.exe', u'sfc.exe', u'shadow.exe', u'shrpubw.exe',
                            u'shutdown.exe', u'sigverif.exe', u'slui.exe', u'smss.exe', u'sndvol.exe', u'snippingtool.exe',
                            u'snmptrap.exe', u'sort.exe', u'soundrecorder.exe', u'spinstall.exe', u'spoolsv.exe',
                            u'sppsvc.exe', u'spreview.exe', u'srdelayed.exe', u'stikynot.exe', u'subst.exe', u'svchost.exe',
                            u'sxstrace.exe', u'synchost.exe', u'syskey.exe', u'systeminfo.exe',
                            u'systempropertiesadvanced.exe', u'systempropertiescomputername.exe',
                            u'systempropertiesdataexecutionprevention.exe', u'systempropertieshardware.exe',
                            u'systempropertiesperformance.exe', u'systempropertiesprotection.exe',
                            u'systempropertiesremote.exe', u'systray.exe', u'tabcal.exe', u'takeown.exe',
                            u'tapiunattend.exe', u'taskeng.exe', u'taskhost.exe', u'taskkill.exe', u'tasklist.exe',
                            u'taskmgr.exe', u'tcmsetup.exe', u'tcpsvcs.exe', u'timeout.exe', u'tpminit.exe',
                            u'tracerpt.exe', u'tracert.exe', u'tscon.exe', u'tsdiscon.exe', u'tskill.exe', u'tstheme.exe',
                            u'tswbprxy.exe', u'tswpfwrp.exe', u'typeperf.exe', u'tzutil.exe', u'ucsvc.exe',
                            u'ui0detect.exe', u'unlodctr.exe', u'unregmp2.exe', u'upnpcont.exe',
                            u'useraccountcontrolsettings.exe', u'userinit.exe', u'utilman.exe', u'vaultcmd.exe',
                            u'vaultsysui.exe', u'vds.exe', u'vdsldr.exe', u'verclsid.exe', u'verifier.exe', u'vmicsvc.exe',
                            u'vssadmin.exe', u'vssvc.exe', u'w32tm.exe', u'waitfor.exe', u'wbadmin.exe', u'wbengine.exe',
                            u'wecutil.exe', u'werfault.exe', u'werfaultsecure.exe', u'wermgr.exe', u'wevtutil.exe',
                            u'wextract.exe', u'wfs.exe', u'where.exe', u'whoami.exe', u'wiaacmgr.exe', u'wiawow64.exe',
                            u'wimserv.exe', u'windowsanytimeupgraderesults.exe', u'wininit.exe', u'winload.exe',
                            u'winlogon.exe', u'winresume.exe', u'winrs.exe', u'winrshost.exe', u'winsat.exe', u'winver.exe',
                            u'wisptis.exe', u'wksprt.exe', u'wlanext.exe', u'wlrmdr.exe', u'wowreg32.exe',
                            u'wpdshextautoplay.exe', u'wpnpinst.exe', u'write.exe', u'wscript.exe', u'wsmanhttpconfig.exe',
                            u'wsmprovhost.exe', u'wsqmcons.exe', u'wuapp.exe', u'wuauclt.exe', u'wudfhost.exe', u'wusa.exe',
                            u'xcopy.exe', u'xpsrchvw.exe', u'xwizard.exe']
	#Calculate lev
	suspicious_files = []
	for legit_name in normal_list:
		for susp_name in list:
		  d = Levenshtein.distance(legit_name.lower(), susp_name.lower())
		  if (d > 0 and d < distance+1):
		      if susp_name.lower() not in normal_list:
		             suspicious_files.append(("'"+legit_name+"'", "'"+susp_name+"'"))
	results = []
	if suspicious_files:
		results.append(("-----------------,----------------".split(',')))
		for row in suspicious_files:
		    results.append((row))
		pd.set_option('display.max_rows', 500) 
		final = pd.DataFrame(results,columns = ['legitimate Files','Suspicious Files'])
		print(final)
	else:
		print('------------------------------------------------')
		print('no suspicious entries with distance ' + str(distance) + ' were found')
		print('------------------------------------------------')
	#End of Lev function#

#duplication function
def duplication(path):
	#Create the DB
        if os.path.isfile('data.db'):
                os.remove('data.db')
                conn = sqlite3.connect('data.db')
                c = conn.cursor()
        else:
                Path('data.db').touch()
                conn = sqlite3.connect('data.db')
                c = conn.cursor()

        #Get CSV files list from a folder
        MFT_files = glob.glob(path + "/*.csv")
        if not MFT_files:
                print("error reading MFT files, check the path specifed")
                sys.exit(2)

        print("Please wait ... it might take a while, depending on the the Size of your MFT files \r")
        #Specify columns to be loaded
        columns = ["ParentPath","FileName","Extension"]

        #Read MFT files and concat them in single dataframe
        def readcsv(params):
            return pd.read_csv(params,usecols=columns)

        df = pd.concat(map(readcsv, MFT_files))

        #convert the dataframe to SQL Tables
        df.to_sql("df",conn, if_exists='append', index = False)
        #query all duplicate exe files - edit as you need
        c.execute('''select FileName,ParentPath from df where Extension = '.exe' AND ParentPath NOT Like "%WinSxS%" AND FileName in
         (select FileName From df GROUP BY FileName HAVING count(*) > 1)
          GROUP BY FileName,ParentPath HAVING count(*) > 1 ORDER BY FileName''')
        results = c.fetchall()
        #arrange and remove unique entries
        for i in range(1 , len(results)):
           current = results[i]
           prev1 = results[i - 1]
           prev2 = results[i - 2]
           if current[0] == prev1[0] and current[0] != prev2[0]:
                   print(prev1)
                   print(current)
           elif current[0] == prev2[0]:
                   print(current)
	#End of duplication function#

try:
   arguments, values = getopt.getopt(argument_list, options, long_options)
   #check each argument
   for currentArgument, currentValue in arguments:
        if ("-h" in currentArgument or "--help" in currentArgument):
            print_usage()
            sys.exit(2)

        elif ("-m" in currentArgument or "--mode" in currentArgument):
            method = currentValue
            if method == "1" and len(argument_list) > 2:
              for cuArgument, cuValue in arguments:
                if ("-p" in cuArgument or "--path" in cuArgument):
                 path = cuValue
                elif ("-d" in cuArgument or "--distance" in cuArgument):
                  distance = int(cuValue)
                  lev(path,distance)
                  sys.exit(2)
            elif method == "2" and len(argument_list) > 2:
               for cuArgument, cuValue in arguments:
                 if ("-p" in cuArgument or "--path" in cuArgument):
                   path = cuValue
                   duplication(path)
                   sys.exit(2)
            else:
               print("incorrect or missing argument, please check the correct syntax using the help option -h")
               sys.exit(2)
        else:
             print("incorrect or missing argument, please check the correct syntax using the help option -h")
             sys.exit(2)
except getopt.error as err:
    # output error, and exit with an error code
    print (str(err))
    sys.exit(2)
