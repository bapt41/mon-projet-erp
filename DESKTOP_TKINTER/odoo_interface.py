#!/usr/bin/env python3
import xmlrpc.client
import base64

class IF_Odoo:
    """
    Interface Python <-> Odoo via XML-RPC.
    Permet la connexion, la récupération de données (fiche d'entreprise,
    produits, ordres de fabrication, commandes clients, tâches récentes),
    et la mise à jour d'un ordre de fabrication par son nom.
    """

    def __init__(self, host, port, db, user, pwd):
        """
        Initialisation avec les paramètres de connexion.
        :param host: Adresse du serveur Odoo (ex: "localhost" ou "172.31.10.137")
        :param port: Port d'accès (ex: "8069" ou "8027")
        :param db:   Nom de la base de données (ex: "demo")
        :param user: Utilisateur (login) Odoo
        :param pwd:  Mot de passe Odoo
        """
        self.host = host
        self.port = port
        self.db   = db
        self.user = user
        self.pwd  = pwd

        self.uid    = None  # Identifiant utilisateur après authentification
        self.models = None  # Proxy pour les appels sur /xmlrpc/2/object

    def connect(self):
        """
        Tente de se connecter à Odoo via XML-RPC.
        Retourne True en cas de succès, False sinon.
        """
        try:
            url = f"http://{self.host}:{self.port}"
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            self.uid = common.authenticate(self.db, self.user, self.pwd, {})
            if not self.uid:
                return False
            self.models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
            return True
        except Exception as e:
            print(f"[IF_Odoo] Erreur de connexion : {e}")
            return False

    def get_company_info(self):
        """
        Récupère la fiche de l'entreprise (res.company).
        Retourne un dictionnaire avec 'name', 'street', 'city', 'phone'.
        """
        if not self.models:
            return {}
        try:
            comps = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'res.company', 'search_read',
                [[]],
                {'fields': ['name', 'street', 'city', 'phone'], 'limit': 1}
            )
            return comps[0] if comps else {}
        except Exception as e:
            print(f"[IF_Odoo] Erreur get_company_info : {e}")
            return {}

    def get_products(self):
        """
        Récupère la liste des produits (product.template) avec :
            - name, list_price, image_1920, categ_id, description_sale.
        Retourne une liste de dictionnaires.
        """
        if not self.models:
            return []
        try:
            products = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'product.template', 'search_read',
                [[]],
                {'fields': ['name', 'list_price', 'image_1920', 'categ_id', 'description_sale'], 'limit': 50}
            )
            return products
        except Exception as e:
            print(f"[IF_Odoo] Erreur get_products : {e}")
            return []

    def get_manufacturing_orders(self, state_filter=None):
        """
        Récupère la liste des Ordres de Fabrication (mrp.production).
        :param state_filter: Filtre par état ('confirmed', 'progress', 'done', 'cancel')
                            ou "all" pour récupérer toutes les OF.
        :return: Liste de dictionnaires contenant 'name', 'product_qty', 'qty_producing', 'state'
        """
        if not self.models:
            return []
        if state_filter is None or state_filter == "all":
            domain = []
            limit_value = 0  # ou supprimer 'limit' dans le dictionnaire
        else:
            domain = [('state', '=', state_filter)]
            limit_value = 50  # ou un nombre adapté
        try:
            orders = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'mrp.production', 'search_read',
                [domain],
                {'fields': ['name', 'product_qty', 'qty_producing', 'state'], 'limit': limit_value}  # Si limit_value vaut 0, cela peut signifier "aucune limite" selon votre version d'Odoo.
            )
            return orders
        except Exception as e:
            print(f"[IF_Odoo] Erreur get_manufacturing_orders : {e}")
            return []





    def update_mo_quantity_by_name(self, mo_name, new_qty):
        """
        Met à jour la quantité produite (qty_producing) d'un Ordre de Fabrication
        en recherchant l'enregistrement par le champ 'name' (ex: "MO/00014").
        :param mo_name: Nom de l'OF.
        :param new_qty: Nouvelle quantité produite (float).
        :return: True si la mise à jour est effectuée, False sinon.
        """
        if not self.models:
            return False
        try:
            recs = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'mrp.production', 'search_read',
                [[('name', '=', mo_name)]],
                {'fields': ['id'], 'limit': 1}
            )
            if not recs:
                print(f"[IF_Odoo] Aucune OF trouvée avec name = {mo_name}")
                return False
            mo_id = recs[0]['id']
            result = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'mrp.production', 'write',
                [[mo_id], {'qty_producing': new_qty}]
            )
            return result
        except Exception as e:
            print(f"[IF_Odoo] Erreur update_mo_quantity_by_name : {e}")
            return False

    def get_sales_order_count(self):
        """
        Retourne le nombre total de commandes clients (sale.order) enregistrées dans Odoo.
        """
        if not self.models:
            return 0
        try:
            count = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'sale.order', 'search_count',
                [[]]
            )
            return count
        except Exception as e:
            print(f"[IF_Odoo] Erreur get_sales_order_count : {e}")
            return 0

    def get_recent_tasks(self, limit=5):
        """
        Récupère les tâches récentes (project.task) depuis Odoo.
        Retourne une liste de dictionnaires contenant les champs
        'name', 'date_deadline', 'user_id' et 'stage_id'.
        Les tâches sont triées par date de création décroissante.
        :param limit: Nombre maximum de tâches à récupérer.
        """
        if not self.models:
            return []
        try:
            tasks = self.models.execute_kw(
                self.db, self.uid, self.pwd,
                'project.task', 'search_read',
                [[]],
                {
                    'fields': ['name', 'date_deadline', 'user_id', 'stage_id'],
                    'limit': limit,
                    'order': 'create_date desc'
                }
            )
            return tasks
        except Exception as e:
            print(f"[IF_Odoo] Erreur get_recent_tasks : {e}")
            return []

    def save_product_image(self, product_id, image_filename):
        """
        Récupère l'image binaire (image_1920) d'un produit (product.template)
        et la sauvegarde dans un fichier.
        :param product_id: ID du produit.
        :param image_filename: Chemin complet du fichier de sauvegarde.
        :return: True si l'image est sauvegardée, False sinon.
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
            image_bytes = base64.b64decode(image_str)
            with open(image_filename, 'wb') as f:
                f.write(image_bytes)
            return True
        except Exception as e:
            print(f"[IF_Odoo] Erreur save_product_image : {e}")
            return False
