// Get the modal
var modal = document.getElementById("confirmModal");

// Get the button that opens the modal
var btn = document.getElementById("confirmModalBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function () {
    modal.style.display = "block";
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
//when the user clicks the cancel button, close the modal
document.getElementById("cancelBtn").addEventListener("click", function () {
    modal.style.display = "none";
});

// Handle confirmation button click
document.getElementById("confirmBtn").addEventListener("click", function () {
    // Submit the form
    document.getElementById("editProfileForm").submit();
    localStorage.setItem('profilePictureUpdated', 'true');
});
