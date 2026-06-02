<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';
import { Compass, ArrowLeft, Home, BookOpen, LayoutDashboard } from 'lucide-vue-next';

const router = useRouter();
const authStore = useAuthStore();

const goBack = () => {
  router.back();
};

const goHome = () => {
  if (authStore.isAuthenticated) {
    if (authStore.isStudent) router.push('/student/dashboard');
    else if (authStore.isTeacher) router.push('/teacher/dashboard');
    else if (authStore.isAdmin) router.push('/admin/dashboard');
  } else {
    router.push('/');
  }
};
</script>

<template>
  <div class="min-h-[80vh] flex items-center justify-center p-6">
    <div class="max-w-2xl w-full flex flex-col items-center text-center space-y-8 animate-fade-in relative z-10">
      
      <!-- Glowing Background Orb -->
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-brand-primary/10 rounded-full blur-[100px] pointer-events-none -z-10"></div>

      <!-- Icon & Status -->
      <div class="space-y-4">
        <div class="relative inline-block">
          <div class="absolute inset-0 bg-brand-primary/20 blur-xl rounded-full"></div>
          <Compass class="w-32 h-32 text-brand-primary animate-pulse relative z-10" stroke-width="1.5" />
        </div>
        <h1 class="text-8xl font-black text-white font-display tracking-tight leading-none text-glow-primary opacity-90">
          404
        </h1>
      </div>

      <!-- Text -->
      <div class="space-y-3 max-w-lg">
        <h2 class="text-2xl md:text-3xl font-bold text-white tracking-wide">
          Signal Lost in the Void
        </h2>
        <p class="text-gray-400 font-light leading-relaxed">
          The page you're looking for has either drifted into deep space, been deleted, or never existed in the first place.
        </p>
      </div>

      <!-- Actions -->
      <div class="flex flex-col sm:flex-row items-center gap-4 pt-4 w-full justify-center">
        <button 
          @click="goBack"
          class="w-full sm:w-auto px-6 py-3.5 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-white font-bold transition-all duration-300 flex items-center justify-center space-x-2"
        >
          <ArrowLeft class="w-4.5 h-4.5" />
          <span>Go Back</span>
        </button>
        
        <button 
          @click="goHome"
          class="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-brand-primary hover:bg-brand-secondary text-white font-bold transition-all duration-300 shadow-lg shadow-brand-primary/20 hover:shadow-brand-primary/40 flex items-center justify-center space-x-2 btn-glow"
        >
          <LayoutDashboard v-if="authStore.isAuthenticated" class="w-4.5 h-4.5" />
          <Home v-else class="w-4.5 h-4.5" />
          <span>Return to Safety</span>
        </button>
      </div>

      <!-- Decorative Grid/Line -->
      <div class="pt-12 w-full max-w-md mx-auto flex items-center justify-center space-x-2 opacity-30 select-none">
        <div class="h-px bg-gradient-to-r from-transparent to-white flex-1"></div>
        <span class="w-2 h-2 rounded-full bg-brand-primary"></span>
        <span class="w-1.5 h-1.5 rounded-full bg-brand-accent"></span>
        <span class="w-2 h-2 rounded-full bg-brand-primary"></span>
        <div class="h-px bg-gradient-to-l from-transparent to-white flex-1"></div>
      </div>
    </div>
  </div>
</template>
