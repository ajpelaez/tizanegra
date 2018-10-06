Vue.component('star-rating', VueStarRating.default);

var rating_app = new Vue({
    delimiters: ['[[', ']]'],
    el: "#rating_app",
    data:{
        rating: 3,
        checked_tags: 0
    },

    methods: {
        select_tag: function (event) {
            if (event.target.checked ) {
                if (this.checked_tags < 3) this.checked_tags += 1;
                else event.preventDefault();
            }
            else this.checked_tags -= 1;
        },
    }
});

$('#reportingModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var commentId = button.data('comment-id'); //
  var modal = $(this);
  modal.find('.modal-body input').val(commentId)
});
