$(document).ready(function() {
    const saveButtons = $('.save-button')

    function removePost(){
        location.reload();
    }

    saveButtons.click(removePost)
})