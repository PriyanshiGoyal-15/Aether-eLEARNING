<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import { useNotificationStore } from '../../store/notifications';
import { 
  ArrowLeft, CheckSquare, Square, PlayCircle, FileText, 
  ChevronDown, ChevronUp, Check, Award, Video, Download, HelpCircle,
  Edit3, Trash2, GraduationCap, Mic, MicOff, Star
} from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();
const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const notifStore = useNotificationStore();

const courseId = route.params.courseId;
const studentId = computed(() => authStore.currentUser?.id);

const course = computed(() => coursesStore.courses.find(c => c.id === courseId));
const enrollment = computed(() => coursesStore.getEnrollment(studentId.value, courseId));

// Currently active lesson
const activeLesson = ref(null);
const expandedModules = ref({});

// Review Form States for Completed Courses
const newRating = ref(5);
const hoverRating = ref(0);
const newComment = ref('');
const isSubmittingReview = ref(false);

const hasSubmittedReview = computed(() => {
  if (!authStore.currentUser?.name) return false;
  return coursesStore.reviews.some(
    r => r.courseId === courseId && r.studentName === authStore.currentUser.name
  );
});

const submitCourseReview = async () => {
  if (!newComment.value.trim()) {
    notifStore.showToast("Incomplete Review", "Please write a comment for your review.", "warning");
    return;
  }
  isSubmittingReview.value = true;
  try {
    await coursesStore.submitReview(
      courseId,
      authStore.currentUser.name,
      newRating.value,
      newComment.value.trim()
    );
    newComment.value = '';
    notifStore.showToast("Review Submitted! ⭐", "Thank you for sharing your feedback with the community!", "success");
  } catch (err) {
    notifStore.showToast("Error", err.message || "Failed to submit review.", "danger");
  } finally {
    isSubmittingReview.value = false;
  }
};

const toggleModule = (moduleId) => {
  expandedModules.value[moduleId] = !expandedModules.value[moduleId];
};

// Check if a lesson is completed
const isLessonCompleted = (lessonId) => {
  if (!enrollment.value) return false;
  return enrollment.value.completedLessons.includes(lessonId);
};

const handleLessonToggle = (lessonId) => {
  if (!enrollment.value) return;
  coursesStore.toggleLessonCompletion(studentId.value, courseId, lessonId);
};

const selectLesson = (lesson) => {
  activeLesson.value = lesson;
};

// Sidebar navigation console tabs: 'syllabus', 'aitutor', 'notepad'
const activeSidebarTab = ref('syllabus');

// 1. Notepad Workspace Logic
const notepadText = ref('');

const loadNotepadNotes = () => {
  if (!course.value || !activeLesson.value) {
    notepadText.value = '';
    return;
  }
  const cacheKey = `aether_notes_${course.value.id}_${activeLesson.value.id}`;
  notepadText.value = localStorage.getItem(cacheKey) || '';
};

const saveNotepadNotes = () => {
  if (!course.value || !activeLesson.value) return;
  const cacheKey = `aether_notes_${course.value.id}_${activeLesson.value.id}`;
  localStorage.setItem(cacheKey, notepadText.value);
};

const clearNotepadNotes = () => {
  notepadText.value = '';
  saveNotepadNotes();
  notifStore.showToast("Notes Cleared", "The study notes for this lesson were emptied.", "info");
};

const exportNotesAsFile = () => {
  if (!notepadText.value.trim() || !course.value || !activeLesson.value) return;
  const blob = new Blob([notepadText.value], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  
  // Format clean file names
  const cleanCourse = course.value.title.replace(/[^a-zA-Z0-9]/g, '_');
  const cleanLesson = activeLesson.value.title.replace(/[^a-zA-Z0-9]/g, '_');
  link.download = `Aether_StudyNotes_${cleanCourse}_${cleanLesson}.txt`;
  
  link.click();
  URL.revokeObjectURL(url);
  notifStore.showToast("Notes Exported! 📝", "Successfully downloaded study notes as a text file.", "success");
};



// Sync Notepad notes on active lesson changes
watch(activeLesson, () => {
  loadNotepadNotes();
});

onMounted(() => {
  // If not enrolled, redirect home
  if (!enrollment.value && authStore.isStudent) {
    router.push(`/courses/${courseId}`);
    return;
  }

  // Pre-expand modules and select first lesson
  if (course.value) {
    course.value.modules.forEach((mod, idx) => {
      expandedModules.value[mod.id] = idx === 0; // expand first module by default
    });
    
    // Set first lesson active
    if (course.value.modules[0]?.lessons[0]) {
      activeLesson.value = course.value.modules[0].lessons[0];
      loadNotepadNotes(); // load initial notes
    }
  }
});
</script>

<template>
  <div v-if="course && enrollment" class="space-y-6 py-4">
    <!-- Back Button / Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <button 
        @click="router.push('/student/dashboard')" 
        class="flex items-center space-x-2 text-sm text-gray-400 hover:text-white transition-colors"
      >
        <ArrowLeft class="w-4 h-4" />
        <span>Exit Player to Dashboard</span>
      </button>

      <!-- Course title and percentage tracking -->
      <div class="flex items-center space-x-4">
        <div class="text-right hidden sm:block">
          <h4 class="text-xs font-bold text-white max-w-[240px] truncate">{{ course.title }}</h4>
          <p class="text-[10px] text-brand-accent font-semibold">{{ enrollment.progressPercent }}% Syllabus Finished</p>
        </div>
        
        <div class="w-24 bg-brand-dark rounded-full h-2 overflow-hidden border border-white/5 shrink-0">
          <div 
            class="bg-gradient-to-r from-brand-primary to-brand-accent h-full transition-all duration-300"
            :style="{ width: `${enrollment.progressPercent}%` }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Celebration Certificate alert -->
    <div 
      v-if="enrollment.progressPercent === 100" 
      class="glass-panel p-4.5 rounded-2xl border border-brand-accent/20 bg-brand-accent/10 flex flex-col sm:flex-row items-center justify-between gap-4 animate-fade-in text-center sm:text-left"
    >
      <div class="flex flex-col sm:flex-row items-center gap-3.5">
        <span class="p-3 bg-brand-accent text-white rounded-xl shadow-lg shadow-brand-accent/15">
          <Award class="w-6 h-6 animate-pulse" />
        </span>
        <div class="space-y-0.5">
          <h3 class="text-sm font-bold text-white font-display">Congratulations! You finished the program!</h3>
          <p class="text-xs text-gray-300">Your verified certificate of completion is generated and ready to download.</p>
        </div>
      </div>
      <button 
        @click="router.push('/student/dashboard')"
        class="px-5 py-2 rounded-xl text-xs font-bold bg-brand-accent text-white hover:bg-emerald-600 transition-all shadow-md shrink-0"
      >
        Go claim Certificate
      </button>
    </div>

    <!-- Course Review Widget -->
    <div 
      v-if="enrollment.progressPercent === 100 && !hasSubmittedReview" 
      class="glass-panel p-6 rounded-2xl border border-white/5 bg-brand-card/65 shadow-xl space-y-4 animate-fade-in"
    >
      <div class="flex items-center space-x-2">
        <Star class="w-5 h-5 text-brand-primary animate-pulse fill-brand-primary/20" />
        <h3 class="text-sm font-bold text-white font-display">Share Your Experience</h3>
      </div>
      <p class="text-xs text-gray-400 font-light leading-relaxed">
        You've completed the program! How did you like the instructor and the syllabus? Let the community know.
      </p>

      <div class="flex flex-col md:flex-row md:items-center gap-4">
        <!-- Interactive Star Rating -->
        <div class="flex items-center space-x-1 border border-white/5 bg-brand-dark/40 px-3 py-2 rounded-xl">
          <button 
            v-for="star in 5" 
            :key="star" 
            type="button"
            @click="newRating = star"
            @mouseenter="hoverRating = star"
            @mouseleave="hoverRating = 0"
            class="focus:outline-none transition-transform hover:scale-115 shrink-0"
          >
            <Star 
              class="w-5 h-5 cursor-pointer transition-colors" 
              :class="star <= (hoverRating || newRating) ? 'text-brand-primary fill-brand-primary' : 'text-gray-600'" 
            />
          </button>
        </div>
        <span class="text-[10px] font-bold text-brand-primary uppercase tracking-widest bg-brand-primary/10 border border-brand-primary/20 px-3 py-2.5 rounded-xl shrink-0">
          {{ newRating === 5 ? 'Excellent ⭐⭐⭐⭐⭐' : newRating === 4 ? 'Great ⭐⭐⭐⭐' : newRating === 3 ? 'Good ⭐⭐⭐' : newRating === 2 ? 'Fair ⭐⭐' : 'Poor ⭐' }}
        </span>
      </div>

      <!-- Comment Textbox -->
      <div class="space-y-2.5">
        <textarea 
          v-model="newComment"
          rows="2"
          placeholder="What was your favorite part of the course? Share your feedback..."
          class="w-full p-3.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-1 focus:ring-brand-primary placeholder-gray-550 leading-relaxed resize-none"
        ></textarea>
        
        <div class="flex justify-end">
          <button 
            @click="submitCourseReview"
            :disabled="isSubmittingReview || !newComment.trim()"
            class="px-5 py-2.5 rounded-xl text-xs font-bold bg-brand-primary hover:bg-brand-secondary text-white transition-all shadow-md shadow-brand-primary/10 disabled:opacity-55 disabled:cursor-not-allowed flex items-center space-x-1.5 cursor-pointer"
          >
            <span>{{ isSubmittingReview ? 'Submitting...' : 'Submit Review' }}</span>
            <Check class="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>

    <!-- Review Confirmation state -->
    <div 
      v-else-if="enrollment.progressPercent === 100 && hasSubmittedReview" 
      class="glass-panel p-4.5 rounded-2xl border border-brand-accent/10 bg-brand-accent/5 flex items-center space-x-3 animate-fade-in"
    >
      <Check class="w-5 h-5 text-brand-accent shrink-0" />
      <p class="text-xs text-gray-350">
        Thank you! Your verified course review has been successfully registered and is now live on the platform.
      </p>
    </div>

    <!-- Main Workspace Player Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
      
      <!-- Left Column (Active Lecture & Viewer) -->
      <div class="lg:col-span-2 space-y-5">
        <!-- Main Media Shell -->
        <div class="glass-panel rounded-3xl overflow-hidden border border-white/5 bg-brand-card shadow-2xl relative">
          <!-- Active Lesson is Video -->
          <div v-if="activeLesson && activeLesson.type === 'video'" class="aspect-video w-full bg-black relative">
            <video 
              :src="activeLesson.url" 
              controls 
              class="w-full h-full object-contain"
            ></video>
          </div>

          <!-- Active Lesson is PDF -->
          <div v-else-if="activeLesson && activeLesson.type === 'pdf'" class="aspect-video w-full bg-brand-dark/60 flex flex-col items-center justify-center p-8 text-center space-y-4">
            <div class="p-4 bg-brand-accent/10 border border-brand-accent/20 rounded-2xl text-brand-accent">
              <FileText class="w-12 h-12" />
            </div>
            <div class="space-y-1">
              <h3 class="text-sm font-bold text-white font-display">{{ activeLesson.title }}</h3>
              <p class="text-xs text-gray-400">PDF Guide Attachment Available</p>
            </div>
            <a 
              :href="activeLesson.url" 
              target="_blank" 
              class="bg-brand-accent text-white px-5 py-2.5 rounded-xl text-xs font-semibold hover:bg-emerald-600 transition-all flex items-center space-x-1.5 shadow-md shadow-brand-accent/10"
            >
              <Download class="w-4 h-4" />
              <span>Open PDF in Tab</span>
            </a>
          </div>

          <!-- Title Bar and Status toggle -->
          <div v-if="activeLesson" class="p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-t border-white/5">
            <div class="space-y-1">
              <span class="px-2 py-0.5 text-[9px] font-bold uppercase tracking-wider bg-white/5 border border-white/5 rounded-md text-gray-400">
                Active Lecture
              </span>
              <h2 class="text-base font-bold text-white font-display leading-snug">{{ activeLesson.title }}</h2>
              <p class="text-xs text-gray-400 flex items-center space-x-1">
                <Video v-if="activeLesson.type === 'video'" class="w-3.5 h-3.5 text-brand-primary" />
                <FileText v-else class="w-3.5 h-3.5 text-brand-accent" />
                <span>{{ activeLesson.type === 'video' ? 'Video Lecture' : 'PDF Study Guide' }} &bull; {{ activeLesson.duration }}</span>
              </p>
            </div>

            <!-- Complete Toggle -->
            <button 
              @click="handleLessonToggle(activeLesson.id)"
              class="flex items-center space-x-2 px-4.5 py-2.5 rounded-xl text-xs font-bold border transition-all shrink-0"
              :class="isLessonCompleted(activeLesson.id)
                ? 'bg-brand-accent/20 text-brand-accent border-brand-accent/30 hover:bg-brand-accent/15'
                : 'bg-brand-primary text-white border-transparent hover:bg-brand-secondary'"
            >
              <Check class="w-4 h-4" />
              <span>{{ isLessonCompleted(activeLesson.id) ? 'Completed!' : 'Mark as Completed' }}</span>
            </button>
          </div>
        </div>

        <!-- Course FAQs / Lecture Overview mockup -->
        <div class="glass-panel p-6 rounded-3xl border border-white/5 bg-brand-card space-y-4">
          <h3 class="text-xs font-bold text-white uppercase tracking-wider">About this Lecture</h3>
          <p class="text-xs text-gray-400 leading-relaxed font-light">
            Use the right-side syllabus panel to skip between video modules. If there is a PDF attachment, open the PDF reader to study reference materials. You must check each item's checkbox to build up your platform completion score.
          </p>
        </div>
      </div>

      <!-- Right Column (Syllabus, AI Tutor, Notepad Sidebar console) -->
      <div class="glass-panel rounded-3xl p-5 border border-white/5 bg-brand-card shadow-2xl space-y-4 h-[600px] flex flex-col justify-start overflow-hidden">
        
        <!-- Interactive Sidebar console Switcher Tabs -->
        <div class="flex items-center space-x-3 border-b border-white/5 pb-2 shrink-0">
          <button 
            @click="activeSidebarTab = 'syllabus'"
            class="px-2 py-1.5 text-[10px] font-bold uppercase tracking-wider border-b-2 transition-all flex items-center space-x-1 cursor-pointer"
            :class="activeSidebarTab === 'syllabus' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
          >
            <GraduationCap class="w-3.5 h-3.5" />
            <span>Syllabus</span>
          </button>
          
          <button 
            @click="activeSidebarTab = 'notepad'"
            class="px-2 py-1.5 text-[10px] font-bold uppercase tracking-wider border-b-2 transition-all flex items-center space-x-1 cursor-pointer"
            :class="activeSidebarTab === 'notepad' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
          >
            <Edit3 class="w-3.5 h-3.5" />
            <span>Notepad</span>
          </button>
        </div>

        <!-- TAB CONTENT AREA (Uses flex-grow overflow-y-auto to allow independent scrolling) -->
        <div class="flex-grow overflow-y-auto space-y-4 pr-1">
          
          <!-- 1. SYLLABUS TAB -->
          <div v-if="activeSidebarTab === 'syllabus'" class="space-y-3">
            <div 
              v-for="mod in course.modules" 
              :key="mod.id"
              class="glass-panel rounded-2xl overflow-hidden border border-white/5 bg-brand-card/45"
            >
              <!-- Module accordion Header -->
              <button 
                @click="toggleModule(mod.id)"
                class="w-full flex items-center justify-between px-4 py-3 hover:bg-white/5 transition-colors text-left"
              >
                <span class="text-xs font-bold text-white font-display line-clamp-1 pr-2">{{ mod.title }}</span>
                <ChevronDown v-if="!expandedModules[mod.id]" class="w-4 h-4 text-gray-500 shrink-0" />
                <ChevronUp v-else class="w-4 h-4 text-gray-500 shrink-0" />
              </button>

              <!-- Lessons checklist -->
              <div v-if="expandedModules[mod.id]" class="border-t border-white/5 divide-y divide-white/5 bg-brand-dark/20">
                <div 
                  v-for="lesson in mod.lessons" 
                  :key="lesson.id"
                  class="flex items-center px-4 py-2.5 hover:bg-white/5 transition-colors text-[10px]"
                  :class="{'bg-brand-primary/5': activeLesson?.id === lesson.id}"
                >
                  <!-- Checkbox click toggles completion -->
                  <button 
                    @click="handleLessonToggle(lesson.id)"
                    class="p-0.5 mr-2 text-gray-400 hover:text-white transition-colors shrink-0"
                  >
                    <CheckSquare v-if="isLessonCompleted(lesson.id)" class="w-4 h-4 text-brand-accent" />
                    <Square v-else class="w-4 h-4 text-gray-500" />
                  </button>

                  <!-- Lesson selector triggers active player selection -->
                  <div 
                    @click="selectLesson(lesson)"
                    class="flex-grow flex items-center justify-between cursor-pointer truncate"
                  >
                    <div class="flex items-center space-x-1.5 truncate">
                      <PlayCircle v-if="lesson.type === 'video'" class="w-3.5 h-3.5 text-brand-primary shrink-0" />
                      <FileText v-else class="w-3.5 h-3.5 text-brand-accent shrink-0" />
                      <span 
                        class="truncate transition-colors"
                        :class="activeLesson?.id === lesson.id ? 'text-brand-primary font-bold' : 'text-gray-300 hover:text-white'"
                      >
                        {{ lesson.title }}
                      </span>
                    </div>
                    <span class="text-[8px] text-gray-500 font-semibold shrink-0 ml-2">{{ lesson.duration }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 2. NOTEPAD TAB -->
          <div v-else-if="activeSidebarTab === 'notepad'" class="flex flex-col h-full space-y-3">
            <div class="flex items-center justify-between shrink-0">
              <span class="text-[9px] font-bold text-gray-400 uppercase tracking-widest flex items-center space-x-1">
                <Edit3 class="w-3.5 h-3.5 text-brand-accent" />
                <span>Lecture Notepad</span>
              </span>
              <div class="flex space-x-1.5 items-center">
                <!-- Voice Recorder Button -->
                <!-- <button 
                  @click="toggleVoiceRecording"
                  :title="isRecordingNotes ? 'Stop Voice Recording' : 'Dictate Notes by Voice'"
                  class="p-1.5 rounded-lg border transition-all cursor-pointer flex items-center justify-center"
                  :class="isRecordingNotes
                    ? 'bg-brand-danger/25 border-brand-danger/35 text-brand-danger animate-pulse scale-105'
                    : 'bg-white/5 border-white/10 hover:bg-brand-primary/10 hover:border-brand-primary/20 text-gray-400 hover:text-brand-primary'"
                >
                  <MicOff v-if="isRecordingNotes" class="w-3.5 h-3.5" />
                  <Mic v-else class="w-3.5 h-3.5" />
                </button> -->

                <button 
                  @click="clearNotepadNotes"
                  title="Clear Notes"
                  class="p-1.5 bg-white/5 hover:bg-red-500/10 border border-white/10 hover:border-red-500/20 text-gray-400 hover:text-red-400 rounded-lg cursor-pointer transition-colors"
                >
                  <Trash2 class="w-3.5 h-3.5" />
                </button>
                <button 
                  @click="exportNotesAsFile"
                  :disabled="!notepadText.trim()"
                  title="Export (.txt)"
                  class="p-1.5 bg-brand-accent/15 border border-brand-accent/25 hover:bg-brand-accent text-white rounded-lg cursor-pointer transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <Download class="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            <!-- Notes typing area -->
            <textarea
              v-model="notepadText"
              @input="saveNotepadNotes"
              placeholder="Write your study notes and summaries for this lecture. Autosaves dynamically scoped to this lesson!"
              class="flex-grow w-full h-[360px] p-3.5 bg-brand-dark/40 border border-white/10 text-gray-250 placeholder-gray-550 text-[10px] rounded-2xl focus:outline-none focus:ring-1 focus:ring-brand-accent leading-relaxed resize-none shadow-inner"
            ></textarea>
            
            <p class="text-[8px] text-gray-500 font-semibold tracking-wider text-center pt-1 shrink-0">
              Notes are persistent and automatically saved in your browser storage.
            </p>
          </div>

        </div>
      </div>

    </div>
  </div>
  
  <div v-else class="text-center py-24 glass-panel max-w-xl mx-auto rounded-3xl border border-white/5">
    <p class="text-xs text-gray-400">Verifying authorization protocols...</p>
  </div>
</template>
