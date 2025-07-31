// @ts-check
const { test, expect } = require('@playwright/test');

test('MCP Server Application Screenshots', async ({ page }) => {
  // Navigate to the application
  await page.goto('/');
  
  // Wait for the page to load
  await page.waitForTimeout(2000);
  
  // Take screenshot of the main page
  await page.screenshot({ path: 'screenshots/main-page.png' });
  
  // Fill in login credentials
  await page.getByLabel('Username').fill('user');
  await page.getByLabel('Password', { exact: true }).fill('user123');
  
  // Take screenshot of login form
  await page.screenshot({ path: 'screenshots/login-form.png' });
  
  // Click login button
  await page.getByRole('button', { name: 'Login' }).click();
  
  // Wait for login to complete
  await page.waitForTimeout(2000);
  
  // Take screenshot of logged in state
  await page.screenshot({ path: 'screenshots/logged-in.png' });
  
  // Select CSV/Excel Reader tool
  await page.getByRole('combobox', { name: 'Select a tool to use:' }).selectOption('CSV/Excel Reader');
  
  // Wait for the tool to load
  await page.waitForTimeout(2000);
  
  // Take screenshot of CSV Reader tool
  await page.screenshot({ path: 'screenshots/csv-reader-tool.png' });
  
  // Select CSV/Excel Analyzer tool
  await page.getByRole('combobox', { name: 'Select a tool to use:' }).selectOption('CSV/Excel Analyzer');
  
  // Wait for the tool to load
  await page.waitForTimeout(2000);
  
  // Take screenshot of CSV Analyzer tool
  await page.screenshot({ path: 'screenshots/csv-analyzer-tool.png' });
  
  // For admin users, also test OPA Policy Evaluator
  // First logout
  await page.getByRole('button', { name: 'Logout' }).click();
  
  // Wait for logout
  await page.waitForTimeout(2000);
  
  // Login as admin
  await page.getByLabel('Username').fill('admin');
  await page.getByLabel('Password', { exact: true }).fill('admin123');
  await page.getByRole('button', { name: 'Login' }).click();
  
  // Wait for login
  await page.waitForTimeout(2000);
  
  // Select OPA Policy Evaluator tool
  await page.getByRole('combobox', { name: 'Select a tool to use:' }).selectOption('OPA Policy Evaluator');
  
  // Wait for the tool to load
  await page.waitForTimeout(2000);
  
  // Take screenshot of OPA Policy Evaluator tool
  await page.screenshot({ path: 'screenshots/opa-policy-evaluator-tool.png' });
});