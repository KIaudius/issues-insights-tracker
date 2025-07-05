<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { login, isAuthenticated, isLoading, authError } from '$lib/stores/auth';
  
  // Form state
  let username = '';
  let password = '';
  let rememberMe = false;
  let errors = { username: '', password: '' };
  
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
    errors = { username: '', password: '' };
    
    if (!username.trim()) {
      errors.username = 'Username is required';
      isValid = false;
    }
    
    if (!password.trim()) {
      errors.password = 'Password is required';
      isValid = false;
    }
    
    return isValid;
  }
  
  // Handle login
  async function handleLogin() {
    if (!validateForm()) return;
    
    try {
      await login(username, password);
      // Redirect will happen automatically via the onMount subscription
    } catch (error) {
      console.error('Login failed:', error);
      // Error is already handled in the auth store
    }
  }
</script>

<svelte:head>
  <title>Login | Issues & Insights</title>
</svelte:head>

<div class="login-page">
  <div class="login-container">
    <div class="login-header">
      <div class="logo">
        <i class="fas fa-bug"></i>
        <span>Issues & Insights</span>
      </div>
      <h1>Welcome Back</h1>
      <p>Sign in to your account to continue</p>
    </div>
    
    <form class="login-form" on:submit|preventDefault={handleLogin}>
      {#if $authError}
        <div class="auth-error">
          <i class="fas fa-exclamation-triangle"></i>
          <span>{$authError}</span>
        </div>
      {/if}
      
      <div class="form-group">
        <label for="username">Username</label>
        <div class="input-with-icon">
          <i class="fas fa-user"></i>
          <input 
            type="text" 
            id="username" 
            bind:value={username} 
            class={errors.username ? 'error' : ''}
            placeholder="Enter your username"
            autocomplete="username"
          />
        </div>
        {#if errors.username}
          <div class="error-message">{errors.username}</div>
        {/if}
      </div>
      
      <div class="form-group">
        <label for="password">Password</label>
        <div class="input-with-icon">
          <i class="fas fa-lock"></i>
          <input 
            type="password" 
            id="password" 
            bind:value={password} 
            class={errors.password ? 'error' : ''}
            placeholder="Enter your password"
            autocomplete="current-password"
          />
        </div>
        {#if errors.password}
          <div class="error-message">{errors.password}</div>
        {/if}
      </div>
      
      <div class="form-options">
        <label class="checkbox-container">
          <input type="checkbox" bind:checked={rememberMe} />
          <span class="checkmark"></span>
          <span>Remember me</span>
        </label>
        
        <a href="/forgot-password" class="forgot-password">Forgot password?</a>
      </div>
      
      <button 
        type="submit" 
        class="login-button" 
        disabled={$isLoading}
      >
        {#if $isLoading}
          <div class="spinner-small"></div>
          <span>Signing in...</span>
        {:else}
          <span>Sign In</span>
        {/if}
      </button>
      
      <div class="register-link">
        <span>Don't have an account?</span>
        <a href="/register">Sign up</a>
      </div>
    </form>
  </div>
</div>

<style>
  .login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
    background-color: var(--background-secondary);
  }
  
  .login-container {
    width: 100%;
    max-width: 400px;
    background-color: var(--background-color);
    border-radius: 0.5rem;
    box-shadow: var(--card-shadow);
    overflow: hidden;
  }
  
  .login-header {
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
  
  .login-header h1 {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
  }
  
  .login-header p {
    margin: 0;
    opacity: 0.8;
  }
  
  .login-form {
    padding: 2rem;
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
  
  .input-with-icon input {
    width: 100%;
    padding: 0.75rem 1rem 0.75rem 2.5rem;
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: 1rem;
    transition: border-color 0.2s;
  }
  
  .input-with-icon input:focus {
    border-color: var(--accent-color);
    outline: none;
  }
  
  .input-with-icon input.error {
    border-color: var(--error-color);
  }
  
  .error-message {
    color: var(--error-color);
    font-size: 0.875rem;
    margin-top: 0.5rem;
  }
  
  .form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  
  .checkbox-container {
    display: flex;
    align-items: center;
    position: relative;
    padding-left: 1.75rem;
    cursor: pointer;
    font-size: 0.875rem;
    user-select: none;
  }
  
  .checkbox-container input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
  }
  
  .checkmark {
    position: absolute;
    top: 0;
    left: 0;
    height: 1rem;
    width: 1rem;
    background-color: var(--background-color);
    border: 1px solid var(--border-color);
    border-radius: 0.25rem;
  }
  
  .checkbox-container:hover input ~ .checkmark {
    background-color: var(--hover-bg);
  }
  
  .checkbox-container input:checked ~ .checkmark {
    background-color: var(--accent-color);
    border-color: var(--accent-color);
  }
  
  .checkmark:after {
    content: "";
    position: absolute;
    display: none;
  }
  
  .checkbox-container input:checked ~ .checkmark:after {
    display: block;
  }
  
  .checkbox-container .checkmark:after {
    left: 0.3rem;
    top: 0.1rem;
    width: 0.25rem;
    height: 0.5rem;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
  }
  
  .forgot-password {
    font-size: 0.875rem;
    color: var(--accent-color);
    text-decoration: none;
  }
  
  .forgot-password:hover {
    text-decoration: underline;
  }
  
  .login-button {
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
  }
  
  .login-button:hover:not(:disabled) {
    background-color: var(--accent-hover);
  }
  
  .login-button:disabled {
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
  
  .register-link {
    margin-top: 1.5rem;
    text-align: center;
    font-size: 0.875rem;
  }
  
  .register-link a {
    color: var(--accent-color);
    font-weight: 500;
    text-decoration: none;
    margin-left: 0.25rem;
  }
  
  .register-link a:hover {
    text-decoration: underline;
  }
</style>
