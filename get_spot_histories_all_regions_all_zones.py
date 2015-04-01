#!/usr/bin/env python

import optparse
from sys import *
import os,sys,re
from optparse import OptionParser
import glob
import subprocess
from os import system
import linecache
import time
import datetime

#=========================
def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog -i <instance type> --days=<days>")
        parser.add_option("-i",dest="instance",type="string",metavar="STRING",
                help="Amazon instance type (e.g. r3.8xlarge, t2.micro, etc.)")
        parser.add_option("--days",dest="days",type="int",metavar="INT",
                help="Timeframe over which to retrieve spot instance price history. Maximum is 90 days.")
	parser.add_option("-d", action="store_true",dest="debug",default=False,
                help="debug")
        options,args = parser.parse_args()

        if len(args) > 0:
                parser.error("Unknown commandline options: " +str(args))

        if len(sys.argv) < 3:
                parser.print_help()
                sys.exit()
        params={}
        for i in parser.option_list:
                if isinstance(i.dest,str):
                        params[i.dest] = getattr(options,i.dest)
        return params

#=============================
def getSpotHistory(params):	

	#Inputs
	instance=sys.argv[1]

	#Regions returned from command: $ ec2-describe-regions
	if os.path.exists('regions.txt'): 
		os.remove('regions.txt')
 
	cmd = 'ec2-describe-regions > regions.txt'
	subprocess.Popen(cmd,shell=True).wait()

	r1 = open('regions.txt','r')

	#Loop over all regions
	for regionline in r1:
		print regionline
		region=regionline.split()[2]

		os.environ["EC2_URL"] = "%s" %(region)

		#Get region name
		region=region.split('.')[1]

		if os.path.exists('%s.txt' %(region)):
			os.remove('%s.txt' %(region))

		#Get list of availability zones
		cmd = 'ec2-describe-availability-zones --region %s > %s.txt' %(region,region)
		print cmd
		subprocess.Popen(cmd,shell=True).wait()

		f1=open('%s.txt' %(region),'r')

		for line in f1: 
			zone=line.split()[1]
		
			if os.path.exists('%s_%s_%s_to_%s_spotHistory.txt' %(zone,instance,timeFrame,currentTime)):
				os.remove('%s_%s_%s_to_%s_spotHistory.txt' %(zone,instance,timeFrame,currentTime))	

			cmd = 'ec2-describe-spot-price-history -t %s -d Linux/UNIX -a %s -s %sT14:10:34-0500 > %s_%s_%s_to_%s_spotHistory.txt' %(instance,zone,timeFrame,zone,instance,timeFrame,currentTime)
			print cmd
			subprocess.Popen(cmd,shell=True).wait()
			

		f1.close()

#==============================
def checkConflicts(params):

	instanceList='m3.large, i2.8xlarge, c3.2xlarge, hs1.8xlarge, c1.xlarge, r3.4xlarge, g2.2xlarge, m1.small, c1.medium, m3.2xlarge, c3.8xlarge, m2.xlarge, r3.2xlarge, t1.micro, cr1.8xlarge, r3.8xlarge, cc1.4xlarge, m1.medium, r3.large, c3.xlarge, i2.xlarge, m3.medium, cc2.8xlarge, m1.large, cg1.4xlarge, i2.2xlarge, c3.large, i2.4xlarge, c3.4xlarge, r3.xlarge, m1.xlarge, hi1.4xlarge, m2.4xlarge, m2.2xlarge, m3.xlarge'.split(',')

	if not params['instance'] in instanceList:
		print 'Error: Instance %s is not a valid Amazon instance type. Exiting.' %(params['instance'])
		sys.exit()

	if params['days'] >90:
		print 'A larger time frame than 90 days has been specified (%i days). Using 90 day limit instead.'
		params['days']=90

	return params

#==============================
def getDates(days):

	today = datetime.datetime.now()
	day_today=today.strftime('%j')

	day_prev=int(day_today)-days


#==============================
if __name__ == "__main__":

	params=setupParserOptions()
	getDates(params['days'])
	params=checkConflicts(params)
