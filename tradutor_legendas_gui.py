import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from deep_translator import GoogleTranslator
import pysrt
import webbrowser

# Idiomas disponíveis
IDIOMAS = {
    "Inglês": "en",
    "Português": "pt",
    "Espanhol": "es",
    "Francês": "fr",
    "Alemão": "de",
    "Italiano": "it",
    "Japonês": "ja",
    "Chinês": "zh-CN"
}

def traduzir_legenda(input_file, output_folder, src_lang, dest_lang, progress_callback=None):
    subs = pysrt.open(input_file)
    translator = GoogleTranslator(source=src_lang, target=dest_lang)
    total = len(subs)

    for i, sub in enumerate(subs, start=1):
        texto_original = sub.text.strip().replace("\n", " ")
        try:
            traducao = translator.translate(texto_original)
            # Quebrar linhas longas automaticamente
            if "\n" in sub.text or len(traducao) > 40:
                partes = traducao.split(" ")
                linhas = []
                linha_temp = ""
                for palavra in partes:
                    if len(linha_temp) + len(palavra) < 40:
                        linha_temp += (palavra + " ")
                    else:
                        linhas.append(linha_temp.strip())
                        linha_temp = palavra + " "
                if linha_temp:
                    linhas.append(linha_temp.strip())
                sub.text = "\n".join(linhas)
            else:
                sub.text = traducao
        except Exception as e:
            print(f"Erro ao traduzir: {texto_original} -> {e}")
        if progress_callback:
            progress_callback(i, total)

    output_file = os.path.join(output_folder, "legenda_traduzida.srt")
    subs.save(output_file, encoding='utf-8')
    return output_file

def selecionar_legenda():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de legenda", "*.srt")])
    if arquivo:
        entrada_var.set(arquivo)

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        saida_var.set(pasta)

def abrir_pasta_saida():
    if saida_var.get():
        webbrowser.open(saida_var.get())
    else:
        messagebox.showwarning("Aviso", "Nenhuma pasta selecionada!")

def alternar_tema():
    tema_atual = app.style.theme.name
    novo_tema = "flatly" if tema_atual == "cyborg" else "cyborg"
    app.style.theme_use(novo_tema)

def iniciar_traducao():
    if not entrada_var.get() or not saida_var.get():
        messagebox.showwarning("Aviso", "Selecione o arquivo de legenda e a pasta de saída!")
        return
    
    botao_traduzir.config(state="disabled")
    progresso["value"] = 0

    def tarefa():
        try:
            traduzir_legenda(
                entrada_var.get(),
                saida_var.get(),
                IDIOMAS[idioma_origem_var.get()],
                IDIOMAS[idioma_destino_var.get()],
                progress_callback=lambda atual, total: progresso.config(value=(atual/total)*100)
            )
            messagebox.showinfo("Concluído", "Legenda traduzida com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            botao_traduzir.config(state="normal")

    threading.Thread(target=tarefa, daemon=True).start()

def mostrar_sobre():
    from tkinter import messagebox
    messagebox.showinfo(
        "Sobre",
        "Tradutor de Legendas v1.0\n"
        "Desenvolvido por: Erik Vasconcelos\n"
        "Contato: erikvasconcelosprogramador@gmail.com\n"
        "GitHub: github.com/erik-vasc"
    )


# --- INTERFACE ---
app = ttk.Window(title="Tradutor de Legendas", themename="cyborg")  # Dark mode por padrão
app.geometry("520x520")
app.resizable(False, False)

entrada_var = tk.StringVar()
saida_var = tk.StringVar()
idioma_origem_var = tk.StringVar(value="Inglês")
idioma_destino_var = tk.StringVar(value="Português")

# --- FRAME PRINCIPAL ---
frame = ttk.Frame(app, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Tradutor de Legendas", font=("Segoe UI", 18, "bold")).pack(pady=10)

# SEÇÃO: Seleção de arquivos
ttk.Label(frame, text="Arquivo de legenda:").pack(anchor="w")
ttk.Entry(frame, textvariable=entrada_var, width=55).pack(pady=2)
ttk.Button(frame, text="📂 Selecionar arquivo", command=selecionar_legenda, bootstyle="info").pack(pady=5)

ttk.Label(frame, text="Pasta de saída:").pack(anchor="w")
ttk.Entry(frame, textvariable=saida_var, width=55).pack(pady=2)
ttk.Button(frame, text="📁 Selecionar pasta", command=selecionar_pasta, bootstyle="info").pack(pady=5)

# SEÇÃO: Idiomas
idiomas_frame = ttk.Frame(frame)
idiomas_frame.pack(pady=10)
ttk.Label(idiomas_frame, text="Origem:").grid(row=0, column=0, padx=5)
ttk.Combobox(idiomas_frame, textvariable=idioma_origem_var, values=list(IDIOMAS.keys()), width=15).grid(row=0, column=1, padx=5)
ttk.Label(idiomas_frame, text="Destino:").grid(row=0, column=2, padx=5)
ttk.Combobox(idiomas_frame, textvariable=idioma_destino_var, values=list(IDIOMAS.keys()), width=15).grid(row=0, column=3, padx=5)

# SEÇÃO: Progresso
progresso = ttk.Progressbar(frame, bootstyle="success-striped", length=400)
progresso.pack(pady=10)

# Botões principais
botoes_frame = ttk.Frame(frame)
botoes_frame.pack(pady=10)

botao_traduzir = ttk.Button(botoes_frame, text="🔄 Traduzir", command=iniciar_traducao, bootstyle="primary")
botao_traduzir.grid(row=0, column=0, padx=5)

ttk.Button(botoes_frame, text="📂 Abrir pasta de saída", command=abrir_pasta_saida, bootstyle="secondary").grid(row=0, column=1, padx=5)
ttk.Button(botoes_frame, text="🌗 Alternar tema", command=alternar_tema, bootstyle="dark").grid(row=0, column=2, padx=5)

ttk.Button(frame, text="ℹ️ Sobre", command=mostrar_sobre, bootstyle="info").pack(pady=5)

creditos_label = ttk.Label(frame, text="Desenvolvido por Erik Vasconcelos", font=("Segoe UI", 9))
creditos_label.pack(side="bottom", pady=10)


app.mainloop()
