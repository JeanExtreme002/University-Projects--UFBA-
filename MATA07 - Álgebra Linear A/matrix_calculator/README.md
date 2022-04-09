# Sobre:

Essa é uma aplicação, em Python 3, para realizar operações de matrizes. Através do terminal, é possível realizar quatro tipos de instruções: comandos de terminal, operações de matrizes, operações de linhas de matrizes e operações aritméticas com elementos de matrizes. Os comandos de terminal são escritos sempre em **minúsculo**, enquanto em operações de matrizes, a instrução sempre inicia-se com o nome de uma matriz em **maiúsculo**, com letras apenas — ela pode ser criada dinamicamente como uma variável — seguida do operador de atribuição.

Para operações de linhas de matrizes, a instrução deve ser iniciada com um **L maiúsculo**, seguida da posição da linha (valor inteiro) na matriz, no qual será manipulada. Já em operações aritméticas com elementos de matrizes, os elementos devem ser escritos com um **E maiúsculo**, seguidos da sua posição (linha, coluna) separados por uma vírgula.

Aviso: Na documentação, os nomes de matrizes possuirão o caractere underline (`_`) apenas para facilitar a visualização dos mesmos. No entanto, isso não é permitido na aplicação. Somente letras maiúsculas!

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
| delete \<matrix\>          | Deleta uma matriz                                    |
| execute \<arquivo.ext\>    | Carrega um arquivo de instruções e as executa        | 
| exit                       | Encerra o programa                                   |
| help                       | Mostra uma lista com todos os comandos do terminal   |
| list                       | Mostra uma lista com todas as matrizes               |
| load \<arquivo.ext\>       | Carrega um arquivo contendo matrizes                 |
| log \<true \| false\>      | Mostra os comandos anteriores                        |
| prop \<matrix\>            | Mostra uma lista com todas as propriedades da matriz |
| save \<arquivo.ext\>       | Salva as matrizes em um arquivo                      |
| show \<true \| false\>     | Mostra a matriz que está sendo utilizada             |
| use \<matrix\>             | Define uma matriz para ser utilizada                 |
  
# Operações de Matrizes:

```
MATRIZ_A = MATRIZ_B + MATRIZ_C  // Soma de Matrizes
  
MATRIZ_A = Matriz_B - MATRIZ_C  // Subtração de Matrizes
  
MATRIZ_A = MATRIZ_B * Escalar   // Multiplicação por Escalar
  
MATRIZ_A = MATRIZ_B / Escalar   // Divisão por Escalar
  
MATRIZ_A = MATRIZ_B * MATRIZ_C  // Produto de Matrizes

MATRIZ_A = MATRIZ_B c           // Conjugada

MATRIZ_A = MATRIZ_B t           // Transposta
  
MATRIZ_A = MATRIZ_B ct          // Conjugada e Transposta (equivalente à "tc")

MATRIZ_A = MATRIZ_B tc          // Transposta e Conjugada (equivalente à "ct")

MATRIZ_A = MATRIZ_B adj         // Matriz adjunta

MATRIZ_A = MATRIZ_B cof         // Matriz cofatora

MATRIZ_A = MATRIZ_B inv         // Matriz inversa

MATRIZ_A = MATRIZ_B m(r, c)     // Menor complementar da matriz a partir de (linha, coluna)
```
 
**OBSERVAÇÃO:** O escalar, nessa e em todas as outras operações, podem ser complexos. No entanto, diferentemente dos valores complexos
salvos no arquivo de matrizes, aqui ele deve obrigatoriamente estar dentro de parênteses. Exemplo: `(-3+4i) (-i) (-5.7i) (i) (4.2-9.3i)`.
 
# Operações de Linhas de Matrizes:
  
```
L(a) <> L(b)                    // Troca a posição entre duas linhas
  
L(a) == L(b)                    // Verifica a igualdade das linhas
  
L(a) += XL(b)                   // Soma L(b) (opcional: multiplicado por um escalar) à linha L(a)
  
L(a) -= XL(b)                   // Subtrai L(b) (opcional: multiplicado por um escalar) da linha L(a)
  
L(a) *= X                       // Multiplica L(a) por um escalar
  
L(a) /= X                       // Divide L(a) por um escalar
```

# Operações Aritméticas com Elementos de Matrizes:

É uma expressão aritmética normal, possuindo um ou mais elementos da matriz no formato **E(r),(c)**. Nessa operação,
você não pode atribuir valores à matriz. Apenas utilizá-las para realizar cálculo, no qual, o resultado será mostrado na tela.
Veja o exemplo abaixo, em que todos os possíveis operadores aritméticos são utilizados:

```
5 * (E1,2 + 17.5 - E4,9) - (E5,5 ** 3) / 2 + E13,5 % 2 - E7,5 * ((3-i) - (i))
```
