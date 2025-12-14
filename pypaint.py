#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyPaint - Application de dessin simple style Paint
"""

import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageTk
import os


class PyPaint:
    def __init__(self, root):
        self.root = root
        self.root.title("PyPaint - Application de Dessin")
        self.root.geometry("1000x700")

        # Variables
        self.current_color = "#000000"
        self.brush_size = 3
        self.current_tool = "pencil"
        self.start_x = None
        self.start_y = None
        self.drawing = False

        # Pour les formes temporaires
        self.temp_shape = None

        # Historique pour Undo/Redo
        self.history = []
        self.history_index = -1
        self.max_history = 50

        # Image PIL pour sauvegarde
        self.canvas_width = 800
        self.canvas_height = 550
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Setup UI
        self.setup_menu()
        self.setup_toolbar()
        self.setup_canvas()
        self.setup_color_palette()
        self.setup_statusbar()

        # Sauvegarder l'état initial
        self.save_state()

        # Raccourcis clavier
        self.setup_shortcuts()

    def setup_menu(self):
        """Créer la barre de menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau", command=self.new_canvas, accelerator="Ctrl+N")
        file_menu.add_command(label="Ouvrir...", command=self.open_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Sauvegarder...", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.quit_app, accelerator="Ctrl+Q")

        # Menu Edition
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edition", menu=edit_menu)
        edit_menu.add_command(label="Annuler", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Rétablir", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Effacer tout", command=self.clear_canvas)

        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="À propos", command=self.show_about)

    def setup_toolbar(self):
        """Créer la barre d'outils"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Style pour les boutons
        style = ttk.Style()
        style.configure("Tool.TButton", padding=5)
        style.configure("ActiveTool.TButton", padding=5, background="lightblue")

        # Frame pour les outils
        tools_frame = ttk.LabelFrame(toolbar, text="Outils")
        tools_frame.pack(side=tk.LEFT, padx=5)

        self.tool_buttons = {}
        tools = [
            ("pencil", "✏️ Crayon", "P"),
            ("eraser", "🧹 Gomme", "E"),
            ("line", "📏 Ligne", "L"),
            ("rectangle", "⬜ Rectangle", "R"),
            ("ellipse", "⭕ Ellipse", "O"),
            ("fill", "🪣 Remplir", "F"),
            ("text", "📝 Texte", "T"),
        ]

        for tool_id, tool_name, shortcut in tools:
            btn = ttk.Button(
                tools_frame,
                text=tool_name,
                command=lambda t=tool_id: self.select_tool(t),
                style="Tool.TButton"
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.tool_buttons[tool_id] = btn

        # Sélectionner crayon par défaut
        self.select_tool("pencil")

        # Frame pour la taille du pinceau
        size_frame = ttk.LabelFrame(toolbar, text="Taille")
        size_frame.pack(side=tk.LEFT, padx=10)

        self.size_var = tk.IntVar(value=3)
        self.size_slider = ttk.Scale(
            size_frame,
            from_=1,
            to=50,
            variable=self.size_var,
            command=self.change_size,
            length=100
        )
        self.size_slider.pack(side=tk.LEFT, padx=5)

        self.size_label = ttk.Label(size_frame, text="3 px")
        self.size_label.pack(side=tk.LEFT, padx=5)

        # Bouton couleur personnalisée
        color_frame = ttk.LabelFrame(toolbar, text="Couleur")
        color_frame.pack(side=tk.LEFT, padx=10)

        self.color_preview = tk.Canvas(color_frame, width=30, height=30, bg=self.current_color)
        self.color_preview.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(
            color_frame,
            text="Choisir...",
            command=self.choose_color
        ).pack(side=tk.LEFT, padx=5)

    def setup_canvas(self):
        """Créer le canvas de dessin"""
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Canvas avec scrollbars
        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="white",
            cursor="crosshair"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bindings souris
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_motion)

    def setup_color_palette(self):
        """Créer la palette de couleurs"""
        palette_frame = ttk.LabelFrame(self.root, text="Palette")
        palette_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        colors = [
            "#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF",
            "#FFFF00", "#FF00FF", "#00FFFF", "#808080", "#800000",
            "#008000", "#000080", "#808000", "#800080", "#008080",
            "#FFA500", "#A52A2A", "#FFC0CB", "#90EE90", "#ADD8E6"
        ]

        for color in colors:
            btn = tk.Button(
                palette_frame,
                bg=color,
                width=3,
                height=1,
                command=lambda c=color: self.set_color(c)
            )
            btn.pack(side=tk.LEFT, padx=1, pady=2)

    def setup_statusbar(self):
        """Créer la barre de statut"""
        self.statusbar = ttk.Frame(self.root)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_coords = ttk.Label(self.statusbar, text="Position: 0, 0")
        self.status_coords.pack(side=tk.LEFT, padx=10)

        self.status_tool = ttk.Label(self.statusbar, text="Outil: Crayon")
        self.status_tool.pack(side=tk.LEFT, padx=10)

        self.status_size = ttk.Label(self.statusbar, text=f"Canvas: {self.canvas_width}x{self.canvas_height}")
        self.status_size.pack(side=tk.RIGHT, padx=10)

    def setup_shortcuts(self):
        """Configurer les raccourcis clavier"""
        self.root.bind("<Control-n>", lambda e: self.new_canvas())
        self.root.bind("<Control-o>", lambda e: self.open_image())
        self.root.bind("<Control-s>", lambda e: self.save_image())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-q>", lambda e: self.quit_app())

        # Raccourcis outils
        self.root.bind("p", lambda e: self.select_tool("pencil"))
        self.root.bind("e", lambda e: self.select_tool("eraser"))
        self.root.bind("l", lambda e: self.select_tool("line"))
        self.root.bind("r", lambda e: self.select_tool("rectangle"))
        self.root.bind("o", lambda e: self.select_tool("ellipse"))
        self.root.bind("f", lambda e: self.select_tool("fill"))
        self.root.bind("t", lambda e: self.select_tool("text"))

    def select_tool(self, tool):
        """Sélectionner un outil"""
        self.current_tool = tool

        # Mettre à jour l'apparence des boutons
        for t, btn in self.tool_buttons.items():
            if t == tool:
                btn.state(["pressed"])
            else:
                btn.state(["!pressed"])

        # Mettre à jour le curseur
        cursors = {
            "pencil": "pencil",
            "eraser": "circle",
            "line": "crosshair",
            "rectangle": "crosshair",
            "ellipse": "crosshair",
            "fill": "spraycan",
            "text": "xterm"
        }
        self.canvas.config(cursor=cursors.get(tool, "crosshair"))

        # Mettre à jour la barre de statut
        tool_names = {
            "pencil": "Crayon",
            "eraser": "Gomme",
            "line": "Ligne",
            "rectangle": "Rectangle",
            "ellipse": "Ellipse",
            "fill": "Remplissage",
            "text": "Texte"
        }
        self.status_tool.config(text=f"Outil: {tool_names.get(tool, tool)}")

    def set_color(self, color):
        """Définir la couleur actuelle"""
        self.current_color = color
        self.color_preview.config(bg=color)

    def choose_color(self):
        """Ouvrir le sélecteur de couleur"""
        color = colorchooser.askcolor(color=self.current_color, title="Choisir une couleur")
        if color[1]:
            self.set_color(color[1])

    def change_size(self, value):
        """Changer la taille du pinceau"""
        self.brush_size = int(float(value))
        self.size_label.config(text=f"{self.brush_size} px")

    def on_motion(self, event):
        """Gérer le mouvement de la souris"""
        self.status_coords.config(text=f"Position: {event.x}, {event.y}")

    def on_press(self, event):
        """Gérer le clic de souris"""
        self.start_x = event.x
        self.start_y = event.y
        self.drawing = True

        if self.current_tool == "fill":
            self.flood_fill(event.x, event.y)
        elif self.current_tool == "text":
            self.add_text(event.x, event.y)

    def on_drag(self, event):
        """Gérer le glissement de souris"""
        if not self.drawing:
            return

        if self.current_tool == "pencil":
            self.draw_pencil(event)
        elif self.current_tool == "eraser":
            self.draw_eraser(event)
        elif self.current_tool in ["line", "rectangle", "ellipse"]:
            self.draw_shape_preview(event)

    def on_release(self, event):
        """Gérer le relâchement de souris"""
        if not self.drawing:
            return

        if self.current_tool in ["line", "rectangle", "ellipse"]:
            self.finalize_shape(event)

        self.drawing = False
        self.start_x = None
        self.start_y = None

        # Sauvegarder l'état pour undo
        if self.current_tool not in ["fill", "text"]:
            self.save_state()

    def draw_pencil(self, event):
        """Dessiner avec le crayon"""
        if self.start_x and self.start_y:
            # Dessiner sur le canvas
            self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y,
                fill=self.current_color,
                width=self.brush_size,
                capstyle=tk.ROUND,
                smooth=True
            )
            # Dessiner sur l'image PIL
            self.draw.line(
                [self.start_x, self.start_y, event.x, event.y],
                fill=self.current_color,
                width=self.brush_size
            )

        self.start_x = event.x
        self.start_y = event.y

    def draw_eraser(self, event):
        """Effacer (dessiner en blanc)"""
        if self.start_x and self.start_y:
            self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y,
                fill="white",
                width=self.brush_size * 2,
                capstyle=tk.ROUND,
                smooth=True
            )
            self.draw.line(
                [self.start_x, self.start_y, event.x, event.y],
                fill="white",
                width=self.brush_size * 2
            )

        self.start_x = event.x
        self.start_y = event.y

    def draw_shape_preview(self, event):
        """Dessiner un aperçu de la forme"""
        if self.temp_shape:
            self.canvas.delete(self.temp_shape)

        if self.current_tool == "line":
            self.temp_shape = self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y,
                fill=self.current_color,
                width=self.brush_size
            )
        elif self.current_tool == "rectangle":
            self.temp_shape = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline=self.current_color,
                width=self.brush_size
            )
        elif self.current_tool == "ellipse":
            self.temp_shape = self.canvas.create_oval(
                self.start_x, self.start_y, event.x, event.y,
                outline=self.current_color,
                width=self.brush_size
            )

    def finalize_shape(self, event):
        """Finaliser la forme et la dessiner sur l'image PIL"""
        if self.current_tool == "line":
            self.draw.line(
                [self.start_x, self.start_y, event.x, event.y],
                fill=self.current_color,
                width=self.brush_size
            )
        elif self.current_tool == "rectangle":
            self.draw.rectangle(
                [self.start_x, self.start_y, event.x, event.y],
                outline=self.current_color,
                width=self.brush_size
            )
        elif self.current_tool == "ellipse":
            self.draw.ellipse(
                [self.start_x, self.start_y, event.x, event.y],
                outline=self.current_color,
                width=self.brush_size
            )

        self.temp_shape = None

    def flood_fill(self, x, y):
        """Remplissage par diffusion (flood fill simplifié)"""
        # Convertir la couleur hex en RGB
        color_rgb = tuple(int(self.current_color[i:i+2], 16) for i in (1, 3, 5))

        # Obtenir la couleur du pixel cliqué
        try:
            target_color = self.image.getpixel((x, y))
        except:
            return

        if target_color == color_rgb:
            return

        # Flood fill simple avec pile
        pixels = self.image.load()
        stack = [(x, y)]
        filled = set()

        while stack and len(filled) < 100000:  # Limite pour éviter les boucles infinies
            px, py = stack.pop()

            if (px, py) in filled:
                continue
            if px < 0 or px >= self.canvas_width or py < 0 or py >= self.canvas_height:
                continue

            current = pixels[px, py]
            if current != target_color:
                continue

            pixels[px, py] = color_rgb
            filled.add((px, py))

            stack.extend([(px+1, py), (px-1, py), (px, py+1), (px, py-1)])

        # Redessiner le canvas
        self.refresh_canvas()
        self.save_state()

    def add_text(self, x, y):
        """Ajouter du texte"""
        text = simpledialog.askstring("Texte", "Entrez votre texte:")
        if text:
            # Dessiner sur le canvas
            self.canvas.create_text(
                x, y,
                text=text,
                fill=self.current_color,
                font=("Arial", self.brush_size * 4),
                anchor="nw"
            )
            # Dessiner sur l'image PIL
            from PIL import ImageFont
            try:
                font = ImageFont.truetype("arial.ttf", self.brush_size * 4)
            except:
                font = ImageFont.load_default()
            self.draw.text((x, y), text, fill=self.current_color, font=font)
            self.save_state()

    def refresh_canvas(self):
        """Rafraîchir le canvas depuis l'image PIL"""
        self.canvas.delete("all")
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    def save_state(self):
        """Sauvegarder l'état actuel pour undo"""
        # Supprimer les états après l'index actuel (pour redo)
        self.history = self.history[:self.history_index + 1]

        # Ajouter le nouvel état
        self.history.append(self.image.copy())
        self.history_index += 1

        # Limiter la taille de l'historique
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.history_index -= 1

    def undo(self):
        """Annuler la dernière action"""
        if self.history_index > 0:
            self.history_index -= 1
            self.image = self.history[self.history_index].copy()
            self.draw = ImageDraw.Draw(self.image)
            self.refresh_canvas()

    def redo(self):
        """Rétablir l'action annulée"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.image = self.history[self.history_index].copy()
            self.draw = ImageDraw.Draw(self.image)
            self.refresh_canvas()

    def new_canvas(self):
        """Créer un nouveau canvas vierge"""
        if messagebox.askyesno("Nouveau", "Effacer le dessin actuel et créer un nouveau document?"):
            self.clear_canvas()

    def clear_canvas(self):
        """Effacer le canvas"""
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.save_state()

    def save_image(self):
        """Sauvegarder l'image"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg"),
                ("BMP", "*.bmp"),
                ("Tous les fichiers", "*.*")
            ]
        )
        if filepath:
            self.image.save(filepath)
            messagebox.showinfo("Sauvegarde", f"Image sauvegardée: {filepath}")

    def open_image(self):
        """Ouvrir une image"""
        filepath = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("Tous les fichiers", "*.*")
            ]
        )
        if filepath:
            try:
                img = Image.open(filepath)
                img = img.convert("RGB")

                # Redimensionner si nécessaire
                if img.width > self.canvas_width or img.height > self.canvas_height:
                    img.thumbnail((self.canvas_width, self.canvas_height))

                # Créer une nouvelle image blanche et coller l'image ouverte
                self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
                self.image.paste(img, (0, 0))
                self.draw = ImageDraw.Draw(self.image)

                self.refresh_canvas()
                self.save_state()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir l'image: {e}")

    def quit_app(self):
        """Quitter l'application"""
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter PyPaint?"):
            self.root.quit()

    def show_about(self):
        """Afficher la fenêtre À propos"""
        messagebox.showinfo(
            "À propos de PyPaint",
            "PyPaint v1.0\n\n"
            "Une application de dessin simple style Paint\n"
            "Créée avec Python et Tkinter\n\n"
            "Raccourcis clavier:\n"
            "P - Crayon\n"
            "E - Gomme\n"
            "L - Ligne\n"
            "R - Rectangle\n"
            "O - Ellipse\n"
            "F - Remplissage\n"
            "T - Texte\n\n"
            "Ctrl+Z - Annuler\n"
            "Ctrl+Y - Rétablir\n"
            "Ctrl+S - Sauvegarder\n"
            "Ctrl+O - Ouvrir"
        )


def main():
    root = tk.Tk()
    app = PyPaint(root)
    root.mainloop()


if __name__ == "__main__":
    main()
