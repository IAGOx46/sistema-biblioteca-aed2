import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import platform

from biblioteca.arvore_avl import ArvoreAVL
from biblioteca.livro import Livro


BG = "#FFFFFF"
SURFACE = "#FAFAFC"
PANEL = "#E3F2FD"        
PRIMARY = "#1E88E5"      
PRIMARY_DARK = "#1565C0"
ACCENT = "#7E57C2"       
GREEN = "#43A047"
TEXT = "#0F1724"
MUTED = "#6B7280"
CANVAS_BG_TOP = "#F3F8FF"
CANVAS_BG_BOTTOM = "#FFFFFF"
BUTTON_FG = "#FFFFFF"
ENTRY_BG = "#FFFFFF"
ENTRY_BORDER = "#E3F2FD"

IS_MAC = platform.system() == "Darwin"



def material_button(master, text, cmd, bg=PRIMARY, fg=BUTTON_FG, pady=8, padx=12):
    btn = tk.Frame(master, bg=bg, bd=0)
    label = tk.Label(btn, text=text, bg=bg, fg=fg, font=("Segoe UI", 10, "bold"), cursor="hand2")
    label.pack(padx=padx, pady=pady)

    label.bind("<Button-1>", lambda e: cmd())

    def on_enter(e):
        btn.config(bg=PRIMARY_DARK)
        label.config(bg=PRIMARY_DARK)

    def on_leave(e):
        btn.config(bg=bg)
        label.config(bg=bg)

    label.bind("<Enter>", on_enter)
    label.bind("<Leave>", on_leave)
    return btn


class RoundedEntry(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, bg=ENTRY_BORDER)
        self.inner = tk.Frame(self, bg=ENTRY_BG)
        self.inner.pack(padx=2, pady=2, fill="x")
        self.entry = ttk.Entry(self.inner, style="Material.TEntry", **kw)
        self.entry.pack(fill="x", padx=6, pady=6)

    def get(self):
        return self.entry.get()

    def insert(self, idx, s):
        return self.entry.insert(idx, s)

    def delete(self, a, b=None):
        return self.entry.delete(a, b)




def aplicar_estilos(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure("Material.TEntry",
                    relief="flat",
                    padding=4,
                    foreground=TEXT,
                    fieldbackground=ENTRY_BG,
                    bordercolor=ENTRY_BORDER)

    style.configure("Material.Vertical.TScrollbar",
                    troughcolor=CANVAS_BG_TOP,
                    background=PRIMARY,
                    arrowcolor=TEXT)

    style.configure("Material.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10))




class ArvoreDesenho:
    def __init__(self, canvas):
        self.canvas = canvas

    def _draw_gradient_bg(self):
        self.canvas.delete("__gradient__")
        w = max(self.canvas.winfo_width(), 800)
        h = max(self.canvas.winfo_height(), 600)
        steps = 20
        for i in range(steps):
            y0 = i * (h / steps)
            y1 = (i + 1) * (h / steps)
            ratio = i / (steps - 1)
            color = self._interp_color(CANVAS_BG_TOP, CANVAS_BG_BOTTOM, ratio)
            self.canvas.create_rectangle(0, y0, w, y1, fill=color, outline="", tags="__gradient__")

    def _interp_color(self, c1, c2, t):
        def hex_to_rgb(h):
            h = h.lstrip("#")
            return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb):
            return "#%02x%02x%02x" % rgb

        r1, g1, b1 = hex_to_rgb(c1)
        r2, g2, b2 = hex_to_rgb(c2)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return rgb_to_hex((r, g, b))

    def desenhar(self, raiz):
        self.canvas.delete("all")
        self._draw_gradient_bg()
        if raiz:
            w = max(self.canvas.winfo_width(), 800)
            self._desenhar_no(raiz, w // 2, 60, max(w // 6, 140))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _desenhar_no(self, no, x, y, deslocamento):
        if no is None:
            return

        if getattr(no, "esquerda", None):
            self.canvas.create_line(x, y, x - deslocamento, y + 100, width=2, fill="#D1E9FF")
        if getattr(no, "direita", None):
            self.canvas.create_line(x, y, x + deslocamento, y + 100, width=2, fill="#D1E9FF")

        self.canvas.create_oval(x - 30 + 3, y - 30 + 3, x + 30 + 3, y + 30 + 3,
                                fill="#E8F4FF", outline="", tags="shadow")

        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30,
                                fill=PRIMARY, outline="", width=0)

        self.canvas.create_text(x, y, text=str(no.livro.id),
                                fill=BUTTON_FG, font=("Segoe UI", 11, "bold"))

        titulo = getattr(no.livro, "titulo", "")
        if titulo:
            short = (titulo[:20] + "...") if len(titulo) > 20 else titulo
            self.canvas.create_text(x, y + 40, text=short,
                                    fill=MUTED, font=("Segoe UI", 8))

        if getattr(no, "esquerda", None):
            self._desenhar_no(no.esquerda, x - deslocamento, y + 100, deslocamento // 2)
        if getattr(no, "direita", None):
            self._desenhar_no(no.direita, x + deslocamento, y + 100, deslocamento // 2)




class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteca AVL — Material Blue")
        self.root.geometry("1250x720")
        self.root.minsize(1000, 600)
        self.root.configure(bg=BG)

        aplicar_estilos(root)
        self.arvore = ArvoreAVL()

        
        shadow = tk.Frame(root, bg="#E3F2FD")
        shadow.place(x=16, y=14, width=420, height=692)        

        left_card = tk.Frame(root, bg=SURFACE, bd=0)
        left_card.place(x=12, y=10, width=420, height=692)     

        header = tk.Frame(left_card, bg=PRIMARY)
        header.pack(fill="x")
        tk.Label(header, text="  Biblioteca", bg=PRIMARY, fg=BUTTON_FG,
                 font=("Segoe UI", 14, "bold")).pack(padx=12, pady=12)

        tk.Frame(left_card, bg="#E6EEF9", height=1).pack(fill="x")

        
        area = tk.Frame(left_card, bg=SURFACE)
        area.pack(fill="both", expand=True)

        canvas_scroll = tk.Canvas(area, bg=SURFACE, highlightthickness=0)
        canvas_scroll.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)

        vscroll = ttk.Scrollbar(area, orient="vertical",
                                command=canvas_scroll.yview,
                                style="Material.Vertical.TScrollbar")
        vscroll.pack(side="right", fill="y", padx=(0, 8), pady=8)

        canvas_scroll.configure(yscrollcommand=vscroll.set)

        content = tk.Frame(canvas_scroll, bg=SURFACE)
        content_id = canvas_scroll.create_window((0, 0), window=content, anchor="nw")

        def on_content_config(event):
            canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
            canvas_scroll.itemconfig(content_id, width=canvas_scroll.winfo_width())

        content.bind("<Configure>", on_content_config)

        def on_canvas_config(event):
            canvas_scroll.itemconfig(content_id, width=event.width)

        canvas_scroll.bind("<Configure>", on_canvas_config)

        if IS_MAC:
            canvas_scroll.bind_all("<MouseWheel>", lambda ev: canvas_scroll.yview_scroll(int(-1 * ev.delta), "units"))
        else:
            canvas_scroll.bind_all("<MouseWheel>", lambda ev: canvas_scroll.yview_scroll(int(-1 * (ev.delta / 120)), "units"))

        
        tk.Label(content, text="Cadastro de Livros", bg=SURFACE, fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(6, 2))

        def mk_entry(label_text):
            tk.Label(content, text=label_text, bg=SURFACE, fg=MUTED,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12, pady=(8, 2))
            r = RoundedEntry(content)
            r.pack(fill="x", padx=12)
            return r

        self.entry_id = mk_entry("ID:")
        self.entry_titulo = mk_entry("Título:")
        self.entry_autor = mk_entry("Autor:")
        self.entry_ano = mk_entry("Ano:")

        
        tk.Label(content, text="Operações", bg=SURFACE, fg=PRIMARY_DARK,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12, 6))

        buttons = [
            ("Inserir Livro", self.inserir),
            ("Emprestar Livro", self.remover),
            ("Buscar Livro", self.buscar),
            ("In-Order", self.listar_in_order),
            ("Pré-Order", self.listar_pre),
            ("Pós-Order", self.listar_pos),
            ("Atualizar", self.atualizar_desenho),
            ("Carregar Dados", self.carregar_json)
        ]

        for (lab, cmd) in buttons:
            b = material_button(content, lab, cmd)
            b.pack(fill="x", padx=14, pady=8)

        self.info = tk.Label(content, text="Livros: 0", bg=SURFACE, fg=MUTED,
                             anchor="w", font=("Segoe UI", 9))
        self.info.pack(fill="x", padx=14, pady=(8, 18))

        
        right_card = tk.Frame(root, bg=BG)
        right_card.place(x=442, y=10, width=850, height=692)

        title_bar = tk.Frame(right_card, bg=CANVAS_BG_TOP)
        title_bar.pack(fill="x")
        tk.Label(title_bar, text="  Visualização da Árvore AVL", bg=CANVAS_BG_TOP,
                 fg=PRIMARY_DARK, font=("Segoe UI", 13, "bold")).pack(side="left", padx=8, pady=8)

        clear_btn = material_button(title_bar, "Limpar", self.limpar_arvore)
        clear_btn.pack(side="right", padx=8, pady=6)

        canvas_frame = tk.Frame(right_card, bg=CANVAS_BG_BOTTOM)
        canvas_frame.pack(fill="both", expand=True, padx=12, pady=12)

        self.canvas = tk.Canvas(canvas_frame, bg=CANVAS_BG_BOTTOM, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        xscroll = ttk.Scrollbar(canvas_frame, orient="horizontal",
                                command=self.canvas.xview,
                                style="Material.Vertical.TScrollbar")
        xscroll.pack(side="bottom", fill="x")

        yscroll = ttk.Scrollbar(canvas_frame, orient="vertical",
                                command=self.canvas.yview,
                                style="Material.Vertical.TScrollbar")
        yscroll.pack(side="right", fill="y")

        self.canvas.configure(xscrollcommand=xscroll.set,
                              yscrollcommand=yscroll.set,
                              scrollregion=(0, 0, 2000, 2000))

        self.desenho = ArvoreDesenho(self.canvas)

        self.status = tk.Label(root, text="Pronto", bg=BG, fg=MUTED,
                               anchor="w", font=("Segoe UI", 9))
        self.status.place(x=12, y=706, width=1226, height=26)

        self.atualizar_info()

    
    def carregar_json(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar arquivo",
            filetypes=[("JSON", "*.json"), ("Todos", "*.*")]
        )
        if not caminho:
            self._set_status("Operação cancelada")
            return

        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)

            if not isinstance(dados, list):
                messagebox.showerror("Erro", "O JSON precisa ser uma lista de objetos.")
                return

            loaded = 0
            for item in dados:
                id_ = item.get("id") or item.get("ID")
                titulo = item.get("titulo") or item.get("title") or ""
                autor = item.get("autor") or item.get("author") or ""
                ano = item.get("ano") or item.get("year") or ""

                try:
                    livro = Livro(int(id_), titulo, autor, ano)
                except Exception:
                    livro = Livro(id_, titulo, autor, ano)

                self.arvore.inserir(livro)
                loaded += 1

            self.atualizar_desenho()
            messagebox.showinfo("Sucesso", f"{loaded} itens carregados.")
            self._set_status("Carregamento concluído")
            self.atualizar_info()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar: {e}")

    def inserir(self):
        try:
            id_ = int(self.entry_id.entry.get().strip())
        except Exception:
            messagebox.showerror("Erro", "ID inválido.")
            self._set_status("Erro: ID inválido")
            return

        livro = Livro(id_,
                      self.entry_titulo.entry.get(),
                      self.entry_autor.entry.get(),
                      self.entry_ano.entry.get())

        self.arvore.inserir(livro)
        self.atualizar_desenho()
        messagebox.showinfo("OK", "Livro inserido.")
        self.atualizar_info()

    def remover(self):
        try:
            id_ = int(self.entry_id.entry.get().strip())
        except Exception:
            messagebox.showerror("Erro", "ID inválido.")
            return

        self.arvore.remove(Livro(id_, "", "", ""))
        self.atualizar_desenho()
        messagebox.showinfo("OK", "Livro removido (se existia).")
        self.atualizar_info()

    def buscar(self):
        try:
            id_ = int(self.entry_id.entry.get().strip())
        except Exception:
            messagebox.showerror("Erro", "ID inválido.")
            return

        livro = Livro(id_, "", "", "")

        encontrado = self.arvore.busca(livro)
        tempo = self.arvore.buscar_com_tempo(livro)
        if encontrado:
            messagebox.showinfo(
                "Livro Disponível",
                f"Tempo: {tempo:.4f}\n"
                f"ID: {encontrado.id}\n"
                f"Título: {encontrado.titulo}\n"
                f"Autor: {encontrado.autor}\n"
                f"Ano: {encontrado.ano}"
            )
        else:
            messagebox.showwarning(
                "Não encontrado",
                "Livro não encontrado."
            )



    def listar_in_order(self):
        print("\n--- IN ORDER ---")
        self.arvore.imprimir_in_order()
        messagebox.showinfo("Console", "Resultado no console.")

    def listar_pre(self):
        print("\n--- PRE ORDER ---")
        self.arvore.imprimir_pre_order()
        messagebox.showinfo("Console", "Resultado no console.")

    def listar_pos(self):
        print("\n--- POS ORDER ---")
        self.arvore.imprimir_pos_order()
        messagebox.showinfo("Console", "Resultado no console.")

    def atualizar_desenho(self):
        self.canvas.update_idletasks()
        self.desenho.desenhar(self.arvore.raiz)

    def limpar_arvore(self):
        if messagebox.askyesno("Confirmar", "Deseja limpar a árvore?"):
            try:
                if hasattr(self.arvore, "limpar"):
                    self.arvore.limpar()
                else:
                    self.arvore = ArvoreAVL()
                self.atualizar_desenho()
                self.atualizar_info()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def _set_status(self, text):
        self.status.config(text=text)

    def atualizar_info(self):
        try:
            n = self.arvore.contar()
        except Exception:
            n = "?"
        self.info.config(text=f"Livros: {n}")
        self._set_status(f"Pronto — nós: {n}")




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
