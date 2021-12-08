#include <iostream>
#include <cmath>
using namespace std;

int draw_pyramid(int *array, int size) {
    int base_size = 0;

    // Obtém o tamanho da base da pirâmide.
    for (int column = 0; column < size; column++) {
        base_size += to_string(*(array + (size - 1) * size + column)).length() + 1;
    }

    int half_base_size = base_size / 2;
    int r_size = to_string(size).length();

    // Imprime cada linha da pirâmide, alinhando ela no meio.
    for (int row = 0; row < size; row++) {
        string row_string = "";

        // Obtém cada valor da linha e adiciona à string.
        for (int column = 0; column <= row; column++) {
            row_string += to_string(*(array + row * size + column)) + " ";
        }

        int spacing_length = half_base_size - ((int) row_string.length() / 2);

        // Imprime a linha atual.
        cout << row << string(r_size - to_string(row).length(), ' ') << " | ";
        cout << string(spacing_length, ' ') << row_string << endl;
    }
}

int main() {
    cout << "Tamanho: ";

    int size;
    cin >> size;
    size++;

    int numbers[size][size];

    // Zera todos os valores do array.
    for (int row = 0; row < size; row++) {
        for (int column = 0; column < size; column++) {
            numbers[row][column] = 0;
        }
    }

    for (int row = 0; row < size; row++) {
        for (int column = 0; column <= row; column++) {
            // Se a coluna e a linha forem diferentes de zero, o valor será a soma dos valores da linha anterior
            // na coluna "column" e "column - 1". Senão, o valor será 1.
            numbers[row][column] = column == 0 || row == 0 ? 1 : numbers[row - 1][column] + numbers[row - 1][column - 1];
        }
    }

    draw_pyramid((int*) numbers, size);
}
