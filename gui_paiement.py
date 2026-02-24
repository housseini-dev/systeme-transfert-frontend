import customtkinter as ctk
from tkinter import messagebox
from paiement import verifier_transfert, effectuer_paiement
from reçus import generer_reçu_retrait

class GuiPaiement(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("Paiement transfert")
        self.geometry("1000x600")
        self.resizable(False, False)


        self.transfert = None

        ctk.CTkLabel(self, text="Vérification du destinataire", font=("Arial", 18)).pack(pady=10)

        self.tel_entry = ctk.CTkEntry(self, placeholder_text="Téléphone destinataire")
        self.tel_entry.pack(pady=5)

        self.nom_entry = ctk.CTkEntry(self, placeholder_text="Nom")
        self.nom_entry.pack(pady=5)

        self.prenom_entry = ctk.CTkEntry(self, placeholder_text="Prénom")
        self.prenom_entry.pack(pady=5)

        self.code_entry = ctk.CTkEntry(self, placeholder_text="Code d'envoi")
        self.code_entry.pack(pady=5)

        ctk.CTkButton(self, text="Vérifier", command=self.verifier).pack(pady=10)

        self.info_label = ctk.CTkLabel(self, text="")
        self.info_label.pack(pady=10)

        self.payer_btn = ctk.CTkButton(
            self,
            text="Valider le paiement",
            command=self.payer,
            state="disabled"
        )
        self.payer_btn.pack(pady=10)

    def verifier(self):
        telephone = self.tel_entry.get()
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        code = self.code_entry.get()

        if not (telephone or code or (nom and prenom)):
            messagebox.showerror(
                "Erreur",
                "Donnez soit le téléphone, soit nom+prénom, soit le code d'envoi"
            )
            return

        self.transfert = verifier_transfert(
            telephone=telephone if telephone else None,
            nom=nom if nom else None,
            prenom=prenom if prenom else None,
            code_envoi=code if code else None
        )

        if self.transfert:
            self.info_label.configure(
                text=f"Transfert trouvé\nMontant : {self.transfert['montant']} FCFA"
            )
            self.payer_btn.configure(state="normal")
        else:
            self.info_label.configure(text="Aucun transfert valide trouvé")
            self.payer_btn.configure(state="disabled")

    def payer(self):
        if not self.transfert:
            return

        effectuer_paiement(
            self.transfert['id_transfert'],
            self.transfert['montant']
        )

        messagebox.showinfo("Succès", " Paiement effectué avec succès\nMercie et Aurevoir :) ")
        self.destroy()


if __name__ == "__main__":
    app = GuiPaiement()
    app.mainloop()
