Vue.component('star-rating', VueStarRating.default);

var teacher_rating_app = new Vue({
    delimiters: ['[[', ']]'],
    el: "#subject_rating",
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