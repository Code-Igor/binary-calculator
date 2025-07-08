# Trabalho desenvolvido por Igor e Caio.


# funçao que soma, criada para ser reutilizada depois
def somar(n1,n2):
    
    #
    resultado = ''

    # definindo a variavel carry, que lida com os excessos criadas pelo 1+1
    carry = '0'

    # laço de repetição para passar pelos bits dos bytes
    for bit in range(7,-1,-1): # ou len(n1)        
      # pega os valores de cada bit
        bit1 = n1[bit]
        bit2 = n2[bit]

      #variavel soma, controla a soma entre os bits
        soma = bit1 + bit2
                 

        # verificações para mudar ela de acordo com cada situação

        if soma == '00': # or soma == '0'
                   
            #verificando o carry, para saber se a soma irá mudar
            if carry == '1':
                soma = '1'
                carry = '0'
            elif carry == '0': #usando elif ao inves de else só por segurança
                soma = '0'


        elif soma == '01' or soma == '10': # or soma =='1

            if carry == '1':
                soma = '0'
            elif carry == '0':
                soma = '1'
                    

        elif soma == "11":

            if carry == '1':
                soma = '1'
            elif carry == '0':
                soma = '0'

            carry = '1'
                

                # recebe a soma e a coloca a esquerda do resultado
        resultado = soma + resultado 


    """
    prints que usamos para verificar erros no código
                
    print('bit1 = '+bit1,'bit2 = '+bit2)
    print('soma antes das verificações:'+soma)
    print('soma depois das verificações: '+soma)
    print('carry:'+carry)
    print('resultado:'+resultado)
    """  
            
    # agora nessa parte do codigo vamos verificar se ocorreu um overflow

    # variaveis para saber o valor do sinal
    somaValor = ''
    resultadoValor = ''
                
    #verifica apenas o primerio bit, para sabermos os sinais do n1, n2 e do resultado, 
    # isso será importante para ver se no final gera ou n um overflow
    for bit in range(7,-1,-1):
        bit1 = n1[bit]
        bit2 = n2[bit]
        bitR = resultado[bit]
                    
                    
        if bit1 == '0' and bit2 == '0':
            somaValor = 'positivo'

        elif bit1 == '1' and bit2 == '1':
            somaValor = 'negativo'
                
        else: # no caso cada byte tem um sinal diferente de si
            somaValor = 'diferente'

                
        if bitR == '0':
            resultadoValor = 'positivo'
        elif bitR == '1':
            resultadoValor = 'negativo'

                
    # resumindo, quando os dois bytes que somamos são de um mesmo sinal mas geram um resultado de sinal diferente
    # gera um overflow
    # logo aqui verificamos que, primeiro, se n1 e n2 possuem valores de sinais iguais
    # depois se esse valor de sinal é igual ao sinal do resultado final
    # no incio achavamos que apenas sobrar um carry gerava um overflow mas descobrimos que nao
    if somaValor != 'diferente' and somaValor != resultadoValor:
        raise ValueError("overflow")
            
    # verifica se o resultado deu overflow na maneira mais tradicional, por segurança caso tneha passado da 
    # primeira verificacao
    elif len(resultado) > 8:
        raise ValueError("overflow")
            
    # colocando um underflow, caso, por algum motivo, a calculadora retornar um valor abaixo de 1 byte
    elif len(resultado) < 8:
        raise ValueError("underflow")
            
    return resultado



# fução de inversao do sinal de um binario, criada para uma melhor organização
def inverterSinal(n):

    n = str(n) # colocando isso apenas para deixar a função mais "funcional", porque nesse trabalho isso n é necessário

    nInvertido = ''

    # laço que pega cada bit (menos o ultimo) e o troca, se 0 entao 1, se 1 entao 0
    for bit in range(len(n)-1):
        bit = n[bit]

        if bit =='0':
            bit = '1'
        elif bit == '1':
            bit = '0'
         
        #adiciona o bit trocado a variavel
        nInvertido += bit
    
    # adiciona o um no ultimo bit
    nInvertido = nInvertido + '1'

    return nInvertido




def calcular (n1,n2, operacao):
    """
    "calcular" realiza operações entre dois números binários de 1 byte
    n1: primeiro número binário
    n2: segundo número binário
    operacao: operação a ser realizada ('+', '-', '*' ou '/')
    return: resultado da operação
    """

    """
    estavamos apenas transformando os dados para string, porém fomos obrigados
    a pedir para o usuario dar um valor em string, caso não seja o sistema retorna um erro.
    motivos: 0000000 é igual a 0 em python. e zeros a esquerda de um, como 01000000, 
    retorna erro por padrão pelo python, pois para octais ele pede 0o:
    "SyntaxError: leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers"
    """ 

    # verificando se os valores são uma string, motivos citados acima
    if not isinstance(n1, str) or not isinstance(n2, str):
        raise TypeError("tipo invalido, esperado uma string")


    # verificando se os valores são válidos
    # passa por cada caracter verificando se é 0 ou 1, caso não seja dispara 
    if any(i not in "01" for i in n1 + n2):
        raise ValueError("valor invalido") 
        

    # verificando se os valores estão no tamanho de 1 byte usando len
    if len(n1) !=8 or len(n2) != 8:
        raise ValueError("tamanho da entrada invalido")
    

    # convertendo o valor da operacao para string só para garantir
    operacao = str(operacao)



    #verificando qual operação foi escolhida utilizando o match
    match operacao:
        case '+':

            soma = somar(n1,n2)
            return soma
            

        case '-':
            
            # a-b = a+(-b), por isso separamos a operação de soma numa função, e a inversao para deixar organizado

            n2Negativo = inverterSinal(n2)

            subtração = somar(n1,n2Negativo)
            return subtração
        
        
        case 'x':

            resultadoMulti = ''
            resultadosMulti = [] 
    
            deslocamento = 0 # representa e controla o deslocamento da soma para a esquerda

    #multiplicação, usando uma lógica parecida com a q usei na soma
     #passa por cada bit do n2
            for bit in range(7, -1, -1):
                bit2 = n2[bit]

        # multiplica o bit do n2 com cada bit do n1
                for bit in range(7, -1, -1):
                    bit1 = n1[bit]

                    multiplicacao = bit1 + bit2

                    if multiplicacao == '00':
                        multiplicacao = '0'
                    elif multiplicacao == '01' or multiplicacao == '10':
                        multiplicacao = '0'
                    elif multiplicacao == '11':
                        multiplicacao = '1'
            
            # 
                    resultadoMulti = multiplicacao + resultadoMulti
        
                # adiciona um 0 a string de acordo com o deslocamento
                for bit in range(deslocamento):
                    resultadoMulti += '0'

                deslocamento += 1 #aumenta o deslocamento a cada iteração

                resultadosMulti.append(resultadoMulti.zfill(16)) # preenche a esquerda da string resultadoMulti 
                # com zeros até que ela tenha exatamente 16 caracteres. importante para a soma
                resultadoMulti = ''
    

            resultadoSoma = ''
            carry = '0'

            for bit in range(15, -1, -1):
                # começa com o carry da iteração anterior
                colSoma = carry

                 # para cada número binário da lista, soma o bit atual 
                for binario in resultadosMulti:

                    # converte os bits e acumula a soma como string (0 + 1, 1 + 1, etc)
                    colSoma = str(int(colSoma) + int(binario[bit]))

                # usando a logica de (bit+bit+carry)
                # conta quantos 1 há na soma acumulada da coluna
                if colSoma.count('1') == 0:
                    # nenhum 1 na soma, resultado é 0 e não há carry
                    resultadoSoma = '0' + resultadoSoma
                    carry = '0'
                elif colSoma.count('1') == 1:
            # um único 1, resultado é 1 e não há carry
                    resultadoSoma = '1' + resultadoSoma
                    carry = '0'
                elif colSoma.count('1') == 2:
                    # dois 1, resultado é 0 e carry vai para a próxima coluna
                    resultadoSoma = '0' + resultadoSoma
                    carry = '1'
                else:
                    # três ou mais 1, resultado é 1 e também há carry
                    resultadoSoma = '1' + resultadoSoma
                    carry = '1'

            # agora, trata o overflow e elimina zeros excedentes à esquerda mantendo o formato 8 bits
    
            # resultadoSoma tem 16 bits (resultado da multiplicação)
            # Precisamos reduzir para 8 bits, tratando overflow
    
            # Pega os 8 bits menos significativos
            resultado8bits = resultadoSoma[-8:]
            # pega os bits excedentes à esquerda
            excedente = resultadoSoma[:-8]

    
    # overflow ocorre se os bits excedentes não forem todos iguais ao bit de sinal do resultado8bits
    # ou seja, se o número não pode ser representado em 8 bits com sinal
            sinal = resultado8bits[0]
            overflow = False
            for bit in excedente:
                if bit != sinal:
                    overflow = True
                    break

            if overflow:
                raise ValueError("overflow")
            else:
        # se não overflow, eliminamos os zeros excedentes à esquerda (que devem ser iguais ao sinal)

                pass

    # retorna o reusultado da soma/ resultado final de 8 bits
            return resultado8bits

        
                   
 

"""
# testando

calculando = calcular("","",'-')
print(calculando)

calculando = calcular("00000000","00000000",'+')
print(calculando)

calculando = calcular("011111110","00000000",'+')
print(calculando)

calculando = calcular("00000010","00000010",'x')
print(calculando)
    
calculando = calcular("01000000","01000000",'x')
print(calculando)
    
"""