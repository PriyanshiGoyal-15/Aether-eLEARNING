<script setup>
import { ref, computed } from 'vue';
import { useCoursesStore } from '../../store/courses';
import { useRouter } from 'vue-router';
import { 
  ArrowLeft, ClipboardCheck, Check, X, BookOpen, 
  ChevronDown, ChevronUp, AlertCircle, MessageSquare
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const router = useRouter();

// Pending course listings
const pendingCourses = computed(() => coursesStore.pendingCourses);

// Inspection Accordion
const expandedCourses = ref({});

const toggleInspection = (courseId) => {
  expandedCourses.value[courseId] = !expandedCourses.value[courseId];
};

// Rejection handling state
const rejectingCourseId = ref(null);
const rejectionReasonText = ref('');

const initiateRejection = (courseId) => {
  rejectingCourseId.value = courseId;
  rejectionReasonText.value = '';
};

const cancelRejection = () => {
  rejectingCourseId.value = null;
  rejectionReasonText.value = '';
};

const handleApproval = async (courseId) => {
  try {
    await coursesStore.approveCourse(courseId);
    alert("Course approved! It is now visible to all students in the public catalog.");
  } catch (err) {
    console.error(err);
    alert(err.message || "Failed to approve course.");
  }
};

const handleRejection = async (courseId) => {
  if (!rejectionReasonText.value) {
    alert("Please provide a rejection reason so the instructor knows what to edit.");
    return;
  }
  
  try {
    await coursesStore.rejectCourse(courseId, rejectionReasonText.value);
    alert("Course rejected and returned to the instructor's draft dashboard.");
    rejectingCourseId.value = null;
    rejectionReasonText.value = '';
  } catch (err) {
    console.error(err);
    alert(err.message || "Failed to reject course.");
  }
};
</script>

<template>
  <div class="space-y-8 py-4">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <button 
        @click="router.push('/admin/dashboard')" 
        class="flex items-center space-x-2 text-sm text-gray-400 hover:text-white transition-colors"
      >
        <ArrowLeft class="w-4 h-4" />
        <span>Back to Portal</span>
      </button>
    </div>

    <!-- Title -->
    <div class="space-y-1">
      <h1 class="text-xl md:text-2xl font-extrabold text-white font-display flex items-center space-x-2">
        <ClipboardCheck class="w-5.5 h-5.5 text-brand-primary" />
        <span>Course Approvals Moderation</span>
      </h1>
      <p class="text-xs text-gray-450">Review teacher uploads, inspect syllabi, and resolve listing status permissions.</p>
    </div>

    <!-- Pending Queue list -->
    <div v-if="pendingCourses.length > 0" class="space-y-6">
      <div 
        v-for="course in pendingCourses" 
        :key="course.id"
        class="glass-panel rounded-3xl overflow-hidden border border-white/5 bg-brand-card shadow-2xl flex flex-col"
      >
        <!-- Course Basic info grid -->
        <div class="p-6 grid grid-cols-1 md:grid-cols-4 gap-6 items-start">
          <!-- Thumbnail -->
          <div class="aspect-video w-full rounded-2xl overflow-hidden bg-slate-800 shrink-0 shadow">
            <img :src="course.thumbnail" :alt="course.title" class="w-full h-full object-cover" />
          </div>

          <!-- Metadata details -->
          <div class="md:col-span-2 space-y-2">
            <div class="flex items-center space-x-2">
              <span class="px-2 py-0.5 text-[9px] font-bold uppercase bg-brand-warning/15 text-brand-warning rounded border border-brand-warning/20">
                Pending Approval
              </span>
              <span class="px-2 py-0.5 text-[9px] font-semibold bg-white/5 text-gray-400 rounded">
                {{ course.category }}
              </span>
            </div>
            
            <h3 class="text-base font-bold text-white font-display leading-snug">{{ course.title }}</h3>
            <p class="text-[11px] text-gray-405 leading-relaxed">{{ course.description }}</p>
            <p class="text-[10px] text-gray-500 font-medium">Instructor: <strong>{{ course.teacherName }}</strong> &bull; Level: {{ course.difficulty }}</p>
          </div>

          <!-- Decision Action items -->
          <div class="flex flex-col gap-2 w-full pt-2 md:pt-0">
            <button 
              @click="handleApproval(course.id)"
              class="w-full py-2 bg-brand-accent hover:bg-emerald-600 text-white text-xs font-bold rounded-xl transition-all shadow-md shadow-brand-accent/10 flex items-center justify-center space-x-1"
            >
              <Check class="w-4 h-4" />
              <span>Approve Program</span>
            </button>

            <button 
              v-if="rejectingCourseId !== course.id"
              @click="initiateRejection(course.id)"
              class="w-full py-2 bg-brand-danger/10 hover:bg-brand-danger/20 text-brand-danger border border-brand-danger/25 text-xs font-bold rounded-xl transition-all flex items-center justify-center space-x-1"
            >
              <X class="w-4 h-4" />
              <span>Reject Program</span>
            </button>
          </div>
        </div>

        <!-- Inline Rejection Form Drawer -->
        <div 
          v-if="rejectingCourseId === course.id"
          class="px-6 pb-6 pt-2 border-t border-white/5 bg-brand-danger/[0.01] animate-fade-in space-y-3.5"
        >
          <div class="space-y-1">
            <label class="text-[11px] font-bold text-brand-danger uppercase tracking-wider block">Reason for Rejection</label>
            <p class="text-[10px] text-gray-400">Outline missing prerequisites, formatting errors, or broken attachment files.</p>
          </div>
          <div class="flex gap-3">
            <input 
              v-model="rejectionReasonText"
              type="text"
              placeholder="e.g. Broken attachments under Module 1. Add legible study guide PDFs."
              class="flex-grow pl-4 pr-4 py-2 bg-brand-dark/50 border border-brand-danger/25 text-xs text-white rounded-xl focus:outline-none focus:ring-1 focus:ring-brand-danger"
            />
            <button 
              @click="handleRejection(course.id)"
              class="px-5 py-2 rounded-xl text-xs font-bold bg-brand-danger text-white hover:opacity-95 transition-opacity"
            >
              Confirm Reject
            </button>
            <button 
              @click="cancelRejection"
              class="px-4.5 py-2 rounded-xl text-xs font-semibold bg-white/5 border border-white/10 text-gray-300 hover:text-white"
            >
              Cancel
            </button>
          </div>
        </div>

        <!-- Syllabi inspector trigger -->
        <div class="border-t border-white/5 bg-brand-dark/25 px-6 py-2.5">
          <button 
            @click="toggleInspection(course.id)"
            class="flex items-center space-x-1.5 text-xs font-bold text-gray-400 hover:text-white transition-colors"
          >
            <BookOpen class="w-4 h-4 text-brand-primary" />
            <span>Inspect Syllabus Curriculum</span>
            <ChevronDown v-if="!expandedCourses[course.id]" class="w-4 h-4" />
            <ChevronUp v-else class="w-4 h-4" />
          </button>
          
          <!-- Syllabus modules listing -->
          <div v-if="expandedCourses[course.id]" class="mt-4 pt-4 border-t border-white/5 space-y-4 animate-fade-in divide-y divide-white/5">
            <div 
              v-for="mod in course.modules" 
              :key="mod.id"
              class="pt-3 first:pt-0 text-[11px]"
            >
              <h4 class="font-bold text-white font-display mb-2">{{ mod.title }}</h4>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pl-4">
                <div 
                  v-for="lesson in mod.lessons" 
                  :key="lesson.id"
                  class="flex items-center space-x-2 text-gray-300"
                >
                  <Check class="w-3.5 h-3.5 text-brand-accent" />
                  <span class="truncate font-light">{{ lesson.title }} ({{ lesson.type }} - {{ lesson.duration }})</span>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Empty queue fallback state -->
    <div 
      v-else 
      class="glass-panel rounded-3xl p-16 text-center border border-white/5 flex flex-col items-center justify-center space-y-4 max-w-xl mx-auto"
    >
      <div class="p-4 bg-brand-accent/15 border border-brand-accent/25 rounded-full text-brand-accent animate-pulse">
        <ClipboardCheck class="w-8 h-8" />
      </div>
      <h3 class="text-base font-bold text-white">Queue Moderated</h3>
      <p class="text-xs text-gray-450 leading-relaxed">
        All pending course submissions are cleared. Approved listings are successfully populated in student course catalogs.
      </p>
      <router-link to="/admin/dashboard" class="inline-block bg-white/5 border border-white/10 hover:bg-white/10 px-5 py-2 rounded-xl text-xs font-semibold text-white transition-colors">
        Return to Analytics
      </router-link>
    </div>
  </div>
</template>
