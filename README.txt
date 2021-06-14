方法
本次作業屬於Time Series Analysis類型，找過幾個方法後決定使用FB所開發的fbprophet framework處理。


Data
1. 電力部分使用「台灣電力公司_過去電力供需資訊」(https://data.gov.tw/dataset/19995)，僅留下日期與備轉容量欄位，其他皆捨去。
2. 額外使用「一年觀測資料-局屬地面測站觀測資料」(https://opendata.cwb.gov.tw/dataset/climate/C-B0024-002)，並依照觀測站位置分為北、中、南、東的氣溫平均值。
3. 由於「一年觀測資料-局屬地面測站觀測資料」為2020/3/16 ~ 2021/3/16，且找不到2020/1/1 ~ 2020/3/15的氣象資料，所以經過merge後的train data為2020/3/16 ~ 2021/1/31的電力和氣象資料。
4. 預測時使用「未來一週天氣預報」，並將最高、最低溫取平均值，東北、東部、東南區域合併。


檔案說明:
1. electricity.csv: 僅留下日期與備轉容量的「台灣電力公司_過去電力供需資訊」。
2. temperature.csv: 整理過的一年觀測資料-局屬地面測站觀測資料。
3. new_temperature.csv: 將whether_forecast.json的資料合併入temperature.csv中。
4. app.py: 主程式。
5. utils.py: 產出new_temperature.csv的輔助程式。


作業使用方式
1. 請先依照env_setup安裝conda環境以及fbprophet套件。
2. 由於需要「未來一週天氣預報」資料，所以請先至https://opendata.cwb.gov.tw/dataset/forecast/F-A0010-001下載json格式，命名為whether_forecast.json並移至作業資料夾中。
3. 執行python utils.py，會將3/23 ~  3/29的資料合併並產出new_temperature.csv檔案。
4. 執行 python app.py 或者 python app.py --training "PATH TO YOUR ELECTRICITY DATA(.csv)" --output "OUTPUT FILE NAME(.csv)"
5. 輸出submission.csv，含3/23 ~ 3/29的備轉容量預測結果。