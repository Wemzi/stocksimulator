<template>
  <div>
    <canvas ref="canvas"></canvas>
    <h1> hello </h1>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  extends: Line,
  props: ['data', 'options'],
  mounted() {
    this.renderChart()
  },
  methods: {
    renderChart() {
      new Chart(this.$refs.canvas, {
        type: 'line',
        data: this.data,
        options: {
          ...this.options,
          scales: {
            y: {
              beginAtZero: true
            },
            x: {
              beginAtZero: true
            }
          }
        }
      })
    }
  }
}
</script>
