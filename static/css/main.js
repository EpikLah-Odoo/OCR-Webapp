// document.getElementById('upload-form').addEventListener('submit', function(e) {
//     e.preventDefault();
    
//     // Disable the submit button
//     document.getElementById('submit-btn').disabled = true;
    
//     // Show the progress bar
//     var progressContainer = document.getElementById('Progress_Status');
//     progressContainer.style.display = 'block';
    
//     var progressBar = document.getElementById('myprogressBar');
//     var progressText = document.getElementById('progress-text');
//     progressBar.style.width = '0%';
    
//     var files = document.querySelector('input[type="file"]').files;
//     var numFiles = files.length;
//     var totalTime = numFiles * 45000; // Number of files multiplied by 45 seconds
    
//     var startTime = new Date().getTime();
//     var endTime = startTime + totalTime;
    
//     function updateProgress() {
//       var currentTime = new Date().getTime();
//       var elapsed = currentTime - startTime;
//       var progress = Math.min((elapsed / totalTime) * 100, 100);
      
//       progressBar.style.width = progress + '%';
//       progressText.textContent = 'Progress: ' + progress.toFixed(2) + '%';
      
//       if (currentTime < endTime) {
//         setTimeout(updateProgress, 500); // Update progress every 500 milliseconds
//       } else {
//         progressText.textContent = 'Upload complete!';
//         // Perform SFTP transfer or other operations here
//         performSftpTransfer(files)
//           .then(() => {
//             // SFTP transfer completed
//             // Redirect or update UI as needed
//             // ...
//           })
//           .catch((error) => {
//             // Handle SFTP transfer error
//             console.error('SFTP transfer error:', error);
//           });
//       }
//     }
    
//     setTimeout(updateProgress, 500);
//   });

// function performSftpTransfer(files) {
//     return new Promise((resolve, reject) => {
//     const sftp = new SFTPClient();
//     // const sftp = new SFTPClient();
//     const serverOptions = {
//         // host: sftpHost,
//         // port: sftpPort,
//         // username: sftpUsername,
//         // password: sftpPassword,
//         host: 'gpt.helpbots.sg',
//         port: 22,
//         username: 'root',
//         password: 'EPIKLAH2023'
//     };
    
//     sftp.connect(serverOptions)
//         .then(() => {
//         const promises = Array.from(files).map((file) => {
//             const remoteFilePath = 'customer_data/' + file.name;
//             return sftp.put(file, remoteFilePath);
//         });
        
//         Promise.all(promises)
//             .then(() => {
//             sftp.end();
//             resolve();
//             })
//             .catch((error) => {
//             sftp.end();
//             reject(error);
//             });
//         })
//         .catch((error) => {
//         reject(error);
//         });
//     });
// }

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
        window.location.href = "/sftp/";
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
