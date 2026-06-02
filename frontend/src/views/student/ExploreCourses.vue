<script setup>
import { ref, computed } from 'vue';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import CourseCard from '../../components/CourseCard.vue';
import { 
  Search, Compass, Star, BookOpen, Clock, PlayCircle, 
  ArrowRight, X, SlidersHorizontal, Sparkles, AlertCircle, ChevronDown,
  Monitor, Cpu, Palette, Award, ShieldCheck, GraduationCap
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();

// Search & Filter State
const searchQuery = ref('');
const selectedCategory = ref('All');
const selectedDifficulty = ref('All');
const sortBy = ref('popularity'); // popularity, rating, duration-asc, duration-desc, title

// List of available difficulties
const difficulties = ['All', 'Beginner', 'Intermediate', 'Advanced'];

// Real-time Approved Course Counts and colorful icons for dynamic categories showcase
const categoryStats = computed(() => {
  const stats = {
    All: { count: 0, icon: Compass, color: 'text-brand-primary bg-brand-primary/10 border-brand-primary/20' },
    Development: { count: 0, icon: Monitor, color: 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20' },
    Backend: { count: 0, icon: Cpu, color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' },
    Design: { count: 0, icon: Palette, color: 'text-amber-400 bg-amber-500/10 border-amber-500/20' }
  };
  
  coursesStore.approvedCourses.forEach(c => {
    stats.All.count++;
    if (stats[c.category]) {
      stats[c.category].count++;
    }
  });

  return stats;
});

// Filtered and Sorted Course List
const filteredAndSortedCourses = computed(() => {
  let list = [...coursesStore.approvedCourses];

  // 1. Filter by Search Query (Title, Description, and Teacher)
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    list = list.filter(course => {
      return (
        course.title.toLowerCase().includes(query) ||
        (course.shortDescription || course.description || '').toLowerCase().includes(query) ||
        course.teacherName.toLowerCase().includes(query)
      );
    });
  }

  // 2. Filter by Category
  if (selectedCategory.value !== 'All') {
    list = list.filter(course => course.category === selectedCategory.value);
  }

  // 3. Filter by Difficulty
  if (selectedDifficulty.value !== 'All') {
    list = list.filter(course => course.difficulty === selectedDifficulty.value);
  }

  // 4. Advanced Sorting
  if (sortBy.value === 'rating') {
    list.sort((a, b) => b.rating - a.rating);
  } else if (sortBy.value === 'popularity') {
    list.sort((a, b) => b.reviewsCount - a.reviewsCount);
  } else if (sortBy.value === 'duration-asc') {
    list.sort((a, b) => {
      const durationA = parseInt(a.duration) || 0;
      const durationB = parseInt(b.duration) || 0;
      return durationA - durationB;
    });
  } else if (sortBy.value === 'duration-desc') {
    list.sort((a, b) => {
      const durationA = parseInt(a.duration) || 0;
      const durationB = parseInt(b.duration) || 0;
      return durationB - durationA;
    });
  } else if (sortBy.value === 'title') {
    list.sort((a, b) => a.title.localeCompare(b.title));
  }

  return list;
});

// Reset all search and filter conditions
const resetFilters = () => {
  searchQuery.value = '';
  selectedCategory.value = 'All';
  selectedDifficulty.value = 'All';
  sortBy.value = 'popularity';
};
</script>

<template>
  <div class="space-y-10 py-4 glow-bg min-h-[85vh]">
    <!-- Welcome Header Title Row -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="space-y-1.5 text-left">
        <h1 class="text-2xl md:text-3xl font-extrabold text-white font-display flex items-center space-x-2">
          <GraduationCap class="w-7 h-7 text-brand-primary" />
          <span>Curriculum Library & Explorer</span>
        </h1>
        <p class="text-xs text-gray-400">Expand your stack. Browse courses, toggle filters, and enroll instantly to start your journey.</p>
      </div>
    </div>

    <!-- 1. Interactive Category Card Widgets (Showcase Row) -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div 
        v-for="(stat, name) in categoryStats" 
        :key="name"
        @click="selectedCategory = name"
        class="glass-panel p-5 rounded-3xl border transition-all duration-300 cursor-pointer flex items-center space-x-4 shadow-xl hover:translate-y-[-4px] active:scale-[0.98]"
        :class="selectedCategory === name 
          ? 'bg-brand-primary/10 border-brand-primary/45 shadow-lg shadow-brand-primary/5' 
          : 'bg-brand-card hover:bg-brand-card-hover border-white/5 hover:border-white/10'"
      >
        <span class="p-3.5 rounded-2xl flex items-center justify-center shrink-0 border" :class="stat.color">
          <component :is="stat.icon" class="w-5 h-5" />
        </span>
        <div class="text-left truncate">
          <p class="text-[10px] font-bold text-gray-500 uppercase tracking-widest">{{ name === 'All' ? 'Overview' : name }}</p>
          <p class="text-base font-black text-white mt-0.5 leading-tight">{{ name }}</p>
          <p class="text-[10px] text-brand-accent font-bold mt-1">{{ stat.count }} Course{{ stat.count === 1 ? '' : 's' }}</p>
        </div>
      </div>
    </div>

    <!-- 2. Dual-Column Sidebar & Grid Catalog -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
      <!-- Left Sidebar: Filter Pane -->
      <aside class="glass-panel p-6 rounded-3xl border border-white/5 bg-brand-card space-y-6 shadow-xl relative overflow-hidden group">
        <!-- Background light design effect -->
        <div class="absolute -right-10 -bottom-10 w-32 h-32 bg-brand-primary/5 rounded-full blur-2xl pointer-events-none"></div>

        <div class="space-y-4">
          <!-- Search Header Widget -->
          <div class="space-y-1.5 text-left border-b border-white/5 pb-4">
            <span class="flex items-center space-x-1.5 text-brand-primary text-[10px] font-bold uppercase tracking-wider">
              <Search class="w-3.5 h-3.5" />
              <span>Query Search</span>
            </span>
            <h3 class="text-xs font-bold text-white uppercase tracking-wider font-display">Refine Courses</h3>
            
            <!-- Custom Search Box -->
            <div class="relative w-full pt-2">
              <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="Search stacks..." 
                class="w-full pl-9 pr-8 py-2.5 bg-brand-dark/40 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-1 focus:ring-brand-primary placeholder-gray-550 transition-all shadow-inner"
              />
              <button 
                v-if="searchQuery" 
                @click="searchQuery = ''"
                class="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white p-0.5 rounded-lg"
              >
                <X class="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          <!-- Difficulty selection radio row checklist -->
          <div class="space-y-3 text-left border-b border-white/5 pb-4">
            <span class="text-[9px] font-bold text-gray-500 uppercase tracking-widest">Select Difficulty</span>
            <div class="space-y-2">
              <label 
                v-for="diff in difficulties" 
                :key="diff"
                class="flex items-center space-x-2.5 text-xs text-gray-300 hover:text-white cursor-pointer select-none"
              >
                <input 
                  type="radio" 
                  name="difficulty" 
                  :value="diff" 
                  v-model="selectedDifficulty"
                  class="accent-brand-primary w-4 h-4 cursor-pointer"
                />
                <span :class="{'text-white font-semibold': selectedDifficulty === diff}">
                  {{ diff === 'All' ? 'All Skill Levels' : diff }}
                </span>
              </label>
            </div>
          </div>

          <!-- Sorting selection dropdown filter -->
          <div class="space-y-2.5 text-left border-b border-white/5 pb-4">
            <span class="text-[9px] font-bold text-gray-500 uppercase tracking-widest">Catalog Sorting</span>
            <div class="relative">
              <select 
                v-model="sortBy"
                class="w-full pl-3 pr-8 py-2.5 bg-brand-dark/40 border border-white/10 text-xs text-gray-300 rounded-xl focus:outline-none focus:ring-1 focus:ring-brand-primary cursor-pointer transition-all shadow-inner appearance-none"
              >
                <option value="popularity">Most Popular</option>
                <option value="rating">Highest Rated</option>
                <option value="duration-asc">Shortest Duration</option>
                <option value="duration-desc">Longest Duration</option>
                <option value="title">Alphabetical A-Z</option>
              </select>
              <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
            </div>
          </div>

          <!-- Student Stats Widget inside Sidebar -->
          <div class="p-4 bg-brand-card border border-white/5 rounded-2xl text-left space-y-3.5 shadow-sm">
            <p class="text-[10px] font-bold text-gray-550 uppercase tracking-widest flex items-center space-x-1.5">
              <Award class="w-3.5 h-3.5 text-brand-primary" />
              <span>My Portal Progress</span>
            </p>
            <div class="grid grid-cols-3 gap-2 text-center">
              <div class="p-2 bg-brand-dark/45 rounded-xl border border-white/5">
                <span class="text-xs font-black text-white block">{{ coursesStore.getStudentEnrollments(authStore.currentUser?.id).length }}</span>
                <span class="text-[8px] text-gray-450 uppercase tracking-wider font-semibold block mt-0.5">Enrolled</span>
              </div>
              <div class="p-2 bg-brand-dark/45 rounded-xl border border-white/5">
                <span class="text-xs font-black text-brand-accent block">{{ coursesStore.getCertificates(authStore.currentUser?.id).length }}</span>
                <span class="text-[8px] text-gray-450 uppercase tracking-wider font-semibold block mt-0.5">Passed</span>
              </div>
              <div class="p-2 bg-brand-dark/45 rounded-xl border border-white/5">
                <span class="text-xs font-black text-brand-warning block">{{ coursesStore.getStudentBookmarks(authStore.currentUser?.id).length }}</span>
                <span class="text-[8px] text-gray-450 uppercase tracking-wider font-semibold block mt-0.5">Saved</span>
              </div>
            </div>
          </div>

          <!-- Quick Tip Widget -->
          <div class="p-3.5 bg-brand-primary/5 border border-brand-primary/15 rounded-2xl text-left space-y-1.5">
            <p class="text-[9px] font-bold text-brand-primary uppercase tracking-widest flex items-center space-x-1">
              <Sparkles class="w-3 h-3 text-brand-primary" />
              <span>Enrollment Tip</span>
            </p>
            <p class="text-[10px] text-gray-400 leading-normal font-light">
              Click bookmark on any approved course card to add it to your wishlist tab inside the main Dashboard.
            </p>
          </div>

          <!-- Reset Filter Button (Visible when filters are active) -->
          <button 
            v-if="selectedCategory !== 'All' || selectedDifficulty !== 'All' || searchQuery !== ''"
            @click="resetFilters"
            class="w-full text-center py-2.5 bg-brand-danger/10 border border-brand-danger/20 text-brand-danger hover:bg-brand-danger/20 transition-all font-semibold text-xs rounded-xl flex items-center justify-center space-x-1.5 cursor-pointer shadow-sm animate-fade-in"
          >
            <SlidersHorizontal class="w-3.5 h-3.5" />
            <span>Reset Browse Filters</span>
          </button>
        </div>
      </aside>

      <!-- Right Column: Course Catalog Grid -->
      <main class="lg:col-span-3 space-y-6">
        <!-- Content section header -->
        <div class="flex items-center justify-between border-b border-white/5 pb-3">
          <div class="flex items-center space-x-2">
            <BookOpen class="w-5 h-5 text-brand-primary" />
            <h2 class="text-sm font-bold text-white font-display uppercase tracking-wider">Approved Programs Catalog</h2>
          </div>
          
          <span class="px-3 py-1 bg-brand-primary/10 border border-brand-primary/20 text-brand-primary text-[10px] font-bold rounded-lg uppercase tracking-wider shadow-inner">
            {{ filteredAndSortedCourses.length }} Matches
          </span>
        </div>

        <!-- Staggered Courses Grid Layout -->
        <div v-if="filteredAndSortedCourses.length > 0" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <div 
            v-for="(course, idx) in filteredAndSortedCourses" 
            :key="course.id"
            class="animate-fade-in"
            :style="{ 'animation-delay': `${idx * 0.05}s` }"
          >
            <CourseCard :course="course" />
          </div>
        </div>

        <!-- Empty search fallback state -->
        <div 
          v-else 
          class="glass-panel rounded-3xl p-12 text-center border border-white/5 flex flex-col items-center justify-center space-y-4 shadow-2xl bg-brand-card/45 animate-fade-in max-w-lg mx-auto"
        >
          <div class="p-4 rounded-full bg-brand-warning/10 text-brand-warning border border-brand-warning/20 shadow-inner">
            <AlertCircle class="w-8 h-8" />
          </div>
          <div class="space-y-1.5">
            <h3 class="text-base font-bold text-white font-display">No Available Programs Found</h3>
            <p class="text-xs text-gray-400 leading-relaxed">
              We couldn't locate any approved programs matching your search queries or filter categories. Try revising your keywords or click below to reset filters.
            </p>
          </div>
          <button 
            @click="resetFilters" 
            class="bg-brand-primary hover:bg-brand-secondary text-white text-xs font-bold px-6 py-2.5 rounded-xl transition-all shadow-md shadow-brand-primary/10 hover:shadow-brand-primary/20 cursor-pointer"
          >
            Clear Search Criteria
          </button>
        </div>
      </main>
    </div>
  </div>
</template>
