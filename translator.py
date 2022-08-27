class language():
    
    def read():
        french_words = ["Démarrer","Paramètres","Crédits","Quitter","Commandes Clavier","Configurer Clavier","Appuyez sur une touche pour aller à droite","Sauter avec Touche C\nSe déplacer avec Flèches\nChanger de Gravité avec X et Direction de la Flèche"]
        english_words = ["Start","Settings","About","Leave","Keyboard Commands","Configure Keyboard","Press a key to go right","Jump with C Key\nMove with Arrows\nChange Gravity with X and Arrow Direction"]

        with open("language.txt") as reader:
            Language_Selected = reader.read()
            reader.close()
        if Language_Selected == "Français":
            return french_words
        if Language_Selected == "English":
            return english_words
    