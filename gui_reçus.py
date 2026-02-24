import customtkinter as ctk
from tkinter import ttk, messagebox
from transfert import liste_transferts_reçus
from reçus import generer_reçu_envoi, generer_reçu_retrait


class GuiReçus(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("Gestion des Reçus")
        self.geometry("1000x600")
        self.resizable(False, False)


        self.selected_data = None
        self.data_cache = []   # 🔥 on stocke les données une seule fois

        # ================= TABLEAU =================
        self.tree = ttk.Treeview(
            self,
            columns=("code", "montant", "statut"),
            show="headings"
        )

        self.tree.heading("code", text="Code Envoi")
        self.tree.heading("montant", text="Montant")
        self.tree.heading("statut", text="Statut")

        self.tree.pack(fill="x", padx=20, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.afficher_apercu)

        # ================= APERCU =================
        self.preview = ctk.CTkTextbox(          
            self,
            width=900,
            height=250,
            font=("Courier", 13)
        )
       
        # ================= BOUTONS =================
        frame_btn = ctk.CTkFrame(self)
        frame_btn.pack(pady=10)

        self.btn_envoi = ctk.CTkButton(frame_btn, text="Générer Reçu Envoi")
        self.btn_envoi.grid(row=0, column=0, padx=20)

        self.btn_retrait = ctk.CTkButton(frame_btn, text="Générer Reçu Retrait")
        self.btn_retrait.grid(row=0, column=1, padx=20)

    # ================= CHARGEMENT =================
    def charger(self):

        self.data_cache = liste_transferts_reçus()

        for row in self.data_cache:
            self.tree.insert("", "end", values=(
                row["code_envoi"],
                row["montant"],
                row["statut"]
            ))

    # ================= APERCU =================
    def afficher_apercu(self, event):

        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if not values:
            return

        code = values[0]

        # 🔥 chercher dans le cache
        self.selected_data = next(
            (row for row in self.data_cache if row["code_envoi"] == code),
            None
        )

        if not self.selected_data:
            return

        self.preview.delete("1.0", "end")

        texte = f"""
=============================
          APERCU RECU
=============================

Code : {self.selected_data.get('code_envoi', '')}

Expediteur :
{self.selected_data.get('nom_expediteur', '')} {self.selected_data.get('prenom_expediteur', '')}

Destinataire :
{self.selected_data.get('nom_destinataire', '')} {self.selected_data.get('prenom_destinataire', '')}

Destination :
{self.selected_data.get('ville_destination', '')} - {self.selected_data.get('pays_destination', '')}

Montant : {self.selected_data.get('montant', 0)} FCFA
Frais   : {self.selected_data.get('frais', 0)} FCFA
Statut  : {self.selected_data.get('statut', '')}
"""

        self.preview.insert("1.0", texte)

    # ================= GENERER ENVOI =================
    def generer_envoi(self):

        if not self.selected_data:
            messagebox.showerror("Erreur", "Veuillez sélectionner un transfert")
            return

        generer_reçu_envoi(self.selected_data)
        messagebox.showinfo("Succès", "Reçu d'envoi généré avec succès")

    # ================= GENERER RETRAIT =================
    def generer_retrait(self):

        if not self.selected_data:
            messagebox.showerror("Erreur", "Veuillez sélectionner un transfert")
            return

        generer_reçu_retrait(self.selected_data)
        messagebox.showinfo("Succès", "Reçu de retrait généré avec succès")


if __name__ == "__main__":
    GuiReçus().mainloop()
