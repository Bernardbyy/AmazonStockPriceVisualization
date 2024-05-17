<img src="https://github.com/Bernardbyy/AmazonStockPriceVisualization/assets/75737130/b91c64ce-73fb-4189-b0f5-2e3152bccb1a" alt="Image 1" width="300" height="300">
<img src="https://github.com/Bernardbyy/AmazonStockPriceVisualization/assets/75737130/b6105f67-a284-4ffe-b066-513a82616770" alt="Image 2" width="300" height="300">



# Amazon Stock Price Visualization 📈🚀📉💸
A Real Time Data Streaming Project using:<br> 
(1) **Kafka Messaging Systems** to send real-time data for topic <br> 
(2) **Spark Structured Streaming** for Stream Processing <br> 
(3) **Flask Web Server** to handle backend to frontend Visualization<br>
(4) **Chart.js** to render real-time visualizations of stock data<br> 

Full Demo On: [Real-Time Amazon Stock Price Visualization w/ Notified Upper and Lower Limits](https://drive.google.com/file/d/16zkV1kaSEBXrfBr7UMDQE0HGE0yTcN_M/view?usp=sharing)

## Kafka (Producer) and Spark Structured Streaming (Consumer)
### (1) Producer: <br>
![image](https://github.com/Bernardbyy/AmazonStockPriceVisualization/assets/75737130/c806e586-5529-4edf-b47a-15cebad2a5b9)


### (2) Consumer: <br>
Submit Spark Job with Specified Arguments of 170 (Upper Limit) and 160 (Lower Limit):<br>
![image](https://github.com/Bernardbyy/AmazonStockPriceVisualization/assets/75737130/e663e162-062a-46ad-95f6-5400f3aecf66)

Flag Turned onto 1 as Actual "price" > Upper Limit Specified:<br>
![image](https://github.com/Bernardbyy/AmazonStockPriceVisualization/assets/75737130/9cca453e-82c3-48c8-b68c-2143ab20e3af)


### (3) Visualization: <br>
Real-Time Amazon Stock Price Line Chart w/ 50-day moving average and Summary Table with Green Records (Notification of price surpassing upper limit)<br>
![image](https://github.com/Bernardbyy/AmazonStockPriceVisualization/assets/75737130/650e5d05-8ad3-4531-a154-96f71536e7a0)


