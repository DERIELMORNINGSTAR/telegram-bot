"""
==============================================
  BOT TELEGRAM POLYVALENT - DOUCE APOCALYPSE
==============================================
Prérequis : pip install python-telegram-bot==20.7
"""

import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ──────────────────────────────────────────────
#  CONFIGURATION
# ──────────────────────────────────────────────

BOT_TOKEN = "METS_TON_TOKEN_ICI"   # ← remplace par le token de @BotFather

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
#  DONNÉES ANIME (personnalisables)
# ──────────────────────────────────────────────

ANIME_GENRES = {
    "⚔️ Action / Shonen": [
        "Demon Slayer (Kimetsu no Yaiba)",
        "Jujutsu Kaisen",
        "Attack on Titan (Shingeki no Kyojin)",
        "One Piece",
        "Bleach: TYBW",
    ],
    "🔮 Surnaturel / Fantasy": [
        "Fullmetal Alchemist: Brotherhood",
        "Re:Zero",
        "Overlord",
        "That Time I Got Reincarnated as a Slime",
        "The Ancient Magus' Bride",
    ],
    "🏯 Historique / Samouraï": [
        "Vinland Saga",
        "Rurouni Kenshin",
        "Dororo",
        "Sword of the Stranger (Film)",
        "Angolmois",
    ],
    "🎭 Drame / Seinen": [
        "Berserk",
        "Monster",
        "Vagabond (Manga)",
        "Neon Genesis Evangelion",
        "Claymore",
    ],
}

ANIME_CITATIONS = [
    ("« La vraie solitude, c'est d'avoir peur de former des liens. »", "Naruto Uzumaki"),
    ("« Un homme qui ne peut pas pleurer est un homme à moitié vivant. »", "Hughes — FMA"),
    ("« Les monstres n'existent pas. Ce sont les hommes qui créent les monstres. »", "Yoichi Hiruma"),
    ("« Abandonne, et tu mourras. Avance, et tu vivras. »", "Attack on Titan"),
    ("« Plus la nuit est sombre, plus les étoiles brillent. »", "Yato — Noragami"),
]

FAQ_DATA = {
    "Quels genres d'anime couvrez-vous ?": "Nous couvrons l'action, le surnaturel, le fantasy, l'historique et le seinen. Tape /genres pour voir la liste complète.",
    "Comment vous contacter ?": "Utilise la commande /contact pour nous joindre directement.",
    "Quand sortent les nouvelles vidéos ?": "Nos vidéos sortent chaque semaine. Reste à l'écoute !",
    "Comment suggérer un anime ?": "Utilise /suggestion suivi du nom de l'anime. Ex: /suggestion Chainsaw Man",
}


# ──────────────────────────────────────────────
#  CLAVIER PRINCIPAL (menu persistant)
# ──────────────────────────────────────────────

def menu_principal():
    clavier = [
        [KeyboardButton("🏠 Accueil"), KeyboardButton("🎌 Genres Anime")],
        [KeyboardButton("💬 Citation du Jour"), KeyboardButton("❓ FAQ")],
        [KeyboardButton("📬 Contact"), KeyboardButton("ℹ️ À Propos")],
    ]
    return ReplyKeyboardMarkup(clavier, resize_keyboard=True, one_time_keyboard=False)


# ──────────────────────────────────────────────
#  COMMANDES
# ──────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    texte = (
        f"✨ *Bienvenue, {user.first_name} !*\n\n"
        "🌸 Je suis le bot officiel de la chaîne *Douce Apocalypse*.\n"
        "Ton guide dans l'univers de l'anime — action, surnaturel, fantasy et plus encore.\n\n"
        "Utilise le menu ci-dessous ou les commandes :\n"
        "• /genres — Explorer les genres anime\n"
        "• /citation — Citation inspirante\n"
        "• /faq — Questions fréquentes\n"
        "• /suggestion — Suggérer un anime\n"
        "• /contact — Nous contacter\n"
        "• /aide — Aide complète"
    )
    await update.message.reply_text(texte, parse_mode="Markdown", reply_markup=menu_principal())


async def aide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = (
        "📖 *LISTE DES COMMANDES*\n\n"
        "/start — Démarrer le bot\n"
        "/genres — Voir les genres anime disponibles\n"
        "/citation — Recevoir une citation anime\n"
        "/faq — Questions fréquentes\n"
        "/suggestion [titre] — Suggérer un anime\n"
        "/contact — Nous envoyer un message\n"
        "/aide — Afficher cette aide\n\n"
        "_Tu peux aussi utiliser les boutons du menu !_"
    )
    await update.message.reply_text(texte, parse_mode="Markdown", reply_markup=menu_principal())


async def genres(update: Update, context: ContextTypes.DEFAULT_TYPE):
    boutons = [
        [InlineKeyboardButton(genre, callback_data=f"genre:{genre}")]
        for genre in ANIME_GENRES.keys()
    ]
    boutons.append([InlineKeyboardButton("🔙 Retour accueil", callback_data="accueil")])
    clavier = InlineKeyboardMarkup(boutons)
    await update.message.reply_text(
        "🎌 *Choisis un genre pour voir des recommandations :*",
        parse_mode="Markdown",
        reply_markup=clavier,
    )


async def citation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    texte_cite, auteur = random.choice(ANIME_CITATIONS)
    texte = f"🌟 *Citation du Jour*\n\n{texte_cite}\n\n— _{auteur}_"
    await update.message.reply_text(texte, parse_mode="Markdown")


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    boutons = [
        [InlineKeyboardButton(question[:40] + "…" if len(question) > 40 else question,
                              callback_data=f"faq:{i}")]
        for i, question in enumerate(FAQ_DATA.keys())
    ]
    boutons.append([InlineKeyboardButton("🔙 Retour", callback_data="accueil")])
    clavier = InlineKeyboardMarkup(boutons)
    await update.message.reply_text(
        "❓ *Foire Aux Questions — Choisis ta question :*",
        parse_mode="Markdown",
        reply_markup=clavier,
    )


async def suggestion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        titre = " ".join(context.args)
        await update.message.reply_text(
            f"✅ Merci pour ta suggestion : *{titre}* !\n"
            "Notre équipe va l'étudier. 🙏",
            parse_mode="Markdown",
        )
        # Ici tu peux ajouter un log ou envoyer la suggestion à un admin
        logger.info(f"Suggestion reçue de {update.effective_user.first_name}: {titre}")
    else:
        await update.message.reply_text(
            "💡 *Comment suggérer un anime ?*\n\n"
            "Tape : `/suggestion [Titre de l'anime]`\n\n"
            "Exemple : `/suggestion Chainsaw Man`",
            parse_mode="Markdown",
        )


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = (
        "📬 *Nous Contacter*\n\n"
        "🔗 *Chaîne YouTube :* [Douce Apocalypse](https://youtube.com)\n"
        "📧 *Email :* contact@doucapocalypse.com\n"
        "💬 *Telegram admin :* @ton_pseudo_admin\n\n"
        "_N'hésite pas à nous écrire pour toute question !_"
    )
    await update.message.reply_text(texte, parse_mode="Markdown", disable_web_page_preview=True)


async def a_propos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = (
        "🌸 *À Propos de Douce Apocalypse*\n\n"
        "Nous sommes une chaîne dédiée à l'univers de l'anime :\n"
        "• Analyses et reviews approfondies\n"
        "• Recommandations par genre\n"
        "• Actualités anime\n"
        "• Discussions et débats\n\n"
        "_Rejoins notre communauté et plonge dans l'univers animé !_ 🎌"
    )
    await update.message.reply_text(texte, parse_mode="Markdown")


# ──────────────────────────────────────────────
#  GESTION DES BOUTONS INLINE
# ──────────────────────────────────────────────

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Genre sélectionné
    if data.startswith("genre:"):
        genre_nom = data[6:]
        animes = ANIME_GENRES.get(genre_nom, [])
        liste = "\n".join(f"  • {a}" for a in animes)
        texte = f"*{genre_nom}*\n\nAnimes recommandés :\n{liste}"
        bouton_retour = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Autres genres", callback_data="genres")],
            [InlineKeyboardButton("🏠 Accueil", callback_data="accueil")],
        ])
        await query.edit_message_text(texte, parse_mode="Markdown", reply_markup=bouton_retour)

    # Retour aux genres
    elif data == "genres":
        boutons = [
            [InlineKeyboardButton(genre, callback_data=f"genre:{genre}")]
            for genre in ANIME_GENRES.keys()
        ]
        boutons.append([InlineKeyboardButton("🔙 Accueil", callback_data="accueil")])
        await query.edit_message_text(
            "🎌 *Choisis un genre :*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(boutons),
        )

    # FAQ sélectionnée
    elif data.startswith("faq:"):
        index = int(data[4:])
        questions = list(FAQ_DATA.keys())
        reponses = list(FAQ_DATA.values())
        if 0 <= index < len(questions):
            texte = f"❓ *{questions[index]}*\n\n{reponses[index]}"
            bouton_retour = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Autres questions", callback_data="faq")],
            ])
            await query.edit_message_text(texte, parse_mode="Markdown", reply_markup=bouton_retour)

    # Retour FAQ
    elif data == "faq":
        boutons = [
            [InlineKeyboardButton(question[:40] + "…" if len(question) > 40 else question,
                                  callback_data=f"faq:{i}")]
            for i, question in enumerate(FAQ_DATA.keys())
        ]
        boutons.append([InlineKeyboardButton("🔙 Retour", callback_data="accueil")])
        await query.edit_message_text(
            "❓ *Choisis ta question :*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(boutons),
        )

    # Accueil
    elif data == "accueil":
        texte = (
            "🏠 *Menu Principal*\n\n"
            "Utilise les boutons ci-dessous ou les commandes du menu !"
        )
        await query.edit_message_text(texte, parse_mode="Markdown")


# ──────────────────────────────────────────────
#  GESTION DES MESSAGES TEXTE (menu clavier)
# ──────────────────────────────────────────────

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = update.message.text.strip()

    if texte == "🏠 Accueil":
        await start(update, context)
    elif texte == "🎌 Genres Anime":
        await genres(update, context)
    elif texte == "💬 Citation du Jour":
        await citation(update, context)
    elif texte == "❓ FAQ":
        await faq(update, context)
    elif texte == "📬 Contact":
        await contact(update, context)
    elif texte == "ℹ️ À Propos":
        await a_propos(update, context)
    else:
        await update.message.reply_text(
            "🤔 Je n'ai pas compris. Utilise /aide ou les boutons du menu.",
            reply_markup=menu_principal(),
        )


# ──────────────────────────────────────────────
#  GESTION DES ERREURS
# ──────────────────────────────────────────────

async def erreur_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Erreur : %s", context.error, exc_info=context.error)


# ──────────────────────────────────────────────
#  LANCEMENT DU BOT
# ──────────────────────────────────────────────

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Commandes
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aide", aide))
    app.add_handler(CommandHandler("genres", genres))
    app.add_handler(CommandHandler("citation", citation))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("suggestion", suggestion))
    app.add_handler(CommandHandler("contact", contact))

    # Boutons inline
    app.add_handler(CallbackQueryHandler(callback_handler))

    # Messages texte (menu)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Erreurs
    app.add_error_handler(erreur_handler)

    print("✅ Bot démarré. Appuie sur Ctrl+C pour arrêter.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
