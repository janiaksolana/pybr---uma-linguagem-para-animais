import sys
import re

class InterpretadorPyBr:
    def __init__(self):
        # Armazena as variáveis e seus valores na memória do interpretador
        self.variaveis = {}

    def avaliar_expressao(self, expr):
        """Avalia números, textos, variáveis ou operações matemáticas simples."""
        expr = expr.strip()
        
        if not expr:
            return ""

        # 1. Se for um texto entre aspas (Ex: "Olá" ou 'Mundo')
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
            
        # 2. Se for apenas um número inteiro
        if expr.isdigit():
            return int(expr)
            
        # 3. Se for uma variável já salva, retorna o valor dela
        if expr in self.variaveis:
            return self.variaveis[expr]
            
        # 4. Operações matemáticas simples ou concatenação de texto (Ex: pontos + 5)
        match = re.match(r"(\w+|\d+|'.*?'|\".*?\")\s*([\+\-\*\/])\s*(\w+|\d+|'.*?'|\".*?\")", expr)
        if match:
            esquerda, operador, direita = match.groups()
            val_esq = self.avaliar_expressao(esquerda)
            val_dir = self.avaliar_expressao(direita)
            
            # Se qualquer um dos lados for texto, o operador '+' junta (concatena) os dois
            if operador == '+': 
                if isinstance(val_esq, int) and isinstance(val_dir, int):
                    return val_esq + val_dir
                return str(val_esq) + str(val_dir)
            if operador == '-': return val_esq - val_dir
            if operador == '*': return val_esq * val_dir
            if operador == '/': return val_esq // val_dir # Divisão inteira
            
        raise SyntaxError(f"Não entendi o que significa: '{expr}'")

    def executar_linha(self, linha):
        """Interpreta e executa uma única linha de código PyBr."""
        linha = linha.strip()
        
        # Ignora linhas vazias ou comentários que começam com '#'
        if not linha or list(linha)[0] == '#':
            return

        # 1. Comando: mostre [expressão]
        if linha.startswith("mostre "):
            conteudo = linha[len("mostre "):]
            print(self.avaliar_expressao(conteudo))
            return

        # 2. Atribuição: [variavel] recebe [expressão]
        if " recebe " in linha:
            nome_var, expr = linha.split(" recebe ", 1)
            nome_var = nome_var.strip()
            
            if not nome_var.isidentifier():
                raise NameError(f"Nome de variável inválido: '{nome_var}'")
                
            self.variaveis[nome_var] = self.avaliar_expressao(expr)
            return

        # 3. Condicional: se [variavel] igual [valor] [comando]
        if linha.startswith("se "):
            # Padrão esperado: se pontos igual 10 mostre "Ganhou"
            match = re.match(r"se\s+(\w+)\s+igual\s+(\w+|\d+|'.*?'|\".*?\")\s+(.+)", linha)
            if match:
                nome_var, valor_esperado, comando_interno = match.groups()
                val_atual = self.variaveis.get(nome_var, None)
                val_esp = self.avaliar_expressao(valor_esperado)
                
                # Se a condição for verdadeira, executa o comando que está na frente
                if val_atual == val_esp:
                    self.executar_linha(comando_interno)
                return
            else:
                raise SyntaxError(f"Uso incorreto do 'se'. Use: se [var] igual [valor] [comando]")

        raise SyntaxError(f"Comando inválido ou não reconhecido: '{linha}'")

    def rodar(self, codigo_fonte):
        """Roda o programa completo, quebrando o texto linha por linha."""
        linhas = codigo_fonte.split("\n")
        for num_linha, linha in enumerate(linhas, 1):
            # Remove espaços extras ou quebras antes de checar se está vazia
            if not linha.strip():
                continue
            try:
                self.executar_linha(linha)
            except Exception as e:
                print(f"Erro na linha {num_linha}: {e}")
                break

# ---------------------------------------------------------------------
# PONTO DE ENTRADA DO INTERPRETADOR
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Caso você queira testar direto sem criar arquivos externos,
    # você pode digitar o código aqui dentro desta variável:
    codigo_teste = """
    # Meu primeiro programa em PyBr
    nome recebe "Gabriel"
    pontos recebe 10

    mostre "Jogador conectado: " + nome
    mostre "Pontuação atual: " + pontos

    se pontos igual 10 mostre "Parabéns! Você atingiu o nível máximo!"
    """

    # Se você passar um arquivo no terminal, ele roda o arquivo. 
    # Se rodar só 'python pybr.py', ele executa o código de teste acima.
    if len(sys.argv) > 1:
        nome_arquivo = sys.argv[1]
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                codigo_do_arquivo = f.read()
            
            interpretador = InterpretadorPyBr()
            interpretador.rodar(codigo_do_arquivo)
        except FileNotFoundError:
            print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
    else:
        # Modo de teste padrão
        interpretador = InterpretadorPyBr()
        interpretador.rodar(codigo_teste)
