<script setup>
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
import { useAuthStore } from './store/auth';
import { useCoursesStore } from './store/courses';
import { useRouter } from 'vue-router';
import { 
  Shield, User, GraduationCap, LogOut, RotateCcw, 
  CheckCircle, BellRing, Settings
} from 'lucide-vue-next';

import { onMounted } from 'vue';

const authStore = useAuthStore();
const coursesStore = useCoursesStore();
const router = useRouter();

onMounted(async () => {
  await coursesStore.fetchCoursesData();
  await authStore.fetchUsers();
});

const quickLogin = (role) => {
  try {
    let email = '';
    let password = '';
    
    if (role === 'student') {
      email = 'student@aether.edu';
      password = 'student123';
    } else if (role === 'teacher') {
      email = 'teacher@aether.edu';
      password = 'teacher123';
    } else if (role === 'admin') {
      email = 'admin@aether.edu';
      password = 'admin123';
    }
    
    authStore.login(email, password);
    
    // Redirect to the appropriate dashboard
    if (role === 'student') router.push('/student/dashboard');
    else if (role === 'teacher') router.push('/teacher/dashboard');
    else if (role === 'admin') router.push('/admin/dashboard');
  } catch (err) {
    alert(err.message);
  }
};

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};

// Developer Action Shortcuts
const triggerAutoComplete = () => {
  if (!authStore.isAuthenticated || !authStore.isStudent) {
    alert("Please log in as a Student first to auto-complete the course!");
    return;
  }
  
  // Auto complete "course-vue"
  coursesStore.enrollInCourse(authStore.currentUser.id, 'course-vue');
  coursesStore.autoCompleteCourse(authStore.currentUser.id, 'course-vue');
  
  alert("Mastering Vue 3 course instantly set to 100%! Claim your certificate in your Dashboard.");
};

const triggerMockNotification = () => {
  if (!authStore.isAuthenticated) {
    alert("Please log in first to receive a simulated alert!");
    return;
  }
  
  coursesStore.addNotification(
    authStore.currentUser.id,
    "Academic Achievement Unlocked! 🌟",
    "Your recent learning assignment was graded. You scored 100%! Keep up the amazing streak.",
    "success"
  );
  
  alert("Notification alert pushed! Click the bell icon in the Navbar header.");
};

const triggerDbReset = () => {
  const confirmReset = confirm("Reset database records? All session logs and created programs will revert to factory defaults.");
  if (confirmReset) {
    coursesStore.resetDatabase();
  }
};
</script>

<template>
  <div class="flex flex-col min-h-screen glow-bg">
    <!-- Navigation -->
    <Navbar />

    <!-- Main Router View -->
    <main class="flex-grow container mx-auto px-4 py-8">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <Footer />

    <!-- Developer Sandbox Switcher & Tools Panel -->
    <!-- <div class="fixed bottom-6 right-6 z-50 group">
      <div class="flex flex-col-reverse items-end space-y-2 space-y-reverse">
        <button class="bg-brand-primary text-white p-3.5 rounded-full shadow-xl shadow-brand-primary/30 flex items-center justify-center hover:bg-brand-secondary opacity-0 group-hover:opacity-100 transition-all duration-300 cursor-pointer">
          <Shield class="w-6 h-6 animate-pulse" />
        </button>
        
        <div class="bg-brand-card border border-white/10 rounded-2xl shadow-2xl p-4.5 w-64 transform scale-95 opacity-0 pointer-events-none group-hover:scale-100 group-hover:opacity-100 group-hover:pointer-events-auto transition-all duration-300 origin-bottom-right space-y-4">
          
          <div>
            <h4 class="text-[10px] font-bold text-gray-550 uppercase tracking-widest mb-2.5">Demo Presets Logins</h4>
            <div class="space-y-1.5">
              <button 
                @click="quickLogin('student')" 
                class="w-full text-left flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs transition-colors cursor-pointer"
                :class="authStore.isStudent ? 'bg-brand-primary text-white font-semibold' : 'hover:bg-white/5 text-gray-300'"
              >
                <GraduationCap class="w-4 h-4" />
                <span>Login as Student</span>
              </button>
              
              <button 
                @click="quickLogin('teacher')" 
                class="w-full text-left flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs transition-colors cursor-pointer"
                :class="authStore.isTeacher ? 'bg-brand-accent text-white font-semibold' : 'hover:bg-white/5 text-gray-300'"
              >
                <User class="w-4 h-4" />
                <span>Login as Teacher</span>
              </button>
              
              <button 
                @click="quickLogin('admin')" 
                class="w-full text-left flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs transition-colors cursor-pointer"
                :class="authStore.isAdmin ? 'bg-brand-warning text-white font-semibold' : 'hover:bg-white/5 text-gray-300'"
              >
                <Shield class="w-4 h-4" />
                <span>Login as Admin</span>
              </button>
            </div>
          </div>

          <div class="pt-3 border-t border-white/5">
            <h4 class="text-[10px] font-bold text-gray-550 uppercase tracking-widest mb-2.5">Sandbox Shortcuts</h4>
            <div class="space-y-1.5">
              <button 
                @click="triggerAutoComplete" 
                class="w-full text-left flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs text-gray-300 hover:text-white hover:bg-white/5 transition-colors cursor-pointer"
              >
                <CheckCircle class="w-4 h-4 text-brand-accent" />
                <span>Auto-Complete Course</span>
              </button>

              <button 
                @click="triggerMockNotification" 
                class="w-full text-left flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs text-gray-300 hover:text-white hover:bg-white/5 transition-colors cursor-pointer"
              >
                <BellRing class="w-4 h-4 text-brand-primary" />
                <span>Simulate Platform Alert</span>
              </button>

              <button 
                @click="triggerDbReset" 
                class="w-full text-left flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs text-brand-danger hover:bg-brand-danger/10 transition-colors cursor-pointer font-medium"
              >
                <RotateCcw class="w-4 h-4 shrink-0" />
                <span>Factory Reset DB</span>
              </button>
            </div>
          </div>

          <div v-if="authStore.isAuthenticated" class="pt-3 border-t border-white/5">
            <button 
              @click="handleLogout" 
              class="w-full text-left flex items-center space-x-2.5 px-3 py-2 rounded-xl text-xs text-brand-danger hover:bg-brand-danger/10 transition-colors cursor-pointer font-medium"
            >
              <LogOut class="w-4 h-4" />
              <span>Quick Logout</span>
            </button>
          </div>
          
          <div class="text-[9px] text-gray-500 text-center select-none pt-1">
            Active: <strong class="text-brand-accent">{{ authStore.currentUser ? authStore.currentUser.name : 'Guest' }}</strong>
          </div>
        </div>
      </div>
    </div> -->
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(6px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
