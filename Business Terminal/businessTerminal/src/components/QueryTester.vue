<template>
  <div id="query-tester">
    <b-card tag="article"
          style="max-width: 20rem;"
          class="mb-2 entries-card">
        <p>{{ data }}</p>
        <button>Test</button>
        <p>{{ result }}</p>
    </b-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      data: "Test",
      result: "",
      test: "haha"
    }
  },
  methods: {
      
  }
}
</script>

<style>

</style>