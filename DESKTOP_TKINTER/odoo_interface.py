
#!/usr/bin/env python3
"""
Interface Odoo using XML-RPC.

Ce module définit la classe IF_Odoo pour :
- Se connecter et s'authentifier sur un serveur Odoo.
- Récupérer la quantité à produire et la quantité en cours de production d'un ordre de fabrication.
- Mettre à jour la quantité produite.
- Récupérer et sauvegarder l'image d'un produit.
"""

import xmlrpc.client
import base64

class IF_Odoo:
    def __init__(self, host, port, db, user, pwd):
        """
        Initialise l'interface avec les paramètres de connexion.
        """
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.pwd = pwd
        self.url = f'http://{host}:{port}'
        self.common = None
        self.models = None
        self.uid = None
        self.odoo_version = None

    def connect(self):
        """
        Se connecte au serveur Odoo via XML-RPC.
        Retourne True en cas de succès, False sinon.
        """
        try:
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = self.common.authenticate(self.db, self.user, self.pwd, {})
            if not self.uid:
                print("Échec de l'authentification.")
                return False
            self.odoo_version = self.common.version().get('server_serie', 'Unknown')
            self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
            print(f"Connexion réussie à Odoo, version: {self.odoo_version}")
            return True
        except Exception as e:
            print("Erreur de connexion :", e)
            return False

    def get_manuf_order_qty_to_product(self, mo_id):
        """
        Récupère la quantité à produire (product_qty) pour un ordre de fabrication donné (mo_id).
        Retourne un entier ou -1 si non trouvé.
        """
        try:
            orders = self.models.execute_kw(self.db, self.uid, self.pwd, 
                                            'mrp.production', 'search_read',
                                            [[('id', '=', int(mo_id))]],
                                            {'fields': ['product_qty']})
            if orders:
                qty = orders[0].get('product_qty', -1)
                print(f"OF {mo_id} - Quantité à produire : {qty}")
                return qty
            else:
                return -1
        except Exception as e:
            print("Erreur dans get_manuf_order_qty_to_product :", e)
            return -1

    def get_manuf_order_qty_producing(self, mo_id):
        """
        Récupère la quantité produite (qty_producing) pour un ordre de fabrication donné (mo_id).
        Retourne un entier ou -1 si non trouvé.
        """
        try:
            orders = self.models.execute_kw(self.db, self.uid, self.pwd,
                                            'mrp.production', 'search_read',
                                            [[('id', '=', int(mo_id))]],
                                            {'fields': ['qty_producing']})
            if orders:
                qty = orders[0].get('qty_producing', -1)
                print(f"OF {mo_id} - Quantité produite : {qty}")
                return qty
            else:
                return -1
        except Exception as e:
            print("Erreur dans get_manuf_order_qty_producing :", e)
            return -1

    def set_manuf_order_qty_producing(self, mo_id, value):
        """
        Met à jour la quantité produite (qty_producing) pour un ordre de fabrication (mo_id).
        Retourne True en cas de succès, False sinon.
        """
        try:
            result = self.models.execute_kw(self.db, self.uid, self.pwd,
                                            'mrp.production', 'write',
                                            [[int(mo_id)], {'qty_producing': value}])
            print(f"Mise à jour OF {mo_id} - Nouvelle quantité produite : {value} (Résultat: {result})")
            return result
        except Exception as e:
            print("Erreur dans set_manuf_order_qty_producing :", e)
            return False

    def save_product_image(self, product_id, image_name):
        """
        Récupère l'image d'un produit (champ 'image_1920' de product.template) et la sauvegarde au format .png.
        Retourne True si l'opération est réussie, False sinon.
        """
        try:
            products = self.models.execute_kw(self.db, self.uid, self.pwd,
                                              'product.template', 'search_read',
                                              [[('id', '=', int(product_id))]],
                                              {'fields': ['image_1920']})
            if products and products[0].get('image_1920'):
                image_str = products[0]['image_1920']
                image_bytes = base64.b64decode(image_str)
                with open(image_name, 'wb') as f:
                    f.write(image_bytes)
                print(f"Image du produit {product_id} sauvegardée sous {image_name}.")
                return True
            else:
                print("Aucune image trouvée pour le produit", product_id)
                return False
        except Exception as e:
            print("Erreur dans save_product_image :", e)
            return False

# Exemple de test de l'interface (à exécuter en ligne de commande)
if __name__ == "__main__":
    odoo = IF_Odoo("192.168.0.17", "8069", "vitre", "inter", "inter")
    if odoo.connect():
        mo_id = 15
        odoo.get_manuf_order_qty_to_product(mo_id)
        odoo.get_manuf_order_qty_producing(mo_id)
        current_qty = odoo.get_manuf_order_qty_producing(mo_id)
        if current_qty != -1:
            odoo.set_manuf_order_qty_producing(mo_id, current_qty + 1)
        # Exemple : sauvegarder l'image du produit avec id 1
        odoo.save_product_image(1, "product_1.png")
