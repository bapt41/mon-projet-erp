#!/usr/bin/env python3
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

# Importez votre interface Odoo
# Par exemple, si odoo_interface.py se trouve dans le même dossier :
from odoo_interface import IF_Odoo

class LoginPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1166x718')
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Login Page')

        # Créez un attribut pour stocker l'instance d'IF_Odoo
        self.odoo_connection = None

        # ============================ Background Image =============================
        self.bg_frame = Image.open('images\\background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        # ============================ Login Frame ==================================
        self.lgn_frame = Frame(self.window, bg='#040405', width=950, height=600)
        self.lgn_frame.place(x=200, y=70)

        # ============================ WELCOME Label ================================
        self.txt = "WELCOME"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"),
                             bg="#040405", fg='white', bd=5, relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=30)

        # ============================ Left Side Image ==============================
        self.side_image = Image.open('images\\vector.png')
        photo_side = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo_side, bg='#040405')
        self.side_image_label.image = photo_side
        self.side_image_label.place(x=5, y=100)

        # ============================ Sign In Image ================================
        self.sign_in_image = Image.open('images\\hyy.png')
        photo_sign = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo_sign, bg='#040405')
        self.sign_in_image_label.image = photo_sign
        self.sign_in_image_label.place(x=620, y=130)

        # ============================ Sign In Label ================================
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white",
                                    font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)

        # ============================ Username =====================================
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_var = StringVar()
        self.username_entry = Entry(self.lgn_frame, textvariable=self.username_var,
                                    highlightthickness=0, relief=FLAT,
                                    bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"),
                                    insertbackground='#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)

        # ===== Username icon
        self.username_icon = Image.open('images\\username_icon.png')
        username_icon_photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=username_icon_photo, bg='#040405')
        self.username_icon_label.image = username_icon_photo
        self.username_icon_label.place(x=550, y=332)

        # ============================ Password =====================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_var = StringVar()
        self.password_entry = Entry(self.lgn_frame, textvariable=self.password_var,
                                    highlightthickness=0, relief=FLAT,
                                    bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"),
                                    show="*", insertbackground='#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)

        # ======== Password icon
        self.password_icon = Image.open('images\\password_icon.png')
        password_icon_photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=password_icon_photo, bg='#040405')
        self.password_icon_label.image = password_icon_photo
        self.password_icon_label.place(x=550, y=414)

        # ======== Show/Hide Password
        self.show_image = ImageTk.PhotoImage(file='images\\show.png')
        self.hide_image = ImageTk.PhotoImage(file='images\\hide.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show_password,
                                  relief=FLAT, activebackground="white",
                                  borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

        # ============================ Login Button ================================
        self.lgn_button = Image.open('images\\btn1.png')
        lgn_button_photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=lgn_button_photo, bg='#040405')
        self.lgn_button_label.image = lgn_button_photo
        self.lgn_button_label.place(x=550, y=450)

        self.login_btn = Button(self.lgn_button_label, text='LOGIN',
                                font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                                bg='#3047ff', cursor='hand2', activebackground='#3047ff',
                                fg='white', command=self.login_action)
        self.login_btn.place(x=20, y=10)

        # ============================ Forgot password =============================
        self.forgot_button = Button(self.lgn_frame, text="Forgot Password ?",
                                    font=("yu gothic ui", 13, "bold underline"),
                                    fg="white", relief=FLAT,
                                    activebackground="#040405",
                                    borderwidth=0, background="#040405",
                                    cursor="hand2")
        self.forgot_button.place(x=630, y=510)

        # =========== Sign Up
        self.sign_label = Label(self.lgn_frame, text='No account yet?',
                                font=("yu gothic ui", 11, "bold"),
                                relief=FLAT, borderwidth=0,
                                background="#040405", fg='white')
        self.sign_label.place(x=550, y=560)

        self.signup_img = ImageTk.PhotoImage(file='images\\register.png')
        self.signup_button_label = Button(self.lgn_frame, image=self.signup_img, bg='#98a65d',
                                          cursor="hand2", borderwidth=0,
                                          background="#040405", activebackground="#040405")
        self.signup_button_label.place(x=670, y=555, width=111, height=35)

    def show_password(self):
        """Afficher le password en clair."""
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide_password,
                                  relief=FLAT, activebackground="white",
                                  borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide_password(self):
        """Masquer le password."""
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show_password,
                                  relief=FLAT, activebackground="white",
                                  borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')

    def login_action(self):
        """
        Logique déclenchée lors du clic sur 'LOGIN'.
        Ici, on va se connecter à Odoo via IF_Odoo.
        """
        username = self.username_var.get()
        password = self.password_var.get()

        # Instanciez IF_Odoo avec votre host/port/db, etc.
        # Si votre Odoo utilise le champ 'user'/'pwd' de manière standard,
        # vous pouvez faire un connect() simple, ou une méthode custom
        # pour passer user/password depuis ce login.
        host = "172.31.10.137"
        port = "8027"
        db = "postgres"   # Adaptez au nom de votre base
        # user = "odoo"    # identifiant Odoo si vous n'utilisez pas le "username" saisi
        # pwd = "myodoo"

        # Si vous voulez utiliser le username/password saisi comme identifiant Odoo,
        # vous pouvez faire:
        self.odoo_connection = IF_Odoo(host, port, db, username, password)

        success = self.odoo_connection.connect()
        if success:
            # Connexion réussie
            messagebox.showinfo("Login", f"Bienvenue, {username} !")
            # Ici, vous pouvez fermer la fenêtre de login et ouvrir la suite :
            # self.window.destroy()
            # main_app = SomeOtherApp(self.odoo_connection)
            # main_app.mainloop()
        else:
            # Connexion échouée
            messagebox.showerror("Erreur", "Impossible de se connecter à Odoo.\nVérifiez vos identifiants/paramètres.")

def page():
    window = Tk()
    LoginPage(window)
    window.mainloop()

if __name__ == '__main__':
    page()
