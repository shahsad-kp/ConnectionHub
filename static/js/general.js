$(document).ready(
    $('.menu-toggle').click(function() {
        let menu = $($(this).attr('for'))
        if (menu.hasClass('menu-active')) {
            menu.removeClass('menu-active')
        } else {
            menu.addClass('menu-active')
        }

        menu.focusout(
            function() {
                menu.removeClass('menu-active')
            }
        )
    })
)