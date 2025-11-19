class VisualizacaoAVL:    
    # impremssão in-order (ordenado)
    
    def imprimir_in_order(self, node):
        if node:
            self.imprimir_in_order(node.esquerda)
            print(f"ID: {node.livro.id} – {node.livro.titulo}")
            self.imprimir_in_order(node.direita)

    
    # impressão pre-order 
    
    def imprimir_pre_order(self, node):
        if node:
            print(f"ID: {node.livro.id} – {node.livro.titulo}")
            self.imprimir_pre_order(node.esquerda)
            self.imprimir_pre_order(node.direita)

    
    # impressão post-order 
    
    def imprimir_post_order(self, node):
        if node:
            self.imprimir_post_order(node.esquerda)
            self.imprimir_post_order(node.direita)
            print(f"ID: {node.livro.id} – {node.livro.titulo}")

    # visualização da AVL
    def visualizar_arvore(self, node, nivel=0, lado="ROOT"):
        if node:
            # imprime primeiro a subárvore da direita
            self.visualizar_arvore(node.direita, nivel + 1, "R")

            # cria o espaçamento proporcional ao nível
            espaco = "     " * nivel
            print(f"{espaco}[{lado}] ID: {node.livro.id}")

            # imprime a subárvore da esquerda
            self.visualizar_arvore(node.esquerda, nivel + 1, "L")
