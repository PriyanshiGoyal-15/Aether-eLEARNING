import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../store/auth';

// Lazy load views for better performance
import Home from '../views/Home.vue';
import CourseDetails from '../views/CourseDetails.vue';
import Login from '../views/auth/Login.vue';
import Register from '../views/auth/Register.vue';

// Student
import StudentDashboard from '../views/student/StudentDashboard.vue';
import ExploreCourses from '../views/student/ExploreCourses.vue';
import CoursePlayer from '../views/student/CoursePlayer.vue';
import QuizArena from '../views/student/QuizArena.vue';

// Teacher
import TeacherDashboard from '../views/teacher/TeacherDashboard.vue';
import CourseCreator from '../views/teacher/CourseCreator.vue';
import StudentMonitor from '../views/teacher/StudentMonitor.vue';
import QuizManager from '../views/teacher/QuizManager.vue';

// Admin
import AdminDashboard from '../views/admin/AdminDashboard.vue';
import CourseApprovals from '../views/admin/CourseApprovals.vue';
import UserManagement from '../views/admin/UserManagement.vue';

// Shared
import Inbox from '../views/Inbox.vue';
import NotFound from '../views/NotFound.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/courses/:id',
    name: 'CourseDetails',
    component: CourseDetails,
    meta: { requiresAuth: true }
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
  {
    path: '/inbox',
    name: 'Inbox',
    component: Inbox,
    meta: { requiresAuth: true }
  },

  // Student Dashboards
  {
    path: '/student/dashboard',
    name: 'StudentDashboard',
    component: StudentDashboard,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/courses',
    name: 'ExploreCourses',
    component: ExploreCourses,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/player/:courseId',
    name: 'CoursePlayer',
    component: CoursePlayer,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/quizzes',
    name: 'QuizArena',
    component: QuizArena,
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
    path: '/teacher/edit/:id',
    name: 'CourseEditor',
    component: CourseCreator,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/students',
    name: 'StudentMonitor',
    component: StudentMonitor,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/quizzes',
    name: 'QuizManager',
    component: QuizManager,
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
    name: 'NotFound',
    component: NotFound,
    meta: { title: 'Page Not Found' }
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

// Dynamic Document Title updater
router.afterEach((to) => {
  const defaultTitle = 'Aether - Premium Tech Education';
  if (to.meta && to.meta.title) {
    document.title = `${to.meta.title} - Aether`;
  } else if (to.name) {
    // Format route name (e.g. 'CourseDetails' -> 'Course Details')
    const formattedName = to.name.replace(/([A-Z])/g, ' $1').trim();
    document.title = `${formattedName} - Aether`;
  } else {
    document.title = defaultTitle;
  }
});

export default router;
