import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def c(ctx, *, valeurs):
    try:
        # Séparer les valeurs par espaces et les convertir en float
        valeurs = [float(v) for v in valeurs.split()]

        # Calculer l'expression 1 / (1 - (1 - (1/valeur1)) * (1 - (1/valeur2)) * ...)
        result = 1
        for v in valeurs:
            result *= (1 - (1/v))
        result = 1 / (1 - result)

        # Envoyer le résultat
        await ctx.send(f"Le résultat est: {result}")
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command()
async def l(ctx, valeur: float):
    try:
        # Calculer l'expression 1 / (1 - 1 / valeur)
        result = 1 / (1 - 1 / valeur)

        # Envoyer le résultat
        await ctx.send(f"Le résultat est: {result}")
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command()
async def kel(ctx, cote_observee: float, cote_reelle: float):
    try:
        kelly_criterion = 1/cote_reelle - (1-1/cote_reelle)/(cote_observee-1)

        # Calculer les différents résultats demandés
        kelly_100 = kelly_criterion * 100
        kelly_2 = kelly_100 / 2
        kelly_4 = kelly_100 / 4
        kelly_6 = kelly_100 / 6
        kelly_8 = kelly_100 / 8

                # Envoyer le résultat
        await ctx.send(f"Kelly : {kelly_100:.2f}\n"
                               f"Kelly /2 : {kelly_2:.2f}\n"
                               f"Kelly /4 : {kelly_4:.2f}\n"
                               f"Kelly /6 : {kelly_6:.2f}\n"    
                               f"Kelly /8 : {kelly_8:.2f}")
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command()
async def xg(ctx, variable: float):
    try:
        # Calculer l'expression 1 / (1 - 0.9 ** (variable * 10))
        result = 1 / (1 - 0.9 ** (variable * 10))

        # Envoyer le résultat
        await ctx.send(f"Le résultat pour la variable {variable} est: {result:.4f}")
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")



@bot.command(name="mmax")
async def mise_max(ctx, cote: float, gainmax: float = 100):
    try:
        # Vérification pour éviter une division par zéro
        if cote <= 1:
            await ctx.send("La cote doit être strictement supérieure à 1.")
            return

        # Calcul de la mise max
        mise = gainmax / (cote - 1)

        # Envoi du résultat
        await ctx.send(f"Pour une cote de {cote} et un gain max de {gainmax}, "
                       f"la mise maximale est: {mise:.2f}")
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command()
async def mpto(ctx, cote1: float, cote2: float):
    try:
        A3 = cote1
        B3 = cote2

        # Calculs des deux formules
        M_A = (2 * A3) / (2 - ((1 / A3 + 1 / B3) - 1) * A3)
        M_B = (2 * B3) / (2 - ((1 / A3 + 1 / B3) - 1) * B3)

        # Envoi des résultats
        await ctx.send(f"odds 1 ({A3}): {M_A:.4f}\n"
                       f"odds 2 ({B3}): {M_B:.4f}")
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

import math
from scipy.stats import poisson

import math
from scipy.stats import poisson

@bot.command()
async def poi(ctx, k: int, lambda_decimal: float):
    try:
        # On veut que P(X >= 1) = 1 / lambda_decimal
        target_prob = 1 / lambda_decimal

        # Plage de recherche pour lambda
        lower_bound = 0.01  # Valeur minimale possible pour lambda
        upper_bound = 1000  # Valeur maximale possible pour lambda
        epsilon = 0.00001  # Précision de la recherche

        # Recherche binaire
        while upper_bound - lower_bound > epsilon:
            lambda_test = (lower_bound + upper_bound) / 2
            prob_less_than_k = poisson.cdf(k-1, lambda_test)
            prob_at_least_k = 1 - prob_less_than_k

            # Ajuster les bornes en fonction du résultat
            if prob_at_least_k > target_prob:
                upper_bound = lambda_test  # Réduire la plage supérieure
            else:
                lower_bound = lambda_test  # Réduire la plage inférieure

        # Le lambda final trouvé
        lambda_guess = (lower_bound + upper_bound) / 2

        # Calcul des xG pour les différents types de buts
        xg_open_play = 0.9 * lambda_guess
        xg_penalty = 0.075 * lambda_guess
        xg_own_goals = 0.67 * lambda_guess

        # Envoi du résultat sous forme de message
        await ctx.send(f"L'équipe marquera {lambda_guess:.5f} buts.\n"
                       f"Le jeu ouvert marque {xg_open_play:.5f} xG.\n"
                       f"Le marqueur de penalty aura {xg_penalty:.5f} xG.\n"
                       f"Il y aura {xg_own_goals:.5f} xA a la passe.")

    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")

@bot.command()
async def sub(ctx, valeur: float, temps: int, D2: float = 1):
    try:
        tim = temps / 90
        Orbit = valeur
        time = tim

        result = 1 / ((1 / Orbit) + ((1 / Orbit) * D2 * ((1 - time) / time)) - (((1 / Orbit) * (1 / Orbit)) * D2 * ((1 - time) / time)))

        await ctx.send(f"Le résultat est: {result}")
    except Exception as e:
        await ctx.send(f"Erreur: {str(e)}")







token = os.environ['izy']
bot.run(token)
