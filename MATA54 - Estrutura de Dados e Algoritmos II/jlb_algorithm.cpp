#include <algorithm>
#include <bits/stdc++.h>
#include <chrono>
#include <cmath>
#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

int alphabet_list_length = 256;
int alphabet_list[256];  

int get_alphabet_size() {
    int size = 0;

    for (int i = 0; i < alphabet_list_length; i++) {
        if (alphabet_list[i] != -1) {
            size += 1;
        }
    }
    return size;
}

void set_alphabet(const string &alphabet) {
    for (int i = 0; i < alphabet_list_length; i++) {
        alphabet_list[i] = -1;
    }
    for (int i = 0; i < alphabet.size(); i++) {
        alphabet_list[(int) alphabet[i]] = i;
    }
}

int symbol_to_int(char symbol) {
    return alphabet_list[(int) symbol];
}

bool comparison_method(long long x, long long y);

long long to_int(const string &sequence, int base) {
    long long value = 0;

    int m = sequence.size();

    for (int index = 0; index < m; index++) {
        int integer = symbol_to_int(sequence[index]);

        if (integer == -1) {
            return - (index + 1);
        }

        int exponent = (m - 1) - index;

        value += integer * pow(base, exponent);
    }
    return value;
}

vector<int> search(const string &sequence, const string &pattern) {
    vector<int> occurrences;
    
    int n = sequence.size();
    int m = pattern.size();

    int base = get_alphabet_size();

    // Preprocessing phase ...
    long long pattern_value = to_int(pattern, base);

    long long frame = -1;
    int start_pos = 0;

    while (frame <= -1 && start_pos < n) {
        frame = to_int(sequence.substr(start_pos, m), base);
        
        if (frame <= -1) {
            start_pos -= frame;
        }
    }
    
    long long most_significant_digit_position = pow(base, m - 1);

    // Searching phase ...
    if (comparison_method(frame, pattern_value)) {
        occurrences.push_back(start_pos);
    }

    for (int i = start_pos + m; i < n; ++i) {
        int element = symbol_to_int(sequence[i]);

        int digit = (int)(frame / most_significant_digit_position);

        if (element == -1) {
            frame = -1;
            i += 1;

            while (frame <= -1 && i < n) {
                frame = to_int(sequence.substr(i, m), base);
                
                if (frame <= -1) {
                    i -= frame;
                }
            }
            i += m - 1;
        }
        else {
            frame = (frame - (digit * most_significant_digit_position)) * base;
            frame = round(frame + element);
        }

        if (comparison_method(frame, pattern_value)) {
            occurrences.push_back(i - m + 1);
        }
    }
    return occurrences;
}

// You can change the comparision method as you wish,
// but the comparision must have complexity O(1).
bool comparison_method(long long x, long long y) {
    return x <= y;
}

int main() {
    string text = "qaaqwawababbgghhjkcabbwaknqtbababbdaaabdwawaawaaa";
    string pattern = "abb";
    string alphabet = "abcd";  // It must be ordered

    cout << "Searching..." << endl;

    set_alphabet(alphabet);

    vector<int> occurrences = search(text, pattern);

    for (int i = 0; i < occurrences.size(); i++) {
        cout << "Found at position: " << occurrences[i] << endl;
    }
}