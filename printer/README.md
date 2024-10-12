🖨️ PrinterApp - L'Application d'Impression Tout-en-Un !
Bienvenue dans PrinterApp : une application simple, puissante et intuitive qui vous permet d'imprimer des documents avec style et flexibilité ! 🚀

🎯 Fonctionnalités Principales :
Sélection d'imprimante : Choisissez parmi vos imprimantes disponibles en un clic !
Impression multi-format : Support pour les fichiers PDF, DOCX, TXT, JPEG, PNG, et bien d'autres.
Aperçu avant impression : Consultez vos fichiers avant de lancer une impression.
Planification d'impression ⏳ : Programmez vos impressions à une date et heure spécifique.
Qualité d'impression : Sélectionnez la qualité d'impression parmi trois niveaux (Économie, Normal, Haute qualité).
Impression Recto-Verso 🖨️ : Gagnez du papier avec l'option recto-verso, si disponible sur votre imprimante.
Ajout de filigrane : Personnalisez vos impressions avec un texte en filigrane.
Historique d'impression : Consultez les documents récemment imprimés.
Sauvegarde et chargement des configurations 💾 : Enregistrez vos paramètres d'impression préférés et rechargez-les à tout moment.
Notification email 📧 : Recevez une notification par email après chaque impression réussie.
Ajout de plusieurs fichiers : Imprimez plusieurs documents en une seule session.
📦 Installation
Pour installer PrinterApp, suivez ces étapes simples :

1. Cloner le projet
bash
Copier le code
git clone https://github.com/darkiiuseai/printerapp.git
cd printerapp
2. Créer et activer un environnement virtuel
bash
Copier le code
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
3. Installer les dépendances
Installez les bibliothèques nécessaires via requirements.txt :

bash
Copier le code
pip install -r requirements.txt
4. Configurer les paramètres d'email
Si vous souhaitez utiliser la fonctionnalité de notification par email, ouvrez le fichier PrinterApp.py et remplacez les informations d'authentification email dans cette section :

python
Copier le code
server.login("your_email@gmail.com", "your_password")
⚠️ Ne partagez jamais vos informations personnelles sur un dépôt public ! Utilisez des variables d'environnement pour les projets de production.

🚀 Utilisation
Lancer l'application
bash
Copier le code
python PrinterApp.py
Interface Graphique (GUI)
Une fois l'application lancée, vous verrez une interface intuitive avec les options suivantes :

Ajouter un fichier : Sélectionnez un ou plusieurs fichiers à imprimer.
Aperçu avant impression : Consultez un aperçu de la liste des fichiers avant de lancer l'impression.
Planification : Programmez une date et une heure pour l'impression (format : JJ/MM/AAAA HH
).
Qualité et recto-verso : Sélectionnez les options d'impression comme la qualité et l'activation du recto-verso.
Filigrane : Entrez un texte pour ajouter un filigrane sur vos impressions.
Historique : Consultez et gérez l'historique des impressions.
🛠️ Fonctionnalités Avancées
1. Sauvegarde des Configurations
Vous pouvez sauvegarder et charger vos configurations d'impression préférées dans un fichier print_config.json. Cela inclut les paramètres de l'imprimante, la qualité, et les options d'impression personnalisées.

2. Notifications Email
Activez les notifications par email pour être informé après chaque impression réussie. Configurez votre compte Gmail dans le script pour recevoir des alertes.

📋 Fichiers Importants
print_config.json : Sauvegarde des configurations d'impression.
user_preferences.txt : Stocke les préférences utilisateurs (ex : imprimante par défaut).
README.md : Ce fichier génial qui vous guide à travers l'utilisation de l'application !
💻 Dépendances
Voici la liste des bibliothèques Python nécessaires pour faire fonctionner l'application :

plaintext
Copier le code
Pillow==9.0.0
PyPDF2==2.10.0
python-docx==0.8.11
pywin32==302
Pour installer les dépendances manuellement, lancez :

bash
Copier le code
pip install Pillow PyPDF2 docx pywin32
📝 Auteurs
darkiifr - Développeur principal
📜 Licence
Ce projet est sous licence MIT. Veuillez consulter le fichier LICENSE pour plus d'informations.

🖼️ Aperçu de l'interface
<p align="center"> <img src="https://via.placeholder.com/800x400.png?text=PrinterApp+Interface" alt="PrinterApp GUI"> </p>
🎉 À venir !
Support pour plus de formats de fichiers : CSV, XLSX, etc.
Gestion des imprimantes réseau.
Intégration avec Google Cloud Print.
Amélioration du système de planification avec des rappels.
Maintenant, imprimez en toute sérénité avec PrinterApp ! 🎉

Légende des Emojis :
🖨️ : Imprimante
🚀 : Lancement rapide
💾 : Sauvegarde
📧 : Notification email
⏳ : Planification