#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from odoo_interface import IF_Odoo

class App(tk.Tk):
    def __init__(self, odoo_interface):
        super().__init__()
        self.title("ERP Odoo - Opérateur Production")
        self.geometry("900x600")

        self.odoo = odoo_interface
        self.connected = False

        # Barre de menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Menu Connexion (F1)
        menu_conn = tk.Menu(menubar, tearoff=0)
        menu_conn.add_command(label="Se connecter (F1)", command=self.f1_connect)
        menubar.add_cascade(label="Connexion", menu=menu_conn)

        # Menu Entreprise (F2)
        menu_company = tk.Menu(menubar, tearoff=0)
        menu_company.add_command(label="Voir fiche entreprise (F2)", command=self.f2_show_company)
        menubar.add_cascade(label="Entreprise", menu=menu_company)

        # Menu Produits (F3)
        menu_product = tk.Menu(menubar, tearoff=0)
        menu_product.add_command(label="Liste des produits (F3)", command=self.f3_show_products)
        menubar.add_cascade(label="Produits", menu=menu_product)

        # Menu OF (F4 & F5)
        menu_of = tk.Menu(menubar, tearoff=0)
        menu_of.add_command(label="Liste des OF (F4)", command=self.f4_show_of)
        menu_of.add_command(label="Modifier qty produite (F5)", command=self.f5_update_mo_qty)
        menubar.add_cascade(label="Ordres Fabrication", menu=menu_of)

        # Cadre principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Label de statut en bas
        self.status_label = ttk.Label(self, text="Statut : non connecté", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    # F1 : Connexion
    def f1_connect(self):
        if self.odoo.connect():
            self.connected = True
            messagebox.showinfo("Connexion", f"Connecté à Odoo (version: {self.odoo.odoo_version})")
            self.status_label.config(text=f"Statut : Connecté à Odoo v{self.odoo.odoo_version}")
        else:
            self.connected = False
            messagebox.showerror("Erreur", "Échec de la connexion à Odoo")
            self.status_label.config(text="Statut : non connecté")

    # F2 : Fiche entreprise
    def f2_show_company(self):
        if not self.connected:
            messagebox.showwarning("Attention", "Veuillez d'abord vous connecter (F1).")
            return
        company = self.odoo.get_company_info()
        if company:
            info = f"Nom: {company.get('name', '')}\n" \
                   f"Adresse: {company.get('street', '')}\n" \
                   f"Ville: {company.get('city', '')}\n" \
                   f"Téléphone: {company.get('phone', '')}"
            messagebox.showinfo("Fiche Entreprise", info)
        else:
            messagebox.showerror("Erreur", "Impossible de récupérer la fiche entreprise.")

    # F3 : Liste des produits
    def f3_show_products(self):
        if not self.connected:
            messagebox.showwarning("Attention", "Veuillez d'abord vous connecter (F1).")
            return
        products = self.odoo.get_products()
        if not products:
            messagebox.showinfo("Info", "Aucun produit trouvé.")
            return

        # On vide le main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        lbl = ttk.Label(self.main_frame, text="Liste des produits (F3)", font=("Arial", 16))
        lbl.pack(pady=10)

        # Affichage sous forme de tableau
        tree = ttk.Treeview(self.main_frame, columns=("price", "img"), show="headings", height=15)
        tree.heading("price", text="Prix")
        tree.heading("img", text="Image (aperçu)")
        tree.column("price", width=100)
        tree.column("img", width=200)
        tree.pack(fill=tk.BOTH, expand=True)

        for prod in products:
            name = prod.get("name", "")
            price = prod.get("list_price", 0.0)
            tree.insert("", tk.END, values=(price, f"{name}"))

        # Si on voulait afficher des images, on pourrait stocker PhotoImage dans un dictionnaire,
        # puis sur clic, ouvrir une nouvelle fenêtre avec l'image décodée.

    # F4 : Liste OF
    def f4_show_of(self):
        if not self.connected:
            messagebox.showwarning("Attention", "Veuillez d'abord vous connecter (F1).")
            return

        # On demande éventuellement un état
        state = self.ask_of_state()
        orders = self.odoo.get_manufacturing_orders(state_filter=state)

        # On vide le main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        lbl = ttk.Label(self.main_frame, text="Liste des Ordres de Fabrication (F4)", font=("Arial", 16))
        lbl.pack(pady=10)

        tree = ttk.Treeview(self.main_frame, columns=("product", "qty", "producing", "state"), show="headings", height=15)
        tree.heading("product", text="Produit")
        tree.heading("qty", text="Qté demandée")
        tree.heading("producing", text="Qté produite")
        tree.heading("state", text="État")
        tree.column("product", width=150)
        tree.column("qty", width=100)
        tree.column("producing", width=100)
        tree.column("state", width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        for of in orders:
            name_of = of.get("name", "")
            product_id = of.get("product_id", ["", ""])[1]  # le deuxième élément du champ Many2one
            qty = of.get("product_qty", 0.0)
            producing = of.get("qty_producing", 0.0)
            state_of = of.get("state", "")
            tree.insert("", tk.END, values=(product_id, qty, producing, state_of))

    # F5 : Modifier la quantité produite d’un OF
    def f5_update_mo_qty(self):
        if not self.connected:
            messagebox.showwarning("Attention", "Veuillez d'abord vous connecter (F1).")
            return

        # Demande l'ID de l'OF
        mo_id_str = tk.simpledialog.askstring("Modifier OF", "Entrez l'ID de l'OF :")
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
            messagebox.showinfo("Succès", f"Quantité produite mise à jour pour l'OF {mo_id}.")
        else:
            messagebox.showerror("Erreur", f"Impossible de mettre à jour l'OF {mo_id}.")

        # (Optionnel) Si vous voulez passer l'OF à 'done' quand la qty produite atteint la qty demandée,
        # vous pouvez appeler self.odoo.set_mo_done(mo_id) selon la logique.

    def ask_of_state(self):
        """
        Petite boîte de dialogue pour demander l'état (confirmed, progress, done, cancel).
        """
        state = tk.simpledialog.askstring("Filtrer OF", "État de l'OF (confirmed, progress, done, cancel) ?\nLaisser vide pour tous.")
        return state

if __name__ == "__main__":
    # Exemple de configuration Odoo
    # Adaptez host, port, db, user, pwd à votre environnement
    odoo_interface = IF_Odoo(
        host="172.31.10.137",
        port="8027",
        db="postgres",
        user="odoo",
        pwd="myodoo"
    )

    app = App(odoo_interface)
    app.mainloop()
