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
    this.renderChart(this.data, this.options)
  },
  methods: {
    renderChart(data, options) {
      console.log(data)
      if (this.chart) {
        this.chart.destroy()
      }
      this.chart = new Chart(this.$refs.canvas, {
        type: 'line',
        data: data,
        options: {
          ...options,
          scales: {
            y: {
              beginAtZero: true
            },
            x: {
              beginAtZero: true
            }
          },
          elements: {
            line: {
              borderColor: 'blue',
              borderWidth: 2
            }
          }
        }
      })
    }
  },
  watch: {
    data: {
      handler(newData) {
        this.renderChart(newData, this.options)
      },
      deep: true
    },
    options: {
      handler(newOptions) {
        this.renderChart(this.data, newOptions)
      },
      deep: true
    }
  }
}
</script>
