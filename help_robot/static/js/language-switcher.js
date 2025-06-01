// static/js/language-switcher.js
class LanguageSwitcher {
    constructor() {
        this.currentLang = document.documentElement.lang || 'en';
        this.init();
        console.log('LanguageSwitcher initialized, current language:', this.currentLang);
    }
    
    init() {
        // SEULEMENT les boutons dans le header avec la classe 'language-btn'
        document.querySelectorAll('#language-switcher .language-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const targetLang = e.target.getAttribute('data-lang');
                console.log('Header language button clicked:', targetLang, 'Current:', this.currentLang);
                if (targetLang !== this.currentLang) {
                    this.switchLanguage(targetLang);
                }
            });
        });
    }
    
    switchLanguage(targetLang) {
        const currentUrl = window.location;
        const currentPath = currentUrl.pathname;
        const currentSearch = currentUrl.search;
        const currentHash = currentUrl.hash;
        
        console.log('Current path:', currentPath);
        
        let newPath = this.translatePath(currentPath, targetLang);
        console.log('New path:', newPath);
        
        const newUrl = newPath + currentSearch + currentHash;
        console.log('Redirecting to:', newUrl);
        
        window.location.href = newUrl;
    }
    
    translatePath(currentPath, targetLang) {
        // Nettoyer le chemin - enlever les doubles slashes
        let cleanPath = currentPath.replace(/\/+/g, '/');
        if (cleanPath === '') cleanPath = '/';
        
        console.log('Clean path:', cleanPath);
        
        // Enlever TOUS les préfixes de langue existants (/en/, /fr/, etc.)
        let pathWithoutLang = this.removeLanguagePrefix(cleanPath);
        console.log('Path without language prefix:', pathWithoutLang);
        
        // Ajouter le nouveau préfixe de langue
        if (targetLang === 'fr') {
            return '/fr' + pathWithoutLang;
        } else {
            return '/en' + pathWithoutLang;
        }
    }
    
    removeLanguagePrefix(path) {
        // Liste des préfixes de langue possibles
        const languagePrefixes = ['/en/', '/fr/', '/es/', '/de/'];
        
        for (let prefix of languagePrefixes) {
            if (path.startsWith(prefix)) {
                let newPath = path.substring(prefix.length - 1); // Garde le '/' final
                return newPath === '' ? '/' : newPath;
            }
        }
        
        // Si aucun préfixe trouvé, retourner le chemin original
        return path;
    }
    
    // Méthode pour ajouter facilement d'autres langues dans le futur
    addLanguage(langCode, langName, flagEmoji) {
        const switcher = document.getElementById('language-switcher');
        if (!switcher) return;
        
        const btn = document.createElement('button');
        btn.setAttribute('data-lang', langCode);
        btn.className = 'language-btn btn btn-sm btn-outline-light';
        btn.innerHTML = `${flagEmoji} ${langName}`;
        btn.addEventListener('click', (e) => {
            const targetLang = e.target.getAttribute('data-lang');
            if (targetLang !== this.currentLang) {
                this.switchLanguage(targetLang);
            }
        });
        switcher.appendChild(btn);
    }
}

// Initialiser le changeur de langue quand la page est chargée
document.addEventListener('DOMContentLoaded', function() {
    window.languageSwitcher = new LanguageSwitcher();
});