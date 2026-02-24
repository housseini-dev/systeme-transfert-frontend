import customtkinter as ctk
from tkinter import messagebox
from reçus import generer_reçu_envoi
from expediteur import ajouter_expediteur
from destinataire import ajouter_destinataire
from destination import lister_pays, chercher_villes_par_pays, get_id_destination
from transfert import creer_transfert


# ---------------- CONFIG UI ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class GuiTransfert(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("GALA TRANSFERT D'ARGENT")
        self.geometry("1000x600")
        self.resizable(False, False)

        # ---------------- VARIABLES ----------------
        self.var_type = ctk.IntVar(value=1)     # 1 = national, 0 = international
        self.var_frais = ctk.IntVar(value=1)    # 1 = inclus, 0 = non

        # ---------------- TITRE ----------------
        ctk.CTkLabel(
            self,
            text="GALA TRANSFERT D'ARGENT",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # =====================================================
        # EXPÉDITEUR
        # =====================================================
        ctk.CTkLabel(main, text="EXPÉDITEUR", font=("Arial", 14, "bold"))\
            .grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.tel_exp = ctk.CTkEntry(main, placeholder_text="Prénom")
        self.tel_exp.grid(row=1, column=0, padx=5, pady=5)

        self.nom_exp = ctk.CTkEntry(main, placeholder_text="Nom")
        self.nom_exp.grid(row=1, column=1, padx=5, pady=5)

        self.prenom_exp = ctk.CTkEntry(main, placeholder_text="Téléphone")
        self.prenom_exp.grid(row=1, column=2, padx=5, pady=5)
        
        self.numero_exp = ctk.CTkEntry(main, placeholder_text="numéro_pièce")
        self.numero_exp.grid(row=1, column=3, padx=5, pady=5)
       
        # =====================================================
        # DESTINATAIRE
        # =====================================================
        ctk.CTkLabel(main, text="DESTINATAIRE", font=("Arial", 14, "bold"))\
            .grid(row=2, column=0, sticky="w", pady=(10, 5))

        self.nom_dest = ctk.CTkEntry(main, placeholder_text="Prénom")
        self.nom_dest.grid(row=3, column=0, padx=5, pady=5)

        self.prenom_dest = ctk.CTkEntry(main, placeholder_text="Nom")
        self.prenom_dest.grid(row=3, column=1, padx=5, pady=5)

        self.tel_dest = ctk.CTkEntry(main, placeholder_text="Téléphone")
        self.tel_dest.grid(row=3, column=2, padx=5, pady=5)
        
        
        self.numero_dest = ctk.CTkEntry(main, placeholder_text="numéro_pièce")
        self.numero_dest.grid(row=3, column=3, padx=5, pady=5)

        # =====================================================
        # DESTINATION
        # =====================================================
        ctk.CTkLabel(main, text="DESTINATION", font=("Arial", 14, "bold"))\
            .grid(row=4, column=0, sticky="w", pady=(10, 5))

        self.combo_pays = ctk.CTkComboBox(
            main,
            values=lister_pays(),
            command=self.charger_villes,
            width=200
        )
        self.combo_pays.grid(row=5, column=0, padx=5, pady=5)

        self.combo_ville = ctk.CTkComboBox(
            main,
            values=[],
            width=200
        )
        self.combo_ville.grid(row=5, column=1, padx=5, pady=5)

        # =====================================================
        # TRANSFERT
        # =====================================================
        self.montant_entry = ctk.CTkEntry(
            main,
            placeholder_text="Montant",
            width=200
        )
        self.montant_entry.grid(row=6, column=0, padx=5, pady=10)

        ctk.CTkRadioButton(
            main, text="National",
            variable=self.var_type, value=1
        ).grid(row=6, column=1, sticky="w")

        ctk.CTkRadioButton(
            main, text="International",
            variable=self.var_type, value=0
        ).grid(row=6, column=2, sticky="w")

        ctk.CTkCheckBox(
            main,
            text="Frais inclus (0,3%)",
            variable=self.var_frais
        ).grid(row=7, column=0, pady=5, sticky="w")

        # =====================================================
        # BOUTON
        # =====================================================
        ctk.CTkButton(
            main,
            text="VALIDER LE TRANSFERT",
            height=40,
            command=self.creer_transfert_gui
        ).grid(row=8, column=0, columnspan=3, pady=20)

    # =====================================================
    # MÉTHODES
    # =====================================================
    def charger_villes(self, pays):
        villes = chercher_villes_par_pays(pays)
        self.combo_ville.configure(values=villes)

        if villes:
            self.combo_ville.set(villes[0])

    def creer_transfert_gui(self):
        try:
            # -------- montant --------
            montant = float(self.montant_entry.get())

            # -------- expéditeur --------
            exp = ajouter_expediteur(
                self.tel_exp.get(),
                self.nom_exp.get(),
                self.prenom_exp.get(),
                self.numero_exp.get()
            )

            if not exp:
                messagebox.showerror("Erreur", " Attention !!! expéditeur introuvale ")
                return

            # -------- destinataire --------
            dest = ajouter_destinataire(
                self.nom_dest.get(),
                self.prenom_dest.get(),
                self.tel_dest.get(),
                self.numero_dest.get()

            )

            if not dest:
                messagebox.showerror("Erreur", " Attention !!! destinataire introuvale ")
                return

            # -------- destination --------
            pays = self.combo_pays.get()
            ville = self.combo_ville.get()
            id_destination = get_id_destination(pays, ville)

            # -------- création transfert --------
            code = creer_transfert(
                exp["id_expediteur"],
                dest["id_destinataire"],
                1,                  # id_agent (temporaire)
                1,                  # id_agence (temporaire)
                id_destination,
                self.var_type.get(),
                self.var_frais.get(),
                montant
            )

            if code:
                messagebox.showinfo(
                    "Succès",
                    f"Transfert effectué avec succès\nCode d’envoi : {code}\nMerci et Aurevoir :)"
                )

        except Exception as e:
            messagebox.showerror("Erreur", str(e))


if __name__ == "__main__":
    GuiTransfert().mainloop()
