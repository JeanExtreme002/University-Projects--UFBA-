__doc__ = """
Esse é um projeto para a disciplina da Universidade
Federal da Bahia (UFBA) MATA-42, Matemática Discreta.

A aplicação em questão é um analisador de relação binária. Através dela,
o usuário pode verificar todas as suas propriedades, gerar a relação
em ordem lexicográfica e gerar o seu fecho, dada uma propriedade.
"""

__author__ = """
Jean Loui Bernard Silva de Jesus    <jeanjesus@ufba.br>
Victor Manoel Conceição de Almeida  <victor.manoel@ufba.br>
Guilherme Amaral Motta              <guilherme.motta@ufba.br>
"""

readme = "SOBRE:\n" + __doc__ + """
\nCRÉDITOS:

Jean Loui Bernard Silva de Jesus :
    - Módulo app.py
    - Módulo conjunto.py
    - Módulo __init__.py
    - Módulo diagrama.py
    - Módulo ordenador.py

Victor Manoel Conceição de Almeida :
    - Módulo propriedades.py

Guilherme Amaral Motta :
    - Módulo classe.py
    - Módulo conversor.py
"""

with open("README.txt", "w") as file:
    file.write(readme)

from conjunto import salvar_conjunto
from relacao import carregar_relacao, salvar_relacao, salvar_relacao_ciclica
from relacao.classe import obter_classe_de_equivalencia
from relacao.conversor import relacao_para_ciclica, relacao_para_matricial, verificar_permutabilidade
from relacao.diagrama import gerar_diagrama
from relacao.ordenador import ordenar_relacao
from relacao.propriedades import ANTI_SIMETRICA, CONGRUENCIA, REFLEXIVA, SIMETRICA, TRANSITIVA, obter_propriedades
from json.decoder import JSONDecodeError
import os, sys

def mostrar_propriedade(propriedade, status, motivo = [False, tuple()]):
    """
    Função para imprimir uma mensagem dizendo se
    a relação possui ou não determinada propriedade.
    """
    if propriedade == CONGRUENCIA:
        propriedade = "de Congruência"

    if status:
        print("- A relação é {}".format(propriedade))
    else:
        params = [propriedade, " " if motivo[0] else " não ", motivo[1]]
        print("- A relação não é {} porque{}possui o par {}".format(*params))

# Solicita ao usuário o nome do arquivo.
nome_do_arquivo = input("Nome do arquivo: ")
diretorio_do_arquivo = os.path.split(nome_do_arquivo)[0]

# Encerra a aplicação caso o arquivo não seja encontrado.
if not os.path.exists(nome_do_arquivo):
    input("ERRO: Não foi possível encontrar o arquivo.")
    sys.exit(1)

# Obtém a relação do arquivo.
try: relacao = carregar_relacao(nome_do_arquivo, "UTF-8")

# Encerra a aplicação caso haja um erro durante a conversão.
except JSONDecodeError:
    input("ERRO: Parece que o conteúdo do arquivo não está no formato correto.")
    sys.exit(1)

# Encerra a aplicação caso não haja nenhum par na relação.
if not relacao:
    input("A relação está vazia.")
    sys.exit(1)

# Encerra a aplicação caso os tipos do elementos X e Y sejam diferentes.
if not type(relacao[0][0]) is type(relacao[0][1]):
    input("ERRO: Os tipos dos elementos X e Y devem ser iguais.")
    sys.exit(1)

# Organiza a relação em ordem lexicográfica.
try: relacao = ordenar_relacao(relacao)

# Encerra a aplicação caso haja um problema com os pares da relação.
except TypeError as error:
    input("ERRO: {}.".format(error))
    sys.exit(1)

# Se os elementos da relação forem numéricos, pergunta ao usuário se ele deseja verificar se a relação
# é uma relação de congruência. Se sim, solicita o módulo, que deve ser um valor numérico.
if not type(relacao[0][0]) is str and input("\nVerificar se é uma relação de congruência? (Y/N): ").upper().startswith("Y"):
    modulo = float(input("Módulo: "))
else: modulo = None

# Obtém todas as propriedades que a relação possui.
propriedades = obter_propriedades(relacao, modulo)

print("\nPropriedades da Relação:\n" + "-" * 70)

# Mostra todas as propriedades que a relação possui ou não possui.
for nome_da_propriedade, info in propriedades.items():
    mostrar_propriedade(nome_da_propriedade, info[0], info[1])

print("-" * 70)

# Verifica se é possível gerar o diagrama de Hasse da relacao. Se sim,
# pergunta ao usuário se ele quer gerar o diagrama.
if propriedades[ANTI_SIMETRICA][0] and propriedades[REFLEXIVA][0] and propriedades[TRANSITIVA][0]:
    if input("\nGerar Diagrama de Hasse da relação? (Y/N): ").upper().startswith("Y"):
        gerar_diagrama(
            os.path.join(diretorio_do_arquivo, "Diagrama de Hasse.png"),
            relacao, comprimento_de_linha = 300, raio_do_ponto = 5
        )

# Verifica se é possível gerar uma classe de equivalência. Se sim,
# pergunta ao usuário se ele quer gerar uma classe de equivalência.
if propriedades[SIMETRICA][0] and propriedades[REFLEXIVA][0] and propriedades[TRANSITIVA][0]:
    if input("\nGerar classe de equivalência da relação? (Y/N): ").upper().startswith("Y"):
        elemento = input("Classe de equivalência: ")

        conjunto = obter_classe_de_equivalencia(relacao, elemento if type(relacao[0][0]) is str else float(elemento))
        salvar_conjunto(conjunto, os.path.join(diretorio_do_arquivo, "Classe de Equivalência {}.txt".format(elemento)))

# Pergunta ao usuário se o mesmo quer que a relação ordenada seja gerada em um arquivo.
if input("\nGerar relação em ordem lexicográfica? (Y/N): ").upper().startswith("Y"):
    salvar_relacao(relacao, os.path.join(diretorio_do_arquivo, "Relação Ordenada.txt"), "UTF-8")

# Pergunta ao usuário se o mesmo quer que a relação em forma matricial seja gerada em um arquivo.
if input("\nGerar relação em forma matricial? (Y/N): ").upper().startswith("Y"):
    matricial = relacao_para_matricial(relacao)

    with open(os.path.join(diretorio_do_arquivo, "Relação Matricial.txt"), "w", encoding = "UTF-8") as file:
        file.write(matricial)
# Pergunta ao usuário se o mesmo quer que a relação ordenada seja gerada em um arquivo.
if verificar_permutabilidade(relacao) and input("\nGerar relação em forma cíclica? (Y/N): ").upper().startswith("Y"):
    ciclica = relacao_para_ciclica(relacao)
    salvar_relacao_ciclica(ciclica, os.path.join(diretorio_do_arquivo, "Relação Cíclica.txt"), "UTF-8")
