<script setup>
import { useNotificationStore } from '../store/notifications';
import { 
  CheckCircle, AlertCircle, AlertTriangle, Info, X, ShieldAlert 
} from 'lucide-vue-next';

const notifStore = useNotificationStore();
</script>

<template>
  <div>
    <!-- Toast Notifications Stack (Top Right Corner) -->
    <div class="fixed top-20 right-6 z-[9999] flex flex-col space-y-3.5 max-w-sm w-full pointer-events-none">
      <transition-group name="toast-list">
        <div 
          v-for="toast in notifStore.toasts" 
          :key="toast.id"
          class="pointer-events-auto w-full glass-panel rounded-2xl border p-4 shadow-2xl flex items-start space-x-3.5 relative overflow-hidden animate-fade-in transition-all duration-300"
          :class="{
            'bg-brand-card/95 border-brand-accent/30 shadow-brand-accent/5': toast.type === 'success',
            'bg-brand-card/95 border-brand-primary/30 shadow-brand-primary/5': toast.type === 'info',
            'bg-brand-card/95 border-brand-warning/30 shadow-brand-warning/5': toast.type === 'warning',
            'bg-brand-card/95 border-brand-danger/30 shadow-brand-danger/5': toast.type === 'danger'
          }"
        >
          <!-- Progress bar glow indicator -->
          <div 
            class="absolute bottom-0 left-0 h-1 bg-gradient-to-r transition-all duration-[4000ms] w-full animate-toast-progress"
            :class="{
              'from-brand-accent to-emerald-500': toast.type === 'success',
              'from-brand-primary to-indigo-500': toast.type === 'info',
              'from-brand-warning to-amber-500': toast.type === 'warning',
              'from-brand-danger to-rose-500': toast.type === 'danger'
            }"
          ></div>

          <!-- Type Icon -->
          <span 
            class="p-1.5 rounded-xl shrink-0 mt-0.5 flex items-center justify-center"
            :class="{
              'bg-brand-accent/15 text-brand-accent': toast.type === 'success',
              'bg-brand-primary/15 text-brand-primary': toast.type === 'info',
              'bg-brand-warning/15 text-brand-warning': toast.type === 'warning',
              'bg-brand-danger/15 text-brand-danger': toast.type === 'danger'
            }"
          >
            <CheckCircle v-if="toast.type === 'success'" class="w-5 h-5" />
            <Info v-else-if="toast.type === 'info'" class="w-5 h-5" />
            <AlertTriangle v-else-if="toast.type === 'warning'" class="w-5 h-5" />
            <AlertCircle v-else class="w-5 h-5" />
          </span>

          <!-- Text block -->
          <div class="space-y-1 flex-grow pr-4">
            <h4 class="text-xs font-bold text-white leading-tight font-display">{{ toast.title }}</h4>
            <p class="text-[11px] text-gray-400 leading-relaxed font-light">{{ toast.message }}</p>
          </div>

          <!-- Close button -->
          <button 
            @click="notifStore.removeToast(toast.id)"
            class="absolute top-3.5 right-3.5 text-gray-500 hover:text-white transition-colors cursor-pointer"
          >
            <X class="w-4 h-4" />
          </button>
        </div>
      </transition-group>
    </div>

    <!-- Custom Glassmorphism Confirmation/Alert Modal Backdrop -->
    <transition name="modal-fade">
      <div 
        v-if="notifStore.modal.active"
        class="fixed inset-0 z-[9998] flex items-center justify-center p-4 bg-brand-dark/70 backdrop-blur-sm"
        @click.self="notifStore.modal.cancelText ? notifStore.modal.resolve(false) : null"
      >
        <!-- Modal Card -->
        <div 
          class="glass-panel max-w-md w-full rounded-3xl border border-white/10 p-6 md:p-8 bg-brand-card shadow-2xl space-y-6 transform scale-100 transition-all duration-300 animate-modal-pop"
          :class="{
            'border-brand-accent/25 shadow-brand-accent/5': notifStore.modal.type === 'success',
            'border-brand-primary/25 shadow-brand-primary/5': notifStore.modal.type === 'info',
            'border-brand-warning/25 shadow-brand-warning/5': notifStore.modal.type === 'warning',
            'border-brand-danger/25 shadow-brand-danger/5': notifStore.modal.type === 'danger'
          }"
        >
          <!-- Header Icon & Text -->
          <div class="flex flex-col items-center text-center space-y-3.5">
            <span 
              class="p-4 rounded-2xl shrink-0 flex items-center justify-center shadow-lg"
              :class="{
                'bg-brand-accent/15 text-brand-accent shadow-brand-accent/10': notifStore.modal.type === 'success',
                'bg-brand-primary/15 text-brand-primary shadow-brand-primary/10': notifStore.modal.type === 'info',
                'bg-brand-warning/15 text-brand-warning shadow-brand-warning/10': notifStore.modal.type === 'warning',
                'bg-brand-danger/15 text-brand-danger shadow-brand-danger/10': notifStore.modal.type === 'danger'
              }"
            >
              <CheckCircle v-if="notifStore.modal.type === 'success'" class="w-8 h-8" />
              <Info v-else-if="notifStore.modal.type === 'info'" class="w-8 h-8" />
              <AlertTriangle v-else-if="notifStore.modal.type === 'warning'" class="w-8 h-8" />
              <ShieldAlert v-else class="w-8 h-8" />
            </span>
            
            <div class="space-y-1.5">
              <h3 class="text-lg md:text-xl font-extrabold text-white font-display leading-tight">{{ notifStore.modal.title }}</h3>
              <p class="text-xs text-gray-400 leading-relaxed font-light">{{ notifStore.modal.message }}</p>
            </div>
          </div>

          <!-- Actions buttons -->
          <div class="flex items-center gap-3">
            <button 
              v-if="notifStore.modal.cancelText"
              @click="notifStore.modal.resolve(false)"
              class="flex-1 py-3 text-xs font-bold bg-white/5 border border-white/10 text-gray-300 hover:text-white rounded-xl transition-all cursor-pointer text-center"
            >
              {{ notifStore.modal.cancelText }}
            </button>
            <button 
              @click="notifStore.modal.resolve(true)"
              class="flex-1 py-3 text-xs font-bold text-white rounded-xl transition-all shadow-lg cursor-pointer text-center"
              :class="{
                'bg-brand-accent hover:bg-emerald-600 shadow-brand-accent/10': notifStore.modal.type === 'success',
                'bg-brand-primary hover:bg-brand-secondary shadow-brand-primary/10': notifStore.modal.type === 'info',
                'bg-brand-warning hover:opacity-95 shadow-brand-warning/10': notifStore.modal.type === 'warning',
                'bg-brand-danger hover:opacity-95 shadow-brand-danger/10': notifStore.modal.type === 'danger'
              }"
            >
              {{ notifStore.modal.confirmText }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style>
/* Toast List Transitions */
.toast-list-enter-active,
.toast-list-leave-active {
  transition: all 0.3s ease;
}
.toast-list-enter-from {
  opacity: 0;
  transform: translateX(30px) scale(0.9);
}
.toast-list-leave-to {
  opacity: 0;
  transform: translateX(30px) scale(0.9);
}

/* Modal Transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

@keyframes toastProgress {
  from { width: 100%; }
  to { width: 0%; }
}
.animate-toast-progress {
  animation: toastProgress 4000ms linear forwards;
}

@keyframes modalPop {
  from { transform: scale(0.9) translateY(10px); }
  to { transform: scale(1) translateY(0); }
}
.animate-modal-pop {
  animation: modalPop 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
</style>
