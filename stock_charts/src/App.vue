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

export default {
  components: {
    StockChart
  },
  data() {
    return {
      stocks: [
        { name: 'AAPL', change: 2.6, values: [1.5, 2.0, 2.5, 1.8, 1.7, 2.3, 2.1, 1.9, 2.4, 2.6] },
        { name: 'GOOGL', change: -0.4, values: [-0.8, -0.6, -0.7, -0.9, -1.0, -0.8, -0.7, -0.6, -0.5, -0.4] },
        { name: 'AMZN', change: 2.3, values: [2.3, 2.1, 2.4, 2.6, 2.7, 2.5, 2.8, 2.9, 2.4, 2.3] },
        { name: 'MSFT', change: -0.8, values: [-1.2, -1.0, -1.1, -1.3, -1.4, -1.2, -1.1, -1.0, -0.9, -0.8] },
        { name: 'TSLA', change: 0.3, values: [0.5, 0.6, 0.4, 0.3, 0.5, 0.7, 0.6, 0.5, 0.4, 0.3] }
      ],
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
      const allValues = this.stocks.flatMap(stock => stock.values);
      this.chartOptions.scales.y.min = Math.min(...allValues) - 1;
      this.chartOptions.scales.y.max = Math.max(...allValues) + 1;

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
  mounted() {
    this.selectedStock = this.stocks[0]
    this.updateChart()
  }
}
</script>
