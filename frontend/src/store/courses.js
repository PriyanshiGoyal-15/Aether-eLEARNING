import { defineStore } from 'pinia';
import { useAuthStore } from './auth';

const API_BASE = 'https://aether-elearning.onrender.com/api';

export const useCoursesStore = defineStore('courses', {
  state: () => {
    return {
      courses: [],
      enrollments: [],
      bookmarks: [],
      reviews: [],
      notifications: [],
    };
  },

  getters: {
    // Student selectors
    approvedCourses: (state) => state.courses.filter(c => c.status === 'approved'),
    pendingCourses: (state) => state.courses.filter(c => c.status === 'pending'),

    // Get enrollment for a student & course
    getEnrollment: (state) => (studentId, courseId) => {
      return state.enrollments.find(e => e.studentId === studentId && e.courseId === courseId);
    },

    // Get student's enrolled courses complete with details & progress
    getStudentEnrollments: (state) => (studentId) => {
      return state.enrollments
        .filter(e => e.studentId === studentId)
        .map(enroll => {
          const course = state.courses.find(c => c.id === enroll.courseId);
          return {
            ...enroll,
            course
          };
        }).filter(e => e.course !== undefined);
    },

    // Get student bookmarks
    getStudentBookmarks: (state) => (studentId) => {
      const bookmarkedIds = state.bookmarks
        .filter(b => b.studentId === studentId)
        .map(b => b.courseId);

      return state.courses.filter(c => bookmarkedIds.includes(c.id) && c.status === 'approved');
    },

    // Get Course Reviews
    getCourseReviews: (state) => (courseId) => {
      return state.reviews.filter(r => r.courseId === courseId);
    },

    // Get Unread Notification Count
    getUnreadNotificationCount: (state) => (userId) => {
      return state.notifications.filter(n => n.userId === userId && !n.read).length;
    },

    // Get User Notifications
    getUserNotifications: (state) => (userId) => {
      return state.notifications.filter(n => n.userId === userId);
    },

    // Certificates (Completed courses - progressPercent is 100)
    getCertificates: (state) => (studentId) => {
      return state.enrollments
        .filter(e => e.studentId === studentId && e.progressPercent === 100)
        .map(enroll => {
          const course = state.courses.find(c => c.id === enroll.courseId);
          return {
            id: `CERT-${enroll.id.toUpperCase()}`,
            courseId: enroll.courseId,
            courseTitle: course?.title || 'Unknown Course',
            completedDate: enroll.completedDate || enroll.enrolledDate,
            instructor: course?.teacherName || 'Aether Academy'
          };
        });
    },

    // Teacher course selectors
    getTeacherCourses: (state) => (teacherId) => {
      return state.courses.filter(c => c.teacherId === teacherId);
    },

    // Students tracking for a teacher
    getTeacherStudents: (state) => (teacherId) => {
      const authStore = useAuthStore();
      const teacherCourses = state.courses.filter(c => c.teacherId === teacherId);
      const teacherCourseIds = teacherCourses.map(c => c.id);

      return state.enrollments
        .filter(e => teacherCourseIds.includes(e.courseId))
        .map(enroll => {
          const course = teacherCourses.find(c => c.id === enroll.courseId);
          const student = authStore.users.find(u => u.id === enroll.studentId);
          return {
            id: enroll.id,
            studentName: student?.name || "Unknown Student",
            studentEmail: student?.email || "",
            courseTitle: course?.title || "Deleted Course",
            progressPercent: enroll.progressPercent,
            enrolledDate: enroll.enrolledDate
          };
        });
    },

    // Admin Dashboard Statistics
    getAdminStats: (state) => {
      const authStore = useAuthStore();
      const totalStudents = authStore.users.filter(u => u.role === 'student').length;
      const totalTeachers = authStore.users.filter(u => u.role === 'teacher').length;
      const activeCourses = state.courses.filter(c => c.status === 'approved').length;
      const pendingApprovals = state.courses.filter(c => c.status === 'pending').length;

      // Group enrollment numbers to find popular courses
      const enrollmentCounts = state.enrollments.reduce((acc, curr) => {
        acc[curr.courseId] = (acc[curr.courseId] || 0) + 1;
        return acc;
      }, {});

      const popularCourses = state.courses
        .filter(c => c.status === 'approved')
        .map(c => ({
          title: c.title,
          enrollmentsCount: enrollmentCounts[c.id] || 0,
          category: c.category,
          rating: c.rating
        }))
        .sort((a, b) => b.enrollmentsCount - a.enrollmentsCount)
        .slice(0, 5);

      return {
        totalStudents,
        totalTeachers,
        activeCourses,
        pendingApprovals,
        popularCourses
      };
    }
  },

  actions: {
    async fetchCoursesData() {
      const authStore = useAuthStore();
      try {
        const response = await fetch(`${API_BASE}/db`);
        if (!response.ok) throw new Error('Failed to load database');
        const db = await response.json();

        this.courses = db.courses;
        this.enrollments = db.enrollments;
        this.bookmarks = db.bookmarks || [];
        this.reviews = db.reviews;
        this.notifications = db.notifications;

        // Also hydrate authStore users
        authStore.users = db.users;
      } catch (err) {
        console.error('Error fetching courses database state:', err);
      }
    },

    async enrollInCourse(studentId, courseId) {
      const response = await fetch(`${API_BASE}/courses/${courseId}/enroll?studentId=${studentId}`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error("Failed to enroll in course.");
      await this.fetchCoursesData();
    },

    async toggleLessonCompletion(studentId, courseId, lessonId) {
      const response = await fetch(`${API_BASE}/courses/${courseId}/lesson-toggle?studentId=${studentId}&lessonId=${lessonId}`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error("Failed to toggle lesson completion.");
      await this.fetchCoursesData();
    },

    async toggleBookmark(studentId, courseId) {
      const response = await fetch(`${API_BASE}/courses/${courseId}/bookmark?studentId=${studentId}`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error("Failed to toggle bookmark.");
      await this.fetchCoursesData();
    },

    isBookmarked(studentId, courseId) {
      return this.bookmarks.some(b => b.studentId === studentId && b.courseId === courseId);
    },

    async submitReview(courseId, studentName, rating, comment) {
      const response = await fetch(`${API_BASE}/courses/${courseId}/reviews`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ studentName, rating, comment })
      });
      if (!response.ok) throw new Error("Failed to submit review.");
      await this.fetchCoursesData();
    },

    async addNotification(userId, title, message, type = 'info') {
      const response = await fetch(`${API_BASE}/notifications`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, title, message, type })
      });
      if (!response.ok) throw new Error("Failed to send notification.");
      await this.fetchCoursesData();
    },

    async markAllNotificationsAsRead(userId) {
      const response = await fetch(`${API_BASE}/notifications/read?userId=${userId}`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error("Failed to mark notifications as read.");
      await this.fetchCoursesData();
    },

    async createCourse(teacherId, teacherName, title, description, category, difficulty, thumbnail, modules) {
      const response = await fetch(`${API_BASE}/courses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          teacherId,
          teacherName,
          title,
          description,
          category,
          difficulty,
          thumbnail,
          modules
        })
      });
      if (!response.ok) throw new Error("Failed to create course.");
      const newCourse = await response.json();
      await this.fetchCoursesData();
      return newCourse;
    },

    async approveCourse(courseId) {
      const response = await fetch(`${API_BASE}/courses/${courseId}/approve`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error("Failed to approve course.");
      await this.fetchCoursesData();
    },

    async rejectCourse(courseId, reason) {
      const response = await fetch(`${API_BASE}/courses/${courseId}/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reason })
      });
      if (!response.ok) throw new Error("Failed to reject course.");
      await this.fetchCoursesData();
    },

    async autoCompleteCourse(studentId, courseId) {
      const response = await fetch(`${API_BASE}/courses/${courseId}/auto-complete?studentId=${studentId}`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error("Failed to auto-complete course.");
      await this.fetchCoursesData();
    },

    async resetDatabase() {
      const response = await fetch(`${API_BASE}/system/reset`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error("Failed to reset database.");
      localStorage.clear();
      window.location.reload();
    }
  }
});
