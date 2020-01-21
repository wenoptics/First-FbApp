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
          @click="openInputFile"
        />
        <div class="status-container">
          <q-btn v-if="inputFileOk === 'intermediate'"
            flat size="1em" round color="grey" icon="warning"/>
          <q-btn v-else-if="inputFileOk"
            flat size="1em" round color="green" icon="check"/>
          <q-btn v-else
            flat size="1em" round color="orange" icon="warning"/>
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
          @click="openTwinFile"
        />
        <div class="status-container">
          <q-btn v-if="modelFileOk === 'intermediate'"
            flat size="1em" round color="grey" icon="warning"/>
          <q-btn v-else-if="modelFileOk"
            flat size="1em" round color="green" icon="check"/>
          <q-btn v-else
            flat size="1em" round color="orange" icon="warning"/>
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
        @click="trySimulation"
      />
    </div>
  </q-page>
</template>

<script>
import path from 'path'
const { dialog } = require('electron').remote
const grpc = window.grpc // const grpc = require('grpc')
const PROTO_PATH = path.join(__statics, '/protos/twindemo.proto')

// use dynamic proto loading, consider changing to static (compiled) for performance?
// let protoLoader = require('@grpc/proto-loader')
const twinProto = grpc.load(PROTO_PATH).twindemo
let twinClient

const connectBackend = function () {
  twinClient = new twinProto.Twin(
    'localhost:50051',
    grpc.credentials.createInsecure())
}

export default {
  name: 'PageIndex',
  data: function () {
    return {
      inputFilePath: '',
      modelFilePath: '',
      inputFileOk: 'intermediate',
      modelFileOk: 'intermediate',
      isLoading: false
    }
  },
  methods: {
    showWarning: function (msg) {
      this.$q.notify({
        color: 'warning',
        message: msg,
        icon: 'warning',
        actions: [{ icon: 'close', color: 'white' }]
      })
    },
    SimulateBatchCSV: function (modelFile, inputFile) {
      const self = this
      this.$q.loading.show()
      twinClient.SimulateBatchCSV({
        model_file_path: modelFile,
        input_file_path: inputFile
      }, function (err, response) {
        self.$q.loading.hide()

        if (err || !response.is_success) {
          if (response) {
            self.showWarning('Simulation Failed: ' + response.message)
          } else {
            console.log(err.stack)
            self.showWarning('Simulation Failed: ' + err)
          }
          return
        }
        console.log('SimulateBatchCSV',
          'Simulation ok:', response.is_success,
          response.message
        )
      })
    },
    trySimulation: function () {
      if (!(this.inputFileOk === true && this.modelFileOk === true)) {
        let message = this.inputFileOk !== true ? ' input' : ''
        this.showWarning(`Model ${message} file is not specified.`)
        return
      }
      this.SimulateBatchCSV(this.modelFilePath, this.inputFilePath)
    },
    openTwinFile: function () {
      let ret = dialog.showOpenDialogSync({
        properties: ['openFile'],
        filters: [
          { name: 'Twin Model', extensions: ['twin'] },
          { name: 'All Files', extensions: ['*'] }
        ]
      })
      if (ret !== undefined) {
        this.modelFilePath = ret[0]
        twinClient.CheckFileTwin({ file_path: this.modelFilePath }, (err, response) => {
          if (err) {}
          this.modelFileOk = response.is_success
        })
      }
    },
    openInputFile: function () {
      let ret = dialog.showOpenDialogSync({
        properties: ['openFile'],
        filters: [
          { name: 'Twin Input File', extensions: ['csv'] },
          { name: 'All Files', extensions: ['*'] }
        ]
      })
      if (ret !== undefined) {
        this.inputFilePath = ret[0]
        twinClient.CheckFileInputCSV({ file_path: this.inputFilePath }, (err, response) => {
          if (err || !response.is_success) {
          }
          this.inputFileOk = response.is_success
        })
      }
    }
  },
  mounted: function () {
    connectBackend()
    this.$nextTick(function () {
      // Code that will run only after the
      // entire view has been rendered
    })
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
