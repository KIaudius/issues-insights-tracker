<script>
  import '../app.css';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import ThemeToggle from '$lib/components/ThemeToggle.svelte';
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  
  // Auth store will be implemented later
  // import { auth } from '$lib/stores/auth';
  
  let isMenuOpen = false;
  
  // Toggle mobile menu
  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
  }
  
  // Close menu when route changes
  $: if (browser && $page.url.pathname) {
    isMenuOpen = false;
  }
  
  // Navigation items
  const navItems = [
    { href: '/', label: 'Dashboard', icon: 'chart-line', requiresAuth: true },
    { href: '/issues', label: 'Issues', icon: 'bug', requiresAuth: true },
    { href: '/users', label: 'Users', icon: 'users', requiresAuth: true, adminOnly: true },
  ];
  
  // For now, we'll simulate authentication until we implement the auth store
  let isAuthenticated = true;
  let user = { role: 'ADMIN' };
  
  function logout() {
    // Will be implemented with auth store
    // auth.logout();
    goto('/login');
  }
</script>

<div class="app">
  <header class="header">
    <div class="container">
      <div class="header-content">
        <div class="logo-container">
          <a href="/" class="logo">
            <i class="fas fa-lightbulb"></i>
            <span>Issues & Insights</span>
          </a>
        </div>
        
        <div class="header-actions">
          <ThemeToggle />
          
          {#if isAuthenticated}
            <button class="profile-button" aria-label="User menu">
              <span class="avatar">{user.role[0]}</span>
            </button>
          {:else}
            <a href="/login" class="btn btn-primary">Login</a>
          {/if}
          
          <button class="menu-button" on:click={toggleMenu} aria-label="Menu">
            <i class="fas fa-{isMenuOpen ? 'times' : 'bars'}"></i>
          </button>
        </div>
      </div>
    </div>
  </header>
  
  <div class="app-container">
    {#if isAuthenticated}
      <aside class="sidebar {isMenuOpen ? 'open' : ''}">
        <nav>
          <ul>
            {#each navItems as item}
              {#if !item.adminOnly || (user && user.role === 'ADMIN')}
                <li>
                  <a 
                    href={item.href} 
                    class="nav-link {$page.url.pathname === item.href ? 'active' : ''}"
                  >
                    <i class="fas fa-{item.icon}"></i>
                    <span>{item.label}</span>
                  </a>
                </li>
              {/if}
            {/each}
          </ul>
          
          <div class="sidebar-footer">
            <button class="btn btn-secondary logout-btn" on:click={logout}>
              <i class="fas fa-sign-out-alt"></i>
              <span>Logout</span>
            </button>
          </div>
        </nav>
      </aside>
    {/if}
    
    <main class="content {!isAuthenticated ? 'full-width' : ''}">
      <div class="container">
        <slot />
      </div>
    </main>
  </div>
</div>

<style>
  .app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  
  .header {
    background-color: var(--background-color);
    border-bottom: 1px solid var(--border-color);
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: var(--card-shadow);
  }
  
  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 4rem;
  }
  
  .logo-container {
    display: flex;
    align-items: center;
  }
  
  .logo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--accent-color);
    text-decoration: none;
  }
  
  .logo:hover {
    text-decoration: none;
  }
  
  .header-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .profile-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 9999px;
    background-color: var(--accent-color);
    color: white;
    border: none;
    cursor: pointer;
    font-weight: 600;
  }
  
  .menu-button {
    display: none;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 9999px;
    background-color: transparent;
    color: var(--text-color);
    border: none;
    cursor: pointer;
  }
  
  .app-container {
    display: flex;
    flex: 1;
  }
  
  .sidebar {
    width: 16rem;
    background-color: var(--background-color);
    border-right: 1px solid var(--border-color);
    height: calc(100vh - 4rem);
    position: sticky;
    top: 4rem;
    overflow-y: auto;
    transition: transform 0.3s ease;
  }
  
  .sidebar nav {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 1rem 0;
  }
  
  .sidebar ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .nav-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1.5rem;
    color: var(--text-color);
    text-decoration: none;
    transition: background-color 0.2s;
  }
  
  .nav-link:hover {
    background-color: var(--hover-bg);
    text-decoration: none;
  }
  
  .nav-link.active {
    background-color: var(--accent-color);
    color: white;
  }
  
  .sidebar-footer {
    margin-top: auto;
    padding: 1rem 1.5rem;
    border-top: 1px solid var(--border-color);
  }
  
  .logout-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    width: 100%;
  }
  
  .content {
    flex: 1;
    padding: 2rem 0;
  }
  
  .content.full-width {
    padding: 0;
  }
  
  .container {
    width: 100%;
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 1rem;
  }
  
  @media (max-width: 768px) {
    .menu-button {
      display: flex;
    }
    
    .sidebar {
      position: fixed;
      left: 0;
      transform: translateX(-100%);
      z-index: 50;
      box-shadow: var(--card-shadow);
    }
    
    .sidebar.open {
      transform: translateX(0);
    }
  }
</style>
