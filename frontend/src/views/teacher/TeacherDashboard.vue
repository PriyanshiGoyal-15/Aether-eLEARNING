<script setup>
import { computed } from 'vue';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import { useRouter } from 'vue-router';
import { 
  Users, BookOpen, Star, DollarSign, PlusCircle, 
  TrendingUp, ClipboardList, HelpCircle, XCircle, CheckCircle, AlertTriangle
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const router = useRouter();

const teacherId = computed(() => authStore.currentUser?.id);
const teacherName = computed(() => authStore.currentUser?.name);

// Teacher's courses
const courses = computed(() => coursesStore.getTeacherCourses(teacherId.value));

// Total students enrolled in teacher's courses
const enrollments = computed(() => coursesStore.getTeacherStudents(teacherId.value));
const totalStudentsCount = computed(() => enrollments.value.length);

// Calculated average rating of all their courses
const averageRating = computed(() => {
  if (courses.value.length === 0) return 5.0;
  const total = courses.value.reduce((acc, curr) => acc + curr.rating, 0);
  return Number((total / courses.value.length).toFixed(1));
});

// Mock revenue metric (e.g. 450 INR per student enrollment)
const mockRevenue = computed(() => {
  return totalStudentsCount.value * 450;
});
</script>

<template>
  <div class="space-y-10 py-4">
    <!-- Welcome Header & Actions -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="space-y-1.5">
        <h1 class="text-2xl md:text-3xl font-extrabold text-white font-display">
          Teacher Portal: Overview
        </h1>
        <p class="text-xs text-gray-450">Manage your course catalog, reviews, and track learning progress.</p>
      </div>

      <!-- Action buttons -->
      <div class="flex flex-wrap items-center gap-3 shrink-0">
        <router-link 
          to="/teacher/students"
          class="px-4.5 py-2.5 bg-white/5 border border-white/10 text-xs font-semibold text-gray-300 hover:text-white rounded-xl transition-all flex items-center space-x-1.5"
        >
          <ClipboardList class="w-4 h-4" />
          <span>Monitor Student Progress</span>
        </router-link>

        <router-link 
          to="/teacher/create"
          class="px-5 py-2.5 bg-brand-accent hover:bg-emerald-600 text-white text-xs font-bold rounded-xl transition-all shadow-md shadow-brand-accent/15 flex items-center space-x-1.5"
        >
          <PlusCircle class="w-4 h-4" />
          <span>Upload Course</span>
        </router-link>
      </div>
    </div>

    <!-- Analytics Dashboard widgets -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- 1. Total Enrolled -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Enrolled Learners</p>
          <h3 class="text-2xl font-extrabold text-white">{{ totalStudentsCount }}</h3>
          <p class="text-[9px] text-brand-accent font-semibold flex items-center space-x-0.5">
            <TrendingUp class="w-3 h-3" />
            <span>Active enrollments</span>
          </p>
        </div>
        <div class="p-3 bg-brand-primary/10 border border-brand-primary/20 text-brand-primary rounded-xl">
          <Users class="w-6 h-6" />
        </div>
      </div>

      <!-- 2. Courses count -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Created Courses</p>
          <h3 class="text-2xl font-extrabold text-white">{{ courses.length }}</h3>
          <p class="text-[9px] text-gray-400 font-medium">Pending & approved</p>
        </div>
        <div class="p-3 bg-brand-accent/10 border border-brand-accent/20 text-brand-accent rounded-xl">
          <BookOpen class="w-6 h-6" />
        </div>
      </div>

      <!-- 3. Ratings -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Average Ratings</p>
          <h3 class="text-2xl font-extrabold text-white">{{ averageRating }} ★</h3>
          <p class="text-[9px] text-brand-warning font-semibold">100% Verified learner stars</p>
        </div>
        <div class="p-3 bg-brand-warning/10 border border-brand-warning/20 text-brand-warning rounded-xl">
          <Star class="w-6 h-6" />
        </div>
      </div>

      <!-- 4. Earnings -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Est. Revenue</p>
          <h3 class="text-2xl font-extrabold text-white">{{ mockRevenue }} INR</h3>
          <p class="text-[9px] text-gray-400 font-medium">Self-paced catalog share</p>
        </div>
        <div class="p-3 bg-brand-primary/10 border border-brand-primary/20 text-brand-primary rounded-xl">
          <DollarSign class="w-6 h-6" />
        </div>
      </div>
    </div>

    <!-- Courses Status Table -->
    <div class="space-y-4">
      <h2 class="text-lg font-bold text-white font-display">My Courses Catalog</h2>
      
      <div class="glass-panel rounded-3xl overflow-hidden border border-white/5 bg-brand-card shadow-2xl">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="bg-brand-dark/50 border-b border-white/5 text-gray-400 font-bold uppercase tracking-wider">
                <th class="px-6 py-4">Title & Details</th>
                <th class="px-6 py-4">Category</th>
                <th class="px-6 py-4">Status</th>
                <th class="px-6 py-4">Difficulty</th>
                <th class="px-6 py-4 text-center">Modules</th>
                <th class="px-6 py-4">Action</th>
              </tr>
            </thead>
            
            <tbody v-if="courses.length > 0" class="divide-y divide-white/5">
              <tr v-for="course in courses" :key="course.id" class="hover:bg-white/[0.02] transition-colors">
                <!-- Title column -->
                <td class="px-6 py-4">
                  <div class="flex items-center space-x-3.5">
                    <img :src="course.thumbnail" :alt="course.title" class="w-10 h-10 rounded-lg object-cover bg-slate-800 shrink-0" />
                    <div class="truncate max-w-[240px]">
                      <h4 class="font-bold text-white truncate text-xs">{{ course.title }}</h4>
                      <p class="text-[10px] text-gray-400 truncate">{{ course.shortDescription || course.description }}</p>
                    </div>
                  </div>
                </td>

                <!-- Category -->
                <td class="px-6 py-4 font-semibold text-gray-300">{{ course.category }}</td>

                <!-- Status column -->
                <td class="px-6 py-4">
                  <div class="flex flex-col space-y-1">
                    <div class="flex items-center space-x-1.5">
                      <CheckCircle v-if="course.status === 'approved'" class="w-4 h-4 text-brand-accent shrink-0" />
                      <HelpCircle v-else-if="course.status === 'pending'" class="w-4 h-4 text-brand-warning shrink-0" />
                      <XCircle v-else class="w-4 h-4 text-brand-danger shrink-0" />
                      <span 
                        class="font-bold uppercase tracking-wider text-[10px]"
                        :class="{
                          'text-brand-accent': course.status === 'approved',
                          'text-brand-warning': course.status === 'pending',
                          'text-brand-danger': course.status === 'rejected',
                        }"
                      >
                        {{ course.status }}
                      </span>
                    </div>
                    <!-- Rejection Alert trigger -->
                    <div 
                      v-if="course.status === 'rejected' && course.rejectionReason"
                      class="flex items-start space-x-1 p-1.5 rounded-lg bg-brand-danger/10 border border-brand-danger/20 text-[10px] text-brand-danger max-w-[200px]"
                    >
                      <AlertTriangle class="w-3.5 h-3.5 shrink-0 mt-0.5" />
                      <span class="leading-relaxed">Reason: {{ course.rejectionReason }}</span>
                    </div>
                  </div>
                </td>

                <!-- Difficulty -->
                <td class="px-6 py-4 font-medium text-gray-350">{{ course.difficulty }}</td>

                <!-- Modules count -->
                <td class="px-6 py-4 text-center font-bold text-white">{{ course.modules.length }}</td>

                <!-- Action button -->
                <td class="px-6 py-4">
                  <router-link 
                    :to="`/courses/${course.id}`"
                    class="px-3.5 py-1.5 bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20 text-white rounded-lg transition-all font-semibold inline-block text-[11px]"
                  >
                    View
                  </router-link>
                </td>
              </tr>
            </tbody>

            <!-- Empty table -->
            <tbody v-else>
              <tr>
                <td colspan="6" class="px-6 py-12 text-center text-gray-500 font-medium">
                  You haven't uploaded any courses yet. Click "Upload Course" to draft your first program.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </div>
</template>
