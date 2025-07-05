import { test, expect } from '@playwright/test';

/**
 * End-to-end tests for authentication flows
 */
test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    // Go to the home page before each test
    await page.goto('/');
  });

  test('login page is accessible', async ({ page }) => {
    // Click the login button/link
    await page.getByRole('link', { name: /sign in/i, exact: false }).click();

    // Check that we're on the login page
    await expect(page).toHaveURL(/.*\/login/);

    // Verify login form elements exist
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Sign In' })).toBeVisible();
  });

  test('shows validation errors with invalid credentials', async ({ page }) => {
    // Navigate to login page
    await page.goto('/login');

    // Try to login with empty credentials
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Expect validation error
    await expect(page.getByText('Email is required')).toBeVisible();

    // Try with invalid email format
    await page.getByLabel('Email').fill('invalid-email');
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Expect email format validation error
    await expect(page.getByText('Invalid email format')).toBeVisible();

    // Try with valid email but no password
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Expect password validation error
    await expect(page.getByText('Password is required')).toBeVisible();

    // Try with invalid credentials
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByLabel('Password').fill('wrongpassword');
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Expect authentication error
    await expect(page.getByText(/invalid credentials|incorrect password/i)).toBeVisible();
  });

  // This test would require test accounts to be set up in the test environment
  test('can login with valid credentials', async ({ page }) => {
    // Test credentials - should be environment variables in real setup
    // NOTE: These are placeholder credentials that should be replaced with test accounts
    const testEmail = 'test-reporter@example.com';
    const testPassword = 'test-password';

    // Navigate to login page
    await page.goto('/login');

    // Fill in credentials
    await page.getByLabel('Email').fill(testEmail);
    await page.getByLabel('Password').fill(testPassword);

    // Click sign in button
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Expect to be redirected to dashboard after successful login
    await expect(page).toHaveURL(/.*\/dashboard/);

    // Verify user is logged in by checking for profile menu or username display
    await expect(page.getByText(/welcome|profile|account/i)).toBeVisible();
  });

  test('can access registration page', async ({ page }) => {
    // Navigate to login page first
    await page.goto('/login');

    // Click on register/sign up link
    await page.getByRole('link', { name: /sign up|register|create account/i }).click();

    // Verify we're on registration page
    await expect(page).toHaveURL(/.*\/register/);

    // Check registration form elements
    await expect(page.getByLabel('Name')).toBeVisible();
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
    await expect(
      page.getByRole('button', { name: /sign up|register|create account/i })
    ).toBeVisible();
  });

  test('can logout after login', async ({ page }) => {
    // This would require logging in first, but we'll skip that step for this example
    // and just check that the logout functionality works

    // First, we need to login
    // NOTE: Setup a test user login helper function for this
    await page.goto('/login');
    await page.getByLabel('Email').fill('test-reporter@example.com');
    await page.getByLabel('Password').fill('test-password');
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Wait for navigation to dashboard
    await page.waitForURL(/.*\/dashboard/);

    // Find and click logout button/link (often in a dropdown menu)
    // This will depend on your UI layout
    await page.getByRole('button', { name: /profile|account|user/i }).click();
    await page.getByRole('button', { name: /logout|sign out/i }).click();

    // Verify logged out - usually redirected to home page or login page
    await expect(page).toHaveURL(/.*\/(login|$)/);

    // Verify logged-out state by checking for login button
    await expect(page.getByRole('link', { name: /sign in|login/i })).toBeVisible();
  });
});
