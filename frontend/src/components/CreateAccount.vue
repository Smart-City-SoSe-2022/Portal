<template>
  <header class="text-center masthead">
    <section class="position-relative py-4 py-xl-5">
      <div class="container">
        <div class="row mb-5">
          <div class="col-md-8 col-xl-6 text-center mx-auto">
            <h2>Registrierung</h2>
            <p class="w-lg-50">
              Um den Smart City Service nutzen zu können, müssen Sie sich registrieren.
            </p>
          </div>
        </div>
        <div class="row d-flex justify-content-center">
          <div class="col-md-6 col-xl-4">
            <div class="card mb-5">
              <div class="card-body d-flex flex-column align-items-center">
                <div class="bs-icon-xl bs-icon-circle bs-icon-primary bs-icon my-4">
                  <svg class="bi bi-person" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"
                       fill="currentColor" viewBox="0 0 16 16">
                    <path
                        d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"></path>
                  </svg>
                </div>
                <form class="text-center" method="post" @submit.prevent="createAccount">
                  <div class="mb-3">
                    <input class="form-control" type="text" name="forename" placeholder="Vorname" v-model="forename"/>
                  </div>
                  <div class="mb-3">
                    <input class="form-control" type="text" name="lastname" placeholder="Nachname" v-model="lastname"/>
                  </div>
                  <div class="mb-3">
                    <input class="form-control" type="text" name="gender" placeholder="Geschlecht" v-model="gender"/>
                  </div>
                  <div class="mb-3">
                    <input class="form-control" type="text" name="address" placeholder="Straße" v-model="address"/>
                  </div>
                  <div class="mb-3">
                    <input class="form-control" type="number" name="plz" placeholder="PLZ" v-model="plz"/>
                  </div>
                  <div class="mb-3">
                    <input class="form-control" type="email" name="email" placeholder="Email" v-model="email"/>
                  </div>
                  <div class="mb-3">
                    <input class="form-control" type="password" name="password"
                           placeholder="Password" v-model="password"/>
                  </div>
                  <div class="mb-3">
                    <button class="btn btn-primary d-block w-100" type="submit">Bestätigen</button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </header>
</template>

<script>
export default {
  name: "CreateAccount",

  data() {
    return {
      forename: null,
      lastname: null,
      gender: null,
      address: null,
      plz: null,
      email: null,
      password: null
    }
  },
  methods: {
    createAccount() {
      var myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");

      var raw = JSON.stringify({
        "forename": this.forename,
        "lastname": this.lastname,
        "gender": this.gender,
        "address": this.address,
        "plz": this.plz,
        "email": this.email,
        "password": this.password
      });

      var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow',
        credentials: "include"
      };

      fetch("http://server.it-humke.de:9001/portal/create", requestOptions)
          .then(response => response.text())
          .then(result => console.log(result))
          .then(() => this.$router.push({
            name: "landingPage"
          }))
          .catch(error => console.log('error', error));
    },
    sendMessage() {
      if (!this.message) {
        this.error = "Bitte eine Nachricht eingeben"
      } else {
        var routing_key = this.routing_key
        if (!routing_key) {
          routing_key = '*.#'
        }

        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        var raw = JSON.stringify({
          "routing_key": routing_key,
          "message": this.message
        });

        var requestOptions = {
          method: 'POST',
          headers: myHeaders,
          body: raw,
          redirect: 'follow',
          credentials: "include"
        };

        fetch("http://server.it-humke.de:9001/portal/message", requestOptions)
            .then(response => response.text())
            .then(result => console.log(result))
            .then(() => this.$router.push({
              name: "helloWorld"
            }))
            .catch(error => console.log('error', error));
      }
    }
  }
}
</script>

<style scoped>

</style>