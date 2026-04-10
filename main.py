import requests
import os

class jeu:
    def __init__(self):
        # On garde les URLs des deux magasins
        self.url_epic = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=fr&country=FR&allowCountries=FR"
        self.url_steam = "https://store.steampowered.com/api/featuredcategories"
        self.webook = os.getenv("DISCORD_WEBHOOK")

    def notifier(self, message):
        """Envoie un message sur Discord si le Webhook existe"""
        if self.webook:
            payload = {"content": message}
            requests.post(self.webook, json=payload)
        else:
            print("❌ Erreur : DISCORD_WEBHOOK non trouvé.")

    def verif_epic(self):
        """Vérifie les jeux gratuits sur Epic Games"""
        print("--- Vérification Epic Games ---")
        re = requests.get(self.url_epic)
        donnees = re.json()
        liste_jeu = donnees['data']['Catalog']['searchStore']['elements']
        
        for item in liste_jeu:
            nom_du_jeu = item['title']
            prix = item['price']['totalPrice']['discountPrice']
            
            # Gestion de l'image sécurisée
            image = item['keyImages'][0]['url'] if item.get('keyImages') else "https://fr.wikipedia.org/wiki/Epic_Games"
            
            if prix == 0:
                print(f"Trouvé (Epic): {nom_du_jeu}")
                self.notifier(f"🎁 **EPIC GAMES** : {nom_du_jeu} est GRATUIT !\n{image}")

    def verif_steam(self):
        """Vérifie les jeux gratuits sur Steam"""
        print("--- Vérification Steam ---")
        re = requests.get(self.url_steam)
        donnees = re.json()
        
        # On cherche dans la catégorie 'specials' (les promos)
        promos = donnees.get('specials', {}).get('items', [])
        
        for jeu in promos:
            # On cherche le -100% (gratuit pour une durée limitée)
            if jeu.get('discount_percent') == 100:
                nom = jeu.get('name')
                app_id = jeu.get('id')
                lien = f"https://store.steampowered.com/app/{app_id}"
                image = jeu.get('header_image')
                
                print(f"Trouvé (Steam): {nom}")
                self.notifier(f"🎁 **STEAM** : {nom} est GRATUIT !\n{lien}\n{image}")

# --- LANCEMENT DU ROBOT ---
mon_robot = jeu()
mon_robot.verif_epic()   # Lance la vérification Epic
mon_robot.verif_steam()  # Lance la vérification Steam