#!/usr/bin/env python3
import xmlrpc.client
import base64

class IF_Odoo:
    """
    Classe d'interface Python <-> Odoo via l'API XML-RPC.
    """

    def __init__(self, host, port, db, user, pwd):
        """
        Paramètres de connexion à Odoo.
        :param host: ex. "localhost" ou "172.31.10.137"
        :param port: ex. "8069"
        :param db:   nom de la base Odoo, ex. "demo"
        :param user: utilisateur Odoo (login)
        :param pwd:  mot de passe Odoo
        """
        self.host = host
        self.port = port
        self.db   = db
        self.user = user
        self.pwd  = pwd

        self.uid    = None  # sera attribué après connect()
        self.models = None  # proxy vers /xmlrpc/2/object

    def connect(self):
        """
        F1 : Tentative de connexion à Odoo via XML-RPC.
        Retourne True si OK, False sinon.
        """
        try:
            url = f"http://{self.host}:{self.port}"
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")

            self.uid = common.authenticate(self.db, self.user, self.pwd, {})
            if not self.uid:
                # Echec d'authentification
                return False

            # On récupère le proxy vers /xmlrpc/2/object
            self.models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
            return True
        except Exception as e:
            print(f"[IF_Odoo] Erreur de connexion : {e}")
            return False

    def get_company_info(self):
        """
        F2 : Récupère la fiche de la société principale (res.company).
        Retourne un dict : {'name':..., 'street':..., 'city':..., 'phone':...} ou {} si non trouvé.
        """
        if not self.models:
            return {}
        try:
            comps = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'res.company', 'search_read',
                [[]],  # tout
                {'fields': ['name', 'street', 'city', 'phone'], 'limit': 1}
            )
            return comps[0] if comps else {}
        except Exception as e:
            print(f"[IF_Odoo] Erreur get_company_info : {e}")
            return {}

    def get_products(self):
        """
        F3 : Récupère la liste des produits (product.template).
        Retourne une liste de dict, ex. :
        [
          {'id':..., 'name':..., 'list_price':..., 'image_1920':...},
          ...
        ]
        """
        if not self.models:
            return []
        try:
            products = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'product.template', 'search_read',
                [[]],
                {'fields': ['name', 'list_price', 'image_1920'], 'limit': 50}
            )
            return products
        except Exception as e:
            print(f"[IF_Odoo] Erreur get_products : {e}")
            return []

    def get_manufacturing_orders(self, state_filter=None):
        """
        F4 : Récupère la liste des Ordres de Fabrication (mrp.production).
        :param state_filter: ex. 'confirmed', 'progress', 'done', 'cancel' ou None
        :return: liste de dict
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
                {'fields': ['name', 'product_qty', 'qty_producing', 'state'], 'limit': 50}
            )
            return orders
        except Exception as e:
            print(f"[IF_Odoo] Erreur get_manufacturing_orders : {e}")
            return []

    def update_mo_quantity(self, mo_id, new_qty):
        """
        F5 : Met à jour la qty_producing d'un Ordre de Fab (mrp.production).
        :param mo_id: l'ID de l'OF (entier)
        :param new_qty: nouvelle quantité produite (float)
        :return: True si OK, False sinon
        """
        if not self.models:
            return False
        try:
            result = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'mrp.production', 'write',
                [[mo_id], {'qty_producing': new_qty}]
            )
            return result  # True ou False
        except Exception as e:
            print(f"[IF_Odoo] Erreur update_mo_quantity : {e}")
            return False

    def save_product_image(self, product_id, image_filename):
        """
        Optionnel : Récupère l'image binaire (image_1920) d'un product.template puis
        la sauvegarde dans un fichier (image_filename).
        """
        if not self.models:
            return False
        try:
            products = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'product.template', 'search_read',
                [[('id', '=', product_id)]],
                {'fields': ['image_1920'], 'limit': 1}
            )
            if not products:
                return False
            image_str = products[0].get('image_1920')
            if not image_str:
                return False

            # On convertit la chaîne base64 en bytes
            image_bytes = base64.b64decode(image_str)

            # On sauvegarde dans un fichier .png
            with open(image_filename, 'wb') as f:
                f.write(image_bytes)

            return True
        except Exception as e:
            print(f"[IF_Odoo] Erreur save_product_image : {e}")
            return False
