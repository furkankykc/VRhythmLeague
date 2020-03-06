(function($){
    "use strict";

    if(jQuery('#UpcomingMatches .navigation > a')) {

        // First load
        var id = 0;
        var val = 5;

        jQuery('#UpcomingMatches').find('li:not(.navigation)').hide();

        for (var nums = id; nums < val; nums++) {
            jQuery('#UpcomingMatches').find("li:eq(" + nums + "):not(.navigation)").fadeIn();
        }

        jQuery('.navigation > a').on('click tap', function () {
            var action = jQuery(this).data('id');
            var currentPage = $(this).parent().data('page');

            var list = jQuery(this).parent().parent();
            var perPage = 5;

            if(action == 'next') {
                var nextPage = currentPage + 1;
            } else {
                if(currentPage - 1 > 0) {
                    var nextPage = currentPage - 1;
                } else {
                    return false;
                }
            }
            // Pagination
            var start = (nextPage * perPage) - perPage;
            var val = start + perPage;

            var items = list.find('li:not(.navigation)').length;

            if(start >= items) {
                return false;
            }

            $(this).parent().data('page', nextPage);

            // Hide items
            jQuery(list).find('li:not(.navigation)').hide();

            for (var nums = start; nums < val; nums++) {
                jQuery(list).find("li:eq(" + nums + "):not(.navigation)").fadeIn();
            }
        });
    }
    
    $(".woocommerce-ordering select").chosen({disable_search: true});

})(jQuery);