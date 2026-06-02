<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../../store/auth';
import { useRouter, useRoute } from 'vue-router';
import { Shield, Eye, EyeOff, Award, AlertCircle } from 'lucide-vue-next';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const email = ref('');
const password = ref('');
const showPassword = ref(false);
const errorMsg = ref('');
const isLoading = ref(false);

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const handleLogin = async () => {
  errorMsg.value = '';
  if (!email.value || !password.value) {
    errorMsg.value = 'Please complete all required fields.';
    return;
  }

  isLoading.value = true;

  try {
    const user = await authStore.login(email.value, password.value);
    
    // Redirect to requested redirect or fallback to role dashboard
    const redirectPath = route.query.redirect;
    if (redirectPath) {
      router.push(redirectPath);
      return;
    }

    if (user.role === 'student') router.push('/student/dashboard');
    else if (user.role === 'teacher') router.push('/teacher/dashboard');
    else if (user.role === 'admin') router.push('/admin/dashboard');
  } catch (err) {
    errorMsg.value = err.message || 'Login failed. Please check credentials.';
  } finally {
    isLoading.value = false;
  }
};

const fillDemoCredentials = async (role) => {
  if (role === 'student') {
    email.value = 'student@aether.edu';
    password.value = 'student123';
  } else if (role === 'teacher') {
    email.value = 'teacher@aether.edu';
    password.value = 'teacher123';
  } else if (role === 'admin') {
    email.value = 'admin@aether.edu';
    password.value = 'admin123';
  }
  await handleLogin();
};
</script>

<template>
  <div class="min-h-[75vh] flex items-center justify-center py-8">
    <div class="w-full max-w-md space-y-6">
      
      <!-- Login Glass Box Panel -->
      <div class="glass-panel rounded-3xl p-8 border border-white/5 bg-brand-card shadow-2xl space-y-6">
        
        <!-- Header logo/text -->
        <div class="flex flex-col items-center text-center space-y-2">
          <span class="p-3 rounded-2xl bg-linear-to-tr from-brand-primary to-brand-secondary text-white shadow-lg shadow-brand-primary/10">
            <Award class="w-7 h-7" />
          </span>
          <h2 class="text-2xl font-bold tracking-tight text-white font-display pt-2">Sign In to Aether</h2>
          <p class="text-xs text-gray-400">Access your courses, dashboards and academic analytics</p>
        </div>

        <!-- Error Alert Bar -->
        <div 
          v-if="errorMsg" 
          class="flex items-start space-x-2.5 p-3 rounded-xl bg-brand-danger/10 border border-brand-danger/25 text-brand-danger text-xs animate-fade-in"
        >
          <AlertCircle class="w-4 h-4 shrink-0 mt-0.5" />
          <span class="font-medium leading-relaxed">{{ errorMsg }}</span>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <!-- Email Input -->
          <div class="space-y-1.5">
            <label for="email" class="text-xs font-semibold text-gray-400">Email Address</label>
            <input 
              v-model="email" 
              type="email" 
              id="email" 
              required 
              placeholder="name@aether.edu" 
              class="w-full pl-4 pr-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
            />
          </div>

          <!-- Password Input -->
          <div class="space-y-1.5">
            <div class="flex justify-between items-center">
              <label for="password" class="text-xs font-semibold text-gray-400">Password</label>
              <a href="#" class="text-[10px] font-semibold text-brand-primary hover:text-brand-secondary">Forgot?</a>
            </div>
            <div class="relative">
              <input 
                v-model="password" 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                required 
                placeholder="••••••••" 
                class="w-full pl-4 pr-10 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
              />
              <button 
                type="button" 
                @click="togglePasswordVisibility" 
                class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
              >
                <EyeOff v-if="showPassword" class="w-4 h-4" />
                <Eye v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- Sign-In CTA button -->
          <button 
            type="submit"
            :disabled="isLoading"
            class="w-full py-2.5 bg-brand-primary text-white text-xs font-bold rounded-xl shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-all glow-btn mt-6 flex items-center justify-center space-x-2 disabled:opacity-70 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading" class="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></span>
            <span>{{ isLoading ? 'Authenticating...' : 'Sign In Account' }}</span>
          </button>
        </form>

        <!-- Redirect to Registration -->
        <div class="text-center text-xs text-gray-400 pt-2">
          <span>New to Aether? </span>
          <router-link to="/register" class="font-bold text-brand-primary hover:text-brand-secondary">Create free account</router-link>
        </div>

        <!-- Divider line -->
        <div class="relative flex items-center justify-center pt-4">
          <div class="absolute inset-0 flex items-center"><div class="w-full border-t border-white/5"></div></div>
          <span class="relative bg-brand-card px-3 text-[10px] font-semibold text-gray-500 uppercase tracking-widest">Demo Sandbox Logins</span>
        </div>

        <!-- Demo Accounts Autofill Grids -->
        <div class="grid grid-cols-3 gap-2">
          <button 
            @click="fillDemoCredentials('student')" 
            class="px-2 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 text-[10px] font-bold text-gray-300 hover:text-white transition-all text-center flex flex-col items-center justify-center gap-1 shrink-0"
          >
            <span class="text-brand-primary font-bold">Student</span>
            <span class="text-[8px] font-normal text-gray-500">priyanshi</span>
          </button>
          <button 
            @click="fillDemoCredentials('teacher')" 
            class="px-2 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 text-[10px] font-bold text-gray-300 hover:text-white transition-all text-center flex flex-col items-center justify-center gap-1 shrink-0"
          >
            <span class="text-brand-accent font-bold">Teacher</span>
            <span class="text-[8px] font-normal text-gray-500">jenkins</span>
          </button>
          <button 
            @click="fillDemoCredentials('admin')" 
            class="px-2 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 text-[10px] font-bold text-gray-300 hover:text-white transition-all text-center flex flex-col items-center justify-center gap-1 shrink-0"
          >
            <span class="text-brand-warning font-bold">Admin</span>
            <span class="text-[8px] font-normal text-gray-500">system</span>
          </button>
        </div>

      </div>
    </div>
  </div>
</template>
