Vue.component('vue-bootstrap-typeahead', VueBootstrapTypeahead);

var search_app =  new Vue({
    delimiters: ['[[', ']]'],
    el: '#search-form',
    data() {
        return {
            teachers: [],
            selected_item: null,
            query: '',
            url: ''
        }
    },
    watch: {
        query(newQuery) {
            axios.get(`/api/get-teachers-and-subjects/${newQuery}`)
            .then((res) => {
                search_app.teachers = res.data.items
            })
        },
        selected_item(){
            window.location.href = search_app.selected_item.url;
        }
    }
});
