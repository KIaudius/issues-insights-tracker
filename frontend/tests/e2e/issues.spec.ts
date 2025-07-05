import { test, expect } from '@playwright/test';

/**
 * End-to-end tests for issue management functionality
 */
test.describe('Issue Management', () => {
  // Helper function to login before tests
  async function login(page, role = 'reporter') {
    await page.goto('/login');

    // Choose login credentials based on role
    let email, password;
    switch (role) {
      case 'admin':
        email = 'test-admin@example.com';
        password = 'admin-password';
        break;
      case 'maintainer':
        email = 'test-maintainer@example.com';
        password = 'maintainer-password';
        break;
      case 'reporter':
      default:
        email = 'test-reporter@example.com';
        password = 'reporter-password';
        break;
    }

    // Perform login
    await page.getByLabel('Email').fill(email);
    await page.getByLabel('Password').fill(password);
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Wait for dashboard to load
    await page.waitForURL(/.*\/dashboard/);
  }

  test.beforeEach(async ({ page }) => {
    // Login as reporter before each test
    await login(page, 'reporter');

    // Navigate to issues page
    await page.goto('/issues');

    // Wait for issue list to load
    await page.waitForSelector('[data-testid="issue-list"]');
  });

  test('can view issue list', async ({ page }) => {
    // Verify issue list components
    await expect(page.getByRole('heading', { name: /issues/i })).toBeVisible();
    await expect(page.getByTestId('issue-list')).toBeVisible();

    // Verify filter components exist
    await expect(page.getByTestId('issue-filters')).toBeVisible();
    await expect(page.getByRole('combobox', { name: /status/i })).toBeVisible();
    await expect(page.getByRole('combobox', { name: /severity/i })).toBeVisible();

    // Verify pagination controls if there are multiple pages
    if (await page.getByTestId('pagination').isVisible()) {
      await expect(page.getByTestId('pagination')).toBeVisible();
    }
  });

  test('can create a new issue', async ({ page }) => {
    // Click create new issue button
    await page.getByRole('button', { name: /create|new issue/i }).click();

    // Wait for modal or page to load
    await page.waitForSelector('[data-testid="issue-form"]');

    // Fill in issue form
    await page.getByLabel('Title').fill('Test Issue Created by E2E Test');
    await page
      .getByLabel('Description')
      .fill('This is a test issue created during automated end-to-end testing.');
    await page.getByLabel(/severity/i).selectOption('MEDIUM');

    // Submit form
    await page.getByRole('button', { name: /submit|create|save/i }).click();

    // Verify success message
    await expect(page.getByText(/issue created successfully/i)).toBeVisible();

    // Verify issue appears in the list
    await page.goto('/issues');
    await expect(page.getByText('Test Issue Created by E2E Test')).toBeVisible();
  });

  test('can view issue details', async ({ page }) => {
    // Find and click on the first issue in the list
    await page.getByTestId('issue-list').getByRole('link').first().click();

    // Wait for issue details to load
    await page.waitForSelector('[data-testid="issue-details"]');

    // Verify issue details components
    await expect(page.getByTestId('issue-details')).toBeVisible();
    await expect(page.getByTestId('issue-title')).toBeVisible();
    await expect(page.getByTestId('issue-description')).toBeVisible();
    await expect(page.getByTestId('issue-metadata')).toBeVisible();

    // Verify issue status and severity are displayed
    await expect(page.getByTestId('issue-status')).toBeVisible();
    await expect(page.getByTestId('issue-severity')).toBeVisible();
  });

  test('reporter cannot change issue status', async ({ page }) => {
    // Find and click on the first issue in the list
    await page.getByTestId('issue-list').getByRole('link').first().click();

    // Wait for issue details to load
    await page.waitForSelector('[data-testid="issue-details"]');

    // Status change buttons/dropdown should not be visible to reporters
    await expect(page.getByRole('button', { name: /change status/i })).not.toBeVisible();
  });

  test('maintainer can change issue status', async ({ page }) => {
    // First logout if already logged in
    await page.goto('/logout');

    // Login as maintainer
    await login(page, 'maintainer');

    // Navigate to issues
    await page.goto('/issues');

    // Find and click on the first issue in the list
    await page.getByTestId('issue-list').getByRole('link').first().click();

    // Wait for issue details to load
    await page.waitForSelector('[data-testid="issue-details"]');

    // Status change control should be visible to maintainers
    await expect(page.getByRole('button', { name: /change status/i })).toBeVisible();

    // Open status change dropdown/modal
    await page.getByRole('button', { name: /change status/i }).click();

    // Select new status
    await page.getByRole('radio', { name: 'IN_PROGRESS' }).click();

    // Confirm status change
    await page.getByRole('button', { name: /save|update|confirm/i }).click();

    // Verify success message
    await expect(page.getByText(/status updated/i)).toBeVisible();

    // Verify status has changed
    await expect(page.getByTestId('issue-status')).toContainText('IN_PROGRESS');
  });

  test('can add comments to an issue', async ({ page }) => {
    // Find and click on the first issue in the list
    await page.getByTestId('issue-list').getByRole('link').first().click();

    // Wait for issue details to load
    await page.waitForSelector('[data-testid="issue-details"]');

    // Scroll to comments section
    await page.getByTestId('issue-comments').scrollIntoViewIfNeeded();

    // Type a new comment
    await page.getByTestId('comment-textarea').fill('This is a test comment from E2E testing');

    // Submit comment
    await page.getByRole('button', { name: /post|add|submit comment/i }).click();

    // Verify comment appears
    await expect(page.getByText('This is a test comment from E2E testing')).toBeVisible();
  });

  test('search functionality returns matching issues', async ({ page }) => {
    // Navigate to issues page
    await page.goto('/issues');

    // Enter search term
    await page.getByTestId('search-input').fill('Test Issue');

    // Submit search (either by clicking a button or pressing Enter)
    await page.keyboard.press('Enter');

    // Wait for search results
    await page.waitForSelector('[data-testid="issue-list"]');

    // Verify search results contain the search term
    const issueCount = await page.getByTestId('issue-list').getByRole('link').count();
    expect(issueCount).toBeGreaterThan(0);

    // Check if at least one issue title contains the search term
    const foundMatchingIssue = await page.getByText(/Test Issue/i).isVisible();
    expect(foundMatchingIssue).toBeTruthy();
  });
});
