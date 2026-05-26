<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCoursesStore } from '../store/courses';
import { useAuthStore } from '../store/auth';
import { 
  ArrowLeft, Star, Clock, BookOpen, User, Calendar, 
  ChevronDown, ChevronUp, Check, Play, FileText, Lock
} from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();
const coursesStore = useCoursesStore();
const authStore = useAuthStore();

const courseId = route.params.id;
const course = computed(() => coursesStore.courses.find(c => c.id === courseId));

// Tabs configuration
const activeTab = ref('overview'); // overview, curriculum, instructor
const expandedModules = ref({});

const toggleModule = (moduleId) => {
  expandedModules.value[moduleId] = !expandedModules.value[moduleId];
};

// Check if student is already enrolled
const isEnrolled = computed(() => {
  if (!authStore.isAuthenticated || !authStore.isStudent) return false;
  return coursesStore.getEnrollment(authStore.currentUser.id, courseId) !== undefined;
});

// Calculate total lesson count
const totalLessonsCount = computed(() => {
  if (!course.value) return 0;
  return course.value.modules.reduce((acc, mod) => acc + mod.lessons.length, 0);
});

// Initialize all modules as expanded by default
onMounted(() => {
  if (course.value) {
    course.value.modules.forEach(mod => {
      expandedModules.value[mod.id] = true;
    });
  }
});

const handleEnrollment = () => {
  if (!authStore.isAuthenticated) {
    // Redirect to login
    router.push({ name: 'Login', query: { redirect: route.fullPath } });
    return;
  }

  if (!authStore.isStudent) {
    alert("Only Student accounts can enroll in courses!");
    return;
  }

  // Enroll student
  coursesStore.enrollInCourse(authStore.currentUser.id, course.value.id);
  
  // Forward to learning player
  router.push(`/student/player/${course.value.id}`);
};

import { onMounted } from 'vue';
</script>

<template>
  <div v-if="course" class="space-y-8 py-4">
    <!-- Back Button -->
    <button 
      @click="router.back()" 
      class="flex items-center space-x-2 text-sm text-gray-400 hover:text-white transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
      <span>Back</span>
    </button>

    <!-- Main Detail Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
      <!-- Left Column (Information Panel) -->
      <div class="lg:col-span-2 space-y-8">
        <!-- Title & Header summary -->
        <div class="space-y-4">
          <div class="flex items-center space-x-2">
            <span class="px-3 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider bg-brand-primary/20 text-brand-primary border border-brand-primary/30">
              {{ course.category }}
            </span>
            <span class="px-3 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider bg-white/5 text-gray-300 border border-white/5">
              {{ course.difficulty }}
            </span>
          </div>

          <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight text-white font-display leading-tight">
            {{ course.title }}
          </h1>

          <p class="text-sm md:text-base text-gray-400 leading-relaxed font-light">
            {{ course.shortDescription || course.description }}
          </p>

          <!-- Author & Review rating summary -->
          <div class="flex flex-wrap items-center gap-6 text-xs text-gray-400 pt-2 border-y border-white/5 py-4">
            <div class="flex items-center space-x-2">
              <div class="w-6 h-6 rounded-full bg-brand-primary/35 flex items-center justify-center font-bold text-white text-[10px]">
                {{ course.teacherName.split(' ').map(n => n[0]).join('').toUpperCase() }}
              </div>
              <span class="font-medium text-white">Instructed by {{ course.teacherName }}</span>
            </div>

            <div class="flex items-center space-x-1 shrink-0">
              <Star class="w-4 h-4 text-brand-warning fill-brand-warning" />
              <span class="font-bold text-white">{{ course.rating.toFixed(1) }}</span>
              <span>({{ course.reviewsCount }} reviews)</span>
            </div>

            <span class="flex items-center space-x-1">
              <Clock class="w-4 h-4 text-brand-primary" />
              <span>{{ course.duration || '4.5 Hours' }} total length</span>
            </span>

            <span class="flex items-center space-x-1">
              <BookOpen class="w-4 h-4 text-brand-accent" />
              <span>{{ course.modules.length }} modules syllabus</span>
            </span>
          </div>
        </div>

        <!-- Detail Tabs Navigation -->
        <div class="space-y-6">
          <div class="flex items-center space-x-1 border-b border-white/5 pb-0">
            <button 
              @click="activeTab = 'overview'"
              class="px-6 py-3 text-xs font-bold uppercase tracking-wider border-b-2 transition-all"
              :class="activeTab === 'overview' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
            >
              Overview
            </button>
            <button 
              @click="activeTab = 'curriculum'"
              class="px-6 py-3 text-xs font-bold uppercase tracking-wider border-b-2 transition-all"
              :class="activeTab === 'curriculum' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
            >
              Curriculum
            </button>
            <button 
              @click="activeTab = 'instructor'"
              class="px-6 py-3 text-xs font-bold uppercase tracking-wider border-b-2 transition-all"
              :class="activeTab === 'instructor' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
            >
              Instructor
            </button>
          </div>

          <!-- Tabs Viewport -->
          <div class="animate-fade-in">
            <!-- 1. Overview Tab -->
            <div v-if="activeTab === 'overview'" class="space-y-6 text-sm text-gray-300 leading-relaxed font-light">
              <div class="space-y-3">
                <h3 class="text-lg font-bold text-white font-display">About This Program</h3>
                <p>{{ course.description }}</p>
              </div>

              <!-- Learning items -->
              <div class="glass-panel p-6 rounded-2xl border border-white/5 space-y-4">
                <h4 class="text-xs font-bold text-white uppercase tracking-wider">What you will learn:</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div class="flex items-start space-x-2 text-xs">
                    <Check class="w-4 h-4 text-brand-accent shrink-0 mt-0.5" />
                    <span>Scaffold dynamic responsive layouts using Vue framework modules</span>
                  </div>
                  <div class="flex items-start space-x-2 text-xs">
                    <Check class="w-4 h-4 text-brand-accent shrink-0 mt-0.5" />
                    <span>Understand responsive components, models, and data-flows</span>
                  </div>
                  <div class="flex items-start space-x-2 text-xs">
                    <Check class="w-4 h-4 text-brand-accent shrink-0 mt-0.5" />
                    <span>Implement secure access configurations and routing limits</span>
                  </div>
                  <div class="flex items-start space-x-2 text-xs">
                    <Check class="w-4 h-4 text-brand-accent shrink-0 mt-0.5" />
                    <span>Create full modular portfolios with clean, production code standards</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 2. Curriculum Tab -->
            <div v-if="activeTab === 'curriculum'" class="space-y-4">
              <h3 class="text-lg font-bold text-white font-display mb-4">Syllabus Breakdown</h3>
              
              <div class="space-y-3">
                <div 
                  v-for="mod in course.modules" 
                  :key="mod.id"
                  class="glass-panel rounded-2xl overflow-hidden border border-white/5 bg-brand-card/40"
                >
                  <!-- Module Header Accordion Trigger -->
                  <button 
                    @click="toggleModule(mod.id)"
                    class="w-full flex items-center justify-between px-5 py-4.5 hover:bg-white/5 transition-colors text-left"
                  >
                    <span class="text-sm font-bold text-white font-display">{{ mod.title }}</span>
                    <div class="flex items-center space-x-3 text-xs text-gray-400">
                      <span>{{ mod.lessons.length }} Items</span>
                      <ChevronDown v-if="!expandedModules[mod.id]" class="w-4 h-4" />
                      <ChevronUp v-else class="w-4 h-4" />
                    </div>
                  </button>

                  <!-- Lessons list -->
                  <div v-if="expandedModules[mod.id]" class="border-t border-white/5 bg-brand-dark/20 divide-y divide-white/5">
                    <div 
                      v-for="lesson in mod.lessons" 
                      :key="lesson.id"
                      class="flex items-center justify-between px-6 py-3.5 text-xs text-gray-300 hover:text-white transition-colors"
                    >
                      <div class="flex items-center space-x-3 truncate">
                        <Play v-if="lesson.type === 'video'" class="w-4 h-4 text-brand-primary shrink-0" />
                        <FileText v-else class="w-4 h-4 text-brand-accent shrink-0" />
                        <span class="truncate">{{ lesson.title }}</span>
                      </div>
                      <span class="text-gray-500 font-medium shrink-0 ml-4">{{ lesson.duration }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 3. Instructor Tab -->
            <div v-if="activeTab === 'instructor'" class="space-y-4">
              <div class="flex items-start space-x-4">
                <div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-brand-primary to-brand-secondary flex items-center justify-center font-bold text-white text-2xl shadow-lg shadow-brand-primary/10">
                  {{ course.teacherName.split(' ').map(n => n[0]).join('').toUpperCase() }}
                </div>
                <div class="space-y-1">
                  <h3 class="text-lg font-bold text-white font-display">{{ course.teacherName }}</h3>
                  <p class="text-xs text-brand-primary font-medium">Senior Educator at Aether Academy</p>
                  <p class="text-xs text-gray-400">Curating highly responsive technology paradigms since 2018.</p>
                </div>
              </div>
              
              <p class="text-xs md:text-sm text-gray-400 leading-relaxed font-light pt-4 border-t border-white/5">
                {{ course.teacherName }} is a dedicated professional instructor with thousands of student enrollments. Specializing in practical project development, her lessons prioritize step-by-step modular architectures, elegant responsive interfaces, and production-ready code principles.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column (Sticky Sidecard Panel) -->
      <div class="lg:sticky lg:top-24 space-y-6">
        <div class="glass-panel rounded-3xl overflow-hidden border border-white/5 bg-brand-card shadow-2xl p-6 flex flex-col space-y-6">
          <!-- Thumbnail aspect card -->
          <div class="aspect-video w-full rounded-2xl overflow-hidden bg-slate-800 shadow-md">
            <img :src="course.thumbnail" :alt="course.title" class="w-full h-full object-cover" />
          </div>

          <!-- Price & Metrics Row -->
          <div class="space-y-1">
            <div class="flex items-end justify-between">
              <span class="text-3xl font-extrabold text-white font-display">Free</span>
              <span class="text-xs text-gray-450 line-through">19,999 INR</span>
            </div>
            <p class="text-[10px] font-semibold text-brand-accent uppercase tracking-wider">Self-paced learning program</p>
          </div>

          <!-- Call To Action -->
          <div class="space-y-2 pt-2">
            <!-- Enrolled Status -->
            <router-link 
              v-if="isEnrolled"
              :to="`/student/player/${course.id}`"
              class="w-full text-center flex items-center justify-center space-x-2 py-3 bg-brand-accent text-white text-sm font-bold rounded-2xl shadow-lg shadow-brand-accent/15 transition-all hover:bg-emerald-600"
            >
              <span>You are Enrolled - Go to Player</span>
            </router-link>

            <!-- Pending Review / Non-student restrictions -->
            <div 
              v-else-if="authStore.isAuthenticated && !authStore.isStudent" 
              class="w-full text-center p-3 rounded-2xl bg-white/5 border border-white/10 text-xs text-gray-400 leading-relaxed"
            >
              <span>Signed in as <strong>{{ authStore.currentUser.role }}</strong>. Dashboard controls are active inside your portal.</span>
            </div>

            <!-- Standard enrollment click -->
            <button 
              v-else
              @click="handleEnrollment"
              class="w-full text-center flex items-center justify-center space-x-2 py-3 bg-brand-primary text-white text-sm font-bold rounded-2xl shadow-lg shadow-brand-primary/20 transition-all hover:bg-brand-secondary glow-btn"
            >
              <span>Enroll Now</span>
            </button>
          </div>

          <!-- Course Specs bullet list -->
          <div class="space-y-3.5 pt-4 border-t border-white/5 text-xs text-gray-300">
            <h4 class="text-[10px] font-bold text-white uppercase tracking-wider">Specifications:</h4>
            
            <div class="flex items-center justify-between">
              <span class="text-gray-450">Format:</span>
              <span class="font-medium text-white">Full On-Demand</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-450">Curriculum:</span>
              <span class="font-medium text-white">{{ totalLessonsCount }} Lessons</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-450">Includes:</span>
              <span class="font-medium text-brand-accent">Verified Certificate</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-450">Access:</span>
              <span class="font-medium text-white">Lifetime Free</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Fallback state if course is not located -->
  <div v-else class="text-center py-24 glass-panel max-w-xl mx-auto rounded-3xl border border-white/5 space-y-4">
    <h3 class="text-xl font-bold text-white">Program Not Found</h3>
    <p class="text-xs text-gray-400">The specific learning route you requested cannot be located in the active directory.</p>
    <router-link to="/" class="inline-block bg-brand-primary text-white text-xs font-semibold px-6 py-2.5 rounded-xl">
      Return Home
    </router-link>
  </div>
</template>
