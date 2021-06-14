import argparse
from fbprophet import Prophet
import pandas as pd
from matplotlib import pyplot

parser = argparse.ArgumentParser()
parser.add_argument('--training', 
                        default='electricity.csv',
                        help='PATH TO YOUR ELECTRICITY DATA(.csv)')
parser.add_argument('--output', 
                        default='submission.csv',
                        help='OUTPUT FILE NAME(.csv)')
args = parser.parse_args()


ele_csv = pd.read_csv(args.training)
ele_csv['ds'] = pd.to_datetime(ele_csv['ds'], format='%Y%m%d')

tmp_csv = pd.read_csv('new_temperature.csv')
tmp_csv['ds'] = pd.to_datetime(tmp_csv['ds'], format='%Y%m%d')
df = pd.merge(ele_csv, tmp_csv, on="ds")
df_train = df.loc[df["ds"]<="2021-01-31"]
df_test  = df.loc[df["ds"]>="2021-03-23"]

model = Prophet(changepoints=['2021-01-31'])
model.add_regressor('North')
model.add_regressor('Mid')
model.add_regressor('South')
model.add_regressor('East')
model.fit(df_train)

pred = model.predict(df_test.drop(columns='y'))
output = pred[['ds', 'yhat']]
output.columns = ['date','operating_reserve(MW)']
output.to_csv(args.output, index=False)
