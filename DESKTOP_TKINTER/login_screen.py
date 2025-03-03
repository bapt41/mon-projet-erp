#!/usr/bin/env python3
import os
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

# On importe IF_Odoo et MainApp pour gérer la suite
from odoo_interface import IF_Odoo
from main import App

class LoginPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1166x718')
        self.window.resizable(0, 0)
        self.window.title('Login Page')

        # ===================== Variables de champ =====================
        self.username_var = StringVar()
        self.password_var = StringVar()

        # ===================== Construction des chemins absolus =====================
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(script_dir, "images")

        bg_path       = os.path.join(img_dir, "background1.png")
        vector_path   = os.path.join(img_dir, "vector.png")
        hyy_path      = os.path.join(img_dir, "hyy.png")
        username_ico  = os.path.join(img_dir, "username_icon.png")
        password_ico  = os.path.join(img_dir, "password_icon.png")
        show_path     = os.path.join(img_dir, "show.png")
        hide_path     = os.path.join(img_dir, "hide.png")
        btn1_path     = os.path.join(img_dir, "btn1.png")
        register_path = os.path.join(img_dir, "register.png")

        # ===================== Background Image =====================
        self.bg_frame = Image.open(bg_path)
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        # ===================== Login Frame centré ===================
        self.lgn_frame = Frame(self.window, bg='#040405', width=950, height=600)
        self.lgn_frame.place(relx=0.5, rely=0.5, anchor="center")

        # ===================== Titre WELCOME ========================
        self.txt = "WELCOME"
        self.heading = Label(
            self.lgn_frame,
            text=self.txt,
            font=('yu gothic ui', 25, "bold"),
            bg="#040405",
            fg='white',
            bd=5,
            relief=FLAT
        )
        self.heading.place(x=80, y=30, width=300, height=30)

        # ===================== Left Side Image ======================
        self.side_image = Image.open(vector_path)
        side_photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=side_photo, bg='#040405')
        self.side_image_label.image = side_photo
        self.side_image_label.place(x=5, y=100)

        # ===================== Sign In Image ========================
        self.sign_in_image = Image.open(hyy_path)
        sign_photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=sign_photo, bg='#040405')
        self.sign_in_image_label.image = sign_photo
        self.sign_in_image_label.place(x=620, y=130)

        # ===================== Label "Sign In" ======================
        self.sign_in_label = Label(
            self.lgn_frame,
            text="Sign In",
            bg="#040405",
            fg="white",
            font=("yu gothic ui", 17, "bold")
        )
        self.sign_in_label.place(x=650, y=240)

        # ===================== Username =============================
        self.username_label = Label(
            self.lgn_frame,
            text="Username",
            bg="#040405",
            fg="#4f4e4d",
            font=("yu gothic ui", 13, "bold")
        )
        self.username_label.place(x=550, y=300)

        # On lie self.username_var au champ
        self.username_entry = Entry(
            self.lgn_frame,
            textvariable=self.username_var,
            highlightthickness=0,
            relief=FLAT,
            bg="#040405",
            fg="#6b6a69",
            font=("yu gothic ui", 12, "bold"),
            insertbackground='#6b6a69'
        )
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(
            self.lgn_frame,
            width=300,
            height=2.0,
            bg="#bdb9b1",
            highlightthickness=0
        )
        self.username_line.place(x=550, y=359)

        # ===== Username icon
        self.username_icon = Image.open(username_ico)
        u_photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=u_photo, bg='#040405')
        self.username_icon_label.image = u_photo
        self.username_icon_label.place(x=550, y=332)

        # ===================== Login Button =========================
        self.lgn_button = Image.open(btn1_path)
        lgn_photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=lgn_photo, bg='#040405')
        self.lgn_button_label.image = lgn_photo
        self.lgn_button_label.place(x=550, y=450)

        self.login = Button(
            self.lgn_button_label,
            text='LOGIN',
            font=("yu gothic ui", 13, "bold"),
            width=20,
            bd=0,
            highlightthickness=0,
            relief='flat',
            fg='white',
            bg='#3047ff',
            activebackground='#3047ff',
            command=self.login_action  # <-- Appel de la méthode login_action
        )
        self.login.place(x=20, y=10)

        # ===================== Password =============================
        self.password_label = Label(
            self.lgn_frame,
            text="Password",
            bg="#040405",
            fg="#4f4e4d",
            font=("yu gothic ui", 13, "bold")
        )
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(
            self.lgn_frame,
            textvariable=self.password_var,
            highlightthickness=0,
            relief=FLAT,
            bg="#040405",
            fg="#6b6a69",
            font=("yu gothic ui", 12, "bold"),
            show="*",
            insertbackground='#6b6a69'
        )
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(
            self.lgn_frame,
            width=300,
            height=2.0,
            bg="#bdb9b1",
            highlightthickness=0
        )
        self.password_line.place(x=550, y=440)

        # ======== Password icon
        self.password_icon = Image.open(password_ico)
        p_photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=p_photo, bg='#040405')
        self.password_icon_label.image = p_photo
        self.password_icon_label.place(x=550, y=414)

        # ======== show/hide password
        self.show_image = ImageTk.PhotoImage(file=show_path)
        self.hide_image = ImageTk.PhotoImage(file=hide_path)

        self.show_button = Button(
            self.lgn_frame,
            image=self.show_image,
            command=self.show,
            relief=FLAT,
            activebackground="white",
            borderwidth=0,
            background="white",
            cursor="hand2"
        )
        self.show_button.place(x=860, y=420)

    def login_action(self):
        """Méthode appelée quand on clique sur LOGIN"""
        username = self.username_var.get()
        password = self.password_var.get()

        # On instancie IF_Odoo avec ces identifiants
        # Adaptez host/port/db à votre configuration
        host = "172.31.10.137"
        port = "8027"
        db   = "odoo_demo"

        # Création de l'interface Odoo
        self.odoo_conn = IF_Odoo(host, port, db, username, password)
        success = self.odoo_conn.connect()
        if success:
            # Connexion OK -> on ferme la fenêtre de login
            self.window.destroy()

            # Ouvrir la fenêtre principale
            app = MainApp(self.odoo_conn)
            app.mainloop()
        else:
            messagebox.showerror("Erreur", "Impossible de se connecter à Odoo.")

    def show(self):
        """Afficher le mot de passe en clair."""
        self.hide_button = Button(
            self.lgn_frame,
            image=self.hide_image,
            command=self.hide,
            relief=FLAT,
            activebackground="white",
            borderwidth=0,
            background="white",
            cursor="hand2"
        )
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        """Re-masquer le mot de passe."""
        self.show_button = Button(
            self.lgn_frame,
            image=self.show_image,
            command=self.show,
            relief=FLAT,
            activebackground="white",
            borderwidth=0,
            background="white",
            cursor="hand2"
        )
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')


def page():
    window = Tk()
    LoginPage(window)
    window.mainloop()

if __name__ == '__main__':
    page()
