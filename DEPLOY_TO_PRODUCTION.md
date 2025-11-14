# Déployer sur fitgang.fr

Vos changements sont dans la branche: `claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n`

## Option 1: Via SSH (Recommandé)

1. **Connectez-vous en SSH à votre serveur:**
   ```bash
   ssh votre_username@fitgang.fr
   ```

2. **Allez dans le répertoire de l'application:**
   ```bash
   cd ~/fitgang_app/saas
   # OU le chemin mentionné dans votre cPanel
   ```

3. **Téléchargez les derniers changements:**
   ```bash
   git fetch origin
   git checkout claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n
   git pull origin claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n
   ```

4. **Nettoyez le cache Python:**
   ```bash
   find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
   find . -name "*.pyc" -delete 2>/dev/null
   ```

5. **Redémarrez le serveur:**
   ```bash
   touch tmp/restart.txt
   # OU via cPanel: Setup Python App → Restart
   ```

## Option 2: Via cPanel Git Deployment

1. Connectez-vous à **cPanel**
2. Allez dans **"Git Version Control"**
3. Trouvez votre repository
4. Cliquez sur **"Manage"**
5. Cliquez sur **"Pull or Deploy"** → **"Update from Remote"**
6. Sélectionnez la branche: `claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n`
7. Allez dans **"Setup Python App"** → **"Restart"**

## Option 3: Merger dans main (Pour déploiement automatique)

Si votre serveur auto-déploie depuis la branche main:

```bash
git checkout main
git merge claude/saccra-fitgang-complete-overhaul-0186TzukF7j2eifnrXaNd51n
git push origin main
```

Puis redémarrez via cPanel.

## ✅ Pour vérifier que ça fonctionne:

Après le déploiement, testez ces pages:
- https://fitgang.fr/profile (profil modernisé)
- https://fitgang.fr/dashboard (système de poids)
- https://fitgang.fr/programmes/programme-seche (page produit Apple)
- https://fitgang.fr/calculators (calculateurs corrigés)

**Videz le cache navigateur après chaque test!**
