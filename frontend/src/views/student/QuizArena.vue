<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import { useNotificationStore } from '../../store/notifications';
import { 
  Gamepad2, Trophy, Clock, Search, ShieldCheck, 
  ChevronRight, ChevronLeft, ChevronDown, CheckCircle, XCircle, X
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const notifStore = useNotificationStore();

const studentId = computed(() => authStore.currentUser?.id);

// Fetched data
const allQuizzes = computed(() => coursesStore.getAllQuizzes);
const enrollments = computed(() => coursesStore.getStudentEnrollments(studentId.value));
const myAttempts = computed(() => coursesStore.getStudentAttempts(studentId.value));

// Filters
const activeDifficulty = ref('All');
const selectedCourseId = ref('All');

// Unique courses for filter
const availableCourses = computed(() => {
  const map = new Map();
  allQuizzes.value.forEach(q => {
    // Find course name from store or use default
    const c = coursesStore.courses.find(c => c.id === q.courseId);
    if (c) map.set(c.id, c.title);
  });
  return map;
});

// Filtered Quizzes
const filteredQuizzes = computed(() => {
  return allQuizzes.value.filter(q => {
    const diffMatch = activeDifficulty.value === 'All' || q.difficulty === activeDifficulty.value;
    const courseMatch = selectedCourseId.value === 'All' || q.courseId === selectedCourseId.value;
    return diffMatch && courseMatch;
  });
});

// Active Quiz State
const activeQuiz = ref(null);
const currentQuestionIdx = ref(0);
const selectedAnswers = ref([]);
const timeRemaining = ref(0);
let timerInterval = null;

// Submission State
const isSubmitting = ref(false);
const quizResult = ref(null); // holds attempt result

// Format Time
const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60).toString().padStart(2, '0');
  const s = (seconds % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
};

const getCourseTitle = (id) => coursesStore.courses.find(c => c.id === id)?.title || "Unknown Course";

// Start Quiz
const startQuiz = (quiz) => {
  activeQuiz.value = quiz;
  currentQuestionIdx.value = 0;
  selectedAnswers.value = new Array(quiz.questions.length).fill(-1);
  quizResult.value = null;
  
  if (quiz.timeLimit > 0) {
    timeRemaining.value = quiz.timeLimit;
    timerInterval = setInterval(() => {
      timeRemaining.value--;
      if (timeRemaining.value <= 0) {
        clearInterval(timerInterval);
        submitQuiz(); // Auto submit
      }
    }, 1000);
  } else {
    timeRemaining.value = 0;
  }
};

const closeQuiz = () => {
  if (timerInterval) clearInterval(timerInterval);
  activeQuiz.value = null;
  quizResult.value = null;
};

// Navigation
const nextQuestion = () => {
  if (currentQuestionIdx.value < activeQuiz.value.questions.length - 1) {
    currentQuestionIdx.value++;
  }
};
const prevQuestion = () => {
  if (currentQuestionIdx.value > 0) {
    currentQuestionIdx.value--;
  }
};

// Submit Quiz
const submitQuiz = async () => {
  if (timerInterval) clearInterval(timerInterval);
  isSubmitting.value = true;
  
  try {
    const timeTaken = activeQuiz.value.timeLimit > 0 ? activeQuiz.value.timeLimit - timeRemaining.value : 0;
    const result = await coursesStore.submitQuizAttempt(
      activeQuiz.value.id,
      studentId.value,
      selectedAnswers.value,
      timeTaken
    );
    quizResult.value = result;
  } catch (err) {
    notifStore.showToast("Error", "Failed to submit quiz.", "danger");
  } finally {
    isSubmitting.value = false;
  }
};

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval);
});
</script>

<template>
  <div class="space-y-8 animate-fade-in pb-12">
    <!-- Header Area -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <h1 class="text-3xl md:text-4xl font-extrabold text-white font-display tracking-tight flex items-center space-x-3">
          <Gamepad2 class="w-8 h-8 text-brand-primary" />
          <span>Quiz Arena</span>
        </h1>
        <p class="text-gray-400 max-w-2xl text-sm md:text-base">
          Test your knowledge, earn badges, and climb the ranks. Browse available quizzes across all programs.
        </p>
      </div>

      <!-- Stats -->
      <div class="flex gap-4">
        <div class="glass-panel px-5 py-3 rounded-2xl border border-white/10 flex items-center space-x-4">
          <div class="p-2 bg-brand-primary/20 text-brand-primary rounded-xl">
            <Trophy class="w-6 h-6" />
          </div>
          <div>
            <p class="text-xs text-gray-400 font-bold uppercase tracking-wider">Avg Score</p>
            <p class="text-xl font-extrabold text-white">
              {{ myAttempts.length ? Math.round(myAttempts.reduce((acc, a) => acc + a.score, 0) / myAttempts.length) : 0 }}%
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters Area -->
    <div class="glass-panel p-4 rounded-2xl border border-white/5 flex flex-col md:flex-row gap-4 items-center justify-between">
      <div class="flex bg-brand-dark/50 p-1 rounded-xl border border-white/5 w-full md:w-auto overflow-x-auto">
        <button 
          v-for="diff in ['All', 'Easy', 'Medium', 'Hard']" 
          :key="diff"
          @click="activeDifficulty = diff"
          class="px-4 py-2 rounded-lg text-sm font-semibold transition-all whitespace-nowrap cursor-pointer"
          :class="activeDifficulty === diff ? 'bg-brand-primary text-white shadow-md' : 'text-gray-400 hover:text-white hover:bg-white/5'"
        >
          {{ diff }}
        </button>
      </div>

      <div class="w-full md:w-64 relative">
        <select 
          v-model="selectedCourseId"
          class="w-full bg-brand-dark/50 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-brand-primary appearance-none cursor-pointer"
        >
          <option value="All">All Courses</option>
          <option v-for="[id, title] in availableCourses" :key="id" :value="id">{{ title }}</option>
        </select>
        <ChevronDown class="w-4 h-4 text-gray-400 absolute right-3 top-3 pointer-events-none" />
      </div>
    </div>

    <!-- Main Grid: Quizzes + History -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Quiz Catalog (Left 2/3) -->
      <div class="lg:col-span-2 space-y-6">
        <h2 class="text-xl font-bold text-white flex items-center space-x-2">
          <Gamepad2 class="w-5 h-5 text-brand-primary" />
          <span>Available Quizzes</span>
        </h2>

        <div v-if="filteredQuizzes.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div 
            v-for="quiz in filteredQuizzes" 
            :key="quiz.id"
            class="glass-panel p-5 rounded-2xl border border-white/5 flex flex-col hover:-translate-y-1 transition-transform duration-300 relative overflow-hidden group"
          >
            <!-- Background Glow -->
            <div class="absolute inset-0 bg-gradient-to-br from-brand-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            
            <div class="flex justify-between items-start mb-3 relative z-10">
              <span 
                class="px-2.5 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase"
                :class="{
                  'bg-brand-accent/20 text-brand-accent': quiz.difficulty === 'Easy',
                  'bg-brand-warning/20 text-brand-warning': quiz.difficulty === 'Medium',
                  'bg-brand-danger/20 text-brand-danger': quiz.difficulty === 'Hard'
                }"
              >
                {{ quiz.difficulty }}
              </span>
              
              <!-- Best Score Badge -->
              <div v-if="coursesStore.getBestAttempt(quiz.id, studentId)" class="flex items-center space-x-1 bg-white/10 px-2 py-1 rounded-lg">
                <Trophy class="w-3 h-3 text-brand-warning" />
                <span class="text-[10px] font-bold text-white">{{ coursesStore.getBestAttempt(quiz.id, studentId).score }}%</span>
              </div>
            </div>

            <h3 class="text-lg font-bold text-white mb-1 leading-tight relative z-10">{{ quiz.title }}</h3>
            <p class="text-xs text-brand-primary mb-4 relative z-10">{{ getCourseTitle(quiz.courseId) }}</p>

            <div class="flex items-center space-x-4 text-xs text-gray-400 mb-6 relative z-10">
              <div class="flex items-center space-x-1.5">
                <ShieldCheck class="w-4 h-4 opacity-70" />
                <span>{{ quiz.questions.length }} Qs</span>
              </div>
              <div class="flex items-center space-x-1.5">
                <Clock class="w-4 h-4 opacity-70" />
                <span>{{ quiz.timeLimit > 0 ? formatTime(quiz.timeLimit) : 'No Limit' }}</span>
              </div>
            </div>

            <div class="mt-auto relative z-10">
              <button 
                @click="startQuiz(quiz)"
                class="w-full py-2.5 bg-white/5 hover:bg-brand-primary border border-white/10 hover:border-brand-primary rounded-xl text-sm font-semibold text-white transition-all duration-300 cursor-pointer"
              >
                Take Quiz
              </button>
            </div>
          </div>
        </div>

        <div v-else class="glass-panel p-12 rounded-3xl border border-white/5 text-center">
          <Gamepad2 class="w-12 h-12 text-gray-600 mx-auto mb-4" />
          <h3 class="text-lg font-bold text-gray-300">No Quizzes Found</h3>
          <p class="text-sm text-gray-500 mt-2">Try adjusting your filters.</p>
        </div>
      </div>

      <!-- Attempts History (Right 1/3) -->
      <div class="space-y-6">
        <h2 class="text-xl font-bold text-white flex items-center space-x-2">
          <Clock class="w-5 h-5 text-brand-secondary" />
          <span>My History</span>
        </h2>

        <div class="glass-panel p-1 rounded-2xl border border-white/5 h-[600px] overflow-y-auto custom-scrollbar">
          <div v-if="myAttempts.length > 0" class="space-y-1 p-2">
            <div 
              v-for="attempt in [...myAttempts].reverse()" 
              :key="attempt.id"
              class="p-4 rounded-xl border border-white/5 bg-white/[0.02] hover:bg-white/[0.04] transition-colors"
            >
              <div class="flex justify-between items-start mb-2">
                <p class="text-sm font-bold text-white truncate max-w-[150px]">
                  {{ allQuizzes.find(q => q.id === attempt.quizId)?.title || 'Deleted Quiz' }}
                </p>
                <span 
                  class="px-2 py-0.5 rounded-full text-[10px] font-bold"
                  :class="attempt.passed ? 'bg-brand-accent/20 text-brand-accent' : 'bg-brand-danger/20 text-brand-danger'"
                >
                  {{ attempt.score }}%
                </span>
              </div>
              <p class="text-[10px] text-gray-500">{{ new Date(attempt.attemptedAt).toLocaleString() }}</p>
            </div>
          </div>
          <div v-else class="p-8 text-center">
            <p class="text-sm text-gray-500">No attempts yet. Take a quiz to see your history!</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quiz Modal Overlay -->
    <div v-if="activeQuiz" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div class="bg-brand-card w-full max-w-3xl max-h-[90vh] overflow-y-auto rounded-3xl border border-white/10 shadow-2xl relative flex flex-col">
        
        <!-- Header -->
        <div class="sticky top-0 bg-brand-dark/95 backdrop-blur px-6 py-4 border-b border-white/10 flex justify-between items-center z-20">
          <div>
            <h3 class="text-xl font-bold text-white">{{ activeQuiz.title }}</h3>
            <p class="text-xs text-gray-400">Passing Score: {{ activeQuiz.passingScore }}%</p>
          </div>
          <div class="flex items-center space-x-4">
            <div v-if="activeQuiz.timeLimit > 0 && !quizResult" class="flex items-center space-x-2 text-brand-warning font-mono text-lg font-bold bg-brand-warning/10 px-3 py-1 rounded-lg">
              <Clock class="w-5 h-5" />
              <span>{{ formatTime(timeRemaining) }}</span>
            </div>
            <button @click="closeQuiz" class="p-2 text-gray-400 hover:text-white bg-white/5 rounded-full cursor-pointer hover:bg-white/10 transition-colors">
              <X class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Quiz Content Area -->
        <div class="p-6 md:p-8 flex-grow">
          
          <!-- RESULTS SCREEN -->
          <div v-if="quizResult" class="space-y-8 animate-fade-in text-center">
            <div class="inline-flex items-center justify-center w-24 h-24 rounded-full mb-2 shadow-2xl"
                 :class="quizResult.passed ? 'bg-brand-accent/20 text-brand-accent' : 'bg-brand-danger/20 text-brand-danger'">
              <Trophy v-if="quizResult.passed" class="w-12 h-12" />
              <XCircle v-else class="w-12 h-12" />
            </div>
            <h2 class="text-3xl font-extrabold text-white">{{ quizResult.score }}%</h2>
            <p class="text-lg text-gray-300">
              {{ quizResult.passed ? 'Congratulations! You passed the quiz.' : 'You did not meet the passing score. Keep practicing!' }}
            </p>

            <div class="bg-white/5 rounded-2xl p-6 text-left space-y-6 mt-8">
              <h3 class="text-lg font-bold text-white border-b border-white/10 pb-2">Review Answers</h3>
              <div v-for="(q, idx) in activeQuiz.questions" :key="q.id" class="space-y-3">
                <p class="text-sm font-semibold text-white">
                  <span class="text-gray-500 mr-2">{{ idx + 1 }}.</span> {{ q.text }}
                </p>
                <div class="pl-6 space-y-2 text-sm">
                  <p v-if="quizResult.answers[idx] === q.correctIndex" class="text-brand-accent flex items-center space-x-2">
                    <CheckCircle class="w-4 h-4" /> <span>You answered correctly.</span>
                  </p>
                  <p v-else class="text-brand-danger flex items-center space-x-2">
                    <XCircle class="w-4 h-4" /> <span>Your answer was incorrect. Correct answer was option {{ q.correctIndex + 1 }}.</span>
                  </p>
                  <div v-if="q.explanation" class="bg-white/5 p-3 rounded-xl border border-white/5 text-gray-300 italic text-xs">
                    <span class="font-bold text-gray-400 not-italic">Explanation:</span> {{ q.explanation }}
                  </div>
                </div>
              </div>
            </div>
            
            <button @click="closeQuiz" class="px-8 py-3 bg-white/10 hover:bg-white/20 text-white font-bold rounded-xl transition-all cursor-pointer">
              Return to Arena
            </button>
          </div>

          <!-- ACTIVE QUESTION SCREEN -->
          <div v-else class="space-y-8">
            <!-- Progress Bar -->
            <div class="space-y-2">
              <div class="flex justify-between text-xs font-bold text-gray-400">
                <span>Question {{ currentQuestionIdx + 1 }} of {{ activeQuiz.questions.length }}</span>
                <span>{{ Math.round(((currentQuestionIdx + 1) / activeQuiz.questions.length) * 100) }}%</span>
              </div>
              <div class="w-full bg-white/10 h-2 rounded-full overflow-hidden">
                <div class="bg-gradient-to-r from-brand-primary to-brand-secondary h-full transition-all duration-300"
                     :style="{ width: `${((currentQuestionIdx + 1) / activeQuiz.questions.length) * 100}%` }">
                </div>
              </div>
            </div>

            <!-- Question & Options -->
            <div class="bg-white/5 rounded-2xl p-6 md:p-8 border border-white/5 space-y-6 shadow-inner">
              <h4 class="text-xl md:text-2xl font-bold text-white leading-relaxed">
                {{ activeQuiz.questions[currentQuestionIdx].text }}
              </h4>
              
              <div class="space-y-3">
                <label 
                  v-for="(option, optIdx) in activeQuiz.questions[currentQuestionIdx].options" 
                  :key="optIdx"
                  class="flex items-center space-x-4 p-4 rounded-xl border cursor-pointer transition-all duration-200"
                  :class="selectedAnswers[currentQuestionIdx] === optIdx ? 'bg-brand-primary/20 border-brand-primary text-white shadow-[0_0_15px_rgba(var(--color-primary),0.3)]' : 'bg-brand-dark/50 border-white/10 text-gray-300 hover:border-white/30 hover:bg-white/5'"
                >
                  <div class="w-5 h-5 rounded-full border flex items-center justify-center shrink-0"
                       :class="selectedAnswers[currentQuestionIdx] === optIdx ? 'border-brand-primary' : 'border-gray-500'">
                    <div v-if="selectedAnswers[currentQuestionIdx] === optIdx" class="w-2.5 h-2.5 rounded-full bg-brand-primary"></div>
                  </div>
                  <span class="text-sm md:text-base leading-tight">{{ option }}</span>
                  <input type="radio" :name="`q-${currentQuestionIdx}`" :value="optIdx" v-model="selectedAnswers[currentQuestionIdx]" class="hidden" />
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer Navigation -->
        <div v-if="!quizResult" class="sticky bottom-0 bg-brand-card/95 backdrop-blur px-6 py-4 border-t border-white/10 flex justify-between items-center rounded-b-3xl">
          <button 
            @click="prevQuestion" 
            :disabled="currentQuestionIdx === 0"
            class="px-5 py-2.5 rounded-xl text-sm font-bold flex items-center space-x-2 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed text-gray-400 hover:bg-white/5 hover:text-white"
          >
            <ChevronLeft class="w-4 h-4" /> <span>Previous</span>
          </button>
          
          <button 
            v-if="currentQuestionIdx < activeQuiz.questions.length - 1"
            @click="nextQuestion"
            class="px-5 py-2.5 bg-brand-primary hover:bg-brand-secondary text-white rounded-xl text-sm font-bold flex items-center space-x-2 transition-all shadow-md cursor-pointer"
          >
            <span>Next</span> <ChevronRight class="w-4 h-4" />
          </button>
          
          <button 
            v-else
            @click="submitQuiz"
            :disabled="isSubmitting"
            class="px-6 py-2.5 bg-brand-accent hover:opacity-90 text-white rounded-xl text-sm font-bold flex items-center space-x-2 transition-all shadow-md cursor-pointer disabled:opacity-50"
          >
            <span v-if="isSubmitting">Submitting...</span>
            <span v-else>Submit Quiz</span>
            <CheckCircle v-if="!isSubmitting" class="w-4 h-4" />
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom scrollbar for history panel */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>
