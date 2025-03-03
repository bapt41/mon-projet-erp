#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import xmlrpc.client


##############################################################################
#                           IF_Odoo (API Odoo)                               #
##############################################################################
class IF_Odoo:
    def __init__(self, host, port, db, user, pwd):
        self.host = host
        self.port = port
        self.db   = db
        self.user = user
        self.pwd  = pwd
        self.uid  = None
        self.models = None

    def connect(self):
        """Connexion via XML-RPC. Retourne True si OK, False sinon."""
        try:
            url = f"http://{self.host}:{self.port}"
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            self.uid = common.authenticate(self.db, self.user, self.pwd, {})
            if not self.uid:
                return False
            self.models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
            return True
        except:
            return False

    # F2 : fiche de l’entreprise
    def get_company_info(self):
        if not self.models:
            return {}
        comps = self.models.execute_kw(
            self.db, self.uid, self.pwd,
            'res.company', 'search_read',
            [[]],
            {'fields': ['name', 'street', 'city', 'phone'], 'limit': 1}
        )
        return comps[0] if comps else {}

    # F3 : liste des produits
    def get_products(self):
        if not self.models:
            return []
        products = self.models.execute_kw(
            self.db, self.uid, self.pwd,
            'product.template', 'search_read',
            [[]],
            {'fields': ['name', 'list_price', 'image_1920'], 'limit': 50}
        )
        return products

    # F4 : liste des OF
    def get_manufacturing_orders(self, state_filter=None):
        if not self.models:
            return []
        domain = []
        if state_filter:
            domain = [('state', '=', state_filter)]
        orders = self.models.execute_kw(
            self.db, self.uid, self.pwd,
            'mrp.production', 'search_read',
            [domain],
            {'fields': ['name', 'product_qty', 'qty_producing', 'state'], 'limit': 50}
        )
        return orders

    # F5 : modifier la quantité produite
    def update_mo_quantity(self, mo_id, new_qty):
        if not self.models:
            return False
        try:
            result = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'mrp.production', 'write',
                [[mo_id], {'qty_producing': new_qty}]
            )
            return result
        except:
            return False


##############################################################################
#                           Fenêtre Principale (F2-F5)                       #
##############################################################################
class MainApp(tk.Tk):
    def __init__(self, odoo_conn):
        super().__init__()
        self.odoo = odoo_conn
        self.title("ERP Odoo - Production")
        self.geometry("1200x800")

        # Barre de menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # F2
        menu_f2 = tk.Menu(menubar, tearoff=0)
        menu_f2.add_command(label="Voir fiche entreprise (F2)", command=self.show_company)
        menubar.add_cascade(label="Entreprise", menu=menu_f2)

        # F3
        menu_f3 = tk.Menu(menubar, tearoff=0)
        menu_f3.add_command(label="Liste des produits (F3)", command=self.show_products)
        menubar.add_cascade(label="Produits", menu=menu_f3)

        # F4
        menu_f4 = tk.Menu(menubar, tearoff=0)
        menu_f4.add_command(label="Liste OF (F4)", command=self.show_of)
        menubar.add_cascade(label="OF", menu=menu_f4)

        # F5
        menu_f5 = tk.Menu(menubar, tearoff=0)
        menu_f5.add_command(label="Modifier qty (F5)", command=self.update_of_qty)
        menubar.add_cascade(label="Production", menu=menu_f5)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Label de statut
        self.status_label = tk.Label(self, text="Connecté à Odoo", bg="#ccc", anchor="w")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    # F2 : Fiche Entreprise
    def show_company(self):
        info = self.odoo.get_company_info()
        if not info:
            messagebox.showwarning("Entreprise", "Impossible de récupérer la fiche entreprise.")
            return
        name   = info.get('name', '')
        street = info.get('street', '')
        city   = info.get('city', '')
        phone  = info.get('phone', '')
        texte = f"Nom : {name}\nAdresse : {street}\nVille : {city}\nTéléphone : {phone}"
        messagebox.showinfo("Entreprise", texte)

    # F3 : Produits
    def show_products(self):
        products = self.odoo.get_products()
        if not products:
            messagebox.showinfo("Produits", "Aucun produit trouvé.")
            return

        # On vide le main_frame
        for w in self.main_frame.winfo_children():
            w.destroy()

        title = tk.Label(self.main_frame, text="Liste des Produits (F3)", font=("Arial", 16))
        title.pack(pady=10)

        columns = ("name", "price")
        tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=20)
        tree.heading("name", text="Nom du Produit")
        tree.heading("price", text="Prix")
        tree.column("name", width=400)
        tree.column("price", width=100)
        tree.pack(fill="both", expand=True)

        for prod in products:
            name  = prod.get("name", "")
            price = prod.get("list_price", 0.0)
            tree.insert("", tk.END, values=(name, price))

    # F4 : Ordres de Fab
    def show_of(self):
        state = tk.simpledialog.askstring("Filtrer", "État OF (confirmed, progress, done, cancel) ou vide :")
        if state:
            orders = self.odoo.get_manufacturing_orders(state_filter=state)
        else:
            orders = self.odoo.get_manufacturing_orders()

        if not orders:
            messagebox.showinfo("OF", "Aucun ordre trouvé.")
            return

        for w in self.main_frame.winfo_children():
            w.destroy()

        title = tk.Label(self.main_frame, text="Liste OF (F4)", font=("Arial", 16))
        title.pack(pady=10)

        columns = ("name", "qty", "produced", "state")
        tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=20)
        tree.heading("name", text="Nom OF")
        tree.heading("qty", text="Qté Demandée")
        tree.heading("produced", text="Qté Produite")
        tree.heading("state", text="État")
        tree.column("name", width=200)
        tree.column("qty", width=100)
        tree.column("produced", width=100)
        tree.column("state", width=100)
        tree.pack(fill="both", expand=True)

        for of in orders:
            name_of   = of.get("name", "")
            qty       = of.get("product_qty", 0.0)
            produced  = of.get("qty_producing", 0.0)
            state_of  = of.get("state", "")
            tree.insert("", tk.END, values=(name_of, qty, produced, state_of))

    # F5 : Modifier qty produite
    def update_of_qty(self):
        mo_id_str = tk.simpledialog.askstring("Modifier OF", "ID de l'OF :")
        if not mo_id_str:
            return
        try:
            mo_id = int(mo_id_str)
        except ValueError:
            messagebox.showerror("Erreur", "ID invalide.")
            return

        new_qty_str = tk.simpledialog.askstring("Modifier OF", "Nouvelle quantité produite :")
        if not new_qty_str:
            return
        try:
            new_qty = float(new_qty_str)
        except ValueError:
            messagebox.showerror("Erreur", "Quantité invalide.")
            return

        ok = self.odoo.update_mo_quantity(mo_id, new_qty)
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

        # Chemins images
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(script_dir, "images")

        bg_path = os.path.join(img_dir, "background1.png")
        vector_path = os.path.join(img_dir, "vector.png")
        hyy_path = os.path.join(img_dir, "hyy.png")
        user_ico = os.path.join(img_dir, "username_icon.png")
        pass_ico = os.path.join(img_dir, "password_icon.png")
        show_img_path = os.path.join(img_dir, "show.png")
        hide_img_path = os.path.join(img_dir, "hide.png")
        btn1_path = os.path.join(img_dir, "btn1.png")

        # Fond
        bg = Image.open(bg_path)
        bg_photo = ImageTk.PhotoImage(bg)
        label_bg = tk.Label(self.root, image=bg_photo)
        label_bg.image = bg_photo
        label_bg.pack(fill="both", expand=True)

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
        vect = Image.open(vector_path)
        vect_photo = ImageTk.PhotoImage(vect)
        tk.Label(self.lgn_frame, image=vect_photo, bg="#040405").place(x=5, y=100)
        self._vect_photo = vect_photo

        # Sign In image
        hyy = Image.open(hyy_path)
        hyy_photo = ImageTk.PhotoImage(hyy)
        tk.Label(self.lgn_frame, image=hyy_photo, bg="#040405").place(x=620, y=130)
        self._hyy_photo = hyy_photo

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

        user_img = Image.open(user_ico)
        user_img_photo = ImageTk.PhotoImage(user_img)
        tk.Label(self.lgn_frame, image=user_img_photo, bg="#040405").place(x=550, y=332)
        self._user_img_photo = user_img_photo

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

        pass_img = Image.open(pass_ico)
        pass_img_photo = ImageTk.PhotoImage(pass_img)
        tk.Label(self.lgn_frame, image=pass_img_photo, bg="#040405").place(x=550, y=414)
        self._pass_img_photo = pass_img_photo

        # Show/Hide
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

        # Bouton Login
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

    def login_action(self):
        """Méthode de connexion Odoo (F1)."""
        username = self.username_var.get()
        password = self.password_var.get()

        # Paramètres Odoo (à adapter)
        host = "172.31.10.137"
        port = "8027"
        db   = "demo"

        # Instancier IF_Odoo
        self.odoo_conn = IF_Odoo(host, port, db, username, password)
        success = self.odoo_conn.connect()
        if success:
            # Fermer la fenêtre de login
            self.root.destroy()
            # Ouvrir la fenêtre principale F2-F5
            app = MainApp(self.odoo_conn)
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
