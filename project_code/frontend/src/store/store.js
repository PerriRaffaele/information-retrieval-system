import {createStore} from 'vuex'
export default createStore({
    state() {
        return {
            results: [],
            query: ""
        }
    },
    getters: {
        getResults(state) {
            return state.results
        },
        getQuery(state) {
            return state.query
        },
    },
    mutations: {
        setResults(state, results) {
            console.log('yessir')
            state.results = results
        },
        setQuery(state, query) {
            state.query = query
        }
    },
    actions: {
        async fetchQuery(context, query) {
            const res = await fetch(`http://localhost:5000/query/${query}`)
            const results = await res.json()
            // console.log(results)
            context.commit("setQuery", query)
            return context.commit("setResults", results)
        },
        resetQuery(context) {
            return context.commit("setQuery", "")
        }
    }
})
