from stack import Stack

class Calculator:
    def __init__(self):
        self.org_exp = None #중위 표기법
        self.postfix_exp = None #후위 표기법
        self.result = None #결과

    def set_ori_exp(self, org_exp):
        self.org_exp = org_exp.replace(' ', '')
        self.postfix_exp = None
        self.result = None

    def get_org_exp(self):
        return self.org_exp

    def get_weight(self, oprt):
        if oprt == '*' or oprt == '/':
            return 9
        if oprt == '+' or oprt == '-':
            return 7
        if oprt == '(':
            return 5
        else:
            return -1

    def convert_to_postfix(self):
        exp_list = []
        oprt_stack = Stack()

        for char in self.get_org_exp():
            # char가 숫자인 경우
            if char.isdigit():
                exp_list.append(char)
            # char가 숫자가 아닌 경우(괄호나 연산자)
            else:
                # 연산자 스택이 비어있거나 char가 (인 경우
                if oprt_stack.empty() or char == "(":
                    # 해당 char를 stack에 넣는다
                    oprt_stack.push(char)
                # char가 )인 경우
                elif char == ")":
                    # 일단 oprt_stack의 맨 위 데이터를 꺼낸다.
                    op = oprt_stack.pop()
                    # (가 나올때 까지 반복
                    while op != '(':
                        # op를 exp_list에 append
                        exp_list.append(op)
                        # stack에서 맨 위 데이터를 다시 꺼낸다. 만약 (인 경우 while문 종료)
                        op = oprt_stack.pop()
                # char가 연산자이면서, oprt_stack의 peek보다 가중치가 큰 경우는 stack에 쌓는다.
                elif self.get_weight(char) > self.get_weight(oprt_stack.peek()):
                    oprt_stack.push(char)
                # char가 (,)가 아니면서, oprt_stack의 peek보다 가중치가 작은 경우
                else:
                    # oprt_stack이 비거나, char가 oprt_stack의 peek보다 가중치가 높아질 때 까지
                    while oprt_stack and self.get_weight(char) <= self.get_weight(oprt_stack.peek()):
                        # oprt_stack에서 연산자를 꺼내 exp_list에 append한다.
                        exp_list.append(oprt_stack.pop())
                    # while문이 종료되면(가중치가 높은 연산자를 exp_list에 append를 끝내면) oprt_stack에 해당 char(연산자)를 넣는다.
                    oprt_stack.push(char)

        # for문이 끝나면(org_exp의 끝까지 순회하면)
        # oprt_stack이 빈 stack이 될 때 까지
        while oprt_stack:
                # oprt_stack에 있는 연산자를 exp_list에 넣는다.
                exp_list.append(oprt_stack.pop())
        # 완성된 exp_list를 join해 postfix_exp로 만든다.
        self.postfix_exp = ''.join(exp_list)


    def get_postfix_exp(self):
        if not self.postfix_exp:
            self.convert_to_postfix()
        return self.postfix_exp

    def calc_two_pord(self, oprd1, oprd2, oprt):
        if oprt == '+':
            return oprd1+oprd2
        elif oprt == '-':
            return oprd1-oprd2
        elif oprt == '*':
            return oprd1*oprd2
        elif oprt == '/':
            return oprd1//oprd2

    def calculate(self):
        oprd_stack = Stack()
        for char in self.get_postfix_exp():
            if char.isdigit():
                oprd_stack.push(int(char))
            else:
                oprd2 = oprd_stack.pop()
                oprd1 = oprd_stack.pop()
                oprd_stack.push(self.calc_two_pord(oprd1, oprd2, char))
        self.result = oprd_stack.pop()

    def get_result(self):
        if not self.result:
            self.calculate()
        return self.result

if __name__ == "__main__":
    calc = Calculator()
    while 1:
        exp = input('수식을 입력하세요 (종료:0)')
        if exp == '0':
            break

        calc.set_ori_exp(exp)
        print(calc.get_org_exp())
        calc.convert_to_postfix()
        print(calc.get_postfix_exp())
        print('{exp} = {result}'.format(
                exp = calc.get_org_exp(), 
                result = calc.get_result()
            )
        ) 
