# Sobre:
Este é um projeto para a disciplina Programação Orientada a Objetos (MATA-55) — um jogo de Xadrez, com modo local e online, criado em Python 3 puro, 
utilizando a biblioteca [pyglet](https://pyglet.org/), por recomendação do professor.

## Preparando o ambiente:
Para executar o jogo, é necessário ter instalado o Python 3.9, ou superior.<br><br> 
Instale as suas dependências utilizando o comando abaixo:
```
pip install -r requirements.txt
```
# Features:

## Controles:
Para jogar, você pode utilizar o mouse, selecionando e movendo uma peça, clicando com o **Botão Esquerdo**. Também é possível jogar com o teclado, 
utilizando o [sistema de notação algébrica de xadrez](https://pt.wikipedia.org/wiki/Nota%C3%A7%C3%A3o_alg%C3%A9brica_de_xadrez). Para tal, escolha 
primeiramente a coluna e, logo em seguida, a linha da peça a ser movida. Faça o mesmo para a seleção do destino. Após isso, aperte ENTER ou SPACE
para finalizar o movimento.

Outras teclas úteis são: **F12** para capturas de tela e **ESC** para voltar ao menu.

*Observação: a captura de tela será salva no diretório `data/screenshots`.* 

## Modo Online:
Para jogar online, abra a tela de configurações e altere, se necessário, o seu endereço IP e o número PORT.<br><br> 
É necessário que um dos jogadores seja o host da partida. Supondo que você seja o host, envie o seu endereço IP e número PORT ao outro jogador. Após 
isso, clique no botão "Play as Host". Posteriormente, o outro jogador deverá clicar no botão "Play as Client". Dessa forma, a conexão estará estabelecida e a partida iniciará automaticamente.

**Temática de Derrota:** Ao ser derrotado em uma partida online, o tema do jogo muda, voltando ao normal somente depois que conseguir uma vitória, no modo local ou online

## Modo Replay:
Todas as partidas, modo local ou online, são salvas automaticamente após o término do jogo, isto é: se não houver abandono durante o jogo. Para conferir 
o replay de uma partida, acesse a tela de histórico e navegue pela lista, buscando o jogo que deseja. Após isso, inicie o replay.

Através do controlador, localizado abaixo do placar do jogo, você poderá retroceder, avançar, pausar ou prosseguir com o jogo. No modo replay, não é possível
alterar as jogadas dinamicamente.

## Conquistas e Easter Eggs:
O jogo conta com um sistema de conquistas, no qual existem determinados eventos, espalhados pelo programa, que liberam conquistas para o jogador. Essas
conquistas podem ser visualizadas novamente na tela de conquistas. Além disso, o jogo também conta com Easter Eggs. Em outras palavras, boa caçada!!

## Título Informativo:
Preste atenção ao título da janela em determinadas telas. Elas podem conter informações úteis como, por exemplo: na tela de histórico, o título da janela
informa o índice do jogo em questão e quantos jogos foram registrados.

## Criptografia:
Com o objetivo de proteger a integridade do jogo, o tráfego dos dados, tal como o arquivo de configurações, é protegido utilizando o pacote 
[crpytography](https://pypi.org/project/cryptography/). Talvez essa não seja a melhor solução para a proteção de dados, mas é suficiente para proteger 
o jogo de cheats :)

## Configurações:
O jogo atualmente conta com algumas opções do configurações, descritas abaixo:
- Resolução de Tela
- Volume de Efeitos Sonoros
- Volume de Músicas
- Endereço IP e Número PORT

## Detecção de Xeque:
Quando o seu rei está em xeque, somente jogadas que o farão sair do xeque estarão liberadas.

## Riqueza no SFX:
Demos atenção ao detalhe de cada peça e ação durante o jogo possuir seu próprio efeito sonoro.

## Arquivo de Log:
Caso algum erro ocorra durante o jogo, o mesmo será salvo no arquivo `log.txt`. Nessa situação, por gentileza, nos encaminhe o arquivo para que possamos solucionar o problema e melhorar o jogo.
