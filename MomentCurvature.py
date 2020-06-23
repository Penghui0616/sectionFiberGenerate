# -*- coding:utf-8 -*-
# @Time     : 2020/6/14 19:42
# @Author   : Penghui Zhang
# @Email    : penghui@tongji.edu.cn
# @File     : MC.py
# @Software : PyCharm

import numpy as np
import math
import matplotlib.pyplot as plt
import copy
import os
import shutil


def mmToInches (mm):
	#mm transform to inches
	inches=mm*0.0393700787
	return inches

def plotLinearRegre (section, direction,x1,y1,x2,y2,xyield,yyield,xmax,ymax):
	#color r,g,b...
	#linestyle,[ '-' | '--' | '-.' | ':' | 'steps' | ��]
	#marker,[ '+' | ',' | '.' | '1' | '2' | '3' | '4' ]
	xscat=np.array(x1)
	yscat=np.array(y1)
	xliner=np.array(x2)
	yliner=np.array(y2)
	width=mmToInches(90)
	height=mmToInches(55)
	plt.figure(1, figsize=(width, height))
	plt.subplot(111)
	p1=plt.plot(xscat,yscat)
	p2=plt.plot(xliner,yliner)
	p3=plt.plot(xyield,yyield,"o")
	p4=plt.plot(xmax,ymax,"o")

	plt.setp(p1, linewidth=1,color='g')
	plt.setp(p2, color='r',linestyle='--',linewidth=1)

	plt.grid(c='k',linestyle='--',linewidth=0.3)
	plt.xlabel("curvature")
	plt.ylabel("moment(kN.m)")
	plt.xlim(0.0, 1.01*max(xscat))
	plt.ylim(3, 1.3*max(yscat))
	plt.title(section+'-'+direction+'-'+str(int(yliner[2])))
	plt.savefig('MCFig/'+section+'-'+direction+'-'+str(int(yliner[2]))+".png",dpi = 600,bbox_inches="tight")
	plt.show()

def MCAnalysis(section, direction):
	fsy = 400000
	try:
		steelDir =  os.listdir('steelRecorder/')
		coreDir =  os.listdir('coreRecorder/')
	except:
		print("Please road MC Analysis")

	momentCurvature=np.loadtxt("MomentCurvature.txt")
	sectCurvature=momentCurvature[:,1]
	sectMoment = momentCurvature[:,0]
	barYieldIndexList=[]

	#寻找钢筋首次屈服点
	for eachFilePath in steelDir:
		barStressStrain=np.loadtxt('steelRecorder/'+eachFilePath)
		barStress=barStressStrain[:,1]
		try:
			indexNum=np.where(barStress>=fsy)[0][0]
			barYieldIndexList.append(indexNum)
		except:
			pass
	barYieldIndex=min(barYieldIndexList)
	barYieldCurvature=sectCurvature[barYieldIndex]
	barYieldMoment=sectMoment[barYieldIndex]
	#print(barYieldMoment,barYieldCurvature)

	#寻找核心混凝土压溃或者纵筋达到极限应变的点
	barCrackIndex = len(sectMoment)-1
	esu = 0.10
	barCrackIndexList = []
	for eachFilePath in steelDir:
		barStressStrain=np.loadtxt('steelRecorder/'+eachFilePath)
		barStrain=barStressStrain[:,2]
		try:
			indexNum=np.where(barStrain>esu)[0][0]
			barCrackIndexList.append(indexNum)
		except:
			pass
	try:
		barCrackIndex=min(barCrackIndexList)
	except:
		pass

	coreCrackIndex = len(sectMoment)-1
	with open(r'ecu.txt') as f:
		ecuList = f.readlines()
		ecuIndex = ecuList.index(section+'\n')
		ecu = float(ecuList[ecuIndex+1].strip())

	coreCrackIndexList = []
	for eachFile1 in coreDir:
		coreStressStrain=np.loadtxt('coreRecorder/'+eachFile1)
		coreStain=coreStressStrain[:,2]
		try:
			indexNum=np.where(coreStain < ecu)[0][0]
			coreCrackIndexList.append(indexNum)
		except:
			pass

	try:
		coreCrackIndex=min(coreCrackIndexList)
	except:
		pass
	crackIndex = min(barCrackIndex, coreCrackIndex)
	if crackIndex == len(sectMoment)-1:
		print("A larger mu is required")

	ultimateMoment = sectMoment[crackIndex]
	ultimateCurvature = sectCurvature[crackIndex]
	#print(ultimateMoment,ultimateCurvature)

	#寻找截面弯矩达到最大点
	momentMaxMoment = max(sectMoment[:crackIndex])
	momentMaxIndex = np.where(sectMoment == momentMaxMoment)
	momentMaxCurvature = sectCurvature[momentMaxIndex][0]
	#print(momentMaxMoment,momentMaxCurvature)


	#计算等效屈服弯矩和曲率
	totArea=np.trapz(sectMoment[:crackIndex], sectCurvature[:crackIndex])
	barYieldX=barYieldCurvature
	barYieldY=barYieldMoment
	tanXY=barYieldY/barYieldX

	epsilon=0.01*totArea
	low=0.0
	high=momentMaxMoment
	ans=(low+high)/2.0
	while abs(ans*ultimateCurvature-ans*0.5*ans/float(tanXY)-totArea)>=epsilon:
		if ans*ultimateCurvature-ans/float(tanXY)*ans*0.5<totArea:
			low=ans
		else:
			high=ans
		ans=(high+low)/2.0

	EffectiveX=ans/float(tanXY)
	blinerX=[0,EffectiveX,ultimateCurvature]
	blinerY=[0,ans,ans]

	plotLinearRegre(section, direction, sectCurvature[:crackIndex],sectMoment[:crackIndex],blinerX,blinerY,\
	                 barYieldCurvature,barYieldMoment,momentMaxCurvature,momentMaxMoment)
	return ans


if not os.path.exists('MCFig'):
	os.makedirs('MCFig')

momentEffectiveList = []
with open(r'MCAnalysis.txt') as f:
	MCInfoList = f.readlines()
	for MCInfo in MCInfoList:
		if os.path.exists('coreRecorder'):
			shutil.rmtree("coreRecorder")
		if os.path.exists('steelRecorder'):
			shutil.rmtree("steelRecorder")
		if os.path.exists('MCInfo.txt'):
			os.remove("MCInfo.txt")
		if os.path.exists('MomentCurvature.txt'):
			os.remove("MomentCurvature.txt")

		section = MCInfo.strip().split()[0]
		direction = MCInfo.strip().split()[1]
		axialLoad = MCInfo.strip().split()[2]
		moment = MCInfo.strip().split()[3]
		MCInfoOpensees = [section, axialLoad, moment]

		with open('MCInfo.txt', "a+") as f:
			f.write(section+'\t')
			f.write(axialLoad+'\t')
			f.write(moment+'\t')
		if direction == 'X':
			os.system('opensees MC_X.tcl')
		elif direction == 'Y':
			os.system('opensees MC_Y.tcl')

		momentEffective = MCAnalysis(section, direction)
		momentEffectiveList.append(momentEffective)

np.savetxt('MomentEffect.txt', momentEffectiveList, fmt="%0.2f")

