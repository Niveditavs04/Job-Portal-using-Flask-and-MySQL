
function searchJobs() {
    // Placeholder function for search functionality
    alert('Search functionality will be implemented in the future.');
  }
  
  function goToJobSeeker() {
    window.location.href = "index1.html";
  }
  
  function goToEmployer() {
    window.location.href = 'employer.html';
  }
  
// script.js

document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('form').addEventListener('submit', function(e) {
      e.preventDefault(); // Prevent form submission
      
      // Get the values of the checkboxes
      var emailNotification = document.getElementById('emailNotification').checked ? 1 : 0;
      var smsNotification = document.getElementById('smsNotification').checked ? 1 : 0;
      
      // You can do something with these values, such as sending them to the server
      
      // For now, let's just log them to the console
      console.log('Email Notification:', emailNotification);
      console.log('SMS Notification:', smsNotification);
      
      // Proceed with form submission if needed
      this.submit();
  });
});
