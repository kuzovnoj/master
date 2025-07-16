def calculate(exp):
    sp1 = exp.split(' ')
    stack1 = []
    stack2 = []
    for i in sp1:
        if i.isdigit():
            stack2.append(int(i))
        else:
            if i == '+':
                if not stack1:
                    stack1.append(i)
                elif stack1[-1] == '(':
                    stack1.append(i)
                else:
                    elem1 = stack2.pop()
                    elem2 = stack2.pop()
                    stack2.append(elem1 + elem2)
            elif i == '-':
                if not stack1:
                    stack1.append(i)
                elif stack1[-1] == '(':
                    stack1.append(i)
                else:
                    elem1 = stack2.pop()
                    elem2 = stack2.pop()
                    stack2.append(elem1 - elem2)
            elif i == '*':
                if not stack1:
                    stack1.append(i)
                elif stack1[-1] == '(' or stack1[-1] == '+' or stack1[-1] == '-':
                    stack1.append(i)
                else:
                    elem1 = stack2.pop()
                    elem2 = stack2.pop()
                    stack2.append(elem1 * elem2)
            elif i == '/':
                if not stack1:
                    stack1.append(i)
                elif stack1[-1] == '(' or stack1[-1] == '+' or stack1[-1] == '-':
                    stack1.append(i)
                else:
                    elem1 = stack2.pop()
                    elem2 = stack2.pop()
                    stack2.append(elem1 / elem2)
            elif i == '^':
                elem1 = stack2.pop()
                elem2 = stack2.pop()
                stack2.append(elem1 ^ elem2)

            elif i == '(':
                stack1.append(i)
            elif i == ')':
                while stack1[-1] != '(':
                    operator = stack1.pop()
                    elem1 = stack2.pop()
                    elem2 = stack2.pop()
                    stack2.append(eval(str(elem1) + operator + str(elem2)))
    print(stack2)
    return stack2[0]


print(calculate('2 + 3 - 5 * 3'))