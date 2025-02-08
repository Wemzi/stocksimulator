<template>
  <div id="app">
    <h1>Stock Tracker</h1>
    <div>
      <label for="stock-select">Select a stock:</label>
      <select id="stock-select" v-model="selectedStock" @change="updateChart">
        <option v-for="stock in stocks" :key="stock.name" :value="stock">{{ stock.name }}</option>
      </select>
    </div>
    <div v-for="stock in stocks" :key="stock.name">
      <p :style="{ color: stock.change > 0 ? 'green' : 'red' }">
        {{ stock.name }}: {{ stock.change }}%
      </p>
    </div>
    <StockChart :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import StockChart from './components/StockChart.vue'
import api from './api/api.js'

export default {
  components: {
    StockChart
  },
  data() {
    return {
      stocks: [],
      selectedStock: null,
      chartData: {},
      chartOptions: {
        animation: {
          duration: 2000,
          easing: 'easeInOutBounce'
        },
        scales: {
          y: {
            beginAtZero: true,
            min: null,
            max: null
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
    }
  },
  methods: {
    updateChart() {
      if (this.selectedStock) {
        const allValues = this.stocks.flatMap(stock => stock.values)
        this.chartOptions.scales.y.min = Math.min(...allValues) - 1
        this.chartOptions.scales.y.max = Math.max(...allValues) + 1

        this.chartData = {
          labels: ['Value 1', 'Value 2', 'Value 3', 'Value 4', 'Value 5', 'Value 6', 'Value 7', 'Value 8', 'Value 9', 'Value 10'],
          datasets: [{
            label: this.selectedStock.name,
            data: this.selectedStock.values,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            fill: false
          }]
        }

        // Print the dataset to the console
        console.log('Chart Dataset:', this.chartData)
      }
    },
    fetchStocks() {
      api.getStocks().then(response => {
        this.stocks = response.data.map(stock => ({
          ...stock,
          values: stock.values.split(',').map(value => parseFloat(value.trim()))
        }))
        this.selectedStock = this.stocks[0]
        this.updateChart()
      }).catch(error => {
        console.error('There was an error!', error)
      })
    }
  },
  mounted() {
    this.fetchStocks()
  }
}
</script>
