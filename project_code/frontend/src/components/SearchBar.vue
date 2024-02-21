<script>

export default {
  data() {
    return{
      query: '',
      message: "Search Science Experiment..."
    }
  },
  methods: {
    async solveQuery() {
      if (this.query) {
        await this.$store.dispatch("fetchQuery", this.query)
      }
    },
    resetQuery() {
      this.query = ''
    },
    setQuery(q) {
      this.query = q
    }
  }
}

</script>

<template>
  <input type="text" v-model="query" :placeholder=this.message @keyup.enter="solveQuery()" spellcheck="false"/>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Montserrat&display=swap");

* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  font-family: "Montserrat", sans-serif;
}

body {
  padding: 20px;
  min-height: 100vh;
  background-color: rgb(234, 242, 255);
}

input {
  display: block;
  width: 550px;
  margin: 20px auto;
  padding: 10px 45px;
  background: black url("assets/search_icon.svg") no-repeat 15px center;
  background-size: 15px 15px;
  font-size: 16px;
  color: #f8f8f8;
  border: none;
  border-radius: 5px;
  box-shadow: rgba(50, 50, 93, 0.25) 0 2px 5px -1px,
  rgba(0, 0, 0, 0.3) 0 1px 3px -1px;
}
</style>