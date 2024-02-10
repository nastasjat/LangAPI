function toggleMenu() {
  var dropdownMenu = document.getElementById("dropdownMenu");
  var menu = document.querySelector('.menu');
  
  var menuWidth = dropdownMenu.offsetWidth;
  var menuHeight = dropdownMenu.offsetHeight;
  var menuRect = menu.getBoundingClientRect();
  
  dropdownMenu.style.left = "-100%"; // Оновлено: Змінено на -100%
  dropdownMenu.style.right = "auto";
  
  if (menuRect.top + menuHeight > window.innerHeight) {
      dropdownMenu.style.top = "auto";
      dropdownMenu.style.bottom = "100%";
  } else {
      dropdownMenu.style.top = "0";
      dropdownMenu.style.bottom = "auto";
  }
  
  dropdownMenu.style.display = (dropdownMenu.style.display === "block") ? "none" : "block";
}

function navigateTo(page) {
  window.location.href = page;
}


function navigateToWithAnchor(page, anchor) {
  window.location.href = page + '#' + anchor;
}



function updateField() {
  var dropdown = document.getElementById("dropdown");
  var selectedValue = document.getElementById("selectedValue");

  // Отримуємо вибране значення та встановлюємо його у поле вводу
  selectedValue.value = dropdown.value;
}


function checkEnter(event) {
  if (event.key === "Enter") {
      saveText();
  }
}

function saveText() {
  // Отримуємо значення з текстового поля
  var userInput = document.getElementById("userInput").value;

  // Виводимо значення в консоль
  console.log("Збережений текст:", userInput);
}


function showPopup() {
  var popup = document.getElementById("popup");
  popup.style.display = "block";
}

function closePopup() {
  var popup = document.getElementById("popup");
  popup.style.display = "none";
}

//filter courses 
function filterCourses() {
    // Collect filter options
    var language = $("#dropdown_language").val();
    var price_from = $("#userInputFrom").val();
    var price_to = $("#userInputTo").val();
    var language_level = $("input[name='level']:checked").val();

    // Send AJAX request
    $.ajax({
        url: "/filtered_courses/",  
        type: "POST",
        data: {
            language: language,
            price_from: price_from,
            price_to: price_to,
            language_level: language_level,
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),  // Include CSRF token
        },
        success: function (data) {
            // Update the container with filtered courses
            $("#curses_block_container").html(data);
        },
        error: function () {
            alert("Error occurred during filtering.");
        },
    });
}

function submitData(clickedBlock, event) {
  // Prevent the default behavior of the anchor tag
  event.preventDefault();
  
  var languageName = clickedBlock.getAttribute('data-language');
  var courseName = clickedBlock.getAttribute('data-course-name');
  var price = clickedBlock.getAttribute('data-price');

  $.ajax({
    url: "/submit_course_data/",
    type: "POST",
    contentType: "application/json; charset=utf-8",  // Add this line
    dataType: "json",  
    data: JSON.stringify({
      language: languageName,
      name: courseName,
      price: price,
    }),
     headers: {
        "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()
    },
    success: function(response) {
      console.log(response);
      // Handle success, e.g., redirect to another page
      window.location.href = "/index3/";
    },
    error: function(xhr, status, error) {
      console.error('Error:', error);
      // Handle error, e.g., display an alert to the user
      alert('Failed to submit data. Please try again.');
    }
  });
}

