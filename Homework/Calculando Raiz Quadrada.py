#lê o valor que se deseja calcular a raiz quadrada
raiz = float(input("Digite o número que deseja calcular a raiz quadrada: "))

#define a precisão do resultado
eps = float(input("Insira a precisão: "))

#define o intervalo do resultado
n1 = float(input("Insira a banda menor do resultado: "))

n2 = float(input("Insira a banda maior do resultado: "))

#realiza o cálculo da média e compara o resultado à raiz que se deseja calcular
while n2-n1 > eps:

    m = (n1+n2)/2

    if m*m < raiz: n1 = m

    elif m*m > raiz: n2 = m

    print ("A raiz de", raiz, "é: ", m)

