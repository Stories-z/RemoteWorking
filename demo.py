class Role:
	manager=0
	enforcer=1
	visitor=2

class Status:
	failure=0
	success=1

taskList = []
userList = []

class Task(object):
	taskID = 0
	taskname = 0
	taskDDL = 0
	taskState = False
	managerIDList = 0
	enforcerIDList = []
	def getUserRole(self,userID):
		if userID == self.managerID:
			return Role.manager
		else:
			if userID in self.enforcerIDList:
				return Role.enforcer
			else:
				return Role.visitor

class User(object):
	def __init__(self,userID):
		self.userID = userID
		self.relativeTaskList = []
		self.taskControllerList = []

	def buildTask(self,taskName):
		task=Task()
		task.taskID=len(taskList)
		task.taskName=taskName
		task.managerID=self.userID
		taskList.append(task)
		self.relativeTaskList.append(task)
		return task.taskID

	def appendTaskController(self,taskID):
		taskController=TaskController(taskID,self.userID)
		self.taskControllerList.append(taskController)

	def removeTaskController(self,index):
		del self.taskControllerList[index]

	def appendRelativeTaskToRelativeTaskList(self,taskID):
		self.relativeTaskList.append(taskList[taskID])

	def removeRelativeTaskFromRelativeTaskList(self,index):
		del self.relativeTaskList[index]

	def getFunction(self,taskControllerIndex,functionIndex):
		return self.taskControllerList[taskControllerIndex].getFunction(functionIndex)

class TaskController(object):
	def __init__(self,taskID,userID):
		self.taskID=taskID

		def removeTask(taskID):
			del taskList[taskID] # controlloer itself not deleted

		def addEnforcerToTask(userID):
			taskList[self.taskID].enforcerIDList.append(userID)
			userList[userID].appendRelativeTaskToRelativeTaskList(self.taskID)

		def removeEnforcerFromTask(userID):
			taskList[taskID].enforcerIDList.remove(userID)
			userList[userID].removeRelativeTaskFromRelativeTaskList(self.taskID)

		def setTaskDDL(ddl):
			taskList[self.taskID].taskDDL=ddl

		def setTaskState(state):
			taskList[self.taskID].taskState=state

		self.functionList = []
		functionListForManager=[removeTask,addEnforcerToTask,removeEnforcerFromTask,setTaskDDL,setTaskState]
		functionListForEnforcer=[addEnforcerToTask,setTaskState]
		role=taskList[taskID].getUserRole(userID)
		if role == Role.manager:
			self.functionList=functionListForManager
		else:
			if role == Role.enforcer:
				self.functionList=functionListForEnforcer
			else:
				self.functionList=[]

	def getFunction(self,index):
		return self.functionList[index]

class TaskViewer(object):
	def __init__(self,taskID,userID):
		task=taskList[taskID]
		print("Here is the view of the task with taskID",task.taskID,":")
		print("  taskName:",task.taskName)
		print("  taskDDL:",task.taskDDL)
		print("  taskState:",task.taskState)
		print("  managerID:",task.managerID)
		print("  enforcerIDList:",task.enforcerIDList)
		print("\n")

if __name__ == '__main__':
	bossID=len(userList)
	boss=User(userID=bossID)
	userList.append(boss)

	workerID=len(userList)
	worker=User(userID=workerID)
	userList.append(worker)

	taskID=boss.buildTask("Do something interesting") #build the task
	print("Task built with taskID",taskID,"by boss with userID",bossID,".\n")
	taskViewer=TaskViewer(taskID,bossID)

	boss.appendTaskController(taskID)
	enforcerAdder=boss.getFunction(0,1)
	enforcerAdder(workerID) #add enforcer to the task
	print("Worker with userID",workerID,"added to task with taskID",taskID,"by boss with userID",bossID,".\n")
	taskViewer=TaskViewer(taskID,bossID)

	ddlSetter=boss.getFunction(0,3)
	ddlSetter(2021)#set the DDL of the task
	print("The DDL of the task with taskID",taskID,"set to",2021,"by boss with userID",bossID,".\n")
	taskViewer=TaskViewer(taskID,bossID)

	worker.appendTaskController(taskID)
	stateSetter=worker.getFunction(0,1)
	stateSetter(True)
	print("The state of the task with taskID",taskID,"set to","True","by worker with userID",workerID,".\n")
	taskViewer=TaskViewer(taskID,workerID)
