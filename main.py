import requests
import os
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv

# On charge le .env pour le Webhook
load_dotenv()

class Jeu:
    def __init__(self):
        self.url_epic = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=fr&country=FR&allowCountries=FR"
        self.url_steam = "https://store.steampowered.com/api/featuredcategories"
        self.webhook = os.getenv("DISCORD_WEBHOOK")
        

        # --- INITIALISATION SQLITE ---
        self.conn = sqlite3.connect("historique_jeux.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS historique (
                cle TEXT PRIMARY KEY, 
                date_ajout TEXT
            )
        ''')
        self.conn.commit()

    def est_deja_notifie(self, cle):
        """Vérifie si le jeu est déjà dans la base de données"""
        self.cursor.execute("SELECT 1 FROM historique WHERE cle = ?", (cle,))
        return self.cursor.fetchone() is not None

    def sauvegarder_jeu(self, cle):
        """Enregistre le jeu pour ne plus le notifier"""
        date_du_jour = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT INTO historique VALUES (?, ?)", (cle, date_du_jour))
        self.conn.commit()

    def nettoyage(self):
        """Supprime les vieilles entrées de plus de 30 jours"""
        limite = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        self.cursor.execute("DELETE FROM historique WHERE date_ajout < ?", (limite,))
        self.conn.commit()

    def notifier(self, message):
        if self.webhook:
            payload = {"content": message}
            try:
                requests.post(self.webhook, json=payload, timeout=10)
            except Exception as e:
                print(f"❌ Erreur Webhook : {e}")
        else:
            print("❌ Erreur : DISCORD_WEBHOOK non trouvé.")

    def verif_epic(self):
        print("--- Vérification Epic Games ---")
        try:
            re = requests.get(self.url_epic, timeout=10)
            donnees = re.json()
            liste_jeu = donnees['data']['Catalog']['searchStore']['elements']
            
            for item in liste_jeu:
                nom_du_jeu = item['title']
                prix = item['price']['totalPrice']['discountPrice']
                
                # On crée une clé unique (Epic n'a pas toujours d'ID simple, le nom suffit)
                cle = f"EPIC_{nom_du_jeu}"
                
                if prix == 0 and not self.est_deja_notifie(cle):
                    image = item['keyImages'][0]['url'] if item.get('keyImages') else ""
                    print(f"✨ Nouveau jeu gratuit (Epic): {nom_du_jeu}")
                    
                    self.notifier(f"🎁 **EPIC GAMES** : {nom_du_jeu} est GRATUIT !\n{image}")
                    self.sauvegarder_jeu(cle)
                else:
                    if prix == 0: print(f"ℹ️ Déjà notifié : {nom_du_jeu}")

        except Exception as e:
            print(f"❌ Erreur Epic : {e}")

    def verif_steam(self):
        print("--- Vérification Steam ---")
        try:
            re = requests.get(self.url_steam, timeout=10)
            donnees = re.json()
            promos = donnees.get('specials', {}).get('items', [])
            
            for jeu in promos:
                if jeu.get('discount_percent') == 100:
                    nom = jeu.get('name')
                    app_id = str(jeu.get('id'))
                    cle = f"STEAM_{app_id}" # Utiliser l'AppID est plus précis
                    
                    if not self.est_deja_notifie(cle):
                        lien = f"https://store.steampowered.com/app/{app_id}"
                        image = jeu.get('header_image')
                        print(f"✨ Nouveau jeu gratuit (Steam): {nom}")
                        
                        self.notifier(f"🎁 **STEAM** : {nom} est GRATUIT !\n{lien}\n{image}")
                        self.sauvegarder_jeu(cle)
                    else:
                        print(f"ℹ️ Déjà notifié : {nom}")

        except Exception as e:
            print(f"❌ Erreur Steam : {e}")

# --- LANCEMENT ---
if __name__ == "__main__":
    mon_robot = Jeu()
    mon_robot.nettoyage()    # On nettoie la base
    mon_robot.verif_epic()   # On check Epic
    mon_robot.verif_steam()  # On check Steam