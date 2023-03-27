# ING301 prosjekt - Del C

I del C av prosjektet skal dere implementere en REST API for en SmartHus sky-tjeneste ved bruk av rammeverket [FastAPI](https://fastapi.tiangolo.com).

## Setup og startkode

Start-koden for prosjektet finnes i dette github repository: 

https://github.com/selabhvl/ing301-projectpartC-startcode.git

some dere kan bruke som mal (**Use as Template**) tilsvarende tidligere startkode for prosjektene. Startkoden inneholder klasser for devices og sensors samt konstruksjon av smarthus demo eksemplet. 

Om dere vil, kan dere utskifte klassene med de klassene som dere selv har utvikler i prosjekt A og prosjekt B. Det er da viktig at klassene implementeres som modeller i [Pydantic](https://docs.pydantic.dev/usage/models/) siden dette brukes av FastAPI som et underliggende rammeverk.

I prosjekt C skal vi ikke integrere data-basen delen. Det er planen at dette skal gjøres i Del D sammen med implementasjon av klient-applikasjoner som bruker REST API'et utviklet i denne del av prosjektet.

For å kunne bruke FastAPI rammeverket skal dette først installeres. Dette kan gjøres med:

```
pip3 install "fastapi[all]"
```

For å kjøre tjenesten som utvikles og for å laste den på nytt når der gjøre endringer i koden kan følgende brukes:

```
uvicorn main:app --reload
```

som gjør at tjenesten settes i drift ved å bruke `uvicorn` web-tjeneren. 

Litt avhengig av Python installasjon kan det være nødvendig å starte web-tjeneren med:

```
python -m uvicorn main:app --reload
```

Det er også mulig å kjøre web-tjenesten i debug-modus ved å kjørt `main.py` scriptet. 

Kommandoene ovenfor må utføres i mappen som inneholder filen `main.py`

For løsning av oppgaven kan det være en god ide å søke inspiration i eksemplet fra forelesningen i uke 12 der FastAPI ble brukt til å utvikle en REST API for sykkelcomputer eksemplet:

Koden finnes her:

https://github.com/selabhvl/ing301public/tree/main/examples/12_restapi_webservices

Der er også hjelp å hente i dokumentasjonen for FastAPI som finnes via:

https://fastapi.tiangolo.com

REST API'et skal dere teste ved å skrive noen test i [Postman](https://www.postman.com) verktøyet som også blev demonstrert på forelesningen i uke 11. 

https://hvl.instructure.com/courses/22301/pages/opptak-fastapi-og-postman?module_item_id=638477 

Testene i Postman for sykkelcomputer eksemplet kan gjerne brukes som inspiration: 

https://github.com/selabhvl/ing301public/blob/main/examples/12_restapi_webservices/BCRestAPI.postman_collection.json

De kan importeres inn i Postman.

## REST API endepunkter

REST API'et som skal utvikles skal gjøre det mulig å hente informasjon om oppbygging av smarthuset viat følgene API endepunkter som alle skal returnere et svar i JSON-format.

- `GET smarthouse/` - information on the smart house

- `GET smarthouse/floor` - information on all floors

- `GET smarthouse/floor/{fid}` - information about a floor given by `fid` 
 
- `GET smarthouse/floor/{fid}/room` - information about all rooms on a given floor `fid`

- `GET smarthouse/floor/{fid}/room/{rid}`- information about a specific room `rid` on a given floor `fid`

API'et ha følgende endepunkter for tilgang til devices

- `GET smarthouse/device` - information on all devices
- `GET smarthouse/device/{did}` - information for a given device `did`

API'et ha følgende endepunkter for tilgang til sensorer

- `GET smarthouse/sensor/{did}/current` - get current sensor measurement for sensor `did`

- `POST smarthouse/sensor/{did}/current` - add measurement for sensor `did`

- `GET smarthouse/sensor/{did}/values?limit=n` - get `n` latest available measurements for sensor `did`. If query parameter not present, then all available measurements.

- `DELETE smarthouse/sensor/{did}/oldest` - delete oldest measurements for sensor `did`

API'et ha følgende endepunkter for tilgang til aktuatorer

- `GET smarthouse/actuator/{did}/current` - get current state for actuator `did`

- `PUT smarthouse/device/{did}` - update current state for actuator `did`


## Levering av prosjekt

Følgende skal leveres

- Linke til github repository med implemetasjon av tjenesten
- Eksportert test-collection fil fra Postman skal legge repository
