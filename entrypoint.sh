#!/bin/bash

# Script d'entrée pour le container Django en production
set -e

echo "🚀 Démarrage du container Help Robot..."

# Fonction pour attendre que la base de données soit prête
wait_for_db() {
    echo "⏳ Attente de la base de données..."
    
    until python manage.py check --database default; do
        echo "Base de données non disponible, attente..."
        sleep 2
    done
    
    echo "✅ Base de données prête!"
}

# Fonction pour appliquer les migrations
apply_migrations() {
    echo "🔄 Application des migrations..."
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    echo "✅ Migrations appliquées!"
}

# Fonction pour collecter les fichiers statiques
collect_static() {
    echo "📦 Collection des fichiers statiques..."
    python manage.py collectstatic --noinput --clear
    echo "✅ Fichiers statiques collectés!"
}

# Fonction pour créer un superutilisateur par défaut si aucun n'existe
create_superuser() {
    echo "👤 Vérification du superutilisateur..."
    
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Création du superutilisateur par défaut...')
    User.objects.create_superuser(
        username='admin',
        email='admin@helprobot.local',
        password='admin123'
    )
    print('Superutilisateur créé: admin/admin123')
    print('⚠️  CHANGEZ LE MOT DE PASSE EN PRODUCTION!')
else:
    print('Superutilisateur déjà existant.')
"
}

# Fonction pour afficher les informations de démarrage
show_startup_info() {
    echo ""
    echo "🎉 Help Robot démarré avec succès!"
    echo "=================================="
    
    if [ "$DEBUG" = "True" ]; then
        echo "⚠️  Mode DEBUG activé"
    else
        echo "🔒 Mode PRODUCTION activé"
    fi
    
    echo "🌐 Serveur Django en écoute sur le port 8000"
    echo "📊 Administration: /admin"
    echo ""
    
    if [ -n "$SERVER_IP" ]; then
        echo "🔗 Accès externe: http://$SERVER_IP:${WEB_PORT:-8000}"
    fi
    
    echo "📋 Hosts autorisés: $ALLOWED_HOSTS"
    echo ""
}

# Exécution des étapes de démarrage
main() {
    # Attendre la base de données
    wait_for_db
    
    # Appliquer les migrations
    apply_migrations
    
    # Collecter les fichiers statiques
    collect_static
    
    # Créer un superutilisateur si nécessaire
    create_superuser
    
    # Afficher les informations de démarrage
    show_startup_info
    
    # Démarrer le serveur Django
    echo "🚀 Démarrage du serveur Django..."
    exec python manage.py runserver 0.0.0.0:8000
}

# Gestion des signaux pour arrêt propre
handle_signal() {
    echo ""
    echo "🛑 Arrêt du serveur Help Robot..."
    exit 0
}

trap handle_signal SIGTERM SIGINT

# Lancer le script principal
main "$@"