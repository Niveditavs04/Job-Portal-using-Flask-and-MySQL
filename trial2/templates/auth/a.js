let names = [
    "Software Development",
    "Web Development", 
    "Mobile App Development",
    "Data Science", 
    "Cybersecurity", 
    "Devops", 
    "AWS Cloud Engineer",
    "MERN Developer", 
    "Java Full Stack Developer",
    "Database Engineer", 
    "Frontend Developer", 
    "Backend Developer",
    "Finance and Accounting",
    "Financial Analysis",
    "Banking",
    "Investment Management",
    "Sales and Marketing",
    "Sales Representatives",
    "Marketing Manager",
    "Digital Marketing Specialist",
    "Advertising",
    "Public Relations",
    "Education",
    "Teaching",
    "Academic Administration",
    "Education Consultant",
    "Instructional Design",
    "Special Education",
    "HR Generalist",
    "Recruiter",
    "Training and Development",
    "Compensation and Benefits",
    "HR Managers"
  ];
  
  // Sort names in ascending order
  let sortedNames = names.sort();
  
  // Reference to input and suggestions div
  let jobTitleInput = document.getElementById("jobTitleInput");
  let autocompleteList = document.createElement("ul");
  autocompleteList.classList.add("autocomplete-list");
  document.querySelector(".autocomplete-wrapper").appendChild(autocompleteList);
  
  // Event listener for input on the job title input field
  jobTitleInput.addEventListener("input", function() {
    // Clear previous suggestions
    autocompleteList.innerHTML = "";
  
    // Get input value
    let inputValue = jobTitleInput.value.toLowerCase();
  
    // Filter names based on input value
    let filteredNames = sortedNames.filter(name => name.toLowerCase().startsWith(inputValue));
  
    // Display filtered names as suggestions
    filteredNames.forEach(name => {
        let suggestion = document.createElement("li");
        suggestion.innerHTML = name;
        suggestion.addEventListener("click", function() {
            jobTitleInput.value = name;
            autocompleteList.innerHTML = "";
        });
        autocompleteList.appendChild(suggestion);
    });
  });
  
  // Close suggestions when clicking outside the input field
  document.addEventListener("click", function(e) {
    if (e.target !== jobTitleInput && e.target.parentNode !== autocompleteList) {
        autocompleteList.innerHTML = "";
    }
  });
  