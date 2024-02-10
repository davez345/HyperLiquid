FROM python:3.10.1

WORKDIR /usr/local/hyperliquid-trading

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash"]