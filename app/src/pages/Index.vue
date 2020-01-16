<template>
  <q-page class="flex flex-center">
    <div class="fit column wrap justify-center items-center content-center">

      <div class="status-row">
        <q-btn
          size="1.2em"
          color="secondary"
          text-color="dark"
          class="q-px-xl q-py-xs"
          label="Input"
          outline
          @click="startClient"
        />
        <div class="status-container">
          <q-btn
            flat
            size="1em"
            round
            color="grey"
            icon="warning"
          />
        </div>
      </div>
      <div class="vl-2"></div>

      <div class="status-row">
        <q-btn
          size="1.2em"
          class="q-px-xl q-py-xl"
          color="secondary"
          text-color="dark"
          label="Twin Model"
          outline
        />
        <div class="status-container">
          <q-btn
            flat
            size="1em"
            round
            color="grey"
            icon="warning"
          />
        </div>
      </div>

      <div class="vl-2 vl-dash"></div>
      <q-btn
        size="1.2em"
        color="secondary"
        text-color="dark"
        class="q-px-xl q-py-xs dash-btn"
        label="Output"
        outline
      />
    </div>
  </q-page>
</template>

<script>
import path from 'path'
const grpc = window.grpc // const grpc = require('grpc')
const PROTO_PATH = path.join(__statics, '/protos/helloworld.proto')

// use dynamic proto loading, consider changing to static (compiled) for performance?
// let protoLoader = require('@grpc/proto-loader')
const helloProto = grpc.load(PROTO_PATH).helloworld

export default {
  name: 'PageIndex',
  methods: {
    sayHello: function (call, callback) {
      callback(null, { message: 'Hello ' + call.request.name + ', from Electron' })
    },
    startServer: function () {
      const server = new grpc.Server()
      server.addService(helloProto.Greeter.service, { sayHello: this.sayHello })
      server.bind('0.0.0.0:50051', grpc.ServerCredentials.createInsecure())
      server.start()
      console.log('server started', server)
    },
    startClient: function () {
      var client = new helloProto.Greeter(
        'localhost:50051',
        grpc.credentials.createInsecure())
      client.sayHello(
        { name: 'FBapp-node' },
        function (err, response) {
          if (err) {
            console.log(err.stack)
          }
          console.log('Greeting:', response.message)
        })
    }
  }
}
</script>

<style lang="scss">
.vl-2 {
  border-left: 1px solid $dark;
  height: 2em;
}

.vl-dash {
  border-left-style: dashed;
}

.dash-btn.q-btn--outline .q-btn__wrapper:before {
  border-style: dashed;
}

.status-row {
  position: relative;
}

.status-container {
  position: absolute;
  top: calc(50% - 1.4em);
  left: -3.5em;
}
</style>
