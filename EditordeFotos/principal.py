import os
import tkinter
from datetime import datetime
from tkinter import filedialog, colorchooser, ttk

from PIL import Image, ImageDraw, ImageFont

nomeproduto = ''
tamanhoproduto = ''
precoproduto = ''
img = ()
with open('D:/pythonProject/EditordeFotos/arquivostxt/fonteusada.txt', 'r') as fonte1:
    global fonte
    fonte = fonte1.read()
with open('D:/pythonProject/EditordeFotos/arquivostxt/pastaparasalvar.txt', 'r') as dir_saida1:
    global dir_saida
    dir_saida = dir_saida1.read()
color = '#a3bdf0'
pergunta_mostrar_foto = False

def salvar_configuracoes():
    global dir_saida, fonte
    with open('D:/pythonProject/EditordeFotos/arquivostxt/pastaparasalvar.txt', 'w') as pastaparasalvar:
        pastaparasalvar.write(dir_saida)
    with open('D:/pythonProject/EditordeFotos/arquivostxt/fonteusada.txt', 'w') as fonteusada:
        fonteusada.write(fonte)
    s = tkinter.Tk()
    t = tkinter.Label(s, text='Configurações salvas', bg='green', fg='white')
    t.pack()
    s.mainloop()

def pergunta_se_quer_mostrar(r):
    global pergunta_mostrar_foto
    if r == False:
        pergunta_mostrar_foto = False
    elif r == True:
        pergunta_mostrar_foto = True

def escolherfonte():
    global fonte
    fonte = filedialog.askopenfilename(title='Selecione a fonte no formato .ttf')
    fonte_escolhida_var.set(fonte)

def defcor(scor):
    global color
    if scor == 'azul':
        color = '#a3bdf0'
        caixaazul['bg'] = color
        caixarosa['bg'] = color
        caixaescolher['bg'] = color
    elif scor == 'rosa':
        color = '#ffd3d4'
        caixaazul['bg'] = color
        caixarosa['bg'] = color
        caixaescolher['bg'] = color

def apagarfotos():
    for foto in img:
        if os.path.exists(foto):
            os.remove(foto)
        else:
            None
    fim = tkinter.Tk()
    msgfim = tkinter.Label(fim, text='FOTOS APAGADAS', bg='yellow', fg='black')
    msgfim.pack()
    fim.mainloop()

def escolhercor():
    global color
    corescolhida = colorchooser.askcolor()
    color = corescolhida[1]
    caixaazul['bg'] = color
    caixarosa['bg'] = color
    caixaescolher['bg'] = color

def processar():
    global nomeproduto, tamanhoproduto, precoproduto, color, tamanhofontec1, tamanhofontec2, tamanhofontec3, img_edt, fonte, pergunta_mostrar_foto
    nomeproduto, tamanhoproduto, precoproduto = nome_produto.get(), tamanho_produto.get(), preco_produto.get()

    for foto in img:
        nome = str(datetime.today()).replace(':', '').replace('-', '').replace('.', '')
        fundobranco = Image.open('D:/pythonProject/EditordeFotos/imagens/undobranco.jpg')
        imagemfrente = Image.open(f"{foto}")
        sizefrente = imagemfrente.size
        fundobranco = fundobranco.resize((sizefrente[0] + sizefrente[0] // 8, sizefrente[1] + sizefrente[1] // 5 + sizefrente[1] // 5 + sizefrente[1] // 5))
        x0 = (fundobranco.size[0] - sizefrente[0]) // 2
        y0 = (fundobranco.size[1] - sizefrente[1]) // 2
        x1 = x0 + sizefrente[0]
        y1 = y0 + sizefrente[1]
        posicao = (x0, y0, x1, y1)
        fundobranco.paste(imagemfrente, posicao)

        # Cria os retângulos
        rect1 = (x0, y0 - (sizefrente[1] // 4), x1, y0 - (sizefrente[1] // 30))  # x, y, largura, altura
        rect2 = (x0, y1 + (sizefrente[1] // 30), x1, y1 + (sizefrente[1] // 4))  # x, y, largura, altura
        rcima = ImageDraw.Draw(fundobranco)
        rcima.rounded_rectangle(rect1, radius=20, fill=color)
        rcima.rounded_rectangle(rect2, radius=20, fill=color)

        # Escreve o texto
        tamanhofontec1 = sizefrente[0] // 8
        tamanhofontec2 = sizefrente[0] // 8
        tamanhofontec3 = sizefrente[0] // 8
        try:
            if int(tamanho_fonte1.get()) != tamanhofontec1:
                tamanhofontec1 = int(tamanho_fonte1.get())
            if int(tamanho_fonte2.get()) != tamanhofontec2:
                tamanhofontec2 = int(tamanho_fonte2.get())
            if int(tamanho_fonte3.get()) != tamanhofontec3:
                tamanhofontec3 = int(tamanho_fonte3.get())
        except:
            None
        fontecima1 = ImageFont.truetype(f'{fonte}', tamanhofontec1)
        fontecima2 = ImageFont.truetype(f'{fonte}', tamanhofontec2)
        fontebaixo = ImageFont.truetype(f'{fonte}', tamanhofontec3)
        rcima.text((fundobranco.size[0] // 2, rect1[1] + sizefrente[1] // 16), f'{nomeproduto}', anchor='mm',
                   font=fontecima1, fill=(0, 0, 0))
        rcima.text((fundobranco.size[0] // 2, rect1[1] + sizefrente[1] // 7), f'{tamanhoproduto}', anchor='mm',
                   font=fontecima2, fill=(0, 0, 0))
        rcima.text((fundobranco.size[0] // 2, rect2[1] + sizefrente[1] // 10), f'{precoproduto}', anchor='mm',
                   font=fontebaixo, fill=(0, 0, 0))
        fundobranco = fundobranco.resize((fundobranco.size[0] // 2, fundobranco.size[1] // 2))
        fundobranco.save(f"{dir_saida}\{nome}.jpg")
        if pergunta_mostrar_foto == True:
            fundobranco.show()
        img_edt.set(f'{img.index(foto) + 1} fotos editadas')
    fim = tkinter.Tk()
    msgfim = tkinter.Label(fim, text='FOTOS PROCESSADAS', padx=10, pady=10, bg='green', fg='white')
    msgfim.pack()
    fim.mainloop()

def selecionarimagens():
    global img
    # Abre uma janela para selecionar as imagens
    img = filedialog.askopenfilenames(title='Selecione as imagens')
    img_var.set(f'{len(img)} fotos selecionadas')

def escolherpastasalvar():
    global dir_saida
    # Abre uma janela de diálogo para escolher o diretório de saída
    dir_saida = filedialog.askdirectory(title='Escolha o diretório de saída')
    dir_saida_var.set(dir_saida)

janela = tkinter.Tk()
janela.title('Editor de fotos')
janela.iconbitmap('D:/pythonProject/EditordeFotos/imagens/ft.ico')
################        cria um objeto com abas            ####################
abas = ttk.Notebook(janela)
abas.grid(row=0, column=0)
abaprincipal = ttk.Frame(abas)
abaconfig = ttk.Frame(abas)
abas.add(abaprincipal, text='Editor')
abas.add(abaconfig, text='Configurações')
############            variavel em tempo real para pasta       ###############
dir_saida_var = tkinter.StringVar()
dir_saida_var.set(dir_saida)
#variavel tempo real para fotos
img_var = tkinter.StringVar()
############        variavel tempo real para fotos editadas     ###############
img_edt = tkinter.StringVar()
#################          variável em tempo real para cor      ###############
var_azul = tkinter.IntVar()
###########      variável tempo real para mostra fonte escolhida   ############
fonte_escolhida_var = tkinter.IntVar()
fonte_escolhida_var.set(fonte)
############        variável tempo real mostrar imagem        ##################
mostrar_var = tkinter.IntVar(value=1)
#########################################################################################
#                                        Aba Editor
#########################################################################################
#############        Nome do produto        ######################
tkinter.Label(abaprincipal, text='Digite o texto dos campos [c1] [c2] [c3]', height=1).grid(row=0, column=0)
nome_produto = tkinter.Entry(abaprincipal, width=30)
nome_produto.grid(row=0, column=1)
################           tamanho do produto        #############
tamanho_produto = tkinter.Entry(abaprincipal, width=30)
tamanho_produto.grid(row=0, column=2)
##############          preco produto     ########################
preco_produto = tkinter.Entry(abaprincipal, width=30)
preco_produto.grid(row=0, column=3)
##################        cor      ###############################
labelcor = tkinter.Label(abaprincipal, text='Cor:', height=2)
labelcor.grid(row=1, column=0)
caixaazul = tkinter.Radiobutton(abaprincipal, text='azul', width=23,bg=color,variable=var_azul, value=0, command=lambda: defcor('azul'))
caixaazul.grid(row=1, column=1)
caixarosa = tkinter.Radiobutton(abaprincipal, text='rosa', width=23, bg=color, variable=var_azul, value=1, command=lambda: defcor('rosa'))
caixarosa.grid(row=1, column=2)
caixaescolher = tkinter.Radiobutton(abaprincipal, text='escolher', width=23, bg=color, variable=var_azul, value=3, command=lambda: escolhercor())
caixaescolher.grid(row=1, column=3)
############        botão de escolher fotos       ###############
botao_fotos = tkinter.Button(abaprincipal, text='Escolher fotos', width=23, bg='gray', pady=5, command=selecionarimagens)
botao_fotos.grid(row=2, column=0)
tkinter.Label(abaprincipal, textvariable=img_var).grid(row=2, column=1, columnspan=2)
###############      botão de processar      ####################
botao_processar = tkinter.Button(abaprincipal, width=23, fg='white', pady=7, bg='green', text='PROCESSAR', command=processar)
botao_processar.grid(row=3, column=0)
tkinter.Label(abaprincipal, textvariable=img_edt).grid(row=3, column=1, columnspan=2)
#botão apagar fotos
botao_apagarfotos = tkinter.Button(abaprincipal, text='APAGAR FOTOS EDITADAS', command=apagarfotos)
tkinter.Label(abaprincipal, text="", height=2).grid(row=4)
botao_apagarfotos.grid(row=5, column=3)
###############################################################################################
#                                      Aba configurações
###############################################################################################
###########       tamanho da fonte     #########################
tkinter.Label(abaconfig, text='Digite o tamanho das fontes [c1] [c2] [c3]', height=1).grid(row=0, column=0)
tamanho_fonte1 = tkinter.Entry(abaconfig, width=30)
tamanho_fonte1.insert(0, '')
tamanho_fonte1.grid(row=0, column=1)
tamanho_fonte2 = tkinter.Entry(abaconfig, width=30)
tamanho_fonte2.grid(row=0, column=2)
tamanho_fonte3 = tkinter.Entry(abaconfig, width=30)
tamanho_fonte3.grid(row=0, column=3)
#############     botão de pasta      #########################
botao_diretório = tkinter.Button(abaconfig, text='Escolha a pasta para salvar', pady=5, bg='gray', width=23, command=escolherpastasalvar)
botao_diretório.grid(row=1, column=0)
tkinter.Label(abaconfig, textvariable=dir_saida_var).grid(row=1, column=1, columnspan=3)
#############     botão de escolher fonte      #################
botao_escolher_fonte = tkinter.Button(abaconfig, text='Selecione a fonte', pady=5, bg='gray', width=23, command=escolherfonte)
botao_escolher_fonte.grid(row=2, column=0)
tkinter.Label(abaconfig, textvariable=fonte_escolhida_var).grid(row=2, column=1, columnspan=3)
############      caixa seletora mostrar        #############
tkinter.Label(abaconfig,text='Mostrar fotos ao final da edição?').grid(row=3, column=0)
mostrar_caixa_sim = tkinter.Radiobutton(abaconfig, text='SIM',value=0, variable=mostrar_var, command=lambda: pergunta_se_quer_mostrar(True))
mostrar_caixa_sim.grid(row=3, column=1)
mostrar_caixa_nao = tkinter.Radiobutton(abaconfig, text='NÃO',value=1, variable=mostrar_var, command=lambda: pergunta_se_quer_mostrar(False))
mostrar_caixa_nao.grid(row=3, column=2)
#############    Botão salvar configurações   ###################
tkinter.Label(abaconfig, text='').grid(row=4, pady=10)
tkinter.Label(abaconfig, text='* não salva tamanho da fonte e nem o seletor mostrar').grid(row=5, column=1, columnspan=2)
botao_salvar_config = tkinter.Button(abaconfig, text='Salvar config', pady=5, bg='gray', width=23, command=lambda: salvar_configuracoes())
botao_salvar_config.grid(row=5, column=3)

janela.mainloop()
