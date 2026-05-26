<script setup>
import { ref, computed } from 'vue';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import { useRouter } from 'vue-router';
import { ArrowLeft, Users, Filter, CheckCircle, Clock } from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const router = useRouter();

const teacherId = computed(() => authStore.currentUser?.id);

// All enrollments under courses of this teacher
const students = computed(() => coursesStore.getTeacherStudents(teacherId.value));

// Get list of courses created by the teacher for filters
const teacherCourses = computed(() => coursesStore.getTeacherCourses(teacherId.value));
const selectedCourse = ref('All');

// Filtered student list
const filteredStudents = computed(() => {
  if (selectedCourse.value === 'All') return students.value;
  return students.value.filter(s => s.courseTitle === selectedCourse.value);
});
</script>

<template>
  <div class="space-y-8 py-4">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <button 
        @click="router.push('/teacher/dashboard')" 
        class="flex items-center space-x-2 text-sm text-gray-400 hover:text-white transition-colors"
      >
        <ArrowLeft class="w-4 h-4" />
        <span>Back to Portal</span>
      </button>

      <!-- Filter dropdown -->
      <div class="flex items-center space-x-2 shrink-0">
        <Filter class="w-4 h-4 text-brand-primary" />
        <span class="text-xs text-gray-400">Filter Course:</span>
        <select 
          v-model="selectedCourse" 
          class="bg-brand-card hover:bg-brand-card-hover border border-white/10 px-3 py-1.5 rounded-xl text-xs text-white focus:outline-none focus:ring-1 focus:ring-brand-primary"
        >
          <option value="All">All Courses</option>
          <option v-for="c in teacherCourses" :key="c.id" :value="c.title">{{ c.title }}</option>
        </select>
      </div>
    </div>

    <!-- Title summary -->
    <div class="space-y-1">
      <h1 class="text-xl md:text-2xl font-extrabold text-white font-display flex items-center space-x-2">
        <Users class="w-5.5 h-5.5 text-brand-primary" />
        <span>Student Progress Gradebook</span>
      </h1>
      <p class="text-xs text-gray-450">Review real-time completion percentages of active students enrolled in your syllabus paths.</p>
    </div>

    <!-- Roster Table list -->
    <div class="glass-panel rounded-3xl overflow-hidden border border-white/5 bg-brand-card shadow-2xl">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="bg-brand-dark/50 border-b border-white/5 text-gray-400 font-bold uppercase tracking-wider">
              <th class="px-6 py-4">Student Profile</th>
              <th class="px-6 py-4">Enrolled Course</th>
              <th class="px-6 py-4">Progress Rating</th>
              <th class="px-6 py-4">Enrolled Date</th>
              <th class="px-6 py-4">Credentials status</th>
            </tr>
          </thead>
          
          <tbody v-if="filteredStudents.length > 0" class="divide-y divide-white/5">
            <tr v-for="student in filteredStudents" :key="student.id" class="hover:bg-white/[0.02] transition-colors">
              
              <!-- Profile detail -->
              <td class="px-6 py-4">
                <div>
                  <h4 class="font-bold text-white text-xs">{{ student.studentName }}</h4>
                  <p class="text-[10px] text-gray-450">{{ student.studentEmail }}</p>
                </div>
              </td>

              <!-- Enrolled Course title -->
              <td class="px-6 py-4 font-semibold text-gray-300 truncate max-w-[200px]" :title="student.courseTitle">
                {{ student.courseTitle }}
              </td>

              <!-- Progress bar column -->
              <td class="px-6 py-4">
                <div class="flex items-center space-x-4 max-w-[180px]">
                  <div class="flex-grow bg-brand-dark rounded-full h-1.5 overflow-hidden">
                    <div 
                      class="h-full bg-gradient-to-r transition-all duration-300"
                      :class="student.progressPercent === 100 ? 'from-brand-accent to-emerald-450' : 'from-brand-primary to-indigo-400'"
                      :style="{ width: `${student.progressPercent}%` }"
                    ></div>
                  </div>
                  <span 
                    class="font-bold shrink-0 text-xs text-right min-w-[32px]"
                    :class="student.progressPercent === 100 ? 'text-brand-accent' : 'text-gray-300'"
                  >
                    {{ student.progressPercent }}%
                  </span>
                </div>
              </td>

              <!-- Enrolled Date -->
              <td class="px-6 py-4 font-medium text-gray-400">{{ student.enrolledDate }}</td>

              <!-- Completion status badge -->
              <td class="px-6 py-4">
                <span 
                  class="px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider border shrink-0 inline-flex items-center space-x-1"
                  :class="student.progressPercent === 100
                    ? 'bg-brand-accent/15 text-brand-accent border-brand-accent/20'
                    : 'bg-brand-primary/10 text-brand-primary border-brand-primary/20'"
                >
                  <CheckCircle v-if="student.progressPercent === 100" class="w-3 h-3" />
                  <Clock v-else class="w-3 h-3" />
                  <span>{{ student.progressPercent === 100 ? 'Graduated' : 'Learning' }}</span>
                </span>
              </td>

            </tr>
          </tbody>

          <!-- Table empty -->
          <tbody v-else>
            <tr>
              <td colspan="5" class="px-6 py-12 text-center text-gray-500 font-medium">
                No student logs located under course category filters.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>
