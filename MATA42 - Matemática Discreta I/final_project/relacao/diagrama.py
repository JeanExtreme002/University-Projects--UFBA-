from PIL import Image, ImageDraw
import math

def criar_diagrama(relacao, comprimento_de_linha = 100):
    """
    Obtém uma relação parcialmente ordenada e cria o seu Diagrama de Hasse, retornando
    um dicionário com as posições dos seus pontos, uma lista com as coordenadas
    de todas as linhas do diagrama e o tamanho (largura, altura) do diagrama.
    """

    # Ordena a relação com base na quantidade de pares com um determinado X.
    relacao = ordenar_relacao(relacao)

    # Mantém na relação apenas os pares que não possuem conexão com outros pares.
    relacao = [(x, y) for x, y in relacao if not existe_conexao(relacao, x, y)]

    menor_pos_x, maior_pos_x = 0, 0
    menor_pos_y, maior_pos_y = 0, 0

    posicoes = dict()
    linhas = []
    atual_x = None
    roots = 0

    # Percorre todos os pares (x, y) da relação para criar as linhas do diagrama.
    for x, y in relacao:

        # Caso o laço de repetição esteja iterando pares com um X diferente, o ângulo
        # será resetado e uma nova razão para o ângulo será calculada.
        if atual_x != x:

            # Se o X não possuir uma raíz, a sua posição no diagrama
            # será a coordenada raíz (0, 0) com a posição X somada à um comprimento N.
            if not x in posicoes:
                posicoes[x] = [0 + comprimento_de_linha * math.ceil(roots / 2) * ((-1) ** roots), 0]
                roots += 1

                menor_pos_x = min([posicoes[x][0], menor_pos_x])
                maior_pos_x = max([posicoes[x][0], maior_pos_x])
                menor_pos_y = min([posicoes[x][1], menor_pos_y])
                maior_pos_y = max([posicoes[x][1], maior_pos_y])

            # Define o X e a posição atual no diagrama.
            atual_x, posicao_atual = x, posicoes[x]

            # Calcula a razão do ângulo e reseta o ângulo atual.
            razao_do_angulo = 180 / obter_total_de_pares(relacao, x)
            angulo, contador = 90, 0

        # Se o Y não tiver uma posição registrada, sua posição será calculada.
        if not y in posicoes:

            # Calcula um novo ângulo para a sua posição.
            angulo += razao_do_angulo * contador * (1 if contador % 2 == 0 else -1)
            contador += 1

            # Calcula a coordenada do Y, com base na coordenada atual.
            posicoes[y] = obter_coordenada(*posicao_atual, angulo, comprimento_de_linha)

            menor_pos_x = min([posicoes[y][0], menor_pos_x])
            maior_pos_x = max([posicoes[y][0], maior_pos_x])
            menor_pos_y = min([posicoes[y][1], menor_pos_y])
            maior_pos_y = max([posicoes[y][1], maior_pos_y])

        # Adiciona à lista a linha, no formato [x1, y1, x2, y2].
        linhas.append([*posicao_atual, *posicoes[y]])

    # Move o diagrama para que o menor XY seja zero.
    for linha in linhas:
        linha[0] += abs(menor_pos_x)
        linha[2] += abs(menor_pos_x)
        linha[1] += abs(menor_pos_y)
        linha[3] += abs(menor_pos_y)

    for value in posicoes:
        posicoes[value][0] += abs(menor_pos_x)
        posicoes[value][1] += abs(menor_pos_y)

    # Retorna os pontos e linhas do diagrama, e seu tamanho.
    return posicoes, linhas, [math.ceil(maior_pos_x - menor_pos_x), math.ceil(maior_pos_y - menor_pos_y)]

def existe_conexao(relacao, x, y, atual_x = None):
    """
    Verifica se a relação possui algum par, com um determinado Y,
    que faça uma conexão com o par inicial.

    Exemplo: Dado a relação [(1,1), (1,2), (1,5), (1,6), (2,2), (2,6)],
    pela transitividade, existe uma conexão para o par (1,6), pois os
    pares (1,2) e (2,6) existem na relação. O mesmo não pode ser dito
    para o par (1,5).
    """
    if atual_x is None: atual_x = x
    if atual_x == y: return False

    for par in relacao:
        if par[0] != atual_x or par[0] == par[1]: continue
        if atual_x != x and par[1] == y: return True
        if existe_conexao(relacao, x, y, par[1]): return True
    return False

def gerar_diagrama(nome_do_arquivo, relacao, comprimento_de_linha = 100, raio_do_ponto = 5, cores = [(255, 255, 255), (0, 0, 0)], texto = True):
    """
    Cria o Diagrama de Hasse de uma relação e o salva em um arquivo de imagem.
    """

    # Espaçamento da borda imagem e distância entre um ponto e seu texto.
    espaco, distancia_de_texto = 10, 10

    # Obtém todos os pontos e linhas do diagrama.
    pontos, linhas, tamanho = criar_diagrama(relacao, comprimento_de_linha = comprimento_de_linha)

    # Cria uma nova imagem RGB, e um canvas para desenhar na imagem.
    imagem = Image.new("RGB", [v + raio_do_ponto * 2 + espaco * 2 for v in tamanho], cores[0])
    canvas = ImageDraw.Draw(imagem)

    # Desenha todas as linhas do diagrama.
    for linha in linhas:
        linha = [v + raio_do_ponto + espaco for v in linha]
        canvas.line(linha, fill = cores[1])

    # Desenha todos os pontos do diagrama.
    for valor, coord in pontos.items():
        coord = [v + raio_do_ponto + espaco for v in coord]
        valor = str(valor)

        # Se a opção de texto estiver habilitada, o valor de cada ponto será desenhado na imagem.
        if texto:

            # Obtém o tamanho do texto e o tamanho da imagem.
            tamanho_de_texto = canvas.textsize(valor)
            largura, altura = imagem.size

            # Verifica se a largura da imagem será maior, caso o texto seja desenhado.
            if tamanho_de_texto[0] + coord[0] + raio_do_ponto + distancia_de_texto > largura:
                largura = math.ceil(tamanho_de_texto[0] + coord[0] + raio_do_ponto + distancia_de_texto)

            # Se o texto ultrapassar a imagem, o tamanho da imagem será aumentada.
            if imagem.size[0] != largura:

                # Cria uma nova imagem, com um tamanho maior, copiando o conteúdo da imagem atual.
                nova_imagem = Image.new("RGB", (largura + espaco, altura), cores[0])
                nova_imagem.paste(imagem)

                # Substitui a imagem atual pela nova imagem.
                imagem = nova_imagem
                canvas = ImageDraw.Draw(imagem)

            # Desenha o texto na imagem.
            canvas.text([coord[0] + raio_do_ponto + distancia_de_texto, coord[1]], valor, fill = cores[1])

        # Desenha o ponto na imagem.
        canvas.ellipse(
            (
                coord[0] - raio_do_ponto,
                coord[1] - raio_do_ponto,
                coord[0] + raio_do_ponto,
                coord[1] + raio_do_ponto
            ),
            fill = cores[1]
        )

    # Salva a imagem.
    imagem.save(nome_do_arquivo)

def obter_coordenada(x1, y1, angulo, distancia):
    """
    Obtém um coordenada inicial (x, y) e retorna uma
    nova coordenada, dado um ângulo e uma distância.
    """
    y2 = distancia * math.sin(math.radians(angulo))
    x2 = distancia * math.sin(math.radians(90 - angulo))
    return [x1 + x2, y1 - y2]

def obter_total_de_pares(relacao, x):
    """
    Retorna a quantidade de pares que a relação possui
    com um determinado X.
    """
    contador = 0

    for par in relacao:
        if par[0] == x: contador += 1
    return contador

def ordenar_relacao(relacao):
    """
    Obtém uma relação e a ordena com base na quantidade
    de pares com um determinado X.
    """
    relacao_original = relacao.copy()
    relacao = relacao.copy()

    relacao_ordenada = []
    total_de_pares = {}

    for i in range(len(relacao)):
        maior, par_maior = 0, (0, 0)

        for par in relacao:
            # Se o total de pares para um determinado X não tiver sido obtido,
            # ele será calculado e registrado no dicionário.
            if not par[0] in total_de_pares:
                total_de_pares[par[0]] = obter_total_de_pares(relacao_original, par[0])

            # Verifica se a quantidade é maior e registra o par.
            if total_de_pares[par[0]] > maior:
                maior = total_de_pares[par[0]]
                par_maior = par

        # Adiciona o par à lista e o remove da relação.
        relacao_ordenada.append(par_maior)
        relacao.remove(par_maior)
    return relacao_ordenada
