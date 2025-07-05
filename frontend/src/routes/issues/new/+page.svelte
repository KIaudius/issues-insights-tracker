<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  // Form state
  let title = '';
  let description = '';
  let severity = 'MEDIUM';
  let files = [];
  let uploading = false;
  let error = null;
  let success = false;
  
  // File upload handling
  let fileInput;
  let selectedFiles = [];
  let dragActive = false;
  
  // Validation
  let errors = {
    title: '',
    description: '',
    files: ''
  };
  
  onMount(() => {
    // Any initialization if needed
  });
  
  function handleFilesSelected(e) {
    const fileList = e.target.files;
    handleFiles(fileList);
  }
  
  function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    dragActive = true;
  }
  
  function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    dragActive = false;
  }
  
  function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    dragActive = false;
    
    if (e.dataTransfer.files) {
      handleFiles(e.dataTransfer.files);
    }
  }
  
  function handleFiles(fileList) {
    // Convert FileList to array and add to selectedFiles
    const newFiles = Array.from(fileList);
    
    // Validate file types and sizes
    const validFileTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'text/plain'];
    const maxFileSize = 5 * 1024 * 1024; // 5MB
    
    const validatedFiles = newFiles.filter(file => {
      // Check file type
      if (!validFileTypes.includes(file.type)) {
        errors.files = `File type ${file.type} is not supported`;
        return false;
      }
      
      // Check file size
      if (file.size > maxFileSize) {
        errors.files = `File ${file.name} exceeds the 5MB size limit`;
        return false;
      }
      
      return true;
    });
    
    if (validatedFiles.length > 0) {
      errors.files = '';
      selectedFiles = [...selectedFiles, ...validatedFiles];
    }
  }
  
  function removeFile(index) {
    selectedFiles = selectedFiles.filter((_, i) => i !== index);
  }
  
  function validateForm() {
    let isValid = true;
    
    // Reset errors
    errors = {
      title: '',
      description: '',
      files: ''
    };
    
    // Validate title
    if (!title.trim()) {
      errors.title = 'Title is required';
      isValid = false;
    } else if (title.length < 5) {
      errors.title = 'Title must be at least 5 characters';
      isValid = false;
    } else if (title.length > 100) {
      errors.title = 'Title must be less than 100 characters';
      isValid = false;
    }
    
    // Validate description
    if (!description.trim()) {
      errors.description = 'Description is required';
      isValid = false;
    } else if (description.length < 20) {
      errors.description = 'Description must be at least 20 characters';
      isValid = false;
    }
    
    // Validate files (at least one file is required)
    if (selectedFiles.length === 0) {
      errors.files = 'At least one file attachment is required';
      isValid = false;
    }
    
    return isValid;
  }
  
  async function submitIssue() {
    if (!validateForm()) return;
    
    uploading = true;
    error = null;
    
    try {
      // In a real implementation, this would post to the API
      // First, create the issue
      // const issueResponse = await fetch('/api/v1/issues/', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ 
      //     title, 
      //     description,
      //     severity 
      //   })
      // });
      // 
      // const issueData = await issueResponse.json();
      // const issueId = issueData.data.id;
      // 
      // // Then upload each file
      // for (const file of selectedFiles) {
      //   const formData = new FormData();
      //   formData.append('file', file);
      //   
      //   await fetch(`/api/v1/issues/${issueId}/attachments`, {
      //     method: 'POST',
      //     body: formData
      //   });
      // }
      
      // For now, we'll simulate a successful submission
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      success = true;
      
      // Redirect to issues list after a short delay
      setTimeout(() => {
        goto('/issues');
      }, 2000);
    } catch (e) {
      console.error('Error submitting issue:', e);
      error = 'Failed to submit issue. Please try again later.';
    } finally {
      uploading = false;
    }
  }
</script>

<svelte:head>
  <title>New Issue | Issues & Insights</title>
</svelte:head>

<div class="new-issue-page">
  <div class="page-header">
    <div class="breadcrumbs">
      <a href="/issues" class="breadcrumb-link">
        <i class="fas fa-arrow-left"></i>
        <span>Back to Issues</span>
      </a>
    </div>
    <h1 class="page-title">Create New Issue</h1>
  </div>
  
  {#if success}
    <div class="success-message">
      <i class="fas fa-check-circle"></i>
      <p>Issue created successfully! Redirecting...</p>
    </div>
  {:else}
    <form class="issue-form" on:submit|preventDefault={submitIssue}>
      <div class="form-group">
        <label for="title">Title <span class="required">*</span></label>
        <input 
          type="text" 
          id="title" 
          bind:value={title} 
          class={errors.title ? 'error' : ''}
          placeholder="Brief summary of the issue"
        />
        {#if errors.title}
          <div class="error-message">{errors.title}</div>
        {/if}
      </div>
      
      <div class="form-group">
        <label for="description">Description <span class="required">*</span></label>
        <textarea 
          id="description" 
          bind:value={description} 
          class={errors.description ? 'error' : ''}
          placeholder="Detailed description of the issue, including steps to reproduce if applicable"
          rows="8"
        ></textarea>
        {#if errors.description}
          <div class="error-message">{errors.description}</div>
        {/if}
        <div class="form-help">
          <i class="fas fa-info-circle"></i>
          <span>Markdown formatting is supported</span>
        </div>
      </div>
      
      <div class="form-group">
        <label for="severity">Severity <span class="required">*</span></label>
        <select id="severity" bind:value={severity}>
          <option value="LOW">Low</option>
          <option value="MEDIUM">Medium</option>
          <option value="HIGH">High</option>
          <option value="CRITICAL">Critical</option>
        </select>
      </div>
      
      <div class="form-group">
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label>Attachments <span class="required">*</span></label>
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div 
          class="file-drop-area {dragActive ? 'active' : ''} {errors.files ? 'error' : ''}"
          on:dragover={handleDragOver}
          on:dragleave={handleDragLeave}
          on:drop={handleDrop}
        >
          <div class="file-drop-content">
            <i class="fas fa-cloud-upload-alt"></i>
            <p>Drag and drop files here or</p>
            <button 
              type="button" 
              class="btn btn-secondary" 
              on:click={() => fileInput.click()}
            >
              Browse Files
            </button>
            <input 
              type="file" 
              bind:this={fileInput} 
              on:change={handleFilesSelected} 
              multiple 
              style="display: none;"
            />
          </div>
        </div>
        {#if errors.files}
          <div class="error-message">{errors.files}</div>
        {/if}
        <div class="form-help">
          <i class="fas fa-info-circle"></i>
          <span>Supported file types: JPG, PNG, GIF, PDF, TXT. Max size: 5MB per file.</span>
        </div>
        
        {#if selectedFiles.length > 0}
          <div class="selected-files">
            <h3>Selected Files ({selectedFiles.length})</h3>
            <ul class="file-list">
              {#each selectedFiles as file, index}
                <li class="file-item">
                  <div class="file-info">
                    <i class="fas {file.type.includes('image') ? 'fa-file-image' : file.type.includes('pdf') ? 'fa-file-pdf' : 'fa-file-alt'}"></i>
                    <span class="file-name">{file.name}</span>
                    <span class="file-size">({(file.size / 1024).toFixed(1)} KB)</span>
                  </div>
                  <button 
                    type="button" 
                    class="remove-file-btn" 
                    on:click={() => removeFile(index)}
                  >
                    <i class="fas fa-times"></i>
                  </button>
                </li>
              {/each}
            </ul>
          </div>
        {/if}
      </div>
      
      {#if error}
        <div class="form-error">
          <i class="fas fa-exclamation-triangle"></i>
          <p>{error}</p>
        </div>
      {/if}
      
      <div class="form-actions">
        <a href="/issues" class="btn btn-secondary">Cancel</a>
        <button 
          type="submit" 
          class="btn btn-primary" 
          disabled={uploading}
        >
          {#if uploading}
            <div class="spinner-small"></div>
            <span>Submitting...</span>
          {:else}
            <i class="fas fa-paper-plane"></i>
            <span>Submit Issue</span>
          {/if}
        </button>
      </div>
    </form>
  {/if}
</div>

<style>
  .new-issue-page {
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
  
  .page-title {
    font-size: 1.875rem;
    font-weight: 700;
    margin: 0;
  }
  
  .issue-form {
    background-color: var(--background-color);
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    padding: 2rem;
    box-shadow: var(--card-shadow);
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
  
  .form-group input,
  .form-group textarea,
  .form-group select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: 1rem;
  }
  
  .form-group input.error,
  .form-group textarea.error,
  .form-group select.error,
  .file-drop-area.error {
    border-color: var(--error-color);
  }
  
  .form-group textarea {
    resize: vertical;
  }
  
  .error-message {
    color: var(--error-color);
    font-size: 0.875rem;
    margin-top: 0.5rem;
  }
  
  .form-help {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-muted);
    font-size: 0.875rem;
    margin-top: 0.5rem;
  }
  
  .file-drop-area {
    border: 2px dashed var(--border-color);
    border-radius: 0.5rem;
    padding: 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .file-drop-area.active {
    border-color: var(--accent-color);
    background-color: var(--hover-bg);
  }
  
  .file-drop-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  
  .file-drop-content i {
    font-size: 2.5rem;
    color: var(--text-muted);
  }
  
  .file-drop-content p {
    margin: 0;
    color: var(--text-muted);
  }
  
  .selected-files {
    margin-top: 1.5rem;
  }
  
  .selected-files h3 {
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
  }
  
  .file-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .file-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    background-color: var(--background-secondary);
    border-radius: 0.375rem;
  }
  
  .file-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .file-info i {
    color: var(--text-muted);
  }
  
  .file-name {
    font-weight: 500;
  }
  
  .file-size {
    font-size: 0.875rem;
    color: var(--text-muted);
  }
  
  .remove-file-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 0.25rem;
    font-size: 0.875rem;
    transition: color 0.2s;
  }
  
  .remove-file-btn:hover {
    color: var(--error-color);
  }
  
  .form-error {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    background-color: var(--error-bg);
    border: 1px solid var(--error-color);
    border-radius: 0.375rem;
    margin-bottom: 1.5rem;
    color: var(--error-color);
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
  }
  
  .spinner-small {
    width: 1rem;
    height: 1rem;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-left-color: white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  .success-message {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 0;
    gap: 1rem;
    text-align: center;
  }
  
  .success-message i {
    font-size: 3rem;
    color: var(--success-color);
  }
  
  .success-message p {
    font-size: 1.25rem;
    font-weight: 500;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
</style>
