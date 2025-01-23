<template>
  <div>
    <canvas id="stock-chart"></canvas>
    <h1> hello </h1>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart } from 'chart.js'

export default {
  extends: Line,
  props: ['data', 'options'],
  mounted() {
    this.renderChart(this.data, this.options)
  }
  
}
</script>

