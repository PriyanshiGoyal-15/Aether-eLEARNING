<script setup>
import { ref, computed } from 'vue';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import { useRouter } from 'vue-router';
import { 
  ArrowLeft, PlusCircle, Trash, Award, BookOpen, 
  Settings, Layers, CheckCircle, Video, FileText
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const router = useRouter();

const teacherId = computed(() => authStore.currentUser?.id);
const teacherName = computed(() => authStore.currentUser?.name);

// Creator form state
const step = ref(1); // 1: Basic Info, 2: Module/Lesson Builder

const title = ref('');
const description = ref('');
const category = ref('Development');
const difficulty = ref('Intermediate');
const thumbnail = ref('');

const modules = ref([
  {
    title: 'Module 1: Getting Started',
    lessons: [
      { title: '1. Introduction to the Program', type: 'video', url: '', duration: '12:30' }
    ]
  }
]);

// Helper options
const categories = ['Development', 'Backend', 'Design'];
const difficulties = ['Beginner', 'Intermediate', 'Advanced'];

const addModule = () => {
  modules.value.push({
    title: `Module ${modules.value.length + 1}: Title here`,
    lessons: [
      { title: '1. First Lecture', type: 'video', url: '', duration: '10:00' }
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
    alert("Please complete the basic course information before submitting!");
    return;
  }

  try {
    // Create course via store
    await coursesStore.createCourse(
      teacherId.value,
      teacherName.value,
      title.value,
      description.value,
      category.value,
      difficulty.value,
      thumbnail.value,
      modules.value
    );

    alert(`Course "${title.value}" created successfully! It is now pending administrative approval.`);
    router.push('/teacher/dashboard');
  } catch (err) {
    console.error(err);
    alert(err.message || "Failed to create course. Please try again.");
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
        <h1 class="text-xl md:text-2xl font-extrabold text-white font-display">Create a New Program</h1>
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
            </select>
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

          <!-- Thumbnail link -->
          <div class="space-y-1.5 md:col-span-2">
            <label for="thumbnail" class="text-xs font-semibold text-gray-400">Thumbnail URL (Unsplash or custom image links)</label>
            <input 
              v-model="thumbnail" 
              type="url" 
              id="thumbnail" 
              placeholder="https://images.unsplash.com/photo-..." 
              class="w-full pl-4 pr-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
            />
            <p class="text-[10px] text-gray-500 leading-normal">Tip: Leave empty to auto-load a premium default tech design placeholder image.</p>
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
            <span>Submit Course to Admin</span>
            <CheckCircle class="w-4 h-4" />
          </button>
        </div>

      </div>

    </div>
  </div>
</template>
