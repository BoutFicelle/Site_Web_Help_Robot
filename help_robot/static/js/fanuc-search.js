// static/js/fanuc-search.js
class FanucSearchManager {
    constructor() {
        this.init();
        console.log('FanucSearchManager initialized');
    }
    
    init() {
        this.setupErrorLanguageSwitcher();
        this.setupQuickLanguageSwitches();
        this.setupSearchForm();
    }
    
    setupErrorLanguageSwitcher() {
        // Gérer les boutons radio pour changer la langue des erreurs
        const errorLangRadios = document.querySelectorAll('#error-language-switcher input[name="error_lang"]');
        const searchForm = document.getElementById('search-form');
        
        if (!errorLangRadios.length || !searchForm) {
            console.log('Error language switcher elements not found');
            return;
        }
        
        errorLangRadios.forEach(radio => {
            radio.addEventListener('change', (e) => {
                console.log('Error language changed to:', e.target.value);
                
                // Auto-submit quand la langue d'erreur change et qu'il y a une recherche
                const searchInput = document.querySelector('input[name="q"]');
                if (searchInput && searchInput.value.trim()) {
                    console.log('Auto-submitting search form with query:', searchInput.value);
                    searchForm.submit();
                }
            });
        });
    }
    
    setupQuickLanguageSwitches() {
        // Empêcher le LanguageSwitcher global d'interférer avec les boutons d'erreur
        document.querySelectorAll('.quick-lang-switch').forEach(link => {
            link.addEventListener('click', (e) => {
                console.log('Quick language switch clicked:', e.target.href);
                // Empêcher le LanguageSwitcher de capturer ce clic
                e.stopPropagation();
            });
        });
    }
    
    setupSearchForm() {
        const searchForm = document.getElementById('search-form');
        const searchInput = document.querySelector('input[name="q"]');
        
        if (!searchForm || !searchInput) {
            console.log('Search form elements not found');
            return;
        }
        
        // Ajouter un indicateur de chargement lors de la recherche
        searchForm.addEventListener('submit', (e) => {
            const submitButton = searchForm.querySelector('button[type="submit"]');
            if (submitButton) {
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Searching...';
                submitButton.disabled = true;
                
                // Restaurer le bouton après un délai (au cas où la soumission échoue)
                setTimeout(() => {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }, 5000);
            }
        });
        
        // Focus automatique sur le champ de recherche si vide
        if (!searchInput.value.trim()) {
            searchInput.focus();
        }
        
        // Suggestions de recherche au survol des exemples
        this.setupSearchSuggestions();
    }
    
    setupSearchSuggestions() {
        // Ajouter des suggestions cliquables
        document.querySelectorAll('code').forEach(codeElement => {
            const suggestionText = codeElement.textContent;
            
            // Rendre les codes d'exemple cliquables
            codeElement.style.cursor = 'pointer';
            codeElement.style.textDecoration = 'underline';
            codeElement.title = `Click to search for "${suggestionText}"`;
            
            codeElement.addEventListener('click', (e) => {
                const searchInput = document.querySelector('input[name="q"]');
                if (searchInput) {
                    searchInput.value = suggestionText;
                    searchInput.focus();
                    console.log('Search suggestion clicked:', suggestionText);
                }
            });
        });
    }
    
    // Méthode utilitaire pour mettre à jour les résultats sans rechargement complet
    updateErrorLanguage(newLang) {
        const currentUrl = new URL(window.location);
        currentUrl.searchParams.set('error_lang', newLang);
        
        // Rediriger vers la nouvelle URL
        window.location.href = currentUrl.toString();
    }
    
    // Méthode pour obtenir la langue actuelle des erreurs depuis l'URL
    getCurrentErrorLanguage() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('error_lang') || 'en';
    }
    
    // Méthode pour obtenir la requête de recherche actuelle
    getCurrentQuery() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('q') || '';
    }
    
    // Méthode pour ajouter une animation aux cartes d'erreur
    animateErrorCards() {
        const errorCards = document.querySelectorAll('.card');
        errorCards.forEach((card, index) => {
            // Animation d'apparition progressive
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.3s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100); // Délai progressif pour chaque carte
        });
    }
}

// Initialiser le gestionnaire de recherche Fanuc quand la page est chargée
document.addEventListener('DOMContentLoaded', function() {
    // Vérifier qu'on est bien sur la page de recherche Fanuc
    if (document.getElementById('search-form')) {
        window.fanucSearchManager = new FanucSearchManager();
        
        // Animer les cartes d'erreur si elles existent
        const errorCards = document.querySelectorAll('.card');
        if (errorCards.length > 0) {
            window.fanucSearchManager.animateErrorCards();
        }
    }
});