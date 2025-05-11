$(document).ready(function () {
    $('#ShowHideBtn').on('click', function () {
        const $sidebar = $('#sidebar');
        if ($sidebar.hasClass('active')) {
            $sidebar.removeClass('active').addClass('inactive');
        } else {
            $sidebar.removeClass('inactive').addClass('active');
        }
    });
});