<template>
  <div id="app">
    <bt-header></bt-header>
    <div class="container">
      <div class="row">
        <div class="col-sm">
            <bt-user-data></bt-user-data>
            <bt-select-user></bt-select-user>
        </div>
        <div class="col-sm">
            <bt-last-entries></bt-last-entries>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import btHeader from './components/Header.vue';
import lastEntries from './components/LastEntries.vue';
import queryTester from './components/QueryTester.vue';
import userData from './components/UserData.vue';
import selectUser from './components/SelectUser.vue';

export default {
  components: {
    'bt-header': btHeader,
    'bt-last-entries': lastEntries,
    'bt-query-tester': queryTester,
    'bt-user-data': userData,
    'bt-select-user': selectUser
  },
  data () {
    return {
      
    }
  }
}
</script>

<style>

</style>