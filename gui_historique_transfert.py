import customtkinter as ctk
from tkinter import ttk
from transfert import historique_transferts


class GuiHistoriqueTransfert(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("Historique des Transferts")
        self.geometry("1000x600")
        self.resizable(False, False)


        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        titre = ctk.CTkLabel(
            self,
            text="HISTORIQUE DES TRANSFERTS",
            font=("Arial", 22, "bold")
        )
        titre.pack(pady=20)

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        colonnes = (
            "Code",
            "Expéditeur",
            "Destinataire",
            "Pays",
            "Ville",
            "Montant",
            "Date",
            "Statut"
        )

        self.table = ttk.Treeview(
            frame,
            columns=colonnes,
            show="headings"
        )

        for col in colonnes:
            self.table.heading(col, text=col)
            self.table.column(col, width=130, anchor="center")

        self.table.pack(fill="both", expand=True)

        self.charger()

    # ================================
    # Charger les transferts
    # ================================
    def charger(self):

        for row in self.table.get_children():
            self.table.delete(row)

        transferts = historique_transferts()

        for t in transferts:
            self.table.insert("", "end", values=(
                t["code_envoi"],
                f'{t["nom_expediteur"]} {t["prenom_expediteur"]}',
                f'{t["nom_destinataire"]} {t["prenom_destinataire"]}',
                t["pays_destination"],
                t["ville_destination"],
                t["montant"],
                t["date_envoi"],
                t["statut"]
            ))


if __name__ == "__main__":
    GuiHistoriqueTransfert().mainloop()
