var user_panel =  new Vue({
    delimiters: ['[[', ']]'],
    el: '#user_panel',
    data: {
        section: 1
    },
    methods:{
        change_section(section_id){
            this.section = section_id;
        }
    }
});
