<script setup>
import { computed, ref } from 'vue';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { Bar } from 'vue-chartjs';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import { useRouter } from 'vue-router';
import { 
  Users, BookOpen, Star, DollarSign, PlusCircle, 
  TrendingUp, ClipboardList, HelpCircle, XCircle, CheckCircle, AlertTriangle,
  Eye, EyeOff, MessageSquare
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const router = useRouter();

const teacherId = computed(() => authStore.currentUser?.id);
const teacherName = computed(() => authStore.currentUser?.name);

// Teacher's courses
const courses = computed(() => coursesStore.getTeacherCourses(teacherId.value));

// Total students enrolled in teacher's courses
const enrollments = computed(() => coursesStore.getTeacherStudents(teacherId.value));
const totalStudentsCount = computed(() => enrollments.value.length);

// Calculated average rating of all their courses
const averageRating = computed(() => {
  if (courses.value.length === 0) return 5.0;
  const total = courses.value.reduce((acc, curr) => acc + coursesStore.getCourseRating(curr.id), 0);
  return Number((total / courses.value.length).toFixed(1));
});

// Calculated total reviews left on their courses
const reviewsCount = computed(() => teacherReviews.value.length);

const totalEarnings = computed(() => coursesStore.getTeacherRevenue(teacherId.value));

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const chartData = computed(() => {
  return {
    labels: courses.value.map(c => c.title.substring(0, 15) + (c.title.length > 15 ? '...' : '')),
    datasets: [
      {
        label: 'Course Enrollments',
        backgroundColor: '#10b981', // brand-accent
        borderRadius: 6,
        data: courses.value.map(c => c.studentsCount || 0)
      }
    ]
  }
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { labels: { color: '#9ca3af' } },
  },
  scales: {
    y: { ticks: { color: '#9ca3af', precision: 0 }, grid: { color: 'rgba(255,255,255,0.05)' } },
    x: { ticks: { color: '#9ca3af' }, grid: { display: false } }
  }
};

// Expanded state for rejection reasons
const expandedReasons = ref({});

const toggleReason = (courseId) => {
  expandedReasons.value[courseId] = !expandedReasons.value[courseId];
};

// Filter reviews belonging to any of this teacher's courses
const teacherCourseIds = computed(() => courses.value.map(c => c.id));
const teacherReviews = computed(() => {
  return coursesStore.reviews.filter(r => teacherCourseIds.value.includes(r.courseId));
});

const getCourseTitle = (courseId) => {
  const c = courses.value.find(course => course.id === courseId);
  return c ? c.title : "Unknown Course";
};

const getCourseRevenue = (courseId) => {
  return coursesStore.payments
    .filter(p => p.status === 'captured' && p.courseId === courseId)
    .reduce((sum, p) => sum + (p.teacherRevenue || 0), 0);
};

const isTogglingReview = ref({});

const toggleReview = async (reviewId) => {
  isTogglingReview.value[reviewId] = true;
  try {
    await coursesStore.toggleReviewVisibility(reviewId);
  } catch (err) {
    notifStore.showToast("Update Failed", "Failed to toggle review visibility: " + err.message, "danger");
  } finally {
    isTogglingReview.value[reviewId] = false;
  }
};
</script>

<template>
  <div class="space-y-10 py-4">
    <!-- Welcome Header & Actions -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="space-y-1.5">
        <h1 class="text-2xl md:text-3xl font-extrabold text-white font-display">
          Teacher Portal: Overview
        </h1>
        <p class="text-xs text-gray-450">Manage your course catalog, reviews, and track learning progress.</p>
      </div>

      <!-- Action buttons -->
      <div class="flex flex-wrap items-center gap-3 shrink-0">
        <router-link 
          to="/teacher/students"
          class="px-4.5 py-2.5 bg-white/5 border border-white/10 text-xs font-semibold text-gray-300 hover:text-white rounded-xl transition-all flex items-center space-x-1.5"
        >
          <ClipboardList class="w-4 h-4" />
          <span>Monitor Student Progress</span>
        </router-link>

        <router-link 
          to="/teacher/create"
          class="px-5 py-2.5 bg-brand-accent hover:bg-emerald-600 text-white text-xs font-bold rounded-xl transition-all shadow-md shadow-brand-accent/15 flex items-center space-x-1.5"
        >
          <PlusCircle class="w-4 h-4" />
          <span>Upload Course</span>
        </router-link>
      </div>
    </div>

    <!-- Analytics Dashboard widgets -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- 1. Total Enrolled -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Enrolled Learners</p>
          <h3 class="text-2xl font-extrabold text-white">{{ totalStudentsCount }}</h3>
          <p class="text-[9px] text-brand-accent font-semibold flex items-center space-x-0.5">
            <TrendingUp class="w-3 h-3" />
            <span>Active enrollments</span>
          </p>
        </div>
        <div class="p-3 bg-brand-primary/10 border border-brand-primary/20 text-brand-primary rounded-xl">
          <Users class="w-6 h-6" />
        </div>
      </div>

      <!-- 2. Courses count -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Created Courses</p>
          <h3 class="text-2xl font-extrabold text-white">{{ courses.length }}</h3>
          <p class="text-[9px] text-gray-400 font-medium">Pending & approved</p>
        </div>
        <div class="p-3 bg-brand-accent/10 border border-brand-accent/20 text-brand-accent rounded-xl">
          <BookOpen class="w-6 h-6" />
        </div>
      </div>

      <!-- 3. Ratings -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Average Ratings</p>
          <h3 class="text-2xl font-extrabold text-white">{{ averageRating }} ★</h3>
          <p class="text-[9px] text-brand-warning font-semibold">100% Verified learner stars</p>
        </div>
        <div class="p-3 bg-brand-warning/10 border border-brand-warning/20 text-brand-warning rounded-xl">
          <Star class="w-6 h-6" />
        </div>
      </div>

      <!-- 4. Total Reviews -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Student Reviews</p>
          <h3 class="text-2xl font-extrabold text-white">{{ reviewsCount }}</h3>
          <p class="text-[9px] text-gray-400 font-medium">Verified learner comments</p>
        </div>
        <div class="p-3 bg-brand-primary/10 border border-brand-primary/20 text-brand-primary rounded-xl">
          <MessageSquare class="w-6 h-6" />
        </div>
      </div>

      <!-- 5. Total Earnings -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Est. Revenue</p>
          <h3 class="text-2xl font-extrabold text-white">₹{{ (totalEarnings / 100).toFixed(2) }}</h3>
          <p class="text-[9px] text-brand-primary font-semibold flex items-center space-x-0.5">
            <DollarSign class="w-3.5 h-3.5" />
            <span>70% Course Split</span>
          </p>
        </div>
        <div class="p-3 bg-brand-primary/10 border border-brand-primary/20 text-brand-primary rounded-xl">
          <DollarSign class="w-6 h-6" />
        </div>
      </div>
    </div>

    <!-- Estimated Revenue Split & Policy Disclosure -->
    <div class="glass-panel p-4.5 rounded-2xl border border-white/5 bg-brand-card/45 flex items-start space-x-3.5 shadow-xl animate-fade-in">
      <div class="p-2 bg-brand-primary/10 border border-brand-primary/20 text-brand-primary rounded-xl shrink-0 mt-0.5 animate-pulse">
        <DollarSign class="w-4 h-4" />
      </div>
      <div class="space-y-1 text-left">
        <h4 class="text-xs font-bold text-white tracking-wide">
          Estimated Revenue & Commission Split Disclosure
        </h4>
        <p class="text-[10px] md:text-xs text-gray-400 leading-relaxed font-light">
          Estimated earnings are computed based on standard payments and subject to a **70% Instructor / 30% Platform split** commission structure. Payouts displayed are net of refund provisions and platform reserves. Reconciled payouts may vary slightly due to gateway transaction processing fees, local taxes (GST), promotional student discounts, or standard currency conversions. Settlement reports are generated on the 1st of each month.
        </p>
      </div>
    </div>

    <!-- Visual Analytics Bar Chart -->
    <div class="space-y-4">
      <h2 class="text-lg font-bold text-white font-display flex items-center space-x-2">
        <TrendingUp class="w-4.5 h-4.5 text-brand-primary" />
        <span>Course Enrollments Chart</span>
      </h2>
      <div class="glass-panel p-5 rounded-3xl border border-white/5 bg-brand-card shadow-2xl h-[300px]">
        <Bar v-if="courses.length > 0" :data="chartData" :options="chartOptions" />
        <div v-else class="flex h-full items-center justify-center text-xs text-gray-500">
          No courses published yet to chart.
        </div>
      </div>
    </div>

    <!-- Courses Status Table -->
    <div class="space-y-4">
      <h2 class="text-lg font-bold text-white font-display">My Courses Catalog</h2>
      
      <div class="glass-panel rounded-3xl overflow-hidden border border-white/5 bg-brand-card shadow-2xl">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="bg-brand-dark/50 border-b border-white/5 text-gray-400 font-bold uppercase tracking-wider">
                <th class="px-6 py-4">Title & Details</th>
                <th class="px-6 py-4">Category</th>
                <th class="px-6 py-4">Status</th>
                <th class="px-6 py-4">Difficulty</th>
                <th class="px-6 py-4 text-center">Modules</th>
                <th class="px-6 py-4">Earnings</th>
                <th class="px-6 py-4">Action</th>
              </tr>
            </thead>
            
            <tbody v-if="courses.length > 0" class="divide-y divide-white/5">
              <tr v-for="course in courses" :key="course.id" class="hover:bg-white/[0.02] transition-colors">
                <!-- Title column -->
                <td class="px-6 py-4">
                  <div class="flex items-center space-x-3.5">
                    <img :src="course.thumbnail" :alt="course.title" class="w-10 h-10 rounded-lg object-cover bg-slate-800 shrink-0" />
                    <div class="truncate max-w-[240px]">
                      <h4 class="font-bold text-white truncate text-xs">{{ course.title }}</h4>
                      <p class="text-[10px] text-gray-400 truncate">{{ course.shortDescription || course.description }}</p>
                    </div>
                  </div>
                </td>

                <!-- Category -->
                <td class="px-6 py-4 font-semibold text-gray-300">{{ course.category }}</td>

                <!-- Status column -->
                <td class="px-6 py-4">
                  <div class="flex flex-col space-y-1">
                    <div class="flex items-center space-x-1.5">
                      <CheckCircle v-if="course.status === 'approved'" class="w-4 h-4 text-brand-accent shrink-0" />
                      <HelpCircle v-else-if="course.status === 'pending'" class="w-4 h-4 text-brand-warning shrink-0" />
                      <XCircle v-else class="w-4 h-4 text-brand-danger shrink-0" />
                      <span 
                        class="font-bold uppercase tracking-wider text-[10px]"
                        :class="{
                          'text-brand-accent': course.status === 'approved',
                          'text-brand-warning': course.status === 'pending',
                          'text-brand-danger': course.status === 'rejected',
                        }"
                      >
                        {{ course.status }}
                      </span>
                    </div>
                    <!-- Rejection Alert trigger -->
                    <div 
                      v-if="course.status === 'rejected' && course.rejectionReason"
                      class="flex flex-col p-2 rounded-lg bg-brand-danger/10 border border-brand-danger/20 text-[10px] text-brand-danger max-w-[200px] shadow-sm"
                    >
                      <div class="flex items-start space-x-1">
                        <AlertTriangle class="w-3.5 h-3.5 shrink-0 mt-0.5" />
                        <span class="leading-relaxed break-all whitespace-normal">
                          Reason: 
                          <template v-if="course.rejectionReason.length > 50">
                            <span v-if="expandedReasons[course.id]">
                              {{ course.rejectionReason }}
                            </span>
                            <span v-else>
                              {{ course.rejectionReason.slice(0, 45) }}...
                            </span>
                          </template>
                          <template v-else>
                            {{ course.rejectionReason }}
                          </template>
                        </span>
                      </div>
                      <button 
                        v-if="course.rejectionReason.length > 50"
                        @click="toggleReason(course.id)"
                        class="text-left font-bold underline hover:no-underline text-[9px] mt-1 ml-[18px] text-brand-danger focus:outline-none transition-colors"
                      >
                        {{ expandedReasons[course.id] ? 'View Less' : 'View More' }}
                      </button>
                    </div>
                  </div>
                </td>

                <!-- Difficulty -->
                <td class="px-6 py-4 font-medium text-gray-350">{{ course.difficulty }}</td>

                <!-- Modules count -->
                <td class="px-6 py-4 text-center font-bold text-white">{{ course.modules.length }}</td>

                <!-- Earnings column -->
                <td class="px-6 py-4 font-bold text-brand-accent">
                  ₹{{ (getCourseRevenue(course.id) / 100).toFixed(2) }}
                </td>

                <!-- Action button -->
                <td class="px-6 py-4 flex items-center space-x-2">
                  <router-link 
                    :to="`/courses/${course.id}`"
                    class="px-2.5 py-1.5 bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20 text-white rounded-lg transition-all font-semibold inline-block text-[11px]"
                  >
                    View
                  </router-link>
                  <router-link 
                    :to="`/teacher/edit/${course.id}`"
                    class="px-2.5 py-1.5 bg-brand-primary/20 border border-brand-primary/30 hover:bg-brand-primary text-white rounded-lg transition-all font-semibold inline-block text-[11px]"
                  >
                    Edit
                  </router-link>
                </td>
              </tr>
            </tbody>

            <!-- Empty table -->
            <tbody v-else>
              <tr>
                <td colspan="6" class="px-6 py-12 text-center text-gray-500 font-medium">
                  You haven't uploaded any courses yet. Click "Upload Course" to draft your first program.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Student Reviews Moderation Console -->
    <div class="space-y-4 pt-4">
      <h2 class="text-lg font-bold text-white font-display flex items-center space-x-2">
        <MessageSquare class="w-5 h-5 text-brand-primary" />
        <span>Syllabus Reviews Moderation</span>
      </h2>

      <div class="glass-panel rounded-3xl overflow-hidden border border-white/5 bg-brand-card shadow-2xl">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="bg-brand-dark/50 border-b border-white/5 text-gray-400 font-bold uppercase tracking-wider">
                <th class="px-6 py-4">Course</th>
                <th class="px-6 py-4">Student</th>
                <th class="px-6 py-4">Feedback</th>
                <th class="px-6 py-4 text-center">Rating</th>
                <th class="px-6 py-4">Visibility</th>
                <th class="px-6 py-4">Action</th>
              </tr>
            </thead>

            <tbody v-if="teacherReviews.length > 0" class="divide-y divide-white/5">
              <tr 
                v-for="rev in teacherReviews" 
                :key="rev.id" 
                class="hover:bg-white/[0.02] transition-colors"
                :class="{'opacity-60 bg-brand-dark/10': rev.hidden}"
              >
                <!-- Course Column -->
                <td class="px-6 py-4 font-bold text-white max-w-[160px] truncate">
                  {{ getCourseTitle(rev.courseId) }}
                </td>

                <!-- Student Column -->
                <td class="px-6 py-4">
                  <div class="flex items-center space-x-2">
                    <div class="w-6 h-6 rounded-full bg-brand-primary/15 text-brand-primary flex items-center justify-center font-bold text-[9px] uppercase">
                      {{ rev.studentName.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase() }}
                    </div>
                    <span class="font-semibold text-gray-300">{{ rev.studentName }}</span>
                  </div>
                </td>

                <!-- Feedback Comment -->
                <td class="px-6 py-4 text-gray-400 max-w-[280px] break-words whitespace-normal leading-relaxed font-light">
                  "{{ rev.comment }}"
                </td>

                <!-- Star Rating -->
                <td class="px-6 py-4 text-center shrink-0">
                  <div class="flex items-center justify-center space-x-0.5">
                    <Star 
                      v-for="star in 5" 
                      :key="star" 
                      class="w-3.5 h-3.5"
                      :class="star <= rev.rating ? 'text-brand-warning fill-brand-warning' : 'text-gray-600'"
                    />
                  </div>
                </td>

                <!-- Status Visibility -->
                <td class="px-6 py-4">
                  <span 
                    class="px-2.5 py-0.5 rounded-full border text-[9px] font-extrabold uppercase tracking-wider flex items-center space-x-1.5 w-fit"
                    :class="rev.hidden 
                      ? 'bg-brand-danger/10 text-brand-danger border-brand-danger/20' 
                      : 'bg-brand-accent/10 text-brand-accent border-brand-accent/20'"
                  >
                    <EyeOff v-if="rev.hidden" class="w-3 h-3" />
                    <Eye v-else class="w-3 h-3" />
                    <span>{{ rev.hidden ? 'Hidden' : 'Visible' }}</span>
                  </span>
                </td>

                <!-- Toggle Actions -->
                <td class="px-6 py-4">
                  <button 
                    @click="toggleReview(rev.id)"
                    :disabled="isTogglingReview[rev.id]"
                    class="px-3.5 py-1.5 rounded-xl border text-[11px] font-bold transition-all cursor-pointer flex items-center space-x-1 hover:scale-[1.03] active:scale-[0.97]"
                    :class="rev.hidden
                      ? 'bg-brand-accent/15 border-brand-accent/25 hover:bg-brand-accent text-white'
                      : 'bg-brand-danger/10 border-brand-danger/20 hover:bg-brand-danger text-white'"
                  >
                    <span>{{ rev.hidden ? 'Show Review' : 'Hide Review' }}</span>
                  </button>
                </td>
              </tr>
            </tbody>

            <tbody v-else>
              <tr>
                <td colspan="6" class="px-6 py-12 text-center text-gray-500 font-medium">
                  No student reviews have been left on your courses yet.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </div>
</template>
