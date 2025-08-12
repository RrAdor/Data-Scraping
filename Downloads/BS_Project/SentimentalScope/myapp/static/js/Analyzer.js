
        // Combined JavaScript functionality
        // Combined JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Profile dropdown toggle
    const profileBtn = document.getElementById('profileBtn');
    const profileDropdown = document.getElementById('profileDropdown');
    
    if (profileBtn && profileDropdown) {
        profileBtn.addEventListener('click', function() {
            profileDropdown.classList.toggle('show');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.user-profile')) {
                profileDropdown.classList.remove('show');
            }
        });
    }
    
    // Logout functionality
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            alert('Logging out...');
            // In a real app, this would redirect to logout endpoint
        });
    }
    
    // Simulate loading for demonstration
    setTimeout(function() {
        document.getElementById('loadingSection').style.display = 'none';
        document.getElementById('newsList').style.display = 'grid';
    }, 1500);
});

// Start Analysis - Auto-runs sentiment analysis and summary
function startAnalysis() {
    console.log('Starting automatic analysis...');
    
    // Get the Start Analysis button and update its state
    const analyzeBtn = document.querySelector('button[onclick="startAnalysis()"]');
    const originalBtnHTML = analyzeBtn ? analyzeBtn.innerHTML : '';
    const originalBtnClass = analyzeBtn ? analyzeBtn.className : '';
    
    // Set button to loading state
    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        analyzeBtn.className = originalBtnClass + ' loading';
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        analyzeBtn.style.cursor = 'not-allowed';
        analyzeBtn.style.opacity = '0.8';
    }
    
    const content = getContentForAnalysis();
    console.log('Content found:', content ? content.substring(0, 100) + '...' : 'No content');
    
    if (!content) {
        // Reset button on error
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.className = originalBtnClass;
            analyzeBtn.innerHTML = originalBtnHTML;
            analyzeBtn.style.cursor = 'pointer';
            analyzeBtn.style.opacity = '1';
        }
        showNotification('No content available for analysis', 'error');
        return;
    }
    
    // Show results section
    const resultsSection = document.getElementById('aiResults');
    const analysisStatus = document.getElementById('analysisStatus');
    
    console.log('Results section found:', !!resultsSection);
    console.log('Analysis status found:', !!analysisStatus);
    
    if (resultsSection) {
        resultsSection.style.display = 'block';
    }
    
    // Update status
    if (analysisStatus) {
        analysisStatus.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing sentiment...';
    }
    
    console.log('About to call analyzeSentiment()...');
    
    // Run sentiment analysis first, then summary
    analyzeSentiment()
        .then(() => {
            console.log('Sentiment analysis completed, starting summary...');
            if (analysisStatus) {
                analysisStatus.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating summary...';
            }
            if (analyzeBtn) {
                analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Summarizing...';
            }
            return generateSummary();
        })
        .then(() => {
            console.log('Summary completed, analysis finished!');
            if (analysisStatus) {
                analysisStatus.innerHTML = '<i class="fas fa-check-circle text-success"></i> Analysis complete!';
            }
            // Update button to completed state
            if (analyzeBtn) {
                analyzeBtn.innerHTML = '<i class="fas fa-check-circle"></i> Analysis Complete!';
                analyzeBtn.className = originalBtnClass + ' success';
                analyzeBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                analyzeBtn.style.color = 'white';
                
                // Reset button after 3 seconds
                setTimeout(() => {
                    analyzeBtn.disabled = false;
                    analyzeBtn.className = originalBtnClass;
                    analyzeBtn.innerHTML = originalBtnHTML;
                    analyzeBtn.style.cursor = 'pointer';
                    analyzeBtn.style.opacity = '1';
                    analyzeBtn.style.background = '';
                    analyzeBtn.style.color = '';
                }, 3000);
            }
            showNotification('Analysis completed successfully!', 'success');
        })
        .catch(error => {
            console.error('Error during analysis:', error);
            if (analysisStatus) {
                analysisStatus.innerHTML = '<i class="fas fa-exclamation-circle text-danger"></i> Analysis failed';
            }
            // Reset button on error
            if (analyzeBtn) {
                analyzeBtn.disabled = false;
                analyzeBtn.className = originalBtnClass;
                analyzeBtn.innerHTML = originalBtnHTML;
                analyzeBtn.style.cursor = 'pointer';
                analyzeBtn.style.opacity = '1';
                analyzeBtn.style.background = '';
                analyzeBtn.style.color = '';
            }
            showNotification('Analysis failed. Please try again.', 'error');
        });
}

// Article display functions
function showArticle(articleId) {
    // In a real app, this would fetch the specific article content
    document.getElementById('articleSection').style.display = 'block';
    document.getElementById('newsList').style.display = 'none';
    document.getElementById('timestampsList').style.display = 'none';
    document.getElementById('summaryBtnContainer').style.display = 'none';
    document.getElementById('summarySection').style.display = 'none';
    
    // Scroll to article section
    document.getElementById('articleSection').scrollIntoView({ behavior: 'smooth' });
}

function hideArticle() {
    document.getElementById('articleSection').style.display = 'none';
    document.getElementById('newsList').style.display = 'grid';
    document.getElementById('timestampsList').style.display = 'block';
    document.getElementById('summaryBtnContainer').style.display = 'block';
}

// Summary functions
function showSummary() {
    document.getElementById('summarySection').style.display = 'block';
    document.getElementById('summaryBtnContainer').style.display = 'none';
    
    // Scroll to summary section
    document.getElementById('summarySection').scrollIntoView({ behavior: 'smooth' });
}

function downloadSummaryPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Get summary text
    const summaryText = document.querySelector('#summarySection .summary-text').innerText;
    
    // Add content to PDF
    doc.text('SentimentScope Analysis Summary', 10, 10);
    doc.text(summaryText, 10, 20, { maxWidth: 180 });
    
    // Save the PDF
    doc.save('sentimentscope-summary.pdf');
}

// AI Analysis Functions
function analyzeSentiment() {
    return new Promise((resolve, reject) => {
        console.log('Running sentiment analysis...');
        
        // Get content to analyze
        const content = getContentForAnalysis();
        
        if (!content) {
            showNotification('No content available for sentiment analysis', 'error');
            reject('No content');
            return;
        }
        
        // Call sentiment analysis API
        fetch('/api/analyze-sentiment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ content: content })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displaySentimentResults(data.sentiment);
                resolve(data.sentiment);
            } else {
                showNotification('Error analyzing sentiment: ' + data.message, 'error');
                reject(data.message);
            }
        })
        .catch(error => {
            console.error('Sentiment analysis error:', error);
            showNotification('Network error during sentiment analysis', 'error');
            reject(error);
        });
    });
}

function generateSummary() {
    return new Promise((resolve, reject) => {
        console.log('Running text summarization...');
        
        // Get content to analyze
        const content = getContentForAnalysis();
        
        if (!content) {
            showNotification('No content available for summarization', 'error');
            reject('No content');
            return;
        }
        
        // Call summarization API
        fetch('/api/generate-summary/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ content: content })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displaySummaryResults(data.summary);
                resolve(data.summary);
            } else {
                showNotification('Error generating summary: ' + data.message, 'error');
                reject(data.message);
            }
        })
        .catch(error => {
            console.error('Summarization error:', error);
            showNotification('Network error during summarization', 'error');
            reject(error);
        });
    });
}

// Helper Functions
function getContentForAnalysis() {
    // Try to get content from different sources
    const contentDisplay = document.getElementById('contentDisplay');
    
    // Check for article content
    const articleContent = contentDisplay.querySelector('.article-content .content-text');
    if (articleContent) {
        return articleContent.textContent.trim();
    }
    
    // Check for transcript content
    const transcriptSegments = contentDisplay.querySelectorAll('.transcript-segment .segment-text');
    if (transcriptSegments.length > 0) {
        return Array.from(transcriptSegments).map(seg => seg.textContent).join(' ').trim();
    }
    
    // Check for manual content
    const manualContent = contentDisplay.querySelector('.manual-content .content-text');
    if (manualContent) {
        return manualContent.textContent.trim();
    }
    
    return null;
}

function displaySentimentResults(sentiment) {
    // Show the sentiment result card
    const sentimentResult = document.getElementById('sentimentResult');
    if (sentimentResult) {
        sentimentResult.style.display = 'block';
    }
    
    // Update main sentiment display
    const sentimentLabel = document.getElementById('sentimentLabel');
    const sentimentIcon = document.getElementById('sentimentIcon');
    const sentimentConfidence = document.getElementById('sentimentConfidence');
    
    if (sentimentLabel) {
        sentimentLabel.textContent = sentiment.label.charAt(0).toUpperCase() + sentiment.label.slice(1);
    }
    if (sentimentConfidence) {
        sentimentConfidence.textContent = Math.round(sentiment.confidence * 100) + '%';
    }
    
    // Update icon based on sentiment
    if (sentimentIcon) {
        let iconClass = 'fas fa-meh';
        if (sentiment.label === 'positive') {
            iconClass = 'fas fa-smile';
            sentimentIcon.style.color = '#10b981';
        } else if (sentiment.label === 'negative') {
            iconClass = 'fas fa-frown';
            sentimentIcon.style.color = '#ef4444';
        } else {
            iconClass = 'fas fa-meh';
            sentimentIcon.style.color = '#6b7280';
        }
        sentimentIcon.innerHTML = `<i class="${iconClass}"></i>`;
    }
    
    // Update sentiment bars with animation
    const scores = sentiment.scores;
    setTimeout(() => {
        const positiveBar = document.getElementById('positiveBar');
        const neutralBar = document.getElementById('neutralBar');
        const negativeBar = document.getElementById('negativeBar');
        const positiveValue = document.getElementById('positiveValue');
        const neutralValue = document.getElementById('neutralValue');
        const negativeValue = document.getElementById('negativeValue');
        
        if (positiveBar) positiveBar.style.width = (scores.positive * 100) + '%';
        if (neutralBar) neutralBar.style.width = (scores.neutral * 100) + '%';
        if (negativeBar) negativeBar.style.width = (scores.negative * 100) + '%';
        
        if (positiveValue) positiveValue.textContent = Math.round(scores.positive * 100) + '%';
        if (neutralValue) neutralValue.textContent = Math.round(scores.neutral * 100) + '%';
        if (negativeValue) negativeValue.textContent = Math.round(scores.negative * 100) + '%';
    }, 500);
    
    console.log('Sentiment analysis completed:', sentiment);
}

function displaySummaryResults(summary) {
    // Show the summary result card
    const summaryResult = document.getElementById('summaryResult');
    if (summaryResult) {
        summaryResult.style.display = 'block';
    }
    
    // Update summary text
    const summaryText = document.getElementById('summaryText');
    if (summaryText) {
        summaryText.textContent = summary.summary;
    }
    
    // Update compression ratio
    const compressionRatio = document.getElementById('compressionRatio');
    if (compressionRatio) {
        compressionRatio.textContent = Math.round(summary.compression_ratio * 100) + '% compression';
    }
    
    // Update stats
    const originalLength = document.getElementById('originalLength');
    const summaryLength = document.getElementById('summaryLength');
    const readingTime = document.getElementById('readingTime');
    
    if (originalLength) {
        originalLength.textContent = summary.original_length + ' words';
    }
    if (summaryLength) {
        summaryLength.textContent = summary.summary_length + ' words';
    }
    if (readingTime) {
        // Calculate reading time (average 200 words per minute)
        const timeInMin = Math.max(1, Math.round(summary.summary_length / 200));
        readingTime.textContent = timeInMin + ' min';
    }
    
    console.log('Text summarization completed:', summary);
}

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
           document.querySelector('meta[name=csrf-token]')?.getAttribute('content') || '';
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Auto remove
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}