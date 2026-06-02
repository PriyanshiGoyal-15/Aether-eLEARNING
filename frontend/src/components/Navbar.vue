<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '../store/auth';
import { useCoursesStore } from '../store/courses';
import { useRouter } from 'vue-router';
import { 
  Menu, X, ChevronDown, LogOut, LayoutDashboard, BookOpen, 
  PlusCircle, Users, ClipboardCheck, UserCheck, ShieldCheck, Award,
  Bell, Info, CheckCircle, AlertTriangle, AlertCircle, Sun, Moon, Gamepad2, Mail
} from 'lucide-vue-next';

const authStore = useAuthStore();
const coursesStore = useCoursesStore();
const router = useRouter();

const isMobileMenuOpen = ref(false);
const isProfileDropdownOpen = ref(false);
const isNotifDropdownOpen = ref(false);

const theme = ref(localStorage.getItem('aether_theme') || 'dark');

const toggleTheme = () => {
  theme.value = theme.value === 'dark' ? 'light' : 'dark';
  localStorage.setItem('aether_theme', theme.value);
  applyTheme();
};

const applyTheme = () => {
  const root = document.documentElement;
  if (theme.value === 'light') {
    root.classList.add('light');
    root.classList.remove('dark');
  } else {
    root.classList.add('dark');
    root.classList.remove('light');
  }
};

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const toggleProfileDropdown = () => {
  isProfileDropdownOpen.value = !isProfileDropdownOpen.value;
  isNotifDropdownOpen.value = false;
};

const toggleNotifDropdown = () => {
  isNotifDropdownOpen.value = !isNotifDropdownOpen.value;
  isProfileDropdownOpen.value = false;
  
  if (isNotifDropdownOpen.value && authStore.isAuthenticated) {
    coursesStore.markAllNotificationsAsRead(authStore.currentUser.id);
  }
};

const handleLogout = () => {
  authStore.logout();
  isProfileDropdownOpen.value = false;
  isNotifDropdownOpen.value = false;
  isMobileMenuOpen.value = false;
  router.push('/');
};

// Close dropdown on click outside
const closeDropdown = (e) => {
  if (!e.target.closest('#profile-dropdown-container')) {
    isProfileDropdownOpen.value = false;
  }
  if (!e.target.closest('#notif-dropdown-container')) {
    isNotifDropdownOpen.value = false;
  }
};

onMounted(() => {
  window.addEventListener('click', closeDropdown);
  applyTheme();
});

onUnmounted(() => {
  window.removeEventListener('click', closeDropdown);
});
</script>

<template>
  <nav class="sticky top-0 z-40 bg-brand-card/75 backdrop-blur-xl border-b border-brand-border shadow-lg shadow-black/15 transition-all duration-300">
    <!-- Gorgeous premium neon separating line at the bottom of the navbar -->
    <div class="absolute bottom-0 left-0 right-0 h-[1.5px] bg-gradient-to-r from-transparent via-brand-primary/20 to-transparent dark:via-brand-primary/25 pointer-events-none"></div>
    <div class="max-w-[1680px] mx-auto px-6 md:px-12 lg:px-16 relative z-10">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-2">
            <span class="p-2 rounded-xl bg-gradient-to-tr from-brand-primary to-brand-secondary text-white shadow-md shadow-brand-primary/20">
              <Award class="w-6 h-6" />
            </span>
            <span class="text-xl font-extrabold tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-300 font-display">AETHER</span>
          </router-link>
        </div>

        <!-- Desktop Navigation Items -->
        <div class="hidden md:flex items-center space-x-1">
          <router-link 
            to="/" 
            class="px-4 py-2 rounded-xl text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200"
            active-class="bg-white/5 text-white font-semibold"
          >
            Home
          </router-link>

          <!-- Student Links -->
          <template v-if="authStore.isAuthenticated && authStore.isStudent">
            <router-link 
              to="/student/dashboard" 
              class="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200"
              active-class="bg-brand-primary/10 text-brand-primary font-semibold"
            >
              <LayoutDashboard class="w-4 h-4" />
              <span>Dashboard</span>
            </router-link>
            <router-link 
              to="/student/courses" 
              class="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200"
              active-class="bg-brand-primary/10 text-brand-primary font-semibold"
            >
              <BookOpen class="w-4 h-4" />
              <span>Explore Courses</span>
            </router-link>
            <router-link 
              to="/student/quizzes" 
              class="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200"
              active-class="bg-brand-primary/10 text-brand-primary font-semibold"
            >
              <Gamepad2 class="w-4 h-4" />
              <span>Quiz Arena</span>
            </router-link>
          </template>

          <!-- Teacher Links -->
          <template v-if="authStore.isAuthenticated && authStore.isTeacher">
            <router-link 
              to="/teacher/dashboard" 
              class="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200"
              active-class="bg-brand-primary/10 text-brand-primary font-semibold"
            >
              <LayoutDashboard class="w-4 h-4" />
              <span>Overview</span>
            </router-link>
            <router-link 
              to="/teacher/create" 
              class="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200"
              active-class="bg-brand-primary/10 text-brand-primary font-semibold"
            >
              <PlusCircle class="w-4 h-4" />
              <span>Create Course</span>
            </router-link>
            <router-link 
              to="/teacher/students" 
              class="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200"
              active-class="bg-brand-primary/10 text-brand-primary font-semibold"
            >
              <Users class="w-4 h-4" />
              <span>Gradebook</span>
            </router-link>
            <!-- <router-link 
              to="/teacher/quizzes" 
              class="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200"
              active-class="bg-brand-primary/10 text-brand-primary font-semibold"
            >
              <Gamepad2 class="w-4 h-4" />
              <span>Quiz Manager</span>
            </router-link> -->
          </template>

          <!-- Admin Links -->
          <template v-if="authStore.isAuthenticated && authStore.isAdmin">
            <router-link 
              to="/admin/dashboard" 
              class="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200"
              active-class="bg-brand-primary/10 text-brand-primary font-semibold"
            >
              <LayoutDashboard class="w-4 h-4" />
              <span>Analytics</span>
            </router-link>
            <router-link 
              to="/admin/approvals" 
              class="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200"
              active-class="bg-brand-primary/10 text-brand-primary font-semibold"
            >
              <ClipboardCheck class="w-4 h-4" />
              <span>Approvals</span>
            </router-link>
            <router-link 
              to="/admin/users" 
              class="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200"
              active-class="bg-brand-primary/10 text-brand-primary font-semibold"
            >
              <UserCheck class="w-4 h-4" />
              <span>Users</span>
            </router-link>
          </template>
        </div>

        <!-- Auth Controls (Desktop) -->
        <div class="hidden md:flex items-center space-x-3">
          <!-- Theme Toggle Button -->
          <button 
            @click="toggleTheme"
            class="p-2 text-gray-400 hover:text-white bg-white/5 border border-white/5 hover:bg-white/10 rounded-xl transition-all flex items-center justify-center cursor-pointer"
            title="Toggle theme"
          >
            <Sun v-if="theme === 'dark'" class="w-4.5 h-4.5 text-brand-warning" />
            <Moon v-else class="w-4.5 h-4.5 text-brand-primary" />
          </button>

          <template v-if="!authStore.isAuthenticated">
            <router-link to="/login" class="text-sm font-medium text-gray-300 hover:text-white px-3 py-2 transition-colors">
              Sign In
            </router-link>
            <router-link to="/register" class="bg-brand-primary hover:bg-brand-secondary text-white text-sm font-semibold px-4.5 py-2 rounded-xl transition-all duration-300 shadow-md shadow-brand-primary/10 hover:shadow-brand-primary/20">
              Get Started
            </router-link>
          </template>

          <template v-else>
            <!-- Inbox Icon -->
            <router-link 
              to="/inbox" 
              class="p-2 text-gray-400 hover:text-white bg-white/5 border border-white/5 hover:bg-white/10 rounded-xl transition-all relative flex items-center justify-center cursor-pointer"
              title="My Inbox"
            >
              <Mail class="w-4.5 h-4.5" />
              <span 
                v-if="coursesStore.getUserEmails(authStore.currentUser.email).length > 0"
                class="absolute -top-1 -right-1 bg-brand-primary text-white text-[8px] font-extrabold w-4 h-4 rounded-full flex items-center justify-center animate-pulse shadow-md shadow-brand-primary/40"
              >
                {{ coursesStore.getUserEmails(authStore.currentUser.email).length }}
              </span>
            </router-link>

            <!-- Notifications Dropdown Bell -->
            <div id="notif-dropdown-container" class="relative">
              <button 
                @click="toggleNotifDropdown"
                class="p-2 text-gray-400 hover:text-white bg-white/5 border border-white/5 hover:bg-white/10 rounded-xl transition-all relative flex items-center justify-center cursor-pointer"
              >
                <Bell class="w-4.5 h-4.5" />
                <span 
                  v-if="coursesStore.getUnreadNotificationCount(authStore.currentUser.id) > 0"
                  class="absolute -top-1 -right-1 bg-brand-danger text-white text-[8px] font-extrabold w-4 h-4 rounded-full flex items-center justify-center animate-pulse"
                >
                  {{ coursesStore.getUnreadNotificationCount(authStore.currentUser.id) }}
                </span>
              </button>

              <!-- Notifications dropdown list panel -->
              <div 
                v-if="isNotifDropdownOpen"
                class="absolute right-0 mt-2.5 w-80 rounded-2xl bg-brand-card border border-white/10 shadow-2xl p-2 animate-fade-in z-50 max-h-[360px] overflow-y-auto"
              >
                <div class="px-3 py-2 border-b border-white/5 mb-1.5 flex justify-between items-center">
                  <h4 class="text-xs font-bold text-white font-display">Notifications</h4>
                  <span class="text-[8px] font-bold text-gray-500 uppercase tracking-wider">Recent Alerts</span>
                </div>

                <div v-if="coursesStore.getUserNotifications(authStore.currentUser.id).length > 0" class="space-y-1">
                  <div 
                    v-for="notif in coursesStore.getUserNotifications(authStore.currentUser.id)" 
                    :key="notif.id"
                    class="p-2.5 rounded-xl flex items-start space-x-2.5 border border-transparent hover:border-white/5 hover:bg-white/[0.01] transition-all"
                    :class="{'bg-white/[0.02]': !notif.read}"
                  >
                    <!-- Category specific visual tag icon -->
                    <span 
                      class="p-1 rounded-lg shrink-0 mt-0.5 flex items-center justify-center"
                      :class="{
                        'bg-brand-primary/15 text-brand-primary': notif.type === 'info',
                        'bg-brand-accent/15 text-brand-accent': notif.type === 'success',
                        'bg-brand-warning/15 text-brand-warning': notif.type === 'warning',
                        'bg-brand-danger/15 text-brand-danger': notif.type === 'danger'
                      }"
                    >
                      <Info v-if="notif.type === 'info'" class="w-3.5 h-3.5" />
                      <CheckCircle v-else-if="notif.type === 'success'" class="w-3.5 h-3.5" />
                      <AlertTriangle v-else-if="notif.type === 'warning'" class="w-3.5 h-3.5" />
                      <AlertCircle v-else class="w-3.5 h-3.5" />
                    </span>

                    <div class="space-y-0.5 flex-grow truncate">
                      <p class="text-xs font-bold text-white leading-tight truncate">{{ notif.title }}</p>
                      <p class="text-[10px] text-gray-400 leading-normal line-clamp-2 white-space-normal">{{ notif.message }}</p>
                      <p class="text-[8px] text-gray-500 font-semibold mt-1">{{ notif.date }}</p>
                    </div>
                  </div>
                </div>

                <div v-else class="p-6 text-center text-[10px] text-gray-500 leading-normal">
                  No active platform alerts found.
                </div>
              </div>
            </div>

            <!-- Profile Dropdown Container -->
            <div id="profile-dropdown-container" class="relative">
              <button 
                @click="toggleProfileDropdown"
                class="flex items-center space-x-2 text-sm font-medium text-gray-300 hover:text-white focus:outline-none bg-white/5 border border-white/5 px-3 py-1.5 rounded-xl transition-all hover:bg-white/10"
              >
                <!-- Custom Gradient avatar with initials -->
                <div class="w-7 h-7 rounded-full bg-gradient-to-tr from-brand-primary to-brand-secondary flex items-center justify-center font-bold text-white text-xs shadow-inner">
                  {{ authStore.currentUser.name.split(' ').map(n => n[0]).join('').slice(0,2).toUpperCase() }}
                </div>
                <span class="max-w-[100px] truncate">{{ authStore.currentUser.name }}</span>
                <ChevronDown class="w-4 h-4 text-gray-400 transition-transform" :class="{'rotate-180': isProfileDropdownOpen}" />
              </button>

              <!-- Dropdown Content -->
              <div 
                v-if="isProfileDropdownOpen"
                class="absolute right-0 mt-2.5 w-60 rounded-2xl bg-brand-card border border-white/10 shadow-2xl p-2 animate-fade-in z-50"
              >
                <div class="px-3.5 py-3 border-b border-white/5 mb-1.5">
                  <p class="text-sm font-semibold text-white truncate">{{ authStore.currentUser.name }}</p>
                  <p class="text-xs text-gray-400 truncate">{{ authStore.currentUser.email }}</p>
                  <div class="mt-2.5">
                    <span 
                      class="px-2 py-0.5 rounded-full text-[10px] font-semibold tracking-wider uppercase shadow-sm"
                      :class="{
                        'bg-brand-primary/20 text-brand-primary border border-brand-primary/30': authStore.isStudent,
                        'bg-brand-accent/20 text-brand-accent border border-brand-accent/30': authStore.isTeacher,
                        'bg-brand-warning/20 text-brand-warning border border-brand-warning/30': authStore.isAdmin
                      }"
                    >
                      {{ authStore.currentUser.role }}
                    </span>
                  </div>
                </div>

                <!-- Role specific redirection in dropdown -->
                <router-link 
                  v-if="authStore.isStudent" 
                  to="/student/dashboard" 
                  class="flex items-center space-x-2 px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5 rounded-xl transition-colors"
                  @click="isProfileDropdownOpen = false"
                >
                  <LayoutDashboard class="w-4 h-4" />
                  <span>My Learning</span>
                </router-link>

                <router-link 
                  v-if="authStore.isTeacher" 
                  to="/teacher/dashboard" 
                  class="flex items-center space-x-2 px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5 rounded-xl transition-colors"
                  @click="isProfileDropdownOpen = false"
                >
                  <LayoutDashboard class="w-4 h-4" />
                  <span>Teacher Portal</span>
                </router-link>

                <router-link 
                  v-if="authStore.isAdmin" 
                  to="/admin/dashboard" 
                  class="flex items-center space-x-2 px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5 rounded-xl transition-colors"
                  @click="isProfileDropdownOpen = false"
                >
                  <ShieldCheck class="w-4 h-4" />
                  <span>Admin Panel</span>
                </router-link>

                <button 
                  @click="handleLogout"
                  class="w-full flex items-center space-x-2 px-3 py-2 text-sm text-brand-danger hover:bg-brand-danger/10 rounded-xl transition-colors text-left font-medium"
                >
                  <LogOut class="w-4 h-4" />
                  <span>Sign Out</span>
                </button>
              </div>
            </div>
          </template>
        </div>

        <!-- Mobile Menu Toggle -->
        <div class="md:hidden flex items-center">
          <button 
            @click="toggleMobileMenu"
            class="inline-flex items-center justify-center p-2 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 focus:outline-none transition-colors"
          >
            <Menu v-if="!isMobileMenuOpen" class="w-6 h-6" />
            <X v-else class="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div 
      v-if="isMobileMenuOpen"
      class="md:hidden bg-brand-card/95 border-b border-brand-border px-4 pt-2 pb-4 space-y-2 animate-fade-in backdrop-blur-md"
    >
      <router-link 
        to="/" 
        class="block px-3.5 py-2 rounded-xl text-base font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-colors"
        @click="isMobileMenuOpen = false"
      >
        Home
      </router-link>

      <!-- Student Menu -->
      <template v-if="authStore.isAuthenticated && authStore.isStudent">
        <router-link 
          to="/student/dashboard" 
          class="block px-3.5 py-2 rounded-xl text-base font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-colors"
          @click="isMobileMenuOpen = false"
        >
          Student Dashboard
        </router-link>
        <router-link 
          to="/student/courses" 
          class="block px-3.5 py-2 rounded-xl text-base font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-colors"
          @click="isMobileMenuOpen = false"
        >
          Explore Courses
        </router-link>
        <router-link 
          to="/student/quizzes" 
          class="block px-3.5 py-2 rounded-xl text-base font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-colors"
          @click="isMobileMenuOpen = false"
        >
          Quiz Arena
        </router-link>
      </template>

      <!-- Teacher Menu -->
      <template v-if="authStore.isAuthenticated && authStore.isTeacher">
        <router-link 
          to="/teacher/dashboard" 
          class="block px-3.5 py-2 rounded-xl text-base font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-colors"
          @click="isMobileMenuOpen = false"
        >
          Teacher Portal
        </router-link>
        <router-link 
          to="/teacher/create" 
          class="block px-3.5 py-2 rounded-xl text-base font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-colors"
          @click="isMobileMenuOpen = false"
        >
          Create Course
        </router-link>
        <router-link 
          to="/teacher/students" 
          class="block px-3.5 py-2 rounded-xl text-base font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-colors"
          @click="isMobileMenuOpen = false"
        >
          Gradebook
        </router-link>
        <router-link 
          to="/teacher/quizzes" 
          class="block px-3.5 py-2 rounded-xl text-base font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-colors"
          @click="isMobileMenuOpen = false"
        >
          Quiz Manager
        </router-link>
      </template>

      <!-- Admin Menu -->
      <template v-if="authStore.isAuthenticated && authStore.isAdmin">
        <router-link 
          to="/admin/dashboard" 
          class="block px-3.5 py-2 rounded-xl text-base font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-colors"
          @click="isMobileMenuOpen = false"
        >
          Admin Overview
        </router-link>
        <router-link 
          to="/admin/approvals" 
          class="block px-3.5 py-2 rounded-xl text-base font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-colors"
          @click="isMobileMenuOpen = false"
        >
          Pending Approvals
        </router-link>
        <router-link 
          to="/admin/users" 
          class="block px-3.5 py-2 rounded-xl text-base font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-colors"
          @click="isMobileMenuOpen = false"
        >
          User Controls
        </router-link>
      </template>

      <!-- User Auth (Mobile) -->
      <div class="pt-4.5 border-t border-brand-border flex flex-col space-y-2">
        <!-- Theme Toggle (Mobile) -->
        <button 
          @click="toggleTheme" 
          class="flex items-center justify-between w-full px-4 py-2.5 rounded-xl border border-white/10 text-sm font-semibold text-gray-300 hover:text-white hover:bg-white/5 transition-colors cursor-pointer"
        >
          <span>Theme Mode</span>
          <div class="flex items-center space-x-1.5">
            <template v-if="theme === 'dark'">
              <span class="text-xs text-brand-warning">Dark</span>
              <Sun class="w-4 h-4 text-brand-warning" />
            </template>
            <template v-else>
              <span class="text-xs text-brand-primary">Light</span>
              <Moon class="w-4 h-4 text-brand-primary" />
            </template>
          </div>
        </button>

        <template v-if="!authStore.isAuthenticated">
          <router-link 
            to="/login" 
            class="text-center w-full px-4 py-2.5 rounded-xl border border-white/10 text-sm font-semibold text-gray-300 hover:text-white hover:bg-white/5 transition-colors"
            @click="isMobileMenuOpen = false"
          >
            Sign In
          </router-link>
          <router-link 
            to="/register" 
            class="text-center w-full px-4 py-2.5 rounded-xl bg-brand-primary text-sm font-semibold text-white hover:bg-brand-secondary transition-colors"
            @click="isMobileMenuOpen = false"
          >
            Get Started
          </router-link>
        </template>
        
        <template v-else>
          <div class="px-3.5 py-2 bg-white/5 rounded-xl mb-2 flex items-center space-x-3">
            <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-brand-primary to-brand-secondary flex items-center justify-center font-bold text-white text-sm">
              {{ authStore.currentUser.name.split(' ').map(n => n[0]).join('').slice(0,2).toUpperCase() }}
            </div>
            <div>
              <p class="text-sm font-semibold text-white">{{ authStore.currentUser.name }}</p>
              <p class="text-xs text-gray-400">{{ authStore.currentUser.email }}</p>
            </div>
          </div>
          <button 
            @click="handleLogout"
            class="w-full text-center px-4 py-2.5 rounded-xl bg-brand-danger/10 text-brand-danger hover:bg-brand-danger/20 transition-all font-medium text-sm"
          >
            Sign Out
          </button>
        </template>
      </div>
    </div>
  </nav>
</template>
