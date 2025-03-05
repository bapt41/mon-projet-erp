gantt
    title Planning du Projet ERP Odoo
    dateFormat  YYYY-MM-DD
    section ERP ODOO
    Déploiement              :done, d1, 2025-03-03, 2025-03-07
    Connexion Tkinter        :active, t1, 2025-03-03, 2025-03-05
    Connexion Odoo           : t2, 2025-03-04, 2025-03-06
    Formation                : t3, 2025-03-05, 2025-03-06
    Création BDD             : t4, 2025-03-06, 2025-03-07
    Archive images           : t5, 2025-03-07, 2025-03-08
    
    section Code
    odoo.py (API XML-RPC)    : c1, 2025-03-04, 2025-03-06
    main.py (App Tkinter)    : c2, 2025-03-05, 2025-03-07
    
    section Configuration et base ODOO
    docker-compose.xml       : db1, 2025-03-03, 2025-03-04
    sauvegarde BD ODOO       : db2, 2025-03-06, 2025-03-07
    
    section Présentation / Dossier technique
    Diaporama                : doc1, 2025-03-06, 2025-03-08
    Gantt                    : doc2, 2025-03-07, 2025-03-08
    Analyse sujet            : doc3, 2025-03-07, 2025-03-08
    Liste Unitaire de Progrès: doc4, 2025-03-07, 2025-03-08
    
    section Tests et Finalisation
    FAT                      : fat, 2025-03-07, 2025-03-08
