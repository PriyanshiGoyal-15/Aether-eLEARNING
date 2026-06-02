<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useCoursesStore } from '../store/courses';
import { useAuthStore } from '../store/auth';
import CourseCard from '../components/CourseCard.vue';
import { 
  Search, GraduationCap, Users, ShieldAlert, Award, Star, Compass, 
  Layers, CheckCircle, ArrowRight, ShieldCheck, PlayCircle, BookOpen,
  ArrowDownCircle, Sparkles, X, ChevronDown, ChevronUp, Trophy, 
  Shield, Mail, Cpu, Palette, Monitor, RefreshCw, Lock
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const router = useRouter();
const isCoursesExpanded = ref(false);
const mobileMenuOpen = ref(false);

const searchQuery = ref('');
const selectedCategory = ref('All');

// Pathfinder wizard state
const pathfinderStep = ref(1);
const selectedGoal = ref('');
const selectedExp = ref('');

const resetPathfinder = () => {
  pathfinderStep.value = 1;
  selectedGoal.value = '';
  selectedExp.value = '';
};

const handleSelectGoal = (goal) => {
  selectedGoal.value = goal;
  pathfinderStep.value = 2;
};

const handleSelectExp = (exp) => {
  selectedExp.value = exp;
  pathfinderStep.value = 3;
};

const recommendedCategory = computed(() => {
  if (selectedGoal.value === 'frontend') return 'Development';
  if (selectedGoal.value === 'backend') return 'Backend';
  if (selectedGoal.value === 'design') return 'Design';
  return 'All';
});

const applyPathfinderResult = () => {
  selectedCategory.value = recommendedCategory.value;
  const catalogEl = document.getElementById('catalog-view');
  if (catalogEl) {
    catalogEl.scrollIntoView({ behavior: 'smooth' });
  }
  setTimeout(() => {
    resetPathfinder();
  }, 1000);
};

// FAQ accordion
const activeFaq = ref(null);

// Newsletter state
const newsletterEmail = ref('');
const newsletterSuccessMsg = ref('');

// Categories
const categories = ['All', 'Development', 'Backend', 'Design'];

const approvedCourses = computed(() => coursesStore.approvedCourses);

const filteredCourses = computed(() => {
  return approvedCourses.value.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                          course.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          course.teacherName.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesCategory = selectedCategory.value === 'All' || course.category === selectedCategory.value;
    return matchesSearch && matchesCategory;
  });
});

const visibleCourses = computed(() => {
  if (isCoursesExpanded.value && authStore.isAuthenticated) {
    return filteredCourses.value;
  }
  return filteredCourses.value.slice(0, 6);
});

const handleViewMoreCourses = () => {
  if (authStore.isAuthenticated) {
    isCoursesExpanded.value = !isCoursesExpanded.value;
  } else {
    router.push({ path: '/login', query: { redirect: '/' } });
  }
};

const toggleFaq = (index) => {
  activeFaq.value = activeFaq.value === index ? null : index;
};

const handleSubscribe = () => {
  if (!newsletterEmail.value.trim()) return;
  newsletterSuccessMsg.value = "You're subscribed! Welcome to the Aether community.";
  newsletterEmail.value = '';
  setTimeout(() => {
    newsletterSuccessMsg.value = '';
  }, 4000);
};

// Unified Guided Product Tour State (Option A)
const tourStep = ref(1);

// Stage 1 (Curate) State
const mockModules = ref(['Syllabus Intro', 'REST Endpoints Map', 'Auth Access Checks']);
const newModuleTitle = ref('');
const addMockModule = () => {
  if (newModuleTitle.value.trim()) {
    mockModules.value.push(newModuleTitle.value.trim());
    newModuleTitle.value = '';
  } else {
    mockModules.value.push('Module ' + (mockModules.value.length + 1) + ': API Handlers');
  }
};

// Stage 2 (Restrict) State
const lockPopupOpen = ref(false);

// Stage 3 (Learn) State
const mockChecklist = ref([
  { text: 'Analyze course outlines', done: true },
  { text: 'Mount sandbox compiler rig', done: true },
  { text: 'Register API Access Guards', done: false }
]);
const toggleMockCheck = (idx) => {
  mockChecklist.value[idx].done = !mockChecklist.value[idx].done;
};
const mockNoteText = ref('Aether Sandbox triggers Hot Module Reloading for instant code changes, while FastAPI handles robust session routing.');

// Stage 4 (Review) State
const activeRating = ref(5);
const feedbackComment = ref('');
const feedbackSubmitted = ref(false);
const seedReviews = ref([
  { name: 'Priyansh G.', rating: 5, comment: 'Incredibly smooth! The auto-saving notepad and stream checkpoint elements work cleanly.' }
]);
const submitMockReview = () => {
  seedReviews.value.unshift({
    name: 'Explorer Beta',
    rating: activeRating.value,
    comment: feedbackComment.value.trim() || 'Awesome operational flow simulation. Complete layout compiles perfectly!'
  });
  feedbackComment.value = '';
  feedbackSubmitted.value = true;
  setTimeout(() => {
    feedbackSubmitted.value = false;
  }, 2500);
};

// Stage 5 (Verify) State
const generatingCert = ref(false);
const certMinted = ref(false);
const mintCertHash = () => {
  generatingCert.value = true;
  setTimeout(() => {
    generatingCert.value = false;
    certMinted.value = true;
  }, 1200);
};

// Developer IDE Sandbox Simulation State
const sandboxTab = ref('backend');
const isCompiling = ref(false);
const sandboxLogs = ref([]);

const runCompileSimulation = () => {
  if (isCompiling.value) return;
  isCompiling.value = true;
  sandboxLogs.value = [];
  
  const steps = sandboxTab.value === 'backend' ? [
    { text: '⚡ Bootstrapping Uvicorn backend worker...', delay: 100 },
    { text: '📡 Loading FastAPI modules & seeding MongoDB catalogs...', delay: 350 },
    { text: '🔒 CourseAccessGuard initialized: Scanning token permissions...', delay: 600 },
    { text: '🔒 Guard: Blocked playback stream for un-enrolled tokens', delay: 850 },
    { text: '🚀 Uvicorn mapping active at http://localhost:8000', delay: 1100 },
    { text: '✓ Compile completed in 294ms. Server is operational.', delay: 1350 }
  ] : [
    { text: '⚡ Mounting client-side Vite asset compiler...', delay: 100 },
    { text: '📦 Bundling dynamic glassmorphic styles & reactive components...', delay: 350 },
    { text: '🎨 Hot Module Replacement ws client bound at port 5173', delay: 600 },
    { text: '🚀 Local Dev Server ready at http://localhost:5173/', delay: 900 },
    { text: '✓ Bundles linked successfully. Hot reload listening...', delay: 1150 }
  ];

  steps.forEach(step => {
    setTimeout(() => {
      sandboxLogs.value.push(step.text);
      if (step.text.startsWith('✓')) {
        isCompiling.value = false;
      }
    }, step.delay);
  });
};

// Simple visual navigation jumps
const jumpToTourStep = (step) => {
  tourStep.value = step;
  const tourEl = document.getElementById('platform-tour');
  if (tourEl) {
    tourEl.scrollIntoView({ behavior: 'smooth' });
  }
};
</script>

<template>
  <div class="min-h-screen bg-brand-dark text-brand-light selection:bg-indigo-500/30 selection:text-indigo-200 overflow-x-hidden font-sans relative">
    
    <!-- Clean, Unified Gradient Accent Lights -->
    <div class="absolute top-[-10rem] left-[10rem] w-[50rem] h-[50rem] rounded-full bg-indigo-600/5 blur-[200px] pointer-events-none"></div>
    <div class="absolute top-[35rem] right-[-10rem] w-[40rem] h-[40rem] rounded-full bg-emerald-600/5 blur-[180px] pointer-events-none"></div>
    <div class="absolute bottom-[20rem] left-[-20rem] w-[55rem] h-[55rem] rounded-full bg-purple-600/5 blur-[220px] pointer-events-none"></div>

    <!-- Radial Mesh Dot Overlay -->
    <div class="absolute inset-0 grid-bg opacity-[0.15] pointer-events-none"></div>



    <!-- Main Entry Context -->
    <main class="pt-28 pb-20 relative z-10">
      <div class="max-w-7xl mx-auto px-6">
        
        <!-- Hero Section: Obsidian Headline & Pulsing Blueprint Interconnect Map -->
        <section class="grid lg:grid-cols-12 gap-12 items-center py-6 md:py-16">
          
          <!-- Headline Panel -->
          <div class="lg:col-span-5 text-left space-y-6">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 hover:bg-indigo-500/15 transition-all">
              <Sparkles class="w-3 h-3 text-indigo-400" />
              <span class="text-[9px] font-bold tracking-widest text-indigo-400 uppercase font-mono">Product Architecture Release</span>
            </div>
            
            <h1 class="text-4xl md:text-5xl lg:text-6xl font-black tracking-tight leading-[1.02] text-white">
              The Real Product
              <span class="bg-gradient-to-r from-indigo-400 via-purple-400 to-emerald-400 bg-clip-text text-transparent block">
                E-Learning Engine
              </span>
            </h1>
            
            <p class="text-xs md:text-sm text-gray-400 leading-relaxed max-w-lg ">
              Aether integrates students, expert educators, and administrators into one unified operational workspace. Experience live video checkpoints, interactive note-taking utilities, course curation centers, and database sandbox compilers.
            </p>

            <div class="flex items-center gap-4 pt-2">
              <a 
                href="#platform-tour" 
                class="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-bold text-xs transition-all shadow-lg shadow-indigo-600/20 flex items-center gap-2"
              >
                Launch Guided Tour
                <ArrowRight class="w-3.5 h-3.5" />
              </a>
              
              <a 
                href="#catalog-view"
                class="px-6 py-3 bg-white/5 hover:bg-white/10 rounded-lg font-bold text-xs transition-all border border-white/10"
              >
                Browse Syllabus Deck
              </a>
            </div>

            <!-- Sleek Metrics -->
            <div class="grid grid-cols-3 gap-6 pt-6 border-t border-white/5 text-left">
              <div>
                <p class="text-xl font-extrabold text-white font-mono">3 Roles</p>
                <p class="text-[9px] text-gray-500 uppercase tracking-widest font-bold font-mono">Sync Telemetry</p>
              </div>
              <div>
                <p class="text-xl font-extrabold text-emerald-400 font-mono">70% Split</p>
                <p class="text-[9px] text-gray-500 uppercase tracking-widest font-bold font-mono">Mentor Royalty</p>
              </div>
              <div>
                <p class="text-xl font-extrabold text-indigo-400 font-mono">Active</p>
                <p class="text-[9px] text-gray-500 uppercase tracking-widest font-bold font-mono">Compiler Sandbox</p>
              </div>
            </div>
          </div>

          <!-- Pulsing System Blueprint map -->
          <div class="lg:col-span-7 relative">
            <div class="absolute -inset-1 bg-gradient-to-r from-indigo-500/20 via-purple-500/10 to-emerald-500/20 rounded-2xl blur-xl opacity-20"></div>
            <div class="relative bg-brand-card border border-brand-border rounded-2xl p-6 md:p-8 flex flex-col justify-between min-h-[500px]">
              
              <!-- Blueprint Title -->
              <div class="flex items-center justify-between pb-4 border-b border-brand-border">
                <div class="flex items-center gap-2">
                  <div class="w-2 h-2 rounded-full bg-indigo-500 animate-ping"></div>
                  <span class="text-[10px] font-mono font-bold text-brand-sub">AETHER SYSTEM BLUEPRINT OVERLAY</span>
                </div>
                <span class="text-[8px] font-mono text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20 uppercase">Interactive System Map</span>
              </div>

              <!-- Animated SVG Pipelines connecting actors -->
              <div class="relative my-8 flex-1 min-h-[380px] flex items-center justify-center">
                
                <!-- SVG Pipeline Cables -->
                <svg class="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 600 380" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <!-- Cable 1: Educator to Access Guard -->
                  <path d="M120 70 Q 280 40 300 185" stroke="rgba(99, 102, 241, 0.2)" stroke-width="1.5" stroke-dasharray="4 4" />
                  <path d="M120 70 Q 280 40 300 185" stroke="#6366f1" stroke-width="1.5" stroke-dasharray="10 150" stroke-linecap="round">
                    <animate attributeName="stroke-dashoffset" values="300;0" dur="4s" repeatCount="indefinite" />
                  </path>

                  <!-- Cable 2: Access Guard to Student -->
                  <path d="M300 185 Q 320 310 480 315" stroke="rgba(16, 185, 129, 0.2)" stroke-width="1.5" stroke-dasharray="4 4" />
                  <path d="M300 185 Q 320 310 480 315" stroke="#10b981" stroke-width="1.5" stroke-dasharray="10 150" stroke-linecap="round">
                    <animate attributeName="stroke-dashoffset" values="300;0" dur="4s" repeatCount="indefinite" />
                  </path>

                  <!-- Cable 3: Student to Review Loop -->
                  <path d="M480 315 Q 520 190 480 70" stroke="rgba(168, 85, 247, 0.2)" stroke-width="1.5" stroke-dasharray="4 4" />
                  <path d="M480 315 Q 520 190 480 70" stroke="#a855f7" stroke-width="1.5" stroke-dasharray="10 150" stroke-linecap="round">
                    <animate attributeName="stroke-dashoffset" values="300;0" dur="4s" repeatCount="indefinite" />
                  </path>

                  <!-- Cable 4: Review Loop to Diploma -->
                  <path d="M480 70 Q 300 190 120 315" stroke="rgba(99, 102, 241, 0.2)" stroke-width="1.5" stroke-dasharray="4 4" />
                  <path d="M480 70 Q 300 190 120 315" stroke="#6366f1" stroke-width="1.5" stroke-dasharray="10 150" stroke-linecap="round">
                    <animate attributeName="stroke-dashoffset" values="300;0" dur="4s" repeatCount="indefinite" />
                  </path>

                  <!-- Cable 5: Diploma to Educator -->
                  <path d="M120 315 Q 80 190 120 70" stroke="rgba(16, 185, 129, 0.2)" stroke-width="1.5" stroke-dasharray="4 4" />
                  <path d="M120 315 Q 80 190 120 70" stroke="#10b981" stroke-width="1.5" stroke-dasharray="10 150" stroke-linecap="round">
                    <animate attributeName="stroke-dashoffset" values="300;0" dur="4s" repeatCount="indefinite" />
                  </path>
                </svg>

                <!-- Interactive Blueprint Nodes -->
                <!-- Node 1: Educator -->
                <div class="absolute top-[20px] left-[20px] z-10">
                  <button 
                    @click="jumpToTourStep(1)"
                    class="bg-brand-dark border border-indigo-500/20 hover:border-indigo-500 rounded-xl p-3.5 text-left w-44 transition-all hover:scale-102 hover:shadow-lg hover:shadow-indigo-500/5 group"
                  >
                    <div class="flex items-center gap-2 mb-1.5">
                      <Users class="w-4 h-4 text-indigo-400" />
                      <span class="text-[10px] font-bold tracking-wider text-brand-light">1. EDUCATOR</span>
                    </div>
                    <p class="text-[9px] text-brand-muted leading-normal">Teacher drafts syllabus, sets ₹ price tag splits.</p>
                  </button>
                </div>

                <!-- Node 2: Access Guard -->
                <div class="absolute top-[130px] left-[210px] z-10">
                  <button 
                    @click="jumpToTourStep(2)"
                    class="bg-brand-dark border border-emerald-500/20 hover:border-emerald-500 rounded-xl p-3.5 text-left w-48 transition-all hover:scale-102 hover:shadow-lg hover:shadow-emerald-500/5 group"
                  >
                    <div class="flex items-center gap-2 mb-1.5">
                      <ShieldCheck class="w-4 h-4 text-emerald-400 animate-pulse" />
                      <span class="text-[10px] font-bold tracking-wider text-brand-light">2. ACCESS GUARD</span>
                    </div>
                    <p class="text-[9px] text-brand-muted leading-normal">Database checks enrollment session tokens.</p>
                  </button>
                </div>

                <!-- Node 3: Student -->
                <div class="absolute bottom-[20px] right-[20px] z-10">
                  <button 
                    @click="jumpToTourStep(3)"
                    class="bg-brand-dark border border-indigo-500/20 hover:border-indigo-500 rounded-xl p-3.5 text-left w-44 transition-all hover:scale-102 hover:shadow-lg hover:shadow-indigo-500/5 group"
                  >
                    <div class="flex items-center gap-2 mb-1.5">
                      <GraduationCap class="w-4 h-4 text-indigo-400" />
                      <span class="text-[10px] font-bold tracking-wider text-brand-light">3. STUDENT</span>
                    </div>
                    <p class="text-[9px] text-brand-muted leading-normal">Notebook streams, milestoned streaks.</p>
                  </button>
                </div>

                <!-- Node 4: Review Loop -->
                <div class="absolute top-[20px] right-[20px] z-10">
                  <button 
                    @click="jumpToTourStep(4)"
                    class="bg-brand-dark border border-purple-500/20 hover:border-purple-500 rounded-xl p-3.5 text-left w-44 transition-all hover:scale-102 hover:shadow-lg hover:shadow-purple-500/5 group"
                  >
                    <div class="flex items-center gap-2 mb-1.5">
                      <Star class="w-4 h-4 text-purple-400" />
                      <span class="text-[10px] font-bold tracking-wider text-brand-light">4. REVIEW LOOP</span>
                    </div>
                    <p class="text-[9px] text-brand-muted leading-normal">Submit syllabus ratings inside player console.</p>
                  </button>
                </div>

                <!-- Node 5: Diploma -->
                <div class="absolute bottom-[20px] left-[20px] z-10">
                  <button 
                    @click="jumpToTourStep(5)"
                    class="bg-brand-dark border border-purple-500/20 hover:border-purple-500 rounded-xl p-3.5 text-left w-44 transition-all hover:scale-102 hover:shadow-lg hover:shadow-purple-500/5 group"
                  >
                    <div class="flex items-center gap-2 mb-1.5">
                      <Award class="w-4 h-4 text-purple-400" />
                      <span class="text-[10px] font-bold tracking-wider text-brand-light">5. DIPLOMA</span>
                    </div>
                    <p class="text-[9px] text-brand-muted leading-normal">Presents verified cryptographed seals.</p>
                  </button>
                </div>

              </div>

              <!-- Blueprint Instructions -->
              <p class="text-[10px] font-mono text-brand-muted text-center border-t border-brand-border pt-4">
                ★ Click any active system blueprint node above to jump directly into the Guided Tour.
              </p>

            </div>
          </div>
        </section>

        <!-- Unified Guided Platform Tour Section (Option A: Flow & Mockups Merged) -->
        <section id="platform-tour" class="py-20 border-t border-white/5 relative">
          
          <div class="text-center max-w-2xl mx-auto mb-16 space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20">
              <Compass class="w-3 h-3 text-indigo-400 animate-spin" style="animation-duration: 6s;" />
              <span class="text-[9px] font-bold text-indigo-400 uppercase tracking-widest font-mono">Interactive Platform Tour</span>
            </div>
            <h2 class="text-3xl md:text-4xl font-black tracking-tight text-white">Unified System Operations Tour</h2>
            <p class="text-xs text-indigo-300 bg-indigo-500/5 border border-indigo-500/20 px-4 py-2.5 rounded-xl mt-3 max-w-xl mx-auto animate-pulse font-mono">
              👉 <strong>Interactive System Simulator:</strong> Click any of the 5 stages below to morph the browser window, then type modules, click locks, toggle checkboxes, or rate stars directly on the live screens!
            </p>
          </div>

          <div class="grid lg:grid-cols-12 gap-12 items-start">
            
            <!-- Left: Stepper Navigation -->
            <div class="lg:col-span-5 space-y-3">
              
              <!-- Step 1 Rail -->
              <div 
                @click="tourStep = 1"
                class="p-4 rounded-xl border text-left cursor-pointer transition-all duration-300 relative overflow-hidden"
                :class="tourStep === 1 ? 'bg-indigo-500/10 border-indigo-500/40 shadow-lg shadow-indigo-600/5' : 'bg-brand-card border-white/5 hover:border-white/10'"
              >
                <div class="flex gap-4 items-start">
                  <span class="w-7 h-7 rounded-lg flex items-center justify-center shrink-0 font-mono font-bold text-xs" :class="tourStep === 1 ? 'bg-indigo-600 text-white' : 'bg-white/5 text-gray-500'">
                    01
                  </span>
                  <div class="space-y-0.5">
                    <h3 class="text-xs font-extrabold transition-colors uppercase tracking-wider" :class="tourStep === 1 ? 'text-indigo-400' : 'text-gray-350'">Educator Syllabus Curation</h3>
                    <p class="text-[11px] text-gray-500 leading-normal">Mentors compile curriculum modules, draft quizzes, set prices, and collect a 70% direct royalty payout.</p>
                  </div>
                </div>
              </div>

              <!-- Step 2 Rail -->
              <div 
                @click="tourStep = 2"
                class="p-4 rounded-xl border text-left cursor-pointer transition-all duration-300 relative overflow-hidden"
                :class="tourStep === 2 ? 'bg-indigo-500/10 border-indigo-500/40 shadow-lg shadow-indigo-600/5' : 'bg-brand-card border-white/5 hover:border-white/10'"
              >
                <div class="flex gap-4 items-start">
                  <span class="w-7 h-7 rounded-lg flex items-center justify-center shrink-0 font-mono font-bold text-xs" :class="tourStep === 2 ? 'bg-indigo-600 text-white' : 'bg-white/5 text-gray-500'">
                    02
                  </span>
                  <div class="space-y-0.5">
                    <h3 class="text-xs font-extrabold transition-colors uppercase tracking-wider" :class="tourStep === 2 ? 'text-indigo-400' : 'text-gray-350'">Access Preview Locks</h3>
                    <p class="text-[11px] text-gray-500 leading-normal">Guests can audit the complete syllabus index, but locks restrict playbacks until verified enrollment keys are mapped.</p>
                  </div>
                </div>
              </div>

              <!-- Step 3 Rail -->
              <div 
                @click="tourStep = 3"
                class="p-4 rounded-xl border text-left cursor-pointer transition-all duration-300 relative overflow-hidden"
                :class="tourStep === 3 ? 'bg-indigo-500/10 border-indigo-500/40 shadow-lg shadow-indigo-600/5' : 'bg-brand-card border-white/5 hover:border-white/10'"
              >
                <div class="flex gap-4 items-start">
                  <span class="w-7 h-7 rounded-lg flex items-center justify-center shrink-0 font-mono font-bold text-xs" :class="tourStep === 3 ? 'bg-indigo-600 text-white' : 'bg-white/5 text-gray-500'">
                    03
                  </span>
                  <div class="space-y-0.5">
                    <h3 class="text-xs font-extrabold transition-colors uppercase tracking-wider" :class="tourStep === 3 ? 'text-indigo-400' : 'text-gray-350'">Gamified Study Workspace</h3>
                    <p class="text-[11px] text-gray-500 leading-normal">Students toggle study checkboxes, watch daily streak multipliers increment, and auto-sync study text notebooks.</p>
                  </div>
                </div>
              </div>

              <!-- Step 4 Rail -->
              <div 
                @click="tourStep = 4"
                class="p-4 rounded-xl border text-left cursor-pointer transition-all duration-300 relative overflow-hidden"
                :class="tourStep === 4 ? 'bg-indigo-500/10 border-indigo-500/40 shadow-lg shadow-indigo-600/5' : 'bg-brand-card border-white/5 hover:border-white/10'"
              >
                <div class="flex gap-4 items-start">
                  <span class="w-7 h-7 rounded-lg flex items-center justify-center shrink-0 font-mono font-bold text-xs" :class="tourStep === 4 ? 'bg-indigo-600 text-white' : 'bg-white/5 text-gray-500'">
                    04
                  </span>
                  <div class="space-y-0.5">
                    <h3 class="text-xs font-extrabold transition-colors uppercase tracking-wider" :class="tourStep === 4 ? 'text-indigo-400' : 'text-gray-350'">In-Player Reviews Loop</h3>
                    <p class="text-[11px] text-gray-500 leading-normal">Upon completing 100% of the syllabus coursework, students drop direct rating critques right within the stream player console.</p>
                  </div>
                </div>
              </div>

              <!-- Step 5 Rail -->
              <div 
                @click="tourStep = 5"
                class="p-4 rounded-xl border text-left cursor-pointer transition-all duration-300 relative overflow-hidden"
                :class="tourStep === 5 ? 'bg-indigo-500/10 border-indigo-500/40 shadow-lg shadow-indigo-600/5' : 'bg-brand-card border-white/5 hover:border-white/10'"
              >
                <div class="flex gap-4 items-start">
                  <span class="w-7 h-7 rounded-lg flex items-center justify-center shrink-0 font-mono font-bold text-xs" :class="tourStep === 5 ? 'bg-indigo-600 text-white' : 'bg-white/5 text-gray-500'">
                    05
                  </span>
                  <div class="space-y-0.5">
                    <h3 class="text-xs font-extrabold transition-colors uppercase tracking-wider" :class="tourStep === 5 ? 'text-indigo-400' : 'text-gray-300'">Verifiable Seals & Registry</h3>
                    <p class="text-[11px] text-gray-500 leading-normal">Generate cryptographic, gold-sealed e-diplomas complete with unique audit keys that are publicly auditable.</p>
                  </div>
                </div>
              </div>

            </div>

            <!-- Right: Centerpiece Morphing Browser Mockup -->
            <div class="lg:col-span-7 relative">
              <div class="absolute -inset-1 bg-gradient-to-r from-indigo-500/10 to-emerald-500/10 rounded-2xl blur-md opacity-20"></div>
              
              <div class="relative bg-brand-card border border-white/5 rounded-2xl shadow-2xl overflow-hidden min-h-[440px] flex flex-col justify-between">
                
                <!-- Mock Top bar -->
                <div class="bg-brand-dark px-4 py-3 flex items-center justify-between border-b border-white/5">
                  <div class="flex items-center gap-1.5">
                    <div class="w-2.5 h-2.5 rounded-full bg-red-500/80"></div>
                    <div class="w-2.5 h-2.5 rounded-full bg-yellow-500/80"></div>
                    <div class="w-2.5 h-2.5 rounded-full bg-green-500/80"></div>
                    <span class="text-[9px] font-mono text-gray-500 ml-4 select-none">aether_workspace_tour.vue</span>
                  </div>
                  <div class="flex items-center gap-1.5 bg-emerald-500/10 px-2.5 py-1 rounded border border-emerald-500/20 animate-pulse">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                    <span class="text-[8px] font-mono text-emerald-400 uppercase tracking-widest font-black">LIVE SIMULATOR RIG — YOU CAN INTERACT WITH THIS SCREEN</span>
                  </div>
                </div>

                <!-- Guided Contents Morphed here -->
                <div class="p-6 flex-1 flex flex-col justify-center">
                  
                  <!-- TOUR STEP 1: Curation Studio -->
                  <div v-if="tourStep === 1" class="space-y-4 animate-fade-in text-left">
                    <div class="flex items-center justify-between">
                      <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Course Creation Suite (Educator)</span>
                      <span class="text-[9px] font-mono text-indigo-400 bg-indigo-500/10 px-1.5 py-0.5 rounded">₹ Seed Arrays</span>
                    </div>

                    <div class="grid md:grid-cols-2 gap-4">
                      
                      <!-- Royalty calculation panel -->
                      <div class="bg-brand-dark border border-white/5 p-4 rounded-xl flex flex-col justify-between h-36">
                        <div>
                          <span class="text-[9px] font-bold text-gray-500 uppercase tracking-widest">Mentor Revenue Payouts</span>
                          <h4 class="text-2xl font-black text-white mt-1">₹84,200</h4>
                          <p class="text-[9px] text-gray-400 mt-0.5">Instant split payouts routed to database.</p>
                        </div>
                        <div class="flex justify-between text-[8px] font-mono text-gray-500 pt-2 border-t border-white/5">
                          <span>Developer split: 70%</span>
                          <span class="text-emerald-400">Direct routed</span>
                        </div>
                      </div>

                      <!-- Interactive Module Builder -->
                      <div class="bg-brand-dark border border-white/5 p-4 rounded-xl h-36 flex flex-col justify-between">
                        <div class="space-y-1">
                          <span class="text-[9px] font-bold text-gray-500 uppercase tracking-widest block">Curriculum Builder</span>
                          <div class="overflow-y-auto max-h-16 pr-1 space-y-1">
                            <div v-for="(mod, idx) in mockModules" :key="idx" class="bg-brand-card/45 border border-white/5 px-2 py-0.5 rounded text-[9px] flex justify-between items-center text-gray-300">
                              <span class="truncate">{{ mod }}</span>
                              <span class="text-[8px] font-mono text-indigo-400">OK</span>
                            </div>
                          </div>
                        </div>

                        <div class="flex gap-2">
                          <input 
                            v-model="newModuleTitle"
                            type="text" 
                            placeholder="Draft module name..." 
                            class="flex-1 bg-brand-card/45 border border-white/10 rounded px-2 py-0.5 text-[9px] focus:outline-none focus:border-indigo-500"
                            @keyup.enter="addMockModule"
                          />
                          <button @click="addMockModule" class="px-2.5 py-0.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-[9px] font-bold whitespace-nowrap shadow-md shadow-indigo-600/10">
                            + Add
                          </button>
                        </div>
                        <span class="text-[8px] text-indigo-400 font-mono italic text-right block animate-pulse">← Try typing a module and click "+ Add" to populate the course list!</span>
                      </div>

                    </div>
                  </div>

                  <!-- TOUR STEP 2: Access Preview Locks -->
                  <div v-if="tourStep === 2" class="space-y-4 animate-fade-in text-left">
                    <div class="flex items-center justify-between">
                      <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">CourseAccessGuard preview limits</span>
                      <span class="text-[9px] font-mono text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded">Security Gate</span>
                    </div>

                    <div class="bg-brand-dark border border-white/5 rounded-xl p-4 space-y-2.5 relative overflow-hidden">
                      <div class="flex justify-between items-center bg-brand-card/45 p-2.5 rounded-lg border border-white/5">
                        <div class="flex items-center gap-2">
                          <PlayCircle class="w-3.5 h-3.5 text-gray-500" />
                          <span class="text-[11px] font-bold text-gray-300">Module 1: Introduction to FastAPI async</span>
                        </div>
                        <span class="text-[8px] font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">PREVIEW OPEN</span>
                      </div>

                      <div 
                        @click="lockPopupOpen = true"
                        class="flex justify-between items-center bg-brand-card/45 p-2.5 rounded-lg border border-dashed border-white/10 hover:border-indigo-500/40 cursor-pointer transition-all group animate-pulse"
                      >
                        <div class="flex items-center gap-2">
                          <Lock class="w-3.5 h-3.5 text-indigo-400 group-hover:text-indigo-300 transition-all" />
                          <span class="text-[11px] font-bold text-indigo-300 group-hover:text-indigo-200 transition-all">Module 2: Advanced CourseAccessGuard security rules</span>
                        </div>
                        <span class="text-[8px] font-mono font-bold text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">TRY CLICKING HERE</span>
                      </div>

                      <!-- Access Guard restricted overlay -->
                      <transition name="fade">
                        <div v-if="lockPopupOpen" class="absolute inset-0 bg-brand-dark/95 flex items-center justify-center p-4">
                          <div class="bg-brand-card border border-indigo-500/30 rounded-xl p-4 max-w-xs text-center space-y-3 relative">
                            <button @click="lockPopupOpen = false" class="absolute top-2 right-2 text-gray-500 hover:text-white">
                              <X class="w-3.5 h-3.5" />
                            </button>
                            <div class="w-9 h-9 rounded-full bg-indigo-500/10 flex items-center justify-center mx-auto border border-indigo-500/20">
                              <Lock class="w-4 h-4 text-indigo-400" />
                            </div>
                            <h4 class="text-xs font-bold text-white uppercase tracking-wider">PREVIEW LOCKED</h4>
                            <p class="text-[10px] text-gray-400 leading-normal">
                              Guest tokens can view the syllabus metadata outline, but full video lessons and sandboxes are blocked until enrollments are purchased.
                            </p>
                            <router-link to="/register" class="block w-full py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-[10px] font-bold transition-all">
                              Enroll to Study
                            </router-link>
                          </div>
                        </div>
                      </transition>
                    </div>
                  </div>

                  <!-- TOUR STEP 3: Gamified Workspace -->
                  <div v-if="tourStep === 3" class="space-y-4 animate-fade-in text-left">
                    <div class="flex items-center justify-between">
                      <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Gamified Study Dashboard</span>
                      <span class="text-[9px] font-mono text-purple-400 bg-purple-500/10 px-1.5 py-0.5 rounded">XP System</span>
                    </div>

                    <div class="grid md:grid-cols-12 gap-4">
                      
                      <!-- Checkbox checklist -->
                      <div class="md:col-span-5 bg-brand-dark border border-white/5 rounded-xl p-3.5 space-y-2">
                        <span class="text-[9px] font-bold text-gray-450 block uppercase tracking-widest">Milestones</span>
                        <div class="space-y-1.5">
                          <div 
                            v-for="(chk, idx) in mockChecklist" 
                            :key="idx" 
                            @click="toggleMockCheck(idx)"
                            class="flex items-center gap-2 cursor-pointer group"
                          >
                            <div class="w-3 h-3 rounded border flex items-center justify-center transition-all" :class="chk.done ? 'bg-indigo-600 border-indigo-600 text-white' : 'border-white/20 group-hover:border-white/40'">
                              <span v-if="chk.done" class="text-[8px] font-bold">✓</span>
                            </div>
                            <span class="text-[9px] truncate transition-colors" :class="chk.done ? 'line-through text-gray-500' : 'text-gray-300 group-hover:text-white'">{{ chk.text }}</span>
                          </div>
                        </div>
                      </div>

                      <!-- Notebook syncer -->
                      <div class="md:col-span-7 bg-brand-dark border border-white/5 rounded-xl p-3.5 space-y-2 flex flex-col justify-between">
                        <div class="flex items-center justify-between">
                          <span class="text-[9px] font-bold text-gray-450 block uppercase tracking-widest">Syncing Text Notes</span>
                          <span class="text-[8px] font-mono text-emerald-400 font-bold">AUTO-SAVES</span>
                        </div>
                        <textarea 
                          v-model="mockNoteText" 
                          rows="2"
                          class="w-full bg-brand-card/45 border border-white/10 rounded-lg p-2 text-[10px] text-gray-350 focus:outline-none focus:border-indigo-500 font-mono resize-none"
                        ></textarea>
                        <span class="text-[8px] text-purple-400 font-mono italic text-right block animate-pulse">← Click checkmarks on the left, or edit this text note!</span>
                      </div>

                    </div>
                  </div>

                  <!-- TOUR STEP 4: Rating Reviews -->
                  <div v-if="tourStep === 4" class="space-y-4 animate-fade-in text-left">
                    <div class="flex items-center justify-between">
                      <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">In-Player Syllabus Completion Rating</span>
                      <span class="text-[9px] font-mono text-indigo-400 bg-indigo-500/10 px-1.5 py-0.5 rounded">Feedback Loop</span>
                    </div>

                    <div class="bg-brand-dark border border-white/5 rounded-xl p-4 space-y-3">
                      <div class="flex items-center justify-between">
                        <span class="text-[10px] font-bold text-gray-300">Rate Syllabus Outlines:</span>
                        
                        <!-- Star click triggers -->
                        <div class="flex gap-1">
                          <button v-for="star in 5" :key="star" @click="activeRating = star" class="focus:outline-none">
                            <Star class="w-3.5 h-3.5 transition-colors" :class="star <= activeRating ? 'text-amber-400 fill-amber-400' : 'text-gray-600'" />
                          </button>
                        </div>
                      </div>

                      <div class="flex gap-2">
                        <input 
                          v-model="feedbackComment"
                          type="text" 
                          placeholder="Type review text..." 
                          class="flex-1 bg-brand-card/45 border border-white/10 rounded-lg px-2.5 py-1 text-[10px] focus:outline-none focus:border-indigo-500"
                          @keyup.enter="submitMockReview"
                        />
                        <button @click="submitMockReview" class="px-3 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-[10px] font-bold transition-all whitespace-nowrap shadow-md">
                          Rate Star
                        </button>
                      </div>
                      <span class="text-[8px] text-indigo-400 font-mono italic text-right block animate-pulse">← Click stars, type comments, and hit "Rate Star" to seed this feedback!</span>

                      <!-- Reviews marquee feed -->
                      <div class="space-y-1.5 border-t border-white/5 pt-2 max-h-20 overflow-y-auto">
                        <div v-for="(rev, idx) in seedReviews" :key="idx" class="bg-brand-card/45 p-2 rounded border border-white/5 text-[9px] space-y-0.5">
                          <div class="flex justify-between items-center">
                            <span class="font-bold text-gray-300">{{ rev.name }}</span>
                            <div class="flex">
                              <Star v-for="s in rev.rating" :key="s" class="w-2 h-2 text-amber-400 fill-amber-400" />
                            </div>
                          </div>
                          <p class="text-gray-400 italic">"{{ rev.comment }}"</p>
                        </div>
                      </div>

                      <transition name="fade">
                        <p v-if="feedbackSubmitted" class="text-[9px] text-emerald-400 text-center font-bold">Review seeded to MongoDB collections successfully!</p>
                      </transition>
                    </div>
                  </div>

                  <!-- TOUR STEP 5: Diploma seals -->
                  <div v-if="tourStep === 5" class="space-y-4 animate-fade-in text-left">
                    <div class="flex items-center justify-between">
                      <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Cryptographic E-Diploma Engine</span>
                      <span class="text-[9px] font-mono text-purple-400 bg-purple-500/10 px-1.5 py-0.5 rounded">SHA-256 Hashes</span>
                    </div>

                    <div class="bg-brand-dark border border-white/5 rounded-xl p-4 flex flex-col items-center justify-center min-h-[160px]">
                      <button 
                        v-if="!certMinted"
                        @click="mintCertHash"
                        class="px-5 py-2.5 bg-gradient-to-r from-emerald-600 to-indigo-600 hover:from-emerald-500 hover:to-indigo-500 text-white rounded-lg font-bold text-xs transition-all shadow-md animate-pulse"
                        :disabled="generatingCert"
                      >
                        {{ generatingCert ? 'MINTING SECURED HASH IN MONGO...' : 'CLICK HERE TO MINT SECURED DIPLOMA' }}
                      </button>

                      <div 
                        v-else 
                        class="w-full bg-brand-card/45 border border-amber-500/20 rounded-xl p-4 text-center space-y-3 relative overflow-hidden animate-fade-in"
                      >
                        <div class="absolute top-1 right-1 w-16 h-16 border-2 border-amber-500/10 rounded-full flex items-center justify-center rotate-12 pointer-events-none">
                          <span class="text-[6px] text-amber-500/30 font-mono font-bold tracking-widest">AETHER TRUST</span>
                        </div>
                        
                        <div class="w-8 h-8 rounded-full bg-amber-500/10 flex items-center justify-center mx-auto border border-amber-500/30">
                          <Award class="w-4 h-4 text-amber-400" />
                        </div>
                        
                        <div>
                          <h4 class="text-[10px] font-bold text-amber-400 font-serif uppercase tracking-widest">DIPLOMA OF COMPLETION</h4>
                          <p class="text-[8px] text-gray-450 mt-0.5">ISSUED BY THE ACADEMIC TRUSTEE FOR COURSE:</p>
                          <p class="text-[10px] font-extrabold text-white uppercase mt-0.5 tracking-tight font-serif">FastAPI Backend System Architectures</p>
                        </div>

                        <div class="border-t border-white/5 pt-2 flex justify-between text-[7px] text-gray-500 font-mono">
                          <span>AUDIT ID: CERT-ENROLL-1</span>
                          <span class="text-emerald-400">HASH: SHA-256 SECURED</span>
                        </div>
                      </div>
                    </div>
                  </div>

                </div>

                <!-- Live Interaction Helper Footnote Banner -->
                <div class="mx-6 my-2 bg-indigo-500/5 border border-indigo-500/15 px-4 py-2 rounded-xl flex items-center justify-center gap-2.5">
                  <Sparkles class="w-3 h-3 text-indigo-400 animate-pulse shrink-0" />
                  <p class="text-[9px] font-mono text-indigo-300 leading-normal text-left">
                    <strong>Try it live:</strong> Click checkboxes, type modules and add them, click locked rows, click star feedback, or trigger diploma minting right inside this preview!
                  </p>
                </div>

                <!-- Mock Footer Navigation -->
                <div class="border-t border-white/5 bg-brand-dark px-6 py-4 flex items-center justify-between">
                  <button 
                    @click="tourStep = tourStep > 1 ? tourStep - 1 : 5" 
                    class="px-3 py-1 bg-white/5 hover:bg-white/10 rounded text-[10px] font-bold border border-white/5 transition-all text-gray-300"
                  >
                    ← Prev Stage
                  </button>

                  <div class="flex gap-1.5">
                    <div v-for="s in 5" :key="s" class="w-1.5 h-1.5 rounded-full transition-all" :class="s === tourStep ? 'w-4 bg-indigo-500' : 'bg-white/10'"></div>
                  </div>

                  <button 
                    @click="tourStep = tourStep < 5 ? tourStep + 1 : 1" 
                    class="px-3 py-1 bg-white/5 hover:bg-white/10 rounded text-[10px] font-bold border border-white/5 transition-all text-gray-300"
                  >
                    Next Stage →
                  </button>
                </div>

              </div>
            </div>

          </div>
        </section>

        <!-- Developer IDE Sandbox Compiler Section -->
        <section id="sandbox" class="py-20 border-t border-white/5 relative">
          
          <div class="text-center max-w-2xl mx-auto mb-16 space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20">
              <Cpu class="w-3 h-3 text-purple-400 animate-pulse" />
              <span class="text-[9px] font-bold text-purple-400 uppercase tracking-widest font-mono">Developer Environment</span>
            </div>
            <h2 class="text-3xl font-black tracking-tight text-white">Interactive Dev Sandbox IDE</h2>
            <p class="text-xs text-gray-400">
              Aether integrates active sandbox frameworks. Click the code editor tabs to inspect our application files, press Compile simulation, and watch the Uvicorn/Vite CLI terminal logging stream in real-time.
            </p>
          </div>

          <div class="relative max-w-4xl mx-auto">
            <div class="absolute -inset-1 bg-gradient-to-r from-purple-500/10 to-indigo-500/10 rounded-2xl blur-md opacity-25"></div>
            
            <div class="relative bg-brand-card border border-white/5 rounded-2xl shadow-2xl overflow-hidden">
              
              <!-- IDE Tabs -->
              <div class="bg-brand-dark px-4 py-3 flex items-center justify-between border-b border-white/5">
                <div class="flex items-center gap-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
                  <span class="text-[10px] font-mono text-gray-400">aether_compilation_rig.py</span>
                </div>
                
                <div class="flex gap-2">
                  <button 
                    @click="sandboxTab = 'backend'"
                    class="px-2.5 py-0.5 rounded text-[10px] font-bold font-mono transition-all"
                    :class="sandboxTab === 'backend' ? 'bg-purple-600 text-white' : 'bg-white/5 text-gray-400 hover:text-white'"
                  >
                    main.py (FastAPI)
                  </button>
                  <button 
                    @click="sandboxTab = 'frontend'"
                    class="px-2.5 py-0.5 rounded text-[10px] font-bold font-mono transition-all"
                    :class="sandboxTab === 'frontend' ? 'bg-purple-600 text-white' : 'bg-white/5 text-gray-400 hover:text-white'"
                  >
                    Home.vue (Vite Client)
                  </button>
                </div>
              </div>

              <!-- Compilation RIG panel -->
              <div class="grid md:grid-cols-12">
                
                <!-- Code Editor View -->
                <div class="md:col-span-7 bg-[#020204] p-5 border-r border-white/5 min-h-[200px]">
                  <pre v-if="sandboxTab === 'backend'" class="text-[10px] text-gray-400 font-mono text-left overflow-x-auto select-none leading-relaxed">
<span class="text-purple-400">from</span> fastapi <span class="text-purple-400">import</span> FastAPI, Depends
<span class="text-purple-400">from</span> app.services <span class="text-purple-400">import</span> CourseAccessGuard

app = FastAPI(title=<span class="text-emerald-400">"Aether Core"</span>)

<span class="text-purple-400">@app.get</span>(<span class="text-emerald-400">"/api/v1/courses/{course_id}/play"</span>)
<span class="text-purple-400">async def</span> play_lesson(course_id: <span class="text-amber-400">str</span>, user = Depends(CourseAccessGuard)):
    <span class="text-gray-500"># Restricts non-enrolled students automatically</span>
    <span class="text-purple-400">return</span> {<span class="text-emerald-400">"status"</span>: <span class="text-emerald-400">"success"</span>, <span class="text-emerald-400">"payload"</span>: <span class="text-emerald-400">"stream_loaded"</span>}
                  </pre>
                  
                  <pre v-else class="text-[10px] text-gray-400 font-mono text-left overflow-x-auto select-none leading-relaxed">
<span class="text-purple-400">&lt;script</span> setup<span class="text-purple-400">&gt;</span>
<span class="text-purple-400">import</span> { ref } <span class="text-purple-400">from</span> <span class="text-emerald-400">'vue'</span>;
<span class="text-purple-400">import</span> { useCoursesStore } <span class="text-purple-400">from</span> <span class="text-emerald-400">'@/store/courses'</span>;

<span class="text-purple-400">const</span> courses = useCoursesStore();
<span class="text-purple-400">const</span> isCompiling = ref(<span class="text-amber-400">false</span>);
<span class="text-purple-400">&lt;/script&gt;</span>

<span class="text-purple-400">&lt;template&gt;</span>
  <span class="text-purple-400">&lt;div</span> class=<span class="text-emerald-400">"glass-card animate-pulse"</span><span class="text-purple-400">&gt;</span>
    Sandbox IDE Compiled Successfully!
  <span class="text-purple-400">&lt;/div&gt;</span>
<span class="text-purple-400">&lt;/template&gt;</span>
                  </pre>
                </div>

                <!-- CLI Terminal output log viewer -->
                <div class="md:col-span-5 bg-[#050508] p-5 flex flex-col justify-between min-h-[200px]">
                  <div class="space-y-2">
                    <div class="flex items-center justify-between text-[9px] font-mono text-gray-500 uppercase tracking-widest pb-1.5 border-b border-white/5">
                      <span>Bash logs feed</span>
                      <span class="text-purple-400">Terminal CLI</span>
                    </div>
                    
                    <div class="space-y-1 font-mono text-[9px] text-left">
                      <p v-if="sandboxLogs.length === 0" class="text-gray-500 italic">No compilations active. Press compiler trigger below.</p>
                      <p 
                        v-for="(log, idx) in sandboxLogs" 
                        :key="idx"
                        :class="{
                          'text-emerald-400 font-bold': log.startsWith('✓'),
                          'text-purple-400': log.startsWith('⚡'),
                          'text-amber-300': log.includes('CourseAccessGuard'),
                          'text-gray-400': !log.startsWith('✓') && !log.startsWith('⚡') && !log.includes('CourseAccessGuard')
                        }"
                      >
                        {{ log }}
                      </p>
                    </div>
                  </div>

                  <button 
                    @click="runCompileSimulation"
                    class="w-full mt-4 py-2 bg-purple-600 hover:bg-purple-500 disabled:bg-purple-900/50 text-white rounded-lg text-xs font-bold transition-all shadow-md flex items-center justify-center gap-2"
                    :disabled="isCompiling"
                  >
                    <RefreshCw class="w-3 h-3" :class="{ 'animate-spin': isCompiling }" />
                    {{ isCompiling ? 'COMPILING SANDBOX...' : 'COMPILE SIMULATION' }}
                  </button>
                </div>

              </div>

            </div>
          </div>
        </section>

        <!-- Course Pathfinder Wizard preference filter calculator -->
        <section class="py-16 relative">
          <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[35rem] h-[15rem] bg-indigo-600/5 rounded-full blur-[120px] pointer-events-none"></div>

          <div class="bg-brand-card border border-white/5 rounded-2xl p-8 md:p-12 relative overflow-hidden text-center max-w-4xl mx-auto">
            
            <div class="text-center mb-8 max-w-lg mx-auto space-y-1">
              <span class="text-[9px] font-bold text-indigo-400 uppercase tracking-widest block font-mono">Interest Filter Matrix</span>
              <h2 class="text-2xl font-black text-white">Interactive Pathfinder Engine</h2>
              <p class="text-xs text-gray-400">Answer two quick interest targets and we will customize the course showroom specifically to your background skill level.</p>
            </div>

            <div class="max-w-xl mx-auto relative z-10">
              
              <!-- Progress Timeline Dot indicators -->
              <div class="flex justify-center items-center gap-2 mb-8">
                <div class="h-1 rounded-full transition-all" :class="pathfinderStep >= 1 ? 'w-10 bg-indigo-500' : 'w-3 bg-white/10'"></div>
                <div class="h-1 rounded-full transition-all" :class="pathfinderStep >= 2 ? 'w-10 bg-indigo-500' : 'w-3 bg-white/10'"></div>
                <div class="h-1 rounded-full transition-all" :class="pathfinderStep >= 3 ? 'w-10 bg-indigo-500' : 'w-3 bg-white/10'"></div>
              </div>

              <!-- Question 1: What is primary goal -->
              <div v-if="pathfinderStep === 1" class="space-y-4 animate-fade-in">
                <p class="text-center font-bold text-xs text-gray-400 uppercase tracking-widest mb-6">Select your primary professional target:</p>
                <div class="grid sm:grid-cols-3 gap-4">
                  
                  <button 
                    @click="handleSelectGoal('frontend')" 
                    class="bg-brand-dark border border-white/5 hover:border-indigo-500/50 rounded-xl p-5 text-center transition-all group"
                  >
                    <div class="w-8 h-8 rounded-lg bg-indigo-500/10 flex items-center justify-center mx-auto mb-3 group-hover:scale-105 transition-all">
                      <Monitor class="w-4 h-4 text-indigo-400" />
                    </div>
                    <span class="font-bold text-xs block text-brand-light uppercase tracking-wider">Frontend UI</span>
                    <span class="text-[9px] text-gray-500 block mt-1 leading-normal">Client aesthetics & Vue setups</span>
                  </button>

                  <button 
                    @click="handleSelectGoal('backend')" 
                    class="bg-brand-dark border border-white/5 hover:border-emerald-500/50 rounded-xl p-5 text-center transition-all group"
                  >
                    <div class="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center mx-auto mb-3 group-hover:scale-105 transition-all">
                      <Cpu class="w-4 h-4 text-emerald-400" />
                    </div>
                    <span class="font-bold text-xs block text-brand-light uppercase tracking-wider">Backend & API</span>
                    <span class="text-[9px] text-gray-500 block mt-1 leading-normal">FastAPI pipelines & DB seeds</span>
                  </button>

                  <button 
                    @click="handleSelectGoal('design')" 
                    class="bg-brand-dark border border-white/5 hover:border-purple-500/50 rounded-xl p-5 text-center transition-all group"
                  >
                    <div class="w-8 h-8 rounded-lg bg-purple-500/10 flex items-center justify-center mx-auto mb-3 group-hover:scale-105 transition-all">
                      <Palette class="w-4 h-4 text-purple-400" />
                    </div>
                    <span class="font-bold text-xs block text-gray-200 uppercase tracking-wider">UI/UX Design</span>
                    <span class="text-[9px] text-gray-500 block mt-1 leading-normal">Wireframes & gradient tokens</span>
                  </button>

                </div>
              </div>

              <!-- Question 2: Experience level -->
              <div v-else-if="pathfinderStep === 2" class="space-y-4 animate-fade-in">
                <p class="text-center font-bold text-xs text-gray-400 uppercase tracking-widest mb-6">Define your active coding background:</p>
                <div class="grid sm:grid-cols-3 gap-4">
                  
                  <button 
                    @click="handleSelectExp('beginner')" 
                    class="bg-brand-dark border border-white/5 hover:border-indigo-500/50 rounded-xl p-5 text-center transition-all"
                  >
                    <span class="text-lg block mb-2">🎓</span>
                    <span class="font-bold text-xs block text-brand-light uppercase tracking-wider">Novice</span>
                    <span class="text-[9px] text-gray-500 block mt-1 leading-normal">Learning basics & system outlines</span>
                  </button>

                  <button 
                    @click="handleSelectExp('intermediate')" 
                    class="bg-brand-dark border border-white/5 hover:border-emerald-500/50 rounded-xl p-5 text-center transition-all"
                  >
                    <span class="text-lg block mb-2">⚡</span>
                    <span class="font-bold text-xs block text-brand-light uppercase tracking-wider">Developer</span>
                    <span class="text-[9px] text-gray-500 block mt-1 leading-normal">Assembled server nodes cleanly</span>
                  </button>

                  <button 
                    @click="handleSelectExp('advanced')" 
                    class="bg-brand-dark border border-white/5 hover:border-purple-500/50 rounded-xl p-5 text-center transition-all"
                  >
                    <span class="text-lg block mb-2">🚀</span>
                    <span class="font-bold text-xs block text-gray-200 uppercase tracking-wider">Lead coder</span>
                    <span class="text-[9px] text-gray-500 block mt-1 leading-normal">Familiar with API compilations</span>
                  </button>

                </div>
                <button @click="pathfinderStep = 1" class="text-[10px] text-gray-500 hover:text-white block mx-auto mt-4 font-bold uppercase font-mono">← Back to goal</button>
              </div>

              <!-- Recommendation Panel -->
              <div v-else-if="pathfinderStep === 3" class="text-center space-y-5 animate-fade-in">
                <div class="w-12 h-12 rounded-full bg-indigo-500/10 flex items-center justify-center mx-auto border border-indigo-500/20">
                  <Trophy class="w-6 h-6 text-indigo-400" />
                </div>
                <div class="space-y-0.5">
                  <p class="text-[10px] text-gray-500 uppercase tracking-widest font-bold font-mono">Custom track recommendation:</p>
                  <p class="text-xl font-extrabold text-indigo-400 uppercase tracking-wider">{{ recommendedCategory }} Curriculum</p>
                </div>
                
                <div class="flex items-center justify-center gap-3">
                  <button @click="applyPathfinderResult" class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-bold text-xs inline-flex items-center gap-2 transition-all shadow-md shadow-indigo-600/20">
                    Apply filter & scroll
                    <ArrowRight class="w-3.5 h-3.5" />
                  </button>
                  <button @click="resetPathfinder" class="px-4 py-2.5 bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white rounded-lg font-bold text-xs border border-white/5 transition-all">
                    Reset Filter
                  </button>
                </div>
              </div>

            </div>

          </div>
        </section>

        <!-- Course Showroom Deck Catalog -->
        <section id="catalog-view" class="py-20 border-t border-white/5 scroll-mt-24">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12">
            <div class="space-y-1 text-left">
              <span class="text-[9px] font-bold text-emerald-400 uppercase tracking-widest block font-mono">Live Syllabus Database</span>
              <h2 class="text-3xl font-black text-white">Browse Premium Curriculums</h2>
              <p class="text-xs text-gray-400">Instantly browse vetted courses compiled and seeded directly inside MongoDB.</p>
            </div>
            
            <div class="relative w-full md:w-80">
              <Search class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="Search syllabi content, teacher..." 
                class="pl-10 pr-4 py-2.5 bg-brand-card border border-white/10 rounded-xl text-xs focus:outline-none focus:border-indigo-500/50 w-full font-mono text-gray-300"
              />
            </div>
          </div>

          <!-- Category filter bubble bar -->
          <div class="flex gap-2 overflow-x-auto pb-4 mb-8">
            <button 
              v-for="cat in categories" 
              :key="cat"
              @click="selectedCategory = cat"
              class="px-5 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition-all border uppercase tracking-wider font-mono"
              :class="selectedCategory === cat ? 'bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-600/10' : 'bg-brand-card border-white/5 text-gray-400 hover:bg-white/5 hover:text-white'"
            >
              {{ cat }}
            </button>
          </div>

          <!-- Grid layout of course cards -->
          <div v-if="filteredCourses.length > 0" class="space-y-8">
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="course in visibleCourses" :key="course.id" class="transition-all duration-300">
                <CourseCard :course="course" />
              </div>
            </div>

            <!-- Expansion / Auth trigger button -->
            <div v-if="filteredCourses.length > 6 || !authStore.isAuthenticated" class="text-center pt-6">
              <button @click="handleViewMoreCourses" class="px-5 py-2.5 bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white rounded-lg font-bold text-xs transition-all inline-flex items-center gap-2 border border-white/10">
                <span>{{ authStore.isAuthenticated ? (isCoursesExpanded ? 'Show Less Courses' : 'View Full Catalog (' + filteredCourses.length + ' courses)') : 'Sign In to access premium databases' }}</span>
                <ChevronDown v-if="!isCoursesExpanded || !authStore.isAuthenticated" class="w-4 h-4" />
                <ChevronUp v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <div v-else class="text-center py-16 bg-brand-card border border-dashed border-white/5 rounded-2xl">
            <div class="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-3">
              <Search class="w-4 h-4 text-gray-500" />
            </div>
            <p class="text-xs text-gray-500 font-mono">No courses found matching search criteria.</p>
            <button @click="searchQuery = ''; selectedCategory = 'All'" class="mt-4 text-xs text-indigo-400 font-bold hover:text-indigo-300 underline">Clear active filters</button>
          </div>
        </section>

        <!-- Dynamic Collapsible FAQ Accordion Section -->
        <section id="faq" class="py-16 border-t border-white/5 scroll-mt-24">
          <div class="text-center mb-12 space-y-1 animate-fade-in">
            <span class="text-[9px] font-bold text-indigo-400 uppercase tracking-widest block font-mono">Platform Clarity Module</span>
            <h2 class="text-3xl font-black text-white">Frequently Asked Questions</h2>
            <p class="text-xs text-gray-400 font-mono">Clear information regarding Aether ecosystem policies.</p>
          </div>

          <div class="max-w-2xl mx-auto space-y-3">
            
            <div class="bg-brand-card border border-white/5 rounded-xl overflow-hidden transition-all">
              <button @click="toggleFaq(1)" class="w-full flex justify-between items-center p-4 text-left hover:bg-white/[0.01]">
                <span class="text-xs md:text-sm font-bold text-gray-300">How does the 70% instructor payout royalty split operate?</span>
                <ChevronDown v-if="activeFaq !== 1" class="w-4 h-4 text-gray-500" />
                <ChevronUp v-else class="w-4 h-4 text-indigo-400" />
              </button>
              <transition name="faq">
                <div v-if="activeFaq === 1" class="px-4 pb-4 text-xs text-gray-400 border-t border-white/5 pt-3 leading-relaxed font-mono">
                  When students purchase your course draft inside Aether, our backend service automatically routes 70% of the funds to the educator ledger arrays, while the platform retains 30% for maintenance.
                </div>
              </transition>
            </div>

            <div class="bg-brand-card border border-white/5 rounded-xl overflow-hidden transition-all">
              <button @click="toggleFaq(2)" class="w-full flex justify-between items-center p-4 text-left hover:bg-white/[0.01]">
                <span class="text-xs md:text-sm font-bold text-gray-300">What does the CourseAccessGuard check for?</span>
                <ChevronDown v-if="activeFaq !== 2" class="w-4 h-4 text-gray-500" />
                <ChevronUp v-else class="w-4 h-4 text-indigo-400" />
              </button>
              <transition name="faq">
                <div v-if="activeFaq === 2" class="px-4 pb-4 text-xs text-gray-400 border-t border-white/5 pt-3 leading-relaxed font-mono">
                  The guard serves as our security gate. Guests can inspect curriculum outlines (Syllabus Breakdowns), but video playbacks and interactive code sandboxes require verified enrollment record matching.
                </div>
              </transition>
            </div>

            <div class="bg-brand-card border border-white/5 rounded-xl overflow-hidden transition-all">
              <button @click="toggleFaq(3)" class="w-full flex justify-between items-center p-4 text-left hover:bg-white/[0.01]">
                <span class="text-xs md:text-sm font-bold text-gray-300">Are my course notes kept safely saved?</span>
                <ChevronDown v-if="activeFaq !== 3" class="w-4 h-4 text-gray-500" />
                <ChevronUp v-else class="w-4 h-4 text-indigo-400" />
              </button>
              <transition name="faq">
                <div v-if="activeFaq === 3" class="px-4 pb-4 text-xs text-gray-400 border-t border-white/5 pt-3 leading-relaxed font-mono">
                  Yes. Aether features persistent text notebooks. Whenever you jot thoughts or notes during course playbacks, the sync engine stores them automatically, allowing you to access them upon subsequent logins.
                </div>
              </transition>
            </div>

          </div>
        </section>

        <!-- Newsletter Subscription Segment -->
        <section class="py-16">
          <div class="bg-brand-card border border-white/5 rounded-2xl p-8 md:p-12 text-center relative overflow-hidden max-w-4xl mx-auto">
            <Mail class="w-8 h-8 text-indigo-400 mx-auto mb-3 animate-bounce" style="animation-duration: 4s;" />
            <h2 class="text-2xl font-black text-white">Subscribe to Aether Digests</h2>
            <p class="text-xs text-gray-400 max-w-sm mx-auto mb-6">Stay informed on system enhancements, new verified sandboxes, and fresh MongoDB syllabus seeds.</p>
            
            <form @submit.prevent="handleSubscribe" class="flex flex-col sm:flex-row gap-2 max-w-md mx-auto relative z-10">
              <input 
                v-model="newsletterEmail" 
                type="email" 
                required
                placeholder="Enter developer email address..." 
                class="flex-1 px-4 py-2.5 bg-brand-dark border border-white/10 rounded-lg focus:outline-none focus:border-indigo-500/50 text-xs font-mono text-gray-300"
              />
              <button type="submit" class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-bold text-xs transition-all shadow-md shadow-indigo-600/10">
                Subscribe
              </button>
            </form>
            <p v-if="newsletterSuccessMsg" class="text-emerald-400 text-xs mt-3 font-mono font-bold">{{ newsletterSuccessMsg }}</p>
          </div>
        </section>

      </div>
    </main>

    <!-- Obsidian Footer -->
    <footer class="border-t border-white/5 py-12 bg-brand-dark relative z-10 text-left">
      <div class="max-w-7xl mx-auto px-6">
        
        <div class="grid md:grid-cols-4 gap-8 mb-10">
          
          <div class="space-y-3">
            <div class="flex items-center gap-2">
              <div class="w-6 h-6 rounded bg-gradient-to-br from-indigo-500 to-emerald-500 flex items-center justify-center">
                <span class="font-extrabold text-white text-[10px]">Æ</span>
              </div>
              <span class="font-bold text-sm text-white">Aether Academy</span>
            </div>
            <p class="text-[10px] text-gray-500 leading-relaxed font-mono">
              Next-generation operational e-learning rig connecting mentors, students, and verifiable hashes.
            </p>
          </div>

          <div class="space-y-2">
            <h4 class="text-[10px] font-bold text-white uppercase tracking-wider font-mono">Operational</h4>
            <div class="flex flex-col gap-1.5 text-[10px] text-gray-500 font-mono">
              <a href="#platform-tour" class="hover:text-white transition-colors">Tour Stepper</a>
              <a href="#sandbox" class="hover:text-white transition-colors">Compiler Rig</a>
              <a href="#catalog-view" class="hover:text-white transition-colors">Syllabi Deck</a>
            </div>
          </div>

          <div class="space-y-2">
            <h4 class="text-[10px] font-bold text-white uppercase tracking-wider font-mono">Registry</h4>
            <div class="flex flex-col gap-1.5 text-[10px] text-gray-500 font-mono">
              <router-link to="/login" class="hover:text-white transition-colors">Course Guard</router-link>
              <a href="#catalog-view" class="hover:text-white transition-colors">Course Showroom</a>
              <span class="text-emerald-400 font-bold uppercase tracking-wider">Ledger Active</span>
            </div>
          </div>

          <div class="space-y-2">
            <h4 class="text-[10px] font-bold text-white uppercase tracking-wider font-mono">Academy</h4>
            <div class="flex flex-col gap-1.5 text-[10px] text-gray-500 font-mono">
              <a href="#faq" class="hover:text-white transition-colors">Curriculum FAQs</a>
              <a href="#" class="hover:text-white transition-colors">Developer SLA</a>
              <span class="text-gray-600">v1.2.0 Seeding</span>
            </div>
          </div>

        </div>

        <div class="flex flex-col sm:flex-row justify-between items-center gap-4 border-t border-white/5 pt-6">
          <div class="flex gap-4 text-[9px] text-gray-500 font-mono">
            <a href="#" class="hover:text-white transition-colors">Terms of Service</a>
            <a href="#" class="hover:text-white transition-colors">Privacy Ledgers</a>
          </div>
          <p class="text-[9px] text-gray-500 font-mono">© 2026 Aether Academy. All rights reserved. Educational DAO.</p>
        </div>

      </div>
    </footer>
  </div>
</template>

<style scoped>
/* FAQ Accordion Transitions */
.faq-enter-active,
.faq-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 200px;
  opacity: 1;
}

.faq-enter-from,
.faq-leave-to {
  max-height: 0;
  opacity: 0;
  padding-top: 0;
  padding-bottom: 0;
}

html {
  scroll-behavior: smooth;
}

/* Moving Grid dot backdrop */
.grid-bg {
  background-image: 
    radial-gradient(circle at 1px 1px, rgba(99, 102, 241, 0.08) 1px, transparent 0);
  background-size: 24px 24px;
  background-position: center;
  mask-image: radial-gradient(ellipse 60% 50% at 50% 50%, #000 70%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse 60% 50% at 50% 50%, #000 70%, transparent 100%);
}

.animate-fade-in {
  animation: fadeIn 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>>