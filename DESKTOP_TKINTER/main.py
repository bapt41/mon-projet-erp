
#!/usr/bin/env python3
"""
Application Desktop ERP avec Tkinter.

Cette application permet de :
- Se connecter à un serveur Odoo via l'interface IF_Odoo.
- Afficher et mettre à jour la quantité produite d'un ordre de fabrication.
- Charger et afficher l'image d'un produit.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt
from PIL import Image, ImageTk
from odoo_interface import IF_Odoo

class App(tk.Tk):
    def __init__(self, odoo_interface):
        super().__init__()
        self.title("ERP Desktop Application")
        self.geometry("800x600")
        self.odoo = odoo_interface
        self.create_widgets()
        self.update_status()  # Lance la mise à jour périodique de la barre de status

    def create_widgets(self):
        # Cadre pour la connexion et les contrôles Odoo
        self.frmOdoo = ttk.Frame(self)
        self.frmOdoo.pack(padx=10, pady=10, fill=tk.X)

        # Bouton de connexion
        self.btnConnect = ttk.Button(self.frmOdoo, text="Connect to Odoo", command=self.on_connect)
        self.btnConnect.pack(side=tk.LEFT, padx=5)

        # Spinbox pour sélectionner l'ID d'un ordre de fabrication
        self.lblMo = ttk.Label(self.frmOdoo, text="MO ID:")
        self.lblMo.pack(side=tk.LEFT, padx=5)
        self.sbxMoId = ttk.Spinbox(self.frmOdoo, from_=1, to=100)
        self.sbxMoId.set(1)
        self.sbxMoId.pack(side=tk.LEFT, padx=5)

        # Bouton pour augmenter la production
        self.btnProducing = ttk.Button(self.frmOdoo, text="Produce", command=self.on_producing)
        self.btnProducing.pack(side=tk.LEFT, padx=5)

        # Bouton pour charger et afficher l'image d'un produit (exemple : produit avec id 1)
        self.btnLoadImage = ttk.Button(self.frmOdoo, text="Load Product Image", command=self.on_load_image)
        self.btnLoadImage.pack(side=tk.LEFT, padx=5)

        # Barre de status en bas de la fenêtre
        self.lblStatus = ttk.Label(self, text="Status: Not connected", relief=tk.SUNKEN, anchor=tk.W)
        self.lblStatus.pack(side=tk.BOTTOM, fill=tk.X)

        # Zone d'affichage de l'image du produit
        self.lblImage = ttk.Label(self)
        self.lblImage.pack(pady=10)

    def on_connect(self):
        # Tentative de connexion à Odoo
        self.lblStatus.config(text="Connecting to Odoo...")
        self.update()  # Rafraîchit l'interface
        if self.odoo.connect():
            messagebox.showinfo("Connection", f"Connected to Odoo version {self.odoo.odoo_version}")
            self.lblStatus.config(text=f"Connected to Odoo version {self.odoo.odoo_version}")
        else:
            messagebox.showerror("Connection Error", "Failed to connect to Odoo")
            self.lblStatus.config(text="Connection failed.")

    def on_producing(self):
        # Récupère l'ID de l'ordre de fabrication depuis la spinbox
        mo_id = self.sbxMoId.get()
        try:
            mo_id_int = int(mo_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid MO ID")
            return

        qty_product = self.odoo.get_manuf_order_qty_to_product(mo_id_int)
        qty_producing = self.odoo.get_manuf_order_qty_producing(mo_id_int)

        if qty_product == -1 or qty_producing == -1:
            messagebox.showerror("Error", "Manufacturing order not found")
            return

        if qty_producing < qty_product:
            new_qty = qty_producing + 1
            if self.odoo.set_manuf_order_qty_producing(mo_id_int, new_qty):
                self.lblStatus.config(text=f"MO {mo_id_int}: Producing Qty updated to {new_qty} / {qty_product}")
            else:
                messagebox.showerror("Error", "Failed to update producing quantity")
        else:
            messagebox.showinfo("Info", "Production already complete for this order.")

    def on_load_image(self):
        # Exemple : charger l'image du produit avec id 1
        product_id = 1
        image_filename = "product_1.png"
        if self.odoo.save_product_image(product_id, image_filename):
            try:
                img = Image.open(image_filename)
                img = img.resize((200, 200))
                photo = ImageTk.PhotoImage(img)
                self.lblImage.config(image=photo)
                self.lblImage.image = photo  # Conserver la référence
                self.lblStatus.config(text="Product image loaded successfully.")
            except Exception as e:
                messagebox.showerror("Image Error", f"Error displaying image: {e}")
        else:
            messagebox.showerror("Image Error", "Failed to load product image.")

    def update_status(self):
        # Mise à jour périodique de la barre de status avec l'heure et la version d'Odoo
        now = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        version = self.odoo.odoo_version if self.odoo.odoo_version else "Not connected"
        self.lblStatus.config(text=f"{now} - Odoo Version: {version}")
        self.after(5000, self.update_status)  # Rafraîchit toutes les 5 secondes

if __name__ == "__main__":
    # Instanciation de l'interface Odoo avec les paramètres de connexion
    odoo_interface = IF_Odoo("192.168.0.17", "8069", "vitre", "inter", "inter")
    app = App(odoo_interface)
    app.mainloop()

