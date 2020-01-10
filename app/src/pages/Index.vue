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
        />
        <div class="status-container">
          <q-btn flat size="1em" round color="grey" icon="warning"/>
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
          <q-btn flat size="1em" round color="grey" icon="warning" />
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
export default {
  name: 'PageIndex'
}
</script>

<style lang="scss">
  .vl-2 {
    border-left: 1px solid $dark;
    height: 2em;
  }

  .vl-dash {
    border-left-style: dashed
  }

  .dash-btn.q-btn--outline .q-btn__wrapper:before {
    border-style: dashed
  }

  .status-row {
    position: relative;
  }

  .status-container {
    position: absolute;
    top: calc( 50% - 1.4em);
    left: -3.5em
  }
</style>
