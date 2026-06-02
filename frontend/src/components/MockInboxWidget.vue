<script setup>
import { ref, computed } from 'vue';
import { useCoursesStore } from '../store/courses';
import { useAuthStore } from '../store/auth';
import { Mail, X, RefreshCw, ChevronRight, Inbox, Clock, Send, ShieldCheck } from 'lucide-vue-next';

const coursesStore = useCoursesStore();
const authStore = useAuthStore();

const isOpen = ref(false);
const selectedEmail = ref(null);
const searchFilter = ref('');

// Computed mock emails list
const emails = computed(() => coursesStore.emails);

// Filtered emails based on search query
const filteredEmails = computed(() => {
  if (!emails.value) return [];
  return emails.value.filter(email => {
    const query = searchFilter.value.toLowerCase();
    return email.to_email.toLowerCase().includes(query) || 
           email.subject.toLowerCase().includes(query) ||
           email.body.toLowerCase().includes(query);
  });
});

const toggleInbox = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value && emails.value.length > 0 && !selectedEmail.value) {
    selectedEmail.value = emails.value[0];
  }
};

const selectEmail = (email) => {
  selectedEmail.value = email;
};

const handleRefresh = async () => {
  await coursesStore.fetchCoursesData();
  if (emails.value.length > 0) {
    // Select the latest if none selected or if previous selected is gone
    if (!selectedEmail.value || !emails.value.some(e => e.id === selectedEmail.value.id)) {
      selectedEmail.value = emails.value[0];
    }
  }
};
</script>

<template>
  <div class="fixed bottom-6 right-6 z-[9999] font-sans">
    
    <!-- Floating Mail Badge Button -->
    <button 
      @click="toggleInbox"
      class="w-14 h-14 bg-gradient-to-tr from-brand-accent to-emerald-600 hover:from-emerald-500 hover:to-brand-accent text-white rounded-full flex items-center justify-center shadow-xl shadow-brand-accent/25 hover:shadow-brand-accent/40 active:scale-95 transition-all duration-300 relative cursor-pointer"
      title="Open Simulated SMTP Client"
    >
      <Mail class="w-6 h-6 animate-pulse" />
      
      <!-- Pulse Notification Badge if there are emails -->
      <span 
        v-if="emails.length > 0"
        class="absolute -top-1 -right-1 w-5 h-5 bg-brand-warning text-brand-dark font-extrabold text-[10px] rounded-full flex items-center justify-center border-2 border-brand-dark animate-bounce"
      >
        {{ emails.length }}
      </span>
    </button>

    <!-- Glassmorphic Mock Mail Client Dialog -->
    <div 
      v-if="isOpen"
      class="fixed bottom-24 right-6 w-[90vw] max-w-2xl h-[500px] glass-panel rounded-3xl border border-white/10 bg-brand-card shadow-2xl overflow-hidden flex flex-col animate-fade-in"
    >
      
      <!-- Header -->
      <div class="px-6 py-4 bg-brand-dark/65 border-b border-white/5 flex items-center justify-between">
        <div class="flex items-center space-x-3.5">
          <span class="p-2 bg-brand-accent/15 border border-brand-accent/25 text-brand-accent rounded-xl">
            <Inbox class="w-5 h-5" />
          </span>
          <div class="text-left">
            <h3 class="text-sm font-extrabold text-white font-display flex items-center space-x-2">
              <span>Aether Mock SMTP Mailer</span>
              <span class="px-2 py-0.5 rounded text-[8px] font-bold uppercase tracking-wider bg-brand-warning/15 text-brand-warning border border-brand-warning/20">Local Sandbox logs</span>
            </h3>
            <p class="text-[10px] text-gray-400">Simulating platform mail delivery in real-time.</p>
          </div>
        </div>

        <div class="flex items-center space-x-2">
          <!-- Refresh -->
          <button 
            @click="handleRefresh" 
            class="p-2 bg-white/5 border border-white/5 hover:bg-white/10 text-gray-300 hover:text-white rounded-xl transition-all cursor-pointer"
            title="Refresh SMTP Directory"
          >
            <RefreshCw class="w-4 h-4" />
          </button>
          
          <!-- Close -->
          <button 
            @click="toggleInbox" 
            class="p-2 bg-white/5 border border-white/5 hover:bg-white/10 text-gray-300 hover:text-white rounded-xl transition-all cursor-pointer"
            title="Close Client Window"
          >
            <X class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- Main Client Content Split Grid -->
      <div class="flex-grow flex overflow-hidden">
        
        <!-- Left Side: List of Messages -->
        <div class="w-5/12 border-r border-white/5 flex flex-col bg-brand-dark/20">
          
          <!-- Search box -->
          <div class="p-3 border-b border-white/5 bg-brand-dark/10">
            <input 
              v-model="searchFilter" 
              type="text" 
              placeholder="Search sent emails..." 
              class="w-full px-3 py-1.5 bg-brand-card hover:bg-brand-card-hover border border-white/10 text-xs text-white rounded-xl focus:outline-none focus:ring-1 focus:ring-brand-accent placeholder-gray-550"
            />
          </div>

          <!-- Roster list -->
          <div class="flex-grow overflow-y-auto divide-y divide-white/5 custom-scrollbar">
            <template v-if="filteredEmails.length > 0">
              <button 
                v-for="email in filteredEmails" 
                :key="email.id"
                @click="selectEmail(email)"
                class="w-full text-left p-3.5 hover:bg-white/[0.02] transition-colors flex items-start space-x-2.5 cursor-pointer relative"
                :class="{'bg-white/[0.03] border-l-2 border-brand-accent': selectedEmail && selectedEmail.id === email.id}"
              >
                <div class="w-7 h-7 rounded-full bg-brand-accent/10 border border-brand-accent/20 text-brand-accent flex items-center justify-center font-bold text-[9px] shrink-0 uppercase mt-0.5">
                  {{ email.to_email.split('@')[0].slice(0,2).toUpperCase() }}
                </div>
                
                <div class="truncate flex-grow text-xs">
                  <div class="flex items-center justify-between gap-1 mb-1">
                    <span class="font-bold text-white truncate max-w-[80px]">{{ email.to_email.split('@')[0] }}</span>
                    <span class="text-[8px] text-gray-550 shrink-0 font-medium">{{ email.date.split(' ')[1] || 'Today' }}</span>
                  </div>
                  <h4 class="font-semibold text-gray-300 truncate mb-0.5">{{ email.subject }}</h4>
                  <p class="text-[10px] text-gray-500 truncate font-light">{{ email.body }}</p>
                </div>
              </button>
            </template>
            
            <div v-else class="flex flex-col items-center justify-center p-8 text-center h-full text-gray-550 space-y-2">
              <Mail class="w-8 h-8 opacity-45" />
              <p class="text-xs font-semibold">No Outgoing Messages</p>
              <p class="text-[10px] font-light leading-normal">Register a new teacher account to log SMTP activity.</p>
            </div>
          </div>
        </div>

        <!-- Right Side: Details View -->
        <div class="w-7/12 flex flex-col bg-brand-card/10 overflow-hidden">
          
          <div v-if="selectedEmail" class="flex flex-col h-full overflow-hidden">
            <!-- Header Specs -->
            <div class="p-5 border-b border-white/5 bg-brand-dark/25 text-left text-xs space-y-2.5">
              <div class="flex items-start justify-between gap-3">
                <h4 class="font-extrabold text-white leading-relaxed">{{ selectedEmail.subject }}</h4>
                <span class="px-2 py-0.5 bg-white/5 text-gray-400 text-[8px] font-bold uppercase rounded border border-white/5 shrink-0">SMTP Sent</span>
              </div>
              
              <div class="flex flex-col space-y-1 text-gray-400 text-[11px]">
                <div class="flex items-center space-x-1.5">
                  <span class="font-semibold text-gray-500">From:</span>
                  <span class="text-brand-primary flex items-center space-x-1">
                    <ShieldCheck class="w-3.5 h-3.5 text-brand-primary" />
                    <span>{{ selectedEmail.from_email }}</span>
                  </span>
                </div>
                <div class="flex items-center space-x-1.5">
                  <span class="font-semibold text-gray-500">To:</span>
                  <span class="text-white">{{ selectedEmail.to_email }}</span>
                </div>
                <div class="flex items-center space-x-1.5">
                  <span class="font-semibold text-gray-500">Date:</span>
                  <span class="text-gray-450">{{ selectedEmail.date }}</span>
                </div>
              </div>
            </div>

            <!-- Email Body Content -->
            <div class="flex-grow p-6 overflow-y-auto text-left text-xs text-gray-300 leading-relaxed font-light whitespace-pre-line custom-scrollbar select-text selection:bg-brand-accent/20">
              {{ selectedEmail.body }}
            </div>
          </div>

          <!-- Empty details state -->
          <div v-else class="flex-grow flex flex-col items-center justify-center text-center p-8 text-gray-550 space-y-3">
            <Mail class="w-10 h-10 opacity-30 animate-pulse" />
            <p class="text-xs font-semibold">Select an email to view SMTP logs</p>
            <p class="text-[10px] font-light leading-normal max-w-xs">Outgoing registration status, credential receipts, and approval notifications will render here live.</p>
          </div>
        </div>

      </div>

      <!-- Footer Info -->
      <div class="px-6 py-2 bg-brand-dark/45 border-t border-white/5 flex items-center justify-between text-[9px] text-gray-550 shrink-0 font-medium">
        <span>Aether Security Sandbox Node: Active</span>
        <span>Local SMTP Port: Simulated</span>
      </div>

    </div>

  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.15);
}
</style>
