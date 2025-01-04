package com.wemzi.stocksimulator;

import java.awt.GraphicsEnvironment;
import java.io.File;

import javax.swing.JFrame;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.ChartUtils;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
@ComponentScan(basePackages = "com.wemzi.stocksimulator")
public class StockDataApplication implements CommandLineRunner {

    public static void main(String[] args) {
        SpringApplication.run(StockDataApplication.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        RestTemplate restTemplate = new RestTemplate();
        String url = "http://localhost:8000/backend/getstockdata";
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

        if (GraphicsEnvironment.isHeadless()) {
            // Save the chart as an image file instead of displaying it in a JFrame
            ChartUtils.saveChartAsPNG(new File("stock_data_chart.png"), barChart, 800, 600);
        } else {
            // Display the chart in a JFrame
            JFrame frame = new JFrame();
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.add(new ChartPanel(barChart));
            frame.pack();
            frame.setVisible(true);
        }
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
