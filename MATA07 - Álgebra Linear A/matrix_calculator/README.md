# Sobre:

Essa é uma aplicação escrita em Python 3 para realizar operações de matrizes. Através do terminal, é possível realizar três tipos de instruções: comandos de terminal, 
operações de matrizes e operações de linhas de matrizes. Os comandos de terminal são escritos sempre em **minúsculo**. Para realizar operações de matrizes, a instrução 
sempre inicia-se com o nome de uma matriz, sempre em **maiúsculo** sem sinal — ela pode ser criada dinamicamente como uma variável — seguida do operador de atribuição (igualdade).
Para operações de linhas de matrizes, a instrução deve ser iniciada com um **L maiúsculo**, seguida da posição da linha (valor inteiro) na matriz, no qual será manipulada.

# Arquivo de Matrizes:

O arquivo de matrizes pode estar em qualquer extensão, contendo quantas matrizes desejar, desde que esteja no seguinte formato:
```
MATRIZ_A X,Y: valor1, valor2, valor3...
MATRIZ_B X,Y: valor1, valor2, valor3...
```
Observação: Os valores também podem ser complexos, devendo estar no formato **x+yi** ou **x-yi**. Além disso, não é necessário preencher a matriz. Caso não
haja valores o suficiente, o resto dos elementos será automaticamente zero. Exemplo de arquivo:
```
MATRIZA 3,5: 5, -12, 8.5, -9+7i, 24-13.5i, 5+i, -34
MATRIZB 7,8: -4i, 5.7, 120, -7, -i, 0, 55, -1-i, 9999
```

# Comandos do Terminal:
| Comando                    | Descrição                                            |
| -------------------------- | ---------------------------------------------------- |
| delete                     | Deleta uma matriz                                    |
| exit                       | Encerra o programa                                   |
| help                       | Mostra uma lista com todos os comandos do terminal   |
| list                       | Mostra uma lista com todas as matrizes               |
| load \<arquivo.ext\>       | Carrega um arquivo contendo matrizes                 |
| log \<true \| false\>      | Mostra os comandos anteriores                        |
| prop                       | Mostra uma lista com todas as propriedades da matriz |
| save \<arquivo.ext\>       | Salva as matrizes em um arquivo                      |
| show \<true \| false\>     | Mostra a matriz que está sendo utilizada             |
| use <matrix>               | Define uma matriz para ser utilizada                 |
  
# Operações de Matrizes:

```
MATRIZ_A = MATRIZ_B + MATRIZ_C  // Soma de Matrizes
  
MATRIZ_A = Matriz_B - MATRIZ_C  // Subtração de Matrizes
  
MATRIZ_A = MATRIZ_B * Escalar   // Multiplicação por Escalar
  
MATRIZ_A = MATRIZ_B / Escalar   // Divisão por Escalar
  
MATRIZ_A = MATRIZ_B * MATRIZ_C  // Produto de Matrizes

MATRIZ_A = MATRIZ_B c           // Conjugada

MATRIZ_A = MATRIZ_B t           // Transposta
  
MATRIZ_A = MATRIZ_B ct          // Conjugada e Transposta

MATRIZ_A = MATRIZ_B tc          // Transposta e Conjugada
```
  
# Operações de Linhas de Matrizes:
  
```
L(a) <> L(b)                    // Troca a posição entre duas linhas
  
L(a) == L(b)                    // Verifica a igualdade das linhas
  
L(a) += XL(b)                   // Soma L(b) (opcional: multiplicado por um escalar) à linha L(a)
  
L(a) -= XL(b)                   // Subtrai L(b) (opcional: multiplicado por um escalar) da linha L(a)
  
L(a) *= X                       // Multiplica L(a) por um escalar
  
L(a) /= X                       // Divide L(a) por um escalar
```
