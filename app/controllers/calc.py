class calc():
    def calc(self, entrada):
        try:
            sinais = ['+', '-', '/', '*', '^']
            cont = 0
            dicionario = []
            dic = []
            for n in entrada:
                if n.isnumeric():
                    dic.insert(cont, n)
                    cont = cont + 1
                else:
                    for sinal in sinais:
                        if sinal in n:
                            dic.insert(cont, n)
                            cont = cont + 1
            result = ' '
            cont = 0
            while cont < dic.__len__():
                d = dic[cont]
                if d.isnumeric:
                    if d != '+' and d != '-' and d != '*' and d != '/' and d != '^' and d != '(' and d != ')':
                        if result in ' ':
                            result = d
                        else:
                            result = result + d
                    else:
                        dicionario.insert(cont - 1, float(result))
                        result = ' '
                    for sinal in sinais:
                        if sinal in d:
                            dicionario.insert(cont, d)

                cont = cont + 1
            if result in ' ':
                dicionario.insert(cont, 0)
            else:
                dicionario.insert(cont, float(result))

            def calc(num1, operacao, num2):
                if operacao is '+':
                    try:
                        return float(num1) + float(num2)
                    except:
                        print('erro', num1, '+', num2)
                if operacao is '-':
                    try:
                        return float(num1) - float(num2)
                    except:
                        print('erro', num1, '-', num2)
                if operacao is '*':
                    try:
                        return float(num1) * float(num2)
                    except:
                        print('erro', num1, '*', num2)
                if operacao is '/':
                    try:
                        return float(num1) / float(num2)
                    except:
                        print('erro', num1, '/', num2)
                if operacao is '^':
                    try:
                        return float(num1) ^ float(num2)
                    except:
                        print('erro', num1, '^', num2)

            cont = int(0)
            result = float(0)
            while cont < dicionario.__len__():
                if cont is 0:
                    result = calc(dicionario[cont], dicionario[cont + 1], dicionario[cont + 2])
                    # print(result, '[', 2, ']')
                    cont = cont + 3
                elif cont is 3:
                    result = calc(result, dicionario[cont], dicionario[cont + 1])
                    # print(result, '[', cont, ']')
                    cont = cont + 3
                else:
                    result = calc(result, dicionario[cont - 1], dicionario[cont])
                    # print(result, '[', cont - 2, ']')
                    cont = cont + 2
            return str(result)
        except:
            return None