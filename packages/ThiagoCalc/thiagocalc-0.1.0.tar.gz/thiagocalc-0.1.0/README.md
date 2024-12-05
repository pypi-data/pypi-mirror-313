Documentação da Calculadora
Este módulo contém uma implementação simples de uma calculadora com operações básicas (soma, subtração, multiplicação e divisão). O módulo também inclui um mecanismo de interação com o usuário para executar essas operações de forma interativa no terminal.

Estrutura do Código
O código é composto por duas classes principais:

Calculadora: Realiza as operações matemáticas.

User: Responsável pela interação com o usuário e gerenciamento do fluxo de operações.

1. Classe Calculadora
A classe Calculadora é responsável pelas operações aritméticas básicas. Ela tem o seguinte formato:

somar(): Retorna a soma de numero1 e numero2.
subtrair(): Retorna a subtração de numero1 e numero2.
multiplicar(): Retorna a multiplicação de numero1 e numero2.
dividir(): Retorna a divisão de numero1 por numero2. Caso numero2 seja zero, retorna uma mensagem de erro ("Erro: divisão por zero não é permitida").
Exemplo de uso da Calculadora:
python
Copiar código
calc = Calculadora(10, 5)
print(calc.somar())  # Output: 15
print(calc.subtrair())  # Output: 5
print(calc.multiplicar())  # Output: 50
print(calc.dividir())  # Output: 2.0


pip install