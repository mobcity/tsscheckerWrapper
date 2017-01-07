#!/usr/bin/python
# -*- coding: UTF-8 -*-

#edit sshd_config in authentication:
#eg. MaxSessions 20
#MaxSessions len(number of versions)
#Fix version display in threads always prints same version
#swap from threading on ssh to process
#Git pull tsschecker/download compiled zip
#mac or linux binary
#os detection using os.environ? for name/file call
#implement find tsschecker folder or download it 
#implement threading and blobs to save to designated destination (tsschecker command? cd?)

import os, getpass, datetime, paramiko, threading, ConfigParser
# Get the project directory to avoid using relative paths
PROJECT_ROOT_DIR = os.getcwd()

# Parse configuration file
c = ConfigParser.ConfigParser()
configFilePath = os.path.join(PROJECT_ROOT_DIR, 'config.cfg')
c.read(configFilePath)

class Config:
    # Pull user info 
    ecid = c.get('device', 'ecid')
    deviceIdentifier = c.get('device', 'deviceIdentifier')
    pwd = c.get('ssh','password')

class SSH:
	ssh=paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	def __init__(self, address, port, user, passwd):
		self.address = address
		self.port = port
		self.user = user
		self.passwd = passwd
	def connect(self):
		SSH.ssh.connect(self.address,self.port,self.user,self.passwd)

deviceInfo={
	'iPhone1,1':{ #iphone 2g
		'1.0':		'1A543a',
		'1.0.1':	'1C25',
		'1.0.2':	'1C28',
		'1.1.1':	'3A109a',
		'1.1.2':	'3B48b',
		'1.1.3':	'4A93',
		'1.1.4':	'4A102',
		'2.0.0':	'5A347',
		'2.0.1':	'5B108',
		'2.0.2':	'5C1',
		'2.1.0':	'5F136',
		'2.2.0':	'5G77',
		'2.2.1':	'5H1',
		'3.0.0':	'7A341',
		'3.0.1':	'7A400',
		'3.1.0':	'7C144',
		'3.1.2':	'7D11',
		'3.1.3':	'7E18'
	},
	'iPhone1,2':{ #iphone 3g
		'2.0.0': 	'5A347',
		'2.0.1': 	'5B108',
		'2.0.2': 	'5C1',
		'2.1.0': 	'5F136',
		'2.2.0': 	'5G77',
		'2.2.1': 	'5H11',
		'3.0.0': 	'7A341',
		'3.0.1': 	'7A400',
		'3.1.0': 	'7C144',
		'3.1.2': 	'7D11',
		'3.1.3': 	'7E18',
		'4.0.0': 	'8A2y3',
		'4.0.1': 	'8A306',
		'4.0.2': 	'8A400',
		'4.1.0': 	'8B117',
		'4.2.1': 	'8C148'
	},
	'iPhone2,1':{
		'3.0.0': 	'7A341',
		'3.0.1':	'7A400',
		'3.1.0':	'7C144',
		'3.1.2':	'7D11',
		'3.1.3':	'7E18',
		'4.0.0':	'8A293',
		'4.0.1':	'8A306',
		'4.0.2':	'8A400',
		'4.1.0':	'8B117',
		'4.2.1':	'8C148a',
		'4.3.0':	'8F190',
		'4.3.1':	'8G4',
		'4.3.2':	'8H7',
		'4.3.3':	'8J2',
		'4.3.4':	'8K2',
		'4.3.5':	'8L1',
		'5.0': 		'9A334',
		'5.0.1':	'9A405',
		'5.1.0':	'9B176',
		'5.1.1':	'9B206',
		'6.0.0':	'10A403',
		'6.0.1':	'10A523',
		'6.1':  	'10B141',
		'6.1.2':	'10B146',
		'6.1.3':	'10B329',
		'6.1.6':	'10B500'
	},
	'iPhone3,1':{ #iphone 4 gsm
		'4.0.0':	'8A293',
		'4.0.1':	'8A306',
		'4.0.2':	'8A400',
		'4.1.0':	'8B117',
		'4.2.1':	'8C148',
		'4.3.0':	'8F190', #first fw with split networks
		'4.3.1':	'8G4',
		'4.3.2':	'8H7',
		'4.3.3':	'8J2',
		'4.3.4':	'8K2',
		'4.3.5':	'8L1',
		'5.0':		'9A334',
		'5.0.1':	'9A405',
		'5.1.0':	'9B176',
		'5.1.1':	'9B206',
		'5.1.1.2':	'9B208',
		'6.0.0':	'10A403',
		'6.0.1':	'10A523',
		'6.1':		'10B144',
		'6.1.2':	'10B146',
		'6.1.3':	'10B329',
		'7.0':		'11A465',
		'7.0.2':	'11A501',
		'7.0.3':	'11B511',
		'7.0.4':	'11B554a',
		'7.0.6':	'11B651',
		'7.1':		'11D169',
		'7.1.1':	'11D201',
		'7.1.2':	'11D257'
	},
	'iPhone3,2':{ #iphone 4 gsm revA 8gb
		'6.0.0':	'10A403',
		'7.0.3':	'11B511',
		'7.0.4': 	'11B554a',
		'7.0.6': 	'11B651',
		'7.1':   	'11D169',
		'7.1.1': 	'11D201',
		'7.1.2': 	'11D257'
	},
	'iPhone3,3':{ #iphone 4 cdma
		'4.2.6': 	'8E600',
		'4.2.7': 	'8E303',
		'4.2.8': 	'8E401',
		'4.2.9': 	'8E501',
		'4.2.10': 	'8E600',
		'5.0': 		'9A334',
		'5.0.1': 	'9A405',
		'5.1.0': 	'9B176',
		'5.1.1': 	'9B206',
		'6.0.0': 	'10A403',
		'6.0.1': 	'10A523',
		'6.1': 		'10B141',
		'6.1.2': 	'10B146',
		'6.1.3': 	'10B329',
		'7.0': 		'11A465',
		'7.0.2': 	'11A501',
		'7.0.3': 	'11B511',
		'7.0.4': 	'11B554a',
		'7.0.6': 	'11B651',
		'7.1': 		'11D167',
		'7.1.1': 	'11D201',
		'7.1.2': 	'11D257'
	},
	'iPhone4,1':{ #iphone 4s 
		'5.0':		'9A334',
		'5.0.1':	'9A405',
		'5.0.1.2':	'9A406',
		'5.1.0':	'9B179',
		'5.1.1': 	'9B206',
		'6.0.0': 	'10A403',
		'6.0.1': 	'10A523',
		'6.1':   	'10B142',
		'6.1.1': 	'10B145',
		'6.1.2':	'10B146',
		'6.1.3':	'10B329',
		'7.0':  	'11A465',
		'7.0.2':	'11A501',
		'7.0.3':	'11B511',
		'7.0.4':	'11B554a',
		'7.0.6':	'11B651',
		'7.1':  	'11D167',
		'7.1.1':	'11D201',
		'7.1.2':	'11D257',
		'8.0':  	'12A365',
		'8.0.1':	'12A402',
		'8.0.2':	'12A405',
		'8.1':  	'12B411',
		'8.1.1':	'12B435',
		'8.1.2':	'12B440',
		'8.1.3':	'12B466',
		'8.2':  	'12D508',
		'8.3':  	'12F70',
		'8.4':  	'12H143',
		'8.4.1':	'12H321',
		'9.0':  	'13A344',
		'9.0.1':	'13A404',
		'9.0.2':	'13A452',
		'9.1.0':	'13B143',
		'9.2':  	'13C75',
		'9.2.1':	'13D15',
		'9.3':  	'13E237',
		'9.3.1':	'13E238',
		'9.3.2':	'13F69',
		'9.3.3':	'13G34',
		'9.3.4':	'13G35',
		'9.3.5':	'13G36'
	},
	'iPhone5,1':{ #iphone 5 gsm
		'6.0.0' :	'10A405',
		'6.0.1' :	'10A525',
		'6.0.2' :	'10A551',
		'6.1'   :	'10B143',
		'6.1.2' :	'10B146',
		'6.1.3' :	'10B329',
		'6.1.4' :	'10B350',
		'7.0'   :	'11A465',
		'7.0.2' :	'11A501',
		'7.0.3' :	'11B511',
		'7.0.4' :	'11B554a',
		'7.0.6' :	'11B651',
		'7.1'   :	'11D167',
		'7.1.1' :	'11D201',
		'7.1.2' :	'11D257',
		'8.0'   :	'12A365',
		'8.0.1' :	'12A402',
		'8.0.2' :	'12A405',
		'8.1'   :	'12B411',
		'8.1.1' :	'12B435',
		'8.1.2' :	'12B440',
		'8.1.3' :	'12B466',
		'8.2'   :	'12D508',
		'8.3'   :	'12F70',
		'8.4'   :	'12H143',
		'8.4.1' :	'12H321',
		'9.0'   :	'13A344',
		'9.0.1' :	'13A404',
		'9.0.2' :	'13A452',
		'9.1.0' :	'13B143',
		'9.2'   :	'13C75',
		'9.2.1' :	'13D15',
		'9.3'   :	'13E237',
		'9.3.1' :	'13E238',
		'9.3.2' :	'13F69',
		'9.3.3' :	'13G34',
		'9.3.4' :	'13G35',
		'9.3.5' :	'13G36',
		'10.0.1':	'14A403',
		'10.0.2':	'14A456',
		'10.1'  :	'14B72',
		'10.1.1':	'14B150',
		'10.2'  :	'14C92'
	},
	'iPhone5,2':{ #iphone 5 gsm+cdma
		'7.0.3' :	'11B511',
		'7.0.4' :	'11B554a',
		'7.0.6' :	'11B651',
		'7.1'   :	'11D167',
		'7.1.1' :	'11D201',
		'7.1.2' :	'11D257',
		'8.0'   :	'12A365',
		'8.0.1' :	'12A402',
		'8.0.2' :	'12A405',
		'8.1'   :	'12B411',
		'8.1.1' :	'12B435',
		'8.1.2' :	'12B440',
		'8.1.3' :	'12B466',
		'8.2'   :	'12D508',
		'8.3'   :	'12F70',
		'8.4'   :	'12H143',
		'8.4.1' :	'12H321',
		'9.0'   :	'13A344',
		'9.0.1' :	'13A404',
		'9.0.2' :	'13A452',
		'9.1.0' :	'13B143',
		'9.2'   :	'13C75',
		'9.2.1' :	'13D15',
		'9.3'   :	'13E237',
		'9.3.1' :	'13E238',
		'9.3.2' :	'13F69',
		'9.3.3' :	'13G34',
		'9.3.4' :	'13G35',
		'9.3.5' :	'13G36',
		'10.0.1':	'14A403',
		'10.0.2':	'14A456',
		'10.1'  : 	'14B72',
		'10.1.1': 	'14B150',
		'10.2'  : 	'14C92'
	},
	'iPhone5,3':{ #iphone 5c gsm
		'7.0.1' :	'11A470a',
		'7.0.2' :	'11A501',
		'7.0.3' :	'11B511',
		'7.0.4' :	'11B554a',
		'7.0.6' :	'11B651',
		'7.1'   :	'11D167',
		'7.1.1' :	'11D201',
		'7.1.2' :	'11D257',
		'8.0'   :	'12A365',
		'8.0.1' :	'12A402',
		'8.0.2' :	'12A405',
		'8.1'   :	'12B411',
		'8.1.1' :	'12B435',
		'8.1.2' :	'12B440',
		'8.1.3' :	'12B466',
		'8.2'   :	'12D508',
		'8.3'   :	'12F70',
		'8.4'   :	'12H143',
		'8.4.1' :	'12H321',
		'9.0'   :	'13A344',
		'9.0.1' :	'13A404',
		'9.0.2' :	'13A452',
		'9.1.0' :	'13B143',
		'9.2'   :	'13C75',
		'9.2.1' :	'13D15',
		'9.3'   :	'13E237',
		'9.3.1' :	'13E238',
		'9.3.2' :	'13F69',
		'9.3.3' :	'13G34',
		'9.3.4' :	'13G35',
		'9.3.5' :	'13G36',
		'10.0.1':	'14A403',
		'10.0.2':	'14A456',
		'10.1'  :	'14B72',
		'10.1.1':	'14B150',
		'10.2'  :	'14C92'
	},
	'iPhone5,4':{ #iphone 5c gsm+cdma
		'7.0.3' : 	'11B511',
		'7.0.4' : 	'11B554a',
		'7.0.5' : 	'11B601',
		'7.0.6' : 	'11B651',
		'7.1'   : 	'11D167',
		'7.1.1' : 	'11D201',
		'7.1.2' : 	'11D257',
		'8.0'   : 	'12A365',
		'8.0.1' : 	'12A402',
		'8.0.2' : 	'12A405',
		'8.1'   : 	'12B411',
		'8.1.1' : 	'12B435',
		'8.1.2' : 	'12B440',
		'8.1.3' : 	'12B466',
		'8.2'   : 	'12D508',
		'8.3'   : 	'12F70',
		'8.4'   : 	'12H143',
		'8.4.1' : 	'12H321',
		'9.0'   : 	'13A344',
		'9.0.1' : 	'13A404',
		'9.0.2' : 	'13A452',
		'9.1.0' : 	'13B143',
		'9.2'   : 	'13C75',
		'9.2.1' : 	'13D15',
		'9.3'   : 	'13E237',
		'9.3.1' : 	'13E238',
		'9.3.2' : 	'13F69',
		'9.3.3' : 	'13G34',
		'9.3.4' : 	'13G35',
		'9.3.5' : 	'13G36',
		'10.0.1': 	'14A403',
		'10.0.2': 	'14A456',
		'10.1'  : 	'14B72',
		'10.1.1': 	'14B150',
		'10.2'  : 	'14C92'
	},
	'iPhone6,1':{ #iphone 5s gsm
		'7.0.1' :	'11A470a',
		'7.0.2' :	'11A501',
		'7.0.3' :	'11B511',
		'7.0.4' :	'11B554a',
		'7.0.6' :	'11B651',
		'7.1'   :	'11D167',
		'7.1.1' :	'11D201',
		'7.1.2' :	'11D257',
		'8.0'   :	'12A365',
		'8.0.1' :	'12A402',
		'8.0.2' :	'12A405',
		'8.1'   :	'12B411',
		'8.1.1' :	'12B435',
		'8.1.2' :	'12B440',
		'8.1.3' :	'12B466',
		'8.2'   :	'12D508',
		'8.3'   :	'12F70',
		'8.4'   :	'12H143',
		'8.4.1' :	'12H321',
		'9.0'   :	'13A344',
		'9.0.1' :	'13A404',
		'9.0.2' :	'13A452',
		'9.1.0' :	'13B143',
		'9.2'   :	'13C75',
		'9.2.1' :	'13D15',
		'9.3'   :	'13E237',
		'9.3.1' :	'13E238',
		'9.3.2' :	'13F69',
		'9.3.3' :	'13G34',
		'9.3.4' :	'13G35',
		'9.3.5' :	'13G36',
		'10.0.1':	'14A403',
		'10.0.2':	'14A456',
		'10.1'  :	'14B72',
		'10.1.1':	'14B150',
		'10.2'  :	'14C92'
	},
	'iPhone6,2':{
		'7.0.1' :	'11A470a',
		'7.0.2' :	'11A501',
		'7.0.3' :	'11B511',
		'7.0.4' :	'11B554a',
		'7.0.5' :	'11B601',
		'7.0.6' :	'11B651',
		'7.1'   :	'11D167',
		'7.1.1' :	'11D201',
		'7.1.2' :	'11D257',
		'8.0'   :	'12A365',
		'8.0.1' :	'12A402',
		'8.0.2' :	'12A405',
		'8.1'   :	'12B411',
		'8.1.1' :	'12B435',
		'8.1.2' :	'12B440',
		'8.1.3' :	'12B466',
		'8.2'   :	'12D508',
		'8.3'   :	'12F70',
		'8.4'   :	'12H143',
		'8.4.1' :	'12H321',
		'9.0'   :	'13A344',
		'9.0.1' :	'13A404',
		'9.0.2' :	'13A452',
		'9.1.0' :	'13B143',
		'9.2'   :	'13C75',
		'9.2.1' :	'13D15',
		'9.3'   :	'13E237',
		'9.3.1' :	'13E238',
		'9.3.2' :	'13F69',
		'9.3.3' :	'13G34',
		'9.3.4' :	'13G35',
		'9.3.5' :	'13G36',
		'10.0.1':	'14A403',
		'10.0.2':	'14A456',
		'10.1'  :	'14B72',
		'10.1.1':	'14B150',
		'10.2'  :	'14C92'
	},
	'iPhone7,1':{ #iphone 6 plus
		'8.0'   :	'12A366',
		'8.0.1' :	'12A402',
		'8.0.2' :	'12A405',
		'8.1'   :	'12B411',
		'8.1.1' :	'12B436',
		'8.1.2' :	'12B440',
		'8.1.3' :	'12B466',
		'8.2'   :	'12D508',
		'8.3'   :	'12F70',
		'8.4'   :	'12H143',
		'8.4.1' :	'12H321',
		'9.0'   :	'13A344',
		'9.0.1' :	'13A404',
		'9.0.2' :	'13A452',
		'9.1.0' :	'13B143',
		'9.2'   :	'13C75',
		'9.2.1' :	'13D20',
		'9.3'   :	'13E233',
		'9.3.1' :	'13E238',
		'9.3.2' :	'13F69',
		'9.3.3' :	'13G34',
		'9.3.4' :	'13G35',
		'9.3.5' :	'13G36',
		'10.0.1':	'14A403',
		'10.0.2':	'14A456',
		'10.1'  :	'14B72',
		'10.1.1':	'14B150',
		'10.2'  :	'14C92'
	},
	'iPhone7,2':{ #iphone 6
		'8.0'   :	'12A365',
		'8.0.1' :	'12A402',
		'8.0.2' :	'12A405',
		'8.1'   :	'12B411',
		'8.1.1' :	'12B436',
		'8.1.2' :	'12B440',
		'8.1.3' :	'12B466',
		'8.2'   :	'12D508',
		'8.3'   :	'12F70', 
		'8.4'   :	'12H143',
		'8.4.1' :	'12H321',
		'9.0'   :	'13A344',
		'9.0.1' :	'13A404',
		'9.0.2' :	'13A452',
		'9.1.0' :	'13B143',
		'9.2'   :	'13C75', 
		'9.2.1' :	'13D20', 
		'9.3'   :	'13E233',
		'9.3.1' :	'13E238',
		'9.3.2' :	'13F69', 
		'9.3.3' :	'13G34', 
		'9.3.4' :	'13G35', 
		'9.3.5' :	'13G36', 
		'10.0.1': 	'14A403',
		'10.0.2': 	'14A456',
		'10.1'  : 	'14B72',
		'10.1.1': 	'14B150',
		'10.2'  : 	'14C92'
	},
	'iPhone8,1':{ #iphone 6s
		'9.0'   :	'13A342',
		'9.0.1' :	'13A342',
		'9.0.2' :	'13A452',
		'9.1.0' :	'13B143',
		'9.2'   :	'13C75', 
		'9.2.1' :	'13D20', 
		'9.3'   :	'13E234',
		'9.3.1' :	'13E238',
		'9.3.2' :	'13F69', 
		'9.3.3' :	'13G34', 
		'9.3.4' :	'13G35', 
		'9.3.5' :	'13G36', 
		'10.0.1':	'14A403',
		'10.0.2':	'14A456',
		'10.1'  :	'14B72', 
		'10.1.1':	'14B150',
		'10.2'  :	'14C92'
	},
	'iPhone8,2':{ #iphone 6s plus
		'9.0'   :	'13A343',
		'9.0.1' :	'13A405',
		'9.0.2' :	'13A452',
		'9.1.0' :	'13B143',
		'9.2'   :	'13C75',
		'9.2.1' :	'13D20',
		'9.3'   :	'13E234',
		'9.3.1' :	'13E238',
		'9.3.2' :	'13F69',
		'9.3.3' :	'13G34',
		'9.3.4' :	'13G35',
		'9.3.5' :	'13G36',
		'10.0.1': 	'14A403',
		'10.0.2': 	'14A456',
		'10.1'  : 	'14B72',
		'10.1.1': 	'14B150',
		'10.2'  : 	'14C92'

	},
	'iPhone8,4':{ #iphone se
		'9.3'   :	'13E233',
		'9.3.1' :	'13E238',
		'9.3.2' :	'13F69', 
		'9.3.3' :	'13G34', 
		'9.3.4' :	'13G35', 
		'9.3.5' :	'13G36', 
		'10.0.1':	'14A403',
		'10.0.2':	'14A456',
		'10.1'  :	'14B72', 
		'10.1.1':	'14B150',
		'10.2'  :	'14C92' 
	},
	'iPhone9,1':{ #iphone 7
		'10.0.1': 	'14A403',
		'10.0.2': 	'14A456',
		'10.0.3': 	'14A551',
		'10.1'  : 	'14B72c',
		'10.1.1': 	'14B150',
		'10.2'  : 	'14C92'
	},

	'iPhone9,2':{ #iphone 7 plus
		'10.0.1': 	'14A403',
		'10.0.2': 	'14A456',
		'10.0.3': 	'14A551',
		'10.1'  : 	'14B72c',
		'10.1.1': 	'14B150',
		'10.2'  : 	'14C92'
	},
	'iPhone9,3':{ #iphone 7
		'10.0.1': 	'14A403',
		'10.0.2': 	'14A456',
		'10.0.3': 	'14A551',
		'10.1'  : 	'14B72c',
		'10.1.1': 	'14B150',
		'10.2'  : 	'14C92'
	},
	'iPhone9,4':{ #iphone 7 plus
		'10.0.1': 	'14A403',
		'10.0.2': 	'14A456',
		'10.0.3': 	'14A551',
		'10.1'  : 	'14B72c',
		'10.1.1': 	'14B150',
		'10.2'  : 	'14C92'
	}	

}

tsscheckerBinPath = os.path.join(PROJECT_ROOT_DIR, 'tsschecker_linux')



#need to adjust this function so that threads are made in for loop
def tsscheckSweep(version, myDeviceLUT, binaryPath, deviceId, ecid):
	try:
		#local_ssh.ssh.exec_command('cd '+PROJECT_ROOT_DIR)
		stdin, stdout, stderr = local_ssh.ssh.exec_command(binaryPath+' -d '+deviceId+' -e '+ecid+' -i '+version+' --buildid '+myDeviceLUT[version]+' -s | grep signed')
		output=stdout.read().split('\n')[0]
		if 'IS being signed' in output:
			print str(datetime.datetime.now().time()) + ' :: '+output+' :: '+ version + '          [✓]'
		else:
			print str(datetime.datetime.now().time()) + ' :: '+output+' :: '+ version
	except Exception as e:
		#quit here the identifier provided by config is not in the device info dictionary
		print str(e)
		pass
	
if __name__ == '__main__':
	"""
	Main slots controller
	"""
	user_config = Config()
	local_ssh = SSH('127.0.0.1', 22, os.getlogin(), user_config.pwd)
	local_ssh.connect()
	for version in deviceInfo[user_config.deviceIdentifier].keys():
		print version, 'Thread initialized!'
		t = threading.Thread(target=tsscheckSweep, args=(version, deviceInfo[user_config.deviceIdentifier], tsscheckerBinPath, user_config.deviceIdentifier, user_config.ecid,))
		t.start()
	print