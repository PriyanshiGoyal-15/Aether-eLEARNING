import { defineStore } from 'pinia';

const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000/api'
  : 'https://aether-elearning-backend.onrender.com/api';

export const useAuthStore = defineStore('auth', {
  state: () => {
    const currentUser = JSON.parse(localStorage.getItem('aether_current_user')) || null;

    return {
      users: [],
      currentUser,
    };
  },
  
  getters: {
    isAuthenticated: (state) => state.currentUser !== null,
    isStudent: (state) => state.currentUser?.role === 'student',
    isTeacher: (state) => state.currentUser?.role === 'teacher',
    isAdmin: (state) => state.currentUser?.role === 'admin',
  },

  actions: {
    async fetchUsers() {
      try {
        const response = await fetch(`${API_BASE}/db`);
        if (!response.ok) throw new Error('Failed to load user database');
        const db = await response.json();
        this.users = db.users;
        
        // Refresh current user status (e.g. if suspended by admin in background)
        if (this.currentUser) {
          const freshUser = this.users.find(u => u.id === this.currentUser.id);
          if (freshUser) {
            if (freshUser.suspended) {
              this.logout();
              throw new Error("Your account has been suspended by the administrator.");
            }
            this.currentUser = { ...freshUser };
            localStorage.setItem('aether_current_user', JSON.stringify(this.currentUser));
          }
        }
      } catch (err) {
        console.error('Error fetching users:', err);
      }
    },

    async login(email, password) {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Invalid email or password.");
      }

      const user = await response.json();
      this.currentUser = user;
      localStorage.setItem('aether_current_user', JSON.stringify(this.currentUser));
      await this.fetchUsers();
      return this.currentUser;
    },

    async register(name, email, password, role, verificationDoc = null) {
      const response = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, role, verificationDoc })
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "An account with this email already exists.");
      }

      const newUser = await response.json();
      if (newUser.role !== 'teacher') {
        this.currentUser = newUser;
        localStorage.setItem('aether_current_user', JSON.stringify(this.currentUser));
      }
      await this.fetchUsers();
      return newUser;
    },

    logout() {
      this.currentUser = null;
      localStorage.removeItem('aether_current_user');
    },

    // Administrative Actions
    async verifyTeacher(userId) {
      const response = await fetch(`${API_BASE}/users/${userId}/verify`, {
        method: 'POST'
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to verify educator account.");
      }

      await this.fetchUsers();
    },

    async toggleSuspension(userId) {
      if (this.currentUser?.id === userId) {
        throw new Error("Cannot suspend yourself!");
      }
      
      const response = await fetch(`${API_BASE}/users/${userId}/suspend`, {
        method: 'POST'
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to update suspension status.");
      }

      await this.fetchUsers();
    },

    async deleteUser(userId) {
      if (this.currentUser?.id === userId) {
        throw new Error("Cannot delete yourself!");
      }

      const response = await fetch(`${API_BASE}/users/${userId}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to delete user.");
      }

      await this.fetchUsers();
    }
  }
});

