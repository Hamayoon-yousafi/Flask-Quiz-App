message_area = document.querySelector('.message_area')  
edit_profile_password = document.querySelector(".edit-profile-password")
edit_profile_confirm_password = document.querySelector(".edit-profile-confirm-password")

 

document.body.addEventListener('click', () => {
    message_area.style.display = "none"
})

if (edit_profile_password.required) {
    edit_profile_confirm_password.required = true
} else {
    edit_profile_confirm_password.required = false
}

function confirmation(event) {
    userconfirmation = confirm("Are you sure?")
    if (userconfirmation == false) {
        event.preventDefault()
    }
}


