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


   