<script setup>
import { useUIStore } from '../store/ui';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-vue-next';

const uiStore = useUIStore();
</script>

<template>
  <div class="fixed top-4 right-4 z-9999 flex flex-col space-y-3 pointer-events-none w-full max-w-sm">
    <TransitionGroup 
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="transform translate-x-12 opacity-0"
      enter-to-class="transform translate-x-0 opacity-100"
      leave-active-class="transition duration-200 ease-in absolute w-full"
      leave-from-class="transform translate-x-0 opacity-100"
      leave-to-class="transform translate-x-12 opacity-0 scale-95"
      move-class="transition duration-300 ease-in-out"
    >
      <div 
        v-for="toast in uiStore.toasts" 
        :key="toast.id"
        class="pointer-events-auto rounded-2xl p-4 shadow-2xl border backdrop-blur-md flex items-start space-x-3 overflow-hidden"
        :class="{
          'bg-brand-card/95 border-brand-accent/30': toast.type === 'success',
          'bg-brand-card/95 border-brand-danger/30': toast.type === 'error',
          'bg-brand-card/95 border-brand-primary/30': toast.type === 'info',
          'bg-brand-card/95 border-brand-warning/30': toast.type === 'warning',
        }"
      >
        <!-- Icon based on type -->
        <div 
          class="shrink-0 p-1.5 rounded-xl border flex items-center justify-center mt-0.5"
          :class="{
            'bg-brand-accent/15 text-brand-accent border-brand-accent/20': toast.type === 'success',
            'bg-brand-danger/15 text-brand-danger border-brand-danger/20': toast.type === 'error',
            'bg-brand-primary/15 text-brand-primary border-brand-primary/20': toast.type === 'info',
            'bg-brand-warning/15 text-brand-warning border-brand-warning/20': toast.type === 'warning',
          }"
        >
          <CheckCircle v-if="toast.type === 'success'" class="w-4.5 h-4.5" />
          <AlertCircle v-else-if="toast.type === 'error'" class="w-4.5 h-4.5" />
          <Info v-else-if="toast.type === 'info'" class="w-4.5 h-4.5" />
          <AlertTriangle v-else-if="toast.type === 'warning'" class="w-4.5 h-4.5" />
        </div>

        <div class="flex-1 space-y-1 pr-2">
          <h4 class="text-sm font-bold text-white leading-tight font-display">{{ toast.title }}</h4>
          <p class="text-xs text-gray-300 leading-normal">{{ toast.message }}</p>
        </div>

        <button 
          @click="uiStore.removeToast(toast.id)"
          class="shrink-0 text-gray-500 hover:text-white transition-colors p-1"
        >
          <X class="w-4 h-4" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>
