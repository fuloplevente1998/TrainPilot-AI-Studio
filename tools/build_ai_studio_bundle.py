#!/usr/bin/env python3
"""Create an AI Studio-safe, self-contained curated native TrainPilot workspace."""
from pathlib import Path
import hashlib
import json
import os
import shutil

src = Path(os.environ["TRAINPILOT_SOURCE"]).resolve()
out = Path(os.environ["GITHUB_WORKSPACE"]).resolve()
native = src / "ai-studio/sources/native-migration"
pr279 = src / "ai-studio/sources/pr279-webview"

def file(a, dest):
    a = Path(a)
    if not a.is_file():
        raise FileNotFoundError(str(a))
    b = out / dest
    b.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(a, b)

def folder(a, dest):
    a = Path(a)
    if not a.is_dir():
        raise FileNotFoundError(str(a))
    shutil.copytree(a, out / dest, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

def doc(name, body):
    p = out / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body.strip() + "\n", encoding="utf-8")

for dir_name in ("android", "reference", "docs/reference"):
    p = out / dir_name
    if p.exists():
        shutil.rmtree(p)

# Keep the WHOLE native Android project, including all phone/Wear tests.
folder(native / "android", "android")
folder(native / "scripts/native", "tools/native-checks")
folder(native / "docs/design/final-ui-ux", "docs/reference/native/design/final-ui-ux")
folder(native / "docs/design/mockups", "docs/reference/native/design/mockups")

native_docs = [
"MIGRATION_STATE.md", "NATIVE_IMPORT_MANIFEST.md", "NATIVE_TOOLCHAIN_POLICY.md",
"docs/NATIVE_RESUME.md", "docs/STUDIO_UI_RESUME.md", "docs/WORK_HANDOFF.md",
"docs/NATIVE_TRANSFER_2026-10-27.md",
"docs/plans/NATIVE_FINAL_DELIVERY.md", "docs/plans/NATIVE_MASTER_PLAN_AND_FIXES.md",
"docs/plans/NATIVE_FINAL_UI_UX_CODEX_HANDOFF.md",
"docs/plans/NATIVE_FINAL_FEATURE_INVENTORY_PLUS_HANDOFF.md",
"docs/plans/NATIVE_DATA_INTEGRITY_FINAL_CHAT_HANDOFF.md",
"docs/plans/NATIVE_PHONE_UI_FINAL_CHAT_HANDOFF.md",
"docs/plans/NATIVE_CALENDAR_MULTIWEEK_HANDOFF.md",
"docs/plans/NATIVE_PROGRAM_ACTIONS_HANDOFF.md",
"docs/plans/NATIVE_HEALTH_SYNC_COMPLETION_CODEX_HANDOFF.md",
"docs/plans/NATIVE_THEME_CONTRAST_PLUS_HANDOFF.md",
"docs/reviews/NATIVE_FINAL_FEATURE_INVENTORY.md",
"docs/reviews/NATIVE_FINAL_FEATURE_INVENTORY.json",
"docs/reviews/NATIVE_FEATURE_PARITY_AUDIT.md",
"docs/reviews/NATIVE_DATA_INTEGRITY_FINAL_GATE_HANDOFF.md",
"docs/reviews/NATIVE_PHONE_UI_FINAL_GATE_HANDOFF.md",
"docs/reviews/NATIVE_PROGRAM_ACTIONS_HANDOFF.md",
"docs/reviews/NATIVE_TRAINING_MODE_APPROVAL_UI_FIX_HANDOFF.md",
"docs/reviews/NATIVE_THEME_CONTRAST_REVIEW.md",
"docs/reviews/PR270_VISUAL_RECHECK_2026-10-29.md",
]
for name in native_docs:
    file(native / name, "docs/reference/native/" + name)
folder(src / "ai-studio/design/pr277", "reference/pr277-design")
folder(pr279 / "www", "reference/pr279-webview/www")
folder(pr279 / "docs/pr277-implementation", "reference/pr279-webview/implementation")
test_prefixes = ("active-workout", "calendar", "coach", "health", "journal", "program",
                 "progress", "training", "workout", "v150", "v151", "v152", "v153",
                 "v154", "v155", "v260", "v261", "v262", "v263", "phase3",
                 "phase4", "phase5", "phase6", "phase7", "wear-phone", "backup")
pr279_tests = sorted(p for p in (pr279 / "tests").glob("*.cjs")
                     if p.name.startswith(test_prefixes))
for p in pr279_tests[:42]:
    file(p, "reference/pr279-webview/tests/" + p.name)
folder(src / "www", "reference/stable-main/www")
for name in ("README.hu.md", "RELEASE_NOTES.md", "SOURCE_VERSION.json",
             "AGENTS.md", "docs/FEATURES.hu.md"):
    file(src / name, "reference/stable-main/" + name)
for name in ("NATIVE_FINAL_FEATURE_INVENTORY.md", "NATIVE_FINAL_FEATURE_INVENTORY.json"):
    file(src / "ai-studio/audits" / name, "docs/reference/audits/" + name)
file(src / "ai-studio/TRAINPILOT_NATIVE_MASTER_SPEC.md",
     "docs/reference/HISTORICAL_MASTER_SPEC_2x4.md")

doc("README.md", """
# TrainPilot – Google AI Studio / Native Android

A külön munkarepo a natív Kotlin + Jetpack Compose TrainPilot befejezéséhez.
A működő régi WebView alkalmazás kizárólag az eredeti fuloplevente1998/TrainPilot repóban marad.

## Elsőként ezeket olvasd el
1. AI_STUDIO_TASK.md – jelenlegi cél, prioritások, bekötések.
2. docs/NAVIGATION_5_PLUS_3.md – a FELHASZNÁLÓ LEGFRISSEBB navigációs döntése.
3. docs/IMPORT_CHECKLIST.md – import és funkcionális ellenőrzőlista.
4. docs/FILE_MANIFEST.json – minden importált fájl SHA256-ellenőrző listája.

## Mappák
- android/ – TELJES natív telefon + Wear OS + shared projekt, Kotlin, Gradle és tesztek.
- reference/pr277-design/ – 8 eredeti UI látványterv.
- reference/pr279-webview/ – a PR279 friss megvalósítása, képek és szelektált viselkedési tesztek.
- reference/stable-main/ – korábbi stabil WebView funkcionális referencia.
- docs/reference/native/ – natív tervek és UI/bekötési/QA dokumentáció.
- docs/reference/audits/ – 107 pontú korábbi natív funkció- és egészségmetrika audit.

FONTOS: a WebView referencia NEM az új alkalmazás. Ne cseréld le a natív kódot WebView-ra.
A régi 2×4 menü és a kísérleti alsó dock történeti referencia; a 2026-10-30-i döntés az 5+3 felső navigáció.
""")

doc("AI_STUDIO_TASK.md", """
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
""")

doc("docs/NAVIGATION_5_PLUS_3.md", """
# Felső navigáció – új, kötelező döntés (2026-10-30)

## 5 főmenü
**Kezdőlap | Edzés | Napló | Egészség | Programok**

Mind az öt tényleges teljes oldalas Compose célpont.
Nem alul, nem 2×4 régi csempemenüben, hanem a felső navigációban.
A képernyő és az aktív edzés állapota lapváltáskor megmarad.

## 3 kisebb felső gomb
**Beállítások | Naptár | Coach**

Minden főmenüből elérhető. Kompakt, hozzáférhető ikon/szöveg.
- Beállítások: teljes oldal, rövid kapcsolódó beállításhoz
  modal bottom sheet / teljes magasságú felugró lap is megengedett.
- Naptár: teljes oldal; csak konkrét szerkesztéshez dialog.
- Coach: teljes oldal a részletes tanácsoknak, progressziónak
  és módoknak; rövid kontextuális javaslat nyílhat felugró lapon.

Nincs automatikusan negyedik felső gyorsgomb; a Progresszió
a Coach és/vagy Napló része. 320–393dp keskeny mobilon ne lógjon
le egyik gomb sem: tömörített ikon+saját felirat vagy görgethető sor.
Nincs PR271 alsó dock. A PR277/PR279 régi 2×4 és a natív Studio
régi navigációs dokumentumai helyett EZ az elsődleges.
""")

doc("docs/IMPORT_CHECKLIST.md", """
# Import- és natív ellenőrzőlista

- Nézd meg a docs/FILE_MANIFEST.json állományt és a teljes fájlszámot;
  ez a repó 950-nél nem tartalmazhat több fájlt.
- Megvannak az android/settings.gradle, android/app, android/wear,
  android/shared, LegacyWebViewMigrator.kt és a backup/restore kódok?
- A reference/pr277-design/references alatt mind a nyolc PNG megvan?
- Elérhető a reference/pr279-webview/www/app.js és a nyolc
  implementation/comparisons kép?
- A reference/stable-main/www a működő régi funkciók olvasási referenciája.
- Az öt teljes oldalas főmenü és a három kisebb gomb mind működik?
- Minden Edzés / Programok / Naptár / Coach / Napló / Egészség
  képernyő valódi ViewModel/repository állapothoz kötött?
- RIR, OK/Undo, pause, timer, GPS, Wear, Health, Drive, Calendar,
  programnapindítás, ZIP/JSON export-import tesztelve?
- Külön ellenőrizve: régi adat sértetlen migrációja és rollback.
- Eredeti TrainPilot repó és éles APK változatlan.
""")

doc("docs/SOURCE_PROVENANCE.md", """
# Forrásállapotok – pontos commitok

Eredeti stabil main és korábbi AI Studio archiválás: 5f026a56b9b6d33c84afa77eb3927b11f0bd6f6a.
Natív migráció: feat/native-android-migration @ 648e971034201511d69585cd5deecaa27eddf942.
PR279 UI referencia: feat/pr277-uiux-implementation-20261029 @ 5ff8cbd0da6533d04e0696229cb013936ae39619.
PR277 dizájn: feat/uiux-page-content-20261029 @ 9aa3721ca675cd66b4fa04d1c91e2b6a871c04ed.
107 pontos audit: PR250 @ fb64307f67459a00def6b81890bc4ba337da00d6.

Ez célzott fájlmásolat, nem branch merge. A natív android/ könyvtár
teljes teszt/forrás/Gradle fáit megőrizzük; a régi WebView tesztkészlet
szándékosan csak válogatott. A BUILD/APK/DEVICE elfogadás külön feladat.
""")

files = sorted(p for p in out.rglob("*") if p.is_file() and ".git" not in p.parts)
entries = [{"path": p.relative_to(out).as_posix(),
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "size": p.stat().st_size}
           for p in files if p.relative_to(out).as_posix() != "docs/FILE_MANIFEST.json"]
total = len(entries) + 1
if total > 950:
    raise SystemExit("FAIL: " + str(total) + " > 950 files. Refuse import.")
doc("docs/FILE_MANIFEST.json", json.dumps({
    "file_count_including_manifest": total, "max_files": 950,
    "native_source": "648e971034201511d69585cd5deecaa27eddf942",
    "pr279_source": "5ff8cbd0da6533d04e0696229cb013936ae39619",
    "pr277_source": "9aa3721ca675cd66b4fa04d1c91e2b6a871c04ed",
    "files": entries
}, ensure_ascii=False, indent=2))
print("CURATED IMPORT COUNT:", total)
for prefix in ("android/", "reference/pr277-design/", "reference/pr279-webview/",
               "reference/stable-main/", "docs/reference/"):
    print(prefix, sum(1 for p in entries if p["path"].startswith(prefix)))
