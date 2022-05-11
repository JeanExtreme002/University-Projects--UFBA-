#include <iostream>
using namespace std;

/*
A fórmula para calcular os Números de Calatan é: (2N)! / [(N + 1)! * N!]. No entanto, 
podemos reduzi-la, dividindo (2N)! por (N + 1)!, a fim de otimizar o código. Dessa forma,
teríamos o produtório de (N + 2) até 2N, dividido pelo fatorial de N. Exemplo:

f(7) = (2 * 7)! / [(7 + 1)! * 7!] = 14! / (8! * 7!) = (14 * 13 * 12 * 11 * 10 * 9) / 7!

Sabendo disso, a função abaixo irá calcular um Número de Calatan, seguindo a ideia
descrita acima, separando em dois arrays os numeradores e denominadores, e dividindo-os
para que possa se chegar em um resultado sem precisar calcular números grandes, evitando
que o valor seja maior que o valor máximo do tipo <T> em C++.
*/
unsigned long long getCalatanNumber(int n) {

    // Obtém os números do numerador.
    int numerator[n - 1];
    int aux = n + 2;

    for (int i = 0; i < n - 1; i++) {
        numerator[i] = aux++;
    }

    // Obtém os números do denominador.
    int denominator[n];

    for (int i = 0; i < n; i++) {
        denominator[i] = i + 1;
    }

    // Divide os numeradores pelos denominadores, se divisível.
    for (int i = 0; i < n; i++) {
        for (int x = 0; x < n - 1; x++) {
            int a = numerator[x];
            int b = denominator[i];

            // Se A for divisível por B, o numerador será dividido pelo denominador.
            if ((a % b) == 0) {
                numerator[x] = a / b;
                denominator[i] = 1;
                break;
            }
        }
    }

    unsigned long long result = 1;

    // Multiplica todos os valores do numerador.
    for (int x = 0; x < n - 1; x++) {
        result *= numerator[x];
    }

    // Divide o resultado do produto pelo denominador.
    for (int i = 0; i < n; i++) {
        result /= denominator[i];
    }

    return result;
}

int main() {
    int n;

    cout << "Stop at position: ";
    cin >> n;

    for (int i = 0; i <= n; i++) {
        cout << getCalatanNumber(i) << endl;
    }
}