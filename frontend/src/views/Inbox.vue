<script setup>
import { computed, ref, onMounted } from 'vue';
import { useAuthStore } from '../store/auth';
import { useCoursesStore } from '../store/courses';
import { Mail, MailOpen, ArrowLeft, Trash2, Calendar } from 'lucide-vue-next';

const authStore = useAuthStore();
const coursesStore = useCoursesStore();

const userEmail = computed(() => authStore.currentUser?.email);
const emails = computed(() => coursesStore.getUserEmails(userEmail.value));

const selectedEmail = ref(null);

const formatDate = (isoString) => {
  const date = new Date(isoString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  });
};

const openEmail = (email) => {
  selectedEmail.value = email;
};

const closeEmail = () => {
  selectedEmail.value = null;
};
</script>

<template>
  <div class="max-w-6xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-extrabold text-white font-display flex items-center space-x-3">
        <Mail class="w-8 h-8 text-brand-primary" />
        <span>My Inbox</span>
      </h1>
      <div class="text-sm text-gray-400">
        {{ emails.length }} Messages
      </div>
    </div>

    <div class="glass-panel rounded-3xl border border-white/5 bg-brand-card overflow-hidden shadow-2xl flex flex-col md:flex-row min-h-[600px]">
      
      <!-- Email List Sidebar -->
      <div 
        class="w-full md:w-1/3 border-r border-white/5 flex flex-col bg-brand-dark/30"
        :class="{ 'hidden md:flex': selectedEmail }"
      >
        <div class="p-4 border-b border-white/5 font-semibold text-gray-300 text-sm uppercase tracking-wider bg-black/20">
          Recent Messages
        </div>
        
        <div class="flex-1 overflow-y-auto">
          <div v-if="emails.length === 0" class="p-8 text-center text-gray-500 text-sm">
            <Mail class="w-12 h-12 mx-auto mb-3 opacity-20" />
            Your inbox is empty
          </div>
          
          <div 
            v-for="(email, idx) in emails" 
            :key="idx"
            @click="openEmail(email)"
            class="p-4 border-b border-white/5 cursor-pointer hover:bg-white/[0.02] transition-colors"
            :class="{ 'bg-brand-primary/10 border-l-2 border-l-brand-primary': selectedEmail === email }"
          >
            <div class="flex justify-between items-start mb-1">
              <span class="text-xs font-bold text-gray-300 truncate pr-2">Aether Team</span>
              <span class="text-[10px] text-gray-500 whitespace-nowrap">{{ formatDate(email.sentAt) }}</span>
            </div>
            <h4 class="text-sm font-semibold text-white truncate mb-1" :class="{ 'text-brand-primary': selectedEmail === email }">
              {{ email.subject }}
            </h4>
            <p class="text-xs text-gray-400 line-clamp-2 leading-relaxed">
              {{ email.body }}
            </p>
          </div>
        </div>
      </div>

      <!-- Email Reader Area -->
      <div 
        class="w-full md:w-2/3 flex flex-col bg-brand-card"
        :class="{ 'hidden md:flex': !selectedEmail }"
      >
        <div v-if="!selectedEmail" class="flex-1 flex flex-col items-center justify-center text-gray-500">
          <MailOpen class="w-16 h-16 mb-4 opacity-10" />
          <p>Select a message to read</p>
        </div>

        <div v-else class="flex-1 flex flex-col">
          <!-- Reader Header -->
          <div class="p-6 border-b border-white/5 space-y-4">
            <button @click="closeEmail" class="md:hidden flex items-center space-x-2 text-xs text-brand-primary hover:text-white transition-colors mb-4">
              <ArrowLeft class="w-4 h-4" />
              <span>Back to Inbox</span>
            </button>
            
            <h2 class="text-2xl font-bold text-white">{{ selectedEmail.subject }}</h2>
            
            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-full bg-brand-primary/20 flex items-center justify-center text-brand-primary font-bold">
                  AT
                </div>
                <div>
                  <p class="font-bold text-gray-200">Aether Team</p>
                  <p class="text-xs text-gray-500">noreply@aether.edu</p>
                </div>
              </div>
              <div class="flex items-center space-x-2 text-gray-500 text-xs">
                <Calendar class="w-4 h-4" />
                <span>{{ formatDate(selectedEmail.sentAt) }}</span>
              </div>
            </div>
          </div>

          <!-- Reader Body -->
          <div class="p-8 flex-1 overflow-y-auto">
            <div class="text-gray-300 leading-relaxed whitespace-pre-wrap text-sm md:text-base max-w-2xl">
              {{ selectedEmail.body }}
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>
