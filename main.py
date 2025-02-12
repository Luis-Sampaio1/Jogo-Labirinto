import threading
import random
import time
import tkinter as tk

# Configuração do labirinto
LAB_SIZE = 15
labirinto = [[" " for _ in range(LAB_SIZE)] for _ in range(LAB_SIZE)]

# Definição de elementos do jogo
PAREDE = "#"
JOGADOR = "P"
INIMIGO = "E"
ARMADILHA = "X"
SAIDA = "S"

# Posições iniciais
jogador_pos = [1, 1]
inimigos = []
armadilhas = []
armadilhas_ativas = []
saida_pos = [LAB_SIZE - 2, LAB_SIZE - 2]

tempo_restante = 15

def gerar_labirinto():
    global labirinto
    labirinto = [[" " for _ in range(LAB_SIZE)] for _ in range(LAB_SIZE)]
    for i in range(LAB_SIZE):
        for j in range(LAB_SIZE):
            if i == 0 or j == 0 or i == LAB_SIZE - 1 or j == LAB_SIZE - 1:
                labirinto[i][j] = PAREDE
            elif i % 2 == 0 and j % 2 == 0:
                labirinto[i][j] = PAREDE
                if i < LAB_SIZE - 2 and j < LAB_SIZE - 2:
                    if random.choice([True, False]):
                        labirinto[i+1][j] = PAREDE
                    else:
                        labirinto[i][j+1] = PAREDE
    labirinto[1][1] = " "
    labirinto[saida_pos[0]][saida_pos[1]] = SAIDA

def atualizar_labirinto():
    for i in range(LAB_SIZE):
        for j in range(LAB_SIZE):
            cor = "white"
            if labirinto[i][j] == PAREDE:
                cor = "black"
            elif [i, j] == jogador_pos:
                cor = "blue"
            elif [i, j] in inimigos:
                cor = "red"
            elif [i, j] in armadilhas and armadilhas_ativas[armadilhas.index([i, j])]:
                cor = "orange"
            elif labirinto[i][j] == SAIDA:
                cor = "green"
            canvas.itemconfig(cells[i][j], fill=cor)
    lbl_tempo.config(text=f"Tempo restante: {tempo_restante}s")

def mover_jogador(event):
    global jogador_pos
    direcoes = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
    dx, dy = direcoes.get(event.keysym.lower(), (0, 0))
    nova_pos = [jogador_pos[0] + dx, jogador_pos[1] + dy]
    if labirinto[nova_pos[0]][nova_pos[1]] != PAREDE:
        jogador_pos = nova_pos
    verificar_estado()
    atualizar_labirinto()

def mover_inimigos():
    while True:
        time.sleep(2)
        for i in range(len(inimigos)):
            dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
            nova_pos = [inimigos[i][0] + dx, inimigos[i][1] + dy]
            if labirinto[nova_pos[0]][nova_pos[1]] != PAREDE:
                inimigos[i] = nova_pos
        atualizar_labirinto()

def alternar_armadilhas():
    while True:
        time.sleep(5)
        for i in range(len(armadilhas_ativas)):
            armadilhas_ativas[i] = not armadilhas_ativas[i]
        atualizar_labirinto()

def cronometro():
    global tempo_restante
    while tempo_restante > 0:
        time.sleep(1)
        tempo_restante -= 1
        atualizar_labirinto()
    resultado("Tempo esgotado! Você perdeu!")

def verificar_estado():
    if jogador_pos in inimigos or (jogador_pos in armadilhas and armadilhas_ativas[armadilhas.index(jogador_pos)]):
        resultado("Você perdeu!")
    elif jogador_pos == saida_pos:
        resultado("Parabéns! Você encontrou a saída!")

def resultado(msg):
    lbl_resultado.config(text=msg)
    root.unbind("<Key>")
    btn_retry.pack()

def reiniciar_jogo():
    global jogador_pos, inimigos, armadilhas, armadilhas_ativas, tempo_restante
    jogador_pos = [1, 1]
    inimigos = [[random.randint(1, LAB_SIZE - 2), random.randint(1, LAB_SIZE - 2)] for _ in range(2)]
    armadilhas = [[random.randint(1, LAB_SIZE - 2), random.randint(1, LAB_SIZE - 2)] for _ in range(3)]
    armadilhas_ativas = [False, False, False]
    tempo_restante = 15
    lbl_resultado.config(text="")
    btn_retry.pack_forget()
    root.bind("<Key>", mover_jogador)
    gerar_labirinto()
    iniciar_jogo()

def iniciar_jogo():
    gerar_labirinto()
    threading.Thread(target=mover_inimigos, daemon=True).start()
    threading.Thread(target=alternar_armadilhas, daemon=True).start()
    threading.Thread(target=cronometro, daemon=True).start()
    atualizar_labirinto()

root = tk.Tk()
root.title("Labirinto com Threads")
canvas = tk.Canvas(root, width=450, height=450)
canvas.pack()
cells = [[canvas.create_rectangle(j*30, i*30, (j+1)*30, (i+1)*30, fill="white", outline="gray") for j in range(LAB_SIZE)] for i in range(LAB_SIZE)]
root.bind("<Key>", mover_jogador)
lbl_tempo = tk.Label(root, text=f"Tempo restante: {tempo_restante}s", font=("Arial", 12))
lbl_tempo.pack()
lbl_resultado = tk.Label(root, text="", font=("Arial", 14))
lbl_resultado.pack()
btn_retry = tk.Button(root, text="Tentar Novamente", font=("Arial", 12), command=reiniciar_jogo)
btn_retry.pack()
btn_retry.pack_forget()
iniciar_jogo()
root.mainloop()
