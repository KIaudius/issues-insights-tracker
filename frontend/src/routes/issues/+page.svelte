<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  
  // Issue data (will be fetched from API)
  let issues = [];
  let totalIssues = 0;
  let loading = true;
  let error = null;
  
  // Pagination
  let currentPage = 1;
  let pageSize = 10;
  let totalPages = 0;
  
  // Filters
  let statusFilter = '';
  let severityFilter = '';
  let searchQuery = '';
  
  // Sort
  let sortField = 'created_at';
  let sortDirection = 'desc';
  
  // Mock user data (will come from auth store)
  const user = { role: 'ADMIN' };
  
  onMount(async () => {
    await loadIssues();
  });
  
  async function loadIssues() {
    loading = true;
    error = null;
    
    try {
      // In a real implementation, this would fetch from the API
      // const response = await fetch(`/api/v1/issues/?page=${currentPage}&limit=${pageSize}&status=${statusFilter}&severity=${severityFilter}&search=${searchQuery}&sort=${sortField}&direction=${sortDirection}`);
      // const data = await response.json();
      // issues = data.data;
      // totalIssues = data.total;
      // totalPages = Math.ceil(totalIssues / pageSize);
      
      // For now, we'll use mock data
      setTimeout(() => {
        const mockIssues = [
          {
            id: 124,
            title: 'API returns 500 error when filtering by date',
            status: 'OPEN',
            severity: 'HIGH',
            reporter: { id: 1, username: 'john.doe' },
            created_at: '2025-07-01T10:30:00Z',
            updated_at: '2025-07-01T10:30:00Z',
            comment_count: 3
          },
          {
            id: 123,
            title: 'Dashboard chart colors need more contrast',
            status: 'TRIAGED',
            severity: 'MEDIUM',
            reporter: { id: 2, username: 'jane.smith' },
            created_at: '2025-06-30T14:20:00Z',
            updated_at: '2025-07-01T09:15:00Z',
            comment_count: 5
          },
          {
            id: 122,
            title: 'Login page not responsive on mobile',
            status: 'IN_PROGRESS',
            severity: 'HIGH',
            reporter: { id: 3, username: 'alex.johnson' },
            created_at: '2025-06-29T11:45:00Z',
            updated_at: '2025-07-01T08:30:00Z',
            comment_count: 7
          },
          {
            id: 121,
            title: 'Typo in welcome email',
            status: 'DONE',
            severity: 'LOW',
            reporter: { id: 4, username: 'sarah.williams' },
            created_at: '2025-06-28T09:10:00Z',
            updated_at: '2025-06-30T16:20:00Z',
            comment_count: 2
          },
          {
            id: 120,
            title: 'Add dark mode support',
            status: 'OPEN',
            severity: 'MEDIUM',
            reporter: { id: 1, username: 'john.doe' },
            created_at: '2025-06-27T15:30:00Z',
            updated_at: '2025-06-27T15:30:00Z',
            comment_count: 4
          },
        ];
        
        // Apply filters if any
        let filteredIssues = [...mockIssues];
        
        if (statusFilter) {
          filteredIssues = filteredIssues.filter(issue => issue.status === statusFilter);
        }
        
        if (severityFilter) {
          filteredIssues = filteredIssues.filter(issue => issue.severity === severityFilter);
        }
        
        if (searchQuery) {
          const query = searchQuery.toLowerCase();
          filteredIssues = filteredIssues.filter(issue => 
            issue.title.toLowerCase().includes(query) || 
            issue.reporter.username.toLowerCase().includes(query)
          );
        }
        
        // Apply sorting
        filteredIssues.sort((a, b) => {
          const aValue = a[sortField];
          const bValue = b[sortField];
          
          if (sortDirection === 'asc') {
            return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
          } else {
            return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
          }
        });
        
        issues = filteredIssues;
        totalIssues = filteredIssues.length;
        totalPages = Math.ceil(totalIssues / pageSize);
        loading = false;
      }, 500);
    } catch (e) {
      console.error('Error fetching issues:', e);
      error = 'Failed to load issues. Please try again later.';
      loading = false;
    }
  }
  
  // Handle page change
  function changePage(page) {
    currentPage = page;
    loadIssues();
  }
  
  // Handle sort change
  function changeSort(field) {
    if (sortField === field) {
      sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      sortField = field;
      sortDirection = 'desc';
    }
    loadIssues();
  }
  
  // Handle filter change
  function applyFilters() {
    currentPage = 1;
    loadIssues();
  }
  
  // Reset filters
  function resetFilters() {
    statusFilter = '';
    severityFilter = '';
    searchQuery = '';
    currentPage = 1;
    loadIssues();
  }
  
  // Format date
  function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
  
  // Get status badge class
  function getStatusBadgeClass(status) {
    switch (status) {
      case 'OPEN': return 'badge-info';
      case 'TRIAGED': return 'badge-warning';
      case 'IN_PROGRESS': return 'badge-primary';
      case 'DONE': return 'badge-success';
      default: return 'badge-secondary';
    }
  }
  
  // Get severity badge class
  function getSeverityBadgeClass(severity) {
    switch (severity) {
      case 'LOW': return 'badge-success';
      case 'MEDIUM': return 'badge-info';
      case 'HIGH': return 'badge-warning';
      case 'CRITICAL': return 'badge-error';
      default: return 'badge-secondary';
    }
  }
</script>

<svelte:head>
  <title>Issues | Issues & Insights</title>
</svelte:head>

<div class="issues-page">
  <div class="page-header">
    <h1 class="page-title">Issues</h1>
    <a href="/issues/new" class="btn btn-primary">
      <i class="fas fa-plus"></i>
      <span>New Issue</span>
    </a>
  </div>
  
  <div class="filters-bar">
    <div class="search-box">
      <i class="fas fa-search search-icon"></i>
      <input 
        type="text" 
        bind:value={searchQuery} 
        placeholder="Search issues..."
        on:keyup={event => event.key === 'Enter' && applyFilters()}
      />
    </div>
    
    <div class="filters">
      <select bind:value={statusFilter} on:change={applyFilters}>
        <option value="">All Statuses</option>
        <option value="OPEN">Open</option>
        <option value="TRIAGED">Triaged</option>
        <option value="IN_PROGRESS">In Progress</option>
        <option value="DONE">Done</option>
      </select>
      
      <select bind:value={severityFilter} on:change={applyFilters}>
        <option value="">All Severities</option>
        <option value="LOW">Low</option>
        <option value="MEDIUM">Medium</option>
        <option value="HIGH">High</option>
        <option value="CRITICAL">Critical</option>
      </select>
      
      <button class="btn btn-secondary" on:click={resetFilters}>
        <i class="fas fa-times"></i>
        <span>Reset</span>
      </button>
    </div>
  </div>
  
  {#if loading}
    <div class="loading-state">
      <div class="spinner"></div>
      <p>Loading issues...</p>
    </div>
  {:else if error}
    <div class="error-state">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{error}</p>
      <button class="btn btn-primary" on:click={loadIssues}>Retry</button>
    </div>
  {:else if issues.length === 0}
    <div class="empty-state">
      <i class="fas fa-search"></i>
      <p>No issues found matching your criteria.</p>
      {#if statusFilter || severityFilter || searchQuery}
        <button class="btn btn-secondary" on:click={resetFilters}>Clear Filters</button>
      {:else}
        <a href="/issues/new" class="btn btn-primary">Create First Issue</a>
      {/if}
    </div>
  {:else}
    <div class="issues-table-container">
      <table class="issues-table">
        <thead>
          <tr>
            <th on:click={() => changeSort('id')} class="sortable">
              ID
              {#if sortField === 'id'}
                <i class="fas fa-sort-{sortDirection === 'asc' ? 'up' : 'down'}"></i>
              {/if}
            </th>
            <th on:click={() => changeSort('title')} class="sortable">
              Title
              {#if sortField === 'title'}
                <i class="fas fa-sort-{sortDirection === 'asc' ? 'up' : 'down'}"></i>
              {/if}
            </th>
            <th on:click={() => changeSort('status')} class="sortable">
              Status
              {#if sortField === 'status'}
                <i class="fas fa-sort-{sortDirection === 'asc' ? 'up' : 'down'}"></i>
              {/if}
            </th>
            <th on:click={() => changeSort('severity')} class="sortable">
              Severity
              {#if sortField === 'severity'}
                <i class="fas fa-sort-{sortDirection === 'asc' ? 'up' : 'down'}"></i>
              {/if}
            </th>
            <th on:click={() => changeSort('reporter.username')} class="sortable">
              Reporter
              {#if sortField === 'reporter.username'}
                <i class="fas fa-sort-{sortDirection === 'asc' ? 'up' : 'down'}"></i>
              {/if}
            </th>
            <th on:click={() => changeSort('created_at')} class="sortable">
              Created
              {#if sortField === 'created_at'}
                <i class="fas fa-sort-{sortDirection === 'asc' ? 'up' : 'down'}"></i>
              {/if}
            </th>
            <th>Comments</th>
          </tr>
        </thead>
        <tbody>
          {#each issues as issue}
            <tr class="issue-row" on:click={() => goto(`/issues/${issue.id}`)}>
              <td>#{issue.id}</td>
              <td class="issue-title">{issue.title}</td>
              <td>
                <span class="badge {getStatusBadgeClass(issue.status)}">{issue.status}</span>
              </td>
              <td>
                <span class="badge {getSeverityBadgeClass(issue.severity)}">{issue.severity}</span>
              </td>
              <td>{issue.reporter.username}</td>
              <td>{formatDate(issue.created_at)}</td>
              <td>
                <span class="comment-count">
                  <i class="fas fa-comment"></i>
                  {issue.comment_count}
                </span>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
    
    {#if totalPages > 1}
      <div class="pagination">
        <button 
          class="pagination-btn" 
          disabled={currentPage === 1}
          on:click={() => changePage(currentPage - 1)}
        >
          <i class="fas fa-chevron-left"></i>
        </button>
        
        {#each Array(totalPages) as _, i}
          <button 
            class="pagination-btn {currentPage === i + 1 ? 'active' : ''}"
            on:click={() => changePage(i + 1)}
          >
            {i + 1}
          </button>
        {/each}
        
        <button 
          class="pagination-btn" 
          disabled={currentPage === totalPages}
          on:click={() => changePage(currentPage + 1)}
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    {/if}
  {/if}
</div>

<style>
  .issues-page {
    padding-bottom: 2rem;
  }
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }
  
  .page-title {
    font-size: 1.875rem;
    font-weight: 700;
    margin: 0;
  }
  
  .filters-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.5rem;
    align-items: center;
  }
  
  .search-box {
    position: relative;
    flex: 1;
    min-width: 200px;
  }
  
  .search-icon {
    position: absolute;
    left: 0.75rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
  }
  
  .search-box input {
    width: 100%;
    padding: 0.5rem 1rem 0.5rem 2.5rem;
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: 0.875rem;
  }
  
  .filters {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  
  .filters select {
    padding: 0.5rem;
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: 0.875rem;
    min-width: 150px;
  }
  
  .loading-state, .error-state, .empty-state {
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
  
  .error-state i, .empty-state i {
    font-size: 3rem;
    color: var(--text-muted);
  }
  
  .issues-table-container {
    overflow-x: auto;
    margin-bottom: 1.5rem;
  }
  
  .issues-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
  }
  
  .issues-table th {
    text-align: left;
    padding: 0.75rem 1rem;
    background-color: var(--background-secondary);
    font-weight: 600;
    border-bottom: 1px solid var(--border-color);
  }
  
  .issues-table th.sortable {
    cursor: pointer;
    user-select: none;
  }
  
  .issues-table th.sortable:hover {
    background-color: var(--hover-bg);
  }
  
  .issues-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border-color);
  }
  
  .issue-row {
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .issue-row:hover {
    background-color: var(--hover-bg);
  }
  
  .issue-title {
    font-weight: 500;
    max-width: 300px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.5rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
    white-space: nowrap;
  }
  
  .comment-count {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    color: var(--text-muted);
  }
  
  .pagination {
    display: flex;
    justify-content: center;
    gap: 0.25rem;
    margin-top: 1.5rem;
  }
  
  .pagination-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    border-radius: 0.375rem;
    border: 1px solid var(--border-color);
    background-color: var(--background-color);
    color: var(--text-color);
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .pagination-btn:hover:not(:disabled) {
    background-color: var(--hover-bg);
  }
  
  .pagination-btn.active {
    background-color: var(--accent-color);
    border-color: var(--accent-color);
    color: white;
  }
  
  .pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  @media (max-width: 768px) {
    .filters-bar {
      flex-direction: column;
      align-items: stretch;
    }
    
    .search-box {
      width: 100%;
    }
    
    .filters {
      width: 100%;
    }
  }
</style>
