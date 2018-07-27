


var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        title: 'Welcome to tiza negra',
        username: '',
        email: '',
        is_username_invalid: false,
        is_email_invalid: false,
        password: '',
        repeated_password: '',
        is_password_invalid: false,
        signup_form_errors: []
    },
    methods:{
        checkUsername(){
            axios.get('/user/check-username/' + this.username)
            .then(function (response) {
                app.signup_form_errors = app.signup_form_errors.filter(function(error) { return error.id !== 1 });

                app.is_username_invalid = !response.data['result'];
                if (app.is_username_invalid) app.signup_form_errors.push({"id" : 1, "message" : response.data['message']});

            })
            .catch(function (error) {
                console.log(error);
            });
        },

        checkEmail(){
            axios.get('/user/check-email/' + this.email)
            .then(function (response) {
                app.signup_form_errors = app.signup_form_errors.filter(function(error) { return error.id !== 2 });

                app.is_email_invalid = !response.data['result'];
                if (app.is_email_invalid) app.signup_form_errors.push({"id" : 2, "message" : response.data['message']});

            })
            .catch(function (error) {
                console.log(error);
            });
        },

        checkPassword(){
            app.signup_form_errors = app.signup_form_errors.filter(function(error) { return error.id !== 3 });
            var re = /^[A-Za-z\d$@$!%*?&]{6,}/;
            this.is_password_invalid = !re.test(this.password);
			if (this.is_password_invalid) app.signup_form_errors.push({"id" : 3, "message" : "Las contraseña debe tener al menos 6 carácteres"});
        },

        checkPasswordsMatch(){
            app.signup_form_errors = app.signup_form_errors.filter(function(error) { return error.id !== 4 });
            this.is_password_invalid = this.password != this.repeated_password
            if (this.is_password_invalid)app.signup_form_errors.push({"id" : 4, "message" : "Las contraseñas introducidas no coinciden"});
        }


    },
    computed:{
        is_username_valid() {
          return !this.is_username_invalid && this.username.length > 0
        },
        is_email_valid() {
          return !this.is_email_invalid && this.email.length > 0
        },
        is_password_valid(){
          return !this.is_password_invalid && this.password.length > 0 && this.repeated_password.length > 0
        }
    }
});




