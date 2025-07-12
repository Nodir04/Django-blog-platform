// Markdown Preview Functionality
document.addEventListener('DOMContentLoaded', function() {
    const contentTextarea = document.getElementById('id_content');
    const previewBtn = document.getElementById('preview-btn');
    const editBtn = document.getElementById('edit-btn');
    const previewDiv = document.getElementById('preview-content');
    const textareaContainer = document.getElementById('textarea-container');
    
    if (!contentTextarea || !previewBtn || !editBtn || !previewDiv || !textareaContainer) {
        return; // Elements not found, exit
    }
    
    // Initialize preview mode state
    let isPreviewMode = false;
    
    // Toggle between edit and preview modes
    function togglePreviewMode() {
        if (isPreviewMode) {
            // Switch to edit mode
            showEditMode();
        } else {
            // Switch to preview mode
            showPreviewMode();
        }
    }
    
    function showEditMode() {
        isPreviewMode = false;
        textareaContainer.style.display = 'block';
        previewDiv.style.display = 'none';
        previewBtn.style.display = 'inline-block';
        editBtn.style.display = 'none';
        previewBtn.classList.remove('active');
        editBtn.classList.add('active');
    }
    
    function showPreviewMode() {
        isPreviewMode = true;
        const markdownContent = contentTextarea.value;
        
        // Send content to server for markdown processing
        fetch('/blog/preview/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                'content': markdownContent
            })
        })
        .then(response => response.json())
        .then(data => {
            previewDiv.innerHTML = data.html;
            textareaContainer.style.display = 'none';
            previewDiv.style.display = 'block';
            previewBtn.style.display = 'none';
            editBtn.style.display = 'inline-block';
            previewBtn.classList.add('active');
            editBtn.classList.remove('active');
            
            // Apply syntax highlighting to code blocks
            if (typeof Prism !== 'undefined') {
                Prism.highlightAll();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error generating preview. Please try again.');
        });
    }
    
    // Event listeners
    previewBtn.addEventListener('click', function(e) {
        e.preventDefault();
        togglePreviewMode();
    });
    
    editBtn.addEventListener('click', function(e) {
        e.preventDefault();
        togglePreviewMode();
    });
    
    // Auto-save functionality (optional)
    let autoSaveTimer;
    contentTextarea.addEventListener('input', function() {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = setTimeout(function() {
            // You can implement auto-save here
            console.log('Auto-save triggered');
        }, 2000); // Save after 2 seconds of no typing
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + P for preview
        if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
            e.preventDefault();
            togglePreviewMode();
        }
        
        // Ctrl/Cmd + S for save (if you want to implement this)
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            // Trigger form submission or save
            document.querySelector('form').submit();
        }
    });
    
    // Add formatting buttons functionality
    const formatButtons = document.querySelectorAll('.format-btn');
    formatButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const format = this.dataset.format;
            insertMarkdown(format);
        });
    });
    
    function insertMarkdown(format) {
        const textarea = contentTextarea;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const selectedText = textarea.value.substring(start, end);
        let replacement = '';
        
        switch (format) {
            case 'bold':
                replacement = `**${selectedText || 'bold text'}**`;
                break;
            case 'italic':
                replacement = `*${selectedText || 'italic text'}*`;
                break;
            case 'code':
                replacement = `\`${selectedText || 'code'}\``;
                break;
            case 'link':
                replacement = `[${selectedText || 'link text'}](url)`;
                break;
            case 'image':
                replacement = `![${selectedText || 'alt text'}](image-url)`;
                break;
            case 'quote':
                replacement = `> ${selectedText || 'quote'}`;
                break;
            case 'h1':
                replacement = `# ${selectedText || 'Heading 1'}`;
                break;
            case 'h2':
                replacement = `## ${selectedText || 'Heading 2'}`;
                break;
            case 'h3':
                replacement = `### ${selectedText || 'Heading 3'}`;
                break;
            case 'ul':
                replacement = `- ${selectedText || 'list item'}`;
                break;
            case 'ol':
                replacement = `1. ${selectedText || 'list item'}`;
                break;
        }
        
        textarea.value = textarea.value.substring(0, start) + replacement + textarea.value.substring(end);
        textarea.focus();
        
        // Set cursor position
        const newCursorPos = start + replacement.length;
        textarea.setSelectionRange(newCursorPos, newCursorPos);
    }
    
    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});