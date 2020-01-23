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
          <q-circular-progress v-else-if="inputFileOk === 'loading'"
            indeterminate size="2em" :thickness="0.2" color="lime" track-color="grey-3"/>
          <q-btn v-else-if="inputFileOk"
            flat size="1em" round color="green" icon="check"/>
          <q-btn v-else
            flat size="1em" round color="orange" icon="warning"/>
          <q-popup-proxy breakpoint=0>
            <q-banner v-if="inputFileOk === true">
              Input File: <a href="#">{{getFileNameFromPath(inputFilePath)}}</a>
            </q-banner>
            <q-banner v-else>
              <template v-slot:avatar>
                <q-icon name="description" color="primary" />
              </template>
              Select a model input file or drag-and-drop.
            </q-banner>
          </q-popup-proxy>
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
          <q-circular-progress v-else-if="modelFileOk === 'loading'"
            indeterminate size="2em" :thickness="0.2" color="lime" track-color="grey-3"/>
          <q-btn v-else-if="modelFileOk"
            flat size="1em" round color="green" icon="check"/>
          <q-btn v-else
            flat size="1em" round color="orange" icon="warning"/>
          <q-popup-proxy breakpoint=0>
            <q-banner v-if="modelFileOk === true">
              Model File: <a href="#">{{getFileNameFromPath(modelFilePath)}}</a>
            </q-banner>
            <q-banner v-else>
              <template v-slot:avatar>
                <q-icon name="description" color="primary" />
              </template>
              Select a Twin model file or drag-and-drop.
            </q-banner>
          </q-popup-proxy>
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
      <div v-if="outputFilePath">
        Result CSV: <a href="#">{{getFileNameFromPath(outputFilePath)}}</a>
      </div>
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
      outputFilePath: '',
      inputFileOk: 'intermediate',
      modelFileOk: 'intermediate',
      isLoading: false,
      backendMessage: 'Ready'
    }
  },
  computed: {
    // a computed getter

  },
  methods: {
    getFileNameFromPath: function (s) {
      return s.split('\\').join('/').split('/').splice(-1)[0]
    },
    showWarning: function (msg) {
      this.$q.notify({
        color: 'warning',
        message: msg,
        icon: 'warning',
        actions: [{ icon: 'close', color: 'white' }]
      })
    },
    resetSimulationStatus: function () {
      this.outputFilePath = ''
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
        self.outputFilePath = response.simulation_output_file
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
      const self = this
      let ret = dialog.showOpenDialogSync({
        properties: ['openFile'],
        filters: [
          { name: 'Twin Model', extensions: ['twin'] },
          { name: 'All Files', extensions: ['*'] }
        ]
      })
      if (ret !== undefined) {
        this.modelFilePath = ret[0]
        this.resetSimulationStatus()
        this.modelFileOk = 'loading'
        twinClient.CheckFileTwin({ file_path: this.modelFilePath }, (err, response) => {
          if (err || !response.is_success) {
            self.showWarning('Load Model Failed')
          }
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
        this.resetSimulationStatus()
        this.inputFileOk = 'loading'
        twinClient.CheckFileInputCSV({ file_path: this.inputFilePath }, (err, response) => {
          if (err || !response.is_success) {
            self.showWarning('Load Input Failed')
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
