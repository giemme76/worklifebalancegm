# OfficePresence

OfficePresence è un'applicazione web che aiuta i dipendenti a monitorare il rispetto della policy di presenza in ufficio e smart working della propria azienda.

L'obiettivo è sapere in ogni momento:

- quanti giorni di presenza sono richiesti nell'anno;
- quanti giorni sono già stati effettuati;
- quanti ne mancano per raggiungere il target;
- se si è in linea con la percentuale di smart working prevista.

L'applicazione è pensata come **login-free**: ogni utente viene identificato tramite un codice univoco generato automaticamente.

---

## Funzionalità

- Configurazione iniziale dell'azienda
- Ricerca automatica del sito aziendale
- Individuazione della sede principale
- Impostazione della percentuale di Smart Working
- Calcolo automatico delle presenze richieste
- Calendario annuale delle presenze
- Dashboard con andamento e obiettivi
- Simulazione dei giorni futuri
- Recupero sessione tramite codice univoco

---

## Come funziona

### Primo accesso

L'utente inserisce:

- Nome azienda
- Sede (proposta automaticamente)
- Percentuale di Smart Working
- Giorni lavorativi settimanali

Al termine viene generato un codice personale.

Esempio:

```
SW-8F2K-7LQ9
```

Il browser memorizza il codice tramite cookie.

Non è richiesta alcuna registrazione.

---

## Tecnologie

Backend

- Python 3.13
- FastAPI
- SQLAlchemy
- MySQL

Frontend

- React
- TailwindCSS

Testing

- pytest
- pytest-cov
- httpx

---

## Struttura del progetto

```
app/
    api/
    services/
    models/
    repositories/
    utils/

tests/
    api/
    services/
    repositories/

docs/

README.md
```

---

## Roadmap

### MVP

- [ ] Creazione sessione
- [ ] Dashboard
- [ ] Calendario
- [ ] Inserimento presenze
- [ ] Calcolo obiettivo annuale

### Versione 2

- [ ] Simulatore
- [ ] Notifiche
- [ ] Esportazione Excel/PDF
- [ ] Dashboard Team

### Versione 3

- [ ] AI Planner
- [ ] Benchmark aziende
- [ ] API pubbliche

---

# Unit Test

Il progetto utilizza **pytest**.

## Avvio dei test

```bash
pytest
```

Con copertura:

```bash
pytest --cov=app
```

---

## Test previsti

### Calcolo obiettivo annuale

Verifica che il numero di giorni di presenza venga calcolato correttamente in base alla percentuale di smart working.

Esempi:

- 40% Smart → 60% presenza
- 60% Smart → 40% presenza

---

### Calcolo giorni mancanti

Verifica:

- giorni effettuati
- giorni mancanti
- percentuale corrente

---

### Simulazione

Controlla che aggiungendo una presenza futura vengano aggiornati:

- obiettivo
- percentuale
- giorni residui

---

### Calendario

Verifica il corretto conteggio di:

- Ufficio
- Smart Working
- Ferie
- Permessi
- Malattia

---

### Sessione

Test su:

- generazione UUID
- recupero tramite codice
- cookie valido
- cookie scaduto

---

### API

Test degli endpoint:

```
GET /dashboard

POST /attendance

GET /calendar

POST /simulation

GET /session/{code}
```

---

## Obiettivo di copertura

Target minimo:

```
Coverage > 90%
```

con particolare attenzione alla logica di business del calcolo delle presenze.
