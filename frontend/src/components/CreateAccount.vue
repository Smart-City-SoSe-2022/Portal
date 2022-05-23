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
                <form class="text-center" method="post">
                  <div class="mb-3"><input class="form-control" type="text" name="forename" placeholder="Vorname"/>
                  </div>
                  <div class="mb-3"><input class="form-control" type="text" name="lastname" placeholder="Nachname"/>
                  </div>
                  <div class="mb-3"><input class="form-control" type="text" name="gender" placeholder="Geschlecht"/>
                  </div>
                  <div class="mb-3"><input class="form-control" type="text" name="address" placeholder="Straße"/>
                  </div>
                  <div class="mb-3"><input class="form-control" type="number" name="plz" placeholder="PLZ"/></div>
                  <div class="mb-3"><input class="form-control" type="email" name="email" placeholder="Email"/></div>
                  <div class="mb-3"><input class="form-control" type="password" name="password"
                                           placeholder="Password"/></div>
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
      routing_key: null,
      message: null,
      error: null
    }
  },
  methods: {
    createAccount() {

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
          redirect: 'follow'
        };

        fetch("http://localhost:5000/message", requestOptions)
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