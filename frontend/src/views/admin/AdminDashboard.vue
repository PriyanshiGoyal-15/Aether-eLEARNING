<script setup>
import { computed, ref, onMounted } from 'vue';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { Bar } from 'vue-chartjs';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import { useRouter } from 'vue-router';
import { 
  ShieldCheck, Users, BookOpen, Clock, ClipboardCheck, 
  TrendingUp, Award, ArrowRight, UserCheck, Star, DollarSign
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const router = useRouter();

const adminStats = computed(() => coursesStore.getAdminStats);
const popularCourses = computed(() => adminStats.value.popularCourses);

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const chartData = computed(() => {
  return {
    labels: popularCourses.value.map(c => c.title.substring(0, 15) + (c.title.length > 15 ? '...' : '')),
    datasets: [
      {
        label: 'Course Enrollments',
        backgroundColor: '#6366f1', // brand-primary
        borderRadius: 6,
        data: popularCourses.value.map(c => c.enrollmentsCount)
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

const getCourseAdminRevenue = (courseId) => {
  return coursesStore.payments
    .filter(p => p.status === 'captured' && p.courseId === courseId)
    .reduce((sum, p) => sum + (p.adminRevenue || 0), 0);
};
</script>

<template>
  <div class="space-y-10 py-4">
    <!-- Welcome Header & Actions -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="space-y-1.5">
        <h1 class="text-2xl md:text-3xl font-extrabold text-white font-display flex items-center space-x-2">
          <ShieldCheck class="w-7 h-7 text-brand-warning" />
          <span>Admin Analytics Control</span>
        </h1>
        <p class="text-xs text-gray-450">Monitor platform activity, manage registered accounts, and moderate course listings.</p>
      </div>

      <!-- Action buttons -->
      <div class="flex flex-wrap items-center gap-3 shrink-0">
        <router-link 
          to="/admin/users"
          class="px-4.5 py-2.5 bg-white/5 border border-white/10 text-xs font-semibold text-gray-300 hover:text-white rounded-xl transition-all flex items-center space-x-1.5"
        >
          <UserCheck class="w-4 h-4" />
          <span>Manage User Accounts</span>
        </router-link>

        <router-link 
          to="/admin/approvals"
          class="px-5 py-2.5 bg-brand-primary hover:bg-brand-secondary text-white text-xs font-bold rounded-xl transition-all shadow-md shadow-brand-primary/15 flex items-center space-x-1.5"
        >
          <ClipboardCheck class="w-4 h-4" />
          <span>Approval Courses Queue</span>
        </router-link>
      </div>
    </div>

    <!-- Stats Grid cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- 1. Total Students -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-450 uppercase tracking-widest">Global Learners</p>
          <h3 class="text-2xl font-extrabold text-white">{{ adminStats.totalStudents }}</h3>
          <p class="text-[9px] text-brand-primary font-semibold flex items-center space-x-0.5">
            <Users class="w-3.5 h-3.5" />
            <span>Registered students</span>
          </p>
        </div>
        <div class="p-3 bg-brand-primary/10 border border-brand-primary/20 text-brand-primary rounded-xl">
          <Users class="w-6 h-6" />
        </div>
      </div>

      <!-- 2. Active Teachers -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-450 uppercase tracking-widest">Active Instructors</p>
          <h3 class="text-2xl font-extrabold text-white">{{ adminStats.totalTeachers }}</h3>
          <p class="text-[9px] text-brand-accent font-semibold flex items-center space-x-0.5">
            <UserCheck class="w-3.5 h-3.5" />
            <span>Active educators</span>
          </p>
        </div>
        <div class="p-3 bg-brand-accent/10 border border-brand-accent/20 text-brand-accent rounded-xl">
          <UserCheck class="w-6 h-6" />
        </div>
      </div>

      <!-- 3. Approved Courses -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-450 uppercase tracking-widest">Active Approved Programs</p>
          <h3 class="text-2xl font-extrabold text-white">{{ adminStats.activeCourses }}</h3>
          <p class="text-[9px] text-gray-400 font-medium">Visible to student list</p>
        </div>
        <div class="p-3 bg-brand-primary/10 border border-brand-primary/20 text-brand-primary rounded-xl">
          <BookOpen class="w-6 h-6" />
        </div>
      </div>

      <!-- 4. Pending Queue -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between" :class="{'border-brand-warning/35 bg-brand-warning/[0.02]': adminStats.pendingApprovals > 0}">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-450 uppercase tracking-widest">Awaiting Moderation</p>
          <h3 class="text-2xl font-extrabold" :class="adminStats.pendingApprovals > 0 ? 'text-brand-warning' : 'text-white'">
            {{ adminStats.pendingApprovals }}
          </h3>
          <p class="text-[9px] font-semibold flex items-center space-x-0.5 animate-pulse" :class="adminStats.pendingApprovals > 0 ? 'text-brand-warning' : 'text-gray-400'">
            <ClipboardCheck class="w-3.5 h-3.5" />
            <span>Review required</span>
          </p>
        </div>
        <div 
          class="p-3 rounded-xl border"
          :class="adminStats.pendingApprovals > 0 
            ? 'bg-brand-warning/15 border-brand-warning/25 text-brand-warning' 
            : 'bg-white/5 border-white/5 text-gray-400'"
        >
          <ClipboardCheck class="w-6 h-6" />
        </div>
      </div>
      

      <!-- 5. Platform Revenue -->
      <div class="glass-panel p-5 rounded-2xl border border-white/5 bg-brand-card flex items-center justify-between">
        <div class="space-y-2">
          <p class="text-[10px] font-bold text-gray-450 uppercase tracking-widest">Platform Revenue</p>
          <h3 class="text-2xl font-extrabold text-white">₹{{ (adminStats.totalRevenue / 100).toFixed(2) }}</h3>
          <p class="text-[9px] text-brand-primary font-semibold flex items-center space-x-0.5">
            <TrendingUp class="w-3.5 h-3.5" />
            <span>30% Admin Split</span>
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
          Platform Revenue & Commission Split Disclosure
        </h4>
     <p class="text-[10px] md:text-xs text-gray-400 leading-relaxed font-light">
  Platform revenue displays aggregate platform earnings net of instructor payables under our standard<strong class="text-white font-bold"> 70% Instructor / 30% Platform split</strong>
  commission structure. Platform revenue records are processed net of refund holds and regional banking transactional overheads. Monthly platform settlements are reconciled on the 1st of each calendar month.
</p>
      </div>
    </div>

    <!-- Analytics Graphs & Popular programs details -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
      
      <!-- Popular Programs Roster -->
      <div class="lg:col-span-2 space-y-4">
        <h2 class="text-lg font-bold text-white font-display flex items-center space-x-2">
          <TrendingUp class="w-4.5 h-4.5 text-brand-primary" />
          <span>Platform Course Popularity Matrix</span>
        </h2>

        <div class="glass-panel rounded-3xl overflow-hidden border border-white/5 bg-brand-card shadow-2xl">
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border-collapse">
              <thead>
                <tr class="bg-brand-dark/50 border-b border-white/5 text-gray-400 font-bold uppercase tracking-wider">
                  <th class="px-6 py-4">Course Name</th>
                  <th class="px-6 py-4">Topic Category</th>
                  <th class="px-6 py-4">Reviews Score</th>
                  <th class="px-6 py-4 text-center">Enrollments</th>
                  <th class="px-6 py-4">Admin Revenue</th>
                </tr>
              </thead>
              
              <tbody v-if="popularCourses.length > 0" class="divide-y divide-white/5">
                <tr v-for="(course, idx) in popularCourses" :key="idx" class="hover:bg-white/[0.02] transition-colors">
                  <td class="px-6 py-4 font-bold text-white max-w-[200px] truncate" :title="course.title">
                    {{ course.title }}
                  </td>
                  <td class="px-6 py-4 font-semibold text-gray-300">{{ course.category }}</td>
                  <td class="px-6 py-4">
                    <div class="flex items-center space-x-1">
                      <Star class="w-3.5 h-3.5 text-brand-warning fill-brand-warning" />
                      <span class="font-bold text-gray-250">{{ course.rating.toFixed(1) }}</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 text-center font-bold text-brand-accent">{{ course.enrollmentsCount }} learners</td>
                  <td class="px-6 py-4 font-bold text-brand-primary">
                    ₹{{ (getCourseAdminRevenue(course.id) / 100).toFixed(2) }}
                  </td>
                </tr>
              </tbody>

              <tbody v-else>
                <tr>
                  <td colspan="4" class="px-6 py-12 text-center text-gray-500 font-medium">
                    Not enough data generated yet. Waiting for learner activity.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <!-- Visual Analytics Bar Chart -->
      <div class="lg:col-span-1 space-y-4">
        <h2 class="text-lg font-bold text-white font-display flex items-center space-x-2">
          <TrendingUp class="w-4.5 h-4.5 text-brand-primary" />
          <span>Enrollments Graph</span>
        </h2>
        <div class="glass-panel p-5 rounded-3xl border border-white/5 bg-brand-card shadow-2xl h-[300px]">
          <Bar v-if="popularCourses.length > 0" :data="chartData" :options="chartOptions" />
          <div v-else class="flex h-full items-center justify-center text-xs text-gray-500">
            No active enrollment data to chart.
          </div>
        </div>
      </div>

    </div>
  </div>
</template>
