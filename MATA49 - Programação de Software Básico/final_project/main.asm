%include "io.inc"

section .bss
    input resb 61
    substring resb 41
    inversed_substring resb 41
    concatened_substring resb 41
    transformed_substring resb 41
    alpha_positions resb 41
    average resb 1
    chars_counter resb 128 ; Caracteres ASCII
    char resb 2

section .data
    
section .text
    
global CMAIN

; Função auxiliar para zerar um vetor (EAX = endereço, ECX = tamanho)
clear_vector:
    mov esi, 0
    mov ebx, 0
    
    dec ECX ; Decrementa ECX pois o índice ESI vai de zero à (tamanho - 1)
    
clear:
    mov [eax + esi], ebx
    inc esi
    
    loop clear
    
    xor eax, eax
    ret
    
CMAIN:
    mov ebp, esp; for correct debugging
    GET_STRING input, 61
    
    ; Obtém a substring do input.
    call get_substring
    
    PRINT_STRING substring
    NEWLINE
    NEWLINE
    
    ; Limpa o vetor contador
    mov eax, chars_counter
    mov ecx, 41
    call clear_vector
    
    ; Limpa o vetor de posições dos caracteres
    mov eax, alpha_positions
    mov ecx, 41
    call clear_vector
    
    ; Realiza a contagem de caracteres e mostra o resultado.
    call count_chars
    PRINT_DEC 1, [chars_counter + 97] ; Quantidade de "a"
    NEWLINE
    
    PRINT_DEC 1, [chars_counter + 109] ; Quantidade de "m"
    NEWLINE
    NEWLINE
    
    ; Inverte a substring.
    call inverse_substring
    PRINT_STRING inversed_substring
    NEWLINE
    NEWLINE
    
    ; Concatena as palavras da substring.
    call concat_substring
    PRINT_STRING concatened_substring
    NEWLINE
    NEWLINE
    
    ; Transforma a string, alternando o "case" dos caracteres, a cada 2 e 3 caracteres.
    call transform_substring
    PRINT_STRING transformed_substring
    NEWLINE
    NEWLINE
    
    ; Imprime cada caractere das palavras, seguido de sua posição no alfabeto.
    call print_alpha_positions
    NEWLINE
    NEWLINE
    
    ; Ordena o vetor utilizando o BubbleSort e o imprime na tela.
    call sort_vector
    call print_sorted_alpha_vector
    NEWLINE

 
    ; Obtém a média das posições das letras no alfabeto.
    call get_average
    PRINT_DEC 2, average

    xor eax, eax
    ret




; ITEM 1: Coleta a substring da entrada do usuário.
get_substring: 
    mov ecx, 41

    mov esi, input + 7
    mov edi, substring
    
    rep movsb
    
    xor eax, eax
    ret 




; ITEM 2: Contar quantos caracteres X existem na substring. 
count_chars:
    mov ebx, 0
    mov ecx, 41
    mov esi, 0 
     
count:
    mov bl, [substring + esi]
    mov eax, [chars_counter + ebx]
    
    inc eax
    mov [chars_counter + ebx], eax
    
    inc esi
    loop count
    
    xor eax, eax
    ret 
   
    
     
       
; ITEM 3: Inverter a substring
inverse_substring:
    mov ecx, 41
    
    mov esi, substring
    mov edi, inversed_substring + 40  ; 41 - 1 pois aqui se trata do índice do elemento, que começa em zero
    
inverse:
    movsb
    
    dec edi
    dec edi

    loop inverse

    xor eax, eax
    ret   




; ITEM 4: Concatenar a substring.
concat_substring:
    mov eax, 0
    mov ecx, 41
    mov esi, 0
    mov edi, 0 
    
concat:    
    mov al, [substring + esi]  
    inc esi
    
    cmp eax, 32 ; ID do caractere de espaço = 32
    jne insert

    loop concat
    
finish:   
    xor eax, eax
    ret 

insert:
    mov [concatened_substring + edi], al
    inc edi
    dec ecx
    
    ; Se contador = 0, ele acaba a execução.
    cmp ecx, 0
    je finish
    
    ; Se não, prossegue para o próximo caractere.
    jmp concat
    
    
    
    
; ITEM 5: Transformar a substring de forma a ter 2 letras maiúsculas e 3 minúsculas em sequência.
transform_substring:
    mov eax, 0
    mov ebx, 2
    mov ecx, 41
    mov edx, 0
    mov esi, 0
    
transform: 
    dec ecx
    
    ; Verifica se já chegou ao final da substring.
    cmp ecx, 0
    jl finish_transform
    
    ; Obtém o caractere.
    mov al, [substring + esi]

    ; Ignora o caractere de espaço
    cmp al, 32;
    je insert_char
    
    ; Alterna entre letras maiúsculas e minúsculas, quando EBX = 0.   
    cmp ebx, 0
    je switch_case
        
execute_operation:
    dec ebx
 
    cmp al, 0 ; Caracteres com sinal, isto é, com ASCII code maior que ord(z) são negativos.
    jl execute_operation_with_sign
 
    cmp edx, 0
    je to_upper
    jmp to_lower

execute_operation_with_sign:
    cmp edx, 0
    je to_upper_with_sign
    jmp to_lower_with_sign

insert_char:
    mov [transformed_substring + esi], al
    inc esi
    jmp transform 

finish_transform:
    xor eax, eax
    ret 
    
switch_case:
    not edx ; Alterna entre 0 e -1
    
    ; Soma ao EAX +0 ou +1, dependendo do estado atual: letra maiúscula ou minúscula.
    mov ebx, 2
    sub ebx, edx

    jmp execute_operation
    
to_upper:
    cmp al, 90
    jg sub_id
    jmp insert_char

to_upper_with_sign:
    cmp al, 223
    jg sub_id
    jmp insert_char

sub_id:
    sub al, 32
    jmp insert_char

to_lower:
    cmp al, 97
    jl add_id
    jmp insert_char
    
to_lower_with_sign:
    cmp al, 224
    jl add_id
    jmp insert_char
    
add_id:
    add al, 32
    jmp insert_char
    



; ITEM 6: Imprimir a posição de cada letra da substring no alfabeto.

; OBS: Acabo de ser informado que não é necessário considerar letras 
; com sinais. Sendo assim, o código abaixo irá considerar que a substring
; é formada apenas por caracteres no range [A-Za-z] + SPACE.
print_alpha_positions:
    mov eax, 0
    mov ecx, 41
    mov esi, 0
    
print_alpha: 
    dec ecx
    
    ; Verifica se já chegou ao final da substring.
    cmp ecx, 0
    jl finish_printing

    ; Obtém o caractere.
    mov al, [substring + esi]
    inc esi
    
    ; Ignora o caractere de espaço
    cmp al, 32;
    je print_alpha
    
    ; Transforma o caractere em maiúsculo.
    cmp al, 90
    jg sub_char_id

print_position:
    ; Imprime o caractere.
    mov [char], al
    PRINT_STRING char 
    
    sub al, 64   
    
    ; Imprime o separador.
    mov dl, ':'
    mov [char], dl
    PRINT_STRING char
    
    ; Imprime a posição da letra.
    mov [char], al
    PRINT_DEC 1, [char]
    
    NEWLINE
    
    ; Armazena a posição em um vetor, para ser utilizando no processo do ITEM 7.
    mov edi, esi
    dec edi
    mov [alpha_positions + edi], al  

    jmp print_alpha

finish_printing:      
    xor eax, eax
    ret 
                      
sub_char_id:
    sub al, 32
    jmp print_position
    
    
    
    
; ITEM 7.1: Ordena o vetor das posições utilizando BubbleSort.
sort_vector:
    mov eax, 0
    mov ebx, 0
    mov edx, 0
    
out_loop:
    mov ecx, 40 ; 41 - 1 pois precisamos verificar sempre o número sucessor.
    sub ecx, edx
    
    mov esi, 0
    mov edi, 1
    
    cmp ecx, 0
    je finish_sort
    
    inc edx
    jmp in_loop
   
finish_sort:   
    xor eax, eax
    ret   
    
in_loop:   
    mov al, [alpha_positions + esi]
    mov bl, [alpha_positions + edi]
    
    cmp al, bl
    jl swap_values

continue_in_loop:
    mov [alpha_positions + esi], al
    mov [alpha_positions + edi], bl
    
    inc esi
    inc edi
    
    loop in_loop
    jmp out_loop
 
swap_values:
    mov ah, al
    mov bh, bl
    mov al, bh
    mov bl, ah
    jmp continue_in_loop

; Imprime o vetor ordenado.
print_sorted_alpha_vector:
    mov ecx, 41

print_vector:
    dec ecx
    
    mov esi, 40
    sub esi, ecx
    
    PRINT_DEC 1, [alpha_positions + esi]
    NEWLINE
    
    cmp ecx, 0
    jne print_vector ; Eu faço isso manualmente para evitar o erro "short jump is out of range"
    
    xor eax, eax
    ret 
    
            
; ITEM 7.2: Obter a média das posições dos caracteres da substring no alfabeto.
get_average:
    mov eax, 0
    mov ebx, 0
    mov ecx, 41
    mov edx, 0
    mov esi, 0
    
calculate: 
    mov bl, [alpha_positions + esi]
    inc esi
    
    ; Ignora os espaços no cálculo.
    cmp bl, 0
    je continue
    
    inc edx
    
    ; Soma a posição.
    add eax, ebx

continue:            
    loop calculate
       
    ; Faz a divisão do somatório pela quantidade de caracteres (ignorando espaços).
    mov ebx, edx
    mov edx, 0
    div ebx
    
    mov [average], eax
    
    xor eax, eax
    ret     