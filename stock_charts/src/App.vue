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
        { name: 'AAPL', change: 1.5 },
        { name: 'GOOGL', change: -0.8 },
        { name: 'AMZN', change: 2.3 },
        { name: 'MSFT', change: -1.2 },
        { name: 'TSLA', change: 0.5 }
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
            beginAtZero: true
          },
          x: {
            beginAtZero: true
          }
        }
      }
    }
  },
  methods: {
    updateChart() {
      this.chartData = {
        labels: ['12h ago', '6h ago', 'Now'],
        datasets: [{
          label: this.selectedStock.name,
          data: [Math.random() * 10, Math.random() * 10, this.selectedStock.change],
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          fill: true
        }]
      }
    }
  },
  mounted() {
    this.selectedStock = this.stocks[0]
    this.updateChart()
  }
}
</script>
