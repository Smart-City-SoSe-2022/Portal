<template>
  <div>
    <p>Name: {{ user.forename }} {{ user.lastname }}</p>
    <p>Geschlecht: {{ user.gender }}</p>
    <p>Adresse: {{ user.address }}</p>
    <p>PLZ: {{ user.plz }}</p>
    <p>Email: {{ user.email }}</p>
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

      fetch("http://localhost:5000/portal/get", requestOptions)
          .then(response => response.json())
          .then(result => {
            console.log(result)
            this.user = result
          })
          .catch(error => console.log('error', error));
    }
  },
  created() {
    this.getAccountDetails()
  }
}
</script>

<style scoped>

</style>