"transactions_by_address": ""https://api.blockchair.com/bitcoin/transactions?q=address:{address}&limit=10&offset=0&no_totals=true&no_"",



Infinitable endpoints (SQL-like queries)
These endpoints allow you to filter, sort, and aggregate blockchain data. The output is database rows. Unlike dashboard and raw endpoints, all infinitable endpoints listed in this section can be considered as just one endpoint as it has the same options and the same output structure across different blockchains and entities. Here it is: https://api.blockchair.com/{:table}{:query}.

Just don't ask why do we call that infinitables… Infinite tables? Maybe.

List of tables ({:table}) our engine supports:

{:btc_chain}/blocks
{:btc_chain}/transactions
{:btc_chain}/mempool/transactions
{:btc_chain}/outputs
{:btc_chain}/mempool/outputs
{:btc_chain}/addresses
{:eth_chain}/blocks
{:eth_chain}/uncles
{:eth_chain}/transactions
{:eth_chain}/mempool/transactions
{:eth_chain}/calls
{:xin_chain}/raw/snapshots
{:xin_chain}/raw/mintings
{:xin_chain}/raw/nodes
bitcoin/omni/properties
ethereum/erc-20/tokens
ethereum/erc-20/transactions
Where:

{:btc_chain} can be one of these: bitcoin, bitcoin-cash, litecoin, bitcoin-sv, dogecoin, dash, groestlcoin, zcash, ecash, or bitcoin/testnet
{:eth_chain} can be only ethereum
{:xin_chain} can be only mixin
Note on mempool tables: to speed up some requests, our architecture have separate tables ({:chain}/mempool/{:entity}) for unconfirmed transactions. Unlike with dashboard endpoints which search entities like transactions in both the blockchain and the mempool, infinitable endpoints don't do that.

The {:query} is optional; in case it's not included in the request, the default sorting applied to the table (for most of the tables it's descending by some id) and the 10 top results are returned.

Here are some example queries without using {:query}:

https://api.blockchair.com/bitcoin/blocks
https://api.blockchair.com/bitcoin-cash/mempool/transactions
The output skeleton is the following:

{
  "data": [
    {
      ... // row 1 data
    },
    ...
    {
      ... // row 10 data
    },    
  ],
  "context": {
    "limit": 10, // the default limit of 10 is applied
    "offset": 0, // no offset has been set
    "rows": 10, // the response contains 10 rows
    "total_rows": N, // but there are N rows in the table matching {:query} (total number of rows if it's not set)
    "state": S, // the latest block number on the blockchain
    ...
  }
}
Further documentation sections describe fields returned for different tables. Some of the dashboard endpoints are using the same fields as well.

How to build a query

The process is somewhat similar to constructing an SQL query, but there are less possibilities of course.

Here are the possible options:

Setting filters — the ?q= section — allows you to set a number of filters (SQL "WHERE")
Setting sortings — the ?s= section — allows you to sort the table (SQL "ORDER BY ")
Setting the limit — the ?limit= section — limits the number of output results (SQL "LIMIT")
Setting the offset — the ?offset= section — offsets the result set (SQL "OFFSET")
Aggregating data — the ?a= sections — allows to group by some columns and calculate using function (SQL "GROUP BY" and functions such as count, max, etc.)
The table (SQL "FROM") is set in the {:table} section of the API request
The order of applying various sections is irrelevant.

A quick example: https://api.blockchair.com/bitcoin/blocks?q=time(2019-01),guessed_miner(AntPool)&s=size(desc)&limit=1. This request:

Makes a query to the bitcoin/blocks table
Filters the table by time (finds all blocks mined in January 2019) and miner (AntPool)
Sorts the table by block size descending
Limits the number of results to 1
What this example does is finding the largest block mined by AntPool in January 2019.

Another example using aggregation: https://api.blockchair.com/bitcoin/blocks?q=time(2019-01-01..2019-01-31)&a=guessed_miner,count()&s=count()(desc). This request:

As the previous one, makes a query to the bitcoin/blocks table
Filters the table by time (in a bit different way, but it's an invariant of time(2019-01))
Groups the table by miner, and calculating the number of rows for each miner using the count() function
Sorts the result set by the number of blocks each miner has found
The ?q= section (filters)

You can use filters as follows: ?q=field(expression)[,field(expression)]..., where field is the column which is going to be filtered, and expression is a filtering expression. These are possilble filtering expressions:

equals — equality — example: https://api.blockchair.com/bitcoin/blocks?q=id(0) finds information about block 0
left.. — non-strict inequality — example: https://api.blockchair.com/bitcoin/blocks?q=id(1..) finds information about block 1 and above
left... — strict inequality — example: https://api.blockchair.com/bitcoin/blocks?q=id(1...) finds information about block 2 and above
..right — non-strict inequality — example: https://api.blockchair.com/bitcoin/blocks?q=id(..1) finds information about blocks 0 and 1
...right — strict inequality — example: https://api.blockchair.com/ bitcoin/blocks?q=id(...1) finds information only about block 0
left..right — non-strict inequality — example: https://api.blockchair.com/bitcoin/blocks?q=id(1..3) finds information about blocks 1, 2 and 3
left...right — strict inequality — example: https://api.blockchair.com/bitcoin/blocks?q=id(1...3) finds information about block 2 only
~like — occurrence in a string (SQL LIKE '%str%' operator) — example: https://api.blockchair.com/bitcoin/blocks?q=coinbase_data_bin(~hello) finds all blocks which contain hello in coinbase_data_bin
^like — occurrence at the beginning of a string (SQL LIKE 'str%' operator, also further mentioned as the STARTS WITH operator) — example: https://api.blockchair.com/bitcoin/blocks?q=coinbase_data_hex(^00) finds all blocks for which coinbase_data_hex begins with 00
For timestamp type fields, values can be specified in the following formats:

YYYY-MM-DD HH:ii:ss
YYYY-MM-DD (converted to the YYYY-MM-DD 00:00:00..YYYY-MM-DD 23:59:59 range)
YYYY-MM (converted to the YYYY-MM-01 00:00:00..YYYY-MM-31 23:59:59 range)
Inequalities are also supported for timestamps, the left and right values must be in the same format, e.g.: https://api.blockchair.com/bitcoin/blocks?q=time(2009-01-03..2009-01-31).

Ordinarilly if there's time column in the table, there should also be date, but there won't be possible to search over the date column directly, but you can search by date using the time column as follows: ?q=time(YYYY-MM-DD)

If the left value in an inequality is larger than the right, they switch places.

If you want to list several filters, you need to separate them using commas like this: https://api.blockchair.com/bitcoin/blocks?q=id(500000..),coinbase_data_bin(~hello)

We're currently testing support for NOT and OR operators (this is an alpha test feature, so we don't guarantee there won't be sudden changes):

The NOT operator is added before the expression for it to be inverted, e.g., https://api.blockchair.com/bitcoin/blocks?q=not,id(1..) returns the block 0
The OR operator can be put between two expressions and takes precedence (like it's when two expressions around OR are wrapped in parentheses), e.g., https://api.blockchair.com/bitcoin/blocks?q=id(1),or,id(2) returns information about blocks 1 and 2.
Maximum guaranteed supported number of filters in one query: 5.

The ?s= section (sortings)

Sorting can be used as follows: ?s=field(direction)[,field(direction)]..., where direction can be either asc for sorting in ascending order, or desc for sorting in descending order.

Here's a basic example: https://api.blockchair.com/bitcoin/blocks?s=id(asc) — sorts blocks by id ascending

If you need to apply several sortings, you can list them separating with commas. The maximum guaranteed number of sortings is 2.

The ?limit= section (limit)

Limit is used like this: ?limit=N, where N is a natural number from 1 to 100. The default is 10. context.limit takes the value of the set limit. In some cases (when using some specific "increased efficiency" filters described below) LIMIT may be ignored, and in such cases the API returns the entire result set, and context.limit will be set to NULL.

A basic example: https://api.blockchair.com/bitcoin/blocks?limit=1 — returns the latest block data (as the default sorting for this table is by block height descending)

Note that increasing the limit leads to an increase in the request cost (see the formula below).

The ?offset= section (offset)

Offset can be used as a paginator, e.g., ?offset=10 returns the next 10 rows. context.offset takes the value of the set offset. The maximum value is 10000. If you need just the last page, it's easier and quicker to change the direction of the sorting to the opposite.

Important: while iterating through the results, it is quite likely that the number of rows in the database will increase because new blocks had found while you were paginating. To avoid that, you may, for example, add an additional condition that limits the block id to the value obtained in context.state in the first query.

Here's an example. Suppose we would like to receive all the latest transactions from the Bitcoin blockchain with amount more than $1M USD. The following request should be perfomed for this:

https://api.blockchair.com/bitcoin/transactions?q=output_total_usd(10000000..)&s=id(desc)
Now, the script with this request to the API for some reason did not work for a while, or a huge amount of transactions worth more than $1 million appeared. With the standard limit of 10 results, the script skipped some transactions. Then firstly we should make the same request once again:

https://api.blockchair.com/bitcoin/transactions?q=output_total_usd(10000000..)&s=id(desc)
From the response we put context.state in a variable {:state}, and further to obtain next results we apply offset and set a filter to "fix" the blockchain state:

https://api.blockchair.com/bitcoin/transactions?q=output_total_usd(10000000..),block_id(..{:state})&s=id(desc)&offset=10
Next we increase the offset value until getting a data set with the transaction that we already knew about.

The ?a= section (data aggregation)

Warning: data aggregation is currently in beta stage on our platform.

To use aggregation, put the fields by which you'd like to group by (zero, one, or several), and fields (at least one) which you'd like to calculate using some aggregate function under the ?a= section. You can also sort the results by one of the fields included in the ?a= section (asc or desc) using the ?s= section, and apply additional filters using the ?q= section.

Let's start with some examples:

https://api.blockchair.com/bitcoin/blocks?a=year,count() — get the total number of Bitcoin blocks by year
https://api.blockchair.com/bitcoin/transactions?a=month,median(fee_usd) — get the median Bitcoin transaction fees by month
https://api.blockchair.com/ethereum/blocks?a=miner,sum(generation)&s=sum(generation)(desc) — get the list of Ethereum miners (except uncle miners) and sort it by the total amount of coins minted
https://api.blockchair.com/bitcoin-cash/blocks?a=sum(fee_total_usd)&q=id(478559..) — calculate how much miners have collected in fees since the fork
In case the table you're aggregating over has a time column, it's always possible to group by the following virtual columns:

date
week (yields YYYY-MM-DD corresponding to Mondays)
month (yields YYYY-MM )
year (yields YYYY )
Supported functions:

avg({:field})
median({:field})
min({:field})
max({:field})
sum({:field})
count()
There are also two special functions:

price({:ticker1}_{:ticker2})— yields the price; works only if you group by date (or one of: week, month, year). For example, it makes it possible to build a chart showing correlation between price and transaction count: https://api.blockchair.com/bitcoin/blocks?a=month,sum(transaction_count),price(btc_usd). Supported tickers: usd, btc, bch, eth, ltc, bsv, doge, dash, grs
f({:expression}) where {:expression} is {:function_1}{:operator}{:function_2}, where {:function_1} and {:function_2} are the supported functions from the above list, and {:operator} is one of the following: +, -, /, * (basic math operators). It's useful to calculate percentages. Example: https://api.blockchair.com/bitcoin/blocks?a=date,f(sum(witness_count)/sum(transaction_count))&q=time(2017-08-24..) — calculates SegWit adoption (by dividing the SegWit transaction count by the total transaction count)
There's also a special ?aq= section which have the following format: ?aq={:i}:{:j} — it applies ith filter to jth function (special functions don't count); after that ith filter has no effect on filtering the table. It's possible to have multiple conditions by separating them with a ;. Here's an example: https://api.blockchair.com/bitcoin/outputs?a=date,f(count()/count())&q=type(nulldata),time(2019-01)&aq=0:0 — calculates the percentage of nulldata outputs in January 2019 by day. The 0th condition (type(nulldata)) is applied to the 0th function (count()) and removed afterwards.

If you use the ?a= section, the default limit is 10000 instead of 10.

It's possible to export aggregated data to TSV or CSV format using &export=tsv or &export=csv accordingly. Example: https://api.blockchair.com/bitcoin/transactions?a=date,avg(fee_usd)&q=time(2019-01-01..2019-04-01)&export=tsv. Please note that data export is only available for aggregated data. If you need to export the whole table or its part, please use Database dumps.

Warning: the f({:expression}) special function, the ?aq= section, and TSV/CSV export are currently in alpha stage on our platform. Special function price({:ticker1}_{:ticker2}) can't be used within special function f({:expression}). There are some known issues when sorting if f({:expression}) is present. There are some known issues when applying the ?aq= section to inequality filters.

Fun example

The following requests return the same result:

https://api.blockchair.com/bitcoin/blocks?a=sum(reward)
https://api.blockchair.com/bitcoin/transactions?a=sum(output_total)&q=is_coinbase(true)
https://api.blockchair.com/bitcoin/outputs?a=sum(value)&q=is_from_coinbase(true)
Export data to TSV or CSV

Please use our Database dumps feature instead of the API (see https://blockchair.com/dumps for documentation)