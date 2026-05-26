<script setup>
import { computed } from 'vue';
import { useCoursesStore } from '../../store/courses';
import { useAuthStore } from '../../store/auth';
import { useRouter } from 'vue-router';
import { 
  ShieldCheck, Users, BookOpen, Clock, ClipboardCheck, 
  TrendingUp, Award, ArrowRight, UserCheck, Star
} from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();
const router = useRouter();

const adminStats = computed(() => coursesStore.getAdminStats);
const popularCourses = computed(() => adminStats.value.popularCourses);
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
          <span>Moderate Courses Queue</span>
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
                </tr>
              </tbody>

              <tbody v-else>
                <tr>
                  <td colspan="4" class="px-6 py-12 text-center text-gray-500 font-medium">
                    No active student enrollments located in platform databases.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Quick Platform tips card -->
      <div class="glass-panel rounded-3xl p-6 border border-white/5 bg-brand-card flex flex-col space-y-4 text-xs text-gray-300">
        <h3 class="text-sm font-bold text-white font-display flex items-center space-x-2">
          <ShieldCheck class="w-4.5 h-4.5 text-brand-warning" />
          <span>Operational Control Guidelines</span>
        </h3>
        
        <p class="leading-relaxed">
          As an Administrator, you have complete governance over Aether Academy's course listings.
        </p>

        <div class="border-t border-white/5 pt-4 space-y-3">
          <div class="flex items-start space-x-2.5">
            <span class="p-1 rounded bg-brand-warning/15 border border-brand-warning/25 text-brand-warning font-bold text-[9px] mt-0.5">QUEUE</span>
            <p>Courses drafted by teachers are set to "Pending" and must be manually inspected and resolved.</p>
          </div>
          <div class="flex items-start space-x-2.5">
            <span class="p-1 rounded bg-brand-danger/15 border border-brand-danger/25 text-brand-danger font-bold text-[9px] mt-0.5">BAN</span>
            <p>You can suspend student/instructor accounts to immediately block platform login permissions.</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>
