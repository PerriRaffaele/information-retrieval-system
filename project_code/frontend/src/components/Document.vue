<script>

export default {
  props: {
    document
  },
  methods: {
    str_limit(value, size) {
      if (!value) return '';
      value = value.toString();

      if (value.length <= size) {
        return value;
      }
      return value.substr(0, size) + '...';
    }
  }
}

</script>

<template>
  <div class="result-box">
    <a v-bind:href="document.link" target="_blank" rel="noreferrer" class="result-title">
      {{ document.title }}
      <p v-if="document.description" class="result-text">
        {{ this.str_limit(document.description, 240) }}
      </p>
      <p v-else class="result-text">
        {{ this.str_limit(document.explanation, 240) }}
      </p>
    </a>
  </div>
</template>

<style scoped>
.result-box {
  width: 800px;
  border: 3px solid;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 20px;
  transition: background-color 0.3s, transform 0.3s;
}

.result-box:hover {
  background-color: black;
  transform: scale(1.05);
}

.result-title {
  display: block;
  font-size: 23px;
  font-weight: bold;
  color:hsl(196, 76%, 39%);
  text-decoration: none;
  margin-bottom: 5px;
}

.result-text {
  font-size: 14px;
  color: lightgray;
  margin: 0;
}
</style>