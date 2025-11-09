from biblioteca.livro import Livro
from biblioteca.arvore_avl import ArvoreAVL

def main():
    arvore = ArvoreAVL()

    while True:
        print("\n=== SISTEMA DE BIBLIOTECA (AVL) ===")
        
        teste = input("Digite 1 para inserir: ")

        if teste == "1":
            id = int(input("ID do livro: "))
            titulo = input("Título: ")
            autor = input("Autor: ")
            ano = input("Ano: ")

            livro = Livro(id, titulo, autor, ano)
            arvore.inserir(livro)
            print("Livro inserido com sucesso!")



if __name__ == "__main__":
    main()
