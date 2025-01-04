package com.wemzi.stocksimulator;

import java.io.File;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtils;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class ChartConfig {

    @Bean
    public JFreeChart generateChart() throws Exception {
        RestTemplate restTemplate = new RestTemplate();
        String url = "http://localhost:8000/backend/updatestockdata";
        Stock[] stocks = restTemplate.getForObject(url, Stock[].class);

        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        for (Stock stock : stocks) {
            dataset.addValue(stock.getValue(), "Current Value", stock.getSymbol());
            dataset.addValue(stock.getHigh52w(), "52-Week High", stock.getSymbol());
            dataset.addValue(stock.getLow52w(), "52-Week Low", stock.getSymbol());
        }

        JFreeChart barChart = ChartFactory.createBarChart(
                "Stock Data",
                "Stock Symbol",
                "Value",
                dataset,
                PlotOrientation.VERTICAL,
                true, true, false);

        // Create the directory if it doesn't exist
        File directory = new File("src/main/resources/static");
        if (!directory.exists()) {
            directory.mkdirs();
        }

        // Save the chart as an image file
        ChartUtils.saveChartAsPNG(new File("src/main/resources/static/stock_data_chart.png"), barChart, 800, 600);

        return barChart;
    }

    static class Stock {
        private String symbol;
        private double value;
        private double change24h;
        private double high52w;
        private double low52w;

        // Getters and setters

        public String getSymbol() {
            return symbol;
        }

        public void setSymbol(String symbol) {
            this.symbol = symbol;
        }

        public double getValue() {
            return value;
        }

        public void setValue(double value) {
            this.value = value;
        }

        public double getChange24h() {
            return change24h;
        }

        public void setChange24h(double change24h) {
            this.change24h = change24h;
        }

        public double getHigh52w() {
            return high52w;
        }

        public void setHigh52w(double high52w) {
            this.high52w = high52w;
        }

        public double getLow52w() {
            return low52w;
        }

        public void setLow52w(double low52w) {
            this.low52w = low52w;
        }
    }
}
