// function emailSubmission(){
//     submit = alert("Thank you for reaching out to us! \nWe will get back to you as soon as possible.");
//     console.log(submit);
// }

// document.getElementById("testBtn").addEventListener("click", (e) => {
//     console.log("Button Clicked")
// });


// const button = document.querySelector("button");

// button.addEventListener("click", (event) => {
//   button.textContent = `Click count: ${event.detail}`;
// });




// Add an event listener to the form
document.getElementById("contact_form").addEventListener('click', (e) => {
    // Prevent the default form submission behavior
    e.preventDefault();

    // Validate the form data
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var message = document.getElementById('message').value;

    if (!name || !email || !phone || !message) {
        alert('Please fill in all required fields.');
        return;
    }

    // Send the form data to the PHP script
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'contact-form-handler.php', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('name=' + name + '&email=' + email + '&message=' + message);
});



document.getElementById("submitEmailBtn").addEventListener("click", (e) => {
    submit = alert("Thank you for reaching out to us! \nWe will get back to you as soon as possible.");
    console.log(submit);
});
