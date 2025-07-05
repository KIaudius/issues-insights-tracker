<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { register, isAuthenticated, isLoading, authError } from '$lib/stores/auth';
  
  // Form state
  let username = '';
  let email = '';
  let password = '';
  let confirmPassword = '';
  let role = 'REPORTER'; // Default role
  let errors = { username: '', email: '', password: '', confirmPassword: '' };
  let registrationSuccess = false;
  
  // Redirect if already authenticated
  onMount(() => {
    const unsubscribe = isAuthenticated.subscribe(value => {
      if (value) {
        goto('/');
      }
    });
    
    return () => {
      unsubscribe();
    };
  });
  
  // Validate form
  function validateForm() {
    let isValid = true;
    errors = { username: '', email: '', password: '', confirmPassword: '' };
    
    // Username validation
    if (!username.trim()) {
      errors.username = 'Username is required';
      isValid = false;
    } else if (username.length < 3) {
      errors.username = 'Username must be at least 3 characters';
      isValid = false;
    }
    
    // Email validation
    if (!email.trim()) {
      errors.email = 'Email is required';
      isValid = false;
    } else if (!isValidEmail(email)) {
      errors.email = 'Please enter a valid email address';
      isValid = false;
    }
    
    // Password validation
    if (!password) {
      errors.password = 'Password is required';
      isValid = false;
    } else if (password.length < 8) {
      errors.password = 'Password must be at least 8 characters';
      isValid = false;
    }
    
    // Confirm password validation
    if (!confirmPassword) {
      errors.confirmPassword = 'Please confirm your password';
      isValid = false;
    } else if (password !== confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
      isValid = false;
    }
    
    return isValid;
  }
  
  // Email validation helper
  function isValidEmail(email) {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(String(email).toLowerCase());
  }
  
  // Handle registration
  async function handleRegister() {
    if (!validateForm()) return;
    
    try {
      const userData = {
        username,
        email,
        password,
        role
      };
      
      await register(userData);
      registrationSuccess = true;
      
      // Redirect to login page after a short delay
      setTimeout(() => {
        goto('/login');
      }, 3000);
    } catch (error) {
      console.error('Registration failed:', error);
      // Error is already handled in the auth store
    }
  }
</script>

<svelte:head>
  <title>Register | Issues & Insights</title>
</svelte:head>

<div class="register-page">
  <div class="register-container">
    <div class="register-header">
      <div class="logo">
        <i class="fas fa-bug"></i>
        <span>Issues & Insights</span>
      </div>
      <h1>Create an Account</h1>
      <p>Sign up to start tracking issues</p>
    </div>
    
    {#if registrationSuccess}
      <div class="success-message">
        <i class="fas fa-check-circle"></i>
        <h2>Registration Successful!</h2>
        <p>Your account has been created. Redirecting to login page...</p>
      </div>
    {:else}
      <form class="register-form" on:submit|preventDefault={handleRegister}>
        {#if $authError}
          <div class="auth-error">
            <i class="fas fa-exclamation-triangle"></i>
            <span>{$authError}</span>
          </div>
        {/if}
        
        <div class="form-group">
          <label for="username">Username <span class="required">*</span></label>
          <div class="input-with-icon">
            <i class="fas fa-user"></i>
            <input 
              type="text" 
              id="username" 
              bind:value={username} 
              class={errors.username ? 'error' : ''}
              placeholder="Choose a username"
              autocomplete="username"
            />
          </div>
          {#if errors.username}
            <div class="error-message">{errors.username}</div>
          {/if}
        </div>
        
        <div class="form-group">
          <label for="email">Email <span class="required">*</span></label>
          <div class="input-with-icon">
            <i class="fas fa-envelope"></i>
            <input 
              type="email" 
              id="email" 
              bind:value={email} 
              class={errors.email ? 'error' : ''}
              placeholder="Enter your email"
              autocomplete="email"
            />
          </div>
          {#if errors.email}
            <div class="error-message">{errors.email}</div>
          {/if}
        </div>
        
        <div class="form-group">
          <label for="password">Password <span class="required">*</span></label>
          <div class="input-with-icon">
            <i class="fas fa-lock"></i>
            <input 
              type="password" 
              id="password" 
              bind:value={password} 
              class={errors.password ? 'error' : ''}
              placeholder="Create a password"
              autocomplete="new-password"
            />
          </div>
          {#if errors.password}
            <div class="error-message">{errors.password}</div>
          {/if}
          <div class="password-requirements">
            Password must be at least 8 characters
          </div>
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">Confirm Password <span class="required">*</span></label>
          <div class="input-with-icon">
            <i class="fas fa-lock"></i>
            <input 
              type="password" 
              id="confirmPassword" 
              bind:value={confirmPassword} 
              class={errors.confirmPassword ? 'error' : ''}
              placeholder="Confirm your password"
              autocomplete="new-password"
            />
          </div>
          {#if errors.confirmPassword}
            <div class="error-message">{errors.confirmPassword}</div>
          {/if}
        </div>
        
        <div class="form-group">
          <label for="role">Role</label>
          <div class="input-with-icon">
            <i class="fas fa-user-tag"></i>
            <select id="role" bind:value={role}>
              <option value="REPORTER">Reporter</option>
              <option value="MAINTAINER">Maintainer</option>
              <option value="ADMIN">Admin</option>
            </select>
          </div>
          <div class="role-info">
            <strong>Note:</strong> Role selection is for demo purposes. In a real application, role assignment would be controlled by administrators.
          </div>
        </div>
        
        <button 
          type="submit" 
          class="register-button" 
          disabled={$isLoading}
        >
          {#if $isLoading}
            <div class="spinner-small"></div>
            <span>Creating Account...</span>
          {:else}
            <span>Create Account</span>
          {/if}
        </button>
        
        <div class="login-link">
          <span>Already have an account?</span>
          <a href="/login">Sign in</a>
        </div>
      </form>
    {/if}
  </div>
</div>

<style>
  .register-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
    background-color: var(--background-secondary);
  }
  
  .register-container {
    width: 100%;
    max-width: 500px;
    background-color: var(--background-color);
    border-radius: 0.5rem;
    box-shadow: var(--card-shadow);
    overflow: hidden;
    margin: 2rem 0;
  }
  
  .register-header {
    padding: 2rem;
    text-align: center;
    background-color: var(--accent-color);
    color: white;
  }
  
  .logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    font-size: 1.25rem;
    font-weight: 700;
  }
  
  .register-header h1 {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
  }
  
  .register-header p {
    margin: 0;
    opacity: 0.8;
  }
  
  .register-form {
    padding: 2rem;
  }
  
  .success-message {
    padding: 3rem 2rem;
    text-align: center;
  }
  
  .success-message i {
    font-size: 3rem;
    color: var(--success-color);
    margin-bottom: 1rem;
  }
  
  .success-message h2 {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 1rem 0;
    color: var(--success-color);
  }
  
  .success-message p {
    margin: 0;
    color: var(--text-muted);
  }
  
  .auth-error {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background-color: var(--error-bg);
    border-radius: 0.375rem;
    color: var(--error-color);
    margin-bottom: 1.5rem;
    font-size: 0.875rem;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }
  
  .required {
    color: var(--error-color);
  }
  
  .input-with-icon {
    position: relative;
  }
  
  .input-with-icon i {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
  }
  
  .input-with-icon input,
  .input-with-icon select {
    width: 100%;
    padding: 0.75rem 1rem 0.75rem 2.5rem;
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: 1rem;
    transition: border-color 0.2s;
  }
  
  .input-with-icon input:focus,
  .input-with-icon select:focus {
    border-color: var(--accent-color);
    outline: none;
  }
  
  .input-with-icon input.error,
  .input-with-icon select.error {
    border-color: var(--error-color);
  }
  
  .error-message {
    color: var(--error-color);
    font-size: 0.875rem;
    margin-top: 0.5rem;
  }
  
  .password-requirements,
  .role-info {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
  }
  
  .register-button {
    width: 100%;
    padding: 0.75rem;
    background-color: var(--accent-color);
    color: white;
    border: none;
    border-radius: 0.375rem;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
    transition: background-color 0.2s;
    margin-top: 1rem;
  }
  
  .register-button:hover:not(:disabled) {
    background-color: var(--accent-hover);
  }
  
  .register-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
  
  .spinner-small {
    width: 1rem;
    height: 1rem;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-left-color: white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .login-link {
    margin-top: 1.5rem;
    text-align: center;
    font-size: 0.875rem;
  }
  
  .login-link a {
    color: var(--accent-color);
    font-weight: 500;
    text-decoration: none;
    margin-left: 0.25rem;
  }
  
  .login-link a:hover {
    text-decoration: underline;
  }
</style>
