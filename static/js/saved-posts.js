$(document).ready(function() {
    const saveButtons = $('.save-button')

    function removePost(){
        $($(this).data('element-id')).remove()
    }

    saveButtons.click(removePost)
})