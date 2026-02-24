import customtkinter as ctk
from tkinter import messagebox
from agence import get_nom_agence
from gui_reçus import GuiReçus
from gui_expediteur import GuiExpediteur
from gui_destinataire import GuiDestinataire
from gui_destination import GuiDestination
from gui_transfert import GuiTransfert
from gui_paiement import GuiPaiement
from gui_historique_transfert import GuiHistoriqueTransfert
from gui_historique_paiement import GuiHistoriquePaiement

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MenuPrincipal(ctk.CTk):

    def __init__(self, agent):
        super().__init__()

        self.agent = agent

        self.title("Menu Principal - Agence")
        self.geometry("800x600")

        # ====== Nom Agence depuis la base ======
        nom_agence = get_nom_agence()

        ctk.CTkLabel(self,
                     text=nom_agence,
                     font=("Arial", 22, "bold")).pack(pady=10)
     
    
        # ====== Agent connecté ======
        ctk.CTkLabel(self,
                     text=f"Agent connecté : {agent['nom_agent']} {agent['prenom_agent']}",
                     font=("Arial", 14)).pack(pady=5)

        # ====== Frame Boutons ======
        frame = ctk.CTkFrame(self)
        frame.pack(pady=30, padx=40, fill="both", expand=True)
        
        # Ligne 1
        ctk.CTkButton(frame,
                      text="Expéditeurs",
                      command=self.ouvrir_expediteur,
                      width=200).grid(row=0, column=0, padx=20, pady=15)

        ctk.CTkButton(frame,
                      text="Destinataires",
                      command=self.ouvrir_destinataire,
                      width=200).grid(row=0, column=1, padx=20, pady=15)

        # Ligne 2
        ctk.CTkButton(frame,
                      text="Destinations",
                      command=self.ouvrir_destination,
                      width=200).grid(row=1, column=0, padx=20, pady=15)

        ctk.CTkButton(frame,
                      text="Transfert",
                      command=self.ouvrir_transfert,
                      width=200).grid(row=1, column=1, padx=20, pady=15)

        # Ligne 3
        ctk.CTkButton(frame,
                      text="Paiement",
                      command=self.ouvrir_paiement,
                      width=200).grid(row=2, column=0, padx=20, pady=15)

        ctk.CTkButton(frame,
                      text="Historique Transferts",
                      command=self.ouvrir_historique_transfert,
                      width=200).grid(row=2, column=1, padx=20, pady=15)

        # Ligne 4
        ctk.CTkButton(frame,
                      text="Historique Paiements",
                      command=self.ouvrir_historique_paiement,
                      width=200).grid(row=3, column=0, padx=20, pady=15)
        
        #======= RECU GENERE =================
        ctk.CTkButton(frame, 
                     text="Reçus",
                     command=self.ouvrir_reçus,
                     width=200).grid(row=3, column=1, padx=20, pady=15)

              

        ctk.CTkButton(frame,
                      text="Déconnexion",
                      command=self.deconnexion,
                      fg_color="red",
                      width=200).grid(row=3, column=2, padx=20, pady=15)

    # ====== Fonctions ouverture ======

    def ouvrir_expediteur(self):
        GuiExpediteur().mainloop()

    def ouvrir_destinataire(self):
        GuiDestinataire().mainloop()

    def ouvrir_destination(self):
        GuiDestination().mainloop()

    def ouvrir_transfert(self):
        GuiTransfert().mainloop()

    def ouvrir_paiement(self):
        GuiPaiement().mainloop()

    def ouvrir_historique_transfert(self):
        GuiHistoriqueTransfert().mainloop()

    def ouvrir_historique_paiement(self):
        GuiHistoriquePaiement().mainloop()
    
    def ouvrir_reçus(self):
        GuiReçus().mainloop()
        

    def deconnexion(self):
        confirm = messagebox.askyesno("Déconnexion",
                                      "Voulez-vous vous déconnecter ?")
        if confirm:
            self.destroy()
            from login import Login
            Login().mainloop()
