# _*_ coding:utf-8 _*_
# 游戏的三个结局：死亡dead，胜利win，超时timeout
# 这个文件不应该需要import隔壁文件的参数或方法，
# 在该文件被调用方法时就直接给方法带入参数

import random
from sys import exit



class End(object):



	def dead(self, player, alien):
		if player == alien:
			self.death = ['被咬下腿部\n伤口处感染寄生于异形的超级细菌\n免疫系统完全破坏\n于两小时后死于失血过多和肺炎',
							  '被咬下头部\n当场毙命',
							  '被咬下丁丁\n被寄生于异形的超级细菌感染\n结果重生出一只巨大丁丁\n过度兴奋而死']
			print '--------------------'
			print '\a你和异形相遇'
			print self.death[random.randint(0 ,2)]
			exit(0)
		else:
			print '\033[33m' + '\n暂时安全\n' + '\033[0m'
			
			
		
	def win(self, full_blood, blood):
		if blood == 0:
			print '---------------------'
			print '\a异形应声倒下\n你击中完美的%d枪\n深空号获救了' % full_blood
			print ''
			print ''
			exit(0)
		else:
			print '\033[33m' + '请继续吧！' + '\033[0m'
			 
		
		
	def timeout(self):
		print '------------------------'
		raw_input('按回车键继续>')
		print ''			
		print ''
		print '漂浮在无声太空的巨型迷宫'
		print '因为生命的消失变得冰冷起来'
		print '空荡的主控大厅响起悲怆的小提琴声'
		print '舷窗外的星河挂在宇宙长廊上'
		print '像一幅150亿年的苍凉壁画'
		print ''
		print ''
		exit(0)
	
	
	