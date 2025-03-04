#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
from odoo_interface import IF_Odoo

class DashboardApp(tk.Tk):
    """
    A modern 'dashboard'-style main window that replaces the old menubar approach.
    """

    def __init__(self, odoo_conn):
        super().__init__()
        self.odoo = odoo_conn
        self.title("ERP Odoo - Production Dashboard")
        self.geometry("1200x800")
        self.configure(bg="#2A2D2E")  # Dark-ish background

        # Path to images
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir    = os.path.join(script_dir, "images")

        # Try loading a background image for the main area (optional)
        self.bg_image = None
        bg_path = os.path.join(img_dir, "background1.png")
        if os.path.exists(bg_path):
            self.bg_image = Image.open(bg_path)
            self.bg_image = self.bg_image.resize((1200, 800), Image.ANTIALIAS)
            self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
            bg_label = tk.Label(self, image=self.bg_image_tk)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a frame for the sidebar
        self.sidebar_frame = tk.Frame(self, bg="#1F2122", width=200)
        self.sidebar_frame.pack(side="left", fill="y")

        # Create a frame for the main content
        self.content_frame = tk.Frame(self, bg="#2A2D2E")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Status bar at bottom
        self.status_label = tk.Label(
            self, text="Connecté à Odoo",
            bg="#444", fg="white", anchor="w"
        )
        self.status_label.pack(side="bottom", fill="x")

        # We will create sub-frames (pages) for F2, F3, F4, F5
        self.frames = {}
        for PageClass in (CompanyPage, ProductsPage, OrdersPage, UpdateQtyPage, HomePage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.content_frame, app=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the "Home" page by default
        self.show_frame("HomePage")

        # Buttons on the sidebar
        self.create_sidebar_buttons()

    def create_sidebar_buttons(self):
        """
        Put big buttons or icons in the sidebar to switch between the pages.
        """
        # Optional: load icons for the buttons if you have them
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir    = os.path.join(script_dir, "images")

        # Example of loading an icon:
        def load_icon(name, size=(24,24)):
            path = os.path.join(img_dir, name)
            if os.path.exists(path):
                img = Image.open(path).resize(size, Image.ANTIALIAS)
                return ImageTk.PhotoImage(img)
            return None

        company_icon = load_icon("fiche entreprise.png") or None
        products_icon = load_icon("liste produits.png") or None
        orders_icon = load_icon("Ordres de Fabrication.png") or None
        qty_icon = load_icon("modification de la quantité produite.png") or None

        # A "home" button (if desired)
        home_btn = tk.Button(
            self.sidebar_frame, text="Accueil", image="", compound="left",
            bg="#1F2122", fg="white", font=("Arial", 14, "bold"),
            bd=0, padx=10, pady=20, anchor="w",
            command=lambda: self.show_frame("HomePage")
        )
        home_btn.pack(fill="x")

        # F2 : Company Info
        comp_btn = tk.Button(
            self.sidebar_frame, text="Entreprise", image=company_icon, compound="left",
            bg="#1F2122", fg="white", font=("Arial", 14, "bold"),
            bd=0, padx=10, pady=20, anchor="w",
            command=lambda: self.show_frame("CompanyPage")
        )
        comp_btn.pack(fill="x")
        comp_btn._icon = company_icon  # keep reference

        # F3 : Products
        prod_btn = tk.Button(
            self.sidebar_frame, text="Produits", image=products_icon, compound="left",
            bg="#1F2122", fg="white", font=("Arial", 14, "bold"),
            bd=0, padx=10, pady=20, anchor="w",
            command=lambda: self.show_frame("ProductsPage")
        )
        prod_btn.pack(fill="x")
        prod_btn._icon = products_icon

        # F4 : Orders
        orders_btn = tk.Button(
            self.sidebar_frame, text="Ordres Fab", image=orders_icon, compound="left",
            bg="#1F2122", fg="white", font=("Arial", 14, "bold"),
            bd=0, padx=10, pady=20, anchor="w",
            command=lambda: self.show_frame("OrdersPage")
        )
        orders_btn.pack(fill="x")
        orders_btn._icon = orders_icon

        # F5 : Update QTY
        qty_btn = tk.Button(
            self.sidebar_frame, text="Modifier Qte", image=qty_icon, compound="left",
            bg="#1F2122", fg="white", font=("Arial", 14, "bold"),
            bd=0, padx=10, pady=20, anchor="w",
            command=lambda: self.show_frame("UpdateQtyPage")
        )
        qty_btn.pack(fill="x")
        qty_btn._icon = qty_icon

    def show_frame(self, page_name):
        """
        Show the frame (page) with the given class name.
        """
        frame = self.frames[page_name]
        frame.tkraise()


class HomePage(tk.Frame):
    """
    A simple "home" dashboard page (optional).
    You can place any welcome text, KPIs, or charts here.
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#2A2D2E")
        self.app = app
        label = tk.Label(self, text="Bienvenue sur votre Dashboard Odoo!",
                         bg="#2A2D2E", fg="white", font=("Arial", 20, "bold"))
        label.pack(pady=40)

        # Example placeholders for charts or stats
        tk.Label(self, text="Ici, vous pouvez afficher des KPI ou graphiques…",
                 bg="#2A2D2E", fg="white", font=("Arial", 14)).pack(pady=10)


class CompanyPage(tk.Frame):
    """
    Corresponds to F2: Show Company Info in a styled frame.
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#2A2D2E")
        self.app = app

        title = tk.Label(self, text="Fiche Entreprise (F2)",
                         bg="#2A2D2E", fg="white", font=("Arial", 18, "bold"))
        title.pack(pady=20)

        # A button to fetch & display the info
        btn = tk.Button(self, text="Afficher Infos",
                        command=self.show_company,
                        bg="#3047ff", fg="white", font=("Arial", 12, "bold"))
        btn.pack(pady=10)

        # A Text or Label widget to display the company data
        self.info_label = tk.Label(self, text="", bg="#2A2D2E", fg="white",
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
    """
    Corresponds to F3: Show the list of Products in a Treeview, with images if you want.
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#2A2D2E")
        self.app = app

        title = tk.Label(self, text="Liste des Produits (F3)",
                         bg="#2A2D2E", fg="white", font=("Arial", 18, "bold"))
        title.pack(pady=20)

        # Button to load product data
        btn = tk.Button(self, text="Charger Produits",
                        command=self.show_products,
                        bg="#3047ff", fg="white", font=("Arial", 12, "bold"))
        btn.pack(pady=10)

        # Create a frame to hold the Treeview
        tree_frame = tk.Frame(self, bg="#2A2D2E")
        tree_frame.pack(fill="both", expand=True, pady=10, padx=20)

        columns = ("name", "price")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        self.tree.heading("name", text="Nom du Produit")
        self.tree.heading("price", text="Prix")
        self.tree.column("name", width=400)
        self.tree.column("price", width=100)
        self.tree.pack(fill="both", expand=True)

    def show_products(self):
        # Clear old data
        for row in self.tree.get_children():
            self.tree.delete(row)

        products = self.app.odoo.get_products()
        if not products:
            messagebox.showinfo("Produits", "Aucun produit trouvé.")
            return

        for prod in products:
            name  = prod.get("name", "")
            price = prod.get("list_price", 0.0)
            self.tree.insert("", tk.END, values=(name, price))


class OrdersPage(tk.Frame):
    """
    Corresponds to F4: List of Manufacturing Orders with optional state filter.
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#2A2D2E")
        self.app = app

        title = tk.Label(self, text="Liste OF (F4)",
                         bg="#2A2D2E", fg="white", font=("Arial", 18, "bold"))
        title.pack(pady=20)

        # Button to load orders (possibly with a simple filter)
        btn_frame = tk.Frame(self, bg="#2A2D2E")
        btn_frame.pack()

        self.filter_var = tk.StringVar()
        filter_label = tk.Label(btn_frame, text="État OF:", bg="#2A2D2E", fg="white")
        filter_label.pack(side="left", padx=5)
        filter_entry = tk.Entry(btn_frame, textvariable=self.filter_var)
        filter_entry.pack(side="left", padx=5)

        load_btn = tk.Button(btn_frame, text="Charger OF",
                             command=self.show_of, bg="#3047ff", fg="white")
        load_btn.pack(side="left", padx=5)

        # Treeview
        tree_frame = tk.Frame(self, bg="#2A2D2E")
        tree_frame.pack(fill="both", expand=True, pady=10, padx=20)

        columns = ("name", "qty", "produced", "state")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        self.tree.heading("name", text="Nom OF")
        self.tree.heading("qty", text="Qté Demandée")
        self.tree.heading("produced", text="Qté Produite")
        self.tree.heading("state", text="État")
        self.tree.column("name", width=200)
        self.tree.column("qty", width=100)
        self.tree.column("produced", width=100)
        self.tree.column("state", width=100)
        self.tree.pack(fill="both", expand=True)

    def show_of(self):
        # Clear old data
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
    """
    Corresponds to F5: Update the produced qty for an MO.
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg="#2A2D2E")
        self.app = app

        title = tk.Label(self, text="Modifier Qté Produite (F5)",
                         bg="#2A2D2E", fg="white", font=("Arial", 18, "bold"))
        title.pack(pady=20)

        # Fields
        form_frame = tk.Frame(self, bg="#2A2D2E")
        form_frame.pack(pady=40)

        tk.Label(form_frame, text="ID de l'OF:", bg="#2A2D2E", fg="white",
                 font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.mo_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.mo_id_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Nouvelle quantité:", bg="#2A2D2E", fg="white",
                 font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.qty_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.qty_var).grid(row=1, column=1, padx=5, pady=5)

        # Button
        update_btn = tk.Button(
            self, text="Mettre à jour",
            bg="#3047ff", fg="white", font=("Arial", 12, "bold"),
            command=self.update_of_qty
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
#                           Écran de Login (F1)                              #
##############################################################################
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1166x718")
        self.root.resizable(0, 0)
        self.root.title("Login Page")

        # Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # PARAMETRES ODOO
        # Ajustez ici selon votre serveur/bdd
        self.host = "172.31.10.137"
        self.port = "8027"
        self.db   = "demo"

        # Exemples de chemins d'images (à adapter si besoin)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir    = os.path.join(script_dir, "images")

        bg_path        = os.path.join(img_dir, "background1.png")
        vector_path    = os.path.join(img_dir, "vector.png")
        hyy_path       = os.path.join(img_dir, "hyy.png")
        user_ico       = os.path.join(img_dir, "username_icon.png")
        pass_ico       = os.path.join(img_dir, "password_icon.png")
        show_img_path  = os.path.join(img_dir, "show.png")
        hide_img_path  = os.path.join(img_dir, "hide.png")
        btn1_path      = os.path.join(img_dir, "btn1.png")

        # Fond
        try:
            bg = Image.open(bg_path)
            bg_photo = ImageTk.PhotoImage(bg)
            label_bg = tk.Label(self.root, image=bg_photo)
            label_bg.image = bg_photo
            label_bg.pack(fill="both", expand=True)
        except:
            # Au cas où l'image ne serait pas trouvée
            self.root.configure(bg="white")

        # Frame
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

        # Image gauche
        try:
            vect = Image.open(vector_path)
            vect_photo = ImageTk.PhotoImage(vect)
            tk.Label(self.lgn_frame, image=vect_photo, bg="#040405").place(x=5, y=100)
            self._vect_photo = vect_photo
        except:
            pass

        # Sign In image
        try:
            hyy = Image.open(hyy_path)
            hyy_photo = ImageTk.PhotoImage(hyy)
            tk.Label(self.lgn_frame, image=hyy_photo, bg="#040405").place(x=620, y=130)
            self._hyy_photo = hyy_photo
        except:
            pass

        # Label Sign In
        tk.Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white",
                 font=("yu gothic ui", 17, "bold")).place(x=650, y=240)

        # Username
        tk.Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                 font=("yu gothic ui", 13, "bold")).place(x=550, y=300)

        self.username_entry = tk.Entry(
            self.lgn_frame,
            textvariable=self.username_var,
            highlightthickness=0,
            relief=tk.FLAT,
            bg="#040405",
            fg="#6b6a69",
            font=("yu gothic ui", 12, "bold"),
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

        # Password
        tk.Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                 font=("yu gothic ui", 13, "bold")).place(x=550, y=380)

        self.password_entry = tk.Entry(
            self.lgn_frame,
            textvariable=self.password_var,
            highlightthickness=0,
            relief=tk.FLAT,
            bg="#040405",
            fg="#6b6a69",
            font=("yu gothic ui", 12, "bold"),
            show="*",
            insertbackground="#6b6a69"
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

        # Show/Hide
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

        # Bouton Login
        try:
            btn1 = Image.open(btn1_path)
            btn1_photo = ImageTk.PhotoImage(btn1)
            btn1_label = tk.Label(self.lgn_frame, image=btn1_photo, bg="#040405")
            btn1_label.image = btn1_photo
            btn1_label.place(x=550, y=450)

            self.login_btn = tk.Button(
                btn1_label,
                text='LOGIN',
                font=("yu gothic ui", 13, "bold"),
                width=20,
                bd=0,
                highlightthickness=0,
                relief='flat',
                fg='white',
                bg='#3047ff',
                activebackground='#3047ff',
                command=self.login_action
            )
            self.login_btn.place(x=20, y=10)
            self._btn1_photo = btn1_photo
        except:
            # fallback si pas d'image
            self.login_btn = tk.Button(
                self.lgn_frame,
                text='LOGIN',
                font=("yu gothic ui", 13, "bold"),
                width=20,
                command=self.login_action
            )
            self.login_btn.place(x=600, y=460)

    def login_action(self):
        """Méthode de connexion Odoo (F1)."""
        username = self.username_var.get()
        password = self.password_var.get()

        # Instancier l'interface Odoo
        self.odoo_conn = IF_Odoo(self.host, self.port, self.db, username, password)
        success = self.odoo_conn.connect()
        if success:
            # Fermer la fenêtre de login
            self.root.destroy()
            # Ouvrir la fenêtre principale F2-F5
            app = DashboardApp(self.odoo_conn)
            app.mainloop()

        else:
            messagebox.showerror("Erreur", "Impossible de se connecter à Odoo.")

    def show_pwd(self):
        # Affiche MDP en clair
        self.hide_button = tk.Button(
            self.lgn_frame,
            image=self.hide_img,
            command=self.hide_pwd,
            relief=tk.FLAT,
            activebackground="white",
            borderwidth=0,
            background="white",
            cursor="hand2"
        )
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide_pwd(self):
        # Re-masque MDP
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
        self.password_entry.config(show='*')


##############################################################################
#                            Point d'entrée main()                            #
##############################################################################
def main():
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()

if __name__ == '__main__':
    main()
