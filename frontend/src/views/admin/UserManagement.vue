<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '../../store/auth';
import { useRouter } from 'vue-router';
import { 
  ArrowLeft, Users, ShieldAlert, Ban, UserCheck, 
  Trash, Search, Filter, ShieldCheck
} from 'lucide-vue-next';

const authStore = useAuthStore();
const router = useRouter();

const searchQuery = ref('');
const roleFilter = ref('All');

// Filter roles options
const roles = ['All', 'student', 'teacher', 'admin'];

// Full users list
const users = computed(() => authStore.users);

// Filtered users list
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          user.email.toLowerCase().includes(searchQuery.value.toLowerCase());
    
    const matchesRole = roleFilter.value === 'All' || user.role === roleFilter.value;
    
    return matchesSearch && matchesRole;
  });
});

const handleToggleSuspension = async (userId) => {
  try {
    await authStore.toggleSuspension(userId);
    alert("User suspension status updated successfully!");
  } catch (err) {
    alert(err.message);
  }
};

const handleDeleteUser = async (userId, name) => {
  const confirmDelete = confirm(`Are you sure you want to permanently delete user account "${name}"? This action is irreversible.`);
  if (!confirmDelete) return;

  try {
    await authStore.deleteUser(userId);
    alert(`Account "${name}" successfully deleted from platform directories.`);
  } catch (err) {
    alert(err.message);
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
