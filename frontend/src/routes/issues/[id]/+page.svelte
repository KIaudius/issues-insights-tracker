<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import FileAttachment from '$lib/components/FileAttachment.svelte';
  
  // Get issue ID from route params
  const issueId = $page.params.id;
  
  // State
  let issue = null;
  let comments = [];
  let attachments = [];
  let loading = true;
  let error = null;
  let commentText = '';
  let statusUpdateComment = '';
  let showStatusModal = false;
  let selectedStatus = '';
  
  // Mock user data (will come from auth store)
  const user = { role: 'ADMIN' };
  const canUpdateStatus = user.role === 'ADMIN' || user.role === 'MAINTAINER';
  
  onMount(async () => {
    await loadIssue();
  });
  
  async function loadIssue() {
    loading = true;
    error = null;
    
    try {
      // In a real implementation, this would fetch from the API
      // const response = await fetch(`/api/v1/issues/${issueId}`);
      // const data = await response.json();
      // issue = data.data;
      
      // For now, we'll use mock data
      setTimeout(() => {
        issue = {
          id: parseInt(issueId),
          title: 'API returns 500 error when filtering by date',
          description: 'When trying to filter issues by date using the date_from and date_to parameters, the API returns a 500 error. This happens consistently when the date format is YYYY-MM-DD.\n\nSteps to reproduce:\n1. Go to /issues\n2. Set date filter to 2025-06-01 to 2025-07-01\n3. Click Apply Filters\n\nExpected: Issues filtered by date\nActual: 500 Internal Server Error',
          status: 'OPEN',
          severity: 'HIGH',
          reporter: { id: 1, username: 'john.doe', email: 'john.doe@example.com' },
          assignee: null,
          created_at: '2025-07-01T10:30:00Z',
          updated_at: '2025-07-01T10:30:00Z',
        };
        
        comments = [
          {
            id: 1,
            issue_id: parseInt(issueId),
            user: { id: 2, username: 'jane.smith', email: 'jane.smith@example.com' },
            content: 'I can reproduce this issue. Looks like there\'s an issue with the date parsing in the API.',
            created_at: '2025-07-01T11:15:00Z',
            updated_at: '2025-07-01T11:15:00Z'
          },
          {
            id: 2,
            issue_id: parseInt(issueId),
            user: { id: 3, username: 'alex.johnson', email: 'alex.johnson@example.com' },
            content: 'The problem is in the date validation middleware. It\'s not handling the ISO format correctly.',
            created_at: '2025-07-01T14:30:00Z',
            updated_at: '2025-07-01T14:30:00Z'
          },
          {
            id: 3,
            issue_id: parseInt(issueId),
            user: { id: 1, username: 'john.doe', email: 'john.doe@example.com' },
            content: 'Thanks for looking into this. Any ETA on a fix?',
            created_at: '2025-07-02T09:45:00Z',
            updated_at: '2025-07-02T09:45:00Z'
          }
        ];
        
        attachments = [
          {
            id: 1,
            issue_id: parseInt(issueId),
            filename: 'error_screenshot.png',
            content_type: 'image/png',
            size: 256000,
            created_at: '2025-07-01T10:35:00Z',
            user: { id: 1, username: 'john.doe' }
          },
          {
            id: 2,
            issue_id: parseInt(issueId),
            filename: 'api_logs.txt',
            content_type: 'text/plain',
            size: 15000,
            created_at: '2025-07-01T14:40:00Z',
            user: { id: 3, username: 'alex.johnson' }
          }
        ];
        
        loading = false;
      }, 500);
    } catch (e) {
      console.error('Error fetching issue:', e);
      error = 'Failed to load issue. Please try again later.';
      loading = false;
    }
  }
  
  // Add a comment
  async function addComment() {
    if (!commentText.trim()) return;
    
    try {
      // In a real implementation, this would post to the API
      // const response = await fetch(`/api/v1/issues/${issueId}/comments`, {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ content: commentText })
      // });
      // const data = await response.json();
      // comments = [...comments, data.data];
      
      // For now, we'll simulate adding a comment
      const newComment = {
        id: comments.length + 1,
        issue_id: parseInt(issueId),
        user: { id: user.id || 1, username: user.username || 'current.user', email: user.email || 'current.user@example.com' },
        content: commentText,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };
      
      comments = [...comments, newComment];
      commentText = '';
    } catch (e) {
      console.error('Error adding comment:', e);
      alert('Failed to add comment. Please try again.');
    }
  }
  
  // Update issue status
  async function updateStatus() {
    if (!selectedStatus || !statusUpdateComment.trim()) return;
    
    try {
      // In a real implementation, this would post to the API
      // const response = await fetch(`/api/v1/issues/${issueId}/status`, {
      //   method: 'PUT',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ 
      //     status: selectedStatus,
      //     comment: statusUpdateComment 
      //   })
      // });
      // const data = await response.json();
      // issue = data.data;
      
      // For now, we'll simulate updating the status
      issue = { ...issue, status: selectedStatus, updated_at: new Date().toISOString() };
      
      // Add status update comment
      const statusComment = {
        id: comments.length + 1,
        issue_id: parseInt(issueId),
        user: { id: user.id || 1, username: user.username || 'current.user', email: user.email || 'current.user@example.com' },
        content: `**Status changed to ${selectedStatus}**: ${statusUpdateComment}`,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };
      
      comments = [...comments, statusComment];
      statusUpdateComment = '';
      showStatusModal = false;
    } catch (e) {
      console.error('Error updating status:', e);
      alert('Failed to update status. Please try again.');
    }
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
  <title>{issue ? `Issue #${issue.id}: ${issue.title}` : 'Issue Details'} | Issues & Insights</title>
</svelte:head>

<div class="issue-page">
  <div class="page-header">
    <div class="breadcrumbs">
      <a href="/issues" class="breadcrumb-link">
        <i class="fas fa-arrow-left"></i>
        <span>Back to Issues</span>
      </a>
    </div>
  </div>
  
  {#if loading}
    <div class="loading-state">
      <div class="spinner"></div>
      <p>Loading issue details...</p>
    </div>
  {:else if error}
    <div class="error-state">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{error}</p>
      <button class="btn btn-primary" on:click={loadIssue}>Retry</button>
    </div>
  {:else if issue}
    <div class="issue-header">
      <div class="issue-title-container">
        <h1 class="issue-title">#{issue.id}: {issue.title}</h1>
        <div class="issue-badges">
          <span class="badge {getStatusBadgeClass(issue.status)}">{issue.status}</span>
          <span class="badge {getSeverityBadgeClass(issue.severity)}">{issue.severity}</span>
        </div>
      </div>
      
      <div class="issue-meta">
        <div class="meta-item">
          <span class="meta-label">Reported by</span>
          <span class="meta-value">{issue.reporter.username}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Created</span>
          <span class="meta-value">{formatDate(issue.created_at)}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Updated</span>
          <span class="meta-value">{formatDate(issue.updated_at)}</span>
        </div>
        
        {#if canUpdateStatus}
          <button class="btn btn-primary" on:click={() => showStatusModal = true}>
            <i class="fas fa-exchange-alt"></i>
            <span>Update Status</span>
          </button>
        {/if}
      </div>
    </div>
    
    <div class="issue-content">
      <div class="issue-main">
        <div class="issue-description card">
          <h2 class="card-title">Description</h2>
          <div class="markdown-content">
            {#each issue.description.split('\n') as paragraph}
              <p>{paragraph}</p>
            {/each}
          </div>
        </div>
        
        <div class="issue-attachments card">
          <h2 class="card-title">Attachments ({attachments.length})</h2>
          {#if attachments.length === 0}
            <p class="text-muted">No attachments for this issue.</p>
          {:else}
            <div class="attachments-list">
              {#each attachments as attachment}
                <FileAttachment {attachment} showPreview={true} />
              {/each}
            </div>
          {/if}
        </div>
        
        <div class="issue-comments card">
          <h2 class="card-title">Comments ({comments.length})</h2>
          
          <div class="comments-list">
            {#each comments as comment}
              <div class="comment">
                <div class="comment-header">
                  <div class="comment-author">
                    <div class="avatar">{comment.user.username[0]}</div>
                    <span class="username">{comment.user.username}</span>
                  </div>
                  <div class="comment-date">{formatDate(comment.created_at)}</div>
                </div>
                <div class="comment-content">
                  {#each comment.content.split('\n') as paragraph}
                    <p>{paragraph}</p>
                  {/each}
                </div>
              </div>
            {/each}
          </div>
          
          <div class="add-comment">
            <h3>Add Comment</h3>
            <div class="comment-form">
              <textarea 
                bind:value={commentText} 
                placeholder="Write your comment here..."
                rows="4"
              ></textarea>
              <button 
                class="btn btn-primary" 
                on:click={addComment}
                disabled={!commentText.trim()}
              >
                <i class="fas fa-paper-plane"></i>
                <span>Submit</span>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="issue-sidebar">
        <div class="sidebar-section card">
          <h3>Issue Details</h3>
          <div class="detail-item">
            <span class="detail-label">Status</span>
            <span class="badge {getStatusBadgeClass(issue.status)}">{issue.status}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Severity</span>
            <span class="badge {getSeverityBadgeClass(issue.severity)}">{issue.severity}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Reporter</span>
            <span>{issue.reporter.username}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Assignee</span>
            <span>{issue.assignee ? issue.assignee.username : 'Unassigned'}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Created</span>
            <span>{formatDate(issue.created_at)}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Updated</span>
            <span>{formatDate(issue.updated_at)}</span>
          </div>
        </div>
      </div>
    </div>
    
    {#if showStatusModal}
      <div class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h3>Update Issue Status</h3>
            <button class="close-btn" on:click={() => showStatusModal = false}>
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label for="status">New Status</label>
              <select id="status" bind:value={selectedStatus}>
                <option value="">Select Status</option>
                <option value="OPEN">Open</option>
                <option value="TRIAGED">Triaged</option>
                <option value="IN_PROGRESS">In Progress</option>
                <option value="DONE">Done</option>
              </select>
            </div>
            <div class="form-group">
              <label for="comment">Comment</label>
              <textarea 
                id="comment"
                bind:value={statusUpdateComment} 
                placeholder="Explain the status change..."
                rows="3"
              ></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" on:click={() => showStatusModal = false}>
              Cancel
            </button>
            <button 
              class="btn btn-primary" 
              on:click={updateStatus}
              disabled={!selectedStatus || !statusUpdateComment.trim()}
            >
              Update Status
            </button>
          </div>
        </div>
      </div>
    {/if}
  {/if}
</div>

<style>
  .issue-page {
    padding-bottom: 2rem;
  }
  
  .page-header {
    margin-bottom: 2rem;
  }
  
  .breadcrumbs {
    margin-bottom: 1rem;
  }
  
  .breadcrumb-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.875rem;
  }
  
  .breadcrumb-link:hover {
    color: var(--accent-color);
    text-decoration: none;
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
  
  .issue-header {
    margin-bottom: 2rem;
  }
  
  .issue-title-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .issue-title {
    font-size: 1.875rem;
    font-weight: 700;
    margin: 0;
  }
  
  .issue-badges {
    display: flex;
    gap: 0.5rem;
  }
  
  .issue-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    align-items: center;
  }
  
  .meta-item {
    display: flex;
    flex-direction: column;
  }
  
  .meta-label {
    font-size: 0.75rem;
    color: var(--text-muted);
  }
  
  .meta-value {
    font-weight: 500;
  }
  
  .issue-content {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 1.5rem;
  }
  
  .card {
    background-color: var(--background-color);
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--card-shadow);
  }
  
  .card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
  }
  
  .markdown-content p {
    margin-bottom: 1rem;
    line-height: 1.6;
  }
  
  .markdown-content p:last-child {
    margin-bottom: 0;
  }
  
  .attachments-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .comments-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .comment {
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 1.5rem;
  }
  
  .comment:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }
  
  .comment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
  }
  
  .comment-author {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .avatar {
    width: 2rem;
    height: 2rem;
    border-radius: 9999px;
    background-color: var(--accent-color);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
  }
  
  .username {
    font-weight: 500;
  }
  
  .comment-date {
    font-size: 0.875rem;
    color: var(--text-muted);
  }
  
  .comment-content p {
    margin-bottom: 1rem;
    line-height: 1.6;
  }
  
  .comment-content p:last-child {
    margin-bottom: 0;
  }
  
  .add-comment h3 {
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
  }
  
  .comment-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .comment-form textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    resize: vertical;
  }
  
  .comment-form button {
    align-self: flex-end;
  }
  
  .issue-sidebar {
    position: sticky;
    top: 6rem;
    height: fit-content;
  }
  
  .sidebar-section {
    margin-bottom: 1.5rem;
  }
  
  .sidebar-section h3 {
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
  }
  
  .detail-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border-color);
  }
  
  .detail-item:last-child {
    border-bottom: none;
  }
  
  .detail-label {
    color: var(--text-muted);
    font-size: 0.875rem;
  }
  
  .badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.5rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
  }
  
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
  }
  
  .modal {
    background-color: var(--background-color);
    border-radius: 0.5rem;
    width: 100%;
    max-width: 500px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid var(--border-color);
  }
  
  .modal-header h3 {
    font-size: 1.125rem;
    font-weight: 600;
    margin: 0;
  }
  
  .close-btn {
    background: none;
    border: none;
    cursor: pointer;
    color: var(--text-muted);
    font-size: 1.25rem;
    padding: 0;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
  
  .form-group {
    margin-bottom: 1.25rem;
  }
  
  .form-group:last-child {
    margin-bottom: 0;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }
  
  .form-group select,
  .form-group textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
  }
  
  .form-group textarea {
    resize: vertical;
  }
  
  .modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    padding: 1.25rem 1.5rem;
    border-top: 1px solid var(--border-color);
  }
  
  @media (max-width: 768px) {
    .issue-content {
      grid-template-columns: 1fr;
    }
    
    .issue-sidebar {
      position: static;
    }
  }
</style>
