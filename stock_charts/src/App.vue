<template>
  <div id="app">
    <h1 class="title">Stock Tracker</h1>
    <div class="container">
      <div class="stock-list">
        <div
          v-for="stock in stocks"
          :key="stock.stock_name"
          :style="{ color: stock.percentage_change > 0 ? 'green' : 'red', cursor: 'pointer', border: selectedStock === stock ? '2px solid blue' : 'none', padding: '5px', marginBottom: '5px' }"
          @click="fetchStockValues(stock)"
        >
          {{ stock.stock_name }}: {{ stock.percentage_change }}%
        </div>
      </div>
      <div class="chart-container">
        <StockChart :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script>
import StockChart from './components/StockChart.vue'
import api from './api/api.js'
import { format } from 'date-fns'

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
        responsive: true,
        maintainAspectRatio: false,
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
            type: 'time',
            time: {
              unit: 'day',
              tooltipFormat: 'MMM d, h:mm a',
              displayFormats: {
                day: 'MMM d'
              }
            }
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
    updateChart(values) {
      if (this.selectedStock && values) {
        // Get the last 10 entries
        const recentValues = values.slice(-10)
        const allValues = recentValues.map(value => value.value)
        this.chartOptions.scales.y.min = Math.min(...allValues) - 1
        this.chartOptions.scales.y.max = Math.max(...allValues) + 1

        this.chartData = {
          labels: recentValues.map(value => format(new Date(value.timestamp), 'MMM d, h:mm a')),
          datasets: [{
            label: this.selectedStock.stock_name,
            data: recentValues.map(value => value.value),
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
          stock_values: (stock.stock_values || []).sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
        }))
        this.selectedStock = this.stocks[0]
        this.fetchStockValues(this.selectedStock)
      }).catch(error => {
        console.error('There was an error!', error)
      })
    },
    fetchStockValues(stock) {
      if (!stock) return
      this.selectedStock = stock
      api.getStockValues(stock.id).then(response => {
        const values = response.data.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
        this.updateChart(values)
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

<style scoped>
.title {
  white-space: nowrap; /* Prevent the title from breaking into two lines */
  text-align: center;
  width: 100%;
  margin: 0;
}

.container {
  display: flex;
  height: 100vh; /* Ensure the container takes full viewport height */
}

.stock-list {
  width: 20vh; /* Adjust the width based on viewport height */
  overflow-y: auto; /* Enable scrolling if the list is too long */
  padding: 10px;
  border-right: 1px solid #ccc;
}

.chart-container {
  flex-grow: 1; /* Take up remaining space */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  overflow: hidden;
  height: 100%; /* Ensure the chart-container takes full height */
  max-width: calc(100vw - 20vh); /* Adjust the max width based on the stock-list width */
}

.chart-container > * {
  width: 90vh; /* Make the chart take full available width */
  height: 90vh; /* Make the chart take full available height */
  max-height: 90vh; /* Limit the chart's maximum height */
  position: relative; /* Position relative to contain absolutely positioned elements */
}
</style>
