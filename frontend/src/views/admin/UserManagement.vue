<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '../../store/auth';
import { useRouter } from 'vue-router';
import { 
  ArrowLeft, Users, ShieldAlert, Ban, UserCheck, 
  Trash, Search, Filter, ShieldCheck
} from 'lucide-vue-next';

import { useNotificationStore } from '../../store/notifications';

const authStore = useAuthStore();
const notifStore = useNotificationStore();
const router = useRouter();

const searchQuery = ref('');
const roleFilter = ref('All');

// Filter roles options
const roles = ['All', 'student', 'teacher', 'admin'];

// Full users list
const users = computed(() => authStore.users);

// Pending verification teachers list
const pendingTeachers = computed(() => {
  return users.value.filter(user => user.role === 'teacher' && user.verificationStatus === 'pending');
});

// Filtered users list (excluding pending teachers so they don't clutter normal active roster directory)
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    // Hide pending teachers from the main database list until approved
    if (user.role === 'teacher' && user.verificationStatus === 'pending') return false;

    const matchesSearch = user.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          user.email.toLowerCase().includes(searchQuery.value.toLowerCase());
    
    const matchesRole = roleFilter.value === 'All' || user.role === roleFilter.value;
    
    return matchesSearch && matchesRole;
  });
});

const handleVerifyTeacher = async (userId, name) => {
  try {
    await authStore.verifyTeacher(userId);
    notifStore.showToast("Educator Verified", `Teacher "${name}" has been successfully approved and notified!`, "success");
  } catch (err) {
    notifStore.showToast("Approval Failed", err.message, "danger");
  }
};

const handleToggleSuspension = async (userId) => {
  try {
    await authStore.toggleSuspension(userId);
    notifStore.showToast("Directory Updated", "User suspension status updated successfully!", "success");
  } catch (err) {
    notifStore.showToast("Update Failed", err.message, "danger");
  }
};

const handleDeleteUser = async (userId, name) => {
  const confirmDelete = await notifStore.showConfirm(
    "Delete User Profile?",
    `Are you sure you want to permanently delete user account "${name}"? All dashboard logs and history will be cleared. This action is irreversible.`,
    "danger",
    "Delete Account",
    "Cancel"
  );
  if (!confirmDelete) return;

  try {
    await authStore.deleteUser(userId);
    notifStore.showToast("Account Deleted", `Account "${name}" successfully deleted from platform directories.`, "success");
  } catch (err) {
    notifStore.showToast("Deletion Failed", err.message, "danger");
  }
};
</script>

<template>
  <div class="space-y-8 py-4">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <button 
        @click="router.push('/admin/dashboard')" 
        class="flex items-center space-x-2 text-sm text-gray-400 hover:text-white transition-colors shrink-0"
      >
        <ArrowLeft class="w-4 h-4" />
        <span>Back to Portal</span>
      </button>

      <!-- Filters & Search block -->
      <div class="flex flex-col sm:flex-row items-center gap-3 w-full sm:w-auto">
        <!-- Search bar -->
        <div class="relative w-full sm:w-60">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search profiles..." 
            class="w-full pl-9 pr-4 py-1.5 bg-brand-card hover:bg-brand-card-hover border border-white/10 rounded-xl text-xs text-white focus:outline-none focus:ring-1 focus:ring-brand-primary"
          />
        </div>

        <!-- Role select -->
        <div class="flex items-center space-x-2 shrink-0 w-full sm:w-auto">
          <Filter class="w-4.5 h-4.5 text-brand-primary" />
          <select 
            v-model="roleFilter"
            class="bg-brand-card hover:bg-brand-card-hover border border-white/10 px-3 py-1.5 rounded-xl text-xs text-white focus:outline-none focus:ring-1 focus:ring-brand-primary w-full sm:w-auto"
          >
            <option v-for="role in roles" :key="role" :value="role">
              {{ role === 'All' ? 'All Roles' : role.toUpperCase() }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Title -->
    <div class="space-y-1">
      <h1 class="text-xl md:text-2xl font-extrabold text-white font-display flex items-center space-x-2">
        <Users class="w-5.5 h-5.5 text-brand-primary" />
        <span>User Accounts Directory</span>
      </h1>
      <p class="text-xs text-gray-450">Review system registration lists, assign suspension locks, or remove accounts.</p>
    </div>

    <!-- Pending Teacher Approvals Widget Queue -->
    <div v-if="pendingTeachers.length > 0" class="space-y-4 animate-fade-in border-b border-white/5 pb-8 mb-4">
      <h2 class="text-xs font-bold text-brand-accent uppercase tracking-wider flex items-center space-x-2 font-display">
        <ShieldAlert class="w-4.5 h-4.5 text-brand-accent" />
        <span>Pending Teacher Approvals ({{ pendingTeachers.length }})</span>
      </h2>
      
      <div class="grid grid-cols-1 gap-4">
        <div 
          v-for="teacher in pendingTeachers" 
          :key="teacher.id"
          class="glass-panel p-5 rounded-2xl border border-brand-accent/25 bg-brand-accent/[0.01] hover:bg-brand-accent/[0.02] transition-all flex flex-col md:flex-row justify-between items-start md:items-center gap-4.5"
        >
          <div class="space-y-2 max-w-xl text-left">
            <div class="flex items-center space-x-3.5">
              <h3 class="text-sm font-bold text-white font-display">{{ teacher.name }}</h3>
              <span class="px-2.5 py-0.5 rounded-full text-[8px] font-bold uppercase bg-brand-accent/15 text-brand-accent border border-brand-accent/20 tracking-wider">Awaiting Verification</span>
            </div>
            <p class="text-[10px] text-gray-400">Registered Email: <span class="text-white font-medium">{{ teacher.email }}</span> • Joined: {{ teacher.joinedDate }}</p>
            
            <!-- Credentials container -->
            <div class="p-3 bg-brand-dark/45 border border-white/5 rounded-xl text-xs space-y-1">
              <span class="text-[9px] font-bold uppercase text-brand-accent tracking-widest block mb-0.5">Submitted Verification Credentials:</span>
              <p class="text-gray-300 font-light leading-relaxed italic text-[11px]">
                "{{ teacher.verificationDoc || 'No qualifications specified.' }}"
              </p>
            </div>
          </div>

          <!-- Quick approval action -->
          <div class="flex items-center space-x-3 shrink-0 self-stretch md:self-auto justify-end">
            <button 
              @click="handleVerifyTeacher(teacher.id, teacher.name)"
              class="px-4.5 py-2.5 bg-brand-accent hover:bg-emerald-600 text-white text-xs font-bold rounded-xl transition-all shadow-md shadow-brand-accent/15 flex items-center space-x-2 cursor-pointer"
            >
              <UserCheck class="w-4 h-4 shrink-0" />
              <span>Verify & Approve Educator</span>
            </button>
            
            <button 
              @click="handleDeleteUser(teacher.id, teacher.name)"
              class="p-2.5 bg-brand-danger/10 border border-brand-danger/20 text-brand-danger hover:bg-brand-danger hover:text-white rounded-xl transition-all cursor-pointer"
              title="Reject & Delete Application"
            >
              <Trash class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Users roster Table -->
    <div class="glass-panel rounded-3xl overflow-hidden border border-white/5 bg-brand-card shadow-2xl">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="bg-brand-dark/50 border-b border-white/5 text-gray-400 font-bold uppercase tracking-wider">
              <th class="px-6 py-4">Full Name</th>
              <th class="px-6 py-4">Email</th>
              <th class="px-6 py-4">Account Role</th>
              <th class="px-6 py-4">Security Status</th>
              <th class="px-6 py-4">Joined Date</th>
              <th class="px-6 py-4 text-right">Administrative Controls</th>
            </tr>
          </thead>
          
          <tbody v-if="filteredUsers.length > 0" class="divide-y divide-white/5">
            <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-white/[0.02] transition-colors">
              
              <!-- Name -->
              <td class="px-6 py-4 font-bold text-white">{{ user.name }}</td>

              <!-- Email -->
              <td class="px-6 py-4 font-semibold text-gray-300">{{ user.email }}</td>

              <!-- Role Badge -->
              <td class="px-6 py-4">
                <span 
                  class="px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider border shrink-0 inline-flex items-center space-x-1"
                  :class="{
                    'bg-brand-primary/15 text-brand-primary border-brand-primary/20': user.role === 'student',
                    'bg-brand-accent/15 text-brand-accent border-brand-accent/20': user.role === 'teacher',
                    'bg-brand-warning/15 text-brand-warning border-brand-warning/20': user.role === 'admin'
                  }"
                >
                  <ShieldCheck v-if="user.role === 'admin'" class="w-3 h-3" />
                  <span>{{ user.role }}</span>
                </span>
              </td>

              <!-- Status -->
              <td class="px-6 py-4">
                <span 
                  class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider"
                  :class="user.suspended 
                    ? 'bg-brand-danger/10 text-brand-danger border border-brand-danger/20' 
                    : 'bg-brand-accent/10 text-brand-accent border border-brand-accent/20'"
                >
                  {{ user.suspended ? 'Suspended' : 'Active' }}
                </span>
              </td>

              <!-- Joined Date -->
              <td class="px-6 py-4 text-gray-400 font-medium">{{ user.joinedDate || '2026-05-26' }}</td>

              <!-- Actions column -->
              <td class="px-6 py-4 text-right">
                <!-- If administrator, hide delete/suspend actions as safeguards -->
                <div v-if="user.role === 'admin'" class="text-[10px] text-gray-500 font-bold uppercase pr-4">
                  Protected System profile
                </div>
                
                <div v-else class="flex justify-end items-center space-x-2">
                  <!-- Suspend toggle -->
                  <button 
                    @click="handleToggleSuspension(user.id)"
                    class="p-2 rounded-xl text-xs font-bold border transition-all flex items-center justify-center space-x-1"
                    :class="user.suspended 
                      ? 'bg-brand-accent/10 border-brand-accent/20 text-brand-accent hover:bg-brand-accent/20' 
                      : 'bg-brand-warning/10 border-brand-warning/20 text-brand-warning hover:bg-brand-warning/20'"
                    :title="user.suspended ? 'Unsuspend Account' : 'Suspend Account'"
                  >
                    <UserCheck v-if="user.suspended" class="w-3.5 h-3.5 shrink-0" />
                    <Ban v-else class="w-3.5 h-3.5 shrink-0" />
                  </button>

                  <!-- Delete account -->
                  <button 
                    @click="handleDeleteUser(user.id, user.name)"
                    class="p-2 bg-brand-danger/10 hover:bg-brand-danger border border-brand-danger/20 hover:border-transparent text-brand-danger hover:text-white rounded-xl transition-all"
                    title="Delete Account Permanently"
                  >
                    <Trash class="w-3.5 h-3.5 shrink-0" />
                  </button>
                </div>
              </td>

            </tr>
          </tbody>

          <!-- Table empty -->
          <tbody v-else>
            <tr>
              <td colspan="6" class="px-6 py-12 text-center text-gray-500 font-medium">
                No user profiles located under active search filter rules.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>
