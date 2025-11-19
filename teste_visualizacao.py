from biblioteca.arvore_avl import ArvoreAVL
from biblioteca.livro import Livro

def print_tree(node, level=0):
    if not node:
        return
    print_tree(node.direita, level + 1)
    print("    " * level + f"- {node.livro.id}")
    print_tree(node.esquerda, level + 1)


arvore = ArvoreAVL()
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

def imprimir_livros_por_id(self):
        print("\n--- Livros ordenados pelo ID ---")
        self.imprimir_in_order()

    #visualização
def visualizar(self):
        print("\n--- Visualização da Árvore AVL ---")
        self._print_tree(self.raiz, 0)

def _print_tree(self, node, nivel):
        if node is not None:
            self._print_tree(node.direita, nivel + 1)
            print("    " * nivel + f"→ (ID {node.livro.id})")
            self._print_tree(node.esquerda, nivel + 1)
