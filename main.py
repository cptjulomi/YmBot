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
            await ctx.send("
