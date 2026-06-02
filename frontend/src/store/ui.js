import { defineStore } from 'pinia';

export const useUIStore = defineStore('ui', {
  state: () => ({
    toasts: []
  }),
  actions: {
    addToast(title, message, type = 'info', duration = 4000) {
      const id = Date.now().toString();
      this.toasts.push({ id, title, message, type });
      
      if (duration > 0) {
        setTimeout(() => {
          this.removeToast(id);
        }, duration);
      }
      return id;
    },
    removeToast(id) {
      const index = this.toasts.findIndex(t => t.id === id);
      if (index > -1) {
        this.toasts.splice(index, 1);
      }
    }
  }
});
