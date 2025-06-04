#!/bin/bash

# Script de déploiement automatique pour Site Web Help Robot
# Ce script crée automatiquement le fichier .env et déploie l'application

echo "🚀 Début du déploiement en production..."

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher des messages colorés
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérification des prérequis
check_requirements() {
    print_status "Vérification des prérequis..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker n'est pas installé"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose n'est pas installé"
        exit 1
    fi
    
    print_status "Prérequis OK ✓"
}

# Génération d'une clé secrète Django
generate_secret_key() {
    python3 -c "
import secrets
import string
alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
password = ''.join(secrets.choice(alphabet) for i in range(50))
print(password)
"
}

# Récupération de l'adresse IP du serveur
get_server_ip() {
    # Essayer plusieurs méthodes pour obtenir l'IP publique
    local ip=""
    
    # Méthode 1: via curl
    ip=$(curl -s https://ipinfo.io/ip 2>/dev/null)
    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        echo "$ip"
        return
    fi
    
    # Méthode 2: via wget
    ip=$(wget -qO- https://ipecho.net/plain 2>/dev/null)
    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        echo "$ip"
        return
    fi
    
    # Méthode 3: IP locale si échec
    ip=$(hostname -I | awk '{print $1}')
    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        print_warning "Impossible d'obtenir l'IP publique, utilisation de l'IP locale: $ip"
        echo "$ip"
        return
    fi
    
    # Fallback
    echo "127.0.0.1"
}

# Création du fichier .env
create_env_file() {
    print_status "Création du fichier .env..."
    
    # Génération des valeurs
    SECRET_KEY=$(generate_secret_key)
    DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
    SERVER_IP=$(get_server_ip)
    
    # Demander le port si nécessaire
    read -p "Port d'écoute du serveur web (défaut: 8000): " WEB_PORT
    WEB_PORT=${WEB_PORT:-8000}
    
    # Création du fichier .env
    cat > .env << EOF
# Configuration de production générée automatiquement
# $(date)

# Django
SECRET_KEY=${SECRET_KEY}
DEBUG=False

# Base de données PostgreSQL
DB_NAME=help_robot_db
DB_USER=help_robot_user
DB_PASSWORD=${DB_PASSWORD}

# Serveur
SERVER_IP=${SERVER_IP}
WEB_PORT=${WEB_PORT}
ALLOWED_HOSTS=${SERVER_IP},localhost,127.0.0.1

# Optionnel: domaine personnalisé
# CUSTOM_DOMAIN=votre-domaine.com
EOF

    print_status "Fichier .env créé avec succès"
    print_status "IP du serveur détectée: ${SERVER_IP}"
    print_status "Port configuré: ${WEB_PORT}"
}

# Mise à jour des settings Django
update_django_settings() {
    print_status "Vérification des settings Django..."
    
    # Créer le répertoire settings s'il n'existe pas
    SETTINGS_DIR="myproject/settings"
    if [ ! -d "$SETTINGS_DIR" ]; then
        print_status "Création du répertoire settings..."
        mkdir -p "$SETTINGS_DIR"
        touch "$SETTINGS_DIR/__init__.py"
    fi
    
    print_status "Settings Django vérifiés"
}

# Arrêt des conteneurs existants
stop_existing_containers() {
    print_status "Arrêt des conteneurs existants..."
    docker-compose down --volumes --remove-orphans 2>/dev/null || true
}

# Construction et démarrage
build_and_start() {
    print_status "Construction des images Docker..."
    docker-compose build --no-cache
    
    print_status "Démarrage des services..."
    docker-compose up -d
    
    # Attendre que la base de données soit prête
    print_status "Attente de la base de données..."
    sleep 10
    
    # Migrations de la base de données
    print_status "Application des migrations..."
    docker-compose exec web python manage.py migrate
    
    # Création du superutilisateur si nécessaire
    print_status "Vérification du superutilisateur..."
    docker-compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Aucun superutilisateur trouvé')
    exit(1)
" 2>/dev/null || {
    print_warning "Aucun superutilisateur trouvé. Création..."
    docker-compose exec web python manage.py createsuperuser --noinput --username admin --email admin@example.com || true
}
}

# Vérification du déploiement
check_deployment() {
    print_status "Vérification du déploiement..."
    
    # Vérifier que les conteneurs sont en marche
    if docker-compose ps | grep -q "Up"; then
        SERVER_IP=$(grep "SERVER_IP=" .env | cut -d'=' -f2)
        WEB_PORT=$(grep "WEB_PORT=" .env | cut -d'=' -f2)
        
        print_status "✅ Déploiement réussi!"
        echo ""
        echo "🌐 Votre site est accessible à l'adresse:"
        echo "   http://${SERVER_IP}:${WEB_PORT}"
        echo ""
        echo "📊 Panel d'administration:"
        echo "   http://${SERVER_IP}:${WEB_PORT}/admin"
        echo ""
        echo "🔧 Commandes utiles:"
        echo "   - Voir les logs: docker-compose logs -f"
        echo "   - Arrêter: docker-compose down"
        echo "   - Redémarrer: docker-compose restart"
        echo ""
    else
        print_error "Échec du déploiement. Vérifiez les logs avec: docker-compose logs"
        exit 1
    fi
}

# Fonction principale
main() {
    echo "🤖 Déploiement Site Web Help Robot - Production"
    echo "=============================================="
    echo ""
    
    check_requirements
    create_env_file
    update_django_settings
    stop_existing_containers
    build_and_start
    check_deployment
}

# Gestion des signaux pour arrêt propre
trap 'print_error "Déploiement interrompu"; exit 1' INT TERM

# Exécution du script principal
main "$@"