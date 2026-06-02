<script setup>
import { ref, computed } from 'vue';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import { useNotificationStore } from '../../store/notifications';
import { 
  Gamepad2, Plus, Trash2, Edit, ChevronRight, ChevronLeft, 
  CheckCircle, XCircle, X, ShieldCheck, Clock
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const notifStore = useNotificationStore();

const teacherId = computed(() => authStore.currentUser?.id);

// Teacher's data
const myQuizzes = computed(() => coursesStore.getTeacherQuizzes(teacherId.value));
const myCourses = computed(() => coursesStore.getTeacherCourses(teacherId.value));

const getCourseTitle = (id) => coursesStore.courses.find(c => c.id === id)?.title || "Unknown Course";

// Delete Quiz
const isDeleting = ref(null);
const deleteQuiz = async (quizId) => {
  const confirmed = await notifStore.showConfirm(
    "Delete Quiz?",
    "This will permanently remove the quiz and all student attempts.",
    "danger",
    "Yes, Delete",
    "Cancel"
  );
  if (confirmed) {
    isDeleting.value = quizId;
    try {
      await coursesStore.deleteQuiz(quizId);
      notifStore.showToast("Success", "Quiz deleted successfully.", "success");
    } catch (err) {
      notifStore.showToast("Error", "Failed to delete quiz.", "danger");
    } finally {
      isDeleting.value = null;
    }
  }
};

// Create Quiz Modal State
const isModalOpen = ref(false);
const currentStep = ref(1); // 1 = Details, 2 = Questions
const isSubmitting = ref(false);

const newQuiz = ref({
  courseId: '',
  title: '',
  difficulty: 'Medium',
  timeLimit: 0,
  passingScore: 70,
  questions: []
});

const openModal = () => {
  newQuiz.value = {
    courseId: myCourses.value.length > 0 ? myCourses.value[0].id : '',
    title: '',
    difficulty: 'Medium',
    timeLimit: 0,
    passingScore: 70,
    questions: []
  };
  currentStep.value = 1;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

// Questions Builder State
const currentQuestion = ref({
  text: '',
  options: ['', '', '', ''],
  correctIndex: 0,
  explanation: ''
});

const addQuestion = () => {
  if (!currentQuestion.value.text || currentQuestion.value.options.some(o => !o)) {
    notifStore.showToast("Validation Error", "Please fill out the question and all 4 options.", "warning");
    return;
  }
  newQuiz.value.questions.push({ ...currentQuestion.value, options: [...currentQuestion.value.options] });
  currentQuestion.value = { text: '', options: ['', '', '', ''], correctIndex: 0, explanation: '' };
};

const removeQuestion = (idx) => {
  newQuiz.value.questions.splice(idx, 1);
};

const submitNewQuiz = async () => {
  if (newQuiz.value.questions.length === 0) {
    notifStore.showToast("Validation Error", "A quiz must have at least one question.", "warning");
    return;
  }
  isSubmitting.value = true;
  try {
    await coursesStore.createQuiz({
      teacherId: teacherId.value,
      teacherName: authStore.currentUser.name,
      ...newQuiz.value
    });
    notifStore.showToast("Quiz Published!", "Your new quiz is now live in the Arena.", "success");
    closeModal();
  } catch (err) {
    notifStore.showToast("Error", "Failed to create quiz.", "danger");
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="space-y-8 animate-fade-in pb-12">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <h1 class="text-3xl md:text-4xl font-extrabold text-white font-display tracking-tight flex items-center space-x-3">
          <Gamepad2 class="w-8 h-8 text-brand-primary" />
          <span>Quiz Manager</span>
        </h1>
        <p class="text-gray-400 max-w-2xl text-sm md:text-base">
          Create, edit, and monitor quizzes for your courses. Engage students with dynamic assessments.
        </p>
      </div>

      <button 
        @click="openModal"
        class="bg-brand-primary hover:bg-brand-secondary text-white px-6 py-3 rounded-xl font-bold flex items-center space-x-2 transition-all shadow-lg shadow-brand-primary/20 cursor-pointer"
      >
        <Plus class="w-5 h-5" />
        <span>Create New Quiz</span>
      </button>
    </div>

    <!-- Existing Quizzes -->
    <div class="space-y-4">
      <h2 class="text-xl font-bold text-white flex items-center space-x-2">
        <ShieldCheck class="w-5 h-5 text-brand-accent" />
        <span>My Quiz Bank</span>
      </h2>

      <div v-if="myQuizzes.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="quiz in myQuizzes" 
          :key="quiz.id"
          class="glass-panel p-6 rounded-3xl border border-white/5 flex flex-col relative group"
        >
          <div class="absolute inset-0 bg-gradient-to-br from-brand-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity rounded-3xl"></div>
          
          <div class="flex justify-between items-start mb-4 relative z-10">
            <span 
              class="px-3 py-1 rounded-full text-xs font-bold tracking-wider uppercase shadow-inner"
              :class="{
                'bg-brand-accent/20 text-brand-accent': quiz.difficulty === 'Easy',
                'bg-brand-warning/20 text-brand-warning': quiz.difficulty === 'Medium',
                'bg-brand-danger/20 text-brand-danger': quiz.difficulty === 'Hard'
              }"
            >
              {{ quiz.difficulty }}
            </span>
            <button 
              @click="deleteQuiz(quiz.id)" 
              class="p-2 bg-brand-danger/10 text-brand-danger rounded-xl hover:bg-brand-danger hover:text-white transition-colors cursor-pointer"
              title="Delete Quiz"
            >
              <Trash2 class="w-4 h-4" v-if="isDeleting !== quiz.id" />
              <div v-else class="w-4 h-4 rounded-full border-2 border-t-transparent border-white animate-spin"></div>
            </button>
          </div>

          <h3 class="text-xl font-bold text-white mb-2 relative z-10 truncate" :title="quiz.title">{{ quiz.title }}</h3>
          <p class="text-sm text-brand-primary mb-6 relative z-10 truncate">{{ getCourseTitle(quiz.courseId) }}</p>

          <div class="grid grid-cols-2 gap-4 mt-auto border-t border-white/10 pt-4 relative z-10">
            <div class="text-center">
              <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wider mb-1">Questions</p>
              <p class="text-lg font-bold text-gray-200">{{ quiz.questions.length }}</p>
            </div>
            <div class="text-center border-l border-white/10">
              <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wider mb-1">Pass Score</p>
              <p class="text-lg font-bold text-gray-200">{{ quiz.passingScore }}%</p>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="glass-panel p-16 rounded-3xl border border-white/5 text-center flex flex-col items-center justify-center">
        <div class="w-20 h-20 bg-white/5 rounded-full flex items-center justify-center mb-6 shadow-inner">
          <Gamepad2 class="w-10 h-10 text-gray-500" />
        </div>
        <h3 class="text-2xl font-bold text-white mb-2">Your Quiz Bank is Empty</h3>
        <p class="text-gray-400 max-w-md">Create your first quiz to challenge your students and reinforce their learning.</p>
        <button 
          @click="openModal"
          class="mt-8 bg-white/10 hover:bg-brand-primary border border-white/10 hover:border-brand-primary text-white px-6 py-3 rounded-xl font-bold transition-all cursor-pointer"
        >
          Create First Quiz
        </button>
      </div>
    </div>

    <!-- Create Quiz Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div class="bg-brand-card w-full max-w-4xl max-h-[90vh] rounded-3xl border border-white/10 shadow-2xl flex flex-col overflow-hidden">
        
        <!-- Header -->
        <div class="bg-brand-dark/95 border-b border-white/10 px-8 py-5 flex justify-between items-center z-10 shadow-sm">
          <div>
            <h3 class="text-2xl font-extrabold text-white">Quiz Wizard</h3>
            <p class="text-sm text-gray-400">Step {{ currentStep }} of 2: {{ currentStep === 1 ? 'Quiz Settings' : 'Add Questions' }}</p>
          </div>
          <button @click="closeModal" class="p-2 text-gray-400 hover:text-white bg-white/5 rounded-full cursor-pointer hover:bg-white/10 transition-colors">
            <X class="w-5 h-5" />
          </button>
        </div>

        <div class="flex-grow overflow-y-auto custom-scrollbar p-8">
          <!-- STEP 1: Details -->
          <div v-if="currentStep === 1" class="space-y-6 max-w-2xl mx-auto">
            <div class="space-y-2">
              <label class="text-sm font-bold text-gray-300">Target Course</label>
              <select v-model="newQuiz.courseId" class="w-full bg-brand-dark/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-brand-primary focus:outline-none appearance-none">
                <option v-for="c in myCourses" :key="c.id" :value="c.id">{{ c.title }}</option>
              </select>
            </div>
            
            <div class="space-y-2">
              <label class="text-sm font-bold text-gray-300">Quiz Title</label>
              <input type="text" v-model="newQuiz.title" placeholder="e.g. Vue 3 Reactivity Basics" class="w-full bg-brand-dark/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-brand-primary focus:outline-none placeholder-gray-600" />
            </div>

            <div class="grid grid-cols-2 gap-6">
              <div class="space-y-2">
                <label class="text-sm font-bold text-gray-300">Difficulty</label>
                <select v-model="newQuiz.difficulty" class="w-full bg-brand-dark/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-brand-primary focus:outline-none appearance-none">
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>
              <div class="space-y-2">
                <label class="text-sm font-bold text-gray-300">Passing Score (%)</label>
                <input type="number" v-model="newQuiz.passingScore" min="1" max="100" class="w-full bg-brand-dark/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-brand-primary focus:outline-none" />
              </div>
            </div>

            <div class="space-y-2">
              <label class="text-sm font-bold text-gray-300">Time Limit (Seconds, 0 = Unlimited)</label>
              <input type="number" v-model="newQuiz.timeLimit" min="0" class="w-full bg-brand-dark/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-brand-primary focus:outline-none" />
            </div>
          </div>

          <!-- STEP 2: Questions -->
          <div v-if="currentStep === 2" class="space-y-8">
            
            <div class="flex gap-8">
              <!-- Left: Form -->
              <div class="w-3/5 space-y-6">
                <div class="bg-white/5 rounded-2xl p-6 border border-white/10 shadow-inner">
                  <h4 class="text-lg font-bold text-white mb-4">Add a Question</h4>
                  
                  <div class="space-y-4">
                    <div>
                      <label class="text-xs font-bold text-gray-400 block mb-1">Question Text</label>
                      <textarea v-model="currentQuestion.text" rows="2" class="w-full bg-brand-dark/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-brand-primary focus:outline-none placeholder-gray-600 text-sm" placeholder="What does HTML stand for?"></textarea>
                    </div>

                    <div class="space-y-2">
                      <label class="text-xs font-bold text-gray-400 block mb-1">Answer Options (Select the correct one)</label>
                      <div v-for="(opt, idx) in currentQuestion.options" :key="idx" class="flex items-center space-x-3">
                        <input type="radio" name="correctAns" :value="idx" v-model="currentQuestion.correctIndex" class="w-4 h-4 cursor-pointer text-brand-primary bg-brand-dark border-white/10 focus:ring-brand-primary focus:ring-offset-brand-dark" title="Mark as correct answer" />
                        <input type="text" v-model="currentQuestion.options[idx]" class="w-full bg-brand-dark/50 border rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none transition-colors" :class="currentQuestion.correctIndex === idx ? 'border-brand-primary shadow-[0_0_10px_rgba(var(--color-primary),0.2)]' : 'border-white/10 focus:border-gray-500'" :placeholder="`Option ${idx + 1}`" />
                      </div>
                    </div>

                    <div>
                      <label class="text-xs font-bold text-gray-400 block mb-1">Explanation (Optional)</label>
                      <input type="text" v-model="currentQuestion.explanation" class="w-full bg-brand-dark/50 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:border-brand-primary focus:outline-none text-sm placeholder-gray-600" placeholder="Why is this answer correct?" />
                    </div>

                    <button @click="addQuestion" class="w-full mt-2 py-3 bg-white/10 hover:bg-white/20 border border-white/10 text-white font-bold rounded-xl transition-all flex justify-center items-center space-x-2 cursor-pointer">
                      <Plus class="w-4 h-4" /> <span>Add Question to Quiz</span>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Right: Added Questions Preview -->
              <div class="w-2/5 flex flex-col h-[500px]">
                <h4 class="text-sm font-bold text-gray-300 mb-4 sticky top-0 bg-brand-card py-2 z-10 flex justify-between items-center border-b border-white/10">
                  <span>Questions Preview</span>
                  <span class="bg-brand-primary/20 text-brand-primary px-2 py-0.5 rounded-full text-xs">{{ newQuiz.questions.length }} Total</span>
                </h4>
                
                <div class="flex-grow overflow-y-auto space-y-3 custom-scrollbar pr-2">
                  <div v-for="(q, idx) in newQuiz.questions" :key="idx" class="bg-white/5 border border-white/10 rounded-xl p-4 relative group">
                    <button @click="removeQuestion(idx)" class="absolute top-2 right-2 p-1.5 bg-brand-danger/20 text-brand-danger rounded-lg opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                      <Trash2 class="w-3.5 h-3.5" />
                    </button>
                    <p class="text-sm font-bold text-white mb-2 pr-6">{{ idx + 1 }}. {{ q.text }}</p>
                    <ul class="space-y-1 text-xs">
                      <li v-for="(o, oIdx) in q.options" :key="oIdx" class="truncate flex items-center space-x-2">
                        <CheckCircle v-if="oIdx === q.correctIndex" class="w-3 h-3 text-brand-accent shrink-0" />
                        <span v-else class="w-3 h-3 border border-gray-600 rounded-full shrink-0"></span>
                        <span :class="oIdx === q.correctIndex ? 'text-brand-accent font-semibold' : 'text-gray-400'">{{ o }}</span>
                      </li>
                    </ul>
                  </div>
                  
                  <div v-if="newQuiz.questions.length === 0" class="h-full flex flex-col items-center justify-center text-center opacity-50 p-6">
                    <Gamepad2 class="w-8 h-8 mb-3" />
                    <p class="text-sm">No questions added yet. Use the form to build your quiz.</p>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- Footer Actions -->
        <div class="bg-brand-dark/95 border-t border-white/10 px-8 py-5 flex justify-between items-center shrink-0">
          <button v-if="currentStep === 2" @click="currentStep = 1" class="px-6 py-2.5 rounded-xl text-sm font-bold text-gray-400 hover:text-white hover:bg-white/10 transition-colors flex items-center space-x-2 cursor-pointer">
            <ChevronLeft class="w-4 h-4" /> <span>Back to Settings</span>
          </button>
          <div v-else></div> <!-- Spacer -->

          <button v-if="currentStep === 1" @click="currentStep = 2" :disabled="!newQuiz.title || !newQuiz.courseId" class="px-8 py-3 bg-brand-primary hover:bg-brand-secondary text-white rounded-xl text-sm font-bold transition-all shadow-lg flex items-center space-x-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed">
            <span>Next: Add Questions</span> <ChevronRight class="w-4 h-4" />
          </button>
          
          <button v-if="currentStep === 2" @click="submitNewQuiz" :disabled="isSubmitting || newQuiz.questions.length === 0" class="px-8 py-3 bg-brand-accent hover:opacity-90 text-white rounded-xl text-sm font-bold transition-all shadow-lg flex items-center space-x-2 cursor-pointer disabled:opacity-50">
            <span v-if="isSubmitting">Publishing...</span>
            <span v-else>Publish Quiz</span>
            <CheckCircle v-if="!isSubmitting" class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
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
