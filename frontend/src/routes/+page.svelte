<script>
  import { onMount } from 'svelte';
  
  // Stats data (will be fetched from API)
  let stats = {
    totalIssues: 0,
    openIssues: 0,
    resolvedIssues: 0,
    averageResolutionTime: 0,
    issuesByStatus: [],
    issuesBySeverity: [],
    recentActivity: []
  };
  
  let loading = true;
  let error = null;
  
  onMount(async () => {
    try {
      // In a real implementation, this would fetch from the API
      // const response = await fetch('/api/v1/stats/dashboard');
      // stats = await response.json();
      
      // For now, we'll use mock data
      setTimeout(() => {
        stats = {
          totalIssues: 124,
          openIssues: 42,
          resolvedIssues: 82,
          averageResolutionTime: 3.5,
          issuesByStatus: [
            { status: 'OPEN', count: 42 },
            { status: 'TRIAGED', count: 18 },
            { status: 'IN_PROGRESS', count: 24 },
            { status: 'DONE', count: 40 }
          ],
          issuesBySeverity: [
            { severity: 'LOW', count: 30 },
            { severity: 'MEDIUM', count: 52 },
            { severity: 'HIGH', count: 32 },
            { severity: 'CRITICAL', count: 10 }
          ],
          recentActivity: [
            { 
              type: 'ISSUE_CREATED', 
              id: 124, 
              title: 'API returns 500 error when filtering by date', 
              user: 'John Doe',
              timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString() 
            },
            { 
              type: 'ISSUE_UPDATED', 
              id: 120, 
              title: 'Login page not responsive on mobile', 
              user: 'Jane Smith',
              timestamp: new Date(Date.now() - 1000 * 60 * 120).toISOString() 
            },
            { 
              type: 'COMMENT_ADDED', 
              id: 118, 
              title: 'Dashboard chart colors need more contrast', 
              user: 'Alex Johnson',
              timestamp: new Date(Date.now() - 1000 * 60 * 180).toISOString() 
            },
            { 
              type: 'ISSUE_CLOSED', 
              id: 115, 
              title: 'Typo in welcome email', 
              user: 'Sarah Williams',
              timestamp: new Date(Date.now() - 1000 * 60 * 240).toISOString() 
            },
          ]
        };
        loading = false;
      }, 500);
    } catch (e) {
      console.error('Error fetching dashboard stats:', e);
      error = 'Failed to load dashboard data. Please try again later.';
      loading = false;
    }
  });
  
  // Format time ago
  function timeAgo(dateString) {
    const date = new Date(dateString);
    const seconds = Math.floor((new Date() - date) / 1000);
    
    let interval = seconds / 31536000;
    if (interval > 1) return Math.floor(interval) + ' years ago';
    
    interval = seconds / 2592000;
    if (interval > 1) return Math.floor(interval) + ' months ago';
    
    interval = seconds / 86400;
    if (interval > 1) return Math.floor(interval) + ' days ago';
    
    interval = seconds / 3600;
    if (interval > 1) return Math.floor(interval) + ' hours ago';
    
    interval = seconds / 60;
    if (interval > 1) return Math.floor(interval) + ' minutes ago';
    
    return Math.floor(seconds) + ' seconds ago';
  }
  
  // Get activity icon
  function getActivityIcon(type) {
    switch (type) {
      case 'ISSUE_CREATED': return 'plus-circle';
      case 'ISSUE_UPDATED': return 'edit';
      case 'ISSUE_CLOSED': return 'check-circle';
      case 'COMMENT_ADDED': return 'comment';
      default: return 'circle';
    }
  }
  
  // Get activity color
  function getActivityColor(type) {
    switch (type) {
      case 'ISSUE_CREATED': return 'text-blue-500';
      case 'ISSUE_UPDATED': return 'text-amber-500';
      case 'ISSUE_CLOSED': return 'text-green-500';
      case 'COMMENT_ADDED': return 'text-purple-500';
      default: return 'text-gray-500';
    }
  }
</script>

<svelte:head>
  <title>Dashboard | Issues & Insights</title>
</svelte:head>

<div class="dashboard">
  <h1 class="page-title">Dashboard</h1>
  
  {#if loading}
    <div class="loading-state">
      <div class="spinner"></div>
      <p>Loading dashboard data...</p>
    </div>
  {:else if error}
    <div class="error-state">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{error}</p>
      <button class="btn btn-primary">Retry</button>
    </div>
  {:else}
    <div class="stats-overview">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-bug"></i>
        </div>
        <div class="stat-content">
          <h3>Total Issues</h3>
          <p class="stat-value">{stats.totalIssues}</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-exclamation-circle"></i>
        </div>
        <div class="stat-content">
          <h3>Open Issues</h3>
          <p class="stat-value">{stats.openIssues}</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-check-circle"></i>
        </div>
        <div class="stat-content">
          <h3>Resolved Issues</h3>
          <p class="stat-value">{stats.resolvedIssues}</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-clock"></i>
        </div>
        <div class="stat-content">
          <h3>Avg. Resolution Time</h3>
          <p class="stat-value">{stats.averageResolutionTime} days</p>
        </div>
      </div>
    </div>
    
    <div class="charts-container">
      <div class="chart-card">
        <h3>Issues by Status</h3>
        <div class="chart-placeholder">
          <!-- In a real implementation, we would use Chart.js or similar -->
          <div class="chart-bars">
            {#each stats.issuesByStatus as item}
              <div class="chart-bar-item">
                <div class="chart-bar-label">{item.status}</div>
                <div class="chart-bar" style="height: {(item.count / stats.totalIssues) * 100}%">
                  <span class="chart-bar-value">{item.count}</span>
                </div>
              </div>
            {/each}
          </div>
        </div>
      </div>
      
      <div class="chart-card">
        <h3>Issues by Severity</h3>
        <div class="chart-placeholder">
          <!-- In a real implementation, we would use Chart.js or similar -->
          <div class="chart-bars">
            {#each stats.issuesBySeverity as item}
              <div class="chart-bar-item">
                <div class="chart-bar-label">{item.severity}</div>
                <div class="chart-bar" style="height: {(item.count / stats.totalIssues) * 100}%">
                  <span class="chart-bar-value">{item.count}</span>
                </div>
              </div>
            {/each}
          </div>
        </div>
      </div>
    </div>
    
    <div class="recent-activity">
      <h3>Recent Activity</h3>
      <div class="activity-list">
        {#each stats.recentActivity as activity}
          <div class="activity-item">
            <div class="activity-icon {getActivityColor(activity.type)}">
              <i class="fas fa-{getActivityIcon(activity.type)}"></i>
            </div>
            <div class="activity-content">
              <p class="activity-title">
                <span class="activity-user">{activity.user}</span> 
                {activity.type === 'ISSUE_CREATED' ? 'created' : 
                 activity.type === 'ISSUE_UPDATED' ? 'updated' : 
                 activity.type === 'ISSUE_CLOSED' ? 'closed' : 
                 activity.type === 'COMMENT_ADDED' ? 'commented on' : 'modified'} 
                issue <a href="/issues/{activity.id}" class="activity-link">#{activity.id}: {activity.title}</a>
              </p>
              <p class="activity-time">{timeAgo(activity.timestamp)}</p>
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .dashboard {
    padding-bottom: 2rem;
  }
  
  .page-title {
    font-size: 1.875rem;
    font-weight: 700;
    margin-bottom: 2rem;
  }
  
  .loading-state, .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 0;
    gap: 1rem;
    color: var(--text-muted);
  }
  
  .spinner {
    width: 3rem;
    height: 3rem;
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: var(--accent-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .error-state i {
    font-size: 3rem;
    color: var(--error-color);
  }
  
  .stats-overview {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .stat-card {
    background-color: var(--background-color);
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    padding: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: var(--card-shadow);
  }
  
  .stat-icon {
    width: 3rem;
    height: 3rem;
    border-radius: 0.5rem;
    background-color: var(--accent-color);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
  }
  
  .stat-content h3 {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-muted);
    margin: 0 0 0.25rem 0;
  }
  
  .stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
  }
  
  .charts-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  @media (max-width: 768px) {
    .charts-container {
      grid-template-columns: 1fr;
    }
  }
  
  .chart-card {
    background-color: var(--background-color);
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    padding: 1.5rem;
    box-shadow: var(--card-shadow);
  }
  
  .chart-card h3 {
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 1.5rem 0;
  }
  
  .chart-placeholder {
    height: 250px;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    padding: 1rem 0;
  }
  
  .chart-bars {
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
    width: 100%;
    height: 100%;
  }
  
  .chart-bar-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: 100%;
  }
  
  .chart-bar {
    width: 2rem;
    background-color: var(--accent-color);
    border-radius: 4px 4px 0 0;
    position: relative;
    min-height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .chart-bar-value {
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
  }
  
  .chart-bar-label {
    margin-top: 0.5rem;
    font-size: 0.75rem;
    color: var(--text-muted);
  }
  
  .recent-activity {
    background-color: var(--background-color);
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    padding: 1.5rem;
    box-shadow: var(--card-shadow);
  }
  
  .recent-activity h3 {
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 1.5rem 0;
  }
  
  .activity-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .activity-item {
    display: flex;
    gap: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-color);
  }
  
  .activity-item:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }
  
  .activity-icon {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 9999px;
    background-color: var(--background-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .activity-content {
    flex: 1;
  }
  
  .activity-title {
    margin: 0 0 0.25rem 0;
    line-height: 1.5;
  }
  
  .activity-user {
    font-weight: 600;
  }
  
  .activity-link {
    font-weight: 500;
  }
  
  .activity-time {
    margin: 0;
    font-size: 0.875rem;
    color: var(--text-muted);
  }
  
  /* Utility classes for activity icons */
  .text-blue-500 {
    color: #3b82f6;
  }
  
  .text-amber-500 {
    color: #f59e0b;
  }
  
  .text-green-500 {
    color: #10b981;
  }
  
  .text-purple-500 {
    color: #8b5cf6;
  }
  
  .text-gray-500 {
    color: #6b7280;
  }
</style>
