$(document).ready(
    $('.menu-toggle').click(function () {
        let menu_id = $(this).attr('for')
        let menu = $(menu_id)
        if (menu.hasClass('menu-active')) {
            menu.removeClass('menu-active')
        } else {
            menu.addClass('menu-active')
        }
    })
)