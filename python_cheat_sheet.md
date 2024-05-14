# Cheat Sheet de Python

## Comentários
Comentários são linhas de código que não são executadas pelo interpretador. Em Python, os comentários são precedidos pelo caractere `#`. Para comentários de várias linhas, pode-se utilizar três aspas duplas `"""` no início e no fim do bloco de comentários.
```python
# Comentário de uma linha
"""
Comentário de várias linhas
"""
```

## Variáveis
Variáveis são espaços de memória que armazenam valores. Em Python, as variáveis são criadas no momento em que um valor é-lhe atribuído. O tipo da variável é inferido automaticamente pelo interpretador.

```python	
var = 1 # Inteiro
var = 1.0 # Ponto flutuante
var = "Hello, World!" # String
var = True # Booleano
var = [1, 2, 3] # Lista
```

## Operações com listas
Listas são coleções de elementos que podem ser de diferentes tipos. Em Python, as listas são indexadas a partir do zero.

```python
lista = [1, 2, 3, 4, 5]
print(lista[0]) # 1
lista[0] = 10 # [10, 2, 3, 4, 5]
lista[10] # IndexError, uma vez que o índice 10 não existe
```

Para além destas operações simples, existem funções que permitem manipular listas.

```python
lista = [1, 2, 3, 4, 5]
lista.append(6) # [1, 2, 3, 4, 5, 6]
lista.pop(1) # [1, 3, 4, 5, 6]
lista.remove(3) # [1, 4, 5, 6]
lista.insert(1, 2) # [1, 2, 4, 5, 6]
```

## Operações aritméticas
Python suporta as operações aritméticas básicas: adição `+`, subtração `-`, multiplicação `*`, divisão `/`, divisão inteira `//`, módulo `%` e exponenciação `**`.

```python
a = 10
b = 3
print(a + b) # 13
print(a - b) # 7
print(a * b) # 30
print(a / b) # 3.3333333333333335
print(a // b) # 3
print(a % b) # 1
print(a ** b) # 1000
```

## Condições
Em Python, as condições são expressas através das palavras-chave `if`, `elif` e `else`.

```python
a = 10
b = 20
if a > b:
    print("a é maior que b")
elif a < b:
    print("a é menor que b")
else:
    print("a é igual a b")
```

Também existem operandos de comparação que podem ser utilizados em condições.

```python
a = 10
b = 20
if a == b:
    print("a é igual a b")
if a != b:
    print("a é diferente de b")
if a > b:
    print("a é maior que b")
if a < b:
    print("a é menor que b")
if a >= b:
    print("a é maior ou igual a b")
if a <= b:
    print("a é menor ou igual a b")
```

Por fim, existem comparadores lógicos que podem ser utilizados para combinar condições.

```python
a = 10
b = 20
if a > 0 and b > 0:
    print("a e b são positivos")
if a > 0 or b > 0:
    print("a ou b é positivo")
if not a > 0:
    print("a é negativo")
```

## Ciclos
Em Python, os ciclos são expressos através das palavras-chave `for` e `while`.

```python
for i in range(5):
    print(i) # 0 1 2 3 4
```

```python
i = 0
while i < 5:
    print(i) # 0 1 2 3 4
    i += 1
```

Podemos fazer variações dos loops, como por exemplo usar a keyword 'in' para iterar sobre uma lista.

```python
lista = [1, 2, 3, 4, 5]
for i in lista:
    print(i) # 1 2 3 4 5
```

Em Python, 'break' e 'continue' são utilizados para controlar o fluxo de execução de um ciclo. 'break' é utilizado para sair do ciclo, enquanto 'continue' é utilizado para passar para a próxima iteração.

```python
for i in range(5):
    if i == 3:
        break
    print(i) # 0 1 2
```

```python
for i in range(5):
    if i == 3:
        continue
    print(i) # 0 1 2 4
```

## Funções
Em Python, as funções são definidas através da palavra-chave `def`. Têm como objetivo encapsular um bloco de código que pode ser reutilizado em diferentes partes do programa.

```python
def soma(a, b):
    return a + b

print(soma(10, 20)) # 30
```

## Classes
Em Python, as classes são definidas através da palavra-chave `class`. Permitem criar objetos que possuem propriedades e métodos. Podemos simplificar propriedades como sendo variáveis que caracterizam o objeto e métodos como funções que o objeto pode executar.

```python
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def apresentar(self):
        print(f"Olá, o meu nome é {self.nome} e tenho {self.idade} anos.")

pessoa = Pessoa("João", 20)
pessoa.apresentar() # Olá, o meu nome é João e tenho 20 anos.
```