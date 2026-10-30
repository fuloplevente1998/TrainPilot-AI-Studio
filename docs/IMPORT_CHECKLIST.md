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
