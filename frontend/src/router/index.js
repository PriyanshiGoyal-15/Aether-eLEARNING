import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../store/auth';

// Lazy load views for better performance
import Home from '../views/Home.vue';
import CourseDetails from '../views/CourseDetails.vue';
import Login from '../views/auth/Login.vue';
import Register from '../views/auth/Register.vue';

// Student
import StudentDashboard from '../views/student/StudentDashboard.vue';
import CoursePlayer from '../views/student/CoursePlayer.vue';

// Teacher
import TeacherDashboard from '../views/teacher/TeacherDashboard.vue';
import CourseCreator from '../views/teacher/CourseCreator.vue';
import StudentMonitor from '../views/teacher/StudentMonitor.vue';

// Admin
import AdminDashboard from '../views/admin/AdminDashboard.vue';
import CourseApprovals from '../views/admin/CourseApprovals.vue';
import UserManagement from '../views/admin/UserManagement.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/courses/:id',
    name: 'CourseDetails',
    component: CourseDetails
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guestOnly: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { guestOnly: true }
  },
  
  // Student Dashboards
  {
    path: '/student/dashboard',
    name: 'StudentDashboard',
    component: StudentDashboard,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/player/:courseId',
    name: 'CoursePlayer',
    component: CoursePlayer,
    meta: { requiresAuth: true, role: 'student' }
  },

  // Teacher Dashboards
  {
    path: '/teacher/dashboard',
    name: 'TeacherDashboard',
    component: TeacherDashboard,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/create',
    name: 'CourseCreator',
    component: CourseCreator,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/students',
    name: 'StudentMonitor',
    component: StudentMonitor,
    meta: { requiresAuth: true, role: 'teacher' }
  },

  // Admin Dashboards
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/approvals',
    name: 'CourseApprovals',
    component: CourseApprovals,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/users',
    name: 'UserManagement',
    component: UserManagement,
    meta: { requiresAuth: true, role: 'admin' }
  },
  
  // Wildcard fallback
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  }
});

// Enforce Access Guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;
  const userRole = authStore.currentUser?.role;

  // 1. Prevent unauthenticated access
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: 'Login', query: { redirect: to.fullPath } });
  }

  // 2. Prevent guest access to guest-only routes (e.g. login/register when already logged in)
  if (to.meta.guestOnly && isAuthenticated) {
    if (userRole === 'student') return next({ name: 'StudentDashboard' });
    if (userRole === 'teacher') return next({ name: 'TeacherDashboard' });
    if (userRole === 'admin') return next({ name: 'AdminDashboard' });
    return next({ name: 'Home' });
  }

  // 3. Enforce Role-Based protections
  if (to.meta.role && to.meta.role !== userRole) {
    // Redirect unauthorized user to their correct dashboard
    if (userRole === 'student') return next({ name: 'StudentDashboard' });
    if (userRole === 'teacher') return next({ name: 'TeacherDashboard' });
    if (userRole === 'admin') return next({ name: 'AdminDashboard' });
    return next({ name: 'Home' });
  }

  next();
});

export default router;
