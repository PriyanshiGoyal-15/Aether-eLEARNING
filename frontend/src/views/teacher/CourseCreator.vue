<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import { useRouter, useRoute } from 'vue-router';
import { 
  ArrowLeft, PlusCircle, Trash, Award, BookOpen, 
  Settings, Layers, CheckCircle, Video, FileText, Upload
} from 'lucide-vue-next';

import { useNotificationStore } from '../../store/notifications';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const notifStore = useNotificationStore();
const router = useRouter();
const route = useRoute();

const teacherId = computed(() => authStore.currentUser?.id);
const teacherName = computed(() => authStore.currentUser?.name);

// Route-based helper computed properties for Edit Mode
const courseId = computed(() => route.params.id);
const isEditMode = computed(() => !!courseId.value);

// Creator form state
const step = ref(1); // 1: Basic Info, 2: Module/Lesson Builder

const title = ref('');
const description = ref('');
const category = ref('Development');
const customCategory = ref('');
const difficulty = ref('Intermediate');
const thumbnail = ref('');
const isPaid = ref(false);
const price = ref(0);

const generateId = (prefix) => `${prefix}-${Math.random().toString(36).substr(2, 9)}`;

const learningOutcomes = ref([
  'Scaffold dynamic responsive layouts using Vue framework modules',
  'Understand responsive components, models, and data-flows'
]);

const addOutcome = () => {
  learningOutcomes.value.push('');
};

const removeOutcome = (idx) => {
  if (learningOutcomes.value.length === 1) {
    learningOutcomes.value[0] = '';
    return;
  }
  learningOutcomes.value.splice(idx, 1);
};

const modules = ref([
  {
    id: generateId('mod'),
    title: 'Module 1: Getting Started',
    lessons: [
      { id: generateId('les'), title: '1. Introduction to the Program', type: 'video', url: '', duration: '12:30' }
    ]
  }
]);

// Helper options
const categories = ['Development', 'Backend', 'Design', 'Data Science', 'Mobile Apps', 'Artificial Intelligence', 'Cybersecurity', 'Cloud Computing'];
const difficulties = ['Beginner', 'Intermediate', 'Advanced'];

onMounted(async () => {
  // Ensure courses data is loaded
  if (coursesStore.courses.length === 0) {
    await coursesStore.fetchCoursesData();
  }

  if (isEditMode.value) {
    const course = coursesStore.courses.find(c => c.id === courseId.value);
    if (course) {
      title.value = course.title || '';
      description.value = course.description || '';
      
      // Determine category selection
      if (categories.includes(course.category)) {
        category.value = course.category;
        customCategory.value = '';
      } else {
        category.value = 'Other';
        customCategory.value = course.category || '';
      }
      
      difficulty.value = course.difficulty || 'Intermediate';
      thumbnail.value = course.thumbnail || '';
      isPaid.value = !!(course.price && course.price > 0);
      price.value = course.price ? course.price / 100 : 0;
      
      // Learning outcomes deep copy
      if (course.learningOutcomes && course.learningOutcomes.length > 0) {
        learningOutcomes.value = [...course.learningOutcomes];
      } else {
        learningOutcomes.value = [''];
      }
      
      // Modules deep copy to avoid editing global state in place
      if (course.modules && course.modules.length > 0) {
        modules.value = JSON.parse(JSON.stringify(course.modules));
      }
    } else {
      notifStore.showToast("Course Not Found", "The requested course could not be found.", "danger");
      router.push('/teacher/dashboard');
    }
  }
});

const uploadThumbnail = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  try {
    notifStore.showToast("Uploading Image...", "Uploading thumbnail picture...", "info");
    const fileUrl = await coursesStore.uploadFile(file);
    thumbnail.value = fileUrl;
    notifStore.showToast("Image Uploaded! 🖼️", "Course thumbnail uploaded successfully!", "success");
  } catch (err) {
    console.error(err);
    notifStore.showToast("Upload Failed", err.message || "Failed to upload image.", "danger");
  }
};

const uploadLessonFile = async (e, modIdx, lesIdx) => {
  const file = e.target.files[0];
  if (!file) return;
  try {
    notifStore.showToast("Uploading Resource...", "Uploading lecture attachment to Aether secure storage...", "info");
    const fileUrl = await coursesStore.uploadFile(file);
    modules.value[modIdx].lessons[lesIdx].url = fileUrl;
    notifStore.showToast("Upload Complete! 📁", "File uploaded successfully!", "success");
  } catch (err) {
    console.error(err);
    notifStore.showToast("Upload Failed", err.message || "Failed to upload file.", "danger");
  }
};

const addModule = () => {
  modules.value.push({
    id: generateId('mod'),
    title: `Module ${modules.value.length + 1}: Title here`,
    lessons: [
      { id: generateId('les'), title: '1. First Lecture', type: 'video', url: '', duration: '10:00' }
    ]
  });
};

const removeModule = (modIdx) => {
  if (modules.value.length === 1) return;
  modules.value.splice(modIdx, 1);
};

const addLesson = (modIdx) => {
  const lessonNum = modules.value[modIdx].lessons.length + 1;
  modules.value[modIdx].lessons.push({
    id: generateId('les'),
    title: `${lessonNum}. New Lecture`,
    type: 'video',
    url: '',
    duration: '10:00'
  });
};

const removeLesson = (modIdx, lesIdx) => {
  if (modules.value[modIdx].lessons.length === 1) return;
  modules.value[modIdx].lessons.splice(lesIdx, 1);
};

const handleCreateCourse = async () => {
  if (!title.value || !description.value) {
    notifStore.showToast("Incomplete Details", "Please complete the basic course information before submitting!", "warning");
    return;
  }

  const finalCategory = category.value === 'Other' ? customCategory.value : category.value;
  if (!finalCategory) {
    notifStore.showToast("Incomplete Details", "Please specify a topic category for the syllabus!", "warning");
    return;
  }

  try {
    const finalPrice = isPaid.value && price.value > 0 ? Math.floor(price.value * 100) : 0;
    const finalOutcomes = learningOutcomes.value.filter(o => o.trim() !== '');

    if (isEditMode.value) {
      // Update course via store
      await coursesStore.updateCourse(
        courseId.value,
        teacherId.value,
        teacherName.value,
        title.value,
        description.value,
        finalCategory,
        difficulty.value,
        thumbnail.value,
        finalPrice,
        modules.value,
        finalOutcomes
      );

      notifStore.showToast("Course Updated! 🎓", `Course "${title.value}" updated successfully! It is now pending administrative review.`, "success");
    } else {
      // Create course via store
      await coursesStore.createCourse(
        teacherId.value,
        teacherName.value,
        title.value,
        description.value,
        finalCategory,
        difficulty.value,
        thumbnail.value,
        finalPrice,
        modules.value,
        finalOutcomes
      );

      notifStore.showToast("Course Proposed! 🎓", `Course "${title.value}" created successfully! It is now pending administrative approval.`, "success");
    }
    router.push('/teacher/dashboard');
  } catch (err) {
    console.error(err);
    notifStore.showToast(
      isEditMode.value ? "Error Updating Course" : "Error Creating Course",
      err.message || "Operation failed. Please try again.",
      "danger"
    );
  }
};
</script>

<template>
  <div class="space-y-8 py-4 max-w-4xl mx-auto">
    <!-- Header row -->
    <div class="flex items-center justify-between">
      <button 
        @click="router.push('/teacher/dashboard')" 
        class="flex items-center space-x-2 text-sm text-gray-400 hover:text-white transition-colors"
      >
        <ArrowLeft class="w-4 h-4" />
        <span>Back to Portal</span>
      </button>

      <div class="flex items-center space-x-2 text-xs font-bold text-gray-500 uppercase tracking-widest">
        <span :class="{'text-brand-primary': step === 1}">1. Core Metadata</span>
        <span>&bull;</span>
        <span :class="{'text-brand-primary': step === 2}">2. Module Architectures</span>
      </div>
    </div>

    <!-- Main Wizard shell -->
    <div class="glass-panel rounded-3xl p-6 md:p-10 border border-white/5 bg-brand-card shadow-2xl space-y-6">
      
      <!-- Wizard Title -->
      <div class="space-y-1">
        <h1 class="text-xl md:text-2xl font-extrabold text-white font-display">{{ isEditMode ? 'Edit Existing Course' : 'Create a New Program' }}</h1>
        <p class="text-xs text-gray-400">Assemble modern lecture syllabi. Admin validation is required before launch.</p>
      </div>

      <!-- Step 1: Basic Info Form -->
      <div v-if="step === 1" class="space-y-6 animate-fade-in">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          <!-- Title -->
          <div class="space-y-1.5 md:col-span-2">
            <label for="title" class="text-xs font-semibold text-gray-400">Course Title</label>
            <input 
              v-model="title" 
              type="text" 
              id="title" 
              required 
              placeholder="e.g. Master Reactivity Paradigms" 
              class="w-full pl-4 pr-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
            />
          </div>

          <!-- Category -->
          <div class="space-y-1.5">
            <label for="category" class="text-xs font-semibold text-gray-400">Topic Category</label>
            <select 
              v-model="category" 
              id="category" 
              class="w-full px-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
            >
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
              <option value="Other">Other (Type custom category...)</option>
            </select>
            
            <div v-if="category === 'Other'" class="mt-2.5 space-y-1 animate-fade-in">
              <label for="customCategory" class="text-[10px] font-semibold text-brand-primary uppercase tracking-wider">Custom Category Name</label>
              <input 
                v-model="customCategory" 
                type="text" 
                id="customCategory" 
                required
                placeholder="e.g. Mobile Apps, Cloud Security" 
                class="w-full pl-4 pr-4 py-2 bg-brand-dark/50 border border-brand-primary text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 transition-all duration-300"
              />
            </div>
          </div>

          <!-- Difficulty -->
          <div class="space-y-1.5">
            <label for="difficulty" class="text-xs font-semibold text-gray-400">Syllabus Target Level</label>
            <select 
              v-model="difficulty" 
              id="difficulty" 
              class="w-full px-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
            >
              <option v-for="dif in difficulties" :key="dif" :value="dif">{{ dif }}</option>
            </select>
          </div>

          <!-- Pricing Config -->
          <div class="space-y-4 md:col-span-2 border border-white/10 rounded-xl p-4 bg-brand-dark/20">
            <div class="flex items-center space-x-3">
              <input 
                type="checkbox" 
                id="isPaid" 
                v-model="isPaid"
                class="w-4 h-4 rounded text-brand-primary focus:ring-brand-primary bg-brand-dark border-white/20"
              />
              <label for="isPaid" class="text-xs font-bold text-white">This is a Premium Course (Paid)</label>
            </div>
            
            <div v-if="isPaid" class="space-y-1.5 animate-fade-in pl-7 border-l-2 border-brand-primary/30 ml-2">
              <label for="price" class="text-xs font-semibold text-gray-400">Course Price (INR)</label>
              <div class="relative">
                <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 font-bold">₹</span>
                <input 
                  v-model.number="price" 
                  type="number" 
                  id="price" 
                  min="1"
                  placeholder="e.g. 499" 
                  class="w-full pl-8 pr-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
                />
              </div>
              <p class="text-[10px] text-brand-primary">You will earn 70% of this revenue per enrollment!</p>
            </div>
          </div>

          <!-- Thumbnail Image Upload -->
          <div class="space-y-2 md:col-span-2">
            <label for="thumbnail" class="text-xs font-semibold text-gray-400">Course Thumbnail Image</label>
            <div class="flex items-center space-x-3">
              <input 
                v-model="thumbnail" 
                type="url" 
                id="thumbnail" 
                placeholder="https://images.unsplash.com/photo-... or upload from laptop" 
                class="flex-grow pl-4 pr-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
              />
              <label class="shrink-0 cursor-pointer px-4.5 py-2.5 bg-brand-primary hover:bg-brand-secondary text-white text-xs font-bold rounded-xl transition-all shadow-md shadow-brand-primary/10 flex items-center space-x-1.5">
                <Upload class="w-3.5 h-3.5" />
                <span>Upload Photo</span>
                <input 
                  type="file" 
                  accept="image/*"
                  class="hidden" 
                  @change="uploadThumbnail"
                />
              </label>
            </div>
            <!-- Interactive live image preview -->
            <div v-if="thumbnail" class="mt-2 aspect-video w-48 rounded-xl overflow-hidden bg-brand-dark border border-white/10 shadow-md">
              <img :src="thumbnail" alt="Thumbnail Preview" class="w-full h-full object-cover" />
            </div>
            <p class="text-[10px] text-gray-550 leading-normal">Tip: Leave empty to auto-load a premium default tech design placeholder image.</p>
          </div>

          <!-- Learning outcomes builder -->
          <div class="space-y-2 md:col-span-2 border border-white/10 rounded-xl p-4 bg-brand-dark/20">
            <label class="text-xs font-bold text-white block">Define Learning Outcomes ("What you will learn")</label>
            <p class="text-[10px] text-gray-400 mb-2">List specific target skills and milestones for this syllabus.</p>
            
            <div class="space-y-2">
              <div 
                v-for="(outcome, idx) in learningOutcomes" 
                :key="idx" 
                class="flex items-center space-x-2 animate-fade-in"
              >
                <div class="w-5 h-5 rounded-full bg-brand-accent/20 text-brand-accent text-[10px] font-bold flex items-center justify-center shrink-0">
                  ✓
                </div>
                <input 
                  v-model="learningOutcomes[idx]" 
                  type="text" 
                  placeholder="e.g. Scaffold dynamic responsive layouts" 
                  class="flex-grow pl-3 pr-3 py-1.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-lg focus:outline-none focus:border-brand-primary"
                />
                <button 
                  type="button" 
                  @click="removeOutcome(idx)" 
                  class="text-gray-500 hover:text-brand-danger transition-colors shrink-0"
                >
                  <Trash class="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
            
            <button 
              type="button" 
              @click="addOutcome"
              class="flex items-center space-x-1 text-[10px] font-semibold text-brand-primary hover:text-brand-secondary transition-colors mt-2"
            >
              <PlusCircle class="w-3.5 h-3.5" />
              <span>Add Outcome bullet</span>
            </button>
          </div>

          <!-- Description -->
          <div class="space-y-1.5 md:col-span-2">
            <label for="description" class="text-xs font-semibold text-gray-400">Detailed Description</label>
            <textarea 
              v-model="description" 
              id="description" 
              rows="5" 
              required
              placeholder="What will students learn in this program? Outline target skills, requirements, and outcomes." 
              class="w-full pl-4 pr-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
            ></textarea>
          </div>
        </div>

        <!-- Next trigger button -->
        <div class="flex justify-end pt-4">
          <button 
            type="button" 
            @click="step = 2"
            class="px-6 py-2.5 bg-brand-primary text-white text-xs font-bold rounded-xl transition-all shadow-md shadow-brand-primary/10 flex items-center space-x-1.5 hover:bg-brand-secondary"
          >
            <span>Proceed to Modules</span>
            <Layers class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- Step 2: Module/Lesson Builder Form -->
      <div v-else-if="step === 2" class="space-y-8 animate-fade-in">
        
        <!-- Interactive modules list tree -->
        <div class="space-y-6">
          <div 
            v-for="(mod, modIdx) in modules" 
            :key="modIdx"
            class="p-5 border border-white/5 bg-brand-dark/20 rounded-2xl space-y-4"
          >
            <!-- Module Title header input -->
            <div class="flex items-center justify-between gap-4">
              <div class="flex items-center space-x-2.5 flex-grow">
                <BookOpen class="w-4 h-4 text-brand-primary shrink-0" />
                <input 
                  v-model="mod.title" 
                  type="text" 
                  required
                  placeholder="Module Header Title" 
                  class="bg-transparent border-b border-white/10 focus:border-brand-primary focus:outline-none text-xs font-bold text-white py-1 px-1 flex-grow"
                />
              </div>
              
              <!-- Remove module -->
              <button 
                type="button" 
                @click="removeModule(modIdx)" 
                class="p-1 text-gray-500 hover:text-brand-danger transition-colors shrink-0"
                v-if="modules.length > 1"
              >
                <Trash class="w-4 h-4" />
              </button>
            </div>

            <!-- Lessons nested container list -->
            <div class="space-y-3.5 pl-6 border-l border-white/5">
              <h5 class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-2">Lectures Checklist:</h5>
              
              <div 
                v-for="(lesson, lesIdx) in mod.lessons" 
                :key="lesIdx"
                class="flex flex-wrap items-center gap-3 bg-brand-card/45 p-3 rounded-xl border border-white/5 text-xs"
              >
                <!-- Lecture type selector (Video / PDF toggle) -->
                <div class="flex items-center space-x-1 border border-white/10 rounded-lg p-0.5 bg-brand-dark/60 shrink-0">
                  <button 
                    type="button"
                    @click="lesson.type = 'video'"
                    class="p-1 rounded text-xs transition-colors flex items-center justify-center"
                    :class="lesson.type === 'video' ? 'bg-brand-primary text-white' : 'text-gray-450 hover:text-white'"
                  >
                    <Video class="w-3.5 h-3.5" />
                  </button>
                  <button 
                    type="button"
                    @click="lesson.type = 'pdf'"
                    class="p-1 rounded text-xs transition-colors flex items-center justify-center"
                    :class="lesson.type === 'pdf' ? 'bg-brand-accent text-white' : 'text-gray-450 hover:text-white'"
                  >
                    <FileText class="w-3.5 h-3.5" />
                  </button>
                </div>

                <!-- Lecture title input -->
                <input 
                  v-model="lesson.title" 
                  type="text" 
                  required
                  placeholder="Lecture Title name" 
                  class="flex-grow pl-3 pr-3 py-1.5 bg-brand-dark/40 border border-white/5 text-xs text-white rounded-lg focus:outline-none focus:ring-1 focus:ring-brand-primary/50 focus:border-brand-primary transition-all min-w-[140px]"
                />

                <!-- Lecture source URL & upload trigger -->
                <div class="flex items-center space-x-2 flex-grow min-w-[200px]">
                  <input 
                    v-model="lesson.url" 
                    type="text" 
                    required
                    :placeholder="lesson.type === 'video' ? 'Video URL or upload video' : 'PDF URL or upload PDF'" 
                    class="flex-grow pl-3 pr-3 py-1.5 bg-brand-dark/40 border border-white/5 text-xs text-white rounded-lg focus:outline-none focus:ring-1 focus:ring-brand-primary/50 focus:border-brand-primary transition-all"
                  />
                  <!-- Upload file trigger -->
                  <label class="shrink-0 cursor-pointer p-1.5 bg-brand-dark/60 hover:bg-brand-primary/20 border border-white/10 rounded-lg text-gray-400 hover:text-white transition-all flex items-center justify-center space-x-1">
                    <Upload class="w-3.5 h-3.5" />
                    <span class="text-[9px] font-bold">Upload</span>
                    <input 
                      type="file" 
                      :accept="lesson.type === 'video' ? 'video/*' : 'application/pdf'"
                      class="hidden" 
                      @change="e => uploadLessonFile(e, modIdx, lesIdx)"
                    />
                  </label>
                </div>

                <!-- Duration -->
                <input 
                  v-model="lesson.duration" 
                  type="text" 
                  placeholder="Duration (e.g. 10:15 or Guide)" 
                  class="w-32 pl-3 pr-3 py-1.5 bg-brand-dark/40 border border-white/5 text-xs text-white rounded-lg focus:outline-none focus:ring-1 focus:ring-brand-primary/50 focus:border-brand-primary transition-all shrink-0"
                />

                <!-- Remove lesson -->
                <button 
                  type="button" 
                  @click="removeLesson(modIdx, lesIdx)" 
                  class="p-1.5 text-gray-500 hover:text-brand-danger transition-colors shrink-0"
                  v-if="mod.lessons.length > 1"
                >
                  <Trash class="w-4 h-4" />
                </button>
              </div>

              <!-- Add lesson trigger -->
              <button 
                type="button" 
                @click="addLesson(modIdx)"
                class="flex items-center space-x-1.5 text-[11px] font-semibold text-brand-primary hover:text-brand-secondary transition-colors pt-2.5"
              >
                <PlusCircle class="w-4.5 h-4.5" />
                <span>Add Lecture Item</span>
              </button>
            </div>

          </div>
        </div>

        <!-- Add Module main trigger -->
        <button 
          type="button" 
          @click="addModule"
          class="w-full border border-dashed border-white/10 hover:border-white/20 rounded-2xl py-4 flex items-center justify-center space-x-2 text-xs font-bold text-gray-400 hover:text-white transition-all bg-white/[0.01]"
        >
          <PlusCircle class="w-4.5 h-4.5 text-brand-primary" />
          <span>Append New Syllabus Module</span>
        </button>

        <!-- Actions footer -->
        <div class="flex justify-between items-center pt-6 border-t border-white/5">
          <button 
            type="button" 
            @click="step = 1"
            class="px-5 py-2 rounded-xl text-xs font-bold bg-white/5 border border-white/10 text-gray-300 hover:text-white transition-colors"
          >
            Go Back
          </button>
          
          <button 
            type="button" 
            @click="handleCreateCourse"
            class="px-6 py-2.5 bg-brand-accent hover:bg-emerald-600 text-white text-xs font-bold rounded-xl transition-all shadow-md shadow-brand-accent/20 flex items-center space-x-1.5"
          >
            <span>{{ isEditMode ? 'Save Course Changes' : 'Submit Course to Admin' }}</span>
            <CheckCircle class="w-4 h-4" />
          </button>
        </div>

      </div>

    </div>
  </div>
</template>
