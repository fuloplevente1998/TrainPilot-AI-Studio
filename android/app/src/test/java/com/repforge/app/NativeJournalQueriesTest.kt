package com.repforge.app

import androidx.room.Room
import androidx.room.withTransaction
import com.repforge.app.data.db.TrainPilotDatabase
import com.repforge.app.data.db.WorkoutHistoryEntity
import kotlinx.coroutines.runBlocking
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], manifest = Config.NONE)
class NativeJournalQueriesTest {
    private fun row(i: Int) = JournalTestFixtures.row(i)

    @Test fun emptyAndLargeJournalsReturnOnlyEightWatchParentsAndBoundedSummaryPages() = runBlocking {
        for (count in listOf(0, 200, 1500)) {
            val db = Room.inMemoryDatabaseBuilder(RuntimeEnvironment.getApplication(), TrainPilotDatabase::class.java).build()
            try {
                val dao = db.workoutHistoryDao()
                db.withTransaction { repeat(count) { dao.insertWorkout(row(it)) } }
                val mini = dao.getWearMiniJournal()
                assertEquals(minOf(8, count), mini.size)
                if (count > 0) assertEquals("w-%04d".format(count - 1), mini.first().workout.id)
                val first = dao.getJournalSummaryPage(32, 0)
                val next = dao.getJournalSummaryPage(32, 32)
                assertEquals(minOf(32, count), first.size)
                assertEquals(minOf(32, (count - 32).coerceAtLeast(0)), next.size)
                assertTrue(first.map { it.id }.intersect(next.map { it.id }.toSet()).isEmpty())
                assertEquals(count, dao.getWorkoutCount())
            } finally { db.close() }
        }
    }
    @Test fun equalTimestampsHaveStablePageBoundariesAndUpdatesAreNotCachedByCount() = runBlocking {
        val db = Room.inMemoryDatabaseBuilder(RuntimeEnvironment.getApplication(), TrainPilotDatabase::class.java).build()
        try {
            val dao = db.workoutHistoryDao()
            db.withTransaction { repeat(40) { dao.insertWorkout(row(it).copy(startedEpochMs = 1000)) } }
            val first = dao.getJournalSummaryPage(32, 0)
            val last = dao.getJournalSummaryPage(32, 32)
            assertEquals(40, (first + last).map { it.id }.toSet().size)
            dao.insertWorkout(row(39).copy(startedEpochMs = 1000, dayName = "Updated"))
            assertEquals("Updated", dao.getJournalSummaryPage(32, 0).first().dayName)
            assertEquals(40, dao.getWorkoutCount())
        } finally { db.close() }
    }

    @Test fun quickFiltersReturnOnlyPrWorkoutsAndGpsCardioWorkouts() = runBlocking {
        val db = Room.inMemoryDatabaseBuilder(RuntimeEnvironment.getApplication(), TrainPilotDatabase::class.java).build()
        try {
            val dao = db.workoutHistoryDao()
            dao.insertWorkout(row(1).copy(id = "w-normal", hasPr226 = false, startedEpochMs = 1000))
            dao.insertWorkout(row(2).copy(id = "w-pr", hasPr226 = true, startedEpochMs = 2000))
            dao.insertWorkout(row(3).copy(id = "w-gps", hasPr226 = false, startedEpochMs = 3000))
            val exId = dao.insertExercise(com.repforge.app.data.db.WorkoutHistoryExerciseEntity(
                workoutHistoryId = "w-gps", orderIndex = 0, exerciseId = "run-outdoor",
                nameHu = "Futás", nameEn = "Running",
                repUnit = "m", loadType = "bodyweight",
                measurementType = "distance", actualRir = null, setRir229 = false
            ))
            dao.insertSets(listOf(com.repforge.app.data.db.WorkoutHistorySetEntity(
                workoutHistoryId = "w-gps", historyExerciseRowId = exId, exerciseId = "run-outdoor",
                setId = "s-1", setNumber = 1, done = true, reps = "900", weight = null,
                leftSeconds = null, rightSeconds = null, distanceMeters = 3200.0,
                actualRir = null, gpsRouteKey163 = null, gpsRouteKey193 = "route-193"
            )))

            val prRows = dao.scanJournalWithQuickFilter(Long.MIN_VALUE, Long.MAX_VALUE, 1, 0, null, "", 32)
            assertEquals(listOf("w-pr"), prRows.map { it.summary.id })

            val gpsRows = dao.scanJournalWithQuickFilter(Long.MIN_VALUE, Long.MAX_VALUE, 0, 1, null, "", 32)
            assertEquals(listOf("w-gps"), gpsRows.map { it.summary.id })
        } finally { db.close() }
    }
}
