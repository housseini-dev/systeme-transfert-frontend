import customtkinter as ctk
from tkinter import ttk
from paiement import historique_paiements


class GuiHistoriquePaiement(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("Historique des Paiements")
        self.geometry("1000x600")
        self.resizable(False, False)


        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Titre
        titre = ctk.CTkLabel(
            self,
            text="HISTORIQUE DES PAIEMENTS",
            font=("Arial", 20, "bold")
        )
        titre.pack(pady=20)

        # Frame tableau
        frame_table = ctk.CTkFrame(self)
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        # Création Treeview
        colonnes = (
            "ID Paiement",
            "Code_envoi",
            "Montant_paye",
            "Date_paiement",
            "Statut_paiement"
        )

        self.table = ttk.Treeview(
            frame_table,
            columns=colonnes,
            show="headings"
        )

        for col in colonnes:
            self.table.heading(col, text=col)
            self.table.column(col, width=150, anchor="center")

        self.table.pack(fill="both", expand=True)

        # Charger données
        self.charger_donnees()

    # ================================
    # Charger les paiements
    # ================================
    def charger_donnees(self):

        for row in self.table.get_children():
            self.table.delete(row)

        paiements = historique_paiements()

        for p in paiements:
            self.table.insert("", "end", values=(
                p["id_paiement"],
                p["code_envoi"],
                p["montant_paye"],
                p["date_paiement"],
                p["statut_paiement"]
            ))


if __name__ == "__main__":
    GuiHistoriquePaiement().mainloop()
