<script>

import Document from "@/components/Document.vue";

export default {
  components: {Document},
  data () {
    return {
      clicked: true,
      isArrowRotated: false,
    }
  },
  props: {
    results: Array,
    topic: String
  },
  methods: {
    show() {
      this.clicked = !this.clicked;
      this.isArrowRotated = !this.isArrowRotated;
    }
  },
  computed: {
    inherent_res() {
      let res = []
      this.results.forEach(el => {
        if (el.subject === this.topic)
          res.push(el)
      })
      return res
    },
    watch: {
      inherent_res: {
        immediate: false,
        deep: false,
        handler(newValue, oldValue) {
          console.log(newValue);
        }
      }
    }
  }
}

</script>

<template>

  <div class="header">
  <img id="logo" src="../assets/atom.svg" alt="Your Image Alt Text"/>
    <h2 @click="show">
      <span style="color: hsl(204, 69%, 33%);">{{ this.topic }}:</span> {{ inherent_res.length }} result<span v-if="inherent_res.length > 1">s</span>
    </h2>
  <div @click="show">
      <img src="../assets/plus.svg" alt="Your Image Alt Text" class="arrow-icon" v-if="!isArrowRotated"/>
      <img src="../assets/plus.svg" alt="Your Image Alt Text" class="arrow-icon-rotated" v-else/>
  </div>
  </div>
  <div v-if="clicked">

  </div>

  <ul v-else v-for="exp in inherent_res">
      <Document :document="exp"></Document>
  </ul>

</template>

<style scoped>
  .arrow-icon, .arrow-icon-rotated {
    width: 20px;
    margin-inline: 15px;
    cursor: pointer;
    margin-top: 10px;

    transition: transform 0.5s ease-in-out;
  }

  .arrow-icon-rotated {
    -webkit-transform: rotate(45deg);
    -ms-transform: rotate(45deg);
    transform: rotate(45deg);

    transition: transform 0.5s ease-in-out;
  }

  .header{
    display: flex;
    flex-direction: row;
    margin-block: 10px;
    align-items: center;
  }

  #logo {
    width: 25px;
    margin-inline: 10px;
  }

  h2 {
    cursor: pointer;
  }

</style>