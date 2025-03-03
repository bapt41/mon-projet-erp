#!/usr/bin/env python3
import xmlrpc.client
import base64

class IF_Odoo:
    def __init__(self, host, port, db, user, pwd):
        """
        host: ex. "172.31.10.137"
        port: ex. "8027"
        db: nom de la base (ex. "odoo")
        user: nom d'utilisateur (ex. "admin")
        pwd: mot de passe (ex. "admin")
        """
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.pwd = pwd
        self.url = f"http://{host}:{port}"
        self.uid = None
        self.odoo_version = None
        self.models = None

    def connect(self):
        """
        Connexion à Odoo via XML-RPC. Retourne True si OK, False sinon.
        """
        try:
            common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
            self.uid = common.authenticate(self.db, self.user, self.pwd, {})
            if not self.uid:
                print("Échec de l'authentification Odoo")
                return False
            self.odoo_version = common.version().get("server_serie", "Unknown")
            self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
            print(f"Connecté à Odoo, version: {self.odoo_version}")
            return True
        except Exception as e:
            print("Erreur de connexion:", e)
            return False

    # F2 : Fiche entreprise
    def get_company_info(self):
        """
        Récupère la fiche de la société principale (res.company).
        Retourne un dict avec les champs intéressants (name, street, etc.)
        """
        if not self.models:
            return {}
        try:
            # On suppose que l'ID de la compagnie principale est 1
            # ou on recherche la première via search_read
            companies = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'res.company', 'search_read',
                [[('id', '>', 0)]],  # ou [()] si vous voulez la première
                {'fields': ['name', 'street', 'city', 'phone'], 'limit': 1}
            )
            if companies:
                return companies[0]
            else:
                return {}
        except Exception as e:
            print("Erreur get_company_info:", e)
            return {}

    # F3 : Liste des produits (avec image)
    def get_products(self):
        """
        Retourne la liste des produits (product.template) avec
        'name', 'list_price', 'image_1920' (image binaire).
        """
        if not self.models:
            return []
        try:
            products = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'product.template', 'search_read',
                [[]],  # Tous les produits
                {'fields': ['name', 'list_price', 'image_1920'], 'limit': 50}
            )
            return products
        except Exception as e:
            print("Erreur get_products:", e)
            return []

    # F4 : Liste des OF
    def get_manufacturing_orders(self, state_filter=None):
        """
        Retourne la liste des ordres de fabrication (mrp.production).
        state_filter peut être 'confirmed', 'progress', 'done', 'cancel'
        """
        if not self.models:
            return []
        domain = []
        if state_filter:
            domain = [('state', '=', state_filter)]
        try:
            orders = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'mrp.production', 'search_read',
                [domain],
                {'fields': ['name', 'product_id', 'product_qty', 'qty_producing', 'state'], 'limit': 50}
            )
            return orders
        except Exception as e:
            print("Erreur get_manufacturing_orders:", e)
            return []

    # F5 : Mettre à jour la quantité produite d'un OF
    def update_mo_quantity(self, mo_id, new_qty):
        """
        Met à jour la qty_producing d'un ordre de fabrication (mrp.production).
        Retourne True si OK, False sinon.
        """
        if not self.models:
            return False
        try:
            result = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'mrp.production', 'write',
                [[mo_id], {'qty_producing': new_qty}]
            )
            return result
        except Exception as e:
            print("Erreur update_mo_quantity:", e)
            return False

    # Exemple pour passer un OF à l'état "done" (optionnel)
    def set_mo_done(self, mo_id):
        """
        Appelle la méthode 'button_mark_done' sur l'OF (Odoo 15).
        """
        try:
            self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'mrp.production', 'button_mark_done',
                [[mo_id]]
            )
            return True
        except Exception as e:
            print("Erreur set_mo_done:", e)
            return False
