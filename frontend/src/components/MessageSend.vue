<template>
  <div class="container mt-4">
    <form @submit.prevent="sendMessage">
      <input
          rows="10"
          class="form-control"
          placeholder="Gebe hier den Routing Key für RabbitMQ an (Standard ist *.#)"
          v-model="routing_key"
      />
      <br/>

      <textarea
          rows="10"
          class="form-control"
          placeholder="Gebe hier die Nachricht für RabbitMQ ein"
          v-model="message"
      >
      </textarea>

      <button class="btn btn-success mt-4">Nachricht senden</button>
    </form>
    <div
        v-if="error"
        class="alert alert-warning alert-dismissible fade show mt-5"
        role="alert"
    >
      <strong>{{ error }}</strong>
    </div>
  </div>
</template>

<script>
export default {
  name: "MessageSend",

  data() {
    return {
      routing_key: null,
      message: null,
      error: null
    }
  },
  methods: {
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
          redirect: 'follow'
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