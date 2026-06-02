<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCoursesStore } from '../store/courses';
import { useAuthStore } from '../store/auth';
import { useNotificationStore } from '../store/notifications';
import { 
  ArrowLeft, Star, Clock, BookOpen, User, Calendar, 
  ChevronDown, ChevronUp, Check, Play, FileText, Lock
} from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();
const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const notifStore = useNotificationStore();

const courseId = route.params.id;
const course = computed(() => coursesStore.courses.find(c => c.id === courseId));

// Tabs configuration
const activeTab = ref('overview'); // overview, curriculum, instructor, reviews
const expandedModules = ref({});
const activePreviewLessonId = ref(null);

const toggleModule = (moduleId) => {
  expandedModules.value[moduleId] = !expandedModules.value[moduleId];
};

// Check if student is already enrolled
const isEnrolled = computed(() => {
  if (!authStore.isAuthenticated || !authStore.isStudent) return false;
  return coursesStore.getEnrollment(authStore.currentUser.id, courseId) !== undefined;
});

// Check if user has preview access (enrolled, or creator teacher, or admin)
const canAccessPreview = computed(() => {
  if (!authStore.isAuthenticated) return false;
  if (authStore.currentUser.role === 'admin') return true;
  if (authStore.currentUser.role === 'teacher' && course.value?.teacherId === authStore.currentUser.id) return true;
  return isEnrolled.value;
});

const toggleLessonPreview = (lesson) => {
  if (!canAccessPreview.value) {
    notifStore.showToast("Locked Content", "Please enroll or purchase this course to access the lectures.", "warning");
    return;
  }
  const key = lesson.id || lesson.title;
  if (activePreviewLessonId.value === key) {
    activePreviewLessonId.value = null;
  } else {
    activePreviewLessonId.value = key;
  }
};

// Calculate total lesson count
const totalLessonsCount = computed(() => {
  if (!course.value) return 0;
  return course.value.modules.reduce((acc, mod) => acc + mod.lessons.length, 0);
});

// Live course reviews from store
const courseReviews = computed(() => coursesStore.getCourseReviews(courseId));

// Review form states
const newRating = ref(5);
const hoverRating = ref(0);
const newComment = ref('');
const isSubmittingReview = ref(false);
const reviewError = ref('');

const submitReview = async () => {
  if (!newComment.value.trim()) {
    reviewError.value = "Please write a review comment.";
    return;
  }
  isSubmittingReview.value = true;
  reviewError.value = '';
  try {
    await coursesStore.submitReview(
      course.value.id,
      authStore.currentUser.name,
      newRating.value,
      newComment.value.trim()
    );
    newComment.value = '';
    newRating.value = 5;
  } catch (err) {
    reviewError.value = err.message || "Failed to submit review.";
  } finally {
    isSubmittingReview.value = false;
  }
};

// Initialize all modules as expanded by default
onMounted(() => {
  if (course.value) {
    course.value.modules.forEach(mod => {
      expandedModules.value[mod.id] = true;
    });
  }
});

// Analytics computations for paid courses
const courseEnrollments = computed(() => {
  return coursesStore.enrollments.filter(e => e.courseId === courseId);
});

const totalEnrolledCount = computed(() => {
  return courseEnrollments.value.length;
});

const totalCompletedCount = computed(() => {
  return courseEnrollments.value.filter(e => e.progressPercent === 100).length;
});

const courseRevenue = computed(() => {
  return coursesStore.payments
    .filter(p => p.status === 'captured' && p.courseId === courseId)
    .reduce((sum, p) => sum + (p.amount || 0), 0);
});

const handleEnrollment = async () => {
  if (!authStore.isAuthenticated) {
    // Redirect to login
    router.push({ name: 'Login', query: { redirect: route.fullPath } });
    return;
  }

  if (!authStore.isStudent) {
    notifStore.showAlert("Access Denied", "Only Student accounts can enroll in courses!", "danger");
    return;
  }

  const coursePrice = course.value.price || 0;

  if (coursePrice > 0) {
    try {
      // 1. Create order
      const order = await coursesStore.createPaymentOrder({
        courseId: course.value.id,
        courseTitle: course.value.title,
        userId: authStore.currentUser.id,
        userName: authStore.currentUser.name,
        amount: coursePrice
      });

      // 2. Open Razorpay
      const options = {
        key: order.keyId,
        amount: order.amount,
        currency: order.currency,
        name: "Aether E-Learning",
        description: `Enrollment for ${course.value.title}`,
        order_id: order.orderId,
        handler: async function (response) {
          try {
            await coursesStore.verifyPayment({
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
              courseId: course.value.id,
              userId: authStore.currentUser.id
            });
            
            // 3. Enroll if verified
            await coursesStore.enrollInCourse(authStore.currentUser.id, course.value.id);
            router.push(`/student/player/${course.value.id}`);
          } catch (err) {
            notifStore.showAlert("Verification Failed", "Payment verification failed. Please contact support.", "danger");
          }
        },
        prefill: {
          name: authStore.currentUser.name,
          email: authStore.currentUser.email
        },
        theme: {
          color: "#6366F1"
        }
      };
      
      const rzp = new window.Razorpay(options);
      rzp.on('payment.failed', function (response){
        notifStore.showAlert("Payment Failed", response.error.description, "danger");
      });
      rzp.open();

    } catch (err) {
      notifStore.showAlert("Initialization Failed", "Failed to initiate payment: " + err.message, "danger");
    }
  } else {
    // Free course fallback
    await coursesStore.enrollInCourse(authStore.currentUser.id, course.value.id);
    router.push(`/student/player/${course.value.id}`);
  }
};
</script>

<template>
  <div v-if="course" class="space-y-8 py-4">
    <!-- Back Button -->
    <button 
      @click="router.back()" 
      class="flex items-center space-x-2 text-sm text-gray-400 hover:text-white transition-colors"
    >
      <ArrowLeft class="w-4 h-4" />
      <span>Back</span>
    </button>

    <!-- Main Detail Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
      <!-- Left Column (Information Panel) -->
      <div class="lg:col-span-2 space-y-8">
        <!-- Title & Header summary -->
        <div class="space-y-4">
          <div class="flex items-center space-x-2">
            <span class="px-3 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider bg-brand-primary/20 text-brand-primary border border-brand-primary/30">
              {{ course.category }}
            </span>
            <span class="px-3 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider bg-white/5 text-gray-300 border border-white/5">
              {{ course.difficulty }}
            </span>
          </div>

          <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight text-white font-display leading-tight">
            {{ course.title }}
          </h1>

          <p class="text-sm md:text-base text-gray-400 leading-relaxed font-light">
            {{ course.shortDescription || course.description }}
          </p>

          <!-- Author & Review rating summary -->
          <div class="flex flex-wrap items-center gap-6 text-xs text-gray-400 pt-2 border-y border-white/5 py-4">
            <div class="flex items-center space-x-2">
              <div class="w-6 h-6 rounded-full bg-brand-primary/35 flex items-center justify-center font-bold text-white text-[10px]">
                {{ course.teacherName.split(' ').map(n => n[0]).join('').toUpperCase() }}
              </div>
              <span class="font-medium text-white">Instructed by {{ course.teacherName }}</span>
            </div>

            <div class="flex items-center space-x-1 shrink-0">
              <Star class="w-4 h-4 text-brand-warning fill-brand-warning" />
              <span class="font-bold text-white">{{ coursesStore.getCourseRating(course.id).toFixed(1) }}</span>
              <span>({{ coursesStore.getCourseReviewsCount(course.id) }} reviews)</span>
            </div>

            <span class="flex items-center space-x-1">
              <Clock class="w-4 h-4 text-brand-primary" />
              <span>{{ course.duration || '4.5 Hours' }} total length</span>
            </span>

            <span class="flex items-center space-x-1">
              <BookOpen class="w-4 h-4 text-brand-accent" />
              <span>{{ course.modules.length }} modules syllabus</span>
            </span>
          </div>
        </div>

        <!-- Detail Tabs Navigation -->
        <div class="space-y-6">
          <div class="flex items-center space-x-1 border-b border-white/5 pb-0 overflow-x-auto scrollbar-none">
            <button 
              @click="activeTab = 'overview'"
              class="px-6 py-3 text-xs font-bold uppercase tracking-wider border-b-2 transition-all whitespace-nowrap"
              :class="activeTab === 'overview' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
            >
              Overview
            </button>
            <button 
              @click="activeTab = 'curriculum'"
              class="px-6 py-3 text-xs font-bold uppercase tracking-wider border-b-2 transition-all whitespace-nowrap"
              :class="activeTab === 'curriculum' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
            >
              Curriculum
            </button>
            <button 
              @click="activeTab = 'instructor'"
              class="px-6 py-3 text-xs font-bold uppercase tracking-wider border-b-2 transition-all whitespace-nowrap"
              :class="activeTab === 'instructor' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
            >
              Instructor
            </button>
            <button 
              @click="activeTab = 'reviews'"
              class="px-6 py-3 text-xs font-bold uppercase tracking-wider border-b-2 transition-all whitespace-nowrap"
              :class="activeTab === 'reviews' ? 'border-brand-primary text-white font-semibold' : 'border-transparent text-gray-400 hover:text-white'"
            >
              Reviews ({{ courseReviews.length }})
            </button>
          </div>

          <!-- Tabs Viewport -->
          <div class="animate-fade-in">
            <!-- 1. Overview Tab -->
            <div v-if="activeTab === 'overview'" class="space-y-6 text-sm text-gray-300 leading-relaxed font-light">
              <div class="space-y-3">
                <h3 class="text-lg font-bold text-white font-display">About This Program</h3>
                <p>{{ course.description }}</p>
              </div>

              <!-- Learning items -->
              <div class="glass-panel p-6 rounded-2xl border border-white/5 space-y-4">
                <h4 class="text-xs font-bold text-white uppercase tracking-wider">What you will learn:</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <template v-if="course.learningOutcomes && course.learningOutcomes.length > 0">
                    <div 
                      v-for="(outcome, oIdx) in course.learningOutcomes" 
                      :key="oIdx" 
                      class="flex items-start space-x-2 text-xs"
                    >
                      <Check class="w-4 h-4 text-brand-accent shrink-0 mt-0.5" />
                      <span>{{ outcome }}</span>
                    </div>
                  </template>
                  <template v-else>
                    <div class="flex items-start space-x-2 text-xs">
                      <Check class="w-4 h-4 text-brand-accent shrink-0 mt-0.5" />
                      <span>Scaffold dynamic responsive layouts using Vue framework modules</span>
                    </div>
                    <div class="flex items-start space-x-2 text-xs">
                      <Check class="w-4 h-4 text-brand-accent shrink-0 mt-0.5" />
                      <span>Understand responsive components, models, and data-flows</span>
                    </div>
                    <div class="flex items-start space-x-2 text-xs">
                      <Check class="w-4 h-4 text-brand-accent shrink-0 mt-0.5" />
                      <span>Implement secure access configurations and routing limits</span>
                    </div>
                    <div class="flex items-start space-x-2 text-xs">
                      <Check class="w-4 h-4 text-brand-accent shrink-0 mt-0.5" />
                      <span>Create full modular portfolios with clean, production code standards</span>
                    </div>
                  </template>
                </div>
              </div>
            </div>

            <!-- 2. Curriculum Tab -->
            <div v-if="activeTab === 'curriculum'" class="space-y-4">
              <h3 class="text-lg font-bold text-white font-display mb-4">Syllabus Breakdown</h3>
              
              <div class="space-y-3">
                <div 
                  v-for="mod in course.modules" 
                  :key="mod.id"
                  class="glass-panel rounded-2xl overflow-hidden border border-white/5 bg-brand-card/45"
                >
                  <!-- Module Header Accordion Trigger -->
                  <button 
                    @click="toggleModule(mod.id)"
                    class="w-full flex items-center justify-between px-5 py-4.5 hover:bg-white/5 transition-colors text-left"
                  >
                    <span class="text-sm font-bold text-white font-display">{{ mod.title }}</span>
                    <div class="flex items-center space-x-3 text-xs text-gray-400">
                      <span>{{ mod.lessons.length }} Items</span>
                      <ChevronDown v-if="!expandedModules[mod.id]" class="w-4 h-4" />
                      <ChevronUp v-else class="w-4 h-4" />
                    </div>
                  </button>

                  <!-- Lessons list -->
                  <div v-if="expandedModules[mod.id]" class="border-t border-white/5 bg-brand-dark/20 divide-y divide-white/5">
                    <template v-for="lesson in mod.lessons" :key="lesson.id || lesson.title">
                      <div 
                        @click="toggleLessonPreview(lesson)"
                        class="flex items-center justify-between px-6 py-3.5 text-xs transition-colors"
                        :class="{
                          'cursor-pointer hover:bg-white/[0.02] text-gray-300 hover:text-white': canAccessPreview,
                          'cursor-not-allowed text-gray-500 bg-brand-dark/10': !canAccessPreview,
                          'bg-brand-primary/5 text-white font-bold': canAccessPreview && activePreviewLessonId === (lesson.id || lesson.title)
                        }"
                      >
                        <div class="flex items-center space-x-3 truncate">
                          <Play v-if="lesson.type === 'video'" class="w-4 h-4 shrink-0" :class="canAccessPreview ? 'text-brand-primary' : 'text-gray-600'" />
                          <FileText v-else class="w-4 h-4 shrink-0" :class="canAccessPreview ? 'text-brand-accent' : 'text-gray-600'" />
                          <span class="truncate">{{ lesson.title }}</span>
                        </div>
                        <div class="flex items-center space-x-3 shrink-0 ml-4">
                          <span class="font-medium" :class="canAccessPreview ? 'text-gray-500' : 'text-gray-600'">{{ lesson.duration }}</span>
                          <span v-if="lesson.url && canAccessPreview" class="text-[9px] px-1.5 py-0.5 rounded bg-brand-primary/10 text-brand-primary font-bold uppercase tracking-wider">Preview</span>
                          <span v-else-if="lesson.url" class="flex items-center space-x-1 text-[9px] px-1.5 py-0.5 rounded bg-white/5 text-gray-500 font-bold uppercase tracking-wider border border-white/5 shrink-0">
                            <Lock class="w-2.5 h-2.5" />
                            <span>Locked</span>
                          </span>
                        </div>
                      </div>

                      <!-- Inline Lesson Preview Panel -->
                      <div v-if="activePreviewLessonId === (lesson.id || lesson.title) && lesson.url" class="px-6 py-4 bg-brand-dark/40 border-t border-white/5 space-y-3 animate-fade-in text-left">
                        <div class="flex items-center justify-between">
                          <span class="text-[10px] font-bold text-brand-primary uppercase tracking-wider">Lecture Review</span>
                          <a :href="lesson.url" target="_blank" class="text-[9px] text-brand-accent hover:underline flex items-center space-x-1 font-bold">
                            <span>Open in new tab</span>
                          </a>
                        </div>
                        
                        <!-- Video Player -->
                        <div v-if="lesson.type === 'video'" class="max-w-xl rounded-xl overflow-hidden bg-black border border-white/10 aspect-video shadow-md">
                          <video :src="lesson.url" controls class="w-full h-full object-contain"></video>
                        </div>
                        
                        <!-- PDF Attachment Card -->
                        <div v-else-if="lesson.type === 'pdf'" class="flex items-center space-x-3 p-3 bg-brand-dark/60 rounded-xl border border-white/5 max-w-xl">
                          <FileText class="w-8 h-8 text-brand-accent shrink-0" />
                          <div class="truncate text-left flex-grow">
                            <p class="text-[10px] font-bold text-white truncate">PDF Study Guide Document</p>
                            <a :href="lesson.url" target="_blank" class="text-[9px] text-gray-400 hover:underline truncate block">
                              {{ lesson.url }}
                            </a>
                          </div>
                        </div>
                      </div>
                    </template>
                  </div>
                </div>
              </div>
            </div>

            <!-- 3. Instructor Tab -->
            <div v-if="activeTab === 'instructor'" class="space-y-4">
              <div class="flex items-start space-x-4">
                <div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-brand-primary to-brand-secondary flex items-center justify-center font-bold text-white text-2xl shadow-lg shadow-brand-primary/10">
                  {{ course.teacherName.split(' ').map(n => n[0]).join('').toUpperCase() }}
                </div>
                <div class="space-y-1">
                  <h3 class="text-lg font-bold text-white font-display">{{ course.teacherName }}</h3>
                  <p class="text-xs text-brand-primary font-medium">Senior Educator at Aether Academy</p>
                  <p class="text-xs text-gray-400">Curating highly responsive technology paradigms since 2018.</p>
                </div>
              </div>
              
              <p class="text-xs md:text-sm text-gray-400 leading-relaxed font-light pt-4 border-t border-white/5">
                {{ course.teacherName }} is a dedicated professional instructor with thousands of student enrollments. Specializing in practical project development, her lessons prioritize step-by-step modular architectures, elegant responsive interfaces, and production-ready code principles.
              </p>
            </div>

            <!-- 4. Reviews Tab -->
            <div v-if="activeTab === 'reviews'" class="space-y-6">
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-bold text-white font-display">Student Feedback</h3>
                <div class="flex items-center space-x-1 shrink-0">
                  <Star class="w-4.5 h-4.5 text-brand-warning fill-brand-warning" />
                  <span class="text-base font-extrabold text-white leading-none">{{ coursesStore.getCourseRating(course.id).toFixed(1) }}</span>
                  <span class="text-xs text-gray-500">/ 5.0</span>
                </div>
              </div>

              <!-- Submit Review form (visible ONLY for enrolled students) -->
              <div v-if="isEnrolled" class="glass-panel p-5.5 rounded-2xl border border-white/5 bg-brand-card space-y-4 text-left shadow-sm">
                <h4 class="text-xs font-bold text-white uppercase tracking-wider flex items-center space-x-1.5 font-display">
                  <Star class="w-4 h-4 text-brand-warning fill-brand-warning" />
                  <span>Rate & Review this Course</span>
                </h4>
                
                <div class="space-y-4">
                  <!-- Star selection widget -->
                  <div class="flex items-center space-x-3">
                    <span class="text-xs text-gray-400">Your Rating:</span>
                    <div class="flex items-center space-x-1">
                      <button 
                        v-for="star in 5" 
                        :key="star"
                        type="button"
                        @click="newRating = star"
                        @mouseover="hoverRating = star"
                        @mouseleave="hoverRating = 0"
                        class="focus:outline-none transition-transform active:scale-95 cursor-pointer"
                      >
                        <Star 
                          class="w-5.5 h-5.5 transition-all duration-150"
                          :class="{
                            'text-brand-warning fill-brand-warning scale-110': star <= (hoverRating || newRating),
                            'text-gray-600': star > (hoverRating || newRating)
                          }"
                        />
                      </button>
                    </div>
                    <span class="text-xs font-extrabold text-brand-warning ml-1.5">{{ newRating }} ★</span>
                  </div>

                  <!-- Comment Input -->
                  <div class="space-y-1.5">
                    <textarea 
                      v-model="newComment"
                      placeholder="Write your review, technical comments, or course critiques..."
                      class="w-full h-24 p-3 bg-brand-dark/40 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-1 focus:ring-brand-primary placeholder-gray-550 leading-relaxed resize-none shadow-inner"
                    ></textarea>
                  </div>

                  <!-- Submit action -->
                  <div class="flex justify-between items-center">
                    <span v-if="reviewError" class="text-xs text-brand-danger font-semibold">{{ reviewError }}</span>
                    <span v-else class="text-[9px] text-gray-500">Your review will update the verified catalog live.</span>

                    <button 
                      @click="submitReview"
                      :disabled="isSubmittingReview"
                      class="px-5 py-2.5 bg-brand-primary hover:bg-brand-secondary text-white text-xs font-bold rounded-xl transition-all shadow-md shadow-brand-primary/20 flex items-center space-x-1.5 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <span>{{ isSubmittingReview ? 'Posting...' : 'Post Review' }}</span>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Reviews list grid -->
              <div v-if="courseReviews.length > 0" class="space-y-4">
                <div 
                  v-for="rev in courseReviews" 
                  :key="rev.id"
                  class="p-4.5 bg-brand-card/30 border border-white/5 rounded-2xl text-left space-y-2.5 shadow-sm animate-fade-in"
                >
                  <div class="flex items-start justify-between gap-3">
                    <div class="flex items-center space-x-2.5 truncate">
                      <div class="w-7 h-7 rounded-full bg-brand-primary/10 border border-brand-primary/20 text-brand-primary flex items-center justify-center font-bold text-[10px] uppercase shrink-0">
                        {{ rev.studentName.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase() }}
                      </div>
                      <div class="truncate">
                        <h5 class="text-xs font-bold text-white truncate">{{ rev.studentName }}</h5>
                        <p class="text-[8px] text-gray-550 font-semibold">{{ rev.date }}</p>
                      </div>
                    </div>

                    <!-- Stars display -->
                    <div class="flex items-center space-x-0.5 shrink-0">
                      <Star 
                        v-for="star in 5" 
                        :key="star"
                        class="w-3.5 h-3.5"
                        :class="star <= rev.rating ? 'text-brand-warning fill-brand-warning' : 'text-gray-600'"
                      />
                    </div>
                  </div>
                  <p class="text-xs text-gray-300 leading-relaxed font-light pl-[38px] pr-2">{{ rev.comment }}</p>
                </div>
              </div>

              <!-- Empty state reviews -->
              <div 
                v-else 
                class="p-8 text-center bg-brand-dark/20 border border-dashed border-white/5 rounded-2xl text-xs text-gray-500 leading-normal"
              >
                No verified reviews found. Be the first to share your learning feedback!
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column (Sticky Sidecard Panel) -->
      <div class="lg:sticky lg:top-24 space-y-6">
        <div class="glass-panel rounded-3xl overflow-hidden border border-white/5 bg-brand-card shadow-2xl p-6 flex flex-col space-y-6">
          <!-- Thumbnail aspect card -->
          <div class="aspect-video w-full rounded-2xl overflow-hidden bg-slate-800 shadow-md">
            <img :src="course.thumbnail" :alt="course.title" class="w-full h-full object-cover" />
          </div>

          <!-- Price & Metrics Row -->
          <div class="space-y-1">
            <div class="flex items-end justify-between">
              <span class="text-3xl font-extrabold text-white font-display">
                {{ course.price > 0 ? `₹${course.price / 100}` : 'Free' }}
              </span>
              <span v-if="course.price > 0" class="text-xs text-brand-accent font-bold">Premium Course</span>
              <span v-else class="text-xs text-gray-450 line-through">19,999 INR</span>
            </div>
            <p class="text-[10px] font-semibold text-brand-accent uppercase tracking-wider">Self-paced learning program</p>
          </div>

          <!-- Call To Action -->
          <div class="space-y-2 pt-2">
            <!-- Enrolled Status -->
            <router-link 
              v-if="isEnrolled"
              :to="`/student/player/${course.id}`"
              class="w-full text-center flex items-center justify-center space-x-2 py-3 bg-brand-accent text-white text-sm font-bold rounded-2xl shadow-lg shadow-brand-accent/15 transition-all hover:bg-emerald-600"
            >
              <span>You are Enrolled - Go to Player</span>
            </router-link>

            <!-- Pending Review / Non-student restrictions -->
            <div 
              v-else-if="authStore.isAuthenticated && !authStore.isStudent" 
              class="w-full text-center p-3 rounded-2xl bg-white/5 border border-white/10 text-xs text-gray-400 leading-relaxed"
            >
              <span>Signed in as <strong>{{ authStore.currentUser.role }}</strong>. Dashboard controls are active inside your portal.</span>
            </div>

            <!-- Standard enrollment click -->
            <button 
              v-else
              @click="handleEnrollment"
              class="w-full text-center flex items-center justify-center space-x-2 py-3 bg-brand-primary text-white text-sm font-bold rounded-2xl shadow-lg shadow-brand-primary/20 transition-all hover:bg-brand-secondary glow-btn"
            >
              <span>Enroll Now</span>
            </button>
          </div>

          <!-- Course Specs bullet list -->
          <div class="space-y-3.5 pt-4 border-t border-white/5 text-xs text-gray-300">
            <h4 class="text-[10px] font-bold text-white uppercase tracking-wider">Specifications:</h4>
            
            <div class="flex items-center justify-between">
              <span class="text-gray-450">Format:</span>
              <span class="font-medium text-white">Full On-Demand</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-450">Curriculum:</span>
              <span class="font-medium text-white">{{ totalLessonsCount }} Lessons</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-450">Includes:</span>
              <span class="font-medium text-brand-accent">Verified Certificate</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-450">Access:</span>
              <span class="font-medium text-white">{{ course.price > 0 ? 'Paid Lifetime' : 'Lifetime Free' }}</span>
            </div>
          </div>

          <!-- Paid Course Performance Metrics -->
          <div v-if="course.price > 0" class="space-y-4 pt-5 border-t border-white/5 text-xs text-gray-300">
            <h4 class="text-[10px] font-bold text-white uppercase tracking-wider flex items-center space-x-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-brand-primary animate-pulse"></span>
              <span>Course Performance Matrix</span>
            </h4>
            
            <div class="grid grid-cols-3 gap-2 text-center">
              <div class="p-2.5 rounded-xl bg-white/[0.02] border border-white/5 flex flex-col justify-between h-14 animate-fade-in">
                <span class="text-[8px] text-gray-450 uppercase tracking-wider leading-none">Revenue</span>
                <span class="font-extrabold text-white text-xs mt-1 truncate">₹{{ (courseRevenue / 100).toFixed(0) }}</span>
              </div>
              <div class="p-2.5 rounded-xl bg-white/[0.02] border border-white/5 flex flex-col justify-between h-14 animate-fade-in">
                <span class="text-[8px] text-gray-450 uppercase tracking-wider leading-none">Learners</span>
                <span class="font-extrabold text-brand-primary text-xs mt-1">{{ totalEnrolledCount }}</span>
              </div>
              <div class="p-2.5 rounded-xl bg-white/[0.02] border border-white/5 flex flex-col justify-between h-14 animate-fade-in">
                <span class="text-[8px] text-gray-450 uppercase tracking-wider leading-none">Completed</span>
                <span class="font-extrabold text-brand-accent text-xs mt-1">{{ totalCompletedCount }}</span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
  
  <!-- Fallback state if course is not located -->
  <div v-else class="text-center py-24 glass-panel max-w-xl mx-auto rounded-3xl border border-white/5 space-y-4">
    <h3 class="text-xl font-bold text-white">Program Not Found</h3>
    <p class="text-xs text-gray-400">The specific learning route you requested cannot be located in the active directory.</p>
    <router-link to="/" class="inline-block bg-brand-primary text-white text-xs font-semibold px-6 py-2.5 rounded-xl">
      Return Home
    </router-link>
  </div>
</template>
