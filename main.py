import os
import discord
from discord.ext import commands
import math
from scipy.stats import poisson

# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté à Discord!')

@bot.command(name='c')
async def calculate_combined_odds(ctx, *, valeurs):
    """Calcule l'expression combinée pour plusieurs valeurs"""
    try:
        valeurs = [float(v) for v in valeurs.split()]
        
        result = 1
        for v in valeurs:
            if v == 0:
                await ctx.send("Erreur: Division par zéro détectée!")
                return
            result *= (1 - (1/v))
        
        if result == 1:
            await ctx.send("Erreur: Résultat indéfini (division par zéro)!")
            return
            
        result = 1 / (1 - result)
        await ctx.send(f"Le résultat est: {result:.4f}")
        
    except ValueError:
        await ctx.send("Erreur: Veuillez entrer des nombres valides séparés par des espaces.")
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command(name='l')
async def calculate_single_odds(ctx, valeur: float):
    """Calcule l'expression 1 / (1 - 1 / valeur)"""
    try:
        if valeur == 0:
            await ctx.send("Erreur: Division par zéro!")
            return
        if valeur == 1:
            await ctx.send("Erreur: Résultat indéfini!")
            return
            
        result = 1 / (1 - 1 / valeur)
        await ctx.send(f"Le résultat est: {result:.4f}")
        
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command(name='kel')
async def kelly_criterion(ctx, cote_observee: float, cote_reelle: float):
    """Calcule le critère de Kelly"""
    try:
        if cote_observee <= 1 or cote_reelle <= 0:
            await ctx.send("Erreur: Les cotes doivent être positives et la cote observée > 1")
            return
            
        kelly_criterion = 1/cote_reelle - (1-1/cote_reelle)/(cote_observee-1)
        
        kelly_100 = kelly_criterion * 100
        kelly_2 = kelly_100 / 2
        kelly_4 = kelly_100 / 4
        kelly_6 = kelly_100 / 6
        kelly_8 = kelly_100 / 8
        
        await ctx.send(f"**Critère de Kelly:**\n"
                      f"Kelly : {kelly_100:.2f}%\n"
                      f"Kelly /2 : {kelly_2:.2f}%\n"
                      f"Kelly /4 : {kelly_4:.2f}%\n"
                      f"Kelly /6 : {kelly_6:.2f}%\n"
                      f"Kelly /8 : {kelly_8:.2f}%")
                      
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command(name='xg')
async def calculate_xg(ctx, variable: float):
    """Calcule l'expression xG"""
    try:
        exponent = variable * 10
        if exponent > 700:  # Éviter l'overflow
            await ctx.send("Erreur: Valeur trop grande, risque de débordement!")
            return
            
        base_calc = 0.9 ** exponent
        if base_calc == 1:
            await ctx.send("Erreur: Division par zéro!")
            return
            
        result = 1 / (1 - base_calc)
        await ctx.send(f"Le résultat xG pour {variable} est: {result:.4f}")
        
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command(name='mmax')
async def mise_maximale(ctx, cote: float, gain_max: float = 100):
    """Calcule la mise maximale pour un gain donné"""
    try:
        if cote <= 1:
            await ctx.send("Erreur: La cote doit être supérieure à 1!")
            return
            
        mise = gain_max / (cote - 1)
        await ctx.send(f"**Mise maximale:**\n"
                      f"Cote: {cote}\n"
                      f"Gain max: {gain_max}\n"
                      f"Mise max: {mise:.2f}")
                      
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command(name='mpto')
async def calcul_mpto(ctx, cote1: float, cote2: float):
    """Calcule les mises proportionnelles"""
    try:
        if cote1 <= 0 or cote2 <= 0:
            await ctx.send("Erreur: Les cotes doivent être positives!")
            return
            
        A3, B3 = cote1, cote2
        
        # Vérifier les conditions pour éviter division par zéro
        condition_A = 2 - ((1/A3 + 1/B3) - 1) * A3
        condition_B = 2 - ((1/A3 + 1/B3) - 1) * B3
        
        if abs(condition_A) < 0.0001 or abs(condition_B) < 0.0001:
            await ctx.send("Erreur: Division par zéro dans le calcul!")
            return
        
        M_A = (2 * A3) / condition_A
        M_B = (2 * B3) / condition_B
        
        await ctx.send(f"**Calcul MPTO:**\n"
                      f"Cote 1 ({A3}): {M_A:.4f}\n"
                      f"Cote 2 ({B3}): {M_B:.4f}")
                      
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command(name='poi')
async def poisson_analysis(ctx, k: int, lambda_decimal: float):
    """Analyse de Poisson pour les buts"""
    try:
        if k < 0 or lambda_decimal <= 0:
            await ctx.send("Erreur: k doit être positif et lambda_decimal > 0!")
            return
            
        target_prob = 1 / lambda_decimal
        
        if target_prob <= 0 or target_prob >= 1:
            await ctx.send("Erreur: Probabilité cible invalide!")
            return
        
        # Recherche binaire pour trouver lambda
        lower_bound = 0.01
        upper_bound = 1000
        epsilon = 0.00001
        iterations = 0
        max_iterations = 1000
        
        while upper_bound - lower_bound > epsilon and iterations < max_iterations:
            lambda_test = (lower_bound + upper_bound) / 2
            prob_less_than_k = poisson.cdf(k-1, lambda_test)
            prob_at_least_k = 1 - prob_less_than_k
            
            if prob_at_least_k > target_prob:
                upper_bound = lambda_test
            else:
                lower_bound = lambda_test
            iterations += 1
        
        lambda_guess = (lower_bound + upper_bound) / 2
        
        # Calculs des xG
        xg_open_play = 0.9 * lambda_guess
        xg_penalty = 0.075 * lambda_guess
        xg_assists = 0.67 * lambda_guess
        
        await ctx.send(f"**Analyse Poisson:**\n"
                      f"L'équipe marquera: {lambda_guess:.5f} buts\n"
                      f"xG jeu ouvert: {xg_open_play:.5f}\n"
                      f"xG penalty: {xg_penalty:.5f}\n"
                      f"xA passes: {xg_assists:.5f}")
                      
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command(name='sub')
async def substitution_calc(ctx, valeur: float, temps: int, D2: float = 1):
    """Calcul pour les substitutions"""
    try:
        if temps <= 0 or temps >= 90:
            await ctx.send("Erreur: Le temps doit être entre 0 et 90 minutes!")
            return
        if valeur <= 0:
            await ctx.send("Erreur: La valeur doit être positive!")
            return
            
        tim = temps / 90
        time_ratio = (1 - tim) / tim
        
        if tim == 0:
            await ctx.send("Erreur: Division par zéro (temps = 0)!")
            return
            
        # Calcul complexe
        inv_orbit = 1 / valeur
        term1 = inv_orbit
        term2 = inv_orbit * D2 * time_ratio
        term3 = inv_orbit * inv_orbit * D2 * time_ratio
        
        denominator = term1 + term2 - term3
        
        if abs(denominator) < 0.0001:
            await ctx.send("Erreur: Division par zéro dans le calcul!")
            return
            
        result = 1 / denominator
        
        await ctx.send(f"**Calcul substitution:**\n"
                      f"Valeur: {valeur}\n"
                      f"Temps: {temps} min\n"
                      f"D2: {D2}\n"
                      f"Résultat: {result:.4f}")
                      
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command(name='help_custom')
async def help_command(ctx):
    """Affiche l'aide personnalisée"""
    help_text = """
**🤖 Commandes disponibles:**

`!c <valeurs>` - Calcul combiné (ex: !c 2.5 3.0 1.8)
`!l <valeur>` - Calcul simple (ex: !l 2.5)
`!kel <cote_obs> <cote_reelle>` - Critère de Kelly
`!xg <variable>` - Calcul xG
`!mmax <cote> [gain_max]` - Mise maximale
`!mpto <cote1> <cote2>` - Mises proportionnelles  
`!poi <k> <lambda>` - Analyse Poisson
`!sub <valeur> <temps> [D2]` - Calcul substitution
`!help_custom` - Cette aide

**Exemple d'utilisation:**
`!kel 2.10 2.00` - Calcule Kelly pour ces cotes
`!c 1.5 2.0 3.5` - Calcule la cote combinée
    """
    await ctx.send(help_text)

def get_discord_token():
    """Récupère le token Discord de façon sécurisée"""
    # Essayer la variable d'environnement
    token = os.environ.get('izy')
    if token:
        return token
    
    # Essayer un fichier token.txt (non recommandé pour la production)
    try:
        with open('token.txt', 'r') as f:
            token = f.read().strip()
            if token:
                return token
    except FileNotFoundError:
        pass
    
    # Demander à l'utilisateur
    print("=" * 50)
    print("⚠️  TOKEN DISCORD REQUIS ⚠️")
    print("=" * 50)
    print("1. Allez sur https://discord.com/developers/applications")
    print("2. Créez une application et un bot")
    print("3. Copiez le token du bot")
    print("4. Activez 'Message Content Intent'")
    print("=" * 50)
    
    token = input("Entrez votre token Discord: ").strip()
    
    if not token:
        print("❌ Aucun token fourni!")
        return None
    
    # Sauvegarder dans un fichier pour la prochaine fois
    try:
        with open('token.txt', 'w') as f:
            f.write(token)
        print("✅ Token sauvegardé dans token.txt")
    except:
        print("⚠️  Impossible de sauvegarder le token")
    
    return token

def main():
    """Fonction principale"""
    print("🚀 Démarrage du bot Discord...")
    
    # Vérifier les dépendances
    try:
        import discord
        import scipy
        print("✅ Toutes les dépendances sont installées")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("Installez avec: pip install discord.py scipy")
        return
    
    # Obtenir le token
    token = get_discord_token()
    if not token:
        print("❌ Impossible de démarrer sans token!")
        input("Appuyez sur Entrée pour quitter...")
        return
    
    # Démarrer le bot
    try:
        print("🔄 Connexion en cours...")
        bot.run(token)
    except discord.LoginFailure:
        print("❌ Token invalide!")
        try:
            os.remove('token.txt')
            print("🗑️  Fichier token supprimé")
        except:
            pass
        input("Appuyez sur Entrée pour quitter...")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
