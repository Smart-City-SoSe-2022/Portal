<template>
  <div class="container">
    <div class="row d-flex justify-content-center">
      <div class="col-md-6 col-xl-4">
        <div class="card mb-5">
          <div class="card-body d-flex flex-column align-items-center">
            <form class="text-center" method="post" @submit.prevent="updateAccount">
              <div class="mb-3">Vorname: <input type="text" v-model="user.forename" name="user.forename"></div>
              <div class="mb-3">Nachname: <input type="text" v-model="user.lastname" name="user.lastname"></div>
              <div class="mb-3">Geschlecht: <input type="text" v-model="user.gender" name="user.gender"></div>
              <div class="mb-3">Adresse: <input type="text" v-model="user.address" name="user.address"></div>
              <div class="mb-3">PLZ: <input type="number" v-model="user.plz" name="user.plz"></div>
              <div class="mb-3">Email: <input type="text" v-model="user.email" name="user.email"></div>
              <div class="mb-3">Password: <input type="password" v-model="user.password" name="user.password"></div>

              <div class="mb-3">
                <button class="btn btn-primary d-block w-100" type="submit">Accountinformationen aktualisieren</button>
              </div>
            </form>

            <div class="mb-3">
              <button class="btn btn-primary d-block w-100" id="deleteAccountButton" @click="deleteAccount">Account löschen</button>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "accountDetails",
  data() {
    return {
      user: {}
    }
  },
  methods: {
    getAccountDetails() {
      var myHeaders = new Headers();

      var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow',
        credentials: "include"
      };

      fetch("http://server.it-humke.de:9001/portal/get", requestOptions)
          .then(response => response.json())
          .then(result => {
            console.log(result)
            this.user = result
          })
          .catch(error => console.log('error', error));
    },

    updateAccount() {
      var myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");

      var raw = JSON.stringify({
        "forename": this.user.forename,
        "lastname": this.user.lastname,
        "gender": this.user.gender,
        "address": this.user.address,
        "plz": this.user.plz,
        "email": this.user.email,
        "password": this.user.password
      });

      var requestOptions = {
        method: 'PUT',
        headers: myHeaders,
        body: raw,
        redirect: 'follow',
        credentials: "include"
      };

      fetch("http://server.it-humke.de:9001/portal/update", requestOptions)
          .then(response => response.text())
          .then(result => console.log(result))
          .then(() => this.$router.push({
            name: "accountDetails"
          }))
          .catch(error => console.log('error', error));
    },

    deleteAccount() {
      var myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");

      var requestOptions = {
        method: 'DELETE',
        headers: myHeaders,
        redirect: 'follow',
        credentials: "include"
      };

      fetch("http://server.it-humke.de:9001/portal/delete", requestOptions)
          .then(response => response.text())
          .then(result => console.log(result))
          .then(() => this.$router.push({
            name: "landingPage"
          }))
          .catch(error => console.log('error', error));
    }
  },
  created() {
    this.getAccountDetails()
  }
}
</script>

<style scoped>
#deleteAccountButton {
  background: red;
}
</style>
