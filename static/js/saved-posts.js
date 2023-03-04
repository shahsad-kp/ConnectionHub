$(document).ready(function() {
    const saveButtons = $('.save-button')

    function removePost(){
        location.reload();
    }

    function getAllElements(post){
        let children = post.parent().parent().children().children();
        return children
    }

    saveButtons.click(removePost)
})