# TrainPilot natív Android befejezése – elsődleges AI Studio utasítás

A meglévő, nagyrészt megvalósult natív Kotlin/Jetpack Compose Android telefon +
Wear OS kódbázist kell folytatnod. A kiemelt hátralévő feladatok:
natív UI, tényleges gomb-/nézet-/ViewModel-/repository-bekötések,
funkcióparitás, mentés/migráció és készülékes igazolás.
NE generálj új WebView-wrapper alkalmazást vagy üres funkciópótló képernyőket.

## A legfrissebb kötelező UI döntés
Az alkalmazás tetején ÖT főmenü, mindegyik teljes oldal:
**Kezdőlap | Edzés | Napló | Egészség | Programok**.
Felettük vagy mellettük HÁROM kisebb, minden főoldalról elérhető gomb:
**Beállítások | Naptár | Coach**. Ezek tényleges teljes oldalt vagy,
ha a feladat indokolja, teljes magasságú lapot nyitnak. A Naptár és a
részletes Coach teljes oldal; a Beállítások főnézete is teljes oldal.
Részletes szerződés: docs/NAVIGATION_5_PLUS_3.md.
Nincs jelenleg negyedik kis gomb. A Progresszió a Coach vagy Napló része.

## Források rangsora
1. A valódi megvalósítás: android/ (natív migráció, SHA 648e9710).
   Megtartani és javítani kell a phone/Wear/shared modulokat, a Compose
   képernyőket, ViewModel-eket, Room/DataStore tárolást, háttérszolgáltatásokat,
   Health Connect/Samsung, GPS, Wear és Google szinkronfolyamatokat.
2. Funkcionális alap: reference/stable-main/www és docs/FEATURES.hu.md.
   A régi éles WebView 1.3.71/2735 működő képességei nem veszhetnek el.
3. Újabb UI/viselkedés: reference/pr279-webview/www és implementation/.
   Nem szabad a WebView fájlokat natív képernyőként beemelni:
   a funkciókat Compose-ra és valódi state/bekötésekre kell átültetni.
4. Vizuál: reference/pr277-design/references/01-settings.png ... 08-programs.png.
   Nyolc valódi dizájn-referenciakép; nem kész app, nem működési bizonyíték.
5. Natív 24-nézetes UI source-binding szerződés:
   docs/reference/native/design/final-ui-ux/ és forrásaudit:
   docs/reference/audits/. Ezek korábbi, ellenőrizendő állapotot írnak le.

A docs/reference/HISTORICAL_MASTER_SPEC_2x4.md RÉGEBBI dokumentum;
kizárólag funkcióleltár és biztonsági referencia. Navigációban ez a
fájl (és minden régi 2×4 / alsó dock leírás) NEM irányadó.

## Nyolc célterület
1. Beállítások: profil, témák/nyelvek HU/EN/DE/RO, timer, Wear,
   engedélyek, Health/Google integráció, mentés és visszaállítás.
2. Edzésindítás: program/nap/ciklus, valódi gyakorlat-előnézet,
   quick/programozott indítás, valódi órás handoff vagy őszinte hiányállapot.
3. Egészségforrások: Health Connect/Samsung engedély, valódi
   utolsó sikeres szinkron, forrás és hiányzó adatok megkülönböztetése.
4. Aktív edzés: súly/ismétlés/sorozat, RIR, előző érték, pihenőidő,
   haptika, OK/visszavonás, pause/finish és tartós mentés.
5. Kültéri GPS mérés: idő/táv/szenzor, jogosultság, route, pause/resume.
6. Teljes képernyős térkép: mentett útvonalak és korrekt állapotok.
7. Napló/PR: részletek, szűrők, teljesítmény, progresszió és fotók.
8. Programok: kompakt programnap-kártyák, edit/tervezés/ciklus és
   működő edzésindítás.

## Nem alkuképes integrációs szerződések
- Egyetlen edzés-/timer-owner a telefon és az óra között, offline
  visszaszinkronizálás; nincs dupla mérés vagy elvesző edzés.
- A telefonról indított konkrét tervezett edzésnap Wear-en indulása
  NEM bizonyított pusztán távoli activity megnyitással. Kell ACK és teszt.
- Health adatforrások engedélyezését, frissítését, provenance-ét ne hamisítsd.
- Google Drive/Calendar engedély, ütközéskezelés, retry és idempotencia;
  ne legyen csendes felülírás.
- Régi adat migráció: LegacyWebViewMigrator.kt,
  LegacyLocalStorageReader.kt, BackupRestoreManager.kt, ZIP/JSON roundtrip
  és android/migration-fixtures/legacy-v1371.json ellenőrzése.
- A meglévő felhasználói app felültelepítéséhez a com.repforge.app
  package, eredeti aláírókulcs és monoton versionCode szükséges;
  éles adat vagy APK felülírása kizárólag kifejezett jóváhagyással.
- Kis telefonon is működő, akadálymentes Compose UI: legalább ~48dp
  érintési cél, Back/IME/rotáció, HU/EN/DE/RO és témák.
- Nem elég a kód létezése: az inaktív gomb, hibás adatbekötés,
  üres képernyő vagy sikertelen navigáció továbbra is HIBA.

## Munkasorrend
1. Importfájlok és Gradle-projekt ellenőrzése; android/ alatt build.
2. Meglévő natív route/VM/action bejárása és hiánylista.
3. Az 5+3 felső navigáció bevezetése meglévő ViewModel/state megtartásával.
4. PR277 oldalmegjelenítés + PR279 hasznos UI javításai; minden
   gomb valós adatra és eseményre kötve.
5. Funkcióparitás: edzés/program/naptár/coach/napló/egészség/GPS/Wear/sync
   és backup. Korábbi 107 pontos audit újramérése.
6. Unit/device/UI tesztek, screenshot diff, külön debug APK.
   Ne állítsd, hogy build, teszt vagy valós készülékes elfogadás sikeres
   ha nem futott le és nincs bizonyíték.

A külön AI Studio repót szerkeszd; az eredeti TrainPilot main-t ne módosítsd.
