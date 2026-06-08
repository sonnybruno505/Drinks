import tkinter as tk
import random
import customtkinter as ctk

# --- Configuração ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# --- Ingredientes ---
cocktail_ingredients = [
    "Vodka", "Rum", "Gin", "Tequila", "Whiskey", "Triple Sec",
    "Lemon Juice", "Orange Juice", "Pineapple Juice", "Cranberry Juice",
    "Grenadine", "Tonic Water", "Soda", "Cola", "Syrup", "Mint", "Ice"
]

mocktail_ingredients = [
    "Lemon Juice", "Orange Juice", "Pineapple Juice", "Cranberry Juice",
    "Apple Juice", "Mango Juice", "Grenadine", "Syrup", "Mint",
    "Coconut Water", "Tonic Water", "Soda", "Cola", "Ice"
]

# --- Partículas ---
particles = []
trail_particles = []
mouse_x, mouse_y = 325, 260

def create_particles():
    for _ in range(50):
        x = random.randint(0, 650)
        y = random.randint(0, 520)
        size = random.randint(2, 5)
        color = random.choice(["#ff33cc","#33ff33","#66ff99","#ffff33","#ff9933"])
        particles.append({'x':x,'y':y,'size':size,'color':color,'dx':random.choice([-1,1]),'dy':random.choice([-1,1])})

def animate_particles():
    canvas.delete("all")
    # Fundo preto
    canvas.create_rectangle(0,0,650,520,fill="#000000", outline="")
    
    # Partículas de fundo
    for p in particles:
        canvas.create_oval(p['x'],p['y'],p['x']+p['size'],p['y']+p['size'],fill=p['color'],outline="")
        p['x'] += (mouse_x - p['x'])*0.01 + p['dx']
        p['y'] += (mouse_y - p['y'])*0.01 + p['dy']
        if p['x']<0 or p['x']>650: p['dx']*=-1
        if p['y']<0 or p['y']>520: p['dy']*=-1

    # Trilha do mouse
    for _ in range(2):  # adiciona suavidade
        trail_particles.append({'x':mouse_x, 'y':mouse_y, 'size':random.randint(3,6),
                                'color':random.choice(["#ff33cc","#33ff33","#66ff99","#ffff33","#ff9933"]),
                                'lifetime':8})

    # Desenha e atualiza rastro
    new_trail = []
    for tp in trail_particles:
        if tp['lifetime'] > 0:
            canvas.create_oval(tp['x'],tp['y'],tp['x']+tp['size'],tp['y']+tp['size'],fill=tp['color'],outline="")
            tp['lifetime'] -= 1
            new_trail.append(tp)
    trail_particles[:] = new_trail
    
    root.after(50, animate_particles)

def mouse_motion(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y

def click_particles():
    # Explosão de partículas ao clicar nos botões
    for _ in range(20):
        trail_particles.append({
            'x': mouse_x + random.randint(-20,20),
            'y': mouse_y + random.randint(-20,20),
            'size': random.randint(4,8),
            'color': random.choice(["#ff33cc","#33ff33","#66ff99","#ffff33","#ff9933"]),
            'lifetime':10
        })

# --- Função para gerar drink ---
def generate_drink(drink_type):
    click_particles()  # efeito de explosão ao clicar
    try:
        num = int(entry.get())
        if num < 2 or num > 6:
            result_label.configure(text="⚠️ Escolha entre 2 e 6 ingredientes.", text_color="#ff3333")
            return
    except ValueError:
        result_label.configure(text="⚠️ Digite um número válido.", text_color="#ff3333")
        return

    if drink_type == "cocktail":
        chosen = random.sample(cocktail_ingredients, num)
        drink_name = "Cocktail 🍸"
        color = "#9b30ff"
    else:
        chosen = random.sample(mocktail_ingredients, num)
        drink_name = "Mocktail 🥤"
        color = "#33ff33"

    result = f"{drink_name} com {num} ingredientes:\n\n"
    for ing in chosen:
        qtd = random.randint(20, 60)
        result += f"🍹 {ing}: {qtd} ml\n"

    result += "\nModo de Preparo:\n"
    result += "1. Adicione os ingredientes em uma coqueteleira com gelo.\n"
    result += "2. Agite bem por alguns segundos.\n"
    result += "3. Coe em um copo e decore a gosto. 🌿"

    result_label.configure(text=result, text_color=color)

# --- Interface ---
root = ctk.CTk()
root.title("Gerador de Drinks Futurista 🍹")
root.geometry("650x520")

canvas = tk.Canvas(root, width=650, height=520, highlightthickness=0, bg="#000000")
canvas.pack(fill="both", expand=True)
canvas.bind('<Motion>', mouse_motion)

# Entrada
label = ctk.CTkLabel(root, text="Quantos ingredientes (2 a 6)?", font=("Comic Sans MS", 16, "bold"), text_color="white")
label.place(x=160, y=15)

entry = ctk.CTkEntry(root, width=50, height=35, font=("Arial", 14), justify="center", fg_color="#111111", text_color="#00ffcc")
entry.place(x=280, y=60)

# Botões arredondados
btn_cocktail = ctk.CTkButton(root, text="Gerar Cocktail 🍸", width=160, height=40, fg_color="#9b30ff", text_color="black", corner_radius=15, font=("Comic Sans MS", 12, "bold"), command=lambda: generate_drink("cocktail"))
btn_cocktail.place(x=150, y=110)

btn_mocktail = ctk.CTkButton(root, text="Gerar Mocktail 🥤", width=160, height=40, fg_color="#33ff33", text_color="black", corner_radius=15, font=("Comic Sans MS", 12, "bold"), command=lambda: generate_drink("mocktail"))
btn_mocktail.place(x=340, y=110)

# Resultado estático
result_label = ctk.CTkLabel(root, text="", font=("Arial", 14, "bold"), width=550, height=330, corner_radius=10, fg_color="#111111", text_color="#00ffcc", justify="left", anchor="nw")
result_label.place(x=50, y=170)

# Inicializa partículas
create_particles()
animate_particles()

root.mainloop()

