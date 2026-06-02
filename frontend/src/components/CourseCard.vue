<script setup>
import { computed } from 'vue';
import { useAuthStore } from '../store/auth';
import { useCoursesStore } from '../store/courses';
import { Star, BookOpen, Clock, PlayCircle, CheckCircle, HelpCircle, Eye, Bookmark, Lock } from 'lucide-vue-next';

const props = defineProps({
  course: {
    type: Object,
    required: true
  }
});

const authStore = useAuthStore();
const coursesStore = useCoursesStore();

// Check if student is enrolled
const enrollment = computed(() => {
  if (!authStore.isAuthenticated || !authStore.isStudent) return null;
  return coursesStore.getEnrollment(authStore.currentUser.id, props.course.id);
});

// Check if bookmarked
const isBookmarked = computed(() => {
  if (!authStore.isAuthenticated || !authStore.isStudent) return false;
  return coursesStore.isBookmarked(authStore.currentUser.id, props.course.id);
});

const toggleBookmark = () => {
  if (!authStore.isAuthenticated || !authStore.isStudent) return;
  coursesStore.toggleBookmark(authStore.currentUser.id, props.course.id);
};

// Computed badge styles for status
const statusBadgeClass = computed(() => {
  if (props.course.status === 'approved') return 'bg-brand-accent/10 text-brand-accent border-brand-accent/20';
  if (props.course.status === 'pending') return 'bg-brand-warning/10 text-brand-warning border-brand-warning/20';
  return 'bg-brand-danger/10 text-brand-danger border-brand-danger/20';
});
</script>

<template>
  <div class="glass-panel rounded-2xl overflow-hidden hover:translate-y-[-6px] transition-all duration-300 group flex flex-col h-full bg-brand-card hover:bg-brand-card-hover border border-white/5 hover:border-white/10 hover:shadow-xl hover:shadow-brand-primary/5">
    <!-- Thumbnail & Badges -->
    <div class="relative aspect-video w-full overflow-hidden bg-slate-800">
      <img 
        :src="course.thumbnail" 
        :alt="course.title" 
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        loading="lazy"
      />
      <!-- Category & Difficulty badges -->
      <div class="absolute top-3.5 left-3.5 flex flex-col gap-1.5 z-10">
        <span class="px-2.5 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider bg-brand-primary text-white backdrop-blur-md shadow-sm">
          {{ course.category }}
        </span>
        <span class="px-2.5 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider bg-brand-dark/85 text-gray-250 backdrop-blur-md border border-white/5">
          {{ course.difficulty }}
        </span>
      </div>
      
      <!-- Overlay Play Button for Enrolled Course -->
      <div 
        v-if="enrollment"
        class="absolute inset-0 bg-brand-dark/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300"
      >
        <PlayCircle class="w-12 h-12 text-white drop-shadow-md" />
      </div>
    </div>

    <!-- Info Content -->
    <div class="p-5 flex-grow flex flex-col">
      <!-- Author, Bookmark & Rating Row -->
      <div class="flex items-center justify-between text-xs text-gray-400 mb-2">
        <div class="flex items-center space-x-1.5 truncate">
          <span class="font-medium truncate max-w-[100px]">By {{ course.teacherName }}</span>
          <!-- Bookmark Button -->
          <button 
            v-if="authStore.isAuthenticated && authStore.isStudent"
            @click.stop.prevent="toggleBookmark"
            class="text-gray-450 hover:text-brand-primary transition-colors cursor-pointer p-0.5 rounded hover:bg-white/5"
            title="Bookmark Course"
          >
            <Bookmark class="w-3.5 h-3.5" :class="{'text-brand-primary fill-brand-primary': isBookmarked}" />
          </button>
        </div>

        <div class="flex items-center space-x-1 shrink-0">
          <Star class="w-3.5 h-3.5 text-brand-warning fill-brand-warning" />
          <span class="font-semibold text-gray-250">{{ coursesStore.getCourseRating(course.id).toFixed(1) }}</span>
          <span class="text-gray-500">({{ coursesStore.getCourseReviewsCount(course.id) }})</span>
        </div>
      </div>

      <!-- Title & Description -->
      <h3 class="text-base font-bold text-white group-hover:text-brand-primary transition-colors line-clamp-1 mb-2 font-display">
        {{ course.title }}
      </h3>
      <p class="text-xs text-gray-400 line-clamp-2 leading-relaxed mb-4 flex-grow">
        {{ course.shortDescription || course.description }}
      </p>

      <!-- Student Enrollment Progress Tracker -->
      <div v-if="enrollment" class="mb-4">
        <div class="flex items-center justify-between text-[11px] font-semibold text-gray-300 mb-1.5">
          <span class="flex items-center space-x-1">
            <CheckCircle v-if="enrollment.progressPercent === 100" class="w-3.5 h-3.5 text-brand-accent" />
            <span>{{ enrollment.progressPercent === 100 ? 'Completed' : 'Learning Progress' }}</span>
          </span>
          <span class="text-brand-accent">{{ enrollment.progressPercent }}%</span>
        </div>
        <div class="w-full bg-brand-dark rounded-full h-1.5 overflow-hidden">
          <div 
            class="bg-gradient-to-r from-brand-primary to-brand-accent h-full transition-all duration-500"
            :style="{ width: `${enrollment.progressPercent}%` }"
          ></div>
        </div>
      </div>

      <!-- Footer Course Meta -->
      <div class="flex items-center justify-between pt-4 border-t border-white/5 text-[11px] text-gray-400 mt-auto shrink-0">
        <div class="flex items-center space-x-3">
          <span class="flex items-center space-x-1">
            <Clock class="w-3.5 h-3.5 text-brand-primary" />
            <span>{{ course.duration || '4 Hours' }}</span>
          </span>
          <span class="flex items-center space-x-1">
            <BookOpen class="w-3.5 h-3.5 text-brand-accent" />
            <span>{{ course.modules.length }} modules</span>
          </span>
        </div>

        <!-- Custom Status indicator (Admin/Teacher view only) -->
        <span 
          v-if="authStore.isAuthenticated && (authStore.isAdmin || (authStore.isTeacher && course.teacherId === authStore.currentUser.id))"
          class="px-2.5 py-0.5 rounded-full border text-[9px] font-bold uppercase tracking-wider shrink-0"
          :class="statusBadgeClass"
        >
          {{ course.status }}
        </span>
      </div>

      <!-- Action Button Row -->
      <div class="mt-4.5 pt-0 shrink-0">
        <!-- Guest View Details (Redirect to Login) -->
        <router-link 
          v-if="!authStore.isAuthenticated" 
          :to="`/login?redirect=/courses/${course.id}`" 
          class="w-full text-center flex items-center justify-center space-x-2 py-2 rounded-xl text-xs font-semibold bg-brand-primary/10 hover:bg-brand-primary/20 text-brand-primary transition-all duration-300 border border-brand-primary/20"
        >
          <Lock class="w-3.5 h-3.5 animate-pulse" />
          <span>Login to View Details</span>
        </router-link>

        <!-- Student Views -->
        <template v-else-if="authStore.isStudent">
          <router-link 
            v-if="enrollment" 
            :to="`/student/player/${course.id}`" 
            class="w-full text-center flex items-center justify-center space-x-2 py-2 rounded-xl text-xs font-semibold bg-gradient-to-r from-brand-primary to-brand-secondary text-white hover:opacity-90 transition-opacity glow-btn"
          >
            <PlayCircle class="w-4 h-4" />
            <span>{{ enrollment.progressPercent === 100 ? 'View Certificate & Modules' : 'Continue Learning' }}</span>
          </router-link>

          <router-link 
            v-else 
            :to="`/courses/${course.id}`" 
            class="w-full text-center flex items-center justify-center space-x-2 py-2 rounded-xl text-xs font-semibold bg-white/5 hover:bg-white/10 text-white transition-colors border border-white/5 hover:border-white/10"
          >
            <span>Learn More & Enroll</span>
          </router-link>
        </template>

        <!-- Teacher / Admin view controls -->
        <template v-else>
          <router-link 
            v-if="authStore.isAdmin && course.status === 'pending'" 
            to="/admin/approvals" 
            class="w-full text-center flex items-center justify-center space-x-2 py-2 rounded-xl text-xs font-semibold bg-brand-warning/20 text-brand-warning hover:bg-brand-warning/30 transition-colors border border-brand-warning/25"
          >
            <HelpCircle class="w-4 h-4" />
            <span>Review Course</span>
          </router-link>
          
          <router-link 
            v-else 
            :to="`/courses/${course.id}`" 
            class="w-full text-center flex items-center justify-center space-x-2 py-2 rounded-xl text-xs font-semibold bg-white/5 hover:bg-white/10 text-white transition-colors border border-white/5"
          >
            <Eye class="w-4 h-4" />
            <span>Inspect Course Page</span>
          </router-link>
        </template>
      </div>
    </div>
  </div>
</template>
