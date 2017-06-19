'''
生成中间代码(四元式)
'''
from Front_end import Abstract_Syntax_Tree as AST

# class IntermediateCode(object):
#   def __init__(self):
#       self.action = None
#       self.firstOperand = None
#       self.secondOperand = None
#       self.NXQ = -1

#   def show(self):
#       print('(' + self.action + ', ' + self.firstOperand + ', ' + self.secondOperand + ', ' + self.nextQuaternary + ')')

class IC(object):
    '''四元式基类'''
    def show(self):
        print('(', end = '')
        for name, value in vars(self).items():
            print(' %s' % value, end = '')
        print(')')

class UnCondJump_IC(IC):
    '''无条件跳转'''
    def __init__(self):
        self.action = 'j'
        self.secondPos = '#'
        self.thirdPos = '#'
        self.NXQ = None

# 废弃这种设计
# class CondJump_IC(IC):
#     '''条件跳转'''
#     def __init__(self):
#         self.action = 'cj'
#         self.leftOperand = None
#         self.rightOperand = None
#         self.NXQ = None

class CondJump_IC(IC):
    '''条件跳转'''
    def __init__(self):
        self.action = 'jc'  # jc表示条件跳转
        self.condition = None
        self.trueLabel = None
        self.falseLabel = None

class BinOpIC(IC):
    '''二元运算'''
    def __init__(self):
        self.action = ''
        self.leftOperand = None
        self.rightOperand = None
        self.aimVar = ''

class AssignIC(IC):
    '''赋值'''
    def __init__(self):
        self.action = ':='
        self.rightValue = None
        self.unusePos = '#' # '#'表示该位置没用
        self.leftValue = ''

class LoadImmediate(IC):
    '''加载立即数'''
    def __init__(self):
        self.action = 'load'
        self.immediateNum = None
        self.thirdPos = '#'    # 不使用
        self.aimVar = ''


class IC_Generator(object):
    '''
    生成四元式
    '''
    def __init__(self, rootNode):
        self.rootNode = rootNode
        self.intermediateCodeBuf = list()
        self.nextTempVarNo = 0
        self.nextLabelNo = 0

    def generate(self, node):
        if node is not None:
            if node.__class__.__name__ == 'AssignmentNode':
                leftValue = node.children[0].name
                rightValue = self.generate(node.children[-1])
                IC_obj = AssignIC()
                IC_obj.leftValue = leftValue
                IC_obj.rightValue = rightValue
                self.intermediateCodeBuf.append(IC_obj)
                return
                # print("a Assign IC Done.")

            if node.__class__.__name__ == 'BinaryOpNode':
                # print("In binaryOpNode:", end = '')
                # print(node.children[0], end = '')
                # print(type(node.children[0]))
                leftValue = self.generate(node.children[0])
                # print("Is Binary_Operation")
                op = node.children[1]   # 运算符号是中间结点(第二个结点)
                # print(node.children[-1])
                rightValue = self.generate(node.children[-1])
                IC_obj = BinOpIC()
                IC_obj.action = op
                IC_obj.leftOperand = leftValue
                IC_obj.rightOperand = rightValue
                IC_obj.aimVar = self.getNewTempVar()
                self.intermediateCodeBuf.append(IC_obj)
                return IC_obj.aimVar
                # print("a binaryOp IC Done.")

            if isinstance(node, int) or isinstance(node, float):
                # print("the node is: " + str(node))
                return node

            if node.__class__.__name__ == 'IdNode':
                # print("node.name is: " + node.name)
                return node.name

            if node.__class__.__name__ == 'UnaryOpNode':
                return -self.generate(node.children[-1])

            if node.__class__.__name__ == 'IfNode':
                condition = self.generate(node.children[0])

                trueLabel = self.getNewLabelName()  # 为真跳转向的位置
                falseLabel = self.getNewLabelName() # 为假跳转向的位置
                breakLabel = self.getNewLabelName() # 分支结束之后的跳转位置(就是if-then或if-then-else结束之后的跳转位置)
                
                conditionIC_obj = CondJump_IC()
                conditionIC_obj.condition = condition
                conditionIC_obj.trueLabel = trueLabel
                conditionIC_obj.falseLabel = falseLabel
                self.intermediateCodeBuf.append(conditionIC_obj)

                # print(trueLabel + ':')
                trueLabelStr = trueLabel + ':'
                self.intermediateCodeBuf.append(trueLabelStr)
                truebody = self.generate(node.children[1])
                unconditionIC_obj = UnCondJump_IC()
                unconditionIC_obj.NXQ = breakLabel
                self.intermediateCodeBuf.append(unconditionIC_obj)

                # 加入对else的支持
                if len(node.children) == 3: # 说明是if-then-else语句,如果只是等于2的话,就只是if-then语句
                    falseLabelStr = falseLabel + ':'
                    self.intermediateCodeBuf.append(falseLabelStr)
                    falsebody = self.generate(node.children[-1])    # else部分
                    unconditionIC_obj = UnCondJump_IC()
                    unconditionIC_obj.NXQ = breakLabel
                    self.intermediateCodeBuf.append(unconditionIC_obj)


                # print("breakLabel is: " + breakLabel + ':')     # 为之后显示的四元式序列标记breakLabel
                breakLabelStr = breakLabel + ':'
                self.intermediateCodeBuf.append(breakLabelStr)

                return  # 一定要加上！


            if node.__class__.__name__ == 'WhileNode':

                currentLastIC = self.intermediateCodeBuf[-1]
                if isinstance(currentLastIC, str):
                    startJudgeLabelStr = currentLastIC
                    startJudgeLabel = currentLastIC[0:-1]
                    # print("the currentLastLabel is: ", end = '')
                    # print(startJudgeLabelStr)
                    # self.intermediateCodeBuf.append(startJudgeLabelStr)   # 这里不需要，因为可以直接用之前已经加到intermediateCodeBuf中label字符串
                else:
                    startJudgeLabel = self.getNewLabelName()
                    startJudgeLabelStr = startJudgeLabel + ':'
                    self.intermediateCodeBuf.append(startJudgeLabelStr)    # 只在这里加就行

                condition = self.generate(node.children[0])

                trueLabel = self.getNewLabelName()
                falseLabel = self.getNewLabelName()
                # breakLabel = self.getNewLabelName()

                conditionIC_obj = CondJump_IC()
                conditionIC_obj.condition = condition
                conditionIC_obj.trueLabel = trueLabel
                conditionIC_obj.falseLabel = falseLabel
                self.intermediateCodeBuf.append(conditionIC_obj)

                trueLabelStr = trueLabel + ':'
                self.intermediateCodeBuf.append(trueLabelStr)
                truebody = self.generate(node.children[1])  # 处理while的循环体

                unconditionIC_obj = UnCondJump_IC()
                unconditionIC_obj.NXQ = startJudgeLabel
                self.intermediateCodeBuf.append(unconditionIC_obj)

                falseLabelStr = falseLabel + ':'
                self.intermediateCodeBuf.append(falseLabelStr)

                return

            if node.__class__.__name__ == 'ForNode':
                # print("ForNode's children number: ", end = '')
                # print(len(node.children))

                loopControlVarName = node.children[0].name  # 循环控制变量
                loopStartBoundary = node.children[1]  # 循环初始值
                loopEndBoundary = node.children[3]  # 循环终止值

                if node.children[2] == 'to':
                    # print("is a TO type for loop")

                    # 先生成一个赋值结点
                    AssignIC_obj = AssignIC()
                    AssignIC_obj.leftValue = loopControlVarName
                    AssignIC_obj.rightValue = loopStartBoundary
                    self.intermediateCodeBuf.append(AssignIC_obj)

                    # 加载立即数,这个立即数就是循环上届loopEndBoundary
                    LoadI_IC_obj = LoadImmediate()
                    LoadI_IC_obj.immediateNum = loopEndBoundary
                    LoadI_IC_obj.aimVar = self.getNewTempVar()
                    self.intermediateCodeBuf.append(LoadI_IC_obj)

                    # 生成循环判断label
                    loopJudgeLabel = self.getNewLabelName()
                    loopJudgeLabelStr = loopJudgeLabel + ':'
                    self.intermediateCodeBuf.append(loopJudgeLabelStr)

                    # 判断是否到达循环结束上界
                    GreaterJudge_IC_obj = BinOpIC()
                    # EqualJudge_IC_obj.action = '=='
                    GreaterJudge_IC_obj.action = '>'
                    GreaterJudge_IC_obj.leftOperand = loopControlVarName
                    GreaterJudge_IC_obj.rightOperand = LoadI_IC_obj.aimVar
                    GreaterJudge_IC_obj.aimVar = self.getNewTempVar()
                    self.intermediateCodeBuf.append(GreaterJudge_IC_obj)

                    # 条件跳转
                    trueLabel = self.getNewLabelName()
                    falseLabel = self.getNewLabelName()
                    conditionIC_obj = CondJump_IC()
                    conditionIC_obj.condition = GreaterJudge_IC_obj.aimVar
                    conditionIC_obj.trueLabel = trueLabel
                    conditionIC_obj.falseLabel = falseLabel
                    self.intermediateCodeBuf.append(conditionIC_obj)

                    # 加入trueLabel
                    trueLabelStr = trueLabel + ':'
                    self.intermediateCodeBuf.append(trueLabelStr)

                    # 处理循环体部分
                    truebody = self.generate(node.children[1])  # 处理while的循环体

                    # 循环体结束之后,做两件事: 递增循环控制变量、加入无条件跳转,跳回到loopJudgeLabel处
                    
                    # 递增循环控制变量
                    AddIC_obj = BinOpIC()
                    AddIC_obj.action = '+'  # 因为是"to"的类型的for循环
                    AddIC_obj.leftOperand = loopControlVarName
                    AddIC_obj.rightOperand = 1  # 递增1
                    AddIC_obj.aimVar = self.getNewTempVar()
                    self.intermediateCodeBuf.append(AddIC_obj)

                    # 无条件跳转
                    unconditionIC_obj = UnCondJump_IC()
                    unconditionIC_obj.NXQ = loopJudgeLabel  # 跳回到loopJudgeLabel处
                    self.intermediateCodeBuf.append(unconditionIC_obj)

                    # 加入falseLabel
                    falseLabelStr = falseLabel + ':'
                    self.intermediateCodeBuf.append(falseLabelStr)


                elif node.children[2] == 'downto':
                    # print("is a TO type for loop")

                    # 先生成一个赋值结点
                    AssignIC_obj = AssignIC()
                    AssignIC_obj.leftValue = loopControlVarName
                    AssignIC_obj.rightValue = loopStartBoundary
                    self.intermediateCodeBuf.append(AssignIC_obj)

                    # 加载立即数,这个立即数就是循环上届loopEndBoundary
                    LoadI_IC_obj = LoadImmediate()
                    LoadI_IC_obj.immediateNum = loopEndBoundary
                    LoadI_IC_obj.aimVar = self.getNewTempVar()
                    self.intermediateCodeBuf.append(LoadI_IC_obj)

                    # 生成循环判断label
                    loopJudgeLabel = self.getNewLabelName()
                    loopJudgeLabelStr = loopJudgeLabel + ':'
                    self.intermediateCodeBuf.append(loopJudgeLabelStr)

                    # 判断是否到达循环结束上界
                    GreaterJudge_IC_obj = BinOpIC()
                    GreaterJudge_IC_obj.action = '<'
                    GreaterJudge_IC_obj.leftOperand = loopControlVarName
                    GreaterJudge_IC_obj.rightOperand = LoadI_IC_obj.aimVar
                    GreaterJudge_IC_obj.aimVar = self.getNewTempVar()
                    self.intermediateCodeBuf.append(GreaterJudge_IC_obj)

                    # 条件跳转
                    trueLabel = self.getNewLabelName()
                    falseLabel = self.getNewLabelName()
                    conditionIC_obj = CondJump_IC()
                    conditionIC_obj.condition = GreaterJudge_IC_obj.aimVar
                    conditionIC_obj.trueLabel = trueLabel
                    conditionIC_obj.falseLabel = falseLabel
                    self.intermediateCodeBuf.append(conditionIC_obj)

                    # 加入trueLabel
                    trueLabelStr = trueLabel + ':'
                    self.intermediateCodeBuf.append(trueLabelStr)

                    # 处理循环体部分
                    truebody = self.generate(node.children[1])  # 处理while的循环体

                    # 循环体结束之后,做两件事: 递增循环控制变量、加入无条件跳转,跳回到loopJudgeLabel处
                    
                    # 递增循环控制变量
                    AddIC_obj = BinOpIC()
                    AddIC_obj.action = '-'  # 因为是"downto"的类型的for循环
                    AddIC_obj.leftOperand = loopControlVarName
                    AddIC_obj.rightOperand = 1  # 递减1
                    AddIC_obj.aimVar = self.getNewTempVar()
                    self.intermediateCodeBuf.append(AddIC_obj)

                    # 无条件跳转
                    unconditionIC_obj = UnCondJump_IC()
                    unconditionIC_obj.NXQ = loopJudgeLabel  # 跳回到loopJudgeLabel处
                    self.intermediateCodeBuf.append(unconditionIC_obj)

                    # 加入falseLabel
                    falseLabelStr = falseLabel + ':'
                    self.intermediateCodeBuf.append(falseLabelStr)

                return

            if node.__class__.__name__ == 'BinaryBoolNode':
                boolLeft = self.generate(node.children[0])
                boolOp = node.children[1]
                boolRight = self.generate(node.children[-1])

                IC_obj = BinOpIC()  # BinOpIC包括二元布尔运算和算术运算
                IC_obj.action = boolOp
                IC_obj.leftOperand = boolLeft
                IC_obj.rightOperand = boolRight
                IC_obj.aimVar = self.getNewTempVar()
                self.intermediateCodeBuf.append(IC_obj)
                return IC_obj.aimVar


            if node.__class__.__name__ == 'NoneLabeledClosedStatementNode':
                # print('IN non_labeled_closed_statement')
                return self.generate(node.children[0])  # non_labeled_closed_statement的子结点只会有一个

            if node.__class__.__name__ == 'CompoundStatementNode':
                return self.generate(node.children[0])  # 子结点也是只有一个

            if node.__class__.__name__ == 'StateListNode':
                # print("IN StateListNode")
                for child in node.children:
                    # return self.generate(child)
                    self.generate(child)
                return  # 这里也一定要加上！

            # if node

        if isinstance(node, AST.Node):
            for child in node.children:
                self.generate(child)

    def print_IC(self):
        self.generate(self.rootNode)
        # for IC in self.intermediateCodeBuf:
        #     IC.show()
        for item in self.intermediateCodeBuf:
            if isinstance(item, IC):
                item.show()
            else:   # 是字符串(例如: 'Label2:')
                print(item)

    def getNewTempVar(self):
        self.nextTempVarNo += 1
        return 'T' + str(self.nextTempVarNo)    # 返回新的临时变量字符串

    def getNewLabelName(self):
        self.nextLabelNo += 1
        return 'Label' + str(self.nextLabelNo)  # 返回新的临时Label字符串
