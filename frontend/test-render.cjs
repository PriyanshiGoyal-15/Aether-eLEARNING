const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();

  await context.addInitScript(() => {
    localStorage.setItem('aether_auth_token', 'mock_token');
    localStorage.setItem('aether_user', JSON.stringify({
      id: 'user-teacher',
      name: 'Mock Teacher',
      email: 'teacher@aether.edu',
      role: 'teacher'
    }));
  });

  const page = await context.newPage();

  page.on('console', msg => console.log('LOG:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

  await page.goto('http://localhost:5173/teacher/quizzes', { waitUntil: 'networkidle' });

  // Wait a bit to ensure async errors are caught
  await page.waitForTimeout(2000);

  await browser.close();
})();
