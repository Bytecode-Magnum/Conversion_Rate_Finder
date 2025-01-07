import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

api_key = os.getenv('api_key')


def to_excel(dataframe):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    dataframe.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


@st.dialog("Calculating")
def calculate_currency():
    try:
        with st.spinner("Please Wait....."):
            # Fetch selected currencies and target currency
            currency_list = [all_currencies.get(each).strip() for each in st.session_state.base_currency]
            currencies = ",".join(currency_list)  # to currency
            source = all_currencies.get(st.session_state.target_currency)  # from currency
            start_date = st.session_state.start_date
            end_date = st.session_state.end_date

            # Determine conversion type: Average or Daily
            if st.session_state.conversion_type == 'Average':
                # Construct API URL for Average Rate
                base_url = (
                    f"https://api.currencylayer.com/timeframe?"
                    f"access_key={api_key}&start_date={start_date}&end_date={end_date}&source={source}&currencies={currencies}"
                )
                response = requests.get(base_url)
                result = response.json().get("quotes")
                df = pd.DataFrame.from_records(result).transpose()
                df.index.name = 'Date'
                for each in df.columns:
                    if len(df.columns) != 1:
                        df.loc[df.index[0], each] = 1 / df[each].mean()
                    else:
                        df.loc[df.index[0], each] = 1 / df[each].mean()
                df = df[0:1]
                time = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
                path = f'./{source}_Currency_Rate_{start_date}_{end_date}_{time}.csv'
                st.success(f"Daily Conversion Rate Calculated and Saved In File {os.path.basename(path)}")
                csv = df.to_csv().encode("utf-8")
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=os.path.basename(path),
                    mime="text/csv",
                )

            elif st.session_state.conversion_type == 'Daily':
                # Construct API URL for Daily Rate
                url = (
                    f"https://api.currencylayer.com/timeframe?"
                    f"access_key={api_key}&start_date={start_date}&end_date={end_date}&source={source}&currencies={currencies}"
                )
                response = requests.get(url)
                result = response.json().get('quotes')
                # Convert response to DataFrame
                df = pd.DataFrame.from_records(result).transpose()
                df.index.name = 'Date'
                time = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
                for each in df.columns:
                    df[each] = 1 / df[each]
                path = f'./{source}_Currency_Rate_{start_date}_{end_date}_{time}.csv'
                st.success(f"Daily Conversion Rate Calculated and Saved In File {os.path.basename(path)}")
                csv = df.to_csv().encode("utf-8")
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=os.path.basename(path),
                    mime="text/csv",
                )

            elif st.session_state.conversion_type == 'Monthly':
                # Construct API URL for Daily Rate
                url = (
                    f"https://api.currencylayer.com/timeframe?"
                    f"access_key={api_key}&start_date={start_date}&end_date={end_date}&source={source}&currencies={currencies}"
                )
                response = requests.get(url)
                result = response.json().get('quotes')

                # Convert response to DataFrame
                df = pd.DataFrame.from_records(result).transpose()
                df.index.name = 'Date'
                df.index = pd.to_datetime(df.index)
                df = df.resample("ME").mean()
                for each in df.columns:
                    df[each] = 1 / df[each].mean()
                time = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
                path = f'./{source}_Currency_Rate_{start_date}_{end_date}_{time}.csv'
                st.success(f"Daily Conversion Rate Calculated and Saved In File {os.path.basename(path)}")
                csv = df.to_csv().encode("utf-8")
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=os.path.basename(path),
                    mime="text/csv",
                )

    except Exception as e:
        st.warning(f"An error occurred: {e}")


st.set_page_config(layout='wide', page_title='Currency Conversion Rate')
st.markdown('<h3><strong>Hi<strong>, We Help you to get the Daily and Average Conversion Rate \
             for All Currencies !!</h3>', unsafe_allow_html=True)

tabs = st.tabs(["Instructions", "Average Conversion Rate"])
if 'target_currency' not in st.session_state:
    st.session_state.target_currency = None
if 'base_currency' not in st.session_state:
    st.session_state.base_currency = None
if 'start_date' not in st.session_state:
    st.session_state.start_date = None
if 'end_date' not in st.session_state:
    st.session_state.end_date = None
if 'conversion_type' not in st.session_state:
    st.session_state.conversion_type = None

select_box_custom_css = """<style>
                        div[data-testid="stSelectbox"] * {
                        color: #ffff !important;
                        weight: bold;
                        }
                        </style>"""

#: navigation bar to navigate to different modules of DAD
st.markdown(select_box_custom_css, unsafe_allow_html=True)
all_currencies = {'AFN - Afghan Afghani': 'AFN',
                  'ALL - Albanian Lek': 'ALL',
                  'AMD - Armenian Dram': 'AMD',
                  'AOA - Angolan Kwanza': 'AOA',
                  'ARS - Argentine Peso': 'ARS',
                  'AUD - Australian Dollar': 'AUD',
                  'AWG - Aruban Florin': 'AWG',
                  'AZN - Azerbaijani Manat': 'AZN',
                  'DZD - Algerian Dinar': 'DZD',
                  'BAM - Bosnia-Herzegovina Convertible Mark': 'BAM',
                  'BBD - Barbadian Dollar': 'BBD',
                  'BDT - Bangladeshi Taka': 'BDT',
                  'BGN - Bulgarian Lev': 'BGN',
                  'BHD - Bahraini Dinar': 'BHD',
                  'BIF - Burundian Franc': 'BIF',
                  'BMD - Bermudan Dollar': 'BMD',
                  'BND - Brunei Dollar': 'BND',
                  'BOB - Bolivian Boliviano': 'BOB',
                  'BRL - Brazilian Real': 'BRL',
                  'BSD - Bahamian Dollar': 'BSD',
                  'BTC - Bitcoin': 'BTC',
                  'BTN - Bhutanese Ngultrum': 'BTN',
                  'BWP - Botswanan Pula': 'BWP',
                  'BYR - Belarusian Ruble': 'BYR',
                  'BZD - Belize Dollar': 'BZD',
                  'GBP - British Pound Sterling': 'GBP',
                  'CAD - Canadian Dollar': 'CAD',
                  'CDF - Congolese Franc': 'CDF',
                  'CLF - Chilean Unit of Account (UF)': 'CLF',
                  'CLP - Chilean Peso': 'CLP',
                  'CNY - Chinese Yuan': 'CNY',
                  'COP - Colombian Peso': 'COP',
                  'CRC - Costa Rican Colón': 'CRC',
                  'CUC - Cuban Convertible Peso': 'CUC',
                  'CUP - Cuban Peso': 'CUP',
                  'CVE - Cape Verdean Escudo': 'CVE',
                  'CZK - Czech Republic Koruna': 'CZK',
                  'HRK - Croatian Kuna': 'HRK',
                  'KHR - Cambodian Riel': 'KHR',
                  'KMF - Comorian Franc': 'KMF',
                  'KYD - Cayman Islands Dollar': 'KYD',
                  'XAF - CFA Franc BEAC': 'XAF',
                  'XOF - CFA Franc BCEAO': 'XOF',
                  'XPF - CFP Franc': 'XPF',
                  'DJF - Djiboutian Franc': 'DJF',
                  'DKK - Danish Krone': 'DKK',
                  'DOP - Dominican Peso': 'DOP',
                  'EGP - Egyptian Pound': 'EGP',
                  'ERN - Eritrean Nakfa': 'ERN',
                  'ETB - Ethiopian Birr': 'ETB',
                  'EUR - Euro': 'EUR',
                  'XCD - East Caribbean Dollar': 'XCD',
                  'FJD - Fijian Dollar': 'FJD',
                  'FKP - Falkland Islands Pound': 'FKP',
                  'GEL - Georgian Lari': 'GEL',
                  'GGP - Guernsey Pound': 'GGP',
                  'GHS - Ghanaian Cedi': 'GHS',
                  'GIP - Gibraltar Pound': 'GIP',
                  'GMD - Gambian Dalasi': 'GMD',
                  'GNF - Guinean Franc': 'GNF',
                  'GTQ - Guatemalan Quetzal': 'GTQ',
                  'GYD - Guyanaese Dollar': 'GYD',
                  'XAU - Gold (troy ounce)': 'XAU',
                  'HKD - Hong Kong Dollar': 'HKD',
                  'HNL - Honduran Lempira': 'HNL',
                  'HTG - Haitian Gourde': 'HTG',
                  'HUF - Hungarian Forint': 'HUF',
                  'IDR - Indonesian Rupiah': 'IDR',
                  'ILS - Israeli New Sheqel': 'ILS',
                  'INR - Indian Rupee': 'INR',
                  'IQD - Iraqi Dinar': 'IQD',
                  'IRR - Iranian Rial': 'IRR',
                  'ISK - Icelandic Króna': 'ISK',
                  'JEP - Jersey Pound': 'JEP',
                  'JMD - Jamaican Dollar': 'JMD',
                  'JOD - Jordanian Dinar': 'JOD',
                  'JPY - Japanese Yen': 'JPY',
                  'KES - Kenyan Shilling': 'KES',
                  'KGS - Kyrgystani Som': 'KGS',
                  'KWD - Kuwaiti Dinar': 'KWD',
                  'KZT - Kazakhstani Tenge': 'KZT',
                  'LAK - Laotian Kip': 'LAK',
                  'LBP - Lebanese Pound': 'LBP',
                  'LRD - Liberian Dollar': 'LRD',
                  'LSL - Lesotho Loti': 'LSL',
                  'LTL - Lithuanian Litas': 'LTL',
                  'LVL - Latvian Lats': 'LVL',
                  'LYD - Libyan Dinar': 'LYD',
                  'IMP - Manx pound': 'IMP',
                  'MAD - Moroccan Dirham': 'MAD',
                  'MDL - Moldovan Leu': 'MDL',
                  'MGA - Malagasy Ariary': 'MGA',
                  'MKD - Macedonian Denar': 'MKD',
                  'MMK - Myanma Kyat': 'MMK',
                  'MNT - Mongolian Tugrik': 'MNT',
                  'MOP - Macanese Pataca': 'MOP',
                  'MRO - Mauritanian Ouguiya': 'MRO',
                  'MUR - Mauritian Rupee': 'MUR',
                  'MVR - Maldivian Rufiyaa': 'MVR',
                  'MWK - Malawian Kwacha': 'MWK',
                  'MXN - Mexican Peso': 'MXN',
                  'MYR - Malaysian Ringgit': 'MYR',
                  'MZN - Mozambican Metical': 'MZN',
                  'ANG - Netherlands Antillean Guilder': 'ANG',
                  'BYN - New Belarusian Ruble': 'BYN',
                  'KPW - North Korean Won': 'KPW',
                  'NAD - Namibian Dollar': 'NAD',
                  'NGN - Nigerian Naira': 'NGN',
                  'NIO - Nicaraguan Córdoba': 'NIO',
                  'NOK - Norwegian Krone': 'NOK',
                  'NPR - Nepalese Rupee': 'NPR',
                  'NZD - New Zealand Dollar': 'NZD',
                  'TWD - New Taiwan Dollar': 'TWD',
                  'OMR - Omani Rial': 'OMR',
                  'PAB - Panamanian Balboa': 'PAB',
                  'PEN - Peruvian Nuevo Sol': 'PEN',
                  'PGK - Papua New Guinean Kina': 'PGK',
                  'PHP - Philippine Peso': 'PHP',
                  'PKR - Pakistani Rupee': 'PKR',
                  'PLN - Polish Zloty': 'PLN',
                  'PYG - Paraguayan Guarani': 'PYG',
                  'QAR - Qatari Rial': 'QAR',
                  'RON - Romanian Leu': 'RON',
                  'RUB - Russian Ruble': 'RUB',
                  'RWF - Rwandan Franc': 'RWF',
                  'CHF - Swiss Franc': 'CHF',
                  'KRW - South Korean Won': 'KRW',
                  'LKR - Sri Lankan Rupee': 'LKR',
                  'RSD - Serbian Dinar': 'RSD',
                  'SAR - Saudi Riyal': 'SAR',
                  'SBD - Solomon Islands Dollar': 'SBD',
                  'SCR - Seychellois Rupee': 'SCR',
                  'SDG - Sudanese Pound': 'SDG',
                  'SEK - Swedish Krona': 'SEK',
                  'SGD - Singapore Dollar': 'SGD',
                  'SHP - Saint Helena Pound': 'SHP',
                  'SLL - Sierra Leonean Leone': 'SLL',
                  'SOS - Somali Shilling': 'SOS',
                  'SRD - Surinamese Dollar': 'SRD',
                  'STD - São Tomé and Príncipe Dobra': 'STD',
                  'SVC - Salvadoran Colón': 'SVC',
                  'SYP - Syrian Pound': 'SYP',
                  'SZL - Swazi Lilangeni': 'SZL',
                  'WST - Samoan Tala': 'WST',
                  'XAG - Silver (troy ounce)': 'XAG',
                  'XDR - Special Drawing Rights': 'XDR',
                  'ZAR - South African Rand': 'ZAR',
                  'THB - Thai Baht': 'THB',
                  'TJS - Tajikistani Somoni': 'TJS',
                  'TMT - Turkmenistani Manat': 'TMT',
                  'TND - Tunisian Dinar': 'TND',
                  'TOP - Tongan Paʻanga': 'TOP',
                  'TRY - Turkish Lira': 'TRY',
                  'TTD - Trinidad and Tobago Dollar': 'TTD',
                  'TZS - Tanzanian Shilling': 'TZS',
                  'AED - United Arab Emirates Dirham': 'AED',
                  'UAH - Ukrainian Hryvnia': 'UAH',
                  'UGX - Ugandan Shilling': 'UGX',
                  'USD - United States Dollar': 'USD',
                  'UYU - Uruguayan Peso': 'UYU',
                  'UZS - Uzbekistan Som': 'UZS',
                  'VEF - Venezuelan Bolívar Fuerte': 'VEF',
                  'VND - Vietnamese Dong': 'VND',
                  'VUV - Vanuatu Vatu': 'VUV',
                  'YER - Yemeni Rial': 'YER',
                  'ZMK - Zambian Kwacha (pre-2013)': 'ZMK',
                  'ZMW - Zambian Kwacha': 'ZMW',
                  'ZWL - Zimbabwean Dollar': 'ZWL'}
with tabs[1]:
    st.empty()
    st.session_state.target_currency = st.selectbox(label='Select the Target Currency', options=all_currencies.keys(),
                                                    index=None, placeholder='Target Currency')
    st.session_state.base_currency = st.multiselect(label='Select the Base Currency', options=all_currencies.keys())
    st.session_state.start_date = st.date_input(label='Select the Start Date', key='start')
    st.session_state.end_date = st.date_input(label='Select the End Date', key='end')
    st.session_state.conversion_type = st.selectbox("Select the Conversion Rate Type",
                                                    options=['Average', 'Daily', 'Monthly'],
                                                    index=0)
    if st.button('Get Conversion Rates'):
        if st.session_state.target_currency is None or \
                st.session_state.base_currency is None or \
                st.session_state.start_date is None or \
                st.session_state.end_date is None or \
                st.session_state.conversion_type is None:
            st.error('Provide all the Details')
        else:
            if (st.session_state.end_date - st.session_state.start_date).days > 365:
                st.error("Maximum 1 year time period can be selected")
            else:
                calculate_currency()

with tabs[0]:
    with tabs[0]:
        st.subheader("Read the Below Instructions:")
        st.markdown("""
     Welcome to the **Currency Conversion Rate Tool**! This tool helps you fetch the daily and average conversion rates for multiple currencies over a specified date range. Follow these steps to get started:

     ### Instructions:
     1. **Target Currency Selection**:
        - Use the dropdown menu to select the target currency for which you want to calculate conversion rates.
        - Example: Select **USD - United States Dollar** as the target currency.

     2. **Base Currency Selection**:
        - Choose one or more base currencies from the multi-select box.
        - Example: Select currencies like **EUR - Euro**, **GBP - British Pound Sterling**, etc.

     3. **Date Range Selection**:
        - Use the date picker to specify the start and end dates for your query.
        - We can select a Maximum Range of 1 Year.
        - Ensure the date range is valid (the end date must not be earlier than the start date).

     4. **Fetch Conversion Rates**:
        - Click the **Get Conversion Rate** button to start the calculation process.
        - Wait a moment while the rates are fetched and processed.

     ### Output:
     - The tool will save the conversion rates in a CSV file with the following naming convention:
       `TargetCurrency_Currency_Rate_StartDate_EndDate_Time.csv`

     ### Notes:
     - Ensure your internet connection is active for the tool to fetch live data.
     - Check that your API key is valid and has sufficient requests available.
     - If you encounter an error, recheck the input details and try again.

     ### Example:
     - **Target Currency**: USD - United States Dollar
     - **Base Currencies**: EUR, GBP, INR
     - **Date Range**: 2025-01-01 to 2025-01-31
     - Output File: `USD_Currency_Rate_2025-01-01_2025-01-31_TimeStamp.csv`

     Happy Currency Tracking!
     """, unsafe_allow_html=True)
