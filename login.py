import customtkinter as ctk
from tkinter import messagebox
from agent import verifier_agent
from menu_principal import MenuPrincipal

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Login(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Connexion Agent")
        self.geometry("500x300")
        self.resizable(False, False)

        ctk.CTkLabel(self,
                     text="Connexion Agence",
                     font=("Arial", 20, "bold")).pack(pady=20)

        self.entry_matricule = ctk.CTkEntry(
            self,
            placeholder_text="Matricule"
        )
        self.entry_matricule.pack(pady=10)

        self.entry_password = ctk.CTkEntry(
            self,
            placeholder_text="Mot de passe",
            show="*"
        )
        self.entry_password.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Se connecter",
            command=self.login
        ).pack(pady=20)

    def login(self):

        matricule = self.entry_matricule.get()
        password = self.entry_password.get()

        agent = verifier_agent(matricule, password)

        if agent:
            messagebox.showinfo(
                "Succès",
                f"Connexion réussie\nBienvenue {agent['nom_agent']}"
            )

            self.withdraw()  # 👈 cache la fenêtre login

            menu = MenuPrincipal(agent)
            menu.mainloop()

            self.destroy()  # 👈 détruit proprement après fermeture du menu

        else:
            messagebox.showerror(
                "Erreur",
                "Matricule ou mot de passe incorrect"
            )

if __name__ == "__main__":
    app = Login()
    app.mainloop()
