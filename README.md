# GitHub explorer

Questo script permette di:
* visualizzare un menu di scelta (singola);
* esplorare un lista di repository GitHub;
* estrarre delle informazioni per ciascuno quali:
    - Nome
    - url (già conosciuta)
    - Licenza in uso
    - Linguaggio principale
* connettersi ad un DB e salvare le informazioni all'interno;
* leggere dal DB e effettuare nuove operazioni;





## Opzioni da passare

1. -c, --crawl - Crawl of the file in input (see -i, --input-file)
2. -d, --dry-run - Dry Run crawl, no information is persisted
3. -i, --input-file - Input file containing the list of repositories to be crawled
4. -p, --perform-check - 