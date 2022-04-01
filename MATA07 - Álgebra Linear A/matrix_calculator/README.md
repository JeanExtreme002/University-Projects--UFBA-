# Sobre:

Essa é uma aplicação escrita em Python 3 para realizar operações de matrizes. Através do terminal, é possível realizar três tipos de instruções: comandos de terminal, 
operações de matrizes e operações de linhas de matrizes. Os comandos de terminal são escritos sempre em **minúsculo**. Para realizar operações de matrizes, a instrução 
sempre inicia-se com o nome de uma matriz, sempre em **maiúsculo** — ela pode ser criada dinamicamente como uma variável — seguida do operador de atribuição (igualdade).
Para operações de linhas de matrizes, a instrução deve ser iniciada com um **L maiúsculo**, seguida da posição da linha (valor inteiro) na matriz, no qual será manipulada.

# Comandos do Terminal:
| Comando                    | Descrição                                            |
| -------------------------- | ---------------------------------------------------- |
| exit                       | Encerra o programa                                   |
| help                       | Mostra uma lista com todos os comandos do terminal   |
| list                       | Mostra uma lista com todas as matrizes               |
| load \<arquivo.ext\>       | Carrega um arquivo contendo matrizes                 |
| log \<true \| false\>      | Mostra os comandos anteriores                        |
| prop                       | Mostra uma lista com todas as propriedades da matriz |
| show \<true \| false\>     | Mostra a matriz que está sendo utilizada             |
| use <matrix>               | Define uma matriz para ser utilizada                 |
  
# Operações de Matrizes:

```
Matriz_A = Matriz_B + Matriz_C  // Soma de Matrizes
  
Matriz_A = Matriz_B - Matriz_C  // Subtração de Matrizes
  
Matriz_A = Matriz_B * Escalar   // Multiplicação por Escalar
  
Matriz_A = Matriz_B / Escalar   // Divisão por Escalar
  
Matriz_A = Matriz_B * Matriz_C  // Produto de Matrizes

Matriz_A = Matriz_B c           // Conjugada

Matriz_A = Matriz_B t           // Transposta
  
Matriz_A = Matriz_B ct          // Conjugada e Transposta

Matriz_A = Matriz_B tc          // Transposta e Conjugada
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
