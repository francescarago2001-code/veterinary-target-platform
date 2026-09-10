# veterinary-target-platform

Sito statico pubblicato con GitHub Pages.

## Deploy

- il sito è composto da file statici (`index.html`, `home.html`, `grazie.html`, CSS inline e risorse in `logo/`)
- il deploy è gestito automaticamente da GitHub Actions tramite `.github/workflows/deploy-pages.yml`
- il form usa Formspree per l’invio (`https://formspree.io/f/xkjnkeea`)

## Note

- non è necessario usare Render o un backend Python per il submit
- il file `app.py` è stato semplificato per servire i file statici in locale e non più per gestire `POST`
