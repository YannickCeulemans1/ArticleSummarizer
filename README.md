## Summarizer
De summarizer zal met het getrained model een samenvatting genereren van een gegeven artikel. 

Wanneer er iets fout gaat in het summarizer programma zal deze foutmelding getoond worden op de webapp. 

#### Functie attributen 
articleLink = De webpagina link van het artikel waarvan de samenvatting moet genereerd worden
ArticleSumRatio = Het aantal zinnen van het artikel wordt gedeeld door dit integer, het resultaat is het aantal zinnen dat de gegenereerde samenvatting zal bevatten. 
minSumLen = Minimum lengte dat de samenvatting moet zijn onafhankelijk van de berekende lengte.
maxSumLen = Maximum lengte dat de samenvatting mag zijn onafhankelijk van de berekende lengte.

## Webscraper
De webscraper zal nakijken ofdat de meegegeven link een bruikbare link is, 
wanneer dit zo is wordt het artikel van de webpagina gehaald en weggeschreven naar "data/article.txt", 
dit bestand zal het summarizer programma dan ook gebruiken voor de samenvatting te maken. 

Wanneer er iets fout gaat in het webscraper programma zal deze foutmelding getoond worden op de webapp. 

#### Functie attributen 
articleLink = De webpagina link van het artikel waarvan de samenvatting moet genereerd worden.


