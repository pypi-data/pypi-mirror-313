# Introduction
Data tools to increase productivity in your workflow

# How to setup
Install with pip:
```
pip install core_pro
```

Copy your client_secret.json to use Google Sheet API. If you don't have the error will raise
[Link tutorial](https://developers.google.com/slides/api/quickstart/python)
```
Please copy your json to the folder with name: 'client_secret.json'
```

If you don't have any python environment, please create your environment with conda
```
conda create -n <your_name> python=3.11 -y && conda activate <your_name>
```

Setup Big Data Account in environment
- Setup in windows
[Link tutorial](https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html#GUID-DD6F9982-60D5-48F6-8270-A27EC53807D0)
```
Set variable **PRESTO_USER** with **Account** on RAM
Set variable **PRESTO_PASSWORD** with **Account Password** on RAM
```

# How to use our power toys
- Query with JDBC - [Notebook](https://git.garena.com/xuankhang.do/how-to-use/-/blob/master/query_jdbc.ipynb)
- Working with Google Sheets - [Notebook](https://git.garena.com/xuankhang.do/how-to-use/-/blob/master/gsheet.ipynb)
- Working with Google Slide
- Working with Google Drive
- Working with Gmail
- Working with AWS Storage - [Notebook](https://git.garena.com/xuankhang.do/how-to-use/-/blob/master/aws.ipynb)
- Working with Google Cloud Storage
