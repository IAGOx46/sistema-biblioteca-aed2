from biblioteca.livro import Livro
from biblioteca.node import Node
import time

class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    #Retorna a altura do nó informado
    def altura(self, node):
        
        return node.altura if node else 0
    #Calcula o Fator de balanciamento
    def fator_balanceamento(self, node):
        
        return self.altura(node.esquerda) - self.altura(node.direita) if node else 0

  
    #Realiza rotação direita
    def rotacao_direita(self, y):
        x = y.esquerda
        T2 = x.direita

        
        x.direita = y
        y.esquerda = T2

        
        y.altura = 1 + max(self.altura(y.esquerda), self.altura(y.direita))
        x.altura = 1 + max(self.altura(x.esquerda), self.altura(x.direita))

        
        return x
    #Realiza rotação esquerda
    def rotacao_esquerda(self, x):
        y = x.direita
        T2 = y.esquerda
        
        y.esquerda = x
        x.direita = T2
        
        x.altura = 1 + max(self.altura(x.esquerda), self.altura(x.direita))
        y.altura = 1 + max(self.altura(y.esquerda), self.altura(y.direita))
  
        return y

    #Método que insere um livro na AVL atualizando a raiz.
    def inserir(self, livro):
        self.raiz, sucesso = self._inserir_recurs(self.raiz, livro)
        return sucesso

    #Insere recursivamente um novo nó
    def _inserir_recurs(self, node, livro):
        if node is None:
            return Node(livro), True  # inserido com sucesso

    # Comparação
        if livro < node.livro:
            node.esquerda, sucesso = self._inserir_recurs(node.esquerda, livro)

        elif livro > node.livro:
            node.direita, sucesso = self._inserir_recurs(node.direita, livro)

        else:
            return node, False  # ID duplicado

    # Atualiza altura
        node.altura = 1 + max(self.altura(node.esquerda), self.altura(node.direita))

    # Calcula o balanceamento
        balanceamento = self.fator_balanceamento(node)

    # Casos de rotação
    # LL
        if balanceamento > 1 and livro < node.esquerda.livro:
            return self.rotacao_direita(node), sucesso

    # RR
        if balanceamento < -1 and livro > node.direita.livro:
            return self.rotacao_esquerda(node), sucesso

    # LR
        if balanceamento > 1 and livro > node.esquerda.livro:
            node.esquerda = self.rotacao_esquerda(node.esquerda)
            return self.rotacao_direita(node), sucesso

    # RL
        if balanceamento < -1 and livro < node.direita.livro:
            node.direita = self.rotacao_direita(node.direita)
            return self.rotacao_esquerda(node), sucesso

        return node, sucesso

    #Remoção

    def remove(self, livro):
        self.raiz = self._remover_recurs(self.raiz, livro)


    def _remover_recurs(self, node, livro):
        if not node:
            return node

        if livro < node.livro:
            node.esquerda = self._remover_recurs(node.esquerda, livro)

        elif livro > node.livro:
            node.direita = self._remover_recurs(node.direita, livro)

        else:
            # Caso 1 e 2: nó com 0 ou 1 filho
            if not node.esquerda:
                return node.direita

            elif not node.direita:
                return node.esquerda

            # Caso 3: nó com dois filhos -> usar sucessor
            sucessor = self.minValueNode(node.direita)
            node.livro = sucessor.livro
            node.direita = self._remover_recurs(node.direita, sucessor.livro)

        # Atualiza altura
        node.altura = 1 + max(self.altura(node.esquerda), self.altura(node.direita))

        # Rebalanceamento AVL
        balanceamento = self.fator_balanceamento(node)

        # Rotação LL
        if balanceamento > 1 and self.fator_balanceamento(node.esquerda) >= 0:
            return self.rotacao_direita(node)

        # Rotação LR
        if balanceamento > 1 and self.fator_balanceamento(node.esquerda) < 0:
            node.esquerda = self.rotacao_esquerda(node.esquerda)
            return self.rotacao_direita(node)

        # Rotação RR
        if balanceamento < -1 and self.fator_balanceamento(node.direita) <= 0:
            return self.rotacao_esquerda(node)

        # Rotação RL
        if balanceamento < -1 and self.fator_balanceamento(node.direita) > 0:
            node.direita = self.rotacao_direita(node.direita)
            return self.rotacao_esquerda(node)

        return node


    def minValueNode(self, node):
        atual = node
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual
    
    
    #Métodos de impressão e Buca

    def imprimir_in_order(self):
        print("\n--- Impressão In-Order (ordenada por ID) ---")
        self._in_order(self.raiz)

    def _in_order(self, node):
        if node:
            self._in_order(node.esquerda)
            print(f"ID: {node.livro.id} | Título: {node.livro.titulo}")
            self._in_order(node.direita)

    def imprimir_pre_order(self):
        print("\n--- Impressão Pré-Order ---")
        self._pre_order(self.raiz)

    def _pre_order(self, node):
        if node:
            print(f"ID: {node.livro.id} | Título: {node.livro.titulo}")
            self._pre_order(node.esquerda)
            self._pre_order(node.direita)

    def imprimir_pos_order(self):
        print("\n--- Impressão Pós-Order ---")
        self._pos_order(self.raiz)

    def _pos_order(self, node):
        if node:
            self._pos_order(node.esquerda)
            self._pos_order(node.direita)
            print(f"ID: {node.livro.id} | Título: {node.livro.titulo}")

   #Busca
    def busca(self, livro):
        return self._busca_recursiva(self.raiz, livro)

    def _busca_recursiva(self, node, livro):
        if node is None:
            return None

        if livro.id == node.livro.id:
            return node.livro

        elif livro.id < node.livro.id:
            return self._busca_recursiva(node.esquerda, livro)

        else:
            return self._busca_recursiva(node.direita, livro)
        
    def buscar_por_titulo(self, titulo, parcial=True):
    
        termo = (titulo or "").strip().lower()
        resultados = []

        if termo == "":
            return resultados
    
        self._buscar_por_titulo_rec(self.raiz, termo, resultados, parcial)
        return resultados

    def _buscar_por_titulo_rec(self, node, termo, resultados, parcial):
        if node is None:
            return
        titulo_node = (getattr(node.livro, "titulo", "") or "").lower()
        if parcial:
            if termo in titulo_node:
                resultados.append(node.livro)
        else:
            if termo == titulo_node:
                resultados.append(node.livro)
            
        self._buscar_por_titulo_rec(node.esquerda, termo, resultados, parcial)
        self._buscar_por_titulo_rec(node.direita, termo, resultados, parcial)


    def busca_com_tempo(self, livro):
        inicio = time.perf_counter()
        resultado = self.busca(livro)
        fim = time.perf_counter()
        return resultado, (fim - inicio) * 1000



    def buscar_por_titulo_com_tempo(self, titulo, parcial=True):
        inicio = time.perf_counter()
        resultados = self.buscar_por_titulo(titulo, parcial=parcial)
        fim = time.perf_counter()
        tempo_ms = (fim - inicio) * 1000
        return resultados, tempo_ms

