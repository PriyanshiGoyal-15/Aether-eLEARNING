<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../../store/auth';
import { useRouter } from 'vue-router';
import { Award, AlertCircle, GraduationCap, User, FileText, CheckCircle, ArrowLeft, ArrowRight } from 'lucide-vue-next';

const authStore = useAuthStore();
const router = useRouter();

const name = ref('');
const email = ref('');
const password = ref('');
const role = ref('student'); // student or teacher
const verificationDoc = ref('');
const errorMsg = ref('');
const isRegisteredPending = ref(false);
const currentStep = ref(1); // Step 1: Account details, Step 2: Verification upload (Teachers only)

const handleNextStep = () => {
  errorMsg.value = '';
  
  if (!name.value || !email.value || !password.value) {
    errorMsg.value = 'Please complete all required fields.';
    return;
  }

  if (password.value.length < 6) {
    errorMsg.value = 'Password must consist of at least 6 characters.';
    return;
  }

  // If student, go straight to registration submission
  if (role.value === 'student') {
    handleRegister();
  } else {
    // If teacher, advance to Step 2 for credentials upload
    currentStep.value = 2;
  }
};

const handleRegister = async () => {
  errorMsg.value = '';

  if (role.value === 'teacher' && !verificationDoc.value.trim()) {
    errorMsg.value = 'Please specify credentials or qualifications for verification.';
    return;
  }

  try {
    const user = await authStore.register(
      name.value, 
      email.value, 
      password.value, 
      role.value, 
      role.value === 'teacher' ? verificationDoc.value.trim() : null
    );
    
    if (user.role === 'teacher') {
      isRegisteredPending.value = true;
    } else {
      router.push('/student/dashboard');
    }
  } catch (err) {
    errorMsg.value = err.message || 'Registration failed. Try again.';
  }
};
</script>

<template>
  <div class="min-h-[75vh] flex items-center justify-center py-8">
    <div class="w-full max-w-md space-y-6">
      
      <!-- Register Glass Panel Container -->
      <div class="glass-panel rounded-3xl p-8 border border-white/5 bg-brand-card shadow-2xl">
        
        <!-- Case A: Teacher Registration Awaiting Verification Status UI -->
        <div v-if="isRegisteredPending" class="flex flex-col items-center text-center space-y-6 py-2 animate-fade-in">
          <span class="p-4 rounded-3xl bg-brand-accent/10 border border-brand-accent/25 text-brand-accent shadow-lg shadow-brand-accent/10">
            <CheckCircle class="w-10 h-10" />
          </span>
          <h2 class="text-xl md:text-2xl font-extrabold tracking-tight text-white font-display">Application Received!</h2>
          
          <div class="space-y-4 text-xs text-gray-300 leading-relaxed font-light px-1">
            <p>
              Thank you for applying as an educator at Aether. To maintain strict educational authenticity, your account requires verified administrator approval.
            </p>
            
            <div class="p-4.5 bg-brand-dark/45 border border-white/5 rounded-2xl text-left space-y-3 text-xs text-gray-400">
              <h4 class="font-bold text-white uppercase tracking-wider text-[10px] text-brand-accent">Next Verification Steps:</h4>
              <ul class="list-disc pl-4 space-y-2 text-[11px] leading-relaxed">
                <li>We have logged your application under address <strong>{{ email }}</strong>.</li>
                <li>A verification process guide has been sent to your email.</li>
                <li>Administrator credentials review takes <strong>4-5 business days</strong>.</li>
                <li>Your profile is currently locked and cannot log in.</li>
                <li>You will receive an approval success email once verified!</li>
              </ul>
            </div>
          </div>

          <button 
            @click="router.push('/login')" 
            class="w-full py-3 bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-bold rounded-xl text-white transition-all shadow-md mt-4 cursor-pointer"
          >
            Return to Sign In
          </button>
        </div>

        <!-- Case B: Multi-Step Form UI -->
        <div v-else class="space-y-6 animate-fade-in">
          
          <!-- Step 2 Navigation Back arrow -->
          <button 
            v-if="currentStep === 2"
            @click="currentStep = 1"
            class="flex items-center space-x-1.5 text-xs text-gray-400 hover:text-white transition-colors cursor-pointer mb-2"
          >
            <ArrowLeft class="w-4 h-4" />
            <span>Back to Step 1: Account Info</span>
          </button>

          <!-- Header -->
          <div class="flex flex-col items-center text-center space-y-2">
            <span class="p-3 rounded-2xl bg-gradient-to-tr from-brand-primary to-brand-secondary text-white shadow-lg shadow-brand-primary/10">
              <Award class="w-7 h-7" />
            </span>
            <h2 class="text-2xl font-bold tracking-tight text-white font-display pt-2">Join Aether Today</h2>
            
            <!-- Progress indicator steps for Teacher -->
            <div v-if="role === 'teacher'" class="flex items-center space-x-2 pt-2.5">
              <span 
                class="px-2 py-0.5 rounded-full text-[9px] font-bold tracking-wider uppercase transition-all"
                :class="currentStep === 1 
                  ? 'bg-brand-primary/20 text-brand-primary border border-brand-primary/35' 
                  : 'bg-brand-dark/65 text-gray-500 border border-white/5'"
              >
                Step 1: Info
              </span>
              <span class="w-3 border-t border-white/10"></span>
              <span 
                class="px-2 py-0.5 rounded-full text-[9px] font-bold tracking-wider uppercase transition-all"
                :class="currentStep === 2 
                  ? 'bg-brand-accent/20 text-brand-accent border border-brand-accent/35' 
                  : 'bg-brand-dark/65 text-gray-500 border border-white/5'"
              >
                Step 2: Verification
              </span>
            </div>
            
            <p v-else class="text-xs text-gray-400">Register your account to unlock learning and educator portals</p>
          </div>

          <!-- Error Panel -->
          <div 
            v-if="errorMsg" 
            class="flex items-start space-x-2.5 p-3 rounded-xl bg-brand-danger/10 border border-brand-danger/25 text-brand-danger text-xs animate-fade-in"
          >
            <AlertCircle class="w-4 h-4 shrink-0 mt-0.5" />
            <span class="font-medium leading-relaxed">{{ errorMsg }}</span>
          </div>

          <!-- STEP 1: Basic Info Form -->
          <form v-if="currentStep === 1" @submit.prevent="handleNextStep" class="space-y-4 animate-fade-in">
            <!-- Role selector segment chips -->
            <div class="space-y-2">
              <label class="text-xs font-semibold text-gray-400 block mb-1">Choose Account Role</label>
              <div class="grid grid-cols-2 gap-3">
                <button 
                  type="button"
                  @click="role = 'student'"
                  class="flex items-center justify-center space-x-2 py-3 rounded-xl text-xs font-bold border transition-all cursor-pointer"
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
                  class="flex items-center justify-center space-x-2 py-3 rounded-xl text-xs font-bold border transition-all cursor-pointer"
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

            <!-- Next / Register CTA Button -->
            <button 
              type="submit" 
              class="w-full py-3 text-xs font-bold rounded-xl text-white shadow-lg transition-all glow-btn mt-6 cursor-pointer flex items-center justify-center space-x-2"
              :class="role === 'student' 
                ? 'bg-brand-primary hover:bg-brand-secondary shadow-brand-primary/20' 
                : 'bg-brand-accent hover:bg-emerald-600 shadow-brand-accent/20'"
            >
              <span>{{ role === 'student' ? 'Create Platform Account' : 'Continue to Step 2' }}</span>
              <ArrowRight v-if="role === 'teacher'" class="w-4 h-4" />
            </button>
          </form>

          <!-- STEP 2: Teacher Verification Credentials Form -->
          <form v-if="currentStep === 2 && role === 'teacher'" @submit.prevent="handleRegister" class="space-y-5 animate-fade-in text-left">
            <div class="space-y-2">
              <label for="verificationDoc" class="text-xs font-semibold text-gray-400 flex items-center space-x-1.5">
                <FileText class="w-4 h-4 text-brand-accent" />
                <span>Verification Documents & Proof</span>
                <span class="text-brand-accent font-bold">*</span>
              </label>
              
              <p class="text-[11px] text-gray-400 leading-relaxed font-light">
                To complete your educator registration, please upload or outline your verification credentials. Specify items like teaching license registration numbers, professional education certifications, academic experience, or reference URLs.
              </p>

              <textarea 
                v-model="verificationDoc" 
                id="verificationDoc" 
                required 
                placeholder="Teaching License / Certifications details: e.g. License ID: EDU-9821, Ph.D in Computer Science from Aether State University. Paste professional references..." 
                class="w-full h-36 p-3.5 bg-brand-dark/50 border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-accent/50 focus:border-brand-accent transition-all duration-300 resize-none shadow-inner leading-relaxed"
              ></textarea>
            </div>

            <div class="p-3 bg-brand-accent/5 border border-brand-accent/25 rounded-2xl text-[10px] text-brand-accent leading-normal flex items-start space-x-2.5">
              <CheckCircle class="w-4 h-4 shrink-0 mt-0.5" />
              <span>
                By submitting this application, you verify that these details are authentic. Credentials evaluation takes 4-5 business days. Outgoing SMTP confirmation logs can be reviewed instantly in the simulated SMTP widget.
              </span>
            </div>

            <!-- Submit Applications Button -->
            <button 
              type="submit" 
              class="w-full py-3 bg-brand-accent hover:bg-emerald-600 text-white text-xs font-bold rounded-xl shadow-lg shadow-brand-accent/20 transition-all glow-btn mt-4 cursor-pointer flex items-center justify-center space-x-1.5"
            >
              <CheckCircle class="w-4 h-4" />
              <span>Submit Educator Application</span>
            </button>
          </form>

          <!-- Redirect back to Sign In (only on Step 1) -->
          <div v-if="currentStep === 1" class="text-center text-xs text-gray-400 pt-2">
            <span>Already registered? </span>
            <router-link to="/login" class="font-bold text-brand-primary hover:text-brand-secondary">Sign In here</router-link>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>
