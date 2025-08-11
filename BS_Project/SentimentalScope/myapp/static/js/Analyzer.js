
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