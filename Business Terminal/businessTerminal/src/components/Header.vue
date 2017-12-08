<template>
  <header id="bt-header">
    <b-navbar id="bt-navbar" toggleable="md" type="dark" variant="danger">

      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

      <b-navbar-brand href="#">E-Food Business Terminal</b-navbar-brand>

      <b-collapse is-nav id="nav_collapse">

        <b-navbar-nav>
          <b-nav-item href="#" disabled>Start</b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
        
        </b-navbar-nav>

      </b-collapse>
    </b-navbar>
  </header>
</template>

<script>
export default {
  data () {
    return {
      
    }
  }
}
</script>

<style>

</style>