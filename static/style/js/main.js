var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        title: 'Welcome to tiza negra',
        username: '',
        email: '',
        university: 'UGR',
        degree: 'GII',
        is_username_invalid: false,
        is_email_invalid: false,
        password: '',
        repeated_password: '',
        is_password_invalid: false,
        signup_form_errors: []
    },
    methods:{
        checkUsername(){
            axios.get("/user/check-username/" + this.username)
            .then(function (response) {
                app.clearPreviousError(1);

                app.is_username_invalid = !response.data['result'];
                if (app.is_username_invalid) app.signup_form_errors.push({"id" : 1, "message" : response.data['message']});

            })
            .catch(function (error) {
                console.log(error);
            });
        },

        checkEmail(){
            axios.get("/user/check-email/" + this.email + emailExtension.textContent)
            .then(function (response) {
                app.clearPreviousError(2);

                app.is_email_invalid = !response.data['result'];
                if (app.is_email_invalid) app.signup_form_errors.push({"id" : 2, "message" : response.data['message']});

            })
            .catch(function (error) {
                console.log(error);
            });
        },

        checkPassword(){
            app.clearPreviousError(3);
            app.clearPreviousError(4);

            if(!app.passwordsMatch()){
                app.signup_form_errors.push({"id" : 4, "message" : "Las contraseñas introducidas no coinciden"});
            }
            if(!app.isPasswordLongerThan5Chars()){
                app.signup_form_errors.push({"id" : 3, "message" : "Las contraseña debe tener al menos 6 carácteres"});
            }

            this.is_password_invalid = !app.passwordsMatch() || !app.isPasswordLongerThan5Chars()

        },

        passwordsMatch(){
            return this.password == this.repeated_password
        },

        isPasswordLongerThan5Chars(){
            var re = /^[A-Za-z\d$@$!%*?&]{6,}/;
            return re.test(this.password);
        },

        manageSignUp() {
            csrftoken = Cookies.get('csrftoken');
            headers = {HTTP_X_CSRFTOKEN: csrftoken};
            signup_data = {
                username : this.username,
                email : this.email,
                password : this.password,
                degree : this.degree,
                university : this.university
            };

            axios.post("/user/signup/", signup_data, headers)
            .then(function (response) {
                app.clearPreviousError(5);
                if(response.data['result']){
                    window.location.href = '/user/panel'
                }
                else{
                    app.signup_form_errors.push({"id" : 5, "message" : response.data['message']});
                    console.log(response);
                }

            })
            .catch(function (error) {
                console.log(error.message);
            });
        },

        clearPreviousError(id){
            app.signup_form_errors = app.signup_form_errors.filter(function(error) { return error.id !== id });
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
        },
        is_form_invalid(){
            return !(this.is_username_valid && this.is_email_valid && this.is_password_valid)
        }
    }
});




