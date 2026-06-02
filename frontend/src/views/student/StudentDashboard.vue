<script setup>
import { ref, computed, watch } from 'vue';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import { useNotificationStore } from '../../store/notifications';
import CourseCard from '../../components/CourseCard.vue';
import { 
  Award, Flame, BookOpen, Clock, Compass, Play, 
  CheckCircle, ArrowRight, X, Printer, ShieldCheck, Bookmark,
  Search, Filter, Target, Zap, Sparkles, Calendar, GraduationCap
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const notifStore = useNotificationStore();

const studentId = computed(() => authStore.currentUser?.id);
const studentName = computed(() => authStore.currentUser?.name);

// Get student enrollments
const enrollments = computed(() => coursesStore.getStudentEnrollments(studentId.value));

// Streak Count
const streak = computed(() => authStore.currentUser?.streakCount || 0);

// Bookmarks list
const bookmarks = computed(() => coursesStore.getStudentBookmarks(studentId.value));
const activeTab = ref('courses'); // courses or bookmarks

// Certificates list
const certificates = computed(() => coursesStore.getCertificates(studentId.value));

// Approved courses that the student is NOT enrolled in yet
const recommendedCourses = computed(() => {
  const enrolledCourseIds = enrollments.value.map(e => e.courseId);
  return coursesStore.approvedCourses.filter(c => !enrolledCourseIds.includes(c.id)).slice(0, 3);
});

// Search & Categories State
const searchQuery = ref('');
const selectedCategory = ref('All');

// Retrieve all categories from the list
const categories = computed(() => {
  const cats = new Set();
  enrollments.value.forEach(e => cats.add(e.course.category));
  bookmarks.value.forEach(b => cats.add(b.category));
  return ['All', ...cats];
});

// Filtered Enrollments & Wishlist
const filteredEnrollments = computed(() => {
  return enrollments.value.filter(e => {
    const titleMatch = e.course.title.toLowerCase().includes(searchQuery.value.toLowerCase());
    const descMatch = (e.course.shortDescription || e.course.description || '').toLowerCase().includes(searchQuery.value.toLowerCase());
    const categoryMatch = selectedCategory.value === 'All' || e.course.category === selectedCategory.value;
    return (titleMatch || descMatch) && categoryMatch;
  });
});

const filteredBookmarks = computed(() => {
  return bookmarks.value.filter(b => {
    const titleMatch = b.title.toLowerCase().includes(searchQuery.value.toLowerCase());
    const descMatch = (b.shortDescription || b.description || '').toLowerCase().includes(searchQuery.value.toLowerCase());
    const categoryMatch = selectedCategory.value === 'All' || b.category === selectedCategory.value;
    return (titleMatch || descMatch) && categoryMatch;
  });
});

// Weekly Target Goals Settings
const weeklyTargetHours = ref(Number(localStorage.getItem('aether_study_target') || '5'));

const hoursStudiedThisWeek = computed(() => {
  // Summing mock progress. Each completed lesson counts as 0.75 hrs. Base enrollment is 0.5 hrs.
  const totalCompleted = enrollments.value.reduce((acc, curr) => acc + curr.completedLessons.length, 0);
  return Number((totalCompleted * 0.75 + enrollments.value.length * 0.5).toFixed(1));
});

const targetPercent = computed(() => {
  if (weeklyTargetHours.value === 0) return 0;
  const pct = Math.round((hoursStudiedThisWeek.value / weeklyTargetHours.value) * 100);
  return Math.min(pct, 100);
});

const selectTargetHours = (hours) => {
  weeklyTargetHours.value = hours;
  localStorage.setItem('aether_study_target', hours.toString());
  notifStore.showToast("Study Goal Updated! 🎯", `Weekly goal successfully changed to ${hours} hours.`, "success");
};

// 7-Day Activity Calendar Check-in Logic
const checkedInDays = ref([]);

// Load the correct checked-in days dynamically per active student account to prevent bleed
watch(studentId, (newId) => {
  if (newId) {
    checkedInDays.value = JSON.parse(localStorage.getItem(`aether_checked_in_days_${newId}`) || '[]');
  } else {
    checkedInDays.value = [];
  }
}, { immediate: true });

const daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

const hasCheckedInToday = computed(() => {
  const todayName = new Date().toLocaleDateString('en-US', { weekday: 'short' }); // e.g. "Mon"
  return checkedInDays.value.includes(todayName);
});

const claimCheckIn = () => {
  const todayName = new Date().toLocaleDateString('en-US', { weekday: 'short' });
  if (checkedInDays.value.includes(todayName)) return;

  checkedInDays.value.push(todayName);
  localStorage.setItem(`aether_checked_in_days_${studentId.value || 'guest'}`, JSON.stringify(checkedInDays.value));

  // Dynamically update user's daily streak count
  if (authStore.currentUser) {
    authStore.currentUser.streakCount = (authStore.currentUser.streakCount || 0) + 1;
    // Update local database lists to keep synced
    const savedUsers = JSON.parse(localStorage.getItem('aether_users') || '[]');
    const idx = savedUsers.findIndex(u => u.id === authStore.currentUser.id);
    if (idx !== -1) {
      savedUsers[idx].streakCount = authStore.currentUser.streakCount;
      localStorage.setItem('aether_users', JSON.stringify(savedUsers));
    }
    localStorage.setItem('aether_current_user', JSON.stringify(authStore.currentUser));
  }

  notifStore.showToast("Streak Boosted! 🔥", "Successfully completed check-in! Keep learning everyday.", "success");
};

// Certificate Modal control
const activeCert = ref(null);
const isCertModalOpen = ref(false);

const openCertModal = (cert) => {
  activeCert.value = cert;
  isCertModalOpen.value = true;
};

const closeCertModal = () => {
  activeCert.value = null;
  isCertModalOpen.value = false;
};
</script>

<template>
  <div class="space-y-10 py-4">
    <!-- Welcome Header & Stats Grid -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="space-y-1.5">
        <h1 class="text-2xl md:text-3xl font-extrabold text-white font-display">
          Welcome back, {{ studentName }}!
        </h1>
        <p class="text-xs text-gray-400">Keep sharpening your skills. Your achievements are detailed below.</p>
      </div>
    </div>

    <!-- Analytics & Activity Board -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Widget 1: Weekly Study Goal (SVG Circular progress ring) -->
      <div class="glass-panel p-6 rounded-3xl border border-white/5 bg-brand-card flex flex-col sm:flex-row items-center justify-between gap-6 shadow-xl relative overflow-hidden group">
        <!-- Decorative subtle background glow -->
        <div class="absolute -right-10 -bottom-10 w-32 h-32 bg-brand-primary/10 rounded-full blur-2xl group-hover:bg-brand-primary/15 transition-all"></div>
        
        <div class="space-y-4 flex-grow">
          <div class="space-y-1">
            <span class="flex items-center space-x-1.5 text-brand-primary text-[10px] font-bold uppercase tracking-wider">
              <Target class="w-3.5 h-3.5" />
              <span>Weekly Target Goal</span>
            </span>
            <h3 class="text-base font-extrabold text-white font-display">Target Study Goal</h3>
            <p class="text-[11px] text-gray-400">Aim for high study hours to build up your skill levels.</p>
          </div>
          
          <!-- Hours Target Selector -->
          <div class="space-y-2">
            <p class="text-[9px] font-bold text-gray-450 uppercase tracking-widest">Select Weekly Target Hours</p>
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="hours in [2, 5, 10, 15]" 
                :key="hours"
                @click="selectTargetHours(hours)"
                class="px-3 py-1.5 rounded-xl text-[10px] font-bold border transition-all cursor-pointer"
                :class="weeklyTargetHours === hours 
                  ? 'bg-brand-primary border-transparent text-white shadow-md shadow-brand-primary/20' 
                  : 'bg-white/5 border-white/15 text-gray-400 hover:text-white hover:bg-white/10'"
              >
                {{ hours }}h / wk
              </button>
            </div>
          </div>
        </div>
        
        <!-- Circular Progress Ring Dashboard -->
        <div class="relative shrink-0 flex flex-col items-center justify-center p-2">
          <svg class="w-28 h-28 transform -rotate-90">
            <!-- Background circle -->
            <circle 
              cx="56" 
              cy="56" 
              r="46" 
              class="stroke-white/5" 
              stroke-width="8" 
              fill="transparent" 
            />
            <!-- Foreground glowing progress circle -->
            <circle 
              cx="56" 
              cy="56" 
              r="46" 
              class="stroke-brand-primary animate-draw-circle" 
              stroke-width="8" 
              fill="transparent" 
              :stroke-dasharray="2 * Math.PI * 46"
              :stroke-dashoffset="2 * Math.PI * 46 * (1 - targetPercent / 100)"
              stroke-linecap="round"
            />
          </svg>
          <!-- Absolute center values -->
          <div class="absolute flex flex-col items-center justify-center text-center">
            <span class="text-lg font-black text-white leading-none">{{ hoursStudiedThisWeek }}h</span>
            <span class="text-[9px] text-brand-primary font-bold mt-0.5">Target: {{ weeklyTargetHours }}h</span>
          </div>
          <p class="text-[9px] text-brand-accent font-bold mt-2 tracking-wide uppercase">{{ targetPercent }}% Completed</p>
        </div>
      </div>
      
      <!-- Widget 2: 7-Day Activity Calendar & Streak check-in -->
      <div class="glass-panel p-6 rounded-3xl border border-white/5 bg-brand-card flex flex-col justify-between gap-5 shadow-xl relative overflow-hidden group">
        <!-- Subtle back glow -->
        <div class="absolute -right-10 -bottom-10 w-32 h-32 bg-brand-warning/5 rounded-full blur-2xl group-hover:bg-brand-warning/10 transition-all"></div>
        
        <div class="flex items-start justify-between gap-4">
          <div class="space-y-1">
            <span class="flex items-center space-x-1.5 text-brand-warning text-[10px] font-bold uppercase tracking-wider">
              <Calendar class="w-3.5 h-3.5" />
              <span>Streak Extender</span>
            </span>
            <h3 class="text-base font-extrabold text-white font-display">Weekly Activity Calendar</h3>
            <p class="text-[11px] text-gray-400">Complete a daily learning session to boost your study velocity!</p>
          </div>
          
          <!-- Pulse Check-in button -->
          <button 
            @click="claimCheckIn"
            :disabled="hasCheckedInToday"
            class="px-4 py-2 text-[10px] font-bold rounded-xl transition-all shadow-md shrink-0 flex items-center space-x-1.5 cursor-pointer select-none"
            :class="hasCheckedInToday 
              ? 'bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 cursor-not-allowed' 
              : 'bg-brand-warning hover:bg-amber-600 text-white shadow-brand-warning/15 hover:scale-[1.03] active:scale-[0.98] animate-pulse'"
          >
            <Zap class="w-3.5 h-3.5" />
            <span>{{ hasCheckedInToday ? 'Checked In Today' : 'Daily Check-In' }}</span>
          </button>
        </div>
        
        <!-- Row of Days -->
        <div class="grid grid-cols-7 gap-2">
          <div 
            v-for="day in daysOfWeek" 
            :key="day"
            class="flex flex-col items-center p-2 rounded-xl border transition-all"
            :class="checkedInDays.includes(day)
              ? 'bg-brand-warning/15 border-brand-warning/30 text-brand-warning font-extrabold scale-[1.02] shadow-sm shadow-brand-warning/5'
              : 'bg-white/5 border-white/5 text-gray-400 font-medium'"
          >
            <span class="text-[9px] uppercase tracking-wider font-semibold">{{ day }}</span>
            <div class="mt-1.5 w-6 h-6 rounded-full flex items-center justify-center bg-brand-dark/40 border border-white/5">
              <CheckCircle v-if="checkedInDays.includes(day)" class="w-3.5 h-3.5 text-brand-warning" />
              <div v-else class="w-1.5 h-1.5 rounded-full bg-white/10"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Course Section & Right sidebar -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
      <!-- Left Column (Active Enrollments & Bookmarks) -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Tabs Header Switcher -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/5 pb-3">
          <div class="flex items-center space-x-2">
            <button 
              @click="activeTab = 'courses'"
              class="px-4 py-2 text-xs font-bold uppercase tracking-wider border-b-2 transition-all flex items-center space-x-2 cursor-pointer"
              :class="activeTab === 'courses' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
            >
              <Play class="w-4 h-4" />
              <span>Enrolled Courses ({{ enrollments.length }})</span>
            </button>
            
            <button 
              @click="activeTab = 'bookmarks'"
              class="px-4 py-2 text-xs font-bold uppercase tracking-wider border-b-2 transition-all flex items-center space-x-2 cursor-pointer"
              :class="activeTab === 'bookmarks' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
            >
              <Bookmark class="w-4 h-4" />
              <span>My Wishlist ({{ bookmarks.length }})</span>
            </button>
          </div>
        </div>

        <!-- Search & Filter Console -->
        <div class="flex flex-col sm:flex-row gap-3">
          <!-- Search input -->
          <div class="relative flex-grow">
            <Search class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
            <input 
              v-model="searchQuery"
              type="text"
              placeholder="Search enrolled or bookmarked courses..."
              class="w-full pl-10 pr-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-1 focus:ring-brand-primary placeholder-gray-550 transition-all shadow-inner"
            />
            <button 
              v-if="searchQuery"
              @click="searchQuery = ''"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white p-0.5 rounded-md hover:bg-white/5"
            >
              <X class="w-3.5 h-3.5" />
            </button>
          </div>
          
          <!-- Category selector drop down -->
          <div class="flex items-center space-x-2 shrink-0">
            <select 
              v-model="selectedCategory"
              class="w-full sm:w-auto px-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-gray-300 rounded-xl focus:outline-none focus:ring-1 focus:ring-brand-primary cursor-pointer transition-all shadow-inner"
            >
              <option value="All">All Categories</option>
              <option 
                v-for="cat in categories.filter(c => c !== 'All')" 
                :key="cat" 
                :value="cat"
              >
                {{ cat }}
              </option>
            </select>
          </div>
        </div>

        <!-- 1. Enrolled Courses Tab Content -->
        <div v-if="activeTab === 'courses'" class="space-y-6">
          <div v-if="filteredEnrollments.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div 
              v-for="enroll in filteredEnrollments" 
              :key="enroll.id"
              class="glass-panel rounded-2xl overflow-hidden bg-brand-card border border-white/5 flex flex-col h-full hover:shadow-lg transition-all"
            >
              <!-- Card Thumbnail aspect -->
              <div class="relative aspect-video w-full overflow-hidden bg-slate-800">
                <img :src="enroll.course.thumbnail" :alt="enroll.course.title" class="w-full h-full object-cover" />
                <!-- Completed Overlay stamp -->
                <div 
                  v-if="enroll.progressPercent === 100" 
                  class="absolute inset-0 bg-brand-accent/20 backdrop-blur-xs flex items-center justify-center"
                >
                  <span class="flex items-center space-x-1.5 px-3 py-1 rounded-full bg-brand-accent text-white text-[10px] font-bold tracking-wider uppercase shadow-md animate-bounce">
                    <CheckCircle class="w-3.5 h-3.5" />
                    <span>Syllabus Completed</span>
                  </span>
                </div>
              </div>

              <!-- Content details -->
              <div class="p-5 flex-grow flex flex-col justify-between">
                <div class="space-y-1 mb-4">
                  <span class="px-2 py-0.5 text-[9px] font-bold uppercase tracking-wider bg-brand-primary/10 text-brand-primary rounded-md">
                    {{ enroll.course.category }}
                  </span>
                  <h3 class="text-sm font-bold text-white font-display line-clamp-1 leading-snug">{{ enroll.course.title }}</h3>
                  <p class="text-[11px] text-gray-400 line-clamp-2">{{ enroll.course.shortDescription || enroll.course.description }}</p>
                </div>

                <!-- Progress bar indicator -->
                <div class="space-y-4">
                  <div class="space-y-1.5">
                    <div class="flex items-center justify-between text-[10px] font-bold text-gray-300">
                      <span>Progress Level</span>
                      <span class="text-brand-accent font-extrabold">{{ enroll.progressPercent }}%</span>
                    </div>
                    <div class="w-full bg-brand-dark rounded-full h-1 overflow-hidden">
                      <div 
                        class="bg-gradient-to-r from-brand-primary to-brand-accent h-full transition-all duration-300"
                        :style="{ width: `${enroll.progressPercent}%` }"
                      ></div>
                    </div>
                  </div>

                  <!-- Action Button rows -->
                  <div class="flex flex-col gap-2 pt-2">
                    <router-link 
                      :to="`/student/player/${enroll.courseId}`"
                      class="w-full text-center py-2 bg-brand-primary/10 text-brand-primary hover:bg-brand-primary hover:text-white text-xs font-semibold rounded-xl transition-all border border-brand-primary/20 hover:border-transparent flex items-center justify-center space-x-1.5"
                    >
                      <Play class="w-3.5 h-3.5 shrink-0" />
                      <span>{{ enroll.progressPercent === 100 ? 'Review Lessons' : 'Resume Modules' }}</span>
                    </router-link>

                    <!-- Certificate Download CTA -->
                    <button 
                      v-if="enroll.progressPercent === 100"
                      @click="openCertModal({
                        id: `CERT-${enroll.id.toUpperCase()}`,
                        courseTitle: enroll.course.title,
                        completedDate: enroll.completedDate || enroll.enrolledDate,
                        instructor: enroll.course.teacherName
                      })"
                      class="w-full text-center py-2 bg-brand-accent/20 text-brand-accent hover:bg-brand-accent hover:text-white text-xs font-semibold rounded-xl transition-all border border-brand-accent/30 hover:border-transparent flex items-center justify-center space-x-1.5"
                    >
                      <Award class="w-3.5 h-3.5 shrink-0" />
                      <span>Download Certificate</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty search results state -->
          <div 
            v-else-if="enrollments.length > 0" 
            class="glass-panel p-12 text-center rounded-2xl border border-white/5 flex flex-col items-center justify-center space-y-3 bg-brand-card/10"
          >
            <div class="p-3 bg-white/5 text-gray-400 border border-white/10 rounded-full">
              <Search class="w-5 h-5" />
            </div>
            <h3 class="text-sm font-bold text-white">No Matching Enrolled Courses</h3>
            <p class="text-xs text-gray-450 leading-relaxed max-w-sm">
              We couldn't find any courses matching "{{ searchQuery }}" with category "{{ selectedCategory }}".
            </p>
            <button 
              @click="searchQuery = ''; selectedCategory = 'All';" 
              class="bg-white/5 border border-white/10 hover:bg-white/10 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all"
            >
              Clear Filters
            </button>
          </div>

          <!-- Enrolled fallback empty state -->
          <div 
            v-else 
            class="glass-panel p-12 text-center rounded-2xl border border-white/5 flex flex-col items-center justify-center space-y-4 bg-brand-card/25"
          >
            <div class="p-3 bg-brand-primary/10 text-brand-primary border border-brand-primary/20 rounded-full">
              <BookOpen class="w-6 h-6" />
            </div>
            <h3 class="text-sm font-bold text-white">No Enrolled Courses</h3>
            <p class="text-xs text-gray-450 leading-relaxed max-w-sm">
              You haven't enrolled in any educational paths yet. Browse approved listings and start building your skill stacks.
            </p>
            <router-link 
              to="/student/courses" 
              class="bg-brand-primary text-white text-xs font-bold px-5 py-2.5 rounded-xl transition-all hover:bg-brand-secondary inline-flex items-center space-x-1"
            >
              <span>Explore Course Catalog</span>
              <ArrowRight class="w-4 h-4" />
            </router-link>
          </div>
        </div>

        <!-- 2. Bookmarked Courses Tab Content -->
        <div v-else-if="activeTab === 'bookmarks'" class="space-y-6 animate-fade-in">
          <div v-if="filteredBookmarks.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div v-for="course in filteredBookmarks" :key="course.id" class="h-full">
              <CourseCard :course="course" />
            </div>
          </div>

          <!-- Empty search bookmarks state -->
          <div 
            v-else-if="bookmarks.length > 0" 
            class="glass-panel p-12 text-center rounded-2xl border border-white/5 flex flex-col items-center justify-center space-y-3 bg-brand-card/10"
          >
            <div class="p-3 bg-white/5 text-gray-400 border border-white/10 rounded-full">
              <Search class="w-5 h-5" />
            </div>
            <h3 class="text-sm font-bold text-white">No Matching Wishlist Items</h3>
            <p class="text-xs text-gray-450 leading-relaxed max-w-sm">
              We couldn't find any bookmarks matching "{{ searchQuery }}" with category "{{ selectedCategory }}".
            </p>
            <button 
              @click="searchQuery = ''; selectedCategory = 'All';" 
              class="bg-white/5 border border-white/10 hover:bg-white/10 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all"
            >
              Clear Filters
            </button>
          </div>
          
          <div 
            v-else 
            class="glass-panel p-12 text-center rounded-2xl border border-white/5 flex flex-col items-center justify-center space-y-4 bg-brand-card/25"
          >
            <div class="p-3 bg-brand-primary/10 text-brand-primary border border-brand-primary/20 rounded-full">
              <Bookmark class="w-6 h-6" />
            </div>
            <h3 class="text-sm font-bold text-white">Your Wishlist is Empty</h3>
            <p class="text-xs text-gray-450 leading-relaxed max-w-sm">
              Bookmark programs in the home catalog to save them for later enrollment reviews.
            </p>
            <router-link 
              to="/student/courses" 
              class="bg-brand-primary text-white text-xs font-bold px-5 py-2.5 rounded-xl transition-all hover:bg-brand-secondary inline-flex items-center space-x-1"
            >
              <span>Browse Catalog Items</span>
              <ArrowRight class="w-4 h-4" />
            </router-link>
          </div>
        </div>
      </div>

      <!-- Right Column (Streaks, Certificates & Suggestions list) -->
      <div class="space-y-8">
        
        <!-- Certificates drawer column -->
        <div class="glass-panel rounded-3xl p-6 border border-white/5 bg-brand-card flex flex-col space-y-4">
          <h3 class="text-sm font-bold text-white font-display flex items-center space-x-2">
            <Award class="w-4.5 h-4.5 text-brand-warning" />
            <span>My Certificates ({{ certificates.length }})</span>
          </h3>

          <div v-if="certificates.length > 0" class="space-y-3">
            <div 
              v-for="cert in certificates" 
              :key="cert.id"
              @click="openCertModal(cert)"
              class="p-3 bg-brand-dark/40 hover:bg-brand-dark/80 border border-white/5 rounded-2xl flex items-center justify-between cursor-pointer group transition-colors"
            >
              <div class="space-y-1 truncate pr-3">
                <p class="text-xs font-bold text-white group-hover:text-brand-accent transition-colors truncate font-display">{{ cert.courseTitle }}</p>
                <p class="text-[9px] text-gray-500 font-semibold">{{ cert.id }}</p>
              </div>
              <Award class="w-5 h-5 text-brand-accent shrink-0" />
            </div>
          </div>
          
          <div v-else class="p-3 bg-brand-dark/20 border border-dashed border-white/5 rounded-2xl text-center text-[11px] text-gray-500 leading-normal">
            Your earned certificates will populate here automatically upon 100% completion of any course.
          </div>
        </div>

        <!-- Recommendations column -->
        <div id="recommended-sec" class="space-y-4">
          <h3 class="text-sm font-bold text-white font-display flex items-center space-x-2">
            <Compass class="w-4.5 h-4.5 text-brand-accent" />
            <span>Recommended for You</span>
          </h3>

          <div v-if="recommendedCourses.length > 0" class="space-y-4">
            <div 
              v-for="course in recommendedCourses" 
              :key="course.id"
              class="p-4 bg-brand-card border border-white/5 rounded-2xl hover:translate-y-[-2px] transition-all flex gap-3.5 items-start"
            >
              <img :src="course.thumbnail" :alt="course.title" class="w-12 h-12 rounded-xl object-cover bg-slate-800 shrink-0" />
              <div class="space-y-1.5 flex-grow truncate">
                <span class="px-1.5 py-0.5 text-[8px] font-bold bg-brand-primary/10 text-brand-primary rounded uppercase">
                  {{ course.category }}
                </span>
                <h4 class="text-xs font-bold text-white truncate">{{ course.title }}</h4>
                <router-link 
                  :to="`/courses/${course.id}`" 
                  class="text-[10px] font-bold text-brand-primary hover:text-brand-secondary inline-flex items-center space-x-0.5"
                >
                  <span>Learn & Enroll</span>
                  <ArrowRight class="w-3 h-3" />
                </router-link>
              </div>
            </div>
          </div>

          <div class="p-3 bg-brand-dark/20 border border-dashed border-white/5 rounded-2xl text-center text-[11px] text-gray-550" v-else>
            You've enrolled in everything! Keep learning.
          </div>
        </div>

      </div>
    </div>

    <!-- Certificate Overlay Printable Modal -->
    <div 
      v-if="isCertModalOpen && activeCert" 
      class="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4 bg-brand-dark/90 backdrop-blur-md animate-fade-in"
    >
      <!-- Modal Inner Box (Expanded to 4xl for landscape proportions) -->
      <div class="relative w-full max-w-4xl bg-brand-card border border-white/10 rounded-3xl overflow-hidden shadow-2xl p-6 md:p-10 space-y-6">
        <!-- Close button (non-printable) -->
        <button 
          @click="closeCertModal"
          class="absolute top-4 right-4 p-2 text-gray-400 hover:text-white bg-white/5 hover:bg-white/10 rounded-xl transition-all print:hidden"
        >
          <X class="w-5 h-5" />
        </button>

        <!-- Printable Certificate Card (Premium gold-sealed landscape design matching user template) -->
        <div class="certificate-paper relative w-full aspect-[1.414/1] bg-white text-[#2c3e50] shadow-2xl rounded-2xl overflow-hidden flex flex-col justify-between select-none shadow-slate-950/30">
          
          <!-- Background SVG Vector Graphics -->
          <svg class="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 1000 707" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <!-- Gold Gradient for strokes and borders -->
              <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#f3d075" />
                <stop offset="50%" stop-color="#c5a880" />
                <stop offset="100%" stop-color="#9a7b45" />
              </linearGradient>
              <!-- Radiant gold gradient for the seal ribbons -->
              <linearGradient id="ribbonGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ffd700" />
                <stop offset="50%" stop-color="#e5b80b" />
                <stop offset="100%" stop-color="#bca06a" />
              </linearGradient>
              <!-- Deep Navy Shadow -->
              <filter id="navyShadow" x="-10%" y="-10%" width="120%" height="120%">
                <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#05080c" flood-opacity="0.3" />
              </filter>
            </defs>
            
            <!-- Deep Dark Slate Navy Backdrop (Filled Shape) -->
            <path d="M 0,0 L 1000,0 L 1000,340 C 850,480 680,535 500,535 C 320,535 150,480 0,340 Z" fill="#19242d" filter="url(#navyShadow)" />
            
            <!-- Curved Gold Accent Line at bottom of navy background -->
            <path d="M 0,340 C 150,480 320,535 500,535 C 680,535 850,480 1000,340" stroke="url(#goldGrad)" stroke-width="4" />

            <!-- Inner Gold Panel Border Frame -->
            <path d="M 35,35 L 965,35 L 965,310 C 825,440 665,490 500,490 C 335,490 175,440 35,310 Z" stroke="url(#goldGrad)" stroke-width="3" stroke-linecap="round" />
            
            <!-- Gold Ribbons hanging from the seal (Center: 500, 535) -->
            <g filter="drop-shadow(0px 3px 4px rgba(0,0,0,0.15))">
              <path d="M 485,530 L 468,615 L 485,600 L 502,615 L 493,530" fill="url(#ribbonGrad)" />
              <path d="M 515,530 L 498,615 L 515,600 L 532,615 L 523,530" fill="url(#ribbonGrad)" />
            </g>
          </svg>

          <!-- Floating 3D Gold Foil Medallion Seal (Positioned exactly over ribbons) -->
          <div class="absolute top-[75.6%] left-1/2 -translate-x-1/2 -translate-y-1/2 z-20 select-none print:transform print:scale-100">
            <div class="relative w-15 h-15 md:w-20 md:h-20 bg-gradient-to-br from-[#ffd700] via-[#e5b80b] to-[#bca06a] rounded-full shadow-lg border border-[#c5a880]/50 p-[3px] flex items-center justify-center animate-shine overflow-hidden">
              <!-- Serrated starburst foil edge -->
              <div class="absolute inset-0 bg-[#e5b80b] rounded-full clip-starburst opacity-60"></div>
              
              <!-- Inner embossed circle -->
              <div class="w-full h-full bg-gradient-to-br from-[#fff099] via-[#e5b80b] to-[#a67b1e] rounded-full p-[1.5px] shadow-inner flex items-center justify-center border border-[#fff]/40">
                <div class="w-full h-full bg-gradient-to-br from-[#dfb954] to-[#c19932] rounded-full flex flex-col items-center justify-center shadow-md relative">
                  <div class="text-[3.5px] md:text-[5px] text-[#3d2c05] font-extrabold uppercase tracking-widest text-center mt-0.5 filter drop-shadow-[0_0.5px_0_rgba(255,255,255,0.4)]">
                    AETHER
                  </div>
                  <Award class="w-5 h-5 md:w-7 md:h-7 text-[#fff] opacity-95 filter drop-shadow-[0_1px_1px_rgba(0,0,0,0.2)] my-0.5" />
                  <div class="text-[3px] md:text-[4px] text-[#3d2c05] font-extrabold uppercase tracking-widest text-center filter drop-shadow-[0_0.5px_0_rgba(255,255,255,0.4)]">
                    VERIFIED
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Content Layout -->
          <div class="relative z-10 flex flex-col justify-between h-full w-full p-6 md:p-12">
            
            <!-- Dark Navy Upper Panel Content -->
            <div class="flex flex-col justify-center items-center text-center space-y-3 pt-2 md:pt-4">
              <!-- Institution Subtitle -->
              <h3 class="text-[8px] md:text-[10px] font-semibold uppercase tracking-[0.25em] text-[#dfc18a] font-sans">
                Aether Academy of Digital Science
              </h3>
              
              <!-- Large Heading -->
              <div class="space-y-0.5">
                <h1 class="text-2xl md:text-5xl font-extrabold tracking-wider text-white font-display uppercase leading-tight">
                  Certificate
                </h1>
                <h2 class="text-[9px] md:text-sm font-semibold tracking-[0.35em] text-gray-300 font-sans uppercase">
                  of Completion
                </h2>
              </div>

              <!-- Proudly Presented text -->
              <p class="text-[8px] md:text-[10px] text-gray-300 tracking-[0.15em] font-sans uppercase pt-2">
                This credential is proudly presented to
              </p>

              <!-- Recipient Name (Beautiful cursive calligraphy) -->
              <h2 class="font-signature text-3xl md:text-5.5xl text-[#e5b80b] tracking-wide leading-none py-1 filter drop-shadow-[0_1.5px_1px_rgba(0,0,0,0.3)]">
                {{ studentName }}
              </h2>

              <!-- Horizontal divider inside dark panel -->
              <div class="w-36 md:w-48 border-t border-white/20 mx-auto py-1"></div>

              <!-- Explanatory Details & Course Name -->
              <div class="space-y-1.5 max-w-xl mx-auto">
                <p class="text-[7px] md:text-[9px] leading-relaxed text-gray-300 tracking-wide font-sans">
                  for having successfully met all strict academic requirements, curriculum milestones, assessments, and capstone practical projects for the comprehensive verified training course
                </p>
                <h4 class="text-xs md:text-base font-bold text-white font-display tracking-widest uppercase">
                  {{ activeCert.courseTitle }}
                </h4>
              </div>
            </div>

            <!-- White Lower Panel Content -->
            <div class="grid grid-cols-3 items-end w-full pb-2">
              
              <!-- Left side: Date of Issue -->
              <div class="text-center space-y-1">
                <p class="text-[9px] md:text-xs text-[#2c3e50] font-semibold font-sans tracking-wide">
                  {{ activeCert.completedDate }}
                </p>
                <div class="border-t border-[#c5a880]/60 w-full max-w-[100px] md:max-w-[140px] mx-auto pt-1"></div>
                <p class="text-[7px] md:text-[8px] text-[#606f7b] font-bold uppercase tracking-widest">Date</p>
              </div>

              <!-- Center side: empty to allow space for the gold seal overlay -->
              <div class="h-1 text-center"></div>

              <!-- Right side: Signature -->
              <div class="text-center space-y-1">
                <!-- Instructor Signature Cursive -->
                <p class="font-signature text-xl md:text-3xl text-[#1034a6] select-none rotate-[-1deg] tracking-wide leading-none pb-0.5">
                  {{ activeCert.instructor }}
                </p>
                <div class="border-t border-[#c5a880]/60 w-full max-w-[100px] md:max-w-[140px] mx-auto pt-1"></div>
                <p class="text-[7px] md:text-[8px] text-[#606f7b] font-bold uppercase tracking-widest">Signature</p>
              </div>

            </div>

          </div>
        </div>

        <!-- Action bar (non-printable) -->
        <div class="flex justify-end pt-2 print:hidden">
          <button 
            @click="closeCertModal"
            class="px-5 py-2 rounded-xl text-xs font-semibold bg-brand-primary text-white hover:bg-brand-secondary transition-all shadow-md shadow-brand-primary/10 border border-white/5"
          >
            Close Viewer
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<style>
/* Custom Certificate Typography & Effects */
.font-serif-cinzel {
  font-family: 'Cinzel', Georgia, serif;
}
.font-serif-playfair {
  font-family: 'Playfair Display', Georgia, serif;
}
.font-signature {
  font-family: 'Great Vibes', cursive;
}
.clip-ribbon {
  clip-path: polygon(0% 0%, 100% 0%, 100% 88%, 50% 100%, 0% 88%);
}
.clip-starburst {
  clip-path: polygon(
    50% 0%, 54% 12%, 65% 5%, 66% 18%, 78% 15%, 76% 28%, 88% 28%, 83% 40%, 93% 43%, 85% 53%, 93% 58%, 83% 66%, 88% 78%, 76% 78%, 78% 90%, 66% 88%, 65% 100%, 54% 93%, 50% 100%, 46% 93%, 35% 100%, 34% 88%, 22% 90%, 24% 78%, 12% 78%, 17% 66%, 7% 58%, 15% 53%, 7% 43%, 17% 40%, 12% 28%, 24% 28%, 22% 15%, 34% 18%, 35% 5%, 46% 12%
  );
}
.certificate-paper {
  box-shadow: 0 25px 50px -12px rgba(17, 24, 39, 0.25);
}

/* Gold foil seal shine animation */
@keyframes shine {
  0% { transform: translateX(-100%) rotate(45deg); }
  100% { transform: translateX(100%) rotate(45deg); }
}
.animate-shine::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.3) 30%,
    rgba(255, 255, 255, 0.7) 50%,
    rgba(255, 255, 255, 0.3) 70%,
    rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(45deg);
  transition: all 0.5s;
}
.animate-shine:hover::after {
  animation: shine 1.2s ease-in-out infinite;
}

/* Print Layout styling overrides */
@media print {
  @page {
    size: landscape;
    margin: 0;
  }
  
  body {
    background: transparent !important;
  }
  
  body * {
    visibility: hidden !important;
  }
  
  /* Force overlay container to occupy full viewport */
  .fixed.inset-0, .fixed.inset-0 * {
    visibility: visible !important;
  }
  
  .fixed.inset-0 {
    position: absolute !important;
    left: 0 !important;
    top: 0 !important;
    width: 100% !important;
    height: 100% !important;
    background: white !important;
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    backdrop-filter: none !important;
  }

  .bg-brand-card {
    background: white !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    width: 100% !important;
    max-width: none !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
  }

  .certificate-paper {
    width: 297mm !important; /* Standard A4 width */
    height: 210mm !important; /* Standard A4 height */
    box-shadow: none !important;
    border-radius: 0 !important;
    border-width: 0 !important;
    padding: 0 !important;
    margin: 0 auto !important;
    background: #ffffff !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  .print\:hidden {
    display: none !important;
  }
}
</style>
