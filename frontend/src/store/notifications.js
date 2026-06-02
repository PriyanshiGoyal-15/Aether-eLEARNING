import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notifications', {
  state: () => ({
    toasts: [],
    modal: {
      active: false,
      title: '',
      message: '',
      type: 'info', // success, info, warning, danger
      confirmText: 'Confirm',
      cancelText: 'Cancel',
      resolve: null,
    }
  }),

  actions: {
    showToast(title, message, type = 'info', duration = 4000) {
      const id = `toast-${Date.now()}`;
      this.toasts.push({ id, title, message, type });
      
      setTimeout(() => {
        this.removeToast(id);
      }, duration);
    },

    removeToast(id) {
      this.toasts = this.toasts.filter(t => t.id !== id);
    },

    showConfirm(title, message, type = 'warning', confirmText = 'Confirm', cancelText = 'Cancel') {
      return new Promise((resolve) => {
        this.modal = {
          active: true,
          title,
          message,
          type,
          confirmText,
          cancelText,
          resolve: (result) => {
            this.modal.active = false;
            resolve(result);
          }
        };
      });
    },

    showAlert(title, message, type = 'info', confirmText = 'OK') {
      return new Promise((resolve) => {
        this.modal = {
          active: true,
          title,
          message,
          type,
          confirmText,
          cancelText: '', // Hide cancel button for basic alerts
          resolve: () => {
            this.modal.active = false;
            resolve(true);
          }
        };
      });
    }
  }
});
