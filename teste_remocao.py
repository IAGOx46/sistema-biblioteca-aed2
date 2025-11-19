from biblioteca.arvore_avl import ArvoreAVL
from biblioteca.livro import Livro

def print_tree(node, level=0):
    if not node:
        return
    print_tree(node.direita, level + 1)
    print("    " * level + f"- {node.livro.id}")
    print_tree(node.esquerda, level + 1)


arvore = ArvoreAVL()

# Inserção
arvore.inserir(Livro(1, "A", "Autor", 2000))
arvore.inserir(Livro(2, "B", "Autor", 2000))
arvore.inserir(Livro(3, "C", "Autor", 2000))
arvore.inserir(Livro(4, "D", "Autor", 2000))
arvore.inserir(Livro(5, "E", "Autor", 2000))

print("\nÁrvore antes das remoções:")
print_tree(arvore.raiz)

# Remoções
print("\nRemovendo E (id=5):")
arvore.remove(Livro(5, "E", "Autor", 2000))
print_tree(arvore.raiz)

print("\nRemovendo D (id=4):")
arvore.remove(Livro(4, "D", "Autor", 2000))
print_tree(arvore.raiz)

print("\nRemovendo B (id=2):")
arvore.remove(Livro(2, "B", "Autor", 2000))
print_tree(arvore.raiz)

print("\nÁrvore final:")
print_tree(arvore.raiz)

#impressão e visualização da arvore

arvore.imprimir_in_order()
arvore.imprimir_pre_order()
arvore.imprimir_pos_order()
arvore.imprimir_livros_por_id()
arvore.visualizar()