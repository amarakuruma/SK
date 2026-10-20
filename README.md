# SK — Mode & élégance

Landing page de vente SK (pièces uniques, livraison à Conakry, commande sur WhatsApp).

- `index.html` : la page complète (aucune installation nécessaire)
- `photos/` : photos des tenues et des clientes
- `logo-sk*` : logo SK (monogramme couture), dont la version ronde pour les photos de profil

## Mettre à jour

- **Pièce vendue** : dans `index.html`, en bas, `const VENDUES = [];` → ajouter son numéro, ex. `[3]` ou `[3, 7]`. La fiche affiche « Vendue ».
- **Numéro WhatsApp** : ligne `const WHATSAPP = '224614903303';`.
- **Liens de pub suivis** : ajouter `?src=fb` ou `?src=tiktok` à l'adresse du site ; la référence apparaît dans chaque message WhatsApp reçu.

## Une page par pièce

`p/<N°>/` contient une page par pièce (photo, prix, bouton WhatsApp). Chaque message WhatsApp envoyé depuis le site contient le lien de la pièce choisie (`https://sk-mode.netlify.app/p/6/`) : WhatsApp affiche sa photo en aperçu, donc Saran voit tout de suite quelle tenue la cliente veut.

Ces pages sont créées par `generer-fiches.py` à partir de `index.html`. Netlify le lance tout seul à chaque mise à jour (`netlify.toml`). En local : `python3 generer-fiches.py`.

## Mise en ligne

Netlify → « Import a Git repository » → GitHub → ce dépôt. Commande de build et dossier de publication déjà réglés dans `netlify.toml`.
