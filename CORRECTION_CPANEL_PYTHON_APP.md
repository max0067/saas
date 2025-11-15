# 🔧 CORRECTION DE LA CONFIGURATION CPANEL - FITGANG.FR

## ❌ PROBLÈME IDENTIFIÉ

Passenger charge depuis le **MAUVAIS répertoire**:
```
ACTUEL: /home/wrbh3411/public_html/flask-version (ancienne version)
CORRECT: /home/wrbh3411/fitgang_app/saas (version à jour)
```

Le `.htaccess` a été corrigé, MAIS **cPanel a sa propre configuration qui l'override**.

---

## ✅ SOLUTION: Modifier dans cPanel → Setup Python App

### ÉTAPE 1: Se connecter à cPanel

1. Allez sur: https://panel.o2switch.fr (ou votre URL cPanel)
2. Connectez-vous avec vos identifiants o2switch

### ÉTAPE 2: Trouver "Setup Python App"

1. Dans cPanel, cherchez la section **"SOFTWARE"**
2. Cliquez sur **"Setup Python App"** ou **"Python App"**
3. Vous verrez une liste d'applications Python

### ÉTAPE 3: Identifier l'application fitgang.fr

Cherchez l'application qui correspond à:
- **Application URL**: `/` ou `https://fitgang.fr`
- **Application Root**: Probablement `/home/wrbh3411/public_html/fitgang.fr` ❌

### ÉTAPE 4: Modifier la configuration

1. Cliquez sur l'**icône crayon (✏️)** ou **"Edit"** à droite de l'application
2. Vous allez voir un formulaire avec:

**AVANT (configuration incorrecte):**
```
Application root: /home/wrbh3411/public_html/fitgang.fr
Application URL: /
Application startup file: passenger_wsgi.py
Application Entry point: application
Python version: 3.6.x ou autre
```

**CHANGEZ EN:**
```
Application root: /home/wrbh3411/fitgang_app/saas
Application URL: /
Application startup file: passenger_wsgi.py
Application Entry point: application
Python version: 3.9+ (ou la plus récente disponible)
```

3. Cliquez sur **"Update"** ou **"Mettre à jour"**

### ÉTAPE 5: Redémarrer l'application

1. Retournez à la liste des applications Python
2. Trouvez fitgang.fr
3. **SI** l'application est "Running" (en vert):
   - Cliquez sur **"STOP APPLICATION"**
   - Attendez 30 secondes
   - Cliquez sur **"START APPLICATION"**

4. **SI** l'application est "Stopped" (en rouge):
   - Cliquez sur **"START APPLICATION"**

### ÉTAPE 6: Vérifier que ça marche

1. Attendez 1 minute complète
2. Ouvrez votre navigateur
3. Allez sur: https://fitgang.fr/blog
4. Faites **Ctrl+Shift+R** pour vider le cache
5. Vérifiez:
   - ✅ 3 cartes par ligne (pas 2)
   - ✅ Images visibles

6. Testez aussi:
   - https://fitgang.fr/workouts (ne devrait plus faire erreur 500)
   - https://fitgang.fr/profile/photos (ne devrait plus faire erreur 500)

---

## 🔍 VÉRIFICATION SSH APRÈS MODIFICATION

Après avoir modifié dans cPanel, vérifiez en SSH:

```bash
# Attendre que Passenger redémarre
sleep 30

# Vérifier les processus Python
ps aux | grep python | grep -v grep
```

**VOUS DEVRIEZ VOIR:**
```
/usr/bin/python3 ... (PAS /public_html/flask-version/3.6/!)
```

**SI VOUS VOYEZ ENCORE:**
```
/home/wrbh3411/virtualenv/public_html/flask-version/3.6/bin/python3.6_bin
```

Alors la modification cPanel n'a pas été prise en compte. Vérifiez que vous avez:
1. Bien sauvegardé (Update)
2. Bien fait STOP puis START
3. Modifié la BONNE application (celle pour fitgang.fr, pas une autre)

---

## ⚠️ SI VOUS NE TROUVEZ PAS "Setup Python App" dans cPanel

Cherchez aussi:
- "Python Selector"
- "Application Python"
- "Passenger Apps"
- Ou contactez le support o2switch en leur disant:

  *"Je dois changer l'Application Root de mon app Python fitgang.fr
  de /home/wrbh3411/public_html/fitgang.fr
  vers /home/wrbh3411/fitgang_app/saas"*

---

## 📊 POURQUOI ÇA NE MARCHE PAS EN LIGNE DE COMMANDE?

Sur o2switch/cPanel, la configuration Passenger est gérée par cPanel.

Même si on modifie le `.htaccess`, cPanel a une **base de données interne**
qui stocke la configuration de chaque Python App.

Cette config cPanel **override** le .htaccess.

C'est pour ça que `pkill python` ne résout rien: Passenger redémarre
automatiquement avec la config stockée dans cPanel.

**IL FAUT ABSOLUMENT PASSER PAR L'INTERFACE CPANEL!**

---

## ✅ RÉSUMÉ

1. ✅ Connectez-vous à cPanel
2. ✅ Setup Python App
3. ✅ Éditer l'app fitgang.fr
4. ✅ Changer Application root → `/home/wrbh3411/fitgang_app/saas`
5. ✅ Update
6. ✅ STOP puis START
7. ✅ Tester https://fitgang.fr/blog

C'est la SEULE solution! 🚀
