from biblioteca.livro import Livro
from biblioteca.arvore_avl import ArvoreAVL

if __name__ == "__main__":
    arvore = ArvoreAVL()

    livro_exemplo = Livro("Dom Casmurro", "Machado de Assis", 1899)
    arvore.inserir(livro_exemplo)

    print("Sistema da biblioteca iniciado com sucesso!")
