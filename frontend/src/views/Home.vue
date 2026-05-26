<script setup>
import { ref, computed } from 'vue';
import { useCoursesStore } from '../store/courses';
import { useAuthStore } from '../store/auth';
import CourseCard from '../components/CourseCard.vue';
import { 
  Search, GraduationCap, Users, ShieldAlert, Award, Star, Compass, 
  Layers, CheckCircle, ArrowRight, ShieldCheck, PlayCircle, BookOpen,
  ArrowDownCircle, Sparkles
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();

const searchQuery = ref('');
const selectedCategory = ref('All');

// List of available categories
const categories = ['All', 'Development', 'Backend', 'Design'];

// Only display approved courses
const approvedCourses = computed(() => coursesStore.approvedCourses);

// Filtered approved courses list
const filteredCourses = computed(() => {
  return approvedCourses.value.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                          course.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          course.teacherName.toLowerCase().includes(searchQuery.value.toLowerCase());
    
    const matchesCategory = selectedCategory.value === 'All' || course.category === selectedCategory.value;
    
    return matchesSearch && matchesCategory;
  });
});

// Interactive feature tab selection for showcase
const activeFeatureTab = ref('student');
</script>

<template>
  <div class="space-y-24 py-6">
    <!-- Hero Banner Section -->
    <section class="relative rounded-3xl overflow-hidden glass-panel p-8 md:p-20 border border-white/5 shadow-2xl flex flex-col items-center text-center space-y-8 bg-gradient-to-br from-brand-card/90 to-brand-dark/40">
      <!-- Glow Background elements -->
      <div class="absolute -top-12 -right-12 w-80 h-80 bg-brand-primary/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -bottom-12 -left-12 w-80 h-80 bg-brand-accent/5 rounded-full blur-3xl pointer-events-none"></div>
      
      <span class="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full text-xs font-bold tracking-wider uppercase bg-brand-primary/10 text-brand-primary border border-brand-primary/20 animate-pulse">
        <Sparkles class="w-3.5 h-3.5" />
        <span>Aether premium learning ecosystem</span>
      </span>

      <h1 class="text-4xl md:text-7xl font-extrabold tracking-tight text-white max-w-4xl leading-tight font-display">
        The Future of <br class="hidden sm:inline"/>
        <span class="bg-clip-text text-transparent bg-gradient-to-r from-brand-primary via-indigo-400 to-brand-accent">
          Self-Paced Digital Education
        </span>
      </h1>

      <p class="text-sm md:text-lg text-gray-400 max-w-3xl leading-relaxed font-light">
        Aether seamlessly bridges students, elite educators, and administrative moderators in a single, high-fidelity environment. Track courses, complete lessons, earn verified credentials, and shape modern syllabus modules in real-time.
      </p>

      <!-- Main Action triggers -->
      <div class="flex flex-col sm:flex-row gap-4 pt-4 w-full sm:w-auto">
        <a 
          href="#catalog-view"
          class="bg-brand-primary hover:bg-brand-secondary text-white font-bold px-8 py-4 rounded-2xl shadow-lg shadow-brand-primary/25 transition-all glow-btn text-center text-sm flex items-center justify-center space-x-2"
        >
          <span>Explore Course Catalog</span>
          <ArrowDownCircle class="w-4.5 h-4.5" />
        </a>
        <router-link 
          v-if="!authStore.isAuthenticated"
          to="/register" 
          class="bg-white/5 hover:bg-white/10 text-white font-semibold px-8 py-4 rounded-2xl border border-white/10 transition-colors text-center text-sm"
        >
          Create Free Account
        </router-link>
        <router-link 
          v-else
          :to="authStore.isStudent ? '/student/dashboard' : authStore.isTeacher ? '/teacher/dashboard' : '/admin/dashboard'"
          class="bg-brand-accent/20 border border-brand-accent/30 text-brand-accent font-semibold px-8 py-4 rounded-2xl transition-all text-center text-sm hover:bg-brand-accent/30"
        >
          Access My Portal Dashboard
        </router-link>
      </div>

      <!-- Quick Platform Counters -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 pt-16 border-t border-white/5 w-full max-w-4xl text-left">
        <div class="space-y-1">
          <div class="flex items-center space-x-2">
            <Users class="w-4.5 h-4.5 text-brand-primary" />
            <span class="text-2xl md:text-3xl font-extrabold text-white">1,500+</span>
          </div>
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Active Learners</p>
        </div>
        
        <div class="space-y-1">
          <div class="flex items-center space-x-2">
            <GraduationCap class="w-4.5 h-4.5 text-brand-accent" />
            <span class="text-2xl md:text-3xl font-extrabold text-white">15+</span>
          </div>
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Elite Educators</p>
        </div>

        <div class="space-y-1">
          <div class="flex items-center space-x-2">
            <Award class="w-4.5 h-4.5 text-brand-warning" />
            <span class="text-2xl md:text-3xl font-extrabold text-white">100%</span>
          </div>
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Success Rate</p>
        </div>

        <div class="space-y-1">
          <div class="flex items-center space-x-2">
            <Star class="w-4.5 h-4.5 text-brand-primary animate-pulse" />
            <span class="text-2xl md:text-3xl font-extrabold text-white">4.9★</span>
          </div>
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Satisfaction Score</p>
        </div>
      </div>
    </section>

    <!-- Platform Pathways Showcase Section -->
    <section class="space-y-12">
      <div class="text-center space-y-3">
        <span class="text-brand-primary font-bold text-xs uppercase tracking-widest">Unified Ecosystem Architecture</span>
        <h2 class="text-3xl md:text-5xl font-extrabold text-white font-display">Three Professional Pathways</h2>
        <p class="text-sm text-gray-400 max-w-2xl mx-auto">Explore how Aether empowers students, instructors, and administrators with specialized high-fidelity workflows.</p>
      </div>

      <!-- Path Selection Buttons -->
      <div class="flex justify-center p-1.5 bg-brand-card/50 border border-white/5 rounded-2xl max-w-lg mx-auto">
        <button 
          @click="activeFeatureTab = 'student'"
          class="flex-1 py-3 text-xs font-bold rounded-xl transition-all flex items-center justify-center space-x-2 cursor-pointer"
          :class="activeFeatureTab === 'student' ? 'bg-brand-primary text-white shadow-lg shadow-brand-primary/10' : 'text-gray-450 hover:text-white'"
        >
          <GraduationCap class="w-4.5 h-4.5" />
          <span>Students</span>
        </button>
        <button 
          @click="activeFeatureTab = 'teacher'"
          class="flex-1 py-3 text-xs font-bold rounded-xl transition-all flex items-center justify-center space-x-2 cursor-pointer"
          :class="activeFeatureTab === 'teacher' ? 'bg-brand-accent text-white shadow-lg shadow-brand-accent/10' : 'text-gray-450 hover:text-white'"
        >
          <Users class="w-4.5 h-4.5" />
          <span>Teachers</span>
        </button>
        <button 
          @click="activeFeatureTab = 'admin'"
          class="flex-1 py-3 text-xs font-bold rounded-xl transition-all flex items-center justify-center space-x-2 cursor-pointer"
          :class="activeFeatureTab === 'admin' ? 'bg-brand-warning text-white shadow-lg shadow-brand-warning/10' : 'text-gray-450 hover:text-white'"
        >
          <ShieldCheck class="w-4.5 h-4.5" />
          <span>Admins</span>
        </button>
      </div>

      <!-- Path Details Content Block -->
      <div class="glass-panel rounded-3xl p-8 md:p-12 border border-white/5 bg-brand-card shadow-2xl">
        <!-- Student Tab -->
        <div v-if="activeFeatureTab === 'student'" class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center animate-fade-in">
          <div class="space-y-6">
            <div class="p-3 bg-brand-primary/10 border border-brand-primary/20 text-brand-primary rounded-2xl w-fit">
              <GraduationCap class="w-8 h-8" />
            </div>
            <h3 class="text-2xl md:text-3xl font-bold text-white font-display">Expand Skills at Your Own Pace</h3>
            <p class="text-sm text-gray-400 leading-relaxed font-light">
              As a student, Aether offers you a premium interactive syllabus dashboard. Select from approved programs, enroll in one click, and track your lesson checklists. Toggle video or PDF resources seamlessly, bookmark favorite courses, and download a verifiable certificate once you complete 100% of the syllabus.
            </p>
            <ul class="space-y-3.5 text-xs text-gray-300">
              <li class="flex items-center space-x-2.5">
                <CheckCircle class="w-4.5 h-4.5 text-brand-accent shrink-0" />
                <span>Seamless self-paced lecture tracking.</span>
              </li>
              <li class="flex items-center space-x-2.5">
                <CheckCircle class="w-4.5 h-4.5 text-brand-accent shrink-0" />
                <span>Instant academic achievement and milestone alerts.</span>
              </li>
              <li class="flex items-center space-x-2.5">
                <CheckCircle class="w-4.5 h-4.5 text-brand-accent shrink-0" />
                <span>Downloadable student certificates signed by instructors.</span>
              </li>
            </ul>
          </div>
          <div class="bg-brand-dark/40 rounded-2xl p-6 border border-white/5 relative overflow-hidden group shadow-inner">
            <div class="absolute inset-0 bg-gradient-to-tr from-brand-primary/5 to-transparent pointer-events-none"></div>
            <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Student UI Preview</h4>
            <div class="space-y-4">
              <div class="p-4 bg-brand-card rounded-xl border border-white/5 flex justify-between items-center">
                <div class="flex items-center space-x-3">
                  <PlayCircle class="w-8 h-8 text-brand-primary" />
                  <div>
                    <p class="text-xs font-bold text-white">Mastering Vue 3: Core Concepts</p>
                    <p class="text-[10px] text-gray-450">Dr. Sarah Jenkins</p>
                  </div>
                </div>
                <span class="text-xs font-extrabold text-brand-accent">25% Done</span>
              </div>
              <div class="p-4 bg-brand-card rounded-xl border border-white/5 space-y-2">
                <div class="flex justify-between items-center">
                  <span class="text-[10px] font-bold text-white uppercase tracking-wider">Lesson Checklist</span>
                  <span class="text-[9px] text-gray-500 font-medium">1 of 4 Completed</span>
                </div>
                <div class="space-y-1.5 text-xs">
                  <div class="flex items-center space-x-2 text-brand-accent">
                    <CheckCircle class="w-4 h-4 shrink-0" />
                    <span class="line-through font-light">1. Welcoming & App scaffolding</span>
                  </div>
                  <div class="flex items-center space-x-2 text-gray-300">
                    <div class="w-4 h-4 rounded border border-white/10 shrink-0"></div>
                    <span>2. Setting up custom styling sheets</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Teacher Tab -->
        <div v-if="activeFeatureTab === 'teacher'" class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center animate-fade-in">
          <div class="space-y-6">
            <div class="p-3 bg-brand-accent/10 border border-brand-accent/20 text-brand-accent rounded-2xl w-fit">
              <Users class="w-8 h-8" />
            </div>
            <h3 class="text-2xl md:text-3xl font-bold text-white font-display">Create Syllabus & Track Students</h3>
            <p class="text-sm text-gray-400 leading-relaxed font-light">
              Educators hold administrative capabilities to build rich interactive course modules. The step-by-step Course Creator wizard makes it simple to add lectures, assign resource attachments, and write curriculum agendas. Teachers also access a comprehensive gradebook, monitoring student progress and completion milestones.
            </p>
            <ul class="space-y-3.5 text-xs text-gray-300">
              <li class="flex items-center space-x-2.5">
                <CheckCircle class="w-4.5 h-4.5 text-brand-accent shrink-0" />
                <span>Interactive draft-based course metadata creation.</span>
              </li>
              <li class="flex items-center space-x-2.5">
                <CheckCircle class="w-4.5 h-4.5 text-brand-accent shrink-0" />
                <span>Dynamic syllabus modules & video/PDF material uploads.</span>
              </li>
              <li class="flex items-center space-x-2.5">
                <CheckCircle class="w-4.5 h-4.5 text-brand-accent shrink-0" />
                <span>Full Gradebook tracking student emails, metrics, & dates.</span>
              </li>
            </ul>
          </div>
          <div class="bg-brand-dark/40 rounded-2xl p-6 border border-white/5 relative overflow-hidden group shadow-inner">
            <div class="absolute inset-0 bg-gradient-to-tr from-brand-accent/5 to-transparent pointer-events-none"></div>
            <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Instructor Dashboard Preview</h4>
            <div class="space-y-4">
              <div class="p-4 bg-brand-card rounded-xl border border-white/5 space-y-3">
                <div class="flex justify-between items-center">
                  <span class="text-[10px] font-bold text-white uppercase tracking-wider">Add Lecture Item</span>
                  <span class="px-2 py-0.5 bg-brand-accent/15 text-brand-accent text-[8px] font-bold rounded">Video</span>
                </div>
                <div class="space-y-2">
                  <input type="text" value="3. Managing Vue Reactivity ref()" disabled class="w-full bg-brand-dark/40 border border-white/5 text-[11px] p-2 rounded-lg text-white" />
                  <input type="text" value="Duration: 18:42" disabled class="w-full bg-brand-dark/40 border border-white/5 text-[11px] p-2 rounded-lg text-gray-400" />
                </div>
              </div>
              <div class="p-4 bg-brand-card rounded-xl border border-white/5">
                <div class="flex items-center justify-between text-xs">
                  <div>
                    <p class="font-bold text-white">Student Enrollment Tracker</p>
                    <p class="text-[9px] text-gray-400">Priyanshi Sharma &bull; priyanshi@aether.edu</p>
                  </div>
                  <span class="px-2 py-1 bg-brand-primary/10 border border-brand-primary/20 text-brand-primary text-[10px] font-bold rounded-lg">95% complete</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Admin Tab -->
        <div v-if="activeFeatureTab === 'admin'" class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center animate-fade-in">
          <div class="space-y-6">
            <div class="p-3 bg-brand-warning/10 border border-brand-warning/20 text-brand-warning rounded-2xl w-fit">
              <ShieldCheck class="w-8 h-8" />
            </div>
            <h3 class="text-2xl md:text-3xl font-bold text-white font-display">System Administration & Moderation</h3>
            <p class="text-sm text-gray-400 leading-relaxed font-light">
              Platform administration controls allow full management of the platform registry. Admins review and moderate new course drafts, reading modules, and syllabus structures. Approve verified proposals to make them active in the catalog, or return them with corrective feedback. Safely manage active user directories, toggle account suspension flags, or remove records.
            </p>
            <ul class="space-y-3.5 text-xs text-gray-300">
              <li class="flex items-center space-x-2.5">
                <CheckCircle class="w-4.5 h-4.5 text-brand-accent shrink-0" />
                <span>Interactive draft moderation and syllabus inspection workflow.</span>
              </li>
              <li class="flex items-center space-x-2.5">
                <CheckCircle class="w-4.5 h-4.5 text-brand-accent shrink-0" />
                <span>Platform directory auditing & suspension lock safeguards.</span>
              </li>
              <li class="flex items-center space-x-2.5">
                <CheckCircle class="w-4.5 h-4.5 text-brand-accent shrink-0" />
                <span>Aggregated metrics mapping popular courses & topics.</span>
              </li>
            </ul>
          </div>
          <div class="bg-brand-dark/40 rounded-2xl p-6 border border-white/5 relative overflow-hidden group shadow-inner">
            <div class="absolute inset-0 bg-gradient-to-tr from-brand-warning/5 to-transparent pointer-events-none"></div>
            <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Admin Moderation Workspace</h4>
            <div class="space-y-4">
              <div class="p-4 bg-brand-card rounded-xl border border-white/5 space-y-3">
                <div class="flex items-center justify-between">
                  <p class="text-xs font-bold text-white">Full-Stack FastAPI Backend</p>
                  <span class="px-2 py-0.5 bg-brand-warning/15 text-brand-warning text-[8px] font-bold rounded">Pending Review</span>
                </div>
                <p class="text-[10px] text-gray-400 line-clamp-1">Deep dive into python asynchronous API models...</p>
                <div class="flex gap-2">
                  <button class="flex-1 py-1.5 bg-brand-accent text-white text-[10px] font-bold rounded-lg cursor-default">Approve</button>
                  <button class="flex-1 py-1.5 bg-brand-danger/10 border border-brand-danger/20 text-brand-danger text-[10px] font-bold rounded-lg cursor-default">Return Draft</button>
                </div>
              </div>
              <div class="p-4 bg-brand-card rounded-xl border border-white/5 flex items-center justify-between text-xs">
                <div class="flex items-center space-x-2.5">
                  <div class="w-7 h-7 rounded-full bg-brand-danger/10 text-brand-danger flex items-center justify-center font-bold text-[10px]">JM</div>
                  <div>
                    <p class="font-bold text-white">John Miller</p>
                    <p class="text-[8px] text-gray-400">john@aether.edu</p>
                  </div>
                </div>
                <span class="px-2 py-0.5 bg-brand-danger/10 text-brand-danger border border-brand-danger/20 text-[8px] font-extrabold uppercase rounded">Suspended</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Course Catalog Section -->
    <section id="catalog-view" class="space-y-8 scroll-mt-24">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div class="space-y-2 text-left">
          <div class="flex items-center space-x-2">
            <Compass class="w-5.5 h-5.5 text-brand-primary" />
            <h2 class="text-2xl md:text-4xl font-extrabold text-white font-display">Browse Course Catalog</h2>
          </div>
          <p class="text-xs md:text-sm text-gray-400 max-w-md">
            Learn trending technologies and styling skills curated by leading educators. Only admin-approved courses appear here.
          </p>
        </div>

        <!-- Search Bar and filters -->
        <div class="flex flex-col sm:flex-row items-center gap-3 shrink-0 w-full md:w-auto">
          <!-- Search -->
          <div class="relative w-full sm:w-72">
            <Search class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4.5 h-4.5 text-gray-400" />
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search courses, mentors..." 
              class="w-full pl-10 pr-4 py-2.5 bg-brand-card/60 hover:bg-brand-card border border-white/10 rounded-xl text-xs text-white focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
            />
          </div>
        </div>
      </div>

      <!-- Categories Tabs Slider -->
      <div class="flex items-center space-x-2 overflow-x-auto pb-2 scrollbar-none border-b border-white/5">
        <button 
          v-for="cat in categories" 
          :key="cat"
          @click="selectedCategory = cat"
          class="px-4.5 py-2.5 rounded-xl text-xs font-bold whitespace-nowrap transition-all cursor-pointer"
          :class="selectedCategory === cat 
            ? 'bg-brand-primary text-white shadow-md shadow-brand-primary/10' 
            : 'bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white'"
        >
          {{ cat }}
        </button>
      </div>

      <!-- Catalog grid container -->
      <div v-if="filteredCourses.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <div 
          v-for="(course, idx) in filteredCourses" 
          :key="course.id"
          class="animate-fade-in"
          :style="{ 'animation-delay': `${idx * 0.05}s` }"
        >
          <CourseCard :course="course" />
        </div>
      </div>

      <!-- Fallback empty search state -->
      <div 
        v-else 
        class="glass-panel rounded-2xl p-12 text-center border border-white/5 flex flex-col items-center justify-center space-y-4 max-w-xl mx-auto"
      >
        <div class="p-4 rounded-full bg-brand-warning/10 text-brand-warning border border-brand-warning/20">
          <ShieldAlert class="w-8 h-8" />
        </div>
        <h3 class="text-lg font-bold text-white">No Programs Found</h3>
        <p class="text-xs text-gray-450 leading-relaxed">
          We couldn't locate any approved programs matching "{{ searchQuery }}" in category "{{ selectedCategory }}". Try refining your search keywords or choosing another category block.
        </p>
        <button 
          @click="searchQuery = ''; selectedCategory = 'All';" 
          class="bg-white/5 hover:bg-white/10 border border-white/10 text-white text-xs font-semibold px-4.5 py-2 rounded-xl transition-all cursor-pointer"
        >
          Reset Filters
        </button>
      </div>
    </section>

    <!-- Testimonials or Philosophy section -->
    <section class="glass-panel rounded-3xl p-8 md:p-16 border border-white/5 bg-brand-dark/25 relative overflow-hidden flex flex-col md:flex-row items-center gap-12">
      <div class="absolute inset-0 bg-gradient-to-tr from-brand-primary/5 to-transparent pointer-events-none"></div>
      <div class="flex-grow space-y-4 text-left max-w-xl">
        <h3 class="text-2xl md:text-3xl font-extrabold text-white font-display">A Philosophy of Uncompromising Quality</h3>
        <p class="text-xs md:text-sm text-gray-400 leading-relaxed font-light">
          Aether E-learning was created with one simple conviction: that online education should feel responsive, rich, and alive. Through gorgeous, interactive glassmorphism components, dynamic visual feedback, and reliable file-based databases, we provide an academic sandbox that is both incredibly secure and visually engaging. 
        </p>
        <router-link 
          to="/register" 
          class="inline-flex items-center space-x-1.5 text-xs font-bold text-brand-primary hover:text-brand-secondary transition-colors"
        >
          <span>Become part of our global academy</span>
          <ArrowRight class="w-4 h-4" />
        </router-link>
      </div>
      <div class="shrink-0 w-full md:w-80 space-y-4">
        <!-- Testimonial card -->
        <div class="p-5 bg-brand-card border border-white/5 rounded-2xl text-left space-y-3.5 shadow-xl">
          <div class="flex items-center space-x-1 text-brand-warning">
            <Star class="w-3.5 h-3.5 fill-current" v-for="n in 5" :key="n" />
          </div>
          <p class="text-[11px] text-gray-300 italic font-light">"The ref() and computed() module tracking makes reactive progress feel like a game. The certificates look incredibly sleek too!"</p>
          <div class="flex items-center space-x-2.5">
            <div class="w-7 h-7 rounded-full bg-brand-primary flex items-center justify-center font-bold text-white text-[10px]">PS</div>
            <div>
              <p class="text-[10px] font-bold text-white">Priyanshi Sharma</p>
              <p class="text-[8px] text-gray-500 font-semibold">Web Development Student</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
