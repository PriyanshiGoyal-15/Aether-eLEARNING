<script setup>
import { Award } from 'lucide-vue-next';
</script>

<template>
  <footer class="bg-brand-dark border-t border-white/5 py-8 mt-16">
    <div class="max-w-[1680px] mx-auto px-6 md:px-12 lg:px-16 flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
      <div class="flex items-center space-x-2">
        <span class="p-1.5 rounded-lg bg-gradient-to-tr from-brand-primary to-brand-secondary text-white">
          <Award class="w-4.5 h-4.5" />
        </span>
        <span class="text-sm font-semibold tracking-wider text-gray-300 font-display">AETHER ACADEMY</span>
      </div>
      
      <p class="text-xs text-gray-500 font-medium">
        &copy; 2026 Aether E-Learning Platform. Engineered with Vue 3, Tailwind CSS & Pinia. All rights reserved.
      </p>

      <div class="flex space-x-4 text-xs text-gray-400">
        <a href="#" class="hover:text-white transition-colors">Privacy Policy</a>
        <a href="#" class="hover:text-white transition-colors">Terms of Use</a>
        <a href="#" class="hover:text-white transition-colors">Support</a>
      </div>
    </div>
  </footer>
</template>
