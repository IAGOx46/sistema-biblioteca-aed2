from biblioteca.livro import Livro
from biblioteca.node import Node


class ArvoreAVL:
    def __init__(self):
        self.raiz = None

  
    def altura(self, node):
        
        return node.altura if node else 0

    def fator_balanceamento(self, node):
        
        return self.altura(node.esquerda) - self.altura(node.direita) if node else 0

  

    def rotacao_direita(self, y):
        x = y.esquerda
        T2 = x.direita

        
        x.direita = y
        y.esquerda = T2

        
        y.altura = 1 + max(self.altura(y.esquerda), self.altura(y.direita))
        x.altura = 1 + max(self.altura(x.esquerda), self.altura(x.direita))

        
        return x

    def rotacao_esquerda(self, x):
        y = x.direita
        T2 = y.esquerda

        
        y.esquerda = x
        x.direita = T2

        
        x.altura = 1 + max(self.altura(x.esquerda), self.altura(x.direita))
        y.altura = 1 + max(self.altura(y.esquerda), self.altura(y.direita))

  
        return y

 
    def inserir(self, livro):
        
        self.raiz = self._inserir_recurs(livro, self.raiz)

    def _inserir_recurs(self, livro, node):
        
        if node is None:
            return Node(livro)

        if livro < node.livro:
            node.esquerda = self._inserir_recurs(livro, node.esquerda)
        elif livro > node.livro:
            node.direita = self._inserir_recurs(livro, node.direita)
        else:
            return node  

        
        node.altura = 1 + max(self.altura(node.esquerda), self.altura(node.direita))

        balanceamento = self.fator_balanceamento(node)


        if balanceamento > 1 and livro < node.esquerda.livro:
            return self.rotacao_direita(node)

      
        if balanceamento < -1 and livro > node.direita.livro:
            return self.rotacao_esquerda(node)

        
        if balanceamento > 1 and livro > node.esquerda.livro:
            node.esquerda = self.rotacao_esquerda(node.esquerda)
            return self.rotacao_direita(node)

        
        if balanceamento < -1 and livro < node.direita.livro:
            node.direita = self.rotacao_direita(node.direita)
            return self.rotacao_esquerda(node)

        return node

#Emelly

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
