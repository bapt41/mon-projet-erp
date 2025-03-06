#05/03/2025
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
        vector_path   = os.path.join(img_dir, "Logo BikeLab_V2.png")
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
        except Exception as e:
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
        odoo_conn = IF_Odoo(self.host, self.port, self.db, username, password)
        success = odoo_conn.connect()
        if success:
            self.root.destroy()
            app = DashboardApp(odoo_conn)
            app.mainloop()
        else:
            messagebox.showerror("Erreur", "Impossible de se connecter à Odoo.")


##############################################################################
#                           Dashboard Principal                              #
##############################################################################
class DashboardApp(tk.Tk):
    """
    Fenêtre principale de l'application ERP Odoo.
    Affiche une barre du haut avec le titre et le profil utilisateur (photo, nom).
    La barre latérale permet de naviguer entre les pages (HomePage, CompanyPage, ProductsPage, OrdersPage).
    La classe surveille également la connexion à Odoo et tente une reconnexion en cas de coupure.
    """
    def __init__(self, odoo_conn):
        super().__init__()
        self.odoo = odoo_conn
        self.title("ERP Odoo - Production Dashboard")
        self.geometry("1280x720")
        self.configure(bg="#10142c")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(script_dir, "images")

        # ---------- Barre du haut ----------
        self.top_bar = tk.Frame(self, bg="#1b1f3b", height=60)
        self.top_bar.pack(side="top", fill="x")

        # Titre
        self.title_label = tk.Label(
            self.top_bar,
            text="ERP Odoo Dashboard",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#1b1f3b"
        )
        self.title_label.pack(side="left", padx=20)

        # Récupération du profil utilisateur
        try:
            profile = self.odoo.get_user_profile()
        except Exception as e:
            print("Erreur lors de la récupération du profil :", e)
            profile = {}
        # Charger la photo de profil si disponible
        self.profile_photo = None
        if profile.get("image_1920"):
            try:
                from io import BytesIO
                import base64
                image_data = base64.b64decode(profile["image_1920"])
                img = Image.open(BytesIO(image_data))
                img = img.resize((40, 40), Image.Resampling.LANCZOS)
                self.profile_photo = ImageTk.PhotoImage(img)
            except Exception as e:
                print("Erreur lors du chargement de l'image de profil:", e)

        # Bouton profil : affiche la photo et le nom, et gère le clic pour déconnexion
        self.profile_button = tk.Button(
            self.top_bar,
            image=self.profile_photo,
            text=profile.get("name", "Utilisateur"),
            compound="left",
            font=("Arial", 12),
            fg="white",
            bg="#1b1f3b",
            activebackground="#1b1f3b",
            bd=0,
            command=self.on_profile_click
        )
        self.profile_button.pack(side="right", padx=20)

        self.account_label = tk.Label(
            self.top_bar,
            text="Connecté",
            font=("Arial", 12),
            fg="white",
            bg="#1b1f3b"
        )
        self.account_label.pack(side="right", padx=10)

        # ---------- Barre latérale ----------
        self.sidebar = tk.Frame(self, bg="#16193c", width=200)
        self.sidebar.pack(side="left", fill="y")

        def load_icon(filename, size=(24,24)):
            path = os.path.join(self.img_dir, filename)
            if os.path.exists(path):
                try:
                    icon_img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
                    return ImageTk.PhotoImage(icon_img)
                except Exception as e:
                    print(f"Erreur lors du chargement de l'icône {filename}: {e}")
            return None

        home_icon = load_icon("home.png")
        comp_icon = load_icon("fiche entreprise.png")
        prod_icon = load_icon("liste produits.png")
        order_icon = load_icon("Ordres de Fabrication.png")

        btn_home = tk.Button(
            self.sidebar,
            text=" Accueil",
            image=home_icon,
            compound="left",
            bg="#16193c",
            fg="white",
            font=("Arial", 13),
            bd=0,
            padx=10,
            pady=10,
            anchor="w",
            command=lambda: self.show_frame("HomePage")
        )
        btn_home._icon = home_icon  # Conserver la référence
        btn_home.pack(fill="x")

        btn_company = tk.Button(
            self.sidebar,
            text=" Entreprise",
            image=comp_icon,
            compound="left",
            bg="#16193c",
            fg="white",
            font=("Arial", 13),
            bd=0,
            padx=10,
            pady=10,
            anchor="w",
            command=lambda: self.show_frame("CompanyPage")
        )
        btn_company._icon = comp_icon
        btn_company.pack(fill="x")

        btn_products = tk.Button(
            self.sidebar,
            text=" Produits",
            image=prod_icon,
            compound="left",
            bg="#16193c",
            fg="white",
            font=("Arial", 13),
            bd=0,
            padx=10,
            pady=10,
            anchor="w",
            command=lambda: self.show_frame("ProductsPage")
        )
        btn_products._icon = prod_icon
        btn_products.pack(fill="x")

        btn_orders = tk.Button(
            self.sidebar,
            text=" Ordres Fab",
            image=order_icon,
            compound="left",
            bg="#16193c",
            fg="white",
            font=("Arial", 13),
            bd=0,
            padx=10,
            pady=10,
            anchor="w",
            command=lambda: self.show_frame("OrdersPage")
        )
        btn_orders._icon = order_icon
        btn_orders.pack(fill="x")

        # ---------- Zone principale (pages) ----------
        self.content_frame = tk.Frame(self, bg="#10142c")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Création des pages (HomePage, CompanyPage, ProductsPage, OrdersPage)
        self.frames = {}
        for PageClass in (HomePage, CompanyPage, ProductsPage, OrdersPage):
            try:
                page = PageClass(self.content_frame, self)
                self.frames[PageClass.__name__] = page
                page.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print(f"Erreur lors de la création de la page {PageClass.__name__} : {e}")

        self.show_frame("HomePage")

        # Démarrer la surveillance de la connexion
        self.check_connection()

    def on_profile_click(self):
        profile = self.odoo.get_user_profile()
        is_admin = not profile.get("share", True)  # Si share est False, l'utilisateur est admin
        admin_text = "admin" if is_admin else "Utilisateur"
        # Vérifier si la fenêtre existe avant d'afficher la boîte de dialogue
        if self.winfo_exists():
            choix = messagebox.askquestion(
                "Profil",
                f"{profile.get('name', 'Utilisateur')}\nStatut : {admin_text}\nVoulez-vous vous déconnecter ?"
            )
            if choix == 'yes':
                self.destroy()
                # Réafficher la page de connexion
                LoginPage(tk.Tk()).root.mainloop()

    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()
        else:
            print(f"[DashboardApp] La page '{page_name}' n'existe pas.")

    def check_connection(self):
        try:
            _ = self.odoo.get_company_info()
        except Exception as e:
            # Vérifier si la fenêtre est toujours active
            if self.winfo_exists():
                try:
                    messagebox.showerror("Erreur de connexion", "La connexion à Odoo a été interrompue.\nL'application va tenter de se reconnecter.")
                except tk.TclError:
                    pass
            self.try_reconnect()
            return
        self.after(10000, self.check_connection)

    def try_reconnect(self):
        try:
            if self.odoo.connect():
                if self.winfo_exists():
                    try:
                        messagebox.showinfo("Connexion rétablie", "La connexion à Odoo a été rétablie.")
                    except tk.TclError:
                        pass
                self.check_connection()
                return
        except Exception as e:
            print("Erreur lors de la reconnexion :", e)
        self.after(5000, self.try_reconnect)
        






##############################################################################
#                          Pages (Home, Company, Products, Orders)           #
##############################################################################
class HomePage(tk.Frame):
    """
    Tableau de bord d'entreprise.
    Affiche la date, l'utilisateur connecté, des KPI et une section Nouveautés.
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#10142c")
        self.app = app

        # Barre de titre avec la date
        title_frame = tk.Frame(self, bg="#10142c")
        title_frame.pack(fill="x", pady=10)
        tk.Label(title_frame, text="Tableau de bord d'entreprise",
                 bg="#10142c", fg="white", font=("Arial", 24, "bold")
        ).pack(side="left", padx=20)
        import datetime
        now = datetime.datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        tk.Label(title_frame, text=f"Aujourd'hui : {date_str}",
                 bg="#10142c", fg="white", font=("Arial", 14)
        ).pack(side="right", padx=20)

        # Infos sur l'utilisateur
        user_name = self.app.odoo.user or "Utilisateur"
        user_frame = tk.Frame(self, bg="#1b1f3b")
        user_frame.pack(fill="x", padx=20, pady=(0,10))
        tk.Label(user_frame, text=f"Connecté en tant que : {user_name}",
                 bg="#1b1f3b", fg="white", font=("Arial", 12, "bold")
        ).pack(side="left", padx=10, pady=10)

        # Section KPI
        kpi_frame = tk.Frame(self, bg="#10142c")
        kpi_frame.pack(fill="x", padx=20, pady=10)
        company_info = self.app.odoo.get_company_info()
        company_text = company_info.get("name", "Non disponible") if company_info else "Non disponible"
        self.create_kpi_card(kpi_frame, "Entreprise", company_text, "#eb53a2").pack(side="left", expand=True, fill="both", padx=5)
        order_count = self.app.odoo.get_sales_order_count()
        self.create_kpi_card(kpi_frame, "Commandes", f"{order_count}", "#ff9900").pack(side="left", expand=True, fill="both", padx=5)
        products = self.app.odoo.get_products()
        product_count = len(products)
        self.create_kpi_card(kpi_frame, "Produits", f"{product_count}", "#3aaed8").pack(side="left", expand=True, fill="both", padx=5)
        of_in_progress = self.app.odoo.get_manufacturing_orders(state_filter="progress")
        of_count = len(of_in_progress)
        self.create_kpi_card(kpi_frame, "OF en cours", f"{of_count}", "#9263f9").pack(side="left", expand=True, fill="both", padx=5)

        # Section Nouveautés
        nouveautes_frame = tk.Frame(self, bg="#10142c")
        nouveautes_frame.pack(fill="both", expand=True, padx=20, pady=(10,20))

        # Nouveautés : Nouvelles OF
        new_of_frame = tk.Frame(nouveautes_frame, bg="#1b1f3b")
        new_of_frame.pack(side="left", expand=True, fill="both", padx=10, pady=5)
        tk.Label(new_of_frame, text="Nouvelles OF", bg="#1b1f3b", fg="white",
                 font=("Arial", 14, "bold")).pack(pady=10)
        new_of = self.app.odoo.get_new_manufacturing_orders(limit=5)
        if new_of:
            for of in new_of:
                name_of = of.get("name", "N/A")
                create_date = of.get("create_date", "")[:10]
                tk.Label(new_of_frame, text=f"• {name_of} (Créé: {create_date})",
                         bg="#1b1f3b", fg="white", font=("Arial", 12)).pack(anchor="w", padx=10, pady=2)
        else:
            tk.Label(new_of_frame, text="Aucune nouvelle OF trouvée",
                     bg="#1b1f3b", fg="white", font=("Arial", 12)).pack(pady=10, padx=10)

        # Nouveautés : Nouvelles Commandes
        new_cmd_frame = tk.Frame(nouveautes_frame, bg="#1b1f3b")
        new_cmd_frame.pack(side="left", expand=True, fill="both", padx=10, pady=5)
        tk.Label(new_cmd_frame, text="Nouvelles Commandes", bg="#1b1f3b", fg="white",
                 font=("Arial", 14, "bold")).pack(pady=10)
        new_cmd = self.app.odoo.get_new_sales_orders(limit=5)
        if new_cmd:
            for order in new_cmd:
                order_name = order.get("name", "N/A")
                create_date = order.get("create_date", "")[:10]
                amount = order.get("amount_total", 0.0)
                tk.Label(new_cmd_frame, text=f"• {order_name} (Créé: {create_date}) - {amount} €",
                         bg="#1b1f3b", fg="white", font=("Arial", 12)).pack(anchor="w", padx=10, pady=2)
        else:
            tk.Label(new_cmd_frame, text="Aucune nouvelle commande trouvée",
                     bg="#1b1f3b", fg="white", font=("Arial", 12)).pack(pady=10, padx=10)

    def create_kpi_card(self, parent, title, value, color):
        frame = tk.Frame(parent, bg="#1b1f3b", width=200, height=80)
        frame.pack_propagate(False)
        tk.Label(frame, text=title, bg="#1b1f3b", fg="white",
                 font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(frame, text=value, bg="#1b1f3b", fg=color,
                 font=("Arial", 16, "bold")).pack()
        return frame


class CompanyPage(tk.Frame):
    """ F2 : Afficher la fiche Entreprise depuis Odoo, avec un logo fixe. """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#10142c")
        self.app = app

        tk.Label(self, text="Fiche Entreprise (F2)", bg="#10142c", fg="white",
                 font=("Arial", 18, "bold")).pack(pady=20)

        btn = tk.Button(self, text="Afficher Infos", bg="#3047ff", fg="white",
                        font=("Arial", 12, "bold"), command=self.show_company)
        btn.pack(pady=10)

        # Label pour afficher le logo
        self.logo_label = tk.Label(self, bg="#10142c")
        self.logo_label.pack(pady=10)

        # Zone de texte pour les informations de l'entreprise
        self.info_label = tk.Label(self, text="", bg="#10142c", fg="white",
                                   font=("Arial", 12), justify="left")
        self.info_label.pack(pady=10)

    def show_company(self):
        # Chargement du logo depuis un fichier fixe
        logo_path = "/home/user/erp/mon-projet-erp/DESKTOP_TKINTER/images/Logo BikeLab.jpg"
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                # Redimensionner le logo selon vos besoins (ici, 150x150 pixels)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(img)
                self.logo_label.config(image=logo_photo, text="")
                self.logo_label.image = logo_photo  # Conserver la référence
            except Exception as e:
                print("Erreur lors du chargement du logo fixe:", e)
                self.logo_label.config(text="Logo non disponible")
        else:
            self.logo_label.config(text="Logo introuvable")

        # Récupérer les informations de l'entreprise depuis Odoo
        info = self.app.odoo.get_company_info()
        if not info:
            messagebox.showwarning("Entreprise", "Impossible de récupérer la fiche entreprise.")
            return

        name = info.get('name', '')
        street = info.get('street', '')
        city = info.get('city', '')
        phone = info.get('phone', '')
        texte = f"Nom : {name}\nAdresse : {street}\nVille : {city}\nTéléphone : {phone}"
        self.info_label.config(text=texte)



class ProductsPage(tk.Frame):
    """ F3 : Afficher la liste des produits Odoo avec image et infos dans des 'tuiles'. """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#10142c")
        self.app = app
        tk.Label(self, text="Liste des Produits (F3)",
                 bg="#10142c", fg="white", font=("Arial", 18, "bold")).pack(pady=20)
        btn = tk.Button(self, text="Charger Produits", bg="#3047ff", fg="white",
                        font=("Arial", 12, "bold"), command=self.show_products)
        btn.pack(pady=10)
        container = tk.Frame(self, bg="#10142c")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        self.canvas = tk.Canvas(container, bg="#10142c", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#10142c")
        for col_index in range(3):
            self.scrollable_frame.grid_columnconfigure(col_index, weight=1, pad=10)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.product_images = []

    def show_products(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.product_images.clear()
        products = self.app.odoo.get_products()
        if not products:
            messagebox.showinfo("Produits", "Aucun produit trouvé.")
            return
        num_cols = 3
        for idx, prod in enumerate(products):
            name = prod.get("name", "N/A")
            price = prod.get("list_price", 0.0)
            categ_id = prod.get("categ_id", False)
            category_name = ""
            if isinstance(categ_id, list) and len(categ_id) == 2:
                category_name = categ_id[1]
            description = prod.get("description_sale", "")
            image_b64 = prod.get("image_1920", False)
            row = idx // num_cols
            col = idx % num_cols
            tile_frame = tk.Frame(self.scrollable_frame, bg="#1b1f3b", bd=2, relief="groove")
            tile_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            if image_b64:
                import base64
                from io import BytesIO
                image_data = base64.b64decode(image_b64)
                img_PIL = Image.open(BytesIO(image_data))
                img_PIL = img_PIL.resize((80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img_PIL)
            else:
                photo = None
            if photo:
                self.product_images.append(photo)
                img_label = tk.Label(tile_frame, image=photo, bg="#1b1f3b")
                img_label.pack(side="top", padx=10, pady=10)
            text_frame = tk.Frame(tile_frame, bg="#1b1f3b")
            text_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
            tk.Label(text_frame, text=f"Name: {name}",
                     bg="#1b1f3b", fg="white", font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(text_frame, text=f"Price: {price}",
                     bg="#1b1f3b", fg="white", font=("Arial", 12)).pack(anchor="w")
            tk.Label(text_frame, text=f"Category: {category_name}",
                     bg="#1b1f3b", fg="white", font=("Arial", 12)).pack(anchor="w")
            tk.Label(text_frame, text=f"Description: {description}",
                     bg="#1b1f3b", fg="white", font=("Arial", 12)).pack(anchor="w")


class OrdersPage(tk.Frame):
    """ F4 : Afficher la liste des Ordres de Fabrication filtrables par état et permettre le double-clic pour modifier. """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#10142c")
        self.app = app

        tk.Label(self, text="Liste OF (F4)", bg="#10142c", fg="white",
                 font=("Arial", 18, "bold")).pack(pady=20)

        filter_frame = tk.Frame(self, bg="#10142c")
        filter_frame.pack(pady=10)
        tk.Label(filter_frame, text="État OF :", bg="#10142c", fg="white",
                 font=("Arial", 12)).pack(side="left", padx=5)

        # Dictionnaire de correspondance pour le filtre (libellés en français)
        self.state_options = {
            "Tout": "all",
            "Confirmé": "confirmed",
            "En cours": "progress",
            "Fait": "done",
            "Annulé": "cancel"
        }
        self.selected_state = tk.StringVar()
        self.selected_state.set("Tout")
        state_menu = tk.OptionMenu(filter_frame, self.selected_state, *self.state_options.keys())
        state_menu.config(font=("Arial", 12))
        state_menu.pack(side="left", padx=5)

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

        # Dictionnaire pour traduire les codes d'état en libellés français
        self.state_labels = {
            "confirmed": "Confirmé",
            "progress": "En cours",
            "done": "Fait",
            "cancel": "Annulé"
        }

        # Lier le double-clic pour ouvrir la fenêtre de détails
        self.tree.bind("<Double-1>", self.on_double_click)

    def show_of(self):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)
            state_label = self.selected_state.get()
            state_value = self.state_options.get(state_label)
            orders = self.app.odoo.get_manufacturing_orders(state_filter=state_value)
            if not orders:
                messagebox.showinfo("OF", "Aucun ordre trouvé.")
                return
            for of in orders:
                name_of = of.get("name", "")
                qty = of.get("product_qty", 0.0)
                produced = of.get("qty_producing", 0.0)
                state_of = of.get("state", "")
                display_state = self.state_labels.get(state_of, state_of)
                self.tree.insert("", tk.END, values=(name_of, qty, produced, display_state))
        except Exception as e:
            messagebox.showerror("Erreur de connexion", "La connexion à Odoo a été interrompue.")
            self.app.try_reconnect()  

    def on_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])['values']
        mo_name = values[0]
        details = self.app.odoo.get_manufacturing_order_details_by_name(mo_name)
        if details:
            OrderDetailsWindow(self.app, details)
        else:
            messagebox.showerror("Erreur", "Détails non trouvés pour cette OF.")


class OrderDetailsWindow(tk.Toplevel):
    def __init__(self, app, order_details):
        super().__init__()
        self.app = app
        self.order_details = order_details
        self.title("Détails de l'OF")
        self.geometry("500x400")
        
        tk.Label(self, text=f"OF : {order_details.get('name', '')}",
                 font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self, text=f"Qté demandée : {order_details.get('product_qty', 0)}",
                 font=("Arial", 12)).pack(pady=5)
        tk.Label(self, text="Qté produite :", font=("Arial", 12)).pack(pady=5)
        
        self.qty_var = tk.StringVar(value=str(order_details.get("qty_producing", 0)))
        tk.Entry(self, textvariable=self.qty_var, font=("Arial", 12)).pack(pady=5)
        
        move_ids = order_details.get("move_raw_ids", [])
        if not move_ids:
            tk.Label(self, text="Aucun composant défini pour cet OF.",
                     font=("Arial", 12), fg="red").pack(pady=5)
        else:
            try:
                move_details = self.app.odoo.models.execute_kw(
                    self.app.odoo.db, self.app.odoo.uid, self.app.odoo.pwd,
                    'stock.move', 'read',
                    [move_ids],
                    {'fields': ['name', 'product_uom_qty', 'quantity_done']}
                )
                tk.Label(self, text="Composants :", font=("Arial", 12, "bold")).pack(pady=5)
                for move in move_details:
                    name = move.get("name", "N/A")
                    qty_needed = move.get("product_uom_qty", 0)
                    qty_done = move.get("quantity_done", 0)
                    tk.Label(self, text=f"- {name}: {qty_done} / {qty_needed}",
                             font=("Arial", 12)).pack(anchor="w", padx=20, pady=2)
            except Exception as e:
                tk.Label(self, text="Erreur lors de la récupération des composants.",
                         font=("Arial", 12), fg="red").pack(pady=5)
                print("Erreur get_move_details:", e)
        
        tk.Button(self, text="Valider la commande", font=("Arial", 12, "bold"),
                  bg="#3047ff", fg="white", command=self.validate_order).pack(pady=20)
    
    def validate_order(self):
        try:
            new_qty = float(self.qty_var.get())
        except ValueError:
            messagebox.showerror("Erreur", "Quantité invalide.")
            return
        mo_name = self.order_details.get("name", "")
        ok = self.app.odoo.update_mo_quantity_by_name(mo_name, new_qty)
        if ok:
            messagebox.showinfo("Succès", f"OF '{mo_name}' mise à jour.")
            self.destroy()
        else:
            messagebox.showerror("Erreur", f"Impossible de mettre à jour l'OF '{mo_name}'.")



##############################################################################
#                           Point d'entrée (main)                            #
##############################################################################
def main():
    try:
        root = tk.Tk()
        LoginPage(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("Interruption par l'utilisateur.")
        # Ici, vous pouvez effectuer des opérations de nettoyage si nécessaire.

if __name__ == '__main__':
    main()


