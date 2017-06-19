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
                breakLabel = self.getNewLabelName() # 分支结束之后的跳转位置
                
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

                # print(breakLabel + ':')     # 为之后显示的四元式序列标记breakLabel
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
                pass

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


# class IC_Generator(object):
#     '''
#     生成四元式
#     '''
#     def __init__(self, rootNode):
#         self.rootNode = rootNode
#         self.intermediateCodeBuf = list()

#     def generate(self, node):
#         if node is not None and isinstance(node, AST.Node):
#             if node.__class__.__name__ == 'AssignmentNode':
                
#                 if isinstance(node.children[-1], int) or isinstance(node.children[-1], float):
#                     IC_obj.rightValue = node.children[-1]
#                 elif node.children[-1].__class__.__name__ == 'Binary_Operation':
#                     IC_obj.rightValue = '@' + str(self.generate(node.children[-1]))
#                 elif node.children[-1].__class__.__name__ == 'Unary_Operation':
#                     if isinstance(node.children[-1].children[-1], int) or isinstance(node.children[-1].children[-1], float):
#                         if node.children[-1].children[0] == '-':
#                             IC_obj.rightValue = -node.children[-1].children[-1]
#                     else:
#                         IC_obj.rightValue = '-@' + str(self.generate(node.children[-1].children[-1]))
                
#                 IC_obj = AssignIC()
#                 self.intermediateCodeBuf.append(IC_obj)
#                 # IC_obj.NXQ = len(self.intermediateCodeBuf)    # 暂时设为当前的四元式的编号
#                 # IC_obj.NXQ = '?'
#                 IC_obj.action = ':='
#                 IC_obj.leftValue = node.children[0].name


#             if node.__class__.__name__ == 'Binary_Operation':
#                 IC_obj = BinOpIC()
#                 self.intermediateCodeBuf.append(IC_obj)
#                 currentNO = len(self.intermediateCodeBuf)

#                 # 左结点
#                 if node.children[0].__class__.__name__ == 'IdNode':
#                     IC_obj.leftOperand = node.children[0].name
#                 elif isinstance(node.children[0], int) or isinstance(node.children[0], float):
#                     IC_obj.leftOperand = node.children[0]
#                 elif node.children[0].__class__.__name__ == 'Binary_Operation':
#                     IC_obj.NXQ = '@' + str(self.generate(node.children[0]))
#                 elif node.children[0].__class__.__name__ == 'Unary_Operation':
#                     if isinstance(node.children[0].children[-1], int) or isinstance(node.children[0].children[-1], float):
#                         if node.children[0].children[0] == '-':
#                             IC_obj.rightValue = -node.children[0].children[-1]
#                     else:
#                         IC_obj.rightValue = '@' + str(self.generate(node.children[0].children[-1]))
                
#                 # 中间结点
#                 IC_obj.action = node.children[1]

#                 # 右结点
#                 if node.children[-1].__class__.__name__ == 'IdNode':
#                     IC_obj.leftOperand = node.children[-1].name
#                 elif isinstance(node.children[-1], int) or isinstance(node.children[-1], float):
#                     IC_obj.leftOperand = node.children[-1]
#                 elif node.children[-1].__class__.__name__ == 'Binary_Operation':
#                     IC_obj.NXQ = '@' + str(self.generate(node.children[-1]))
#                 elif node.children[-1].__class__.__name__ == 'Unary_Operation':
#                     if isinstance(node.children[-1].children[-1], int) or isinstance(node.children[-1].children[-1], float):
#                         if node.children[-1].children[0] == '-':
#                             IC_obj.rightValue = -node.children[-1].children[-1]
#                     else:
#                         IC_obj.rightValue = '@' + str(self.generate(node.children[-1].children[-1]))

#                 return currentNO

#             # if node.__class__.__name__ == 'Unary_Operation':
#             #   if isinstance(node.children[-1], int) or isinstance(node.children[-1], float):
#             #       if node.children[0] == '-':

#         if isinstance(node, AST.Node):
#             for child in node.children:
#                 self.generate(child)

#     def print_IC(self):
#         self.generate(self.rootNode)
#         for IC in self.intermediateCodeBuf:
#             IC.show()