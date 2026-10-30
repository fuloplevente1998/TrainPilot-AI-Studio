package com.repforge.app.ui.navigation

/** Canonical upper navigation: five primary destinations, three utility destinations.
 * The retired primary Progress route remains accessible as a secondary page.
 * Workout/session lifecycle and navigation guards are preserved.
 */
internal object NativeMainMenu {
    val routes = listOf("home", "training", "journal", "health", "programs")
    val topUtilities = listOf("settings", "calendar", "coach")

    // Scroll the primary bar rather than clipping localized labels on small phones.
    fun topTabsScrollable(availableWidthDp: Float, fontScale: Float): Boolean =
        availableWidthDp < 430f || fontScale > 1.15f

    fun topTabScrollTarget(maxScrollPx: Int, index: Int, tabCount: Int = routes.size): Int {
        if (maxScrollPx <= 0 || tabCount <= 1) return 0
        val validIndex = index.coerceIn(0, tabCount - 1)
        return ((maxScrollPx.toLong() * validIndex) / (tabCount - 1)).toInt()
    }

    // Keep all existing screens and deep links reachable.
    val secondaryRoutes = listOf("calendar", "coach", "quick_workout", "quick_outdoor",
        "active_workout", "settings", "weight_journal", "exercise_library",
        "weight_journal_add", "progress")

    fun selected(route: String, settingsOrigin: String = "home"): String = when (route) {
        "active_workout", "quick_workout", "quick_outdoor", "exercise_library" -> "training"
        "calendar", "coach" -> "home"
        "progress" -> "journal"
        "weight_journal", "weight_journal_add" -> "health"
        "settings" -> if (settingsOrigin == "settings") "home" else selected(settingsOrigin)
        else -> route.takeIf { it in routes } ?: "home"
    }

    fun destination(route: String, hasActiveWorkout: Boolean): String {
        require(route in routes || route in secondaryRoutes)
        return if (route == "training" && hasActiveWorkout) "active_workout" else route
    }

    /** Opening Settings is not leaving an active workout; other pages are. */
    fun pausesWorkout(current: String, target: String, settingsOrigin: String = "home"): Boolean =
        target != "settings" && target != "active_workout" &&
            (current == "active_workout" || (current == "settings" && settingsOrigin == "active_workout"))

    fun navigationAllowed(target: String, starting: Boolean, finishing: Boolean, finalizing: Boolean,
        restoreBlocked: Boolean, commandsSuspended: Boolean): Boolean =
        !starting && !finishing && !restoreBlocked &&
            (target == "active_workout" || (!finalizing && !commandsSuspended))

    fun labels(language: String) = when (language) {
        "en" -> listOf("Home", "Training", "Journal", "Health", "Programs")
        "de" -> listOf("Startseite", "Training", "Protokoll", "Gesundheit", "Programme")
        "ro" -> listOf("Acasă", "Antrenament", "Jurnal", "Sănătate", "Programe")
        else -> listOf("Kezdőlap", "Edzés", "Napló", "Egészség", "Programok")
    }

    fun title(route: String, language: String): String {
        if (route in routes) return labels(language)[routes.indexOf(route)]
        val names = when (language) {
            "en" -> listOf("Calendar", "Coach", "Quick workout", "Outdoor workout",
                "Training", "Settings", "Weight journal", "Exercise library",
                "Weight journal", "Progress", "Back")
            "de" -> listOf("Kalender", "Coach", "Schnelltraining", "Training im Freien",
                "Training", "Einstellungen", "Gewichtsprotokoll", "Übungsbibliothek",
                "Gewichtsprotokoll", "Fortschritt", "Zurück")
            "ro" -> listOf("Calendar", "Coach", "Antrenament rapid", "Antrenament în aer liber",
                "Antrenament", "Setări", "Jurnal de greutate", "Bibliotecă de exerciții",
                "Jurnal de greutate", "Progres", "Înapoi")
            else -> listOf("Naptár", "Coach", "Gyors edzés", "Szabadtéri edzés",
                "Edzés", "Beállítások", "Testsúlynapló", "Gyakorlatkönyvtár",
                "Testsúlynapló", "Fejlődés", "Vissza")
        }
        return names[secondaryRoutes.indexOf(route).takeIf { it >= 0 } ?: names.lastIndex]
    }

    fun backLabel(language: String) = title("back", language)
}
