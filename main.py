# ---------------------------------------------------
# Analisador lexico da linguagem D
# Programa principal: imprime a sequencia de tokens de um arquivo fonte
#
# uso: python3 main.py [arquivo.d]
# ---------------------------------------------------
import os        # usado para verificar se o arquivo existe
import sys       # argumentos da linha de comando e encerramento do programa

from ttoken import TOKEN
from lexico import Lexico


# detectaCodificacao: descobre como os bytes do arquivo devem ser lidos
def detectaCodificacao(caminho):
    # o fonte pode estar em utf-8 ou latin-1; latin-1 aceita qualquer byte
    # e serve de ultimo recurso
    with open(caminho, 'rb') as arq:
        dados = arq.read()
    try:
        dados.decode('utf-8')
        return 'utf-8'
    except UnicodeDecodeError:
        return 'latin-1'


# abreFonte: abre o arquivo; se nao conseguir, mostra o motivo e encerra
def abreFonte(caminho):
    try:
        codificacao = detectaCodificacao(caminho)
        return open(caminho, 'r', encoding=codificacao)
    except OSError as erro:
        print(f'erro: nao foi possivel abrir "{caminho}": {erro.strerror}')
        sys.exit(1)


# so executa quando este arquivo e rodado diretamente
if __name__ == '__main__':
    # sys.argv[0] e o main.py; sys.argv[1] e o arquivo informado, se houver
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
    else:
        # sem argumento, usa o fonte de demonstracao, se estiver presente
        caminho = 'testes/exemplo.d'
        if not os.path.exists(caminho):
            print('uso: python3 main.py <arquivo.d>')
            sys.exit(1)

    # o lexico le o fonte inteiro no construtor, entao o arquivo pode ser fechado
    arqfonte = abreFonte(caminho)
    lexico = Lexico(arqfonte)
    arqfonte.close()

    # pede um token por vez e imprime, ate chegar ao fim do arquivo
    tokenLido = lexico.getToken()
    while tokenLido[0] != TOKEN.eof:
        lexico.imprimeToken(tokenLido)
        tokenLido = lexico.getToken()
    # imprime tambem o proprio <eof>
    lexico.imprimeToken(tokenLido)
