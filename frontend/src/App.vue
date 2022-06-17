<template>
  <nav class="navbar navbar-light navbar-expand bg-light navigation-clean">
    <div class="container">
      <router-link class="navbar-brand" to="/">Smart City</router-link>
      <button class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navcol-1"></button>
      <div id="navcol-1" class="collapse navbar-collapse" style="transform: perspective(2220px);">
        <router-link class="btn btn-primary ms-auto" role="button" to="/create">Registrieren</router-link>
        <router-link class="btn btn-primary" role="button" to="/login">Anmelden</router-link>
        <router-link class="btn btn-primary" role="button" to="/details">Accountinformationen</router-link>
        <button class="btn btn-primary" @click="logout">Abmelden</button>
      </div>
    </div>
  </nav>
  <div class="container">
    <ul class="list-inline mb-2">
      <li class="list-inline-item"><a href="http://server.it-humke.de:8003">Stadtverwaltung</a></li>
      <li class="list-inline-item"><span>⋅</span></li>
      <li class="list-inline-item"><a href="http://server.it-humke.de:8002">Fahrzeugvermietung</a></li>
      <li class="list-inline-item"><span>⋅</span></li>
      <li class="list-inline-item"><a href="#">Bank</a></li>
      <li class="list-inline-item"><span>⋅</span></li>
      <li class="list-inline-item"><a href="#">Local Finder</a></li>
    </ul>
  </div>
  <router-view/>
  <footer class="bg-light footer">
    <div class="container">
      <div class="row">
        <div class="col-lg-6 text-center text-lg-start my-auto h-100">
          <ul class="list-inline mb-2">
            <li class="list-inline-item"><a href="#">About</a></li>
            <li class="list-inline-item"><span>⋅</span></li>
            <li class="list-inline-item"><a href="#">Contact</a></li>
            <li class="list-inline-item"><span>⋅</span></li>
            <li class="list-inline-item"><a href="#">Terms of Use</a></li>
            <li class="list-inline-item"><span>⋅</span></li>
            <li class="list-inline-item"><a href="#">Privacy Policy</a></li>
          </ul>
          <p class="text-muted small mb-4 mb-lg-0">© Smart City 2022. All Rights Reserved.</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>

export default {
  name: 'App',
  components: {},
  methods: {
    logout() {
      var myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");

      var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow',
        credentials: "include"
      };

      fetch("http://server.it-humke.de:9001/portal/logout", requestOptions)
          .then(response => response.text())
          .then(result => console.log(result))
          .then(() => this.$router.push({
            name: "landingPage"
          }))
          .catch(error => console.log('error', error));
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
