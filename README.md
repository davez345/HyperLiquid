# Hyperliquid Trading Bot
> HFT Bot Designed for the Hyperliquid Exchange and Focused on Trading Volume

## Installation and Running
#### Note: This program was designed to run inside a Docker container
1. Download latest release `.zip` file or clone the repository to your local machine


2. Rename `example_config.py` to `config.py` and set variables to desired outcomes
    - Note: In each trading iteration, the bot alternates between taking long and short positions. The starting position
      (either long or short) for each iteration is selected randomly. Wallets are indexed, and their positions are determined based
      on this index. Ie. Wallets at even indices (where `i % 2 == 0`) will adopt the starting security position for that iteration where as
      those wallets at odd indices will take the opposite position
      - Ex 1. 3 wallets (in order) where starting security position = L : L S L
      - Ex 2. 3 wallets (in order) where starting security position = S : S L S


3. Ensure you have Docker installed (https://docs.docker.com/get-docker)


4. In the root directory of the hyperliquid-trading project workspace, run the following command:
   ```bash 
   docker-compose run hyperliquid-trading
   ```
   

5. To run the program, run the following command in the default container directory:
   ```bash
   python volume_bot.py
   ```


## Investment Risk Disclaimer
By using this bot, you agree to do so at your own risk. The information and strategies provided through this program are not to be interpreted as investment, trading, or any other type of advice. Performance of the bot is not guaranteed, and past performance is not indicative of future results. Trading cryptocurrencies involves significant risk, including the potential for substantial profit as well as loss.

You are strongly advised to seek professional advice from financial, legal, and tax experts to evaluate the risks and ensure compliance with local laws and regulations before engaging in any trading activities. The bot, its developers, or associated parties shall not be liable for any losses you may incur.

This disclaimer and the bot's functionalities may be modified at any time without notice. Usage of any brand names or trademarks does not imply endorsement. If the bot contains affiliate or third-party links, they are provided for your convenience, and their inclusion does not imply our endorsement or responsibility for their content.