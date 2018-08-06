Vue.component('star-rating', VueStarRating.default);

var teacher_rating_app = new Vue({
    delimiters: ['[[', ']]'],
    el: "#teacher_rating_form",
    data:{
        rating: 3
    }
});