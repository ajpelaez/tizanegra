Vue.component('star-rating', VueStarRating.default);

var rating_app = new Vue({
    delimiters: ['[[', ']]'],
    el: "#rating_app",
    data:{
        rating: 3,
        current_comment_id: 0,
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

        addPositiveScore: function(comment_id){
            this.current_comment_id = comment_id;
            rating_app.addScore(this.current_comment_id, true);
        },

        addNegativeScore: function(comment_id){
            this.current_comment_id = comment_id;
            rating_app.addScore(this.current_comment_id, false);
        },

        addScore(comment_id, is_positive) {
            console.log(comment_id);
            rate_data = {
                comment_id : comment_id,
                is_positive : is_positive
            };

            var positive_counter = document.getElementById("positive-counter-"+comment_id);
            var negative_counter = document.getElementById("negative-counter-"+comment_id);
            var positive_score = parseInt(positive_counter.innerText);
            var negative_score = parseInt(negative_counter.innerText);

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios.post("/api/rate-comment/", rate_data)
            .then(function (response) {
                console.log(response.data);
                if (response.data['result']){
                    if (response.data['created']){
                        if (is_positive) positive_counter.innerHTML = positive_score + 1;
                        else negative_counter.innerHTML = negative_score + 1;
                    }
                    else if (response.data['changed']){
                        if (is_positive){
                            positive_counter.innerHTML = positive_score+1;
                            negative_counter.innerHTML = negative_score-1;
                        }
                        else{
                            positive_counter.innerHTML = positive_score-1;
                            negative_counter.innerHTML = negative_score+1;
                        }
                    }
                }
            })
            .catch(function (error) {
                console.log(error.message);
            });
        },

    }
});