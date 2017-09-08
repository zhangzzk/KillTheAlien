# _*_ coding:utf-8 _*_
# choi，judge，player，alien，shoot等都写在这里
# 由于原代码上面几个应用比较乱，改写时要小心且尽量简化
# 

import random
import End




room = [[1, 1],  [1, 2],  [1, 3],  [1, 4],  [1, 5],

        [2, 1],  [2, 2],  [2, 3],  [2, 4],  [2, 5],

        [3, 1],  [3, 2],           [3, 4],  [3, 5],
         
        [4, 1],  [4, 2],  [4, 3],  [4, 4],  [4, 5],
         
        [5, 1],  [5, 2],  [5, 3],  [5, 4],  [5, 5]]

green_house = [[2, 3], [3, 2], [3, 4], [4, 3]]

colors = {
	'RED': '\033[91m',
	'GREEN': '\033[92m',
	'END': '\033[0m',
	'YELLOW': '\033[33m'
}
		



class Alien(object):

	global room, green_house, colors
	
	def __init__(self, blood):
		self.full_blood = blood
		self.blood = blood
		self.init_inform = '它似乎还没有来过这个房间'
		self.track = {}
		for i in room:
			self.track[str(i)] = self.init_inform
		self.cur_pos = self.start_pos()	
		
	def start_pos(self):
		self.cur_pos = room[random.randint(0, len(room) - 1)]
		while self.cur_pos in green_house:
			self.cur_pos = room[random.randint(0, len(room) - 1)]
		return self.cur_pos
		
	def rand(self, pos):
		self.row_line = random.randint(0, 1)
		if random.randint(0, 1):
			pos[self.row_line] += random.randint(1, 2)
			# print '+1'
		else:
			pos[self.row_line] -= random.randint(1, 2)
			# print '-1'
		return pos
		
	def move(self):
		self.mid_val = self.rand(list(self.cur_pos))
		while not Judge().in_map(self.mid_val) or self.mid_val in green_house:
			self.mid_val = list(self.cur_pos)
			self.mid_val = self.rand(self.mid_val)
		self.cur_pos = self.mid_val	
		#print '异形位置：',self.cur_pos#;print player.cam_pos # 这行测试用的
		self.track[str(self.cur_pos)] = '它似乎来过这个房间'
		if self.cur_pos in player.cam_pos:
			print ''
			print '{0[RED]}！！！！你安装的监视仪发出警报: {1}{0[END]}'.format(colors, self.cur_pos)
		else:
			print ''
			print colors['YELLOW'] + '你听见了一些动静，它在移动，或许留下了一些痕迹' + colors['END']
		End.End().dead(player.cur_pos, self.cur_pos)
		
		
		
class Judge(object):

	global room
	
	def direction(self, statement):
		self.direc = raw_input('%s\n>' % statement)
		if self.direc != 'up' and \
			self.direc != 'down' and \
			self.direc != 'left' and \
			self.direc != 'right':
			print colors['RED'] + "我特么不知道你想干啥！" + colors['END']
			self.direction(statement)
		else:
			return self.direc
			
	def in_map(self, pos):
		if pos in room:
			return True
		else:
			return False
			
			
			
class Player(object):

	global colors
	
	def __init__(self, start_pos, cam):
		self.cur_pos = start_pos
		self.cam = cam
		self.cam_pos = []
		
	def change(self, pos, direc):
		if direc == 'down':
			pos[0] += 1
		elif direc == 'up':
			pos[0] -= 1
		elif direc == 'left':
			pos[1] -= 1
 		elif direc == 'right':
 			pos[1] += 1
 		return pos
		
	def move(self):
		self.direc = Judge().direction('去哪个方向')
		self.may_pos = self.change(list(self.cur_pos), self.direc)
		while not Judge().in_map(self.may_pos):
			print colors['RED'] + '\n不能通行！\n自毁系统已经禁止了飞船的任何出入\n' + colors['END']
			self.direc = Judge().direction('去哪个方向')
			self.may_pos = self.change(list(self.cur_pos), self.direc)
		self.cur_pos = list(self.may_pos)

	
	def choi1(self):
		self.choice = raw_input('move, stay, camera or shoot?\n>')
		if self.choice == 'shoot':
			self.shoot()
			self.choi2()
		elif self.choice == 'stay':
			print colors['YELLOW'] + '你停留在了原地，它来了' + colors['END']
			End.End().dead(self.cur_pos, alien.cur_pos)
		elif self.choice == 'move':
			self.move()	
			End.End().dead(self.cur_pos, alien.cur_pos)
		elif self.choice == 'camera' and self.cam > 0:
			self.cam -= 1
			# print self.cam # 测试行
			self.cam_pos.append(list(self.cur_pos))
			# print self.cam_pos # 测试行
			print ''
			print colors['YELLOW'] + '你在此处设置了一个检测仪' + colors['END']
			self.choi2()
		elif self.choice == 'camera' and self.cam <= 0:
			print colors['RED'] + '你已经没有检测仪了' + colors['END']
			self.choi1()
		else:
			print colors['RED'] + '你特么要干啥!' + colors['END']
			self.choi1()
			
	def choi2(self):
		self.choice = raw_input('move or stay?\n>')
		if self.choice == 'move':
			self.move()
		elif self.choice == 'stay':
			print colors['YELLOW'] + '\n你停留在了原地，异形不见踪影\n' + colors['END']
		else:
			print colors['RED'] + '你特么要干啥!' + colors['END']
			self.choi2()
			
	def shoot(self):
		self.judge = Judge().direction('朝哪个方向开枪')
		if self.cur_pos[0] == alien.cur_pos[0] + 1 and self.cur_pos[1] == alien.cur_pos[1] and self.judge == 'up' or \
			self.cur_pos[0] == alien.cur_pos[0] - 1 and self.cur_pos[1] == alien.cur_pos[1] and self.judge == 'down' or \
			self.cur_pos[1] == alien.cur_pos[1] + 1 and self.cur_pos[0] == alien.cur_pos[0] and self.judge == 'left' or \
			self.cur_pos[1] == alien.cur_pos[1] - 1 and self.cur_pos[0] == alien.cur_pos[0] and self.judge == 'right':
			alien.blood -= 1
			print ''
			print colors['YELLOW'] + '命中！' + colors['END']
			self.death = ['正中后肢', '正中腹部', '正中前胸']
			print colors['YELLOW'] + self.death[random.randint(0, 2)] + colors['END']
			print ''
			End.End().win(alien.full_blood, alien.blood)
		else:
			print colors['YELLOW'] + "\n你什么也没有打中，它似乎不在那里\n" + colors['END']
		
		
		
		
# --------------------------------------------------------------------------------------------------------------		

		
		
		
		
		
class Engine(object):

	global green_house, colors
	
	def __init__(self, time):
		self.step = 0
		self.time = time
		
	def start(self):
		print ''
		print 'Earth Time: 5:43 pm\n'
		print '狗蛋！醒醒！！\n'
		raw_input('按回车键继续>')
		print """
深空号飞船遭遇不明生物入侵！%d分钟后生命自毁系统将自动开启！
作为唯一脱离冬眠状态的船长
你需要在自毁开始前找到The Alien并且杀死它
拯救你冬眠中的船员以及你自己的生命
""" % self.time
		raw_input('按回车键继续>')
		print """			
这是深空号各船舱的坐标，绿色标识为安全舱：\n
[1, 1]   [1, 2]   [1, 3]   [1, 4]   [1, 5]

[2, 1]   [2, 2]   {1[GREEN]}{0[0]}{1[END]}   [2, 4]   [2, 5]

[3, 1]   {1[GREEN]}{0[1]}{1[END]}            {1[GREEN]}{0[2]}{1[END]}   [3, 5]
         
[4, 1]   [4, 2]   {1[GREEN]}{0[3]}{1[END]}   [4, 4]   [4, 5]
         
[5, 1]   [5, 2]   [5, 3]   [5, 4]   [5, 5]
""".format(green_house, colors)
		print """
检测系统被异形破坏了，它最后一次出现的位置是：

%s
			
""" % alien.cur_pos
		raw_input('按回车键继续>\n')
		
		print '你现在的位置：%s' % player.cur_pos
		print "输入'up', 'down', 'right', 'left'在房间移动"
		print "输入'up', 'down', 'right', 'left'向隔壁一间船舱开枪"
		print "你需要击中三次才能杀死异形"
		print "异形一直在移动，一次移动一个房间，或直线上两个房间，而你不会想和它在同一房间相遇"
		print "但你手中有%d架检测仪，异形经过时它们会发出警报" % player.cam
		print "时间紧迫，小心行事"
		print "Good Luck"
		print ''
		print 'Time Count: %d mins left\n' % self.time
		raw_input('按回车键继续>')

	def engine(self):
		while self.step < self.time / 10:
			self.step += 1
			alien.move()
			player.choi1()
			self.inform()
			if self.step in range(6, 30, 5):
				print ''
				print """
这是深空号各船舱的坐标：\n
[1, 1]   [1, 2]   [1, 3]   [1, 4]   [1, 5]

[2, 1]   [2, 2]   {1[GREEN]}{0[0]}{1[END]}   [2, 4]   [2, 5]

[3, 1]   {1[GREEN]}{0[1]}{1[END]}            {1[GREEN]}{0[2]}{1[END]}   [3, 5]
         
[4, 1]   [4, 2]   {1[GREEN]}{0[3]}{1[END]}   [4, 4]   [4, 5]
         
[5, 1]   [5, 2]   [5, 3]   [5, 4]   [5, 5]
""".format(green_house, colors)
		print 'Time has run out!'
		print '自毁系统开启'
		End.End().timeout()
		
	def inform(self):
		print '\n---------------------------'
		print '你的位置：', player.cur_pos
		print ''
		print 'Time Count: %d mins left' % (self.time - self.step * 10)
		print ''	
		print '异形血量：', alien.blood
		print ''
		print '剩余检测仪数量：', player.cam
		print ''
		print '检测仪位置：', str(player.cam_pos)
		print ''
		print '线索：', alien.track[str(player.cur_pos)]
		print '---------------------------'
			
		
		
		
alien = Alien(5)
player = Player([2, 3], 5)		
play = Engine(280)
# 可以写一个跳过start的分支
play.start()
play.engine()

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		