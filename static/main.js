// Mobile menu toggle
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const navLinks = document.querySelector('.nav-links');

if (mobileMenuBtn && navLinks) {
  mobileMenuBtn.addEventListener('click', () => {
    mobileMenuBtn.classList.toggle('active');
    navLinks.classList.toggle('active');
  });
}

// Close mobile menu when clicking on a link
const navItems = document.querySelectorAll('.nav-links a');
navItems.forEach(item => {
  alert("mobile")
  item.addEventListener('click', () => {
    if (mobileMenuBtn.classList.contains('active')) {
      mobileMenuBtn.classList.remove('active');
      navLinks.classList.remove('active');
    }
  });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    
    const targetId = this.getAttribute('href');
    if (targetId === '#') return;
    
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      window.scrollTo({
        top: targetElement.offsetTop - 80,
        behavior: 'smooth'
      });
    }
  });
});

// Form validation for query form
const queryForm = document.getElementById('query-form');
if (queryForm) {
  queryForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const category = document.getElementById('queryCategory').value;
    const message = document.getElementById('message').value;
    
    if (!fullName || !email || !category || !message) {
      alert('Please fill in all required fields');
      return;
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      alert('Please enter a valid email address');
      return;
    }
    
    // Form submission would go here
    alert('Thank you! Your query has been submitted successfully.');
    queryForm.reset();
  });
}

// Review filter functionality
const reviewFilter = document.getElementById('review-filter');
if (reviewFilter) {
  reviewFilter.addEventListener('change', function() {
    // This would normally filter the reviews based on selection
    console.log('Filter changed to:', this.value);
    // For now, we'll just show a message
    alert(`Reviews filtered by: ${this.value}`);
  });
}

// Like button functionality
const likeButtons = document.querySelectorAll('.like-btn');
likeButtons.forEach(button => {
  button.addEventListener('click', function() {
    const likeCount = this.querySelector('span');
    let currentLikes = parseInt(likeCount.innerText);
    
    // Toggle like state
    if (this.classList.contains('liked')) {
      this.classList.remove('liked');
      currentLikes -= 1;
    } else {
      this.classList.add('liked');
      currentLikes += 1;
    }
    
    likeCount.innerText = currentLikes;
  });
});

// Write a review button functionality
const writeReviewBtn = document.querySelector('.write-review-container .btn');
if (writeReviewBtn) {
  writeReviewBtn.addEventListener('click', function() {
    alert('Review form would open here');
    // In a real implementation, this would open a modal or navigate to a review form
  });
}

// Add active class to nav links based on scroll position
window.addEventListener('scroll', function() {
  const sections = document.querySelectorAll('section[id]');
  const scrollPosition = window.scrollY;
  
  sections.forEach(section => {
    const sectionTop = section.offsetTop - 100;
    const sectionHeight = section.offsetHeight;
    const sectionId = section.getAttribute('id');
    
    if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
      document.querySelector(`.nav-links a[href="#${sectionId}"]`)?.classList.add('active');
    } else {
      document.querySelector(`.nav-links a[href="#${sectionId}"]`)?.classList.remove('active');
    }
  });
});

// Pagination functionality
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const pageNumbers = document.querySelectorAll('.page-numbers a');

if (prevBtn && nextBtn && pageNumbers.length) {
  // Set initial state
  let currentPage = 1;
  
  // Update active page
  const updateActivePage = (pageNum) => {
    pageNumbers.forEach(page => {
      page.classList.remove('active');
      if (parseInt(page.innerText) === pageNum) {
        page.classList.add('active');
      }
    });
  };
  
  // Previous button click
  prevBtn.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      updateActivePage(currentPage);
    }
  });
  
  // Next button click
  nextBtn.addEventListener('click', () => {
    if (currentPage < pageNumbers.length) {
      currentPage++;
      updateActivePage(currentPage);
    }
  });
  
  // Page number click
  pageNumbers.forEach(page => {
    page.addEventListener('click', (e) => {
      e.preventDefault();
      currentPage = parseInt(page.innerText);
      updateActivePage(currentPage);
    });
  });
}

const redirectToPage = (a) => {
  const value = Number(a);
  console.log(value);
  if (value === 1) {
    window.location.href = "profile";
  } else {
    window.location.href = "login";
  }
}
