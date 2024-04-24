from App import	App

from Router import Router

if __name__ == "__main__":
    app = App()
    game = Router(app)
    app.mainloop()

# List of ttk widgets : https://www.pythontutorial.net/tkinter/tkinter-ttk/

# Mouvement du cavalier 👍
# Mouvement des pions 👍
# Fonction "get_pieces_on_case" 👍
# Fonction "get_allowed_squares" pour chaque piece (hors clouage) 👍
# Roque, grand Roque => Vérifier si roi est attaqué, si les cases de roque sont attaquées, si le roi et la tour n'ont jamais bougé 👍
# Prises 👍
# Prise en passant 👍
# Promotion => Menu, image des pièces les unes au-dessus des autres. Fond blanc => affiche une frame sur le canvas avec canvas.create_window qui contient les images 👍
# Distinction roque / grand roque dans les logs 👍
# Clouage 👍
# => Cavalier 👍
# => Tour 👍
# => Fou 👍
# => Reine 👍
# => Pion 👍
# Echecs => (attention, prendre en compte la prise en passant) ? 👍
#   => Pion 👍
#   => Tour 👍
#   => Fou 👍
#   => Cavalier 👍
#   => Reine 👍
#   => Mouvements du roi 👍
# => Echec du cavalier : 
#       - Cavalier peut être mangé (en tenant compte des clouages, etc..;)
#       - Sinon, échec et mat
# => Double échec :
#       - Roi peut bouger
#       - Sinon, échec et mat
# => Echec de la tour / du fou / de la reine :
#       - Roi peut bouger
#       - Piece peut être mangée
#       - Pièce peut s'interposer
#       - Sinon, échec et mat
# => Echec du pion :
#       - Pion peut être mangé
#       - Roi peut bouger
#       - Sinon, échec et mat
# Tour attaque roi => case entre la tour et le roi inaccessible, mais derrière le roi est accessible 👍
# Echec et mat 👍
# PAT 👍
# Insuffisance matérielle 👍
# 50 moves rule
# Nulle par répétition

