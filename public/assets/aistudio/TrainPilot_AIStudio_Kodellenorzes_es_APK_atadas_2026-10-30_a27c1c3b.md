# TrainPilot AI Studio – kódellenőrzés, javítási feladatok és APK-átadás

**Dátum:** 2026-10-30  
**Címzett:** Google AI Studio fejlesztői agent  
**Munkarepozitórium:** https://github.com/fuloplevente1998/TrainPilot-AI-Studio  
**Eredeti, működő alkalmazás:** https://github.com/fuloplevente1998/TrainPilot – **NEM MÓDOSÍTHATÓ**  
**Ellenőrzött munkarepo-HEAD:** `2b5ce211f7d81eed3d50e09fc68e63962b99450c`  
**AI Studio fejlesztési commit:** `1a83af99e6cdb0adc3cd57c6e03cfad63ac35590`  
**Hibás CI-futás:** https://github.com/fuloplevente1998/TrainPilot-AI-Studio/actions/runs/41070924705

## 1. Cél

A már elkészült **natív Kotlin + Jetpack Compose** TrainPilot Android-alkalmazást kell folytatni, **nem újragenerálni**. A telefonos, Wear OS, adatbázis-, edzés-, GPS-, egészségügyi, Google-szinkron- és mentés/migrációs kódot meg kell őrizni.

**Első mérföldkő:** javított, hibamentesen forduló natív Android-debug APK előállítása **GitHub Actions** segítségével, letölthető build artifactként. Ezt a felhasználó saját Android-eszközön teszteli. **APK-t csak sikeres build után tekints elkészültnek; sikeres build nem egyenlő készülékes elfogadással.**

### Kötelező navigáció: felső 5+3

- **Öt főmenü:** Kezdőlap | Edzés | Napló | Egészség | Programok.
- **Három kisebb felső gomb:** Beállítások | Naptár | Coach.
- Ezek valódi natív képernyőket/állapotot nyitnak; a Naptár és a részletes Coach teljes oldal, a beállításoknál részablak megengedett.
- A **Fejlődés/Progresszió/PR** a Naplóból és a Coachból elérhető marad.
- A régi **2×4** navigációt és a kísérleti alsó dokkot **ne állítsd vissza**.
- A részletekhez olvasd el az `AI_STUDIO_TASK.md` és `docs/NAVIGATION_5_PLUS_3.md` dokumentumokat.

## 2. Ami ténylegesen elkészült az AI Studio munkájában

Az `1a83af99` commitban valós Kotlin/Compose forrásmódosítások történtek:

| Terület | Ellenőrzött változás | Állapot |
|---|---|---|
| Napló | **Összes / PR edzések / GPS Kardió** gyorsszűrők; új Room DAO-lekérdezés, ViewModel- és Paging-bekötés | Implementálva, új build/tesztek még nem igazoltak |
| Napló és Coach | Közvetlen átlépés a Fejlődés/PR oldalra | Bekötve, feliratjavítás szükséges |
| Programok | Kompaktabb edzésnap-kártyák, legfeljebb három gyakorlatnév előnézetével, „+N” kijelzés | Implementálva, eszközön vizsgálandó |
| Aktív edzés | Következő gyakorlat kártyája | Implementálva, interakció tesztelendő |
| Aktív edzés | Gyors RIR-választó | Jelenleg **fordítási hibát okoz** |
| Aktív edzés | „Auto-prefill ✓” jelzés | Félrevezető feltétel; javítandó |
| Progresszió | Napló-visszalépés és új képernyőváltó | Bekötve, működését tesztelni kell |
| Felső navigáció | Megmaradt az **öt főmenü + három kisebb gomb** elrendezés | Célzott UI/Back/állapot teszt szükséges |

Az új repó a vizsgálat időpontjában **903 Git-fájlt** tartalmazott, ebből **8 AI Studio ideiglenes kép** és **14 Gradle-cache fájl**. Az 1000 fájlos AI Studio importkorlát miatt ezeket célszerű eltávolítani. A működő eredeti TrainPilot repo változatlan.

## 3. Kritikus blokkoló – Kotlin buildhiba

**CI:** https://github.com/fuloplevente1998/TrainPilot-AI-Studio/actions/runs/41070924705  
**Eredmény:** `failure`, a `:app:compileDebugKotlin` feladaton állt meg. **Nem készült igazoltan működő új APK.**

A GitHub Actions naplóban található hibák:

| Fájl / sor a hibás commitban | Fordítóhiba | Javítás |
|---|---|---|
| `android/app/src/main/java/com/repforge/app/ui/workout/ActiveWorkoutScreen.kt:887` | `Unresolved reference 'rir'` | Az `ActiveSetUiModel` valódi mezője **`actualRir: Int?`**. A `.rir` hivatkozást cseréld `.actualRir`-re. |
| Ugyanott `:901` | `Unresolved reference 'compareTo'` | Az összehasonlítást a helyes `Int?` típussal vizsgáld újra az előző javítás után (`actualRir != null && actualRir >= 4`). |
| Ugyanott `:905` | `Unresolved reference 'heightIn'` | Add hozzá az importokhoz: `import androidx.compose.foundation.layout.heightIn`. |

**Ne csak a fenti három sort javítsd:** fordítsd le az **egész `:app` modult**, és a következő fordítási hibákat is javítsd. A megelőző navigációs CI sikeres volt, ez a hiba a legutóbbi AI Studio módosításai után jelentkezett.

## 4. További konkrét javítandók

### 4.1. Coach Fejlődés-gombjának hibás felirata

Fájl: `android/app/src/main/java/com/repforge/app/ui/coach/CoachScreen.kt`.

- A `coach_open_progress` gomb helyesen `onProgress` műveletet hív.
- A felirata viszont jelenleg `Text(words[18])`, amely másutt **Egészség** feliratként szerepel.
- Használd a megfelelő **Fejlődés/Progresszió** szöveget (`words[19]`) vagy meglévő lokalizált string-erőforrást, minden támogatott nyelven.

### 4.2. Félrevezető „Auto-prefill ✓” címke

Fájl: `android/app/src/main/java/com/repforge/app/ui/workout/ActiveWorkoutScreen.kt`.

A jelenlegi `hasPrefilledWeight` feltétel csupán azt vizsgálja, szerepel-e nem nulla súly a sorozatokban. **Ez önmagában nem bizonyítja automatikus előkitöltés megtörténtét.**

- Csak hiteles forrás-/eredetjelölés alapján mutasd az automatikus előkitöltés címkéjét.
- Ha a modell nem tartalmaz ilyen mezőt, **inkább távolítsd el ezt a jelzést**, de a súlyadatokat és az előkitöltés meglévő mechanikáját ne módosítsd indokolatlanul.

### 4.3. Gyors RIR-választó

- A gyors gombok érintési célja legyen legalább körülbelül **48 dp** magas; jelenleg `36.dp` szerepel.
- A választó ne engedjen műveletet, ha az edzés nem a telefon szerkeszthető tulajdona, szüneteltetett/átadás alatti vagy lezárás alatt van, a meglévő natív szerkesztési korlátok szerint.
- A sorozat RIR-értéke a **tényleges `actualRir` adatmodellt** és a meglévő `viewModel.setSetRir(...)` műveletet használja, nem helyi demóállapotot.
- Teszteld a kijelölés, kikapcsolás, visszavonás, visszatöltés és Wear-átadás eseteit; ne legyen adatsérülés.

### 4.4. AI Studio és Gradle-cache fájlok

A legutóbbi commitba került **8 `.aistudio/artifacts/.../.tempmediaStorage/*.png`** és **14 `android/.gradle/**`** fájl.

- A kizárólag generált/ideiglenes fájlokat távolítsd el a Gitből (a működő projektforrásokat, Gradle wrapper JAR-t és dizájnreferenciákat **ne**).
- Szükség esetén javítsd a `.gitignore` szabályokat.
- **Kivétel:** az `android/app/libs/samsung-health-data-api-1.1.0.aar` fontos buildfüggőség; ezt **ne töröld**.
- Import alatt maradjon a repo **1000 fájlnál**, lehetőleg **950 alatt**. A fájlintegritás-workflow továbbra is fusson.

### 4.5. Napló új adatbázis-szűrője

Érintett fájlok:

- `android/app/src/main/java/com/repforge/app/data/db/TrainPilotDaos.kt`
- `android/app/src/main/java/com/repforge/app/ui/journal/NativeJournalRepository.kt`
- `android/app/src/main/java/com/repforge/app/ui/journal/JournalViewModel.kt`
- `android/app/src/main/java/com/repforge/app/ui/journal/JournalScreen.kt`
- `android/app/src/test/java/com/repforge/app/NativeJournalQueriesTest.kt`

Ellenőrizd a PR/GPS szűrő helyes találatait, a szöveges kereséssel, dátumszűrővel és lapozással való együttműködést, a migrált/hiányos előzményeket, a teljesítményt és az adatbázis-frissítési eseményeket. **A meglévő napló nem veszíthet rekordokat.**

## 5. Funkciók, amelyek továbbra is igazolandók

**Kód létezik, de ez nem készülékes működési bizonyíték.** A kiadás előtt külön ellenőrizd:

- **Kezdőlap:** valós edzés-, program- és egészségösszesítő, működő gyorsműveletek.
- **Edzés:** gyors/programozott indítás, aktuális/előző sorozat, OK/Undo, RIR, egyetlen stopper-/edzés-tulajdonos, háttérből visszatérés.
- **Napló/Fejlődés:** új szűrők, rekordok, fotók, statisztika, útvonal és visszanavigálás.
- **Programok/Naptár/Coach:** programnap indítása, szerkesztés, ütemezés, valódi progresszió és ajánlások.
- **Egészség:** Health Connect/Samsung jogosultság, tényleges adatforrás és utolsó sikeres szinkron, hiányzó adatok korrekt megjelenítése.
- **GPS/útvonal:** engedélyek, indulás/szünet/visszaállás, útvonal megőrzése.
- **Wear OS:** szinkron, offline visszatérés, egyetlen edzés-owner; konkrét telefonos programnap Wear-ről történő indítását csak visszaigazolt protokoll és teszt alapján állítsd működőnek.
- **Google Drive/Calendar:** bejelentkezés, jogosultságok, ütközéskezelés, visszaállítás, nincs csendes felülírás.
- **Adatmigráció:** régi WebView JSON/ZIP mentés importálása, migráció utáni állomány- és adatsérülés-ellenőrzés; visszagörgetési útvonal.
- **UI/UX:** mind a nyolc PR277 referenciakép, PR279 javítások, 5+3 felső menü, 320–393 dp, HU/EN/DE/RO, témák, Back/rotáció/hozzáférhetőség.

## 6. Kötelező munkasorrend az agentnek

1. **Olvasd el** az `AI_STUDIO_TASK.md`, `docs/NAVIGATION_5_PLUS_3.md`, `docs/IMPORT_CHECKLIST.md` dokumentumokat, és ellenőrizd az aktuális repo-HEAD-et.
2. **Javítsd a `:app:compileDebugKotlin` blokkoló hibáit**, és futtasd újra a teljes natív telefonos modul fordítását.
3. **Javítsd a feliratozást, a RIR-gombokat és a félrevezető Auto-prefill jelzést**; állítsd helyre a teszteket.
4. **Takarítsd ki a Gitből a generált cache/ideiglenes képeket**, és frissítsd a fájllistát.
5. **Futtasd a releváns JVM/Room/Compose teszteket**, majd Wear OS fordítást és az elérhető integrációs ellenőrzéseket. A sikertelen tesztet ne hagyd figyelmen kívül.
6. **Csak sikeres fordítás és tesztek után készíts GitHub Actions debug APK-t**, töltsd fel GitHub Actions artifactként.
7. Add meg a **pontos commit SHA-t**, a **CI-futás URL-jét**, a **letölthető APK artifact nevét/linkjét**, valamint a **megmaradt hiányosságokat**.

## 7. GitHub Actions – következő mérföldkő: APK

Javasolt egy **külön** `.github/workflows/build-native-debug-apk.yml` workflow, amely:

- `ubuntu-latest` runneren checkoutolja az aktuális `TrainPilot-AI-Studio` repót.
- Java 17-et és a runner Android SDK-ját használja; a korábbi `android-actions/setup-android@v3` nálunk egyszer SDK-telepítési hibával leállt, ezért ne függj tőle ellenőrzés nélkül.
- Az `android/` könyvtárban a projekt wrapperével futtatja: `./gradlew :app:assembleDebug --no-daemon --stacktrace`.
- A kész APK-t a várható `android/app/build/outputs/apk/debug/app-debug.apk` helyről ellenőrzés után GitHub Actions artifactként tölti fel (`actions/upload-artifact@v4`).
- Külön jelzi a build, unit tesztek és Wear build állapotát; **nem hirdet zöldet, ha valamelyik kötelező lépés hibás**.
- `workflow_dispatch`-csal kézzel is indítható, és a futáson belül egyértelműen látszik a commit SHA.

### Kritikus telepítési és adatbiztonsági figyelmeztetés

A natív projekt aktuális debug konfigurációjában az alap `applicationId` **`com.repforge.app`**, a korábbi telepített TrainPilot is ezt a csomagnevet használja. **Az eltérő debug aláírás miatt a debug APK nem alkalmas biztonságos, helyben történő frissítésre** a meglévő alkalmazás fölött; ne kérd a felhasználót, hogy törölje a működő alkalmazását.

A külön telepíthető UI-teszthez először vizsgáld meg az **elkülönített debug `applicationIdSuffix`** (például `.aistudio`) biztonságos használatát és a hozzá kapcsolódó `FileProvider`, authority, Health/Google és Wear konfigurációkat. Ha nincs teljesen validált izolált debug-variáns, **ne telepítsük rá a meglévő alkalmazásra**; használj külön tesztkészüléket/profilt vagy egyeztetett megoldást. Az éles csomagazonosságú, eredeti aláírású frissítés és a valódi legacy in-place migráció **külön, ellenőrzött release-/upgrade-teszt**, nem egyenlő a debug APK-val. Aláírókulcsot és jelszót ne helyezz el a repóban.

## 8. Kötelező zárójelentés

A munka végén ilyen szerkezetben válaszolj a felhasználónak:

1. **Commit:** melyik SHA-n készült el a munka.
2. **Javított fájlok:** röviden, tényleges fájlnevekkel.
3. **Build és tesztek:** minden futás pontos parancsa, státusza és GitHub URL-je.
4. **APK:** artifact neve/linkje, debug package ID, aláírás jellege, telepítési korlátok.
5. **Nyitott pontok:** ami még nem működik vagy nincs eszközön igazolva.
6. **Tesztelési útmutató:** mit próbáljon ki a felhasználó először (navigáció, edzés, RIR/Undo, programok, napló, egészség/GPS, Wear), és hogyan jelentse vissza a hibákat.

**Ne állítsd, hogy minden funkció teljes vagy az APK készen van, amíg ténylegesen nem igazoltad. Az eredeti `fuloplevente1998/TrainPilot` repó és az ottani éles alkalmazás változatlan marad.**
