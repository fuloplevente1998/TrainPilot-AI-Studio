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

## A két fejlesztési állapot külön kezelendő
- A natív források eredetileg a 648e9710 commitból kerültek be; a külön repóban már saját UI-változtatások is vannak.
- A tools/build_ai_studio_bundle.py és a Build TrainPilot AI Studio import GitHub Action **egyszeri bootstrap**: kézi újrafuttatása újramásolhatja az eredeti natív snapshotot, és felülírhatja az itt végzett UI-munkát. Ne indítsd újra célzott mentés/összevetés nélkül.
- A natív módosítások a külön repó main ágán folytatódnak. A valós készüléken és régi adatokon végzett tesztelés ettől függetlenül szükséges.
