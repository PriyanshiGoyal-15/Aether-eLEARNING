<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../../store/auth';
import { useRouter } from 'vue-router';
import { Award, AlertCircle, GraduationCap, User } from 'lucide-vue-next';

const authStore = useAuthStore();
const router = useRouter();

const name = ref('');
const email = ref('');
const password = ref('');
const role = ref('student'); // student or teacher
const errorMsg = ref('');

const handleRegister = async () => {
  errorMsg.value = '';
  
  if (!name.value || !email.value || !password.value) {
    errorMsg.value = 'Please complete all required fields.';
    return;
  }

  if (password.value.length < 6) {
    errorMsg.value = 'Password must consist of at least 6 characters.';
    return;
  }

  try {
    const user = await authStore.register(name.value, email.value, password.value, role.value);
    
    // Auto-logged in on register, forward to appropriate dashboard
    if (user.role === 'student') router.push('/student/dashboard');
    else if (user.role === 'teacher') router.push('/teacher/dashboard');
  } catch (err) {
    errorMsg.value = err.message || 'Registration failed. Try again.';
  }
};
</script>

<template>
  <div class="min-h-[75vh] flex items-center justify-center py-8">
    <div class="w-full max-w-md space-y-6">
      
      <!-- Register Glass Panel Container -->
      <div class="glass-panel rounded-3xl p-8 border border-white/5 bg-brand-card shadow-2xl space-y-6">
        
        <!-- Header -->
        <div class="flex flex-col items-center text-center space-y-2">
          <span class="p-3 rounded-2xl bg-gradient-to-tr from-brand-primary to-brand-secondary text-white shadow-lg shadow-brand-primary/10">
            <Award class="w-7 h-7" />
          </span>
          <h2 class="text-2xl font-bold tracking-tight text-white font-display pt-2">Join Aether Today</h2>
          <p class="text-xs text-gray-400">Register your account to unlock learning and educator portals</p>
        </div>

        <!-- Error Panel -->
        <div 
          v-if="errorMsg" 
          class="flex items-start space-x-2.5 p-3 rounded-xl bg-brand-danger/10 border border-brand-danger/25 text-brand-danger text-xs animate-fade-in"
        >
          <AlertCircle class="w-4 h-4 shrink-0 mt-0.5" />
          <span class="font-medium leading-relaxed">{{ errorMsg }}</span>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleRegister" class="space-y-4">
          <!-- Role selector segment chips -->
          <div class="space-y-2">
            <label class="text-xs font-semibold text-gray-400 block mb-1">Choose Account Role</label>
            <div class="grid grid-cols-2 gap-3">
              <button 
                type="button"
                @click="role = 'student'"
                class="flex items-center justify-center space-x-2 py-3 rounded-xl text-xs font-bold border transition-all"
                :class="role === 'student'
                  ? 'bg-brand-primary/20 text-brand-primary border-brand-primary shadow-inner shadow-brand-primary/5' 
                  : 'bg-brand-dark/40 text-gray-450 border-white/10 hover:bg-white/5'"
              >
                <GraduationCap class="w-4.5 h-4.5" />
                <span>Student</span>
              </button>
              
              <button 
                type="button"
                @click="role = 'teacher'"
                class="flex items-center justify-center space-x-2 py-3 rounded-xl text-xs font-bold border transition-all"
                :class="role === 'teacher'
                  ? 'bg-brand-accent/20 text-brand-accent border-brand-accent shadow-inner shadow-brand-accent/5' 
                  : 'bg-brand-dark/40 text-gray-450 border-white/10 hover:bg-white/5'"
              >
                <User class="w-4.5 h-4.5" />
                <span>Teacher</span>
              </button>
            </div>
          </div>

          <!-- Full Name -->
          <div class="space-y-1.5">
            <label for="name" class="text-xs font-semibold text-gray-400">Full Name</label>
            <input 
              v-model="name" 
              type="text" 
              id="name" 
              required 
              placeholder="e.g. Priyanshi Sharma" 
              class="w-full pl-4 pr-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
            />
          </div>

          <!-- Email Address -->
          <div class="space-y-1.5">
            <label for="email" class="text-xs font-semibold text-gray-400">Email Address</label>
            <input 
              v-model="email" 
              type="email" 
              id="email" 
              required 
              placeholder="name@example.com" 
              class="w-full pl-4 pr-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
            />
          </div>

          <!-- Password -->
          <div class="space-y-1.5">
            <label for="password" class="text-xs font-semibold text-gray-400">Password</label>
            <input 
              v-model="password" 
              type="password" 
              id="password" 
              required 
              placeholder="Minimum 6 characters" 
              class="w-full pl-4 pr-4 py-2.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary/50 focus:border-brand-primary transition-all duration-300"
            />
          </div>

          <!-- Submit Register Button -->
          <button 
            type="submit" 
            class="w-full py-2.5 text-xs font-bold rounded-xl text-white shadow-lg transition-all glow-btn mt-6"
            :class="role === 'student' 
              ? 'bg-brand-primary hover:bg-brand-secondary shadow-brand-primary/20' 
              : 'bg-brand-accent hover:bg-emerald-600 shadow-brand-accent/20'"
          >
            Create Platform Account
          </button>
        </form>

        <!-- Redirect back to Sign In -->
        <div class="text-center text-xs text-gray-400 pt-2">
          <span>Already registered? </span>
          <router-link to="/login" class="font-bold text-brand-primary hover:text-brand-secondary">Sign In here</router-link>
        </div>

      </div>
    </div>
  </div>
</template>
