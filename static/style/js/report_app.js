$('#reportingModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var commentId = button.data('comment-id'); //
  var modal = $(this);
  modal.find('.modal-body #comment-id').val(commentId)
});


var report_app =  new Vue({
    delimiters: ['[[', ']]'],
    el: '#report-form',
    data: {
        report_reason: "",
        form_is_not_sent: true,
        received_message: ""
    },
    methods:{
        resetApp(){
            setTimeout(function(){
                report_app.report_reason = "";
                report_app.form_is_not_sent = true;
                report_app.received_message = "";
            }, 3000);
        },

        sendReport() {
            report_data = {
                comment_id : $("#comment-id").val(),
                report_reason : this.report_reason
            };

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios.post("/api/report-comment/", report_data)
            .then(function (response) {
                report_app.form_is_not_sent = false;
                console.log(response.data)
                report_app.received_message = response.data['message'];
            })
            .catch(function (error) {
                console.log(error.message);
            });
        },
    }
});
