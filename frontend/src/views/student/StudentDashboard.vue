<script setup>
import { ref, computed } from 'vue';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import CourseCard from '../../components/CourseCard.vue';
import { 
  Award, Flame, BookOpen, Clock, Compass, Play, 
  CheckCircle, ArrowRight, X, Printer, ShieldCheck, Bookmark
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();

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

const printCert = () => {
  window.print();
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

      <!-- Quick stats summaries -->
      <div class="flex flex-wrap items-center gap-4 shrink-0">
        <!-- Enrolled count -->
        <div class="flex items-center space-x-3 px-4.5 py-2.5 bg-brand-card border border-white/5 rounded-2xl shadow-sm">
          <BookOpen class="w-5 h-5 text-brand-primary" />
          <div>
            <div class="text-sm font-bold text-white">{{ enrollments.length }}</div>
            <p class="text-[9px] font-semibold text-gray-405 uppercase tracking-wider">Courses</p>
          </div>
        </div>

        <!-- Streak Count -->
        <div class="flex items-center space-x-3 px-4.5 py-2.5 bg-brand-card border border-white/5 rounded-2xl shadow-sm">
          <Flame class="w-5 h-5 text-brand-warning animate-bounce" />
          <div>
            <div class="text-sm font-bold text-white">{{ streak }} Days</div>
            <p class="text-[9px] font-semibold text-gray-455 uppercase tracking-wider">Daily Streak</p>
          </div>
        </div>

        <!-- Certificates Count -->
        <div class="flex items-center space-x-3 px-4.5 py-2.5 bg-brand-card border border-white/5 rounded-2xl shadow-sm">
          <Award class="w-5 h-5 text-brand-accent" />
          <div>
            <div class="text-sm font-bold text-white">{{ certificates.length }}</div>
            <p class="text-[9px] font-semibold text-gray-455 uppercase tracking-wider">Certificates</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Course Section & Right sidebar -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
      <!-- Left Column (Active Enrollments & Bookmarks) -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Tabs Header Switcher -->
        <div class="flex items-center space-x-4 border-b border-white/5 pb-0">
          <button 
            @click="activeTab = 'courses'"
            class="px-4 py-2.5 text-xs font-bold uppercase tracking-wider border-b-2 transition-all flex items-center space-x-2 cursor-pointer"
            :class="activeTab === 'courses' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
          >
            <Play class="w-4 h-4" />
            <span>Enrolled Courses ({{ enrollments.length }})</span>
          </button>
          
          <button 
            @click="activeTab = 'bookmarks'"
            class="px-4 py-2.5 text-xs font-bold uppercase tracking-wider border-b-2 transition-all flex items-center space-x-2 cursor-pointer"
            :class="activeTab === 'bookmarks' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
          >
            <Bookmark class="w-4 h-4" />
            <span>My Wishlist ({{ bookmarks.length }})</span>
          </button>
        </div>

        <!-- 1. Enrolled Courses Tab Content -->
        <div v-if="activeTab === 'courses'" class="space-y-6">
          <div v-if="enrollments.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div 
              v-for="enroll in enrollments" 
              :key="enroll.id"
              class="glass-panel rounded-2xl overflow-hidden bg-brand-card border border-white/5 flex flex-col h-full hover:shadow-lg transition-all"
            >
              <!-- Card Thumbnail aspect aspect -->
              <div class="relative aspect-video w-full overflow-hidden bg-slate-800">
                <img :src="enroll.course.thumbnail" :alt="enroll.course.title" class="w-full h-full object-cover" />
                <!-- Completed Overlay stamp -->
                <div 
                  v-if="enroll.progressPercent === 100" 
                  class="absolute inset-0 bg-brand-accent/20 backdrop-blur-xs flex items-center justify-center"
                >
                  <span class="flex items-center space-x-1.5 px-3 py-1 rounded-full bg-brand-accent text-white text-[10px] font-bold tracking-wider uppercase shadow-md">
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
                      <span class="text-brand-accent">{{ enroll.progressPercent }}%</span>
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
                      class="w-full text-center py-2 bg-brand-primary/10 text-brand-primary hover:bg-brand-primary text-white hover:text-white text-xs font-semibold rounded-xl transition-all border border-brand-primary/20 hover:border-transparent flex items-center justify-center space-x-1.5"
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
            <a 
              href="#recommended-sec" 
              class="bg-brand-primary text-white text-xs font-bold px-5 py-2.5 rounded-xl transition-all hover:bg-brand-secondary inline-flex items-center space-x-1"
            >
              <span>Explore Course Catalog</span>
              <ArrowRight class="w-4 h-4" />
            </a>
          </div>
        </div>

        <!-- 2. Bookmarked Courses Tab Content -->
        <div v-else-if="activeTab === 'bookmarks'" class="space-y-6 animate-fade-in">
          <div v-if="bookmarks.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div v-for="course in bookmarks" :key="course.id" class="h-full">
              <CourseCard :course="course" />
            </div>
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
            <a 
              href="/" 
              class="bg-brand-primary text-white text-xs font-bold px-5 py-2.5 rounded-xl transition-all hover:bg-brand-secondary inline-flex items-center space-x-1"
            >
              <span>Browse Catalog Items</span>
              <ArrowRight class="w-4 h-4" />
            </a>
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
      <!-- Modal Inner Box -->
      <div class="relative w-full max-w-3xl bg-brand-card border border-white/10 rounded-3xl overflow-hidden shadow-2xl p-6 md:p-12 space-y-6">
        <!-- Close button (non-printable) -->
        <button 
          @click="closeCertModal"
          class="absolute top-4 right-4 p-2 text-gray-400 hover:text-white bg-white/5 hover:bg-white/10 rounded-xl transition-all print:hidden"
        >
          <X class="w-5 h-5" />
        </button>

        <!-- Printable Certificate Card -->
        <div class="border-[8px] border-double border-brand-warning/35 p-6 md:p-10 rounded-2xl flex flex-col items-center text-center space-y-6 bg-brand-dark/20 bg-[radial-gradient(circle_at_center,rgba(245,158,11,0.02),transparent_70%)]">
          <!-- Emblem logo -->
          <div class="flex items-center justify-center p-4 rounded-full bg-brand-warning/10 text-brand-warning border border-brand-warning/20">
            <Award class="w-12 h-12" />
          </div>

          <!-- Titles -->
          <div class="space-y-1">
            <h3 class="text-xs font-bold tracking-widest text-brand-warning uppercase font-display">Aether Academy of Digital Science</h3>
            <p class="text-2xl md:text-3xl font-extrabold tracking-tight text-white font-display">CERTIFICATE OF COMPLETION</p>
          </div>

          <!-- Divider -->
          <div class="w-24 border-t-2 border-brand-warning/45"></div>

          <!-- Body -->
          <div class="space-y-4">
            <p class="text-xs text-gray-400 font-medium italic tracking-wider">This verifies that</p>
            <h4 class="text-xl md:text-2xl font-extrabold text-white font-display tracking-wide uppercase">{{ studentName }}</h4>
            <p class="text-xs text-gray-400 leading-relaxed max-w-md mx-auto font-light">
              has successfully fulfilled all strict curriculum modules, assessments, and coding projects for the verified training course
            </p>
            <h5 class="text-base md:text-lg font-bold text-brand-accent font-display tracking-tight">{{ activeCert.courseTitle }}</h5>
          </div>

          <!-- Signatures row -->
          <div class="grid grid-cols-2 gap-8 w-full max-w-md pt-8 border-t border-white/5">
            <div class="space-y-1">
              <p class="text-xs font-bold text-white font-display italic tracking-wide">{{ activeCert.instructor }}</p>
              <div class="border-t border-gray-600/40 w-full pt-1"></div>
              <p class="text-[9px] text-gray-500 font-semibold uppercase tracking-wider">Course Instructor</p>
            </div>
            
            <div class="space-y-1">
              <div class="flex items-center justify-center space-x-1 text-xs font-bold text-brand-primary font-display tracking-wider">
                <ShieldCheck class="w-3.5 h-3.5" />
                <span>AETHER VERIFIED</span>
              </div>
              <div class="border-t border-gray-600/40 w-full pt-1"></div>
              <p class="text-[9px] text-gray-500 font-semibold uppercase tracking-wider">Chief Academic Officer</p>
            </div>
          </div>

          <!-- Credentials footer -->
          <div class="flex justify-between w-full pt-6 text-[9px] text-gray-500 font-medium">
            <span>Issue Date: {{ activeCert.completedDate }}</span>
            <span>ID: {{ activeCert.id }}</span>
          </div>
        </div>

        <!-- Action bar (non-printable) -->
        <div class="flex justify-end space-x-3 pt-2 print:hidden">
          <button 
            @click="closeCertModal"
            class="px-4.5 py-2 rounded-xl text-xs font-semibold bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white transition-colors border border-white/5"
          >
            Close Viewer
          </button>
          <button 
            @click="printCert"
            class="px-5 py-2 rounded-xl text-xs font-semibold bg-brand-primary text-white hover:bg-brand-secondary transition-all flex items-center space-x-1.5 shadow-md shadow-brand-primary/10"
          >
            <Printer class="w-4 h-4" />
            <span>Print Certificate</span>
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<style>
/* Print Layout styling overrides */
@media print {
  body * {
    visibility: hidden;
  }
  
  .fixed.inset-0, .fixed.inset-0 * {
    visibility: visible;
  }
  
  .fixed.inset-0 {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: auto;
    background: white !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  .bg-brand-card {
    background: white !important;
    border: none !important;
    box-shadow: none !important;
  }
  
  .border-double {
    border-color: #d97706 !important; /* solid color gold */
  }

  .text-white {
    color: #111827 !important;
  }
  
  .text-brand-warning {
    color: #b45309 !important;
  }

  .text-brand-accent {
    color: #047857 !important;
  }

  .text-gray-400, .text-gray-500 {
    color: #4b5563 !important;
  }

  .print\:hidden {
    display: none !important;
  }
}
</style>
