document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Disable the submit button
    document.getElementById('submit-btn').disabled = true;
    
    // Show the progress bar
    var progressContainer = document.getElementById('Progress_Status');
    // progressContainer.style.display = 'block';
    
    var progressBar = document.getElementById('myprogressBar');
    progressBar.style.display = 'block';
    var progressText = document.getElementById('progress-text');
    progressBar.style.width = '0%';
    
    var files = document.querySelector('input[type="file"]').files;
    var numFiles = files.length;
    var totalTime = numFiles * 45000; // Number of files multiplied by 45 seconds
    
    var startTime = new Date().getTime();
    var endTime = startTime + totalTime;
    
    function updateProgress() {
      var currentTime = new Date().getTime();
      var elapsed = currentTime - startTime;
      var progress = Math.min((elapsed / totalTime) * 100, 100);
      
      progressBar.style.width = progress + '%';
      progressText.textContent = 'Progress: ' + progress.toFixed(2) + '%';
      
      if (currentTime < endTime) {
        setTimeout(updateProgress, 500); // Update progress every 500 milliseconds
      } else {
        progressText.textContent = 'Upload complete!';
        window.location.href = "/sftp_invoices/";
        // Redirect or update UI as needed
        // ...
        // Enable the submit button
        document.getElementById('submit-btn').disabled = false;
        // Hide the progress bar
        progressContainer.style.display = 'none';
      }
    }
    
    setTimeout(updateProgress, 500);
    
    // Submit the form asynchronously using AJAX
    var formData = new FormData(this);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', this.action, true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        // File upload completed successfully
        // ...
        
      } else if (xhr.readyState === 4 && xhr.status !== 200) {
        // File upload failed
        // ...
      }
    };
    xhr.send(formData);
});
