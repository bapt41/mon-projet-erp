#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from odoo_interface import IF_Odoo  # Votre interface vers Odoo

##############################################################################
#                               Login Page (F1)                              #
##############################################################################
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1166x718")
        self.root.resizable(0, 0)
        self.root.title("Login Page")

        # Paramètres de connexion Odoo
        self.host = "172.31.10.137"
        self.port = "8027"
        self.db   = "demo"

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir    = os.path.join(script_dir, "images")

        bg_path       = os.path.join(img_dir, "background1.png")
        vector_path   = os.path.join(img_dir, "vector.png")
        hyy_path      = os.path.join(img_dir, "hyy.png")
        user_ico      = os.path.join(img_dir, "username_icon.png")
        pass_ico      = os.path.join(img_dir, "password_icon.png")
        show_img_path = os.path.join(img_dir, "show.png")
        hide_img_path = os.path.join(img_dir, "hide.png")
        btn1_path     = os.path.join(img_dir, "btn1.png")

        # ----------- Fond -----------
        try:
            bg = Image.open(bg_path)
            bg_photo = ImageTk.PhotoImage(bg)
            label_bg = tk.Label(self.root, image=bg_photo)
            label_bg.image = bg_photo
            label_bg.pack(fill="both", expand=True)
        except:
            self.root.configure(bg="white")

        # ----------- Frame de login -----------
        self.lgn_frame = tk.Frame(self.root, bg="#040405", width=950, height=600)
        self.lgn_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Titre
        self.heading = tk.Label(
            self.lgn_frame,
            text="WELCOME",
            font=("yu gothic ui", 25, "bold"),
            bg="#040405",
            fg="white"
        )
        self.heading.place(x=80, y=30, width=300, height=30)

        # Image gauche (optionnelle)
        try:
            vect = Image.open(vector_path)
            vect_photo = ImageTk.PhotoImage(vect)
            tk.Label(self.lgn_frame, image=vect_photo, bg="#040405").place(x=5, y=100)
            self._vect_photo = vect_photo
        except:
            pass

        # Image “Sign In” (optionnelle)
        try:
            hyy = Image.open(hyy_path)
            hyy_photo = ImageTk.PhotoImage(hyy)
            tk.Label(self.lgn_frame, image=hyy_photo, bg="#040405").place(x=620, y=130)
            self._hyy_photo = hyy_photo
        except:
            pass

        # Label “Sign In”
        tk.Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white",
                 font=("yu gothic ui", 17, "bold")).place(x=650, y=240)

        # ----------- Username -----------
        tk.Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                 font=("yu gothic ui", 13, "bold")).place(x=550, y=300)

        self.username_entry = tk.Entry(
            self.lgn_frame, textvariable=self.username_var,
            highlightthickness=0, relief=tk.FLAT,
            bg="#040405", fg="#6b6a69", font=("yu gothic ui", 12, "bold"),
            insertbackground="#6b6a69"
        )
        self.username_entry.place(x=580, y=335, width=270)

        tk.Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1",
                  highlightthickness=0).place(x=550, y=359)

        try:
            user_img = Image.open(user_ico)
            user_img_photo = ImageTk.PhotoImage(user_img)
            tk.Label(self.lgn_frame, image=user_img_photo, bg="#040405").place(x=550, y=332)
            self._user_img_photo = user_img_photo
        except:
            pass

        # ----------- Password -----------
        tk.Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                 font=("yu gothic ui", 13, "bold")).place(x=550, y=380)

        self.password_entry = tk.Entry(
            self.lgn_frame, textvariable=self.password_var,
            highlightthickness=0, relief=tk.FLAT,
            bg="#040405", fg="#6b6a69", font=("yu gothic ui", 12, "bold"),
            show="*", insertbackground="#6b6a69"
        )
        self.password_entry.place(x=580, y=416, width=244)

        tk.Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1",
                  highlightthickness=0).place(x=550, y=440)

        try:
            pass_img = Image.open(pass_ico)
            pass_img_photo = ImageTk.PhotoImage(pass_img)
            tk.Label(self.lgn_frame, image=pass_img_photo, bg="#040405").place(x=550, y=414)
            self._pass_img_photo = pass_img_photo
        except:
            pass

        # ----------- Bouton Show/Hide MDP -----------
        try:
            show_img = ImageTk.PhotoImage(file=show_img_path)
            hide_img = ImageTk.PhotoImage(file=hide_img_path)
            self.show_img = show_img
            self.hide_img = hide_img
            self.show_button = tk.Button(
                self.lgn_frame,
                image=self.show_img,
                command=self.show_pwd,
                relief=tk.FLAT,
                activebackground="white",
                borderwidth=0,
                background="white",
                cursor="hand2"
            )
            self.show_button.place(x=860, y=420)
        except:
            pass

        # ----------- Bouton Login -----------
        try:
            btn1 = Image.open(btn1_path)
            btn1_photo = ImageTk.PhotoImage(btn1)
            btn1_label = tk.Label(self.lgn_frame, image=btn1_photo, bg="#040405")
            btn1_label.image = btn1_photo
            btn1_label.place(x=550, y=450)

            self.login_btn = tk.Button(
                btn1_label, text='LOGIN',
                font=("yu gothic ui", 13, "bold"),
                width=20, bd=0, highlightthickness=0, relief='flat',
                fg='white', bg='#3047ff', activebackground='#3047ff',
                command=self.login_action
            )
            self.login_btn.place(x=20, y=10)
            self._btn1_photo = btn1_photo
        except:
            # Fallback si pas d'image
            self.login_btn = tk.Button(
                self.lgn_frame, text='LOGIN',
                font=("yu gothic ui", 13, "bold"),
                width=20, command=self.login_action
            )
            self.login_btn.place(x=600, y=460)

    def show_pwd(self):
        """ Affiche le mot de passe en clair. """
        self.hide_button = tk.Button(
            self.lgn_frame, image=self.hide_img,
            command=self.hide_pwd, relief=tk.FLAT,
            activebackground="white", borderwidth=0,
            background="white", cursor="hand2"
        )
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide_pwd(self):
        """ Re-masque le mot de passe. """
        self.show_button = tk.Button(
            self.lgn_frame, image=self.show_img,
            command=self.show_pwd, relief=tk.FLAT,
            activebackground="white", borderwidth=0,
            background="white", cursor="hand2"
        )
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')

    def login_action(self):
        """ Méthode de connexion Odoo (F1). """
        username = self.username_var.get()
        password = self.password_var.get()

        # Connexion à Odoo
        odoo_conn = IF_Odoo(self.host, self.port, self.db, username, password)
        success = odoo_conn.connect()
        if success:
            # Fermer la fenêtre de login
            self.root.destroy()
            # Ouvrir la fenêtre principale (Dashboard)
            app = DashboardApp(odoo_conn)
            app.mainloop()
        else:
            messagebox.showerror("Erreur", "Impossible de se connecter à Odoo.")


##############################################################################
#                           Dashboard Principal                              #
##############################################################################
class DashboardApp(tk.Tk):
    """
    Fenêtre principale : barre du haut, barre latérale, pages internes (F2-F5).
    """
    def __init__(self, odoo_conn):
        super().__init__()
        self.odoo = odoo_conn
        self.title("ERP Odoo - Production Dashboard")
        self.geometry("1280x720")
        self.configure(bg="#10142c")  # Couleur de fond principale

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(script_dir, "images")

        # ---------- Barre du haut (top bar) ----------
        self.top_bar = tk.Frame(self, bg="#1b1f3b", height=60)
        self.top_bar.pack(side="top", fill="x")

        # Titre à gauche
        self.title_label = tk.Label(
            self.top_bar, text="ERP Odoo Dashboard",
            font=("Arial", 16, "bold"), fg="white", bg="#1b1f3b"
        )
        self.title_label.pack(side="left", padx=20)

        # Label “Compte” à droite (optionnel)
        self.account_label = tk.Label(
            self.top_bar, text="Connecté", font=("Arial", 12),
            fg="white", bg="#1b1f3b"
        )
        self.account_label.pack(side="right", padx=20)

        # ---------- Barre latérale (sidebar) ----------
        self.sidebar = tk.Frame(self, bg="#16193c", width=200)
        self.sidebar.pack(side="left", fill="y")

        # Boutons du sidebar
        # On charge éventuellement des icônes
        def load_icon(filename, size=(24,24)):
            path = os.path.join(self.img_dir, filename)
            if os.path.exists(path):
                icon_img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(icon_img)
            return None

        home_icon   = load_icon("home.png")
        comp_icon   = load_icon("fiche entreprise.png")
        prod_icon   = load_icon("liste produits.png")
        order_icon  = load_icon("Ordres de Fabrication.png")
        qty_icon    = load_icon("modification de la quantité produite.png")

        btn_home = tk.Button(
            self.sidebar, text=" Accueil", image=home_icon, compound="left",
            bg="#16193c", fg="white", font=("Arial", 13),
            bd=0, padx=10, pady=10, anchor="w",
            command=lambda: self.show_frame("HomePage")
        )
        btn_home._icon = home_icon
        btn_home.pack(fill="x")

        btn_company = tk.Button(
            self.sidebar, text=" Entreprise", image=comp_icon, compound="left",
            bg="#16193c", fg="white", font=("Arial", 13),
            bd=0, padx=10, pady=10, anchor="w",
            command=lambda: self.show_frame("CompanyPage")
        )
        btn_company._icon = comp_icon
        btn_company.pack(fill="x")

        btn_products = tk.Button(
            self.sidebar, text=" Produits", image=prod_icon, compound="left",
            bg="#16193c", fg="white", font=("Arial", 13),
            bd=0, padx=10, pady=10, anchor="w",
            command=lambda: self.show_frame("ProductsPage")
        )
        btn_products._icon = prod_icon
        btn_products.pack(fill="x")

        btn_orders = tk.Button(
            self.sidebar, text=" Ordres Fab", image=order_icon, compound="left",
            bg="#16193c", fg="white", font=("Arial", 13),
            bd=0, padx=10, pady=10, anchor="w",
            command=lambda: self.show_frame("OrdersPage")
        )
        btn_orders._icon = order_icon
        btn_orders.pack(fill="x")

        btn_update = tk.Button(
            self.sidebar, text=" Modifier Qté", image=qty_icon, compound="left",
            bg="#16193c", fg="white", font=("Arial", 13),
            bd=0, padx=10, pady=10, anchor="w",
            command=lambda: self.show_frame("UpdateQtyPage")
        )
        btn_update._icon = qty_icon
        btn_update.pack(fill="x")

        # ---------- Zone principale (pages) ----------
        self.content_frame = tk.Frame(self, bg="#10142c")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Création des frames/pages
        self.frames = {}
        for PageClass in (HomePage, CompanyPage, ProductsPage, OrdersPage, UpdateQtyPage):
            page = PageClass(self.content_frame, self)
            self.frames[PageClass.__name__] = page
            page.place(x=0, y=0, relwidth=1, relheight=1)

        # Page d’accueil par défaut
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        """ Affiche la page demandée en la mettant au premier plan. """
        frame = self.frames[page_name]
        frame.tkraise()


##############################################################################
#                          Pages (F2-F5 + Home)                              #
##############################################################################
class HomePage(tk.Frame):
    """
    Page d'accueil / Tableau de bord.
    On y affiche la date du jour, l'utilisateur connecté, 
    et quelques indicateurs clés (KPI).
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#10142c")
        self.app = app

        # On récupère l'utilisateur connecté (si vous avez son nom depuis Odoo ou depuis la LoginPage)
        # Par exemple, si vous avez un attribut self.app.odoo.user => on l'affiche
        user_name = self.app.odoo.user or "Utilisateur"

        # 1) Barre de titre / date
        title_frame = tk.Frame(self, bg="#10142c")
        title_frame.pack(fill="x", pady=10)

        tk.Label(title_frame, text="Tableau de bord d'entreprise",
                 bg="#10142c", fg="white", font=("Arial", 24, "bold")
        ).pack(side="left", padx=20)

        # Date du jour
        import datetime
        now = datetime.datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        tk.Label(title_frame, text=f"Aujourd'hui : {date_str}",
                 bg="#10142c", fg="white", font=("Arial", 14)
        ).pack(side="right", padx=20)

        # 2) Infos sur l'utilisateur
        user_frame = tk.Frame(self, bg="#1b1f3b")
        user_frame.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(user_frame, text=f"Connecté en tant que : {user_name}",
                 bg="#1b1f3b", fg="white", font=("Arial", 12, "bold")
        ).pack(side="left", padx=10, pady=10)

        # 3) Section “KPI” / Indicateurs
        # On imagine quelques indicateurs (chiffre d'affaires, nombre de commandes, etc.)
        # On les affiche dans des cards horizontales
        kpi_frame = tk.Frame(self, bg="#10142c")
        kpi_frame.pack(fill="x", padx=20, pady=10)

        # Exemple : 3 KPI côte à côte
        # KPI 1
        self.create_kpi_card(kpi_frame, "CA Mensuel", "1500k €", "#eb53a2").pack(side="left", expand=True, fill="both", padx=5)
        # KPI 2
        self.create_kpi_card(kpi_frame, "Commandes", "320", "#3aaed8").pack(side="left", expand=True, fill="both", padx=5)
        # KPI 3
        self.create_kpi_card(kpi_frame, "Clients Actifs", "1,200", "#9263f9").pack(side="left", expand=True, fill="both", padx=5)

        # 4) Section “Quick Links” ou “Dernières Tâches”
        bottom_frame = tk.Frame(self, bg="#10142c")
        bottom_frame.pack(fill="both", expand=True, padx=20, pady=(10,20))

        # Quick links
        quick_links_frame = tk.Frame(bottom_frame, bg="#1b1f3b")
        quick_links_frame.pack(side="left", fill="y", padx=5, pady=5)

        tk.Label(quick_links_frame, text="Quick Links", bg="#1b1f3b", fg="white",
                 font=("Arial", 14, "bold")).pack(pady=10, padx=10)

        # Quelques liens factices
        links = ["Créer un produit", "Lister OF en cours", "Gérer la facturation", "Rapport des ventes"]
        for link in links:
            tk.Button(quick_links_frame, text=link, bg="#3047ff", fg="white",
                      font=("Arial", 10), bd=0, padx=10, pady=5).pack(pady=5, padx=10, fill="x")

        # Espace pour un “mini calendrier” ou “tâches”
        tasks_frame = tk.Frame(bottom_frame, bg="#1b1f3b")
        tasks_frame.pack(side="right", expand=True, fill="both", padx=5, pady=5)

        tk.Label(tasks_frame, text="Tâches récentes", bg="#1b1f3b", fg="white",
                 font=("Arial", 14, "bold")).pack(pady=10, padx=10)

        # Liste factice
        tasks = [
            "OF #1002: Production en cours",
            "Commande #SO1001: à livrer",
            "Inventaire mensuel",
            "Formation opérateurs",
        ]
        for task in tasks:
            tk.Label(tasks_frame, text=f"• {task}", bg="#1b1f3b", fg="white",
                     font=("Arial", 12)).pack(anchor="w", padx=20, pady=2)

    def create_kpi_card(self, parent, title, value, color):
        """
        Crée un 'card' de KPI (titre + valeur), renvoie un Frame.
        :param parent: frame parent
        :param title: ex. "CA Mensuel"
        :param value: ex. "150k €"
        :param color: ex. "#eb53a2" (couleur du chiffre)
        """
        frame = tk.Frame(parent, bg="#1b1f3b", width=200, height=80)
        frame.pack_propagate(False)  # pour garder la taille mini

        tk.Label(frame, text=title, bg="#1b1f3b", fg="white",
                 font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(frame, text=value, bg="#1b1f3b", fg=color,
                 font=("Arial", 16, "bold")).pack()

        return frame



class CompanyPage(tk.Frame):
    """ F2 : Afficher la fiche Entreprise depuis Odoo. """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#10142c")
        self.app = app

        tk.Label(self, text="Fiche Entreprise (F2)", bg="#10142c", fg="white",
                 font=("Arial", 18, "bold")).pack(pady=20)

        # Bouton pour charger
        btn = tk.Button(self, text="Afficher Infos", bg="#3047ff", fg="white",
                        font=("Arial", 12, "bold"), command=self.show_company)
        btn.pack(pady=10)

        self.info_label = tk.Label(self, text="", bg="#10142c", fg="white",
                                   font=("Arial", 12), justify="left")
        self.info_label.pack(pady=10)

    def show_company(self):
        info = self.app.odoo.get_company_info()
        if not info:
            messagebox.showwarning("Entreprise", "Impossible de récupérer la fiche entreprise.")
            return
        name   = info.get('name', '')
        street = info.get('street', '')
        city   = info.get('city', '')
        phone  = info.get('phone', '')
        texte  = f"Nom : {name}\nAdresse : {street}\nVille : {city}\nTéléphone : {phone}"
        self.info_label.config(text=texte)


class ProductsPage(tk.Frame):
    """ F3 : Afficher la liste des produits Odoo avec image et infos dans des 'tuiles'. """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#10142c")
        self.app = app

        # Label titre
        tk.Label(self, text="Liste des Produits (F3)",
                 bg="#10142c", fg="white", font=("Arial", 18, "bold")).pack(pady=20)

        # Bouton pour charger les produits
        btn = tk.Button(self, text="Charger Produits", bg="#3047ff", fg="white",
                        font=("Arial", 12, "bold"), command=self.show_products)
        btn.pack(pady=10)

        # --- Création d'une zone scrollable ---
        # On utilise un Canvas + un Frame + une Scrollbar
        container = tk.Frame(self, bg="#10142c")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(container, bg="#10142c", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#10142c")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Pour conserver les références d'images (sinon garbage collector)
        self.product_images = []

    def show_products(self):
        # On vide le contenu existant (si on reclique plusieurs fois)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.product_images.clear()

        # Récupérer les produits avec les champs souhaités
        # Pour la catégorie, la description, etc., il faut préciser ces champs dans l'interface Odoo
        # Par exemple, adapter la méthode get_products() pour inclure 'categ_id', 'description_sale', ...
        products = self.app.odoo.get_products()  # À adapter si nécessaire

        if not products:
            messagebox.showinfo("Produits", "Aucun produit trouvé.")
            return

        # Pour chaque produit, créer une tuile
        for idx, prod in enumerate(products):
            name  = prod.get("name", "N/A")
            price = prod.get("list_price", 0.0)
            
            # On suppose qu'on a 'categ_id' et 'description_sale' si vous les avez demandés
            categ_id = prod.get("categ_id", False)  # parfois c'est [id, "nom de la catégorie"]
            # Si c'est un Many2one, Odoo renvoie un tuple [id, "NomCat"]
            category_name = ""
            if isinstance(categ_id, list) and len(categ_id) == 2:
                category_name = categ_id[1]

            description = prod.get("description_sale", "")

            # Récupérer l'image base64
            image_b64 = prod.get("image_1920", False)

            # Frame “tuile”
            tile_frame = tk.Frame(self.scrollable_frame, bg="#1b1f3b", bd=2, relief="groove")
            tile_frame.pack(fill="x", pady=5, padx=5)

            # Décoder l'image si présente
            if image_b64:
                import base64
                image_data = base64.b64decode(image_b64)
                # Convertir en PhotoImage via PIL
                from io import BytesIO
                img_PIL = Image.open(BytesIO(image_data))
                img_PIL = img_PIL.resize((80, 80), Image.Resampling.LANCZOS)  # Redimension
                photo = ImageTk.PhotoImage(img_PIL)
            else:
                photo = None

            if photo:
                self.product_images.append(photo)  # garder la référence
                img_label = tk.Label(tile_frame, image=photo, bg="#1b1f3b")
                img_label.pack(side="left", padx=10, pady=10)

            # Frame pour le texte (nom, prix, catégorie, description)
            text_frame = tk.Frame(tile_frame, bg="#1b1f3b")
            text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            # Nom
            tk.Label(text_frame, text=f"Name: {name}",
                     bg="#1b1f3b", fg="white", font=("Arial", 12, "bold")
                     ).pack(anchor="w")

            # Prix
            tk.Label(text_frame, text=f"Price: {price}",
                     bg="#1b1f3b", fg="white", font=("Arial", 12)
                     ).pack(anchor="w")

            # Catégorie
            tk.Label(text_frame, text=f"Category: {category_name}",
                     bg="#1b1f3b", fg="white", font=("Arial", 12)
                     ).pack(anchor="w")

            # Description
            tk.Label(text_frame, text=f"Description: {description}",
                     bg="#1b1f3b", fg="white", font=("Arial", 12)
                     ).pack(anchor="w")



class OrdersPage(tk.Frame):
    """ F4 : Afficher la liste des Ordres de Fab, avec un éventuel filtre d'état. """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#10142c")
        self.app = app

        tk.Label(self, text="Liste OF (F4)", bg="#10142c", fg="white",
                 font=("Arial", 18, "bold")).pack(pady=20)

        filter_frame = tk.Frame(self, bg="#10142c")
        filter_frame.pack()

        tk.Label(filter_frame, text="État OF :", bg="#10142c", fg="white",
                 font=("Arial", 12)).pack(side="left", padx=5)

        self.filter_var = tk.StringVar()
        filter_entry = tk.Entry(filter_frame, textvariable=self.filter_var)
        filter_entry.pack(side="left", padx=5)

        btn_load = tk.Button(filter_frame, text="Charger OF", bg="#3047ff", fg="white",
                             font=("Arial", 12), command=self.show_of)
        btn_load.pack(side="left", padx=5)

        tree_frame = tk.Frame(self, bg="#10142c")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("name", "qty", "produced", "state")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        self.tree.heading("name", text="Nom OF")
        self.tree.heading("qty", text="Qté Demandée")
        self.tree.heading("produced", text="Qté Produite")
        self.tree.heading("state", text="État")
        self.tree.column("name", width=150)
        self.tree.column("qty", width=100)
        self.tree.column("produced", width=100)
        self.tree.column("state", width=100)
        self.tree.pack(fill="both", expand=True)

    def show_of(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        state = self.filter_var.get().strip()
        if state:
            orders = self.app.odoo.get_manufacturing_orders(state_filter=state)
        else:
            orders = self.app.odoo.get_manufacturing_orders()

        if not orders:
            messagebox.showinfo("OF", "Aucun ordre trouvé.")
            return

        for of in orders:
            name_of   = of.get("name", "")
            qty       = of.get("product_qty", 0.0)
            produced  = of.get("qty_producing", 0.0)
            state_of  = of.get("state", "")
            self.tree.insert("", tk.END, values=(name_of, qty, produced, state_of))


class UpdateQtyPage(tk.Frame):
    """ F5 : Mettre à jour la quantité produite d'un OF. """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#10142c")
        self.app = app

        tk.Label(self, text="Modifier Qté Produite (F5)", bg="#10142c", fg="white",
                 font=("Arial", 18, "bold")).pack(pady=20)

        form_frame = tk.Frame(self, bg="#10142c")
        form_frame.pack(pady=30)

        tk.Label(form_frame, text="ID de l'OF :", bg="#10142c", fg="white",
                 font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.mo_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.mo_id_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Nouvelle quantité :", bg="#10142c", fg="white",
                 font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.qty_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.qty_var).grid(row=1, column=1, padx=5, pady=5)

        update_btn = tk.Button(
            self, text="Mettre à jour", bg="#3047ff", fg="white",
            font=("Arial", 12, "bold"), command=self.update_of_qty
        )
        update_btn.pack()

    def update_of_qty(self):
        mo_id_str = self.mo_id_var.get().strip()
        if not mo_id_str:
            return
        try:
            mo_id = int(mo_id_str)
        except ValueError:
            messagebox.showerror("Erreur", "ID invalide.")
            return

        new_qty_str = self.qty_var.get().strip()
        if not new_qty_str:
            return
        try:
            new_qty = float(new_qty_str)
        except ValueError:
            messagebox.showerror("Erreur", "Quantité invalide.")
            return

        ok = self.app.odoo.update_mo_quantity(mo_id, new_qty)
        if ok:
            messagebox.showinfo("Succès", f"OF {mo_id} mis à jour.")
        else:
            messagebox.showerror("Erreur", f"Impossible de mettre à jour l'OF {mo_id}.")


##############################################################################
#                           Point d'entrée (main)                            #
##############################################################################
def main():
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()

if __name__ == '__main__':
    main()
