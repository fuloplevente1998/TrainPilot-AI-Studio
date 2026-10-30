# Forrásállapotok – pontos commitok

Eredeti stabil main és korábbi AI Studio archiválás: 5f026a56b9b6d33c84afa77eb3927b11f0bd6f6a.
Natív migráció: feat/native-android-migration @ 648e971034201511d69585cd5deecaa27eddf942.
PR279 UI referencia: feat/pr277-uiux-implementation-20261029 @ 5ff8cbd0da6533d04e0696229cb013936ae39619.
PR277 dizájn: feat/uiux-page-content-20261029 @ 9aa3721ca675cd66b4fa04d1c91e2b6a871c04ed.
107 pontos audit: PR250 @ fb64307f67459a00def6b81890bc4ba337da00d6.

Ez célzott fájlmásolat, nem branch merge. A natív android/ könyvtár
teljes teszt/forrás/Gradle fáit megőrizzük; a régi WebView tesztkészlet
szándékosan csak válogatott. A BUILD/APK/DEVICE elfogadás külön feladat.
