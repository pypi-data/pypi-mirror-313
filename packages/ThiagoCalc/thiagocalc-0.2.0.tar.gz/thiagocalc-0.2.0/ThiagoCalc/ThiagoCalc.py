class Calculadora:
    def __init__(self, numero1, numero2):
        self.numero1 = numero1
        self.numero2 = numero2

    def somar(self):
        return self.numero1 + self.numero2

    def subtrair(self):
        return self.numero1 - self.numero2

    def multiplicar(self):
        return self.numero1 * self.numero2

    def dividir(self):
        if self.numero2 != 0:
            return self.numero1 / self.numero2
        else:
            return "Erro: divisão por zero não é permitida"



# class User:
#     def operar_calculadora(self):
#         while True:
#             entrada = input("Digite 'parar' para sair ou qualquer tecla para continuar: ").strip().lower()
#             if entrada == 'parar':
#                 print("Operação encerrada.")
#                 break

#             try:
#                 numero1 = float(input("Digite o primeiro número: "))
#                 numero2 = float(input("Digite o segundo número: "))
#                 operacao = input("Escolha a operação (+, -, *, /): ").strip()

#                 calc = Calculadora(numero1, numero2)

#                 if operacao == '+':
#                     print("Resultado:", calc.somar())
#                 elif operacao == '-':
#                     print("Resultado:", calc.subtrair())
#                 elif operacao == '*':
#                     print("Resultado:", calc.multiplicar())
#                 elif operacao == '/':
#                     print("Resultado:", calc.dividir())
#                 else:
#                     print("Operação inválida.")
#             except ValueError:
#                 print("Erro: digite números válidos.")

# # uso
# user = User()
# user.operar_calculadora()