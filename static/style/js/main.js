var signup_app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#signup_form',
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
                signup_app.clearPreviousError(1);

                signup_app.is_username_invalid = !response.data['result'];
                if (signup_app.is_username_invalid) signup_app.signup_form_errors.push({"id" : 1, "message" : response.data['message']});

            })
            .catch(function (error) {
                console.log(error);
            });
        },

        checkEmail(){
            axios.get("/user/check-email/" + this.email + emailExtension.textContent)
            .then(function (response) {
                signup_app.clearPreviousError(2);

                signup_app.is_email_invalid = !response.data['result'];
                if (signup_app.is_email_invalid) signup_app.signup_form_errors.push({"id" : 2, "message" : response.data['message']});

            })
            .catch(function (error) {
                console.log(error);
            });
        },

        checkPassword(){
            signup_app.clearPreviousError(3);
            signup_app.clearPreviousError(4);

            if(!signup_app.passwordsMatch()){
                signup_app.signup_form_errors.push({"id" : 4, "message" : "Las contraseñas introducidas no coinciden"});
            }
            if(!signup_app.isPasswordLongerThan5Chars()){
                signup_app.signup_form_errors.push({"id" : 3, "message" : "Las contraseña debe tener al menos 6 carácteres"});
            }

            this.is_password_invalid = !signup_app.passwordsMatch() || !signup_app.isPasswordLongerThan5Chars()

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
                signup_app.clearPreviousError(5);
                if(response.data['result']){
                    window.location.href = '/user/panel'
                }
                else{
                    signup_app.signup_form_errors.push({"id" : 5, "message" : response.data['message']});
                    console.log(response);
                }

            })
            .catch(function (error) {
                console.log(error.message);
            });
        },

        clearPreviousError(id){
            signup_app.signup_form_errors = signup_app.signup_form_errors.filter(function(error) { return error.id !== id });
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





var teacher_rating_app = new Vue({
    delimiters: ['[[', ']]'],
    el: "#teacher_rating_form",
    data:{
        rating: 3
    }
});