document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Set progress width from data attribute
    document.querySelectorAll('.progress-fill').forEach(progress => {
        progress.style.width = progress.getAttribute('data-width');
    });

    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    // Extract search data from HTML elements
    const searchData = [];
    
    // Add subjects to search data
    document.querySelectorAll('.search-subject-data').forEach(subjectElement => {
        const subject = {
            id: subjectElement.getAttribute('data-id'),
            name: subjectElement.getAttribute('data-name'),
            type: 'subject',
            url: subjectElement.getAttribute('data-url')
        };
        searchData.push(subject);
        
        // Add quizzes within this subject
        const subjectName = subject.name;
        subjectElement.querySelectorAll('.search-quiz-data').forEach(quizElement => {
            searchData.push({
                id: quizElement.getAttribute('data-id'),
                name: quizElement.getAttribute('data-name'),
                subject: subjectName,
                chapter: quizElement.getAttribute('data-chapter'),
                type: 'quiz',
                url: quizElement.getAttribute('data-url')
            });
        });
    });

    // Search input event listener
    searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        
        // Clear previous results
        searchResults.innerHTML = '';
        
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }
        
        // Filter subjects and quizzes based on search query
        const filteredResults = searchData.filter(item => 
            item.name.toLowerCase().includes(query) || 
            (item.type === 'quiz' && item.subject && item.subject.toLowerCase().includes(query)) ||
            (item.type === 'quiz' && item.chapter && item.chapter.toLowerCase().includes(query))
        );
        
        // Display results
        if (filteredResults.length > 0) {
            filteredResults.forEach(result => {
                const resultItem = document.createElement('div');
                resultItem.className = 'search-result-item';
                
                let resultContent = `
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${result.name}</strong>
                            <span class="search-result-tag tag-${result.type}">${result.type}</span>
                `;
                
                if (result.type === 'quiz') {
                    resultContent += `<div><small class="text-muted">${result.subject} - ${result.chapter}</small></div>`;
                }
                
                resultContent += `
                        </div>
                        <i class="fas fa-chevron-right text-muted"></i>
                    </div>
                `;
                
                resultItem.innerHTML = resultContent;
                
                // Add click event to navigate to the item
                resultItem.addEventListener('click', function() {
                    window.location.href = result.url;
                });
                
                searchResults.appendChild(resultItem);
            });
            
            searchResults.style.display = 'block';
        } else {
            const noResults = document.createElement('div');
            noResults.className = 'search-result-item';
            noResults.innerHTML = '<div class="text-muted text-center">No results found</div>';
            searchResults.appendChild(noResults);
            searchResults.style.display = 'block';
        }
    });
    
    // Close search results when clicking outside
    document.addEventListener('click', function(event) {
        if (!searchInput.contains(event.target) && !searchResults.contains(event.target)) {
            searchResults.style.display = 'none';
        }
    });
    
    // Show results again when focusing on input
    searchInput.addEventListener('focus', function() {
        if (this.value.trim().length >= 2) {
            searchResults.style.display = 'block';
        }
    });
    
    // Handle escape key to close search results
    searchInput.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            searchResults.style.display = 'none';
            searchInput.blur();
        }
    });
});